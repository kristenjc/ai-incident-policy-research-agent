"""AI Incident & Policy Research: a deep research agent over the AI Incident Database and AGORA.

Lead -> (Incident Researcher, Trend Analyst, Policy Researcher in parallel) -> Writer -> citation check.
    uv run app.py      then open http://localhost:8000
"""

import asyncio
import csv
import io
import json
import os
import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import uvicorn
from agents import Agent, ModelSettings, RunContextWrapper, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request
from fastapi.responses import FileResponse, Response, StreamingResponse

import data_tools as dt
from context_panel import AgentContexts, PanelHooks, add_context_panel

load_dotenv(Path(__file__).parent / ".env")
set_tracing_disabled(True)

MODEL = LitellmModel(model=os.environ.get("LEAD_MODEL", "vertex_ai/gemini-3.5-flash"), api_key="unused")
RESEARCHER_MODEL = LitellmModel(model=os.environ.get("RESEARCHER_MODEL", "vertex_ai/gemini-3.5-flash-lite"), api_key="unused")
SETTINGS = ModelSettings(extra_args={"vertex_location": "global", "timeout": 90, "num_retries": 2})

MAX_RESEARCHERS = 6  # in all, per run. Prompts ask for restraint; code enforces it.
LEAD_TURNS = 10
RESEARCHER_TURNS = 8
RESEARCH_BUDGET_S = 200  # graders wait 5 minutes: past this, stop researching and write with what we have
TOOL_OUTPUT_CHARS = 4000  # per tool call in /chat's tool_calls

CITE = re.compile(r"\[(AIID|AGORA) #(\d+)\]")


@dataclass
class Research:
    """One run's state, shared by every agent and tool in it. The model never sees it."""

    hooks: "RecordingHooks"
    question: str = ""
    brief: dict | None = None
    clarification: dict | None = None
    researchers: int = 0
    findings: list[dict] = field(default_factory=list)  # {agent, role, task, text}
    seen: set[str] = field(default_factory=set)  # every "AIID #n" / "AGORA #n" a tool returned


# --- Hooks: the context panel, plus a record of every tool call with its agent ---


class RecordingHooks(PanelHooks):
    def __init__(self, contexts: AgentContexts, emit):
        super().__init__(contexts, emit)
        self.calls: list[dict] = []  # {agent, name, arguments, call_id, output}
        self._by_id: dict[str, dict] = {}

    async def on_llm_end(self, context, agent, response):
        await super().on_llm_end(context, agent, response)
        for item in response.output:
            if getattr(item, "type", None) == "function_call":
                try:
                    args = json.loads(item.arguments or "{}")
                except ValueError:
                    args = item.arguments
                call = {"agent": agent.name, "name": item.name, "arguments": args, "call_id": item.call_id, "output": None}
                self.calls.append(call)
                self._by_id[item.call_id] = call
                self.emit({"type": "tool", "agent": agent.name, "name": item.name, "arguments": args, "call_id": item.call_id})

    async def on_tool_start(self, context, agent, tool):
        pass  # the "tool" event above already says it, with arguments

    async def on_tool_end(self, context, agent, tool, result):
        call_id = getattr(context, "tool_call_id", None)
        if call_id in self._by_id and not self._by_id[call_id]["output"]:
            self.record_output(call_id, str(result))

    def record_output(self, call_id: str | None, output: str) -> None:
        if call_id in self._by_id:
            call = self._by_id[call_id]
            call["output"] = output
            self.emit({"type": "tool_result", "agent": call["agent"], "call_id": call_id, "summary": summarize(call["name"], output)})

    def outputs(self, name: str) -> list[dict]:
        """Parsed outputs of every call to a tool, oldest first."""
        out = []
        for c in self.calls:
            if c["name"] == name and c["output"]:
                try:
                    out.append(json.loads(c["output"]))
                except ValueError:
                    pass
        return out


def summarize(name: str, output: str) -> str:
    """One line about a tool's result, for the agent cards on the page."""
    try:
        o = json.loads(output)
    except ValueError:
        line = output.strip().splitlines()[0] if output.strip() else "(empty)"
        return line if len(line) <= 90 else line[:87] + "…"
    if not isinstance(o, dict):
        return "done"
    if "error" in o:
        return "error: " + str(o["error"])[:80]
    if name == "describe_data":
        return f"{o['incidents']['count']} incidents, {o['policies']['count']} policy documents"
    if name == "set_brief":
        b = o.get("brief", {})
        return "scope: " + (", ".join(b.get("use_cases") or []) or "whole dataset")
    if name in ("search_incidents",):
        return f"{o['matched']} incidents matched"
    if name == "count_incidents":
        return f"{o['unique_incidents']} incidents in {len(o['rows'])} groups"
    if name == "compare_periods":
        return f"{o['period_a']}: {o['total_a']} → {o['period_b']}: {o['total_b']} incidents"
    if name == "search_policies":
        st = ", ".join(f"{v} {k.lower()}" for k, v in o.get("status_among_matches", {}).items())
        return f"{o['matched']} documents" + (f" ({st})" if st else "")
    if name == "search_policy_text":
        return f"{len(o['documents'])} documents, best section each"
    if name == "coverage_matrix":
        gaps = [r["risk_domain"] for r in o["rows"] if r["coverage"] != "enacted"]
        return f"{o['policy_docs_mentioning_use_case']} policy docs; " + (f"gaps: {', '.join(gaps)}" if gaps else "every risk domain has enacted policy")
    if name == "get_incident":
        return str(o.get("title", ""))[:90]
    if name == "get_policy":
        return f"{str(o.get('name', ''))[:70]} ({o.get('status')})"
    if name == "policy_keywords":
        return f"{len(o.get('keywords', []))} search phrases"
    if name == "risks_to_policy_tags":
        return ", ".join(o.get("agora_tags", []))[:90]
    return "done"


def _call(ctx: RunContextWrapper[Research], fn, **kwargs) -> str:
    """Run a data tool, remember every ID it returned, and give the model JSON it can reason about."""
    try:
        result = fn(**{k: v for k, v in kwargs.items() if v is not None})
    except Exception as e:  # the model cannot see an exception: tell it what went wrong
        result = {"error": f"{type(e).__name__}: {e}"}
    text = json.dumps(result, ensure_ascii=False, default=str)
    for kind, n in CITE.findall(text):
        ctx.context.seen.add(f"{kind} #{n}")
    ctx.context.hooks.record_output(getattr(ctx, "tool_call_id", None), text)
    return text


# --- Tools: incidents ---


@function_tool
def search_incidents(
    ctx: RunContextWrapper[Research],
    use_case: str | None = None,
    risk_domain: str | None = None,
    risk_subdomain: str | None = None,
    keyword: str | None = None,
    intent: str | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    include_secondary: bool = False,
    limit: int = 12,
) -> str:
    """Find AI incidents. Returns how many match, the most common risk subdomains among them, and example incidents.

    Args:
        use_case: A use case name from describe_data, e.g. 'Hiring and employment'.
        risk_domain: An MIT risk domain, e.g. 'Discrimination and Toxicity'.
        risk_subdomain: An MIT risk subdomain, e.g. 'Fraud, scams, and targeted manipulation'.
        keyword: Free-text search over titles and descriptions, e.g. 'resume screening gender'.
        intent: 'Intentional' (misuse) or 'Unintentional' (failure).
        year_from: First year to include.
        year_to: Last year to include.
        include_secondary: Also match incidents whose secondary use case is use_case.
        limit: Examples to return, at most 25.
    """
    return _call(ctx, dt.search_incidents, use_case=use_case, risk_domain=risk_domain, risk_subdomain=risk_subdomain,
                 keyword=keyword, intent=intent, year_from=year_from, year_to=year_to,
                 include_secondary=include_secondary, limit=limit)


@function_tool
def get_incident(ctx: RunContextWrapper[Research], incident_id: int) -> str:
    """Everything recorded about one incident, including editor notes and harm details when classified.

    Args:
        incident_id: The AIID incident number.
    """
    return _call(ctx, dt.get_incident, incident_id=incident_id)


@function_tool
def count_incidents(
    ctx: RunContextWrapper[Research],
    group_by: Literal["year", "risk_domain", "risk_subdomain", "intent", "responsible_entity", "timing", "use_case", "deployer"] = "year",
    split_by: Literal["risk_domain", "risk_subdomain", "intent", "responsible_entity", "use_case"] | None = None,
    use_case: str | None = None,
    risk_domain: str | None = None,
    keyword: str | None = None,
    intent: str | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    include_secondary: bool = False,
) -> str:
    """Count unique incidents, grouped (and optionally split, for a stacked chart). Returns counts, shares and caveats.

    Args:
        group_by: What to count by.
        split_by: A second breakdown within each group, e.g. group_by='year', split_by='risk_domain'.
        use_case: Limit to one use case.
        risk_domain: Limit to one MIT risk domain.
        keyword: Limit to incidents matching this text.
        intent: 'Intentional' or 'Unintentional'.
        year_from: First year to include.
        year_to: Last year to include.
        include_secondary: Also count incidents whose secondary use case is use_case.
    """
    return _call(ctx, dt.count_incidents, group_by=group_by, split_by=split_by, use_case=use_case,
                 risk_domain=risk_domain, keyword=keyword, intent=intent, year_from=year_from, year_to=year_to,
                 include_secondary=include_secondary)


@function_tool
def compare_periods(
    ctx: RunContextWrapper[Research],
    period_a: str,
    period_b: str,
    group_by: Literal["risk_domain", "risk_subdomain", "intent", "responsible_entity", "use_case"] = "risk_domain",
    use_case: str | None = None,
    risk_domain: str | None = None,
) -> str:
    """Compare the mix of incidents in two periods: counts, shares within each period, and the change in share.

    Args:
        period_a: Earlier period, e.g. '2019-2021'.
        period_b: Later period, e.g. '2023-2025'.
        group_by: What to compare.
        use_case: Limit to one use case.
        risk_domain: Limit to one MIT risk domain.
    """
    return _call(ctx, dt.compare_periods, period_a=period_a, period_b=period_b, group_by=group_by,
                 use_case=use_case, risk_domain=risk_domain)


# --- Tools: policies ---


@function_tool
def search_policies(
    ctx: RunContextWrapper[Research],
    query: str | None = None,
    tags: list[str] | None = None,
    status: Literal["Enacted", "Proposed", "Defunct"] | None = None,
    jurisdiction: str | None = None,
    authority: str | None = None,
    applies_private: bool | None = None,
    proposed_from: int | None = None,
    limit: int = 10,
) -> str:
    """Find AGORA policy documents by their summaries and tags. Returns status, dates, what they require.

    Args:
        query: Words to match against names and summaries, e.g. 'deepfake election'.
        tags: AGORA tags the document must carry, e.g. ['Bias'] or ['Disclosure'].
        status: 'Enacted' (in force), 'Proposed', or 'Defunct' (failed or expired).
        jurisdiction: 'United States', 'China', 'Multinational', 'Other countries'.
        authority: Part of the issuing body's name, e.g. 'California' or 'Congress'.
        applies_private: True for documents that primarily apply to the private sector.
        proposed_from: Only documents proposed in or after this year.
        limit: Documents to return, at most 20.
    """
    return _call(ctx, dt.search_policies, query=query, tags=tags, status=status, jurisdiction=jurisdiction,
                 authority=authority, applies_private=applies_private, proposed_from=proposed_from, limit=limit)


@function_tool
def search_policy_text(
    ctx: RunContextWrapper[Research],
    query: str,
    status: Literal["Enacted", "Proposed", "Defunct"] | None = None,
    jurisdiction: str | None = None,
    limit: int = 8,
) -> str:
    """Search the full text of policy sections. Best for specific provisions, e.g. 'bias audit automated employment'.

    Args:
        query: What the provision is about.
        status: 'Enacted', 'Proposed', or 'Defunct'.
        jurisdiction: 'United States', 'China', 'Multinational', 'Other countries'.
        limit: Documents to return, at most 15.
    """
    return _call(ctx, dt.search_policy_text, query=query, status=status, jurisdiction=jurisdiction, limit=limit)


@function_tool
def get_policy(ctx: RunContextWrapper[Research], agora_id: int, query: str | None = None) -> str:
    """One policy document: long summary, tags, and its sections most relevant to query.

    Args:
        agora_id: The AGORA document number.
        query: What you want from it, to pick the relevant sections.
    """
    return _call(ctx, dt.get_policy, agora_id=agora_id, query=query)


@function_tool
def policy_keywords(ctx: RunContextWrapper[Research], use_case: str) -> str:
    """Hand-written search phrases for finding policies about a use case.

    Args:
        use_case: A use case name from describe_data.
    """
    return _call(ctx, dt.policy_keywords, use_case=use_case)


@function_tool
def risks_to_policy_tags(ctx: RunContextWrapper[Research], risk_domain: str) -> str:
    """The AGORA tags that correspond to an MIT risk domain (a hand-made crosswalk).

    Args:
        risk_domain: An MIT risk domain, e.g. 'Privacy & Security'.
    """
    return _call(ctx, dt.risks_to_policy_tags, risk_domain=risk_domain)


@function_tool
def coverage_matrix(
    ctx: RunContextWrapper[Research],
    use_case: str | None = None,
    jurisdiction: str | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
) -> str:
    """For each risk domain with incidents in this use case: incident count, and how many policies about the use
    case address that risk, by status. Shows where incidents have no enacted policy.

    Args:
        use_case: A use case name, or none for the whole dataset.
        jurisdiction: Limit policies to one jurisdiction, e.g. 'United States'.
        year_from: First incident year.
        year_to: Last incident year.
    """
    return _call(ctx, dt.coverage_matrix, use_case=use_case, jurisdiction=jurisdiction, year_from=year_from,
                 year_to=year_to)


# --- Tools: the Lead's ---


@function_tool
def describe_data(ctx: RunContextWrapper[Research]) -> str:
    """What the datasets hold: use cases with incident counts, years, risk domains, policy jurisdictions and
    statuses, and caveats. Call this first."""
    return _call(ctx, dt.describe_data)


@function_tool
def ask_user(ctx: RunContextWrapper[Research], question: str, options: list[str]) -> str:
    """Ask the user to clarify before researching. The run stops after this: reply DONE next.

    Args:
        question: One short question.
        options: 2 to 5 short answers the user can click, grounded in what the data holds.
    """
    ctx.context.clarification = {"question": question, "options": options[:5]}
    return "Question sent to the user. Reply DONE."


@function_tool
def set_brief(
    ctx: RunContextWrapper[Research],
    mode: Literal["use_case", "overview"],
    focus: str,
    use_cases: list[str] | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    jurisdiction: str | None = None,
) -> str:
    """Record the scope every researcher will work within. Call once, before research.

    Args:
        mode: 'use_case' to investigate specific use cases, 'overview' for patterns across the whole dataset.
        focus: One sentence: what the user wants to learn.
        use_cases: Use case names from describe_data (mode 'use_case').
        year_from: First incident year, if the user gave one.
        year_to: Last incident year, if the user gave one.
        jurisdiction: Policy jurisdiction, if the user gave one, e.g. 'United States'.
    """
    try:
        cases = [dt._match_name(u, dt.TAXONOMY.keys(), "use_case") for u in (use_cases or [])]
    except ValueError as e:
        return json.dumps({"error": str(e)})
    if mode == "use_case" and not cases:
        return json.dumps({"error": "mode 'use_case' needs at least one use case."})
    ctx.context.brief = {"mode": mode, "focus": focus, "use_cases": cases, "year_from": year_from,
                         "year_to": year_to, "jurisdiction": jurisdiction}
    ctx.context.hooks.emit({"type": "brief", "brief": ctx.context.brief})
    return json.dumps({"ok": True, "brief": ctx.context.brief})


# --- Researchers: three specialists, each in a fresh context ---

_RESEARCHER_RULES = """
Rules:
- Use only what your tools return. Never use outside knowledge about incidents, companies or laws.
- Cite every fact with the tag the tool gave it, exactly: [AIID #123] or [AGORA #456]. Numbers need no tag,
  but say which tool and filters they came from in a few words.
- If the data does not answer part of your task, say so in a final bullet that starts "Gap:".
- Reply with at most 10 bullets and nothing else."""

incident_researcher = Agent(
    name="Incident Researcher",
    instructions="""\
You find out what has gone wrong. Given a research brief and a task, identify the failure modes reported in the
AI Incident Database for that scope.

1. Call search_incidents with the brief's use case and years. Note how many matched and the subdomains among them.
2. For the 3 to 5 most common subdomains, search again with risk_subdomain (or a keyword) to get examples.
3. Read 2 or 3 incidents with get_incident when a detail matters (who was harmed, editor notes).
4. Report each failure mode as one bullet: what failed, how many incidents in that subdomain, and 2 or 3
   example incidents with their tags. Mention when examples are intentional misuse rather than a system failure.
   Mention medium or low use-case label confidence when it applies to an example.
""" + _RESEARCHER_RULES,
    model=RESEARCHER_MODEL,
    model_settings=SETTINGS,
    tools=[search_incidents, get_incident],
)

trend_analyst = Agent(
    name="Trend Analyst",
    instructions="""\
You find out how reported incidents changed over time. Given a research brief and a task:

1. Call count_incidents with group_by='year' and split_by='risk_domain' for the brief's scope. This one feeds the
   report's chart, so always make it.
2. Call compare_periods to compare an earlier and a later span of full years (e.g. 2019-2021 vs 2023-2025)
   by risk_domain or risk_subdomain, and by intent if relevant.
3. Report: the totals by period, the largest shifts in share (in percentage points), and whether failures are
   mostly intentional misuse or unintentional. Copy numbers exactly from the tool output.
Always state that the latest year is partial and that these are reported incidents, not rates. If fewer than
20 incidents match, say the counts are too small to call a trend.
""" + _RESEARCHER_RULES,
    model=RESEARCHER_MODEL,
    model_settings=SETTINGS,
    tools=[count_incidents, compare_periods],
)

policy_researcher = Agent(
    name="Policy Researcher",
    instructions="""\
You find out which policies address these risks, using AGORA. Given a research brief and a task:

1. Call coverage_matrix for the brief's use case and jurisdiction to see which risk domains have enacted policy.
2. Call policy_keywords for the use case, then search_policy_text with 2 or 3 of those phrases (one call each),
   and with status='Enacted' at least once.
3. Read the 2 to 4 most relevant documents with get_policy(query=...) to see what they actually require.
4. Report each relevant policy as one bullet: name, authority, status and date, what it requires (strategies,
   incentives such as fines), and which failure it addresses. Keep Enacted, Proposed and Defunct distinct:
   only Enacted documents are in force. End with which risks have no enacted policy in the data.
AGORA is mostly US documents and is not a complete record of AI law: say so if the brief asks about elsewhere.
""" + _RESEARCHER_RULES,
    model=RESEARCHER_MODEL,
    model_settings=SETTINGS,
    tools=[coverage_matrix, policy_keywords, search_policy_text, search_policies, get_policy, risks_to_policy_tags],
)

RESEARCHERS = {"incidents": incident_researcher, "trends": trend_analyst, "policy": policy_researcher}


@function_tool
async def research(ctx: RunContextWrapper[Research], role: Literal["incidents", "trends", "policy"], task: str) -> str:
    """Send a specialist researcher on one task, within the brief. Returns its cited findings.

    Args:
        role: 'incidents' (what failed, with examples), 'trends' (counts over time), or 'policy' (relevant policies).
        task: One specific thing to find out.
    """
    run = ctx.context
    if run.brief is None:
        return "Call set_brief first."
    if run.researchers >= MAX_RESEARCHERS:
        return "No researchers left. Reply DONE."
    run.researchers += 1
    same_role = sum(1 for f in run.findings if f["role"] == role) + 1
    base = RESEARCHERS[role]
    agent = base.clone(name=base.name if same_role == 1 else f"{base.name} {same_role}")
    prompt = f"Research brief: {json.dumps(run.brief)}\nQuestion from the user: {run.question}\nYour task: {task}"
    try:
        result = await Runner.run(agent, prompt, context=run, hooks=run.hooks, max_turns=RESEARCHER_TURNS)
        text = str(result.final_output)
    except Exception as e:
        text = f"Gap: this researcher stopped early ({type(e).__name__}). Its part of the question is not answered."
    run.findings.append({"agent": agent.name, "role": role, "task": task, "text": text})
    return text


lead = Agent(
    name="Lead",
    instructions=f"""\
You lead a research team that investigates reported AI failures (AI Incident Database) and the policies that
address them (AGORA). Users are product teams, governance practitioners and researchers.

1. Call describe_data.
2. Decide if the request is clear. Call ask_user instead of researching when:
   - it names no use case and does not ask about the dataset as a whole (e.g. "is AI dangerous?");
   - it could mean several use cases (e.g. "AI in cars": autonomous vehicles, or in-car voice assistants?);
   - it asks for something the data can't give as asked: incident rates or frequencies (AIID holds reported
     incidents only), or policies outside the US (AGORA is about 92% US). Offer what the data can do instead.
   Options must be things the data holds, e.g. use case names. After ask_user, reply DONE.
   Earlier turns of the conversation, if any, come first in the input: use the user's answers to them.
3. Call set_brief. Use mode 'overview' for questions about the whole dataset ("most common failures since 2020").
4. In ONE turn, call research three times so the researchers work in parallel: role 'incidents', role 'trends'
   and role 'policy', each with a task specific to the question.
5. Check the findings. Call research again, for just the missing part, when:
   - a researcher reports a Gap that another search could fill (e.g. no enacted policy found: try other terms);
   - the question asked something no researcher covered.
   At most 2 follow-up rounds, {MAX_RESEARCHERS} researchers in all.
6. When the question is covered, or a gap can't be filled from this data, reply DONE and nothing else.""",
    model=MODEL,
    model_settings=SETTINGS,
    tools=[describe_data, ask_user, set_brief, research],
)

writer = Agent(
    name="Writer",
    instructions="""\
Write a research report in markdown that answers the user's question, using only the findings you're given.

Structure, with these headings:
# <a specific title>
**Bottom line.** 3 or 4 sentences that answer the question directly.
## What has gone wrong
One bullet per failure mode: what failed, how often, and example incidents.
## How reporting has changed
Two to four sentences on the trend, then a line with only [[CHART]] on it. The chart shows exactly the CHART FACTS
you're given. Any count over time (totals, peak year, period totals, largest category) must come from CHART FACTS,
word for word in its numbers. You may add shares from the Trend Analyst (e.g. the share that was intentional) only
when its filters match the brief. Never describe a rise or fall that CHART FACTS don't show.
## Policies that address these risks
A markdown table: Policy | Authority | Status (date) | What it requires | Addresses. Enacted first.
Then a line with only [[COVERAGE]] on it, then one or two sentences on where incidents have no enacted policy.
## What this data can't tell you
Bullets: the limits that affect THIS answer (e.g. reported counts are not rates, partial latest year, AGORA is
mostly US, small counts, LLM-assigned use-case labels, hand-made risk crosswalk).

Rules:
- Keep every citation tag exactly as written in the findings: [AIID #123] or [AGORA #456]. Every sentence or table
  row that states a fact about an incident or policy ends with one. Never invent a tag or a number.
- Incidents are worldwide: AIID has no reliable location field. If the brief names a policy jurisdiction, say once
  that only the policies are limited to it.
- Keep Enacted, Proposed and Defunct distinct. Never call a proposed or defunct bill law.
- If the findings don't answer part of the question, say so in that section.
- Plain, specific sentences. No "pivotal", "landscape", "it is worth noting", "underscores".
- In overview mode, replace "What has gone wrong" with "The most common reported failures".""",
    model=MODEL,
    model_settings=SETTINGS,
)


# --- After the Writer: charts, coverage table, citations, all from tool output rather than the model ---


def _chart(brief: dict | None) -> dict | None:
    """Computed from the brief's scope, so the chart, its facts and the Writer's trend sentences agree."""
    if not brief:
        return None
    return dt.chart_for_scope(brief.get("use_cases") or None, brief.get("year_from"), brief.get("year_to"))


def scope_line(brief: dict | None) -> str:
    """Says plainly what was searched: incidents are worldwide, policies may be limited to one jurisdiction."""
    if not brief:
        return ""
    cases = ", ".join(brief.get("use_cases") or []) or "all use cases"
    years = f"{brief.get('year_from') or 'all years'}–{brief.get('year_to') or 'latest'}" if (brief.get("year_from") or brief.get("year_to")) else "all years"
    pol = brief.get("jurisdiction") or "all jurisdictions (about 92% US)"
    return f"*Scope · Incidents: {cases}, {years}, worldwide (AIID has no reliable location field) · Policies: {pol}*"


def _coverage(hooks: RecordingHooks) -> dict | None:
    out = [o for o in hooks.outputs("coverage_matrix") if o.get("rows")]
    return out[-1] if out else None


def _chart_table(chart: dict) -> str:
    rows = [f"| {r['year']}{' (partial)' if r['year'] == chart['partial_year'] else ''} | {r['incidents']} |" for r in chart["rows"]]
    facts = "\n".join(f"- {x}" for x in chart["facts"])
    return "| Year | Reported incidents |\n|---|---|\n" + "\n".join(rows) + "\n\n" + facts


def _coverage_table(cov: dict) -> str:
    head = "| Risk domain | Incidents | Enacted | Proposed | Defunct | Coverage |\n|---|---|---|---|---|---|\n"
    body = "\n".join(f"| {r['risk_domain']} | {r['incidents']} | {r['policies_enacted']} | {r['policies_proposed']} | "
                     f"{r['policies_defunct']} | {r['coverage']} |" for r in cov["rows"])
    return head + body + f"\n\n*Coverage method: {cov['method']}*"


def check_citations(markdown: str, seen: set[str]) -> tuple[str, dict]:
    """Every tag must name a real record that a tool returned during this run. Tags become links."""
    cited, verified, unverified, details = [], [], [], {}

    def link(m):
        kind, n = m.group(1), int(m.group(2))
        key = f"{kind} #{n}"
        cited.append(key)
        exists = (n in dt.INCIDENTS.index) if kind == "AIID" else (n in dt.DOCS.index)
        if exists and key in seen:
            verified.append(key)
            if kind == "AIID":
                r = dt.INCIDENTS.loc[n]
                details[key] = {"title": r["title"], "date": r["date"], "url": dt.AIID_URL.format(id=n)}
            else:
                r = dt.DOCS.loc[n]
                details[key] = {"title": r["name"], "status": r["status"], "date": dt._clean(r["status_date"]),
                                "url": dt.AGORA_URL.format(id=n)}
            return f"[{key}]({details[key]['url']})"
        unverified.append(key)
        return f"[{key} ⚠ unverified]"

    out = CITE.sub(link, markdown)
    stats = {"cited": len(set(cited)), "verified": len(set(verified)), "unverified": sorted(set(unverified)),
             "records": details}
    return out, stats


async def deep_research(question: str, history: list[dict], hooks: RecordingHooks) -> dict:
    run = Research(hooks=hooks, question=question)
    earlier = "".join(f"User: {h['user']}\nYou: {h['assistant']}\n\n" for h in history[-4:])
    prompt = (f"Earlier in this conversation:\n{earlier}" if earlier else "") + f"User's request: {question}"

    # 1. Research: clarify or plan, fan out, check for gaps. Capped in time so a grader never waits > 5 min.
    try:
        await asyncio.wait_for(Runner.run(lead, prompt, context=run, hooks=hooks, max_turns=LEAD_TURNS), RESEARCH_BUDGET_S)
    except asyncio.TimeoutError:
        hooks.activity("Lead", f"research time budget ({RESEARCH_BUDGET_S}s) used up: writing with the findings so far")
    except Exception as e:
        if not run.findings and not run.clarification:
            raise
        hooks.activity("Lead", f"stopped early ({type(e).__name__}): writing with the findings so far")

    if run.clarification and not run.findings:
        return {"kind": "clarification", "markdown": run.clarification["question"], **run.clarification}
    if not run.findings:
        return {"kind": "answer", "markdown": "The research team found nothing to report for this question.", "report": {}}

    # 2. Write: one call. The Writer sees the question, the brief and the findings, nothing else.
    chart, cov = _chart(run.brief), _coverage(hooks)
    findings = "\n\n---\n\n".join(f"## {f['agent']} — {f['task']}\n\n{f['text']}" for f in run.findings)
    extra = ""
    if chart:
        extra += "\n\nCHART FACTS (computed in code from the chart at [[CHART]]):\n" + "\n".join(f"- {x}" for x in chart["facts"])
    if cov:
        extra += "\n\nCoverage matrix (rendered at [[COVERAGE]]):\n" + _coverage_table(cov)
    written = await Runner.run(writer, f"Question: {question}\nBrief: {json.dumps(run.brief)}\n\nFindings:\n\n{findings}{extra}", hooks=hooks)
    markdown = str(written.final_output).strip()

    # 3. Check: citations against tool output; chart and coverage from tool output.
    markdown, citations = check_citations(markdown, run.seen)
    hooks.emit({"type": "activity", "agent": "Citation check",
                "text": f"{citations['verified']}/{citations['cited']} citations verified against tool output"})
    for slot in ("[[CHART]]", "[[COVERAGE]]"):
        if slot not in markdown:
            markdown += f"\n\n{slot}"
    scope = scope_line(run.brief)
    if scope:  # right under the title
        lines = markdown.split("\n", 1)
        markdown = f"{lines[0]}\n\n{scope}\n\n{lines[1] if len(lines) > 1 else ''}" if lines[0].startswith("# ") else f"{scope}\n\n{markdown}"
    plain = markdown.replace("[[CHART]]", _chart_table(chart) if chart else "").replace("[[COVERAGE]]", _coverage_table(cov) if cov else "")
    return {
        "kind": "answer",
        "markdown": plain,
        "report": {"markdown": markdown, "brief": run.brief, "chart": chart, "coverage": cov, "citations": citations,
                   "researchers": [{"agent": f["agent"], "task": f["task"]} for f in run.findings]},
    }


# --- FastAPI App ---

HERE = Path(__file__).parent
sessions: dict[str, AgentContexts] = {}  # run_id -> every agent's context, for the context panel
conversations: dict[str, list[dict]] = {}  # session_id -> [{user, assistant}], so clarifications carry over

app = FastAPI()
add_context_panel(app, sessions)


@app.get("/")
def index():
    return FileResponse(HERE / "index.html", headers={"Cache-Control": "no-cache"})


@app.get("/api/meta")
def meta():
    """What the front end shows before a run: use cases with counts, and the data's caveats."""
    d = dt.describe_data()
    return {"use_cases": {k: v["incidents"] for k, v in d["incidents"]["use_cases"].items()},
            "years": d["incidents"]["years"], "partial_year": dt.LATEST_YEAR,
            "incidents": d["incidents"]["count"], "policies": d["policies"]["count"],
            "policy_status": d["policies"]["status"], "jurisdictions": d["policies"]["jurisdictions"],
            "caveats": d["caveats"]}


def _scope_args(use_case: list[str] | None, year_from: int | None, year_to: int | None) -> dict:
    return {"use_cases": [u for u in (use_case or []) if u] or None, "year_from": year_from, "year_to": year_to}


@app.get("/api/counts")
def counts(use_case: str | None = None, year_from: int | None = None, year_to: int | None = None,
           jurisdiction: str | None = None):
    """Live counts for the question area: incidents in scope, and policy documents for a jurisdiction."""
    try:
        inc = dt._filter_incidents(use_case=use_case or None, year_from=year_from, year_to=year_to)
    except ValueError:
        inc = dt.INCIDENTS.iloc[0:0]
    docs = dt.DOCS if not jurisdiction else dt.DOCS[dt.DOCS["jurisdiction"] == jurisdiction]
    return {"incidents": int(inc["incident_id"].nunique()), "policies": int(len(docs)),
            "enacted": int((docs["status"] == "Enacted").sum())}


@app.get("/api/incidents")
def incidents(use_case: list[str] | None = Query(None), year_from: int | None = None, year_to: int | None = None,
              year: int | None = None, split_by: str | None = None, split_value: str | None = None,
              exclude: list[str] | None = Query(None), offset: int = 0, limit: int = 25):
    """The incidents behind a chart bar or table cell, 25 at a time, for the page's drawer."""
    return dt.list_incidents(**_scope_args(use_case, year_from, year_to), year=year, split_by=split_by,
                             split_value=split_value, exclude=exclude, offset=offset, limit=min(limit, 100))


@app.get("/api/incidents.csv")
def incidents_csv(use_case: list[str] | None = Query(None), year_from: int | None = None, year_to: int | None = None,
                  year: int | None = None, split_by: str | None = None, split_value: str | None = None,
                  exclude: list[str] | None = Query(None)):
    """Every incident behind the chart (or one bar), as CSV."""
    rows = dt.list_incidents(**_scope_args(use_case, year_from, year_to), year=year, split_by=split_by,
                             split_value=split_value, exclude=exclude, limit=None)["items"]
    buf = io.StringIO()
    if rows:
        w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return Response(buf.getvalue(), media_type="text/csv",
                    headers={"Content-Disposition": 'attachment; filename="incidents.csv"'})


def _start(session_id: str | None):
    session_id = session_id or str(uuid.uuid4())
    run_id = str(uuid.uuid4())
    sessions[run_id] = AgentContexts()
    return session_id, run_id


def _remember(session_id: str, question: str, result: dict) -> None:
    said = result["markdown"] if result["kind"] == "clarification" else "(wrote a report)"
    if result["kind"] == "clarification":
        said += " Options: " + "; ".join(result.get("options", []))
    conversations.setdefault(session_id, []).append({"user": question, "assistant": said})


@app.post("/chat")
async def chat(request: Request):
    """Project 1's shape: {message, session_id?} -> {answer, session_id, tool_calls[{agent, name, ...}]}."""
    body = await request.json()
    question = (body.get("message") or body.get("question") or "").strip()
    session_id, run_id = _start(body.get("session_id"))
    hooks = RecordingHooks(sessions[run_id], lambda e: None)
    result = await deep_research(question, conversations.get(session_id, []), hooks)
    _remember(session_id, question, result)
    tool_calls = [{"agent": c["agent"], "name": c["name"], "arguments": c["arguments"],
                   "output": (c["output"] or "")[:TOOL_OUTPUT_CHARS]} for c in hooks.calls]
    return {
        "answer": result["markdown"],
        "session_id": session_id,
        "run_id": run_id,
        "tool_calls": tool_calls,
        "needs_clarification": result["kind"] == "clarification",
        "options": result.get("options", []),
        "report": result.get("report"),
    }


@app.get("/run")
async def run(question: str, session_id: str | None = None):
    """The same research, streamed as Server-Sent Events for the page."""
    session_id, run_id = _start(session_id)
    queue: asyncio.Queue = asyncio.Queue()
    hooks = RecordingHooks(sessions[run_id], queue.put_nowait)

    async def work():
        try:
            result = await deep_research(question, conversations.get(session_id, []), hooks)
            _remember(session_id, question, result)
            queue.put_nowait({"type": "done", **result})
        except Exception as e:
            queue.put_nowait({"type": "error", "message": f"{type(e).__name__}: {str(e)[:500]}"})

    task = asyncio.create_task(work())

    async def events():
        try:
            yield f"data: {json.dumps({'type': 'start', 'run_id': run_id, 'session_id': session_id})}\n\n"
            while True:
                event = await queue.get()
                yield f"data: {json.dumps(event, default=str)}\n\n"
                if event["type"] in ("done", "error"):
                    break
        finally:
            task.cancel()

    return StreamingResponse(events(), media_type="text/event-stream")


if __name__ == "__main__":
    # Cloud Run sets PORT and needs 0.0.0.0; locally this is http://localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
