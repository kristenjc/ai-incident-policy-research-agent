# Incident × Policy Desk

A deep research agent that investigates **reported AI failures** and **the policies that address them**. Ask about an
AI use case (hiring tools, chatbots, deepfakes, facial recognition…) or about the dataset as a whole. A team of agents
works out what has gone wrong, how reports changed over the years, and which laws and bills apply, and whether they
are actually enacted. Every claim in the report links to the incident or policy document behind it.

**Who it's for**
- **Product teams** shipping AI features who want to know how similar systems have failed, and what rules they may face.
- **Governance and policy teams** looking for risks that have incidents but no enacted policy.
- **Researchers and students** tracking patterns in reported AI incidents.

Path: **Deep Research** (`submission.json`).

## Data

| Source | What we use | Where it came from | Files |
|---|---|---|---|
| [AI Incident Database](https://incidentdatabase.ai) (AIID) | 1,784 reported incidents, 1983 to 2026-10-30, with MIT risk taxonomy (84% coverage), CSETv1 (11%) and GMF (1.5%) classifications | Excel export from the AIID site, downloaded 2026-11-02 (`data/raw/AIID_Excel_Export-20261102.xlsx`) | `data/processed/incidents.csv` |
| [AGORA](https://agora.eto.tech) (Emerging Technology Observatory) | 1,255 AI law, bill, rule and policy documents with status (546 enacted, 287 proposed, 422 defunct), tags, summaries, and 10,215 text segments | Bulk download from AGORA (`documents.csv`, `segments.csv`, `authorities.csv`) | `data/processed/agora_documents.csv`, `agora_segments.csv` |

**Built offline, by us** (`scripts/`):
- `prep_data.py`: cleans both datasets, keeps the useful columns, and joins AGORA tags onto documents and segments. Writes `MANIFEST.json` with counts and caveats.
- `classify_use_cases.py`: labels every incident with one of 17 use cases (`use_case_taxonomy.json`) using Gemini Flash-Lite, with a confidence (1,600 high, 146 medium, 30 low). Output: `incident_use_cases.csv`. AIID has no field like this so this was creates to allow users to ask questions specific to an AI use case (eg. autonomous vechiles, hiring, etc).
- `risk_crosswalk.csv`: a hand-made map from MIT risk domains to AGORA harm and risk-factor tags. It links the two datasets. It is not an official mapping.
- `use_case_policy_keywords.json`: hand-written search phrases per use case. AGORA's own application tags don't line up with our use cases (it has no "hiring" tag), so policy search is by text.

**What the data can't answer** (the agent says so when it applies):
- AIID counts are *reported* incidents, shaped by news coverage and editor curation. They are not incident rates.
- 2026 is a partial year.
- AGORA is about 92% US documents, and not a complete record of AI law. Many documents are proposed or defunct bills.
- "What technically failed" is only classified for about 1.5% of incidents (GMF).

## How it works

```
User question
  └─ Lead (gemini-3.5-flash)
       describe_data → ask_user (if vague) → set_brief → research ×3 in one turn → gap check (≤2 follow-ups, ≤6 researchers)
         ├─ Incident Researcher (flash-lite): search_incidents, get_incident
         ├─ Trend Analyst (flash-lite):       count_incidents, compare_periods
         └─ Policy Researcher (flash-lite):   coverage_matrix, policy_keywords, search_policy_text,
                                              search_policies, get_policy, risks_to_policy_tags
  └─ Writer (flash): sees only the question, brief and findings
  └─ Citation check (code): every [AIID #n] / [AGORA #n] must exist AND have been returned by a tool in this run
```

- **Three researcher shapes with different jobs and tools**, each started in a fresh context and run in parallel.
  The Lead writes a **research brief** (use cases, years, jurisdiction, focus), so all three researchers work within the same scope.
- **Vague questions get a clarifying question first**, with clickable options drawn from the data. This happens when
  there's no use case, the use case is ambiguous, or the question asks for something the data can't give (rates, non-US law).
- **The tools compute; the models don't.** Every count is a pandas query over unique incident IDs, and the partial year is
  always flagged. Policy text search is BM25 over AGORA segments (`data_tools.py`, no extra dependencies).
- **The chart and the coverage matrix in the report come straight from tool output**, not from model text.
- **Coverage matrix:** for each risk domain in a use case, it shows the incident count and how many enacted / proposed /
  defunct policies about that use case carry a matching tag. This is how the report points to risks with incidents but
  no enacted policy.
- **Citations are checked by code.** A tag the tools never returned is marked `⚠ unverified` in the report, and the page
  shows "N/M citations verified".
- Time budget: the Lead gets 200 s, then the Writer works with whatever was found, so an answer returns within the
  graders' 5 minutes.

### API

`POST /chat` keeps Project 1's shape:

```json
// request
{"message": "What failures have been reported for AI hiring tools?", "session_id": "optional, to answer a clarifying question"}
// response
{"answer": "<markdown report, or the clarifying question>",
 "session_id": "...",
 "tool_calls": [{"agent": "Policy Researcher", "name": "search_policy_text", "arguments": {...}, "output": "..."}],
 "needs_clarification": false, "options": [],
 "report": {"brief": {...}, "chart": {...}, "coverage": {...}, "citations": {"cited": 14, "verified": 14, "unverified": []}}}
```

`GET /run?question=...` streams the same run as server-sent events for the web page. `GET /context` feeds the
agent-context panel ("Show agent contexts").

## Sample queries

Expected answers below come from the processed files, computed with `data_tools.py`.
Model-alone answers come from `scripts/baseline.py` (same model, no tools, no system prompt): see `baselines.md`.

**1. "What failures have been reported for AI hiring tools, and which US policies address them? Which are actually enacted?"**
- Expected: 37 incidents are labeled *Hiring and employment*. The most common MIT subdomain is *Unfair discrimination and
  misrepresentation* (10), then privacy compromise (6) and lack of robustness (5). Examples: Amazon's recruiting tool
  showing gender bias (AIID #37), an employee terminated by an automated system (AIID #35). Enacted: New York City's Local Law
  on automated employment decision tools, which requires a bias audit within a year before use (AGORA #72, enacted
  2021-12-11), and the NYC DCWP rules implementing it (AGORA #2002, 2023-07-05).
- Source: `incidents.csv` + `incident_use_cases.csv` (use_case, mit_risk_subdomain); `agora_segments.csv` / `agora_documents.csv` (status).
- Model alone: *(paste from baselines.md)*
- Agent: *(paste from baselines.md)*

**2. "How did reported deepfake incidents change from 2020-2022 to 2023-2025, and what share were intentional misuse? Which enacted US state laws target deepfakes?"**
- Expected: *Synthetic media and deepfakes* went from 43 incidents (2020–22) to 496 (2023–25). Intentional misuse went from
  70% to 88% of them. *Fraud, scams, and targeted manipulation* is the largest subdomain (21 → 286). Enacted state laws
  include California AB 2839 (AGORA #1549), Michigan HB 5144 (AGORA #1515) and Arizona SB 1359 (AGORA #1485), mostly about
  deceptive election media.
- Source: `incidents.csv` (year, mit_intent, mit_risk_subdomain) + `incident_use_cases.csv`; `agora_segments.csv`.
- Model alone: *(paste)* · Agent: *(paste)*

**3. "For content recommendation and moderation systems, which kinds of reported AI failure have no enacted US policy addressing them?"**
- Expected: 149 incidents. Only 20 US policy documents are about recommendation or moderation systems (2 enacted, 4
  proposed, 14 defunct). *Malicious Actors & Misuse* (16 incidents) and *Socioeconomic & Environmental Harms* (8) have no
  matching policy, and *Human-Computer Interaction* (4) has proposed policy only. Caveat: this depends on the hand-made crosswalk and keyword matching.
- Source: `coverage_matrix` over `incidents.csv`, `incident_use_cases.csv`, `agora_documents.csv`, `risk_crosswalk.csv`, `use_case_policy_keywords.json`.
- Model alone: *(paste)* · Agent: *(paste)*

**Something it should push back on:** "How often do AI healthcare systems fail in the EU?" The Lead should ask for
clarification or say what the data can't do: AIID has reported incidents, not rates; only 38 incidents are healthcare;
and AGORA has few EU documents (for example the EU AI Act, AGORA #757).

## Run it

```bash
gcloud auth application-default login
uv run app.py                       # http://localhost:8000
uv run data_tools.py                # self-check of the data tools (no model needed)
uv run python tests/test_flow.py    # end-to-end check of the agent wiring with a scripted model (no credentials needed)
uv run python scripts/baseline.py   # no-tools baselines for this README
```

Models default to `vertex_ai/gemini-3.5-flash` (Lead, Writer) and `vertex_ai/gemini-3.5-flash-lite` (researchers).
Override them with `LEAD_MODEL` / `RESEARCHER_MODEL`.

## Deploy

Cloud Run with continuous deploy from GitHub, following the course guide. The data (`data/processed`, about 24 MB) is
committed and ships with the image. `app.py` listens on `0.0.0.0:$PORT`. Set the request timeout to 600 s
(`gcloud run services update <service> --timeout=600`). The agent caps itself at about 4 minutes.
