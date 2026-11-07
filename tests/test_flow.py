"""End-to-end check of the agent wiring with a scripted model instead of Gemini (no credentials needed).

    uv run python tests/test_flow.py

The fake model plays each agent by its instructions: the Lead calls describe_data, set_brief, then three
researchers in one turn; researchers call their tools once; the Writer cites what they found. Real data, real
tools, real hooks, real citation check.
"""

import asyncio
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.items import ModelResponse  # noqa: E402
from agents.models.interface import Model  # noqa: E402
from agents.usage import Usage  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from openai.types.responses import ResponseFunctionToolCall, ResponseOutputMessage, ResponseOutputText  # noqa: E402

import app  # noqa: E402


def call(name, **args):
    cid = "call_" + uuid.uuid4().hex[:8]
    return ResponseFunctionToolCall(id=cid, call_id=cid, name=name, arguments=json.dumps(args), type="function_call")


def say(text):
    return ResponseOutputMessage(id="m_" + uuid.uuid4().hex[:6], role="assistant", status="completed", type="message",
                                 content=[ResponseOutputText(text=text, type="output_text", annotations=[])])


def tool_outputs(items):
    return [i for i in items if isinstance(i, dict) and i.get("type") == "function_call_output"]


class Scripted(Model):
    def __init__(self, vague=False):
        self.vague = vague

    async def get_response(self, system_instructions, input, model_settings, tools, output_schema, handoffs,
                           tracing, *a, **k):
        items = input if isinstance(input, list) else [{"role": "user", "content": input}]
        done = tool_outputs(items)
        text = json.dumps(items, default=str)
        sys_ = system_instructions or ""
        if sys_.startswith("You lead"):
            if not done:
                return self._r([call("describe_data")])
            if len(done) == 1:
                if self.vague and "Earlier in this conversation" not in text:
                    return self._r([call("ask_user", question="Which use case?", options=["Hiring and employment", "Chatbots and AI assistants"])])
                return self._r([call("set_brief", mode="use_case", focus="hiring failures and policy",
                                     use_cases=["hiring"], jurisdiction="United States")])
            if len(done) == 2 and "Question sent" not in text:
                return self._r([call("research", role=r, task=f"{r} task") for r in ("incidents", "trends", "policy")])
            return self._r([say("DONE")])
        if sys_.startswith("You find out what has gone wrong"):
            if not done:
                return self._r([call("search_incidents", use_case="Hiring and employment", limit=3)])
            ids = sorted(set(app.CITE.findall(done[-1]["output"])))[:2]
            return self._r([say("- Biased screening " + " ".join(f"[{k} #{n}]" for k, n in ids))])
        if sys_.startswith("You find out how reported"):
            if not done:
                return self._r([call("count_incidents", group_by="year", split_by="risk_domain", use_case="Hiring and employment")])
            return self._r([say("- Counts rose.")])
        if sys_.startswith("You find out which policies"):
            if not done:
                return self._r([call("coverage_matrix", use_case="Hiring and employment", jurisdiction="United States"),
                                call("search_policy_text", query="automated employment decision bias audit", status="Enacted")])
            ids = sorted(set(app.CITE.findall(done[-1]["output"])))[:2]
            return self._r([say("- NYC rule " + " ".join(f"[{k} #{n}]" for k, n in ids))])
        if sys_.startswith("Write a research report"):
            assert "CHART FACTS" in text and "Peak full year" in text, "the Writer must get the chart facts"
            cites = " ".join(f"[{k} #{n}]" for k, n in app.CITE.findall(text)[:4])
            return self._r([say(f"# Hiring\n**Bottom line.** Stuff {cites} and a fake [AIID #999999].\n## How reporting has changed\nUp.\n[[CHART]]\n")])
        raise AssertionError("unknown agent: " + sys_[:60])

    def _r(self, output):
        return ModelResponse(output=output, usage=Usage(), response_id=None)

    def stream_response(self, *a, **k):
        raise NotImplementedError


def use(model):
    for agent in (app.lead, app.writer, *app.RESEARCHERS.values()):
        agent.model = model


def main():
    use(Scripted())
    client = TestClient(app.app)
    r = client.post("/chat", json={"message": "What failures have been reported for AI hiring tools, and which US policies address them?"})
    assert r.status_code == 200, r.text
    body = r.json()
    agents = {c["agent"] for c in body["tool_calls"]}
    assert {"Lead", "Incident Researcher", "Trend Analyst", "Policy Researcher"} <= agents, agents
    rep = body["report"]
    assert rep["chart"] and rep["chart"]["split"], "chart missing"
    assert rep["coverage"]["rows"], "coverage missing"
    c = rep["citations"]
    assert "AIID #999999" in c["unverified"] and c["verified"] >= 2, c
    assert "| Year | Reported incidents |" in body["answer"] and "[[CHART]]" not in body["answer"]
    assert body["answer"].split("\n")[2].startswith("*Scope · Incidents: Hiring and employment"), body["answer"][:300]
    assert "Policies: United States" in body["answer"] and rep["chart"]["facts"]
    assert {e["agent"] for e in body["tool_calls"]} and all(c["output"] for c in body["tool_calls"]), "every call has output"
    print("chat ok:", len(body["tool_calls"]), "tool calls;", c["verified"], "verified,", c["unverified"], "unverified")

    # Clarification, then the answer in the same session
    use(Scripted(vague=True))
    r = client.post("/chat", json={"message": "Is AI dangerous?"}).json()
    assert r["needs_clarification"] and r["options"], r
    r2 = client.post("/chat", json={"message": "Hiring and employment", "session_id": r["session_id"]}).json()
    assert not r2["needs_clarification"] and r2["report"]["chart"], r2["answer"][:300]
    print("clarification ok:", r["answer"], r["options"])

    # The streamed version
    use(Scripted())
    with client.stream("GET", "/run", params={"question": "AI hiring failures and US policy"}) as s:
        kinds = [json.loads(line[6:])["type"] for line in s.iter_lines() if line.startswith("data: ")]
    assert kinds[0] == "start" and kinds[-1] == "done" and "tool" in kinds and "brief" in kinds, kinds
    print("run ok:", {k: kinds.count(k) for k in set(kinds)})
    assert client.get("/api/meta").json()["incidents"] == 1784
    page = client.get("/api/incidents", params={"use_case": "Hiring and employment", "year": 2021}).json()
    assert page["total"] == 8 and len(page["items"]) == 8, page["total"]
    big = client.get("/api/incidents", params={"use_case": "Synthetic media and deepfakes", "offset": 25}).json()
    assert big["total"] == 680 and len(big["items"]) == 25 and big["offset"] == 25
    csv_text = client.get("/api/incidents.csv", params={"use_case": "Synthetic media and deepfakes"}).text
    assert csv_text.count("\n") >= 681, csv_text.count("\n")
    print("drill-down ok")
    print("all ok")


if __name__ == "__main__":
    main()
