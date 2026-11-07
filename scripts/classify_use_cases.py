"""Offline build step 2: label every AIID incident with an AI use case (LLM, run once, results committed).

AIID has no use-case field with good coverage, so "most commonly reported use cases" and "incidents for
use case X" need one. This labels each incident with ONE primary use case from a fixed list (plus an
optional secondary), so counts are deterministic and the Researchers filter on a column.

    uv run scripts/classify_use_cases.py run                 # label all incidents (resumable)
    uv run scripts/classify_use_cases.py run --limit 20      # try a few first
    uv run scripts/classify_use_cases.py sample              # write a 60-row sheet to hand-check
    uv run scripts/classify_use_cases.py score               # accuracy from your hand-checked sheet

Needs data/processed/incidents.csv (run prep_data.py first) and Vertex AI access: `gcloud auth
application-default login`. If LiteLLM complains about the project, set VERTEXAI_PROJECT.

Outputs (data/processed/)
  incident_use_cases.csv    incident_id, use_case, secondary_use_case, confidence, model
  use_case_taxonomy.json    label -> definition (the Lead uses it to map a user's words to a label)
  use_case_check.csv        the hand-check sheet (sample/score only)
Machine labels are a caveat: report the hand-checked accuracy in the README.
"""

import argparse
import asyncio
import json
import random
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "processed"
CACHE = ROOT / "data" / "raw" / "use_case_labels.jsonl"  # append-only, so a crash or rerun loses nothing
DEFAULT_MODEL = "vertex_ai/gemini-3.5-flash-lite"       # same family the starter uses for Researchers

# What the AI system was being USED for (not the harm). Edit freely, then delete the cache and rerun.
TAXONOMY = {
    "Hiring and employment": "Resume screening, job-candidate scoring, workplace monitoring, algorithmic management of workers.",
    "Chatbots and AI assistants": "General-purpose or companion chatbots and LLM assistants, including hallucinated answers and unsafe advice.",
    "Synthetic media and deepfakes": "Generating or altering images, video, audio or voice: deepfakes, voice clones, AI art, fake content.",
    "Content recommendation and moderation": "Social media feeds, recommender systems, search ranking, automated content moderation or filtering.",
    "Facial recognition and biometrics": "Face recognition, biometric identification or tracking, emotion recognition.",
    "Law enforcement and criminal justice": "Predictive policing, risk-assessment scores, gunshot or crime detection, courts, immigration enforcement.",
    "Autonomous vehicles and driver assistance": "Self-driving cars, robotaxis, autopilot, drones used for transport.",
    "Healthcare and medicine": "Diagnosis, clinical decision support, medical devices, health-insurance decisions, mental-health apps.",
    "Education": "Grading, proctoring, plagiarism or AI-text detection, tutoring, student monitoring.",
    "Finance, insurance and credit": "Credit scoring, lending, trading, fraud detection, insurance pricing.",
    "Government services and public administration": "Benefits eligibility, welfare, tax, public-sector automated decisions.",
    "Military and defense": "Weapons, targeting, military surveillance or autonomy.",
    "Robotics and industrial automation": "Factory, warehouse and service robots, industrial control systems.",
    "Software development and AI agents": "Coding assistants and autonomous agents acting on software, accounts or infrastructure.",
    "Customer service, retail and advertising": "Support bots, pricing, ad targeting, e-commerce, marketing.",
    "Consumer devices and smart home": "Voice assistants, toys, wearables, home devices.",
    "Other or unclear": "Use does not fit any label above, or the description is too vague to tell.",
}
LABELS = list(TAXONOMY)

SYSTEM = (
    "You label AI incident reports with the AI USE CASE: what the AI system was being used for, not the "
    "harm it caused. Choose exactly one primary label from the list; choose a secondary label only if a "
    "second use case clearly applies, else null. Use 'Other or unclear' sparingly.\n\nLabels:\n"
    + "\n".join(f"- {k}: {v}" for k, v in TAXONOMY.items())
    + '\n\nReply with JSON only: {"primary": "<label>", "secondary": "<label or null>", '
    '"confidence": "high" | "medium" | "low"}'
)


def incident_text(r) -> str:
    parts = [f"Title: {r.title}", f"Description: {r.description}"]
    for name, col in (("Implicated systems", r.implicated_systems), ("Deployer", r.deployer), ("Harmed", r.harmed)):
        if col:
            parts.append(f"{name}: {col}")
    return "\n".join(parts)


def parse(text: str) -> dict | None:
    try:
        d = json.loads(text.strip().removeprefix("```json").removesuffix("```").strip())
    except (ValueError, AttributeError):
        return None
    if d.get("primary") not in LABELS:
        return None
    sec = d.get("secondary")
    return {"use_case": d["primary"], "secondary_use_case": sec if sec in LABELS and sec != d["primary"] else "",
            "confidence": d.get("confidence") if d.get("confidence") in ("high", "medium", "low") else "low"}


def is_rate_limit(e: Exception) -> bool:
    return "ratelimit" in type(e).__name__.lower() or "429" in str(e)[:200] or "resource exhausted" in str(e).lower()


async def label_one(litellm, sem, model, r) -> dict:
    empty = {"incident_id": r.incident_id, "use_case": "", "secondary_use_case": "", "confidence": "", "model": model}
    bad_replies = 0
    async with sem:
        for attempt in range(7):
            try:
                extra = {"vertex_location": "global"} if model.startswith("vertex_ai/") else {}
                resp = await litellm.acompletion(
                    model=model, temperature=0, num_retries=0, timeout=90, **extra,
                    response_format={"type": "json_object"},
                    messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": incident_text(r)}])
                out = parse(resp.choices[0].message.content)
                if out:
                    return {"incident_id": r.incident_id, **out, "model": model}
                bad_replies += 1
                if bad_replies >= 2:  # model keeps returning something unusable: leave it for a later run
                    return empty
            except Exception as e:
                if not is_rate_limit(e) or attempt == 6:
                    print(f"  ! incident {r.incident_id}: {type(e).__name__}: {str(e)[:120]}")
                    return empty
                # Quota hit: back off (2, 4, 8, ... up to 60 s, with jitter) and try again. Other slots wait
                # too, because this task still holds a semaphore slot while it sleeps.
                await asyncio.sleep(min(60, 2 ** (attempt + 1)) + random.random())
    return empty


async def run(model: str, limit: int | None, concurrency: int) -> None:
    import litellm  # imported here so `sample` / `score` work without Vertex set up

    inc = pd.read_csv(DATA / "incidents.csv", dtype=str, keep_default_na=False)
    done = {}
    if CACHE.exists():
        for line in CACHE.read_text().splitlines():
            rec = json.loads(line)
            if rec["use_case"]:
                done[rec["incident_id"]] = rec
    todo = [r for r in inc.itertuples() if r.incident_id not in done][:limit]
    print(f"{len(done)} cached, labelling {len(todo)} with {model}")
    sem = asyncio.Semaphore(concurrency)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with CACHE.open("a") as f:
        for coro in asyncio.as_completed([label_one(litellm, sem, model, r) for r in todo]):
            rec = await coro
            if rec["use_case"]:
                done[rec["incident_id"]] = rec
                f.write(json.dumps(rec) + "\n")
                f.flush()
    out = pd.DataFrame(done.values()).reindex(columns=["incident_id", "use_case", "secondary_use_case", "confidence", "model"])
    out = out.sort_values("incident_id", key=lambda s: s.astype(int))
    out.to_csv(DATA / "incident_use_cases.csv", index=False)
    (DATA / "use_case_taxonomy.json").write_text(json.dumps(TAXONOMY, indent=2))
    missing = len(inc) - len(out)
    print(f"wrote {len(out)} labels ({missing} still unlabelled: rerun to retry)")
    print(out["use_case"].value_counts().to_string())
    print("confidence:", out["confidence"].value_counts().to_dict())


def sample(n: int = 60) -> None:
    inc = pd.read_csv(DATA / "incidents.csv", dtype=str, keep_default_na=False)
    lab = pd.read_csv(DATA / "incident_use_cases.csv", dtype=str, keep_default_na=False)
    m = inc.merge(lab, on="incident_id")
    s = m.sample(min(n, len(m)), random_state=7)  # fixed seed: the same sample each time
    s[["incident_id", "title", "description", "use_case", "secondary_use_case", "confidence"]].assign(
        label_ok="", better_label="").to_csv(DATA / "use_case_check.csv", index=False)
    print(f"Wrote {len(s)} rows to use_case_check.csv. Put Y or N in label_ok (and the right label in "
          "better_label when N), then run `score`. Counts as correct if the primary OR the secondary fits.")


def score() -> None:
    d = pd.read_csv(DATA / "use_case_check.csv", dtype=str, keep_default_na=False)
    d = d[d["label_ok"].str.upper().isin(["Y", "N"])]
    if d.empty:
        raise SystemExit("No rows with label_ok = Y/N yet.")
    ok = (d["label_ok"].str.upper() == "Y")
    n, p = len(d), ok.mean()
    print(f"hand-checked {n}: accuracy {p:.0%} (+/- {1 / n ** 0.5:.0%}, the course's 1/sqrt(n) margin)")
    print("by confidence:\n" + d.assign(ok=ok).groupby("confidence")["ok"].agg(["mean", "count"]).round(2).to_string())
    print("\nmost common mistakes:\n" + d[~ok].groupby(["use_case", "better_label"]).size().sort_values(ascending=False).head(8).to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["run", "sample", "score"])
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--concurrency", type=int, default=3, help="parallel requests; lower it if you hit 429s")
    a = ap.parse_args()
    if a.cmd == "run":
        asyncio.run(run(a.model, a.limit, a.concurrency))
    else:
        sample() if a.cmd == "sample" else score()