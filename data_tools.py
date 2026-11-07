"""Data access for the agents: AI Incident Database (AIID) incidents and AGORA policy documents.

Everything here is plain pandas and returns JSON-safe dicts, so it can be tested without a model:
    uv run data_tools.py

The agents never write queries. They call these functions with parameters, so counts are computed
the same way every time: always over unique incident IDs, with the partial latest year flagged.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "processed"

AIID_URL = "https://incidentdatabase.ai/cite/{id}/"
AGORA_URL = "https://agora.eto.tech/instrument/{id}"
UNCLASSIFIED = "(not classified)"

# --- Load once, at import ---

MANIFEST = json.loads((DATA / "MANIFEST.json").read_text())
TAXONOMY: dict[str, str] = json.loads((DATA / "use_case_taxonomy.json").read_text())
POLICY_KEYWORDS: dict[str, list[str]] = {
    k: v for k, v in json.loads((DATA / "use_case_policy_keywords.json").read_text()).items() if not k.startswith("_")
}

_inc = pd.read_csv(DATA / "incidents.csv")
_uc = pd.read_csv(DATA / "incident_use_cases.csv")[["incident_id", "use_case", "secondary_use_case", "confidence"]]
INCIDENTS = _inc.merge(_uc, on="incident_id", how="left").drop_duplicates("incident_id").set_index("incident_id", drop=False)
for col in ["mit_risk_domain", "mit_risk_subdomain", "mit_intent", "mit_responsible_entity", "mit_timing", "use_case"]:
    INCIDENTS[col] = INCIDENTS[col].fillna(UNCLASSIFIED)

DOCS = pd.read_csv(DATA / "agora_documents.csv").set_index("agora_id", drop=False)
DOCS["jurisdiction"] = DOCS["jurisdiction"].fillna("Unknown")
SEGMENTS = pd.read_csv(DATA / "agora_segments.csv")
CROSSWALK = pd.read_csv(DATA / "risk_crosswalk.csv")

LATEST_YEAR = int(INCIDENTS["year"].max())  # partial: the export ends mid-year
TAG_COLUMNS = ["applications", "harms", "incentives", "risk_factors", "strategies"]

# Short names the agents may use for group_by
GROUPS = {
    "year": "year",
    "risk_domain": "mit_risk_domain",
    "risk_subdomain": "mit_risk_subdomain",
    "intent": "mit_intent",
    "responsible_entity": "mit_responsible_entity",
    "timing": "mit_timing",
    "use_case": "use_case",
    "deployer": "deployer",
}


def _tags(value) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return []
    return [t.strip() for t in value.split(";") if t.strip()]


def _clip(text, n: int) -> str:
    text = "" if not isinstance(text, str) else " ".join(text.split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def _clean(value):
    """NaN -> None, numpy -> python, for JSON."""
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


# --- BM25, small and dependency-free ---

_STOP = set(
    "a an and are as at be by for from has have in is it its of on or that the this to was were will with "
    "shall may any such other under section sec subsection paragraph act".split()
)


def _tokens(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", str(text).lower())
    return [w[:-1] if len(w) > 4 and w.endswith("s") else w for w in words if w not in _STOP and len(w) > 1]


class BM25:
    def __init__(self, texts: list[str], k1: float = 1.4, b: float = 0.75):
        self.k1, self.b = k1, b
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        self.lengths = []
        for i, text in enumerate(texts):
            counts = Counter(_tokens(text))
            self.lengths.append(sum(counts.values()))
            for term, tf in counts.items():
                self.postings[term].append((i, tf))
        self.n = len(texts)
        self.avg = (sum(self.lengths) / self.n) if self.n else 1.0

    def scores(self, query: str) -> dict[int, float]:
        out: dict[int, float] = defaultdict(float)
        for term in set(_tokens(query)):
            plist = self.postings.get(term)
            if not plist:
                continue
            idf = math.log(1 + (self.n - len(plist) + 0.5) / (len(plist) + 0.5))
            for i, tf in plist:
                norm = tf + self.k1 * (1 - self.b + self.b * self.lengths[i] / self.avg)
                out[i] += idf * tf * (self.k1 + 1) / norm
        return out


_INC_INDEX = BM25(
    (INCIDENTS["title"].fillna("") + " " + INCIDENTS["description"].fillna("") + " " + INCIDENTS["deployer"].fillna("")
     + " " + INCIDENTS["developer"].fillna("") + " " + INCIDENTS["implicated_systems"].fillna("")).tolist()
)
_INC_IDS = INCIDENTS["incident_id"].tolist()

# Long segments are mostly boilerplate past the start: index the first 3,000 characters
_SEG_INDEX = BM25(
    (SEGMENTS["doc_name"].fillna("") + " " + SEGMENTS["summary"].fillna("") + " " + SEGMENTS["text"].fillna("").str[:3000]).tolist()
)
_DOC_INDEX = BM25(
    (DOCS["name"].fillna("") + " " + DOCS["casual_name"].fillna("") + " " + DOCS["short_summary"].fillna("")
     + " " + DOCS["long_summary"].fillna("")).tolist()
)
_DOC_IDS = DOCS["agora_id"].tolist()

# Each document's full lowercase text, for keyword matching (coverage_matrix)
_DOC_TEXT = (
    DOCS["name"].fillna("") + " " + DOCS["casual_name"].fillna("") + " " + DOCS["short_summary"].fillna("") + " "
    + DOCS["long_summary"].fillna("")
).str.lower()
_DOC_HEAD = _DOC_TEXT.copy()
_seg_text = SEGMENTS.groupby("document_id")["text"].apply(lambda s: " ".join(s.fillna(""))).str.lower()
_DOC_TEXT = _DOC_TEXT + " " + _seg_text.reindex(DOCS.index).fillna("")


# --- Helpers for filters ---


def _match_name(value: str | None, options, what: str) -> str | None:
    """Accept an exact or case-insensitive partial name; raise with the valid options otherwise."""
    if value is None or value == "":
        return None
    options = [o for o in options if isinstance(o, str)]
    for o in options:
        if o.lower() == value.lower():
            return o
    partial = [o for o in options if value.lower() in o.lower()]
    if len(partial) == 1:
        return partial[0]
    raise ValueError(f"Unknown {what} '{value}'. Use one of: {sorted(options)}")


def _filter_incidents(use_case=None, risk_domain=None, risk_subdomain=None, intent=None, year_from=None,
                      year_to=None, include_secondary=False, keyword=None) -> pd.DataFrame:
    df = INCIDENTS
    if use_case:
        ucs = [_match_name(u, TAXONOMY.keys(), "use_case") for u in ([use_case] if isinstance(use_case, str) else use_case)]
        mask = df["use_case"].isin(ucs)
        if include_secondary:
            mask |= df["secondary_use_case"].isin(ucs)
        df = df[mask]
    if risk_domain:
        df = df[df["mit_risk_domain"] == _match_name(risk_domain, INCIDENTS["mit_risk_domain"].unique(), "risk_domain")]
    if risk_subdomain:
        df = df[df["mit_risk_subdomain"] == _match_name(risk_subdomain, INCIDENTS["mit_risk_subdomain"].unique(), "risk_subdomain")]
    if intent:
        df = df[df["mit_intent"] == _match_name(intent, INCIDENTS["mit_intent"].unique(), "intent")]
    if year_from:
        df = df[df["year"] >= int(year_from)]
    if year_to:
        df = df[df["year"] <= int(year_to)]
    if keyword:
        scores = _INC_INDEX.scores(keyword)
        hit_ids = {_INC_IDS[i] for i, s in scores.items() if s > 0}
        df = df[df["incident_id"].isin(hit_ids)].copy()
        df["_score"] = df["incident_id"].map({_INC_IDS[i]: s for i, s in scores.items()})
    return df


def _filters_used(**kw) -> dict:
    return {k: v for k, v in kw.items() if v not in (None, "", False)}


def _incident_card(row) -> dict:
    return {
        "cite": f"[AIID #{int(row['incident_id'])}]",
        "date": row["date"],
        "title": row["title"],
        "description": _clip(row["description"], 260),
        "deployer": _clean(row["deployer"]),
        "risk_subdomain": row["mit_risk_subdomain"],
        "intent": row["mit_intent"],
        "reports": int(row["report_count"]),
        "use_case_label_confidence": _clean(row["confidence"]),
    }


def _doc_card(row, summary_chars: int = 280) -> dict:
    return {
        "cite": f"[AGORA #{int(row['agora_id'])}]",
        "name": row["name"],
        "authority": row["authority"],
        "jurisdiction": row["jurisdiction"],
        "status": row["status"],
        "status_date": _clean(row["status_date"]),
        "proposed_date": _clean(row["proposed_date"]),
        "summary": _clip(row["short_summary"], summary_chars),
        "strategies": _tags(row["strategies"])[:8],
        "incentives": _tags(row["incentives"]),
        "applies_to": ", ".join(x for x, f in [("government", row["applies_government"]), ("private sector", row["applies_private"])] if f) or "unspecified",
    }


# --- Tools ---


def describe_data() -> dict:
    """What the two datasets hold: the options to choose from and what the data can't do."""
    uc_counts = INCIDENTS["use_case"].value_counts()
    return {
        "incidents": {
            "count": len(INCIDENTS),
            "years": [int(INCIDENTS["year"].min()), LATEST_YEAR],
            "partial_year": LATEST_YEAR,
            "latest_incident_date": MANIFEST.get("aiid_latest_incident_date"),
            "use_cases": {k: {"incidents": int(uc_counts.get(k, 0)), "about": v} for k, v in TAXONOMY.items()},
            "risk_domains": INCIDENTS["mit_risk_domain"].value_counts().to_dict(),
            "taxonomy_coverage": MANIFEST.get("coverage"),
        },
        "policies": {
            "count": len(DOCS),
            "status": DOCS["status"].value_counts().to_dict(),
            "jurisdictions": DOCS["jurisdiction"].value_counts().to_dict(),
            "top_authorities": DOCS["authority"].value_counts().head(8).to_dict(),
        },
        "caveats": MANIFEST.get("caveats", []) + [
            "Use-case labels were assigned to each incident by an LLM (Gemini Flash-Lite) from its title and description.",
        ],
    }


def search_incidents(use_case=None, risk_domain=None, risk_subdomain=None, keyword=None, intent=None,
                     year_from=None, year_to=None, include_secondary=False, limit=12) -> dict:
    df = _filter_incidents(use_case, risk_domain, risk_subdomain, intent, year_from, year_to, include_secondary, keyword)
    limit = max(1, min(int(limit or 12), 25))
    if keyword:
        df = df.sort_values("_score", ascending=False)
        order = "best keyword match first"
    else:
        df = df.sort_values(["report_count", "date"], ascending=False)
        order = "most-reported first"
    out = {
        "filters": _filters_used(use_case=use_case, risk_domain=risk_domain, risk_subdomain=risk_subdomain,
                                 keyword=keyword, intent=intent, year_from=year_from, year_to=year_to,
                                 include_secondary=include_secondary),
        "matched": len(df),
        "shown": min(limit, len(df)),
        "order": order,
        "subdomains_among_matches": df["mit_risk_subdomain"].value_counts().head(8).to_dict(),
        "incidents": [_incident_card(r) for _, r in df.head(limit).iterrows()],
    }
    if len(df) == 0:
        out["note"] = "No incidents match. Try a broader filter, include_secondary=true, or a keyword."
    return out


def get_incident(incident_id: int) -> dict:
    incident_id = int(incident_id)
    if incident_id not in INCIDENTS.index:
        return {"error": f"No incident {incident_id}."}
    row = INCIDENTS.loc[incident_id]
    keep = ["incident_id", "date", "title", "description", "deployer", "developer", "harmed", "implicated_systems",
            "report_count", "mit_risk_domain", "mit_risk_subdomain", "mit_responsible_entity", "mit_intent",
            "mit_timing", "use_case", "secondary_use_case", "confidence", "cset_tangible_harm", "cset_sector",
            "cset_country", "cset_lives_lost", "cset_injuries", "gmf_technical_failure", "editor_notes"]
    out = {k: _clean(row[k]) for k in keep if _clean(row[k]) not in (None, "")}
    out["cite"] = f"[AIID #{incident_id}]"
    out["url"] = AIID_URL.format(id=incident_id)
    return out


def count_incidents(group_by: str = "year", split_by: str | None = None, use_case=None, risk_domain=None,
                    risk_subdomain=None, keyword=None, intent=None, year_from=None, year_to=None,
                    include_secondary=False, top: int = 12) -> dict:
    if group_by not in GROUPS or (split_by and split_by not in GROUPS):
        raise ValueError(f"group_by and split_by must be one of {list(GROUPS)}")
    df = _filter_incidents(use_case, risk_domain, risk_subdomain, intent, year_from, year_to, include_secondary, keyword)
    total = int(df["incident_id"].nunique())
    g = GROUPS[group_by]
    counts = df.groupby(g)["incident_id"].nunique().sort_index() if group_by == "year" else \
        df.groupby(g)["incident_id"].nunique().sort_values(ascending=False)
    if group_by != "year":
        counts = counts.head(max(1, min(int(top or 12), 30)))
    rows = [{group_by: _clean(k), "incidents": int(v), "share": round(v / total, 3) if total else 0} for k, v in counts.items()]
    out = {
        "filters": _filters_used(use_case=use_case, risk_domain=risk_domain, risk_subdomain=risk_subdomain,
                                 keyword=keyword, intent=intent, year_from=year_from, year_to=year_to,
                                 include_secondary=include_secondary),
        "group_by": group_by,
        "unique_incidents": total,
        "rows": rows,
    }
    if split_by:
        s = GROUPS[split_by]
        top_split = df[s].value_counts().head(6).index.tolist()
        pivot = df.assign(_s=df[s].where(df[s].isin(top_split), "Other")).groupby([g, "_s"])["incident_id"].nunique()
        out["split_by"] = split_by
        out["split"] = [{group_by: _clean(a), split_by: b, "incidents": int(v)} for (a, b), v in pivot.items()
                        if group_by != "year" or a in counts.index]
    notes = []
    if group_by == "year" or year_to is None or int(year_to or 0) >= LATEST_YEAR:
        notes.append(f"{LATEST_YEAR} is a partial year (data ends {MANIFEST.get('aiid_latest_incident_date')}). Compare full years only.")
    notes.append("Counts are reported incidents curated by AIID editors, not true incident rates.")
    if group_by in ("risk_domain", "risk_subdomain", "intent", "responsible_entity", "timing"):
        unc = int((df[g] == UNCLASSIFIED).sum())
        if unc:
            notes.append(f"{unc} of {total} matched incidents have no MIT classification.")
    out["notes"] = notes
    return out


def _period(p: str) -> tuple[int, int]:
    m = re.fullmatch(r"\s*(\d{4})\s*(?:-\s*(\d{4}))?\s*", str(p))
    if not m:
        raise ValueError(f"Period '{p}' must look like '2020-2022' or '2024'.")
    a = int(m.group(1))
    return a, int(m.group(2) or a)


def compare_periods(period_a: str, period_b: str, group_by: str = "risk_domain", use_case=None, risk_domain=None,
                    keyword=None, include_secondary=False) -> dict:
    if group_by not in GROUPS or group_by == "year":
        raise ValueError(f"group_by must be one of {[g for g in GROUPS if g != 'year']}")
    (a0, a1), (b0, b1) = _period(period_a), _period(period_b)
    g = GROUPS[group_by]
    res = {}
    for name, (y0, y1) in (("a", (a0, a1)), ("b", (b0, b1))):
        df = _filter_incidents(use_case, risk_domain, None, None, y0, y1, include_secondary, keyword)
        res[name] = (df["incident_id"].nunique(), df.groupby(g)["incident_id"].nunique(), y1 - y0 + 1)
    keys = res["a"][1].index.union(res["b"][1].index)
    rows = []
    for k in keys:
        ca, cb = int(res["a"][1].get(k, 0)), int(res["b"][1].get(k, 0))
        sa = ca / res["a"][0] if res["a"][0] else 0
        sb = cb / res["b"][0] if res["b"][0] else 0
        rows.append({group_by: k, "count_a": ca, "count_b": cb, "share_a": round(sa, 3), "share_b": round(sb, 3),
                     "share_change_pts": round(100 * (sb - sa), 1)})
    rows.sort(key=lambda r: -(r["count_a"] + r["count_b"]))
    out = {
        "period_a": f"{a0}-{a1}", "period_b": f"{b0}-{b1}", "group_by": group_by,
        "filters": _filters_used(use_case=use_case, risk_domain=risk_domain, keyword=keyword, include_secondary=include_secondary),
        "total_a": int(res["a"][0]), "total_b": int(res["b"][0]),
        "per_year_a": round(res["a"][0] / res["a"][2], 1), "per_year_b": round(res["b"][0] / res["b"][2], 1),
        "rows": rows[:15],
        "notes": ["Shares are within each period, so they compare the mix of failures even when total reporting grew."],
    }
    if max(a1, b1) >= LATEST_YEAR:
        out["notes"].append(f"{LATEST_YEAR} is a partial year: its totals are lower than a full year's.")
    return out


def _filter_docs(status=None, jurisdiction=None, authority=None, applies_private=None, proposed_from=None,
                 tags=None) -> pd.DataFrame:
    df = DOCS
    if status:
        df = df[df["status"] == _match_name(status, DOCS["status"].unique(), "status")]
    if jurisdiction:
        df = df[df["jurisdiction"] == _match_name(jurisdiction, DOCS["jurisdiction"].unique(), "jurisdiction")]
    if authority:
        df = df[df["authority"].fillna("").str.contains(authority, case=False, regex=False)]
    if applies_private is not None:
        df = df[df["applies_private"] == bool(applies_private)]
    if proposed_from:
        df = df[df["proposed_date"].fillna("0000").str[:4].astype(int) >= int(proposed_from)]
    for tag in tags or []:
        tag = str(tag).strip().lower()
        has = pd.Series(False, index=df.index)
        for col in TAG_COLUMNS:
            has |= df[col].fillna("").str.lower().apply(lambda v: any(t.strip() == tag or t.strip().startswith(tag + ":") for t in v.split(";")))
        df = df[has]
    return df


def search_policies(query=None, tags=None, status=None, jurisdiction=None, authority=None, applies_private=None,
                    proposed_from=None, limit=10) -> dict:
    df = _filter_docs(status, jurisdiction, authority, applies_private, proposed_from, tags)
    limit = max(1, min(int(limit or 10), 20))
    if query:
        scores = _DOC_INDEX.scores(query)
        by_id = {_DOC_IDS[i]: s for i, s in scores.items() if s > 0}
        df = df[df["agora_id"].isin(by_id)].copy()
        df["_score"] = df["agora_id"].map(by_id)
        df = df.sort_values("_score", ascending=False)
    else:
        df = df.sort_values("status_date", ascending=False)
    out = {
        "filters": _filters_used(query=query, tags=tags, status=status, jurisdiction=jurisdiction, authority=authority,
                                 applies_private=applies_private, proposed_from=proposed_from),
        "matched": len(df),
        "status_among_matches": df["status"].value_counts().to_dict(),
        "documents": [_doc_card(r) for _, r in df.head(limit).iterrows()],
    }
    if len(df) == 0:
        out["note"] = "No documents match. Try search_policy_text, which searches the full text, or fewer filters."
    return out


def search_policy_text(query: str, status=None, jurisdiction=None, limit=8) -> dict:
    """Search the text of policy segments (sections). Best for specific provisions."""
    scores = _SEG_INDEX.scores(query)
    seg = SEGMENTS.iloc[[i for i, s in sorted(scores.items(), key=lambda x: -x[1])[:400]]].copy()
    seg["_score"] = [scores[i] for i in seg.index]
    if status:
        seg = seg[seg["doc_status"] == _match_name(status, DOCS["status"].unique(), "status")]
    if jurisdiction:
        seg = seg[seg["jurisdiction"].fillna("Unknown") == _match_name(jurisdiction, DOCS["jurisdiction"].unique(), "jurisdiction")]
    seg = seg[~seg["non_operative"].fillna(False)]
    limit = max(1, min(int(limit or 8), 15))
    seen, hits = set(), []
    for _, r in seg.iterrows():  # best segment per document
        if r["document_id"] in seen:
            continue
        seen.add(r["document_id"])
        doc = DOCS.loc[r["document_id"]]
        hits.append({
            "cite": f"[AGORA #{int(r['document_id'])}]",
            "document": doc["name"],
            "authority": doc["authority"],
            "status": doc["status"],
            "status_date": _clean(doc["status_date"]),
            "segment_summary": _clip(r["summary"], 240),
            "excerpt": _clip(r["text"], 420),
        })
        if len(hits) >= limit:
            break
    return {"query": query, "filters": _filters_used(status=status, jurisdiction=jurisdiction), "documents": hits,
            "note": "Each hit is the best-matching section of a document. Keyword relevance is not legal applicability."}


def get_policy(agora_id: int, query: str | None = None) -> dict:
    agora_id = int(agora_id)
    if agora_id not in DOCS.index:
        return {"error": f"No AGORA document {agora_id}."}
    row = DOCS.loc[agora_id]
    out = _doc_card(row, summary_chars=900)
    out.update({
        "casual_name": _clean(row["casual_name"]),
        "long_summary": _clip(row["long_summary"], 1500),
        "harms": _tags(row["harms"]),
        "risk_factors": _tags(row["risk_factors"]),
        "applications": _tags(row["applications"]),
        "strategies": _tags(row["strategies"]),
        "tags_may_be_unreviewed_machine_output": bool(row["machine_output"]),
        "source_link": _clean(row["link"]),
        "url": AGORA_URL.format(id=agora_id),
    })
    segs = SEGMENTS[(SEGMENTS["document_id"] == agora_id) & ~SEGMENTS["non_operative"].fillna(False)]
    if query and len(segs):
        idx = BM25((segs["summary"].fillna("") + " " + segs["text"].fillna("")).tolist())
        sc = idx.scores(query)
        segs = segs.iloc[[i for i, _ in sorted(sc.items(), key=lambda x: -x[1])[:3]]] if sc else segs.head(3)
    else:
        segs = segs.head(3)
    out["sections"] = [{"summary": _clip(r["summary"], 300), "excerpt": _clip(r["text"], 600)} for _, r in segs.iterrows()]
    return out


def risks_to_policy_tags(risk_domain: str) -> dict:
    rd = _match_name(risk_domain, CROSSWALK["mit_risk_domain"].unique(), "risk_domain")
    rows = CROSSWALK[CROSSWALK["mit_risk_domain"] == rd]
    return {"risk_domain": rd, "agora_tags": rows["agora_tag"].tolist(),
            "note": "Hand-made mapping by the project authors, not an official crosswalk. Use the tags in search_policies(tags=[...])."}


def _docs_for_use_case(use_case: str | None, extra_keywords=None) -> tuple[pd.Series, list[str]]:
    """Documents about the use case, with how often they mention it. A document counts if a phrase appears in
    its name or summaries, or at least 3 times in its text: one passing mention is not a policy about it."""
    words = list(POLICY_KEYWORDS.get(use_case, [])) if use_case else []
    words += [w.lower() for w in (extra_keywords or []) if w]
    if not words:
        return pd.Series(1, index=DOCS.index), []
    pattern = re.compile("|".join(r"\b" + re.escape(w.lower()) for w in words))
    hits = _DOC_TEXT.apply(lambda t: len(pattern.findall(t)))
    in_head = _DOC_HEAD.apply(lambda t: bool(pattern.search(t)))
    keep = in_head | (hits >= 3)
    return hits[keep], words


def policy_keywords(use_case: str) -> dict:
    uc = _match_name(use_case, TAXONOMY.keys(), "use_case")
    return {"use_case": uc, "keywords": POLICY_KEYWORDS.get(uc, []),
            "note": "Hand-written search phrases. Try them in search_policy_text, one or two at a time."}


def coverage_matrix(use_case: str | None = None, extra_keywords: list[str] | None = None, jurisdiction=None,
                    year_from=None, year_to=None) -> dict:
    """For each MIT risk domain: how many incidents, and how many policy documents that mention the use case
    also carry a tag mapped to that risk domain, by status."""
    uc = _match_name(use_case, TAXONOMY.keys(), "use_case") if use_case else None
    inc = _filter_incidents(use_case=uc, year_from=year_from, year_to=year_to)
    hits, words = _docs_for_use_case(uc, extra_keywords)
    docs = DOCS.loc[hits.index].assign(_hits=hits.values)
    if jurisdiction:
        docs = docs[docs["jurisdiction"] == _match_name(jurisdiction, DOCS["jurisdiction"].unique(), "jurisdiction")]
    tagsets = docs.apply(lambda r: {f"{c}|{t}" for c in ("harms", "risk_factors") for t in _tags(r[c])}, axis=1)
    rows = []
    for domain, n in inc["mit_risk_domain"].value_counts().items():
        if domain == UNCLASSIFIED:
            continue
        cw = CROSSWALK[CROSSWALK["mit_risk_domain"] == domain]
        wanted = {f"{c}|{t}" for c, t in zip(cw["agora_column"], cw["agora_tag"])}
        match = docs[tagsets.apply(lambda s: bool(s & wanted))] if len(docs) else docs
        by_status = match["status"].value_counts().to_dict() if len(match) else {}
        enacted = match[match["status"] == "Enacted"].sort_values("_hits", ascending=False)
        rows.append({
            "risk_domain": domain,
            "incidents": int(n),
            "policies_enacted": int(by_status.get("Enacted", 0)),
            "policies_proposed": int(by_status.get("Proposed", 0)),
            "policies_defunct": int(by_status.get("Defunct", 0)),
            "example_enacted": [f"[AGORA #{int(i)}] {_clip(DOCS.loc[i, 'name'], 70)}" for i in enacted["agora_id"].head(3)],
            "coverage": "enacted" if by_status.get("Enacted") else ("proposed only" if by_status.get("Proposed") else "none found"),
        })
    return {
        "use_case": uc or "all",
        "jurisdiction": jurisdiction,
        "incidents_matched": int(inc["incident_id"].nunique()),
        "policy_docs_mentioning_use_case": int(len(docs)),
        "policy_docs_by_status": docs["status"].value_counts().to_dict(),
        "keywords_used": words,
        "rows": rows,
        "method": ("A policy counts for a risk domain if it is about the use case (a keyword in its name or summaries, "
                   "or 3+ mentions in its text) and "
                   "carries an AGORA harm or risk-factor tag that the hand-made crosswalk maps to that domain. "
                   "Only annotated AGORA documents have tags. Defunct documents are not in force."),
    }


# --- For the report and the page: the chart for a brief, its facts, and the incidents behind it ---


def chart_for_scope(use_cases=None, year_from=None, year_to=None, split_by: str = "risk_domain") -> dict:
    """The report's chart, computed from the brief's scope (not from whichever count an agent made last),
    with facts in plain sentences that the Writer must use for any trend number."""
    c = count_incidents("year", split_by=split_by, use_case=use_cases or None, year_from=year_from, year_to=year_to)
    rows = c["rows"]
    out = {"group_by": "year", "rows": rows, "split_by": split_by, "split": c.get("split", []),
           "filters": {"use_cases": use_cases or [], "year_from": year_from, "year_to": year_to},
           "partial_year": LATEST_YEAR, "latest_date": MANIFEST.get("aiid_latest_incident_date"),
           "top": []}
    split_totals: dict[str, int] = {}
    for r in out["split"]:
        split_totals[r[split_by]] = split_totals.get(r[split_by], 0) + r["incidents"]
    out["top"] = [k for k in split_totals if k != "Other"]
    out["facts"] = chart_facts(rows, out["split"], split_by, c["unique_incidents"])
    return out


def chart_facts(rows: list[dict], split: list[dict], split_by: str, total: int) -> list[str]:
    by_year = {r["year"]: r["incidents"] for r in rows}
    if not by_year:
        return ["No incidents match this scope."]
    facts = [f"{total} reported incidents in scope, {min(by_year)}–{max(by_year)}."]
    full = {y: n for y, n in by_year.items() if y < LATEST_YEAR}
    if full:
        peak = max(full, key=lambda y: (full[y], y))
        facts.append(f"Peak full year: {peak}, with {full[peak]} incidents.")
        last = max(full)
        recent = list(range(last - 2, last + 1))
        before = list(range(last - 5, last - 2))
        n_recent, n_before = sum(full.get(y, 0) for y in recent), sum(full.get(y, 0) for y in before)
        facts.append(f"{recent[0]}–{recent[-1]}: {n_recent} incidents; {before[0]}–{before[-1]}: {n_before} incidents.")
        if split:
            def top_in(years):
                t: dict[str, int] = {}
                for r in split:
                    if r["year"] in years and r[split_by] not in ("Other", UNCLASSIFIED):
                        t[r[split_by]] = t.get(r[split_by], 0) + r["incidents"]
                if not t:
                    return None
                k = max(t, key=t.get)
                n = sum(full.get(y, 0) for y in years)
                return k, t[k], n
            for years in (recent, before):
                top = top_in(years)
                if top and top[2]:
                    facts.append(f"Largest {split_by.replace('_', ' ')} in {years[0]}–{years[-1]}: {top[0]} "
                                 f"({top[1]} of {top[2]}, {round(100 * top[1] / top[2])}%).")
    if LATEST_YEAR in by_year:
        facts.append(f"{LATEST_YEAR} so far (data ends {MANIFEST.get('aiid_latest_incident_date')}): "
                     f"{by_year[LATEST_YEAR]} incidents. A partial year: not comparable to full years.")
    if total < 20:
        facts.append("Fewer than 20 incidents: too few to call a trend.")
    return facts


def list_incidents(use_cases=None, year_from=None, year_to=None, year=None, split_by=None, split_value=None,
                   exclude=None, offset: int = 0, limit: int | None = 25) -> dict:
    """The incidents behind a chart bar or table cell, for the page's drawer (paged) or CSV (all)."""
    df = _filter_incidents(use_case=use_cases or None, year_from=year_from, year_to=year_to)
    if year:
        df = df[df["year"] == int(year)]
    if split_by in GROUPS and split_value:
        col = GROUPS[split_by]
        if split_value == "Other":
            df = df[~df[col].isin(exclude or [])]
        else:
            df = df[df[col] == split_value]
    df = df.sort_values("date", ascending=False, kind="stable")
    total = len(df)
    if limit is not None:
        df = df.iloc[int(offset): int(offset) + int(limit)]
    cols = ["incident_id", "date", "title", "deployer", "use_case", "mit_risk_domain", "mit_risk_subdomain",
            "mit_intent", "report_count", "confidence", "description"]
    items = [{k: _clean(r[k]) for k in cols} | {"url": AIID_URL.format(id=int(r["incident_id"]))} for _, r in df.iterrows()]
    return {"total": total, "offset": int(offset), "items": items}


if __name__ == "__main__":
    # Self-check: uv run data_tools.py
    d = describe_data()
    assert d["incidents"]["count"] == 1784 and d["policies"]["count"] == 1255
    s = search_incidents(use_case="hiring", limit=3)
    assert s["matched"] > 20 and s["incidents"], s
    c = count_incidents("year", split_by="risk_domain", use_case="Synthetic media and deepfakes")
    assert sum(r["incidents"] for r in c["rows"]) == c["unique_incidents"]
    print(json.dumps(compare_periods("2020-2022", "2023-2025", use_case="Chatbots"), indent=1)[:800])
    print(json.dumps(search_policy_text("automated employment decision tool bias audit", limit=3), indent=1)[:1500])
    print(json.dumps(coverage_matrix("Hiring and employment", jurisdiction="United States"), indent=1)[:2000])
    print(json.dumps(get_policy(s["incidents"][0]["cite"] and 1, query="data"), indent=1)[:600])
    print("ok")
