# AI Incident and Policy Research Agent 

Link: https://ai-incident-policy-research-agent-git-108380990875.europe-west1.run.app/

## What is it?
A data exploratory agent that investigates **reported AI failures** and **the policies that address them**, and generates a report that summarizes findings.  


Ask about reported incidents related to a specific AI use case (ie. Ai hiring, deepfakes, autonomous driving, etc) and relevant AI policies targeting these use cases. The data exploratory agent will find relevant reported incidents, how reported incidents have changed over the years, and what laws and bills apply. 


## Who is it for?
- **Product Teams and Builders** shipping AI features who want to know how similar systems have failed, and what policies they may need to be aware of.
- **Governance and policy teams** looking for gaps in current policies pertaining to different AI use cases.
- **Researchers and Students** interested in tracking patterns in reported AI incidents.

## How to run locally?

```bash
gcloud auth application-default login
uv run app.py                       # http://localhost:8000
uv run data_tools.py                # self-check of the data tools
uv run python tests/test_flow.py    # end-to-end check of the agent wiring with a scripted model (no credentials needed)
uv run python scripts/baseline.py   # generate baseline outputs to compare answers from the same model with no tools and no system prompt vs. my agent's answer.
```

Models default to `vertex_ai/gemini-3.5-flash` (Lead, Writer) and `vertex_ai/gemini-3.5-flash-lite` (researchers).

## Repo Structure
```
project2-redo/
├── app.py                    # FastAPI server and agent system: Lead, three researchers, Writer, citation check
├── data_tools.py             # Functions that search and count the data; agents call these as tools
├── index.html                # Chat interface served at /
├── context_panel.py          # Server side of the panel showing each agent's context and timeline
├── context-panel.js          # Browser side of that panel
├── baselines.md              # Model alone vs. agent answers for the sample queries
├── scripts/
│   ├── prep_data.py          # Cleans raw AIID and AGORA downloads into data/processed/
│   ├── classify_use_cases.py # Labels each incident with one of 17 AI use cases using Gemini
│   └── baseline.py           # Generates baselines.md
├── tests/
│   └── test_flow.py          # End-to-end test with a fake model (no credentials needed)
├── data/
│   ├── raw/                  # Original AIID and AGORA downloads
│   └── processed/            # Cleaned data the app loads at runtime
└── pyproject.toml, uv.lock   # Dependencies (uv)
```


## Data

### Where it came from

| Source | What it is | Raw files in `data/raw/` |
|---|---|---|
| [AI Incident Database](https://incidentdatabase.ai) (AIID) | Reported AI failures, each with a title, description, date, deployer/developer, and classifications from three taxonomies (MIT AI Risk Repository, CSETv1, GMF) | `AIID_Excel_Export-20261102.xlsx`: the site's Excel export, downloaded on 2026-11-02. |
| [AGORA](https://agora.eto.tech) (Emerging Technology Observatory) | AI laws, bills, rules and policies, with status, authority, summaries, thematic tags, and the full text split into sections ("segments") | `documents.csv`, `segments.csv`, `authorities.csv`: AGORA's bulk CSV download, downloaded on 2026-11-02. |

### Data Processing

To rebuild processed data from the raw downloads: `uv run scripts/prep_data.py build`, then `uv run scripts/classify_use_cases.py run` (needs Vertex AI access).

This only needs to be run once offline. The outputs are committed to `data/processed/`, so the application doesn't use `data/raw/`.

1. **`scripts/prep_data.py build`** cleans both AI Incident data and AGORA data and writes `risk_crosswalk.csv`, `MANIFEST.json` (row counts, coverage, caveats).
2. **`scripts/classify_use_cases.py run`** labels each incident with one of 17 use cases (`use_case_taxonomy.json`), plus an optional secondary use case and a confidence. AIID has no use-case field, so this is what lets the agent pull reported incidents related to a user-specified use case. Model: Gemini 3.5 Flash-Lite at temperature 0; raw responses are cached in `data/raw/use_case_labels.jsonl`. The model returned no usable answer for 8 incidents (likely blocked by its safety filters: sexual content involving minors, non-consensual imagery, or defamation of a named person), so those 8 were labelled by hand and are marked `manual` in the `confidence` and `model` columns. All 1,784 incidents have a use case.
3. **Hand-made files** that link the two datasets:
   - `risk_crosswalk.csv`: maps each MIT risk domain to AGORA harm and risk-factor tags (24 pairs). This is not an official mapping.
   - `use_case_policy_keywords.json`: search phrases per use case (e.g. "deepfake", "companion chatbot"). AGORA's own application tags don't line up with our use cases, so policies are matched by text: a document is "about" a use case if a phrase is in its name or summaries, or appears 3+ times in its text.


### Limitations of the data
- AIID counts are *reported* incidents, drawn from news coverage. They are not true incident rates, and 2026 is a partial year (data ends 2026-10-30).
- AGORA is mostly US documents (1,155 of 1,255) and not a complete record of AI law. Many documents are proposed or defunct bills, not law in force.
- Use-case labels were assigned by an LLM, and the risk crosswalk and policy keywords are hand-made. These are NOT official classifications.

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

Expected answers are computed directly from the processed files with `data_tools.py` (no model involved), so they are the numbers the agent's report should match. Full side-by-side outputs (model with no tools and no system prompt vs. this agent) are in `baselines.md`.

### 1. For autonomous vehicles and driver assistance: what failures have been reported, how have they changed over time, and which policies address them?

**Expected answer**
- **Failures:** 123 reported incidents, 2014–2026. The most-reported include the 2016 Tesla Autopilot fatal crash [AIID #52] and the 2018 Uber self-driving car that killed a pedestrian [AIID #4].
- **Over time:** a handful per year until 2018; peak full year 2022 with 20. 2020–2022 had 37 incidents and 2023–2025 had 31, so no rising trend. Safety failures are 92% then 84% of each period. 2026 has 20 so far (partial year).
- **Policies:** 64 AGORA documents are about autonomous vehicles (61 US): 29 enacted, 19 proposed, 16 defunct. The enacted ones most focused on AVs are state laws, e.g. California AB 1777 (2024) [AGORA #4104], California SB 480 (2025) [AGORA #4992], Connecticut SB 260 (2017) [AGORA #1664] and Iowa SB 302 (2019) [AGORA #1621].

**Where it comes from**
- Files: `incidents.csv` (`year`, `mit_risk_domain`, `mit_risk_subdomain`, `report_count`) joined to `incident_use_cases.csv` (`use_case`); `agora_documents.csv` (`status`, `authority`, `jurisdiction`) and `agora_segments.csv` (text), matched with `use_case_policy_keywords.json`.
- Functions: `dt.chart_for_scope(["Autonomous vehicles and driver assistance"])`, `dt.coverage_matrix("Autonomous vehicles and driver assistance")`.
- API: `GET /api/counts?use_case=Autonomous vehicles and driver assistance` → `"incidents": 123`; `GET /api/incidents.csv?use_case=Autonomous vehicles and driver assistance` lists them.

**Model vs Agent's Answer** 

Refer to baselines.md [(No Tool, No System Prompt) Model's Answer to Query 1](baselines.md#no-tool-no-system-prompt-models-answer-to-query-1) and [Agent's Answer to Query 1](baselines.md#agents-answer-to-query-1) for see the full output.

### 2. How have reported deepfake incidents changed from 2020–2022 to 2023–2025, and what share are intentional misuse? What enacted state laws target them?

**Expected answer**
- **Change:** 43 incidents in 2020–2022 → 499 in 2023–2025, about 11.6 times as many. Peak full year 2025 with 250.
- **Intentional misuse:** 30 of 43 (70%) in 2020–2022 → 440 of 499 (88%) in 2023–2025 (73% → 92% if unclassified incidents are excluded). Most fall under "Malicious Actors & Misuse", led by fraud, scams and targeted manipulation.
- **Enacted state laws:** 44 enacted documents from 21 US states are about deepfakes or synthetic media (most from California 7, New Hampshire 5, New York 5), plus 5 enacted federal documents. Examples: Minnesota HF 1370 (2023) [AGORA #1517], Utah HB 148 (2024) [AGORA #1532], Washington HB 1999 (2024) [AGORA #1537], California AB 2839 (2024) [AGORA #1549], Colorado SB 25-288 (2025) [AGORA #4523]. They target election deepfakes and non-consensual intimate images.

**Where it comes from**
- Files: `incidents.csv` (`year`, `mit_intent`, `mit_risk_domain`) joined to `incident_use_cases.csv`; `agora_documents.csv` filtered to `status = Enacted`, `jurisdiction = United States`, and a state `authority`.
- Functions: `dt.compare_periods("2020-2022", "2023-2025", group_by="intent", use_case="Synthetic media and deepfakes")`, `dt.coverage_matrix("Synthetic media and deepfakes", jurisdiction="United States")`.
- API: `GET /api/counts?use_case=Synthetic media and deepfakes&year_from=2020&year_to=2022` → `"incidents": 43`; with `year_from=2023&year_to=2025` → `"incidents": 499`.

**Model vs Agent's Answer** 

Refer to baselines.md [(No Tool, No System Prompt) Model's Answer to Query 2](baselines.md#no-tool-no-system-prompt-models-answer-to-query-2) and [Agent's Answer to Query 2](baselines.md#agents-answer-to-query-2) for see the full output.

### 3. What has gone wrong with AI chatbots and companions, and do any enacted policies address harms to minors?

**Expected answer**
- **Failures:** 255 reported incidents. The largest risk domains are misinformation (75, almost all "false or misleading information", e.g. ChatGPT inventing case law used in court [AIID #541]), discrimination and toxicity (45, mostly exposure to toxic content), privacy and security (32), and human-computer interaction (22, overreliance and unsafe use, e.g. the Tessa eating-disorder chatbot giving diet advice [AIID #545]). 167 are unintentional and 38 intentional.
- **Over time:** 25 incidents in 2020–2022 → 182 in 2023–2025; peak full year 2025 with 91.
- **Policies for minors: yes.** 114 AGORA documents are about chatbots (48 enacted). Enacted laws with specific protections for minors: California SB 243 (2025) [AGORA #4944], Washington HB 2225 (2026) [AGORA #6694], Colorado HB 1263 (2026) [AGORA #6741], Idaho SB 1297 (2026) [AGORA #6727] and Hawaii SB 3001 (2026) [AGORA #5401]. Common requirements: disclose that the user is talking to an AI, suicide and self-harm protocols, and extra safeguards for minors (e.g. no sexually explicit content, limits on emotional dependence).

**Where it comes from**
- Files: `incidents.csv` (`mit_risk_domain`, `mit_risk_subdomain`, `mit_intent`, `year`) joined to `incident_use_cases.csv`; `agora_documents.csv` (`short_summary`, `status`) and `agora_segments.csv` (`text`) for the minor-protection provisions.
- Functions: `dt.count_incidents("risk_domain", use_case="Chatbots and AI assistants")`, `dt.search_policy_text("companion chatbot minors", status="Enacted")`.
- API: `GET /api/counts?use_case=Chatbots and AI assistants` → `"incidents": 255`.

**Model vs Agent's Answer** 

Refer to baselines.md [(No Tool, No System Prompt) Model's Answer to Query 3](baselines.md#no-tool-no-system-prompt-models-answer-to-query-3) and [Agent's Answer to Query 3](baselines.md#agents-answer-to-query-3) for see the full output.