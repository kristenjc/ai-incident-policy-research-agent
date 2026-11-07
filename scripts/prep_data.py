"""Offline build step: raw AIID + AGORA exports -> slim, agent-ready CSVs in data/processed/.

    uv run scripts/prep_data.py build
    uv run scripts/prep_data.py build --aiid path/to/AIID_Excel_Export-XXXX.xlsx --agora-dir path/to/agora_csvs --out data/processed

Defaults: data/raw/AIID_Excel_Export*.xlsx and data/raw/agora/{documents,segments,authorities}.csv
(or put the AGORA CSVs directly in data/raw/).

Outputs
  incidents.csv        1 row per AIID incident: identity, MIT risk class, selected CSETv1/GMF fields, citation url
  agora_documents.csv  1 row per AGORA document: metadata, status, summaries, tags as '; ' lists
  agora_segments.csv   1 row per AI-related segment: text, summary, tags, plus the doc's name/status/jurisdiction
  risk_crosswalk.csv   DRAFT hand-made map: MIT risk domain -> AGORA harm / risk-factor tags (review it!)
  MANIFEST.json        provenance, row counts, coverage and caveats (paste into README / agent prompt)

Deliberately dropped: AIID Reports sheet (no incident id to join on), Entities sheet (ids + names only),
Editors/hash columns, ~20 sparse CSETv1 columns, AGORA's 99 one-hot tag columns (folded into 5 list
columns), AGORA plaintext/pdf retrieval bookkeeping, and segments flagged 'Not AI-related'.
"""

import pandas as pd
import argparse
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

# AIID incidents sheet: raw column -> our name. Everything not listed is dropped.
AIID_KEEP = {
    "Incident ID": "incident_id", "date": "date", "year": "year", "title": "title",
    "description": "description", "deployer": "deployer", "developer": "developer", "harmed": "harmed",
    "Implicated Systems": "implicated_systems", "report_count": "report_count", "Data Sources": "taxonomies",
    # MIT risk taxonomy: ~84% of incidents. The backbone for "failure patterns".
    "Risk Domain": "mit_risk_domain", "Risk Subdomain": "mit_risk_subdomain",
    "Responsible Entity": "mit_responsible_entity", "Intent": "mit_intent", "Timing": "mit_timing",
    # CSETv1: ~11% of incidents. Kept: harm severity, sector, geography, who was affected.
    "Tangible Harm": "cset_tangible_harm", "AI Harm Level": "cset_ai_harm_level",
    "Rights Violation": "cset_rights_violation", "Lives Lost": "cset_lives_lost", "Injuries": "cset_injuries",
    "Sector of Deployment": "cset_sector", "Public Sector Deployment": "cset_public_sector",
    "Location Region": "cset_region", "Country Code": "cset_country", "AI Task": "cset_ai_task",
    "Autonomy Level": "cset_autonomy", "Involving Minor": "cset_involving_minor",
    "Protected Characteristic": "cset_protected_characteristic",
    # GMF: ~1-2% of incidents. Few rows, but it is the only 'what technically failed' field.
    "Technical Failure": "gmf_technical_failure", "AI Technology": "gmf_ai_technology", "AI Goal": "gmf_ai_goal",
    # Editors' caveats ("borderline incident", "should be an issue"): 30% populated, useful for honesty.
    "Editor Notes": "editor_notes",
}
TAG_GROUPS = ["Applications", "Harms", "Incentives", "Risk factors", "Strategies"]

DOC_KEEP = {
    "AGORA ID": "agora_id", "Official name": "name", "Casual name": "casual_name", "Link to document": "link",
    "Authority": "authority", "Collections": "collections", "Most recent activity": "status",
    "Most recent activity date": "status_date", "Proposed date": "proposed_date", "Annotated?": "annotated",
    "Validated?": "validated", "Primarily applies to the government": "applies_government",
    "Primarily applies to the private sector": "applies_private", "Short summary": "short_summary",
    "Long summary": "long_summary", "Summaries and tags may include unreviewed machine output": "machine_output",
    "Number of segments created": "n_segments",
}
SEG_KEEP = {
    "Document ID": "document_id", "Segment position": "position", "Text": "text", "Summary": "summary",
    "Non-operative": "non_operative", "Segment annotated": "annotated", "Segment validated": "validated",
    "Summaries and tags may include unreviewed machine output": "machine_output",
}

# Risk Crosswalk between MIT AI Risk Repository domain -> AGORA tags (not official mapping). 
CROSSWALK = {
    "Discrimination and Toxicity": ["Risk factors: Bias", "Harms: Discrimination", "Harms: Detrimental content"],
    "Privacy & Security": ["Risk factors: Privacy", "Risk factors: Security", "Risk factors: Security: Cybersecurity",
                           "Harms: Violation of civil or human rights, including privacy"],
    "Misinformation": ["Harms: Detrimental content", "Risk factors: Security: Dissemination"],
    "Malicious Actors & Misuse": ["Risk factors: Security", "Risk factors: Security: Cybersecurity",
                                  "Risk factors: Security: Dissemination", "Harms: Financial loss"],
    "Human-Computer Interaction": ["Risk factors: Transparency", "Risk factors: Interpretability and explainability",
                                   "Risk factors: Safety"],
    "Socioeconomic & Environmental Harms": ["Harms: Ecological harm", "Harms: Financial loss"],
    "AI system safety, failures, and limitations": ["Risk factors: Reliability", "Risk factors: Reliability: Robustness",
                                                    "Risk factors: Safety", "Harms: Harm to health/safety",
                                                    "Harms: Harm to property", "Harms: Harm to infrastructure"],
}


def is_true(s: pd.Series) -> pd.Series:
    """AGORA mixes 'true'/'false' and 'True'/'False' between columns."""
    return s.astype(str).str.strip().str.lower().eq("true")


def listify(v) -> str:
    """'["a", "b"]' -> 'a; b'. Plain strings and blanks pass through."""
    if pd.isna(v):
        return ""
    v = str(v).strip()
    if v.startswith("["):
        try:
            return "; ".join(str(x) for x in json.loads(v))
        except ValueError:
            pass
    return v


def fold_tags(df: pd.DataFrame) -> pd.DataFrame:
    """One-hot 'Group: Tag' columns -> one 'a; b; c' column per group."""
    out = pd.DataFrame(index=df.index)
    for g in TAG_GROUPS:
        cols = [c for c in df.columns if c.startswith(g + ":")]
        flags = pd.DataFrame({c: is_true(df[c]) for c in cols})
        names = [c[len(g) + 1:].strip() for c in cols]
        out[g.lower().replace(" ", "_")] = flags.apply(lambda r: "; ".join(n for n, f in zip(names, r) if f), axis=1)
    return out


def read_aiid(path: Path) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name="Incidents", header=None, dtype=str)
    header_row = raw.index[raw.iloc[:, 0] == "Incident ID"][0]  # the sheet has banner rows above the header
    df = raw.iloc[header_row + 1:].copy()
    df.columns = raw.iloc[header_row]
    return df.reset_index(drop=True)


def build_incidents(path: Path) -> pd.DataFrame:
    df = read_aiid(path)
    missing = [c for c in AIID_KEEP if c not in df.columns]
    if missing:
        print("  ! AIID columns not found (renamed upstream?):", missing)
    df = df[[c for c in AIID_KEEP if c in df.columns]].rename(columns=AIID_KEEP)
    df["date"] = df["date"].str[:10]
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    for c in df.columns:
        if c not in ("incident_id", "year", "date", "report_count"):
            df[c] = df[c].map(listify)
    df["url"] = "https://incidentdatabase.ai/cite/" + df["incident_id"] + "/"  # the citation the agent uses
    return df


def build_agora(src: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    read = lambda n: pd.read_csv(src / n, dtype=str, keep_default_na=False)
    docs, segs, auth = read("documents.csv"), read("segments.csv"), read("authorities.csv")

    d = pd.concat([docs[list(DOC_KEEP)].rename(columns=DOC_KEEP), fold_tags(docs)], axis=1)
    d = d.merge(auth[["Name", "Jurisdiction"]].rename(columns={"Name": "authority", "Jurisdiction": "jurisdiction"}),
                on="authority", how="left")
    for c in ("annotated", "validated", "applies_government", "applies_private", "machine_output"):
        d[c] = is_true(d[c])
    for c in ("status_date", "proposed_date"):  # one raw date is '7202-..': keep only plausible years
        yr = pd.to_numeric(d[c].str[:4], errors="coerce")
        d[c] = d[c].where(yr.between(2000, 2030), "")

    s = pd.concat([segs[list(SEG_KEEP)].rename(columns=SEG_KEEP), fold_tags(segs)], axis=1)
    s = s[~is_true(segs["Not AI-related"])]            # noise: provisions that don't concern AI
    s = s[s["document_id"].isin(d["agora_id"])]         # orphans (no document row)
    for c in ("non_operative", "annotated", "validated", "machine_output"):
        s[c] = is_true(s[c])
    s.insert(0, "segment_id", s["document_id"] + ":" + s["position"])
    meta = d[["agora_id", "name", "authority", "jurisdiction", "status"]].rename(
        columns={"agora_id": "document_id", "name": "doc_name", "status": "doc_status"})
    s = s.merge(meta, on="document_id", how="left")  # denormalised so filtering to 'Enacted' needs no join
    return d, s


def build(aiid: Path, agora: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    inc = build_incidents(aiid)
    docs, segs = build_agora(agora)
    inc.to_csv(out / "incidents.csv", index=False)
    docs.to_csv(out / "agora_documents.csv", index=False)
    segs.to_csv(out / "agora_segments.csv", index=False)
    # agora_column matches the list columns of agora_documents/segments ('harms', 'risk_factors'); agora_tag
    # is one item inside that column.
    pd.DataFrame([(k, t.split(": ", 1)[0].lower().replace(" ", "_"), t.split(": ", 1)[1])
                  for k, v in CROSSWALK.items() for t in v],
                 columns=["mit_risk_domain", "agora_column", "agora_tag"]).to_csv(out / "risk_crosswalk.csv", index=False)

    has = lambda col: float((inc[col] != "").mean().round(3))
    manifest = {
        "built": date.today().isoformat(),
        "aiid_source": aiid.name, "agora_source": "documents.csv, segments.csv, authorities.csv",
        "counts": {"incidents": len(inc), "agora_documents": len(docs), "agora_segments_kept": len(segs)},
        "aiid_latest_incident_date": inc["date"].max(),
        "aiid_year_range": [int(inc["year"].min()), int(inc["year"].max())],
        "coverage": {"mit_risk_class": has("mit_risk_domain"), "csetv1": has("cset_tangible_harm"),
                     "gmf": has("gmf_technical_failure")},
        "agora_status_counts": docs["status"].value_counts().to_dict(),
        "agora_jurisdiction_counts": docs["jurisdiction"].fillna("").value_counts().to_dict(),
        "agora_annotated_docs": int(docs["annotated"].sum()),
        "agora_segments_with_tags": int((segs[[c.lower().replace(" ", "_") for c in TAG_GROUPS]] != "").any(axis=1).sum()),
        "caveats": [
            "AIID counts reflect news coverage and editor curation, not true incident rates.",
            "The latest AIID year is partial. Compare full years only.",
            "Only the MIT taxonomy covers most incidents; CSETv1 and GMF cover a small minority.",
            "AGORA is dominated by US documents and many are proposed or defunct bills, not law in force.",
            "AGORA tags exist only for annotated documents/segments; some are unreviewed machine output.",
            "AGORA is not a complete record of AI-relevant law.",
            "risk_crosswalk.csv (MIT risk domain -> AGORA tags) is hand-made by the project authors, "
            "not an official mapping. It reflects judgment calls and has not been validated.",
        ],
    }
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))
    for p in sorted(out.glob("*")):
        print(f"{p.name:22s}{p.stat().st_size / 1e6:7.2f} MB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build"])
    ap.add_argument("--aiid", type=Path)
    ap.add_argument("--agora-dir", type=Path)
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "processed")
    a = ap.parse_args()
    raw = ROOT / "data" / "raw"
    aiid = a.aiid or next(iter(sorted(raw.glob("AIID_Excel_Export*.xlsx"))), None)
    agora = a.agora_dir or (raw / "agora" if (raw / "agora" / "documents.csv").exists() else raw)
    if not aiid or not (agora / "documents.csv").exists():
        raise SystemExit("Put the AIID .xlsx and AGORA CSVs under data/raw/, or pass --aiid and --agora-dir.")
    build(aiid, agora, a.out)
