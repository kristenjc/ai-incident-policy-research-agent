"""The README's baseline: the same model, no tools, no system prompt, on the three sample queries.

    uv run python scripts/baseline.py            -> writes baselines.md
    uv run python scripts/baseline.py --agent    -> also runs the agent on each query (needs ~3 min each)

Needs gcloud application-default credentials, like the app.
"""

import asyncio
import sys
from pathlib import Path

import litellm

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

QUERIES = [
    "What failures have been reported for AI hiring tools, and which US policies address them? Which are actually enacted?",
    "How did reported deepfake incidents change from 2020-2022 to 2023-2025, and what share were intentional misuse? Which enacted US state laws target deepfakes?",
    "For content recommendation and moderation systems, which kinds of reported AI failure have no enacted US policy addressing them?",
]
MODEL = "vertex_ai/gemini-3.5-flash"


async def bare(q: str) -> str:
    r = await litellm.acompletion(model=MODEL, messages=[{"role": "user", "content": q}], vertex_location="global")
    return r.choices[0].message.content


async def agent(q: str) -> str:
    import app
    from context_panel import AgentContexts

    hooks = app.RecordingHooks(AgentContexts(), lambda e: None)
    result = await app.deep_research(q, [], hooks)
    return result["markdown"]


async def main():
    with_agent = "--agent" in sys.argv
    out = ["# Baselines: same model, no tools, no system prompt\n"]
    for i, q in enumerate(QUERIES, 1):
        out.append(f"## Query {i}\n\n> {q}\n\n### Model alone\n\n{await bare(q)}\n")
        if with_agent:
            out.append(f"### Agent\n\n{await agent(q)}\n")
        print(f"query {i} done")
    (ROOT / "baselines.md").write_text("\n".join(out))
    print("wrote baselines.md")


if __name__ == "__main__":
    asyncio.run(main())
