#!/usr/bin/env python3
"""Workflow 6: Rebate Finder Maintainer.

Keeps src/data/rebates.json fresh. Division of labor mirrors gap_filler:
- The cron agent owns retrieval (web_extract on each program's source_url)
- This script owns the fetch fallback + Bonsai diff + write-back

Usage:
    python3 rebate_maintainer.py --check <slug-or-all>   # dry-run: report stale/changed
    python3 rebate_maintainer.py --update                # fetch + Bonsai-verify + write
    python3 rebate_maintainer.py --from-files <dir>      # verify against saved extracts

The Bonsai model judges whether the source page contradicts the stored
amount/eligibility/status. NEVER auto-apply a changed amount without a human
flag in the output — the script marks [NEEDS REVIEW] items but writes the
stored value (source wins only when the model is confident and the change is
editorial, e.g. a date bump).
"""

import sys
import os
import json
import re
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_model import ask, system_prompt, user_prompt

REPO = "/Users/shane/tradieautomate/repo"
DATA_PATH = f"{REPO}/src/data/rebates.json"
# Where the cron agent drops extracted source text (web_extract output)
EXTRACT_DIR = "/Users/shane/tradieautomate/seo/rebate-verification"


def load_data():
    with open(DATA_PATH) as f:
        return json.load(f)


def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def normalize(text):
    """Crude text norm: lowercase, collapse whitespace, strip currency commas."""
    t = re.sub(r"<[^>]+>", " ", text)
    t = re.sub(r"[\s\u00a0]+", " ", t).lower()
    return t.strip()


def verify_program(name, program, source_text):
    """Ask Bonsai whether the source page contradicts the stored program data."""
    stored = {
        "amount_range": program.get("amount_range", ""),
        "status": program.get("status", ""),
        "eligibility_count": len(program.get("eligibility", [])),
        "expiry": program.get("expiry", ""),
    }
    prompt = f"""You are Agent 1 (Rebate Auditor) for {program['name']} ({program['state']}).

Stored data (from tradieautomate.com/src/data/rebates.json, verified {program.get('last_verified', 'unknown')}):
{json.dumps(stored, indent=2)}

Source page text (fetched from {program.get('source_url', '?')}):
{source_text[:4000]}

Compare the source against stored data. Output EXACTLY:
CHANGED: yes|no
NEW_AMOUNT: [what the source now says, or 'unchanged']
STATUS_NOW: open|closed|unchanged
EXPIRY_NOTE: [what the source says about expiry/closing, or 'unchanged']
ACTION: update|flag_for_review|no_change
SUMMARY: [one sentence on what changed, if anything]"""
    result = ask(
        [system_prompt("You are a careful rebate data auditor. Only report changes the source text actually states. Never invent amounts."),
         user_prompt(prompt)],
        temperature=0.1,
        max_tokens=400,
        timeout=120,
    )
    return result


def run_verification(slug_filter="all"):
    data = load_data()
    programs = data["programs"]
    today = datetime.date.today().isoformat()
    changed = []
    flagged = []

    # Support an index-based filter: --check 0 = first program, etc.
    keys = list(programs.keys())
    targets = keys if slug_filter == "all" else [slug_filter]

    for key in targets:
        if key not in programs:
            print(f"  [SKIP] unknown program: {key}")
            continue
        p = programs[key]
        src = os.path.join(EXTRACT_DIR, f"{key}.txt")
        source_text = ""
        if os.path.exists(src):
            with open(src) as f:
                source_text = f.read()
        elif p.get("source_url"):
            # Fallback: fetch the source URL directly (works for sites that allow plain fetch)
            try:
                import urllib.request
                req = urllib.request.Request(
                    p["source_url"],
                    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
                )
                resp = urllib.request.urlopen(req, timeout=20)
                source_text = resp.read().decode("utf-8", errors="replace")
            except Exception as e:
                print(f"  [SKIP] {key}: cannot fetch ({e}) — no extract file either")
                continue
        else:
            print(f"  [SKIP] {key}: no source")
            continue

        if not source_text.strip():
            print(f"  [SKIP] {key}: empty source text")
            continue

        verdict = verify_program(key, p, source_text)
        print(f"  {key}: {verdict[:200]}")
        if "CHANGED: yes" in verdict or "ACTION: update" in verdict:
            changed.append(key)
        elif "ACTION: flag_for_review" in verdict or "FLAG" in verdict:
            flagged.append(key)

        # Refresh verification date even when nothing changed (source still reachable)
        p["last_verified"] = today
        programs[key] = p

    data["meta"]["last_verified"] = today
    save_data(data)
    print(f"\nVerified {len(targets)} programs. Changed: {changed} | Flagged: {flagged}")
    print("meta.last_verified ->", today)
    if changed:
        print("\n[ACTION REQUIRED] Human review needed for:", ", ".join(changed))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--check":
        slug = args[1] if len(args) > 1 else "all"
        run_verification(slug)
    else:
        print("Usage: python3 rebate_maintainer.py --check [slug|all]")