#!/usr/bin/env python3
"""Workflow 3: Queue Triage Prioritizer

Scores each fix_queue item by estimated effort and business impact,
then ranks by impact-per-effort. Writes back to fix_queue.

Usage:
    python3 triage.py                    # Process all queue items
    python3 triage.py --dry-run          # Print rankings without writing
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_model import ask, system_prompt, user_prompt

FIX_QUEUE = "/Users/shane/tradieautomate/fix_queue.json"


def read_queue():
    with open(FIX_QUEUE) as f:
        return json.load(f)


def write_queue(q):
    with open(FIX_QUEUE, "w") as f:
        json.dump(q, f, indent=2)


def score_items(items, dry_run=False):
    """Score all IN QUEUE items by effort and impact using the local model.

    Bonsai is a reasoning model at ~14 tok/s, so a single call for 30+ items
    would exceed timeouts. Score in batches of 8, then merge results.
    """
    import re

    scored = []
    batch_size = 8
    active = [i for i in items if i.get("status") == "IN QUEUE"]

    for start in range(0, len(active), batch_size):
        batch_items = active[start : start + batch_size]

        # Compact description with the global index for post-merge mapping
        descriptions = [
            f"[{items.index(item)}] slug={item['slug']} tier={item['tier']} pos={item['position']} "
            f"imp={item['impressions']} ctr={item.get('ctr', 0)}% fix={item.get('fix_recommendation', '?')} "
            f"recently_updated={item.get('recently_updated')}"
            for item in batch_items
        ]

        prompt = f"""You are a triage prioritizer for a trade blog content queue. Score each item below by EFFORT (1-5) and IMPACT (1-5), then compute an impact-per-effort score.

Scoring rules:
- EFFORT 1 = tiny fix (meta rewrite, 1-line change)
- EFFORT 3 = medium (new 200-word section, new link)
- EFFORT 5 = deep content (2000+ word article, research)
- IMPACT 1 = negligible traffic gain (< 10 clicks)
- IMPACT 3 = moderate (10-50 extra clicks)
- IMPACT 5 = high (100+ extra clicks or direct conversion impact)

recently_updated: True means any meta/content change would be wasted - score effort=0 (skip).
gov_domain_competition: True means even a good meta may not move position - score impact 1 lower.
ai_overview_suppression: True means users get answers without clicking - score impact 2 lower.
tier 3 items are striking distance (pos 7-10) - higher impact potential per meta change.

Queue items (batch {start//batch_size + 1}):
{chr(10).join(descriptions)}

Output for each item as:
[idx] effort=X impact=X score=X.X
No other text. Keep responses short and consistent."""

        result = ask(
            [system_prompt("You are a strict, consistent triage scorer. Output only the scores, no commentary."),
             user_prompt(prompt)],
            temperature=0.1,
            max_tokens=1600,
            timeout=240,
        )

        for line in result.strip().split("\n"):
            m = re.match(r'\[(\d+)\]\s+effort=(\d+)\s+impact=(\d+)\s+score=([\d.]+)', line)
            if m:
                idx = int(m.group(1))
                if idx < len(items):
                    items[idx]["effort_score"] = int(m.group(2))
                    items[idx]["impact_score"] = int(m.group(3))
                    items[idx]["triage_score"] = float(m.group(4))

    # Sort by triage_score descending
    scored = [i for i in items if "triage_score" in i]
    scored.sort(key=lambda i: i["triage_score"], reverse=True)

    return scored


def main(dry_run=False):
    q = read_queue()
    items = q["items"]
    
    print(f"Queue: {len(items)} items, {sum(1 for i in items if i.get('status')=='IN QUEUE')} IN QUEUE")
    
    scored = score_items(items, dry_run)
    
    print(f"\n{'RANK':>5} {'SLUG':<50} {'EFFORT':>7} {'IMPACT':>7} {'SCORE':>6}")
    print("-" * 80)
    for rank, item in enumerate(scored, 1):
        print(f"{rank:>5} {item['slug']:<50} {item.get('effort_score','?'):>7} {item.get('impact_score','?'):>7} {item.get('triage_score','?'):>6}")
        if rank >= 20:
            break

    if not dry_run:
        # Persist scores back to queue
        for item in q["items"]:
            for scored_item in scored:
                if item["slug"] == scored_item["slug"] and "triage_score" in scored_item:
                    item["effort_score"] = scored_item["effort_score"]
                    item["impact_score"] = scored_item["impact_score"]
                    item["triage_score"] = scored_item["triage_score"]
                    break
        
        # Add a ranked action list
        q["ranked_actions"] = [
            {"rank": r, "slug": i["slug"], "score": i.get("triage_score", 0),
             "effort": i.get("effort_score", 5), "impact": i.get("impact_score", 1),
             "fix": i.get("fix_recommendation", "?")}
            for r, i in enumerate(scored, 1)
        ]
        
        write_queue(q)
        print(f"\n✅ Scores written to {FIX_QUEUE}")
        print(f"   Ranked actions: {len(scored)} items scored")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    main(dry_run)