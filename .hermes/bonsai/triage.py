#!/usr/bin/env python3
"""Workflow 3: Queue Triage Prioritizer

Scores each actionable fix_queue item by estimated effort and business impact,
then ranks by impact-per-effort. Writes back to fix_queue.

Recently-updated pages are NOT sent to the model: their meta/content was
changed inside the GSC window, so any further fix is wasted effort. They are
recorded deterministically as effort=0 / impact=0 / monitoring and excluded
from ranked_actions.

Scoring is resilient to reasoning-model output drift: lines are parsed by
slug (not by index), unmatched items are retried once, and anything still
unscored is marked `triage_scored: false` instead of silently defaulting to 0.

Usage:
    python3 triage.py                    # Process all queue items
    python3 triage.py --dry-run          # Print rankings without writing
"""

import sys
import os
import json
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_model import ask, system_prompt, user_prompt

FIX_QUEUE = "/Users/shane/tradieautomate/fix_queue.json"
BATCH = 8


def read_queue():
    with open(FIX_QUEUE) as f:
        return json.load(f)


def write_queue(q):
    with open(FIX_QUEUE, "w") as f:
        json.dump(q, f, indent=2)


def build_prompt(batch, n):
    lines = [
        f"{item['slug']} | tier={item['tier']} pos={item['position']} "
        f"imp={item['impressions']} ctr={item.get('ctr', 0)}% "
        f"fix={item.get('fix_recommendation', '?')} "
        f"flags={','.join(k for k, v in (item.get('flags') or {}).items() if v) or 'none'}"
        for item in batch
    ]
    return f"""You are a triage prioritizer for an Australian trades blog content queue.
Score each item for EFFORT (1-5) and IMPACT (1-5).

EFFORT: 1 = meta/title rewrite (minutes). 3 = new 200-word section or internal links. 5 = deep content rewrite (hours).
IMPACT: 1 = <10 clicks. 3 = 10-50 clicks. 5 = 100+ clicks or direct conversion impact.
Adjust: gov_domain_competition -> impact -1. ai_overview_suppression -> impact -2.
tier 3 = striking distance pos 7-10, best click-per-edit potential.

Items (batch {n}):
{chr(10).join(lines)}

Output exactly one line per item, no commentary, no reasoning:
slug | effort=N | impact=N
"""


EXPECTED_CTR = [(3, 0.15), (5, 0.08), (10, 0.05), (15, 0.03), (20, 0.02), (30, 0.01)]


def impact_ceiling(item):
    """Deterministic cap on the model's impact score, from real click headroom.

    The model sees only tier/pos/imp and will happily score a 105-impression
    page as 'impact 5'. A page cannot deliver more clicks than its impressions
    allow: ceiling = reachable clicks at benchmark CTR for its position
    (1.5x allowance for a position gain) minus clicks already won.
    """
    pos = item.get("position", 100)
    impr = item.get("impressions", 0)
    clicks = item.get("clicks", 0)
    ctr = next((c for limit, c in EXPECTED_CTR if pos <= limit), 0.005)
    gain = max(0.0, impr * ctr * 1.5 - clicks)
    if gain >= 80:
        return 5
    if gain >= 40:
        return 4
    if gain >= 15:
        return 3
    if gain >= 5:
        return 2
    return 1


def apply_caps(items):
    for i in items:
        if i.get("status") != "IN QUEUE" or i.get("recently_updated"):
            continue
        pos, impr, clicks = i.get("position", 100), i.get("impressions", 0), i.get("clicks", 0)
        ctr = next((c for limit, c in EXPECTED_CTR if pos <= limit), 0.005)
        i["click_headroom"] = round(impr * ctr * 1.5 - clicks, 1)
        cap = impact_ceiling(i)
        if i.get("impact_score", 0) > cap:
            i["impact_capped_from"] = i["impact_score"]
            i["impact_score"] = cap
        if i.get("effort_score", 0) > 0:
            i["triage_score"] = round(i["impact_score"] / i["effort_score"], 2)


LINE = re.compile(r"^[\s\-\*\d\.\)]*([a-z0-9][a-z0-9\-]{8,}?)\s*\|\s*effort\s*=?\s*(\d)\s*\|\s*impact\s*=?\s*(\d)", re.I)


def parse(reply, batch):
    """Return {slug: (effort, impact)} matched against known batch slugs."""
    out = {}
    known = {i["slug"]: i for i in batch}
    for line in reply.splitlines():
        m = LINE.search(line)
        if not m:
            continue
        raw = m.group(1).strip("-").lower()
        slug = raw if raw in known else next((s for s in known if s.startswith(raw) or raw.startswith(s[:24])), None)
        if slug and slug not in out:
            e = max(1, min(5, int(m.group(2))))
            imp = max(1, min(5, int(m.group(3))))
            out[slug] = (e, imp)
    return out


def score_batch(batch, n):
    prompt = build_prompt(batch, n)
    reply = ask(
        [system_prompt("You are a strict, consistent triage scorer. Output only the score lines, no commentary."),
         user_prompt(prompt)],
        temperature=0.1,
        max_tokens=1200,
        timeout=300,
    )
    return parse(reply, batch)


def main(dry_run=False, cap_only=False):
    q = read_queue()
    items = q["items"]

    if cap_only:
        apply_caps(items)
        ranked = sorted(
            [i for i in items if i.get("status") == "IN QUEUE" and i.get("triage_score")],
            key=lambda i: (-i["triage_score"], -i.get("click_headroom", 0), -i["impressions"]),
        )
        q["ranked_actions"] = [
            {"rank": r, "slug": i["slug"], "score": i["triage_score"],
             "effort": i["effort_score"], "impact": i["impact_score"],
             "fix": i.get("fix_recommendation", "?"), "tier": i["tier"],
             "impressions": i["impressions"], "ctr": i["ctr"], "position": i["position"],
             "click_headroom": i.get("click_headroom"),
             "impact_capped_from": i.get("impact_capped_from")}
            for r, i in enumerate(ranked, 1)
        ]
        write_queue(q)
        print(f"✅ caps applied, {len(ranked)} ranked actions rewritten")
        for a in q["ranked_actions"][:10]:
            print(a["rank"], a["slug"], a["effort"], a["impact"], a["score"])
        return

    for item in items:
        item.pop("triage_scored", None)

    monitoring = [i for i in items if i.get("recently_updated")]
    for i in monitoring:
        i["effort_score"], i["impact_score"], i["triage_score"] = 0, 0, 0.0
        i["triage_scored"] = True
        i["triage_note"] = "meta changed inside current GSC window - monitoring, no action"

    active = [i for i in items if not i.get("recently_updated") and i.get("status") == "IN QUEUE"]
    print(f"Queue: {len(items)} items | {len(active)} actionable | {len(monitoring)} monitoring")

    for b in range(0, len(active), BATCH):
        batch = active[b:b + BATCH]
        got = score_batch(batch, b // BATCH + 1)
        missing = [i for i in batch if i["slug"] not in got]
        if missing:
            got.update(score_batch(missing, f"{b // BATCH + 1} retry"))
        for i in batch:
            if i["slug"] in got:
                e, imp = got[i["slug"]]
                i["effort_score"], i["impact_score"] = e, imp
                i["triage_score"] = round(imp / e, 2)
                i["triage_scored"] = True
            else:
                i["triage_scored"] = False
                i["effort_score"], i["impact_score"], i["triage_score"] = 0, 0, 0.0

    apply_caps(items)
    scored = [i for i in items if i.get("triage_scored") and (i.get("triage_score") or 0) > 0]
    scored.sort(key=lambda i: (-i["triage_score"], -i.get("click_headroom", 0), -i["impressions"]))

    print(f"\n{'RANK':>4} {'SLUG':<52} {'EFF':>3} {'IMP':>3} {'SCORE':>5}")
    print("-" * 74)
    for r, i in enumerate(scored, 1):
        print(f"{r:>4} {i['slug']:<52} {i['effort_score']:>3} {i['impact_score']:>3} {i['triage_score']:>5}")
    unscored = [i["slug"] for i in active if not i.get("triage_scored")]
    if unscored:
        print(f"\n⚠️ unscored (model output unparsed): {len(unscored)} -> {unscored}")

    if not dry_run:
        q["ranked_actions"] = [
            {"rank": r, "slug": i["slug"], "score": i["triage_score"],
             "effort": i["effort_score"], "impact": i["impact_score"],
             "fix": i.get("fix_recommendation", "?"),
             "tier": i["tier"], "impressions": i["impressions"], "ctr": i["ctr"],
             "position": i["position"]}
            for r, i in enumerate(scored, 1)
        ]
        q["monitoring"] = [
            {"slug": i["slug"], "impressions": i["impressions"], "clicks": i["clicks"],
             "ctr": i["ctr"], "position": i["position"],
             "note": i.get("triage_note", "recently updated")}
            for i in monitoring
        ]
        write_queue(q)
        print(f"\n✅ Scores written to {FIX_QUEUE}")
        print(f"   ranked_actions: {len(q['ranked_actions'])} | monitoring: {len(q['monitoring'])}")


if __name__ == "__main__":
    main("--dry-run" in sys.argv, "--cap-only" in sys.argv)
