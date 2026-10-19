#!/usr/bin/env python3
"""Workflow 3: Queue Triage Prioritizer — traffic-first scoring.

The old version scored effort/impact on integers 1-5 and ranked impact/effort.
That collapsed into buckets (2.0, then a wall of 1.0s) and ignored how much
traffic a page can actually gain. This version scores TRAFFIC:

    projected_clicks = click_headroom x (impact/10)
    triage_score     = projected_clicks / effort

where click_headroom is deterministic (benchmark CTR for the page's current
position, x1.5 position-gain allowance, minus clicks already won). The local
model only supplies judgement the maths can't: effort 1-10, capture confidence
1-10, and the traffic lever (meta / internal / content / authority).

`authority` is a hard zero: a page blocked by a gov E-E-A-T wall or AI-overview
suppression cannot be fixed by editing it, so it must never rank.

Recently-updated pages are never sent to the model (their meta changed inside
the GSC window). They are recorded as monitoring and excluded from ranking.

Usage:
    python3 triage.py                # score + rank + write
    python3 triage.py --dry-run      # print only
    python3 triage.py --cap-only     # re-rank using stored scores, no model
"""

import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_model import ask, system_prompt, user_prompt

FIX_QUEUE = "/Users/shane/tradieautomate/fix_queue.json"
BATCH = 8

# Benchmark organic CTR by position (conservative).
EXPECTED_CTR = [(3, 0.15), (5, 0.08), (10, 0.05), (15, 0.03), (20, 0.02), (30, 0.01)]

LEVERS = ("meta", "internal", "content", "authority")


def read_queue():
    with open(FIX_QUEUE) as f:
        return json.load(f)


def write_queue(q):
    with open(FIX_QUEUE, "w") as f:
        json.dump(q, f, indent=2)


def build_prompt(batch, n):
    lines = [
        f"{item['slug']} | pos={item['position']} imp={item['impressions']} "
        f"ctr={item.get('ctr', 0)}% clicks={item.get('clicks', 0)} "
        f"fix={item.get('fix_recommendation', '?')}"
        for item in batch
    ]
    return f"""You are a traffic triage scorer for an Australian trades blog.

For each page decide how to WIN CLICKS, then score effort and capture.

EFFORT (1-10):
 1-2  title/meta rewrite (minutes)
 3-4  add 2-5 internal links, or a small section
 5-6  add a 200-400 word section / FAQ block
 7-10 deep content rewrite or new comparison content (hours)

CAPTURE (1-10): how much of this page's click headroom can this fix realistically win?
 1-2  almost none (page already matches intent; problem is authority)
 3-4  small CTR lift
 5-7  most of the headroom (clear snippet/intent mismatch)
 8-10 nearly all of it (page ranks well, snippet is simply wrong or missing)

LEVER — exactly one:
 meta      = title/description is the blocker (position is fine, CTR is not)
 internal  = needs links from stronger pages to widen reach
 content   = missing depth/facts the searcher needs
 authority = blocked by gov/E-E-A-T/AI-overview; editing cannot fix it

Rules:
- If position > 20, CTR is rarely the problem: prefer internal or content.
- If the page has zero clicks but strong position and high impressions, meta is usually right.
- Use authority when the SERP is owned by .gov.au or an AI overview answers the query inline.

Items (batch {n}):
{chr(10).join(lines)}

Output exactly one line per item, no commentary:
slug | effort=N | capture=N | lever=WORD
"""


def impact_ceiling(item):
    """Cap capture on what the page's real click headroom can support (1-10)."""
    pos = item.get("position", 100)
    impr = item.get("impressions", 0)
    clicks = item.get("clicks", 0)
    ctr = next((c for limit, c in EXPECTED_CTR if pos <= limit), 0.005)
    gain = max(0.0, impr * ctr * 1.5 - clicks)
    for threshold, cap in ((150, 10), (100, 9), (70, 8), (45, 7), (30, 6),
                           (18, 5), (10, 4), (5, 3), (2, 2)):
        if gain >= threshold:
            return cap
    return 1


def apply_caps(items):
    for i in items:
        if i.get("status") != "IN QUEUE":
            continue
        if i.get("recently_updated"):
            # Meta changed inside the GSC window — no action, no ranking.
            i["triage_score"] = 0.0
            i["projected_clicks"] = 0.0
            continue
        pos, impr, clicks = i.get("position", 100), i.get("impressions", 0), i.get("clicks", 0)
        ctr = next((c for limit, c in EXPECTED_CTR if pos <= limit), 0.005)
        headroom = max(0.0, impr * ctr * 1.5 - clicks)
        i["click_headroom"] = round(headroom, 1)

        cap = impact_ceiling(i)
        if i.get("impact_score", 0) > cap:
            i["impact_capped_from"] = i["impact_score"]
            i["impact_score"] = cap

        lever = i.get("traffic_lever")
        effort = i.get("effort_score") or 0
        if lever == "authority":
            i["projected_clicks"] = 0.0
            i["triage_score"] = 0.0
            continue
        if effort > 0:
            projected = headroom * (i.get("impact_score", 0) / 10.0)
            i["projected_clicks"] = round(projected, 1)
            i["triage_score"] = round(projected / effort, 2)
        else:
            i["projected_clicks"] = 0.0
            i["triage_score"] = 0.0


LINE = re.compile(
    r"^\s*[-*\d.)\s]*([a-z0-9][a-z0-9\-]{8,}?)\s*\|\s*effort\s*=?\s*(\d{1,2})"
    r"\s*\|\s*capture\s*=?\s*(\d{1,2})(?:\s*\|\s*lever\s*=?\s*([a-z]+))?",
    re.I,
)


def parse(reply, batch):
    """Return {slug: (effort, capture, lever)} matched against known slugs."""
    out = {}
    known = {i["slug"]: i for i in batch}
    for line in reply.splitlines():
        m = LINE.search(line)
        if not m:
            continue
        raw = m.group(1).strip("-").lower()
        slug = raw if raw in known else next(
            (s for s in known if s.startswith(raw) or raw.startswith(s[:24])), None)
        if not slug or slug in out:
            continue
        effort = max(1, min(10, int(m.group(2))))
        capture = max(1, min(10, int(m.group(3))))
        lever = (m.group(4) or "").lower()
        if lever not in LEVERS:
            lever = "content"
        out[slug] = (effort, capture, lever)
    return out


def score_batch(batch, n):
    prompt = build_prompt(batch, n)
    reply = ask(
        [system_prompt("You are a strict traffic triage scorer. Output only the score lines."),
         user_prompt(prompt)],
        temperature=0.1,
        max_tokens=1600,
        timeout=300,
    )
    return parse(reply, batch)


def ranked_entry(rank, i):
    return {
        "rank": rank,
        "slug": i["slug"],
        "score": i.get("triage_score", 0),
        "projected_clicks": i.get("projected_clicks", 0),
        "click_headroom": i.get("click_headroom"),
        "effort": i.get("effort_score", 0),
        "impact": i.get("impact_score", 0),
        "lever": i.get("traffic_lever", "?"),
        "fix": i.get("fix_recommendation", "?"),
        "tier": i["tier"],
        "impressions": i["impressions"],
        "ctr": i["ctr"],
        "position": i["position"],
        "impact_capped_from": i.get("impact_capped_from"),
    }


def main(dry_run=False, cap_only=False):
    q = read_queue()
    items = q["items"]

    if cap_only:
        apply_caps(items)
        ranked = sorted(
            [i for i in items if i.get("status") == "IN QUEUE"
             and not i.get("recently_updated")
             and (i.get("triage_score") or 0) > 0],
            key=lambda i: (-i["triage_score"], -i.get("click_headroom", 0)),
        )
        q["ranked_actions"] = [ranked_entry(r, i) for r, i in enumerate(ranked, 1)]
        q["triage_summary"] = {
            "ranked": len(ranked),
            "authority_blocked": sum(1 for i in items if i.get("traffic_lever") == "authority"),
            "by_lever": {lv: sum(1 for i in ranked if i.get("traffic_lever") == lv)
                         for lv in LEVERS},
            "total_projected_clicks": round(
                sum(i.get("projected_clicks", 0) for i in ranked), 1),
        }
        q["triage_at"] = datetime.now().isoformat(timespec="seconds")
        write_queue(q)
        print(f"✅ re-ranked {len(ranked)} actions from stored scores")
        for a in q["ranked_actions"][:10]:
            print(f"  {a['rank']:2d}. {a['slug'][:42]:42s} {a['projected_clicks']:>6}clicks "
                  f"eff{a['effort']} {a['lever']}")
        return

    for item in items:
        item.pop("triage_scored", None)

    monitoring = [i for i in items if i.get("recently_updated")]
    for i in monitoring:
        i["effort_score"], i["impact_score"], i["triage_score"] = 0, 0, 0.0
        i["projected_clicks"], i["traffic_lever"] = 0.0, "monitoring"
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
                e, cap, lever = got[i["slug"]]
                i["effort_score"], i["impact_score"] = e, cap
                i["traffic_lever"] = lever
                i["triage_scored"] = True
            else:
                i["triage_scored"] = False
                i["effort_score"], i["impact_score"] = 0, 0
                i["traffic_lever"] = "content"

    apply_caps(items)

    scored = [i for i in items
              if i.get("triage_scored") and (i.get("triage_score") or 0) > 0]
    scored.sort(key=lambda i: (-i["triage_score"], -i.get("click_headroom", 0)))

    print(f"\n{'RANK':>4} {'SLUG':<46} {'PROJ':>6} {'EFF':>4} {'CAP':>4} {'LEVER':<9} {'SCORE':>6}")
    print("-" * 84)
    for r, i in enumerate(scored, 1):
        print(f"{r:>4} {i['slug'][:46]:<46} {i.get('projected_clicks',0):>6} "
              f"{i['effort_score']:>4} {i['impact_score']:>4} "
              f"{i.get('traffic_lever','?'):<9} {i['triage_score']:>6}")

    blocked = [i["slug"] for i in active if i.get("traffic_lever") == "authority"]
    if blocked:
        print(f"\n🚫 authority-blocked (excluded from ranking): {len(blocked)}")
    unscored = [i["slug"] for i in active if not i.get("triage_scored")]
    if unscored:
        print(f"⚠️ unscored (unparsed model output): {len(unscored)} -> {unscored}")

    if not dry_run:
        q["ranked_actions"] = [ranked_entry(r, i) for r, i in enumerate(scored, 1)]
        q["monitoring"] = [
            {"slug": i["slug"], "impressions": i["impressions"], "clicks": i["clicks"],
             "ctr": i["ctr"], "position": i["position"],
             "note": i.get("triage_note", "recently updated")}
            for i in monitoring
        ]
        q["triage_at"] = datetime.now().isoformat(timespec="seconds")
        q["triage_summary"] = {
            "ranked": len(scored),
            "authority_blocked": len(blocked),
            "by_lever": {lv: sum(1 for i in scored if i.get("traffic_lever") == lv)
                         for lv in LEVERS},
            "total_projected_clicks": round(sum(i.get("projected_clicks", 0) for i in scored), 1),
        }
        write_queue(q)
        print(f"\n✅ written: {len(q['ranked_actions'])} ranked | "
              f"projected +{q['triage_summary']['total_projected_clicks']} clicks/month")


if __name__ == "__main__":
    main("--dry-run" in sys.argv, "--cap-only" in sys.argv)
