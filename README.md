# AI Incident and Policy Research Agent 

---
Each agent should come with a README.md that:

Describes the project and who the target user is
Where your data came from and how someone could load it (it’s not strictly necessary that the grader can load it, just that they understand where it came from).
Lists three sample queries for the grader to test with. For each, give the answer you expect and the file, table or API endpoint it comes from.
For each sample query, include the answer from the same model with no tools and no system prompt, next to your agent's answer. This will help us measure the effectiveness of how your agent uses the information even if the model already knows the domain.
---

## What is it?
A data exploratory agent that investigates **reported AI failures** and **the policies that address them**, and generates a report that summarizes findings.  


Ask about reported incidents related to a specific AI use case (ie. Ai hiring, deepfakes, autonomous driving, etc) and relevant AI policies targeting these use cases. The data exploratory agent will find relevant reported incidents, how reported incidents have changed over the years, and what laws and bills apply. 


## Who is it for?
- **Product Teams and Builders** shipping AI features who want to know how similar systems have failed, and what policies they may need to be aware of.
- **Governance and policy teams** looking for gaps in current policies pertaining to different AI use cases.
- **Researchers and Students** interested in tracking patterns in reported AI incidents.

## How to get started?

```bash
gcloud auth application-default login
uv run app.py                       # http://localhost:8000
uv run data_tools.py                # self-check of the data tools (no model needed)
uv run python tests/test_flow.py    # end-to-end check of the agent wiring with a scripted model (no credentials needed)
uv run python scripts/baseline.py   # generate baseline outputs to compare answers from the same model with no tools and no system prompt vs. my agent's answer.
```

Models default to `vertex_ai/gemini-3.5-flash` (Lead, Writer) and `vertex_ai/gemini-3.5-flash-lite` (researchers).


## Data

| Source | What we use | Where it came from | Files |
|---|---|---|---|
| [AI Incident Database](https://incidentdatabase.ai) (AIID) | 1,784 reported incidents, 1983 to 2026-10-30, with MIT risk taxonomy (84% coverage), CSETv1 (11%) and GMF (1.5%) classifications | Excel export from the AIID site, downloaded 2026-11-02 (`data/raw/AIID_Excel_Export-20261102.xlsx`) | `data/processed/incidents.csv` |
| [AGORA](https://agora.eto.tech) | 1,255 AI law, bill, rule and policy documents with status (546 enacted, 287 proposed, 422 defunct), tags, summaries, and 10,215 text segments | Bulk download from AGORA (`data/raw/documents.csv`, `data/raw/segments.csv`, `data/raw/authorities.csv`) | `data/processed/agora_documents.csv`, `data/processed/agora_segments.csv` |

Some processing was done on the raw data to make it more usable for this proejct. See files in (`scripts/`):
- `prep_data.py`: cleans both datasets, keeps useful columns, and joins AGORA tags onto documents and segments. Writes `MANIFEST.json` with counts and caveats.
- `classify_use_cases.py`: labels every reported incident with one of 17 use cases (`data/processed/use_case_taxonomy.json`) using Gemini Flash-Lite, with a confidence (1,600 high, 146 medium, 30 low). Output: `data/processed/incident_use_cases.csv`. AIID has no field like this, so this was done so we can get all reported incidents for a specific use case. 
- `data/processed/risk_crosswalk.csv`: a hand-made map from MIT risk domains to AGORA harm and risk-factor tags. This links the AI Incident and AGORA Policy dataset. This is not an official mapping.
- `data/processed/use_case_policy_keywords.json`: hand-written search phrases per use case. AGORA's own application tags don't line up with our AI use cases, so policy search is by text.

**Limitations of the Data** 
- AIID counts are *reported* incidents, drawn from news coverage. They are not true incident rates.
- 2026 is a partial year.
- AGORA mostly consists of US documents, and not a complete record of all AI law. Many documents are proposed or defunct bills, and not enacted bills. 

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
  The Lead writes a research brief (use cases, years, jurisdiction, focus), so all three researchers work within the same scope.
    - **Incident Researcher Agent:** Identify relevant reported incidents related to user query.
    - **Trend Analyst Agent:** Analyze how reported incidents have changed over the years, uses reported incidents relevant to user query.
    - **Policy Researcher Agent:** Identify relevant policies related to user query.
- **Vague user queries are prompted with a clarification** clickable options are generated from the data to help user narrow down query scope. Clarification is rquired when the user doesn't specify a use case, the use case is ambiguous, or the query asks for something the data cannot provide.

## Sample Queries

1. For autonomous vehicles and driver assistance: what failures have been reported, how have they changed over time, and which policies address them?


2. How have reported deepfake incidents changed fro 2020-2022 to 2023-2025, and what share are intentional misuse? What enacted state laws target them?


3. What has gone wrong with AI chatbots and companions, and do any enacted policies address harms to minors?

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

