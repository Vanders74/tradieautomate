#!/usr/bin/env python3
"""JEV Meta Tournament — generate variants, score with Jev, bracket finalists.
Test workflow for pre-flight title/meta A-B testing."""
import json
import os
import sys

sys.path.insert(0, os.path.expanduser("~/tradieautomate/repo/scripts"))
from jev_classify import jev_classify

# ── Test case: worst-scoring high-volume meta ──────────────────────────────
SLUG = "servicem8-vs-jobber-tradie-software-guide-2026"
CURRENT_TITLE = "ServiceM8 vs Jobber: Job Management Software for Australian Solar and Electrical Businesses"
CURRENT_META = "ServiceM8 vs Jobber 2026: which job management software wins for Australian solar and electrical businesses? Pricing, CCEW compliance, and mobile workflow compared side-by-side."

# ── Generate 20 variants: 10 titles × 10 metas, mixed patterns ────────────
TITLE_VARIANTS = [
    # Pattern A: Honest Review
    "ServiceM8 vs Jobber 2026: Honest Review for Aussie Solar & Electrical Tradies",
    # Pattern B: Year + Feature
    "ServiceM8 vs Jobber 2026 | Pricing, CCEW Compliance & Mobile Workflow Compared",
    # Pattern C: Action Guide
    "ServiceM8 vs Jobber: Which Job Management Software Should Aussie Tradies Choose in 2026?",
    # Pattern D: Question Hook
    "Is ServiceM8 or Jobber Better for Australian Solar & Electrical Businesses?",
    # Pattern E: Cost/Deadline
    "ServiceM8 vs Jobber 2026: Pricing, Features & Which Saves You the Most",
    # Pattern F: Comparison vs
    "ServiceM8 vs Jobber: The 2026 Showdown for Solar & Electrical Contractors",
    # Pattern G variants / custom
    "ServiceM8 vs Jobber 2026: The Verdict for Australian Solar & Electrical Trades",
    "ServiceM8 or Jobber in 2026? A No-Nonsense Guide for Aussie Solar & Electrical Tradies",
    "ServiceM8 vs Jobber: The Australian Trades Comparison You Can Actually Use",
    "Job Management for Solar & Electrical: ServiceM8 vs Jobber Compared in 2026",
]

META_VARIANTS = [
    # Data/differentiator-led
    "ServiceM8 vs Jobber 2026: $39/mo vs $29/mo for Aussie solar & electrical tradies. CCEW compliance, Xero sync & mobile workflow — which wins?",
    "ServiceM8 from $29/mo beats Jobber for compliance-heavy Aussie trades; Jobber wins on client experience. Full pricing & feature breakdown.",
    "ServiceM8 vs Jobber 2026 compared for Australian solar & electrical businesses: pricing, CCEW forms, Xero integration and mobile invoicing.",
    # Question-led
    "Which is right for your trade business — ServiceM8 or Jobber? We compare pricing, CCEW compliance and daily workflow in plain English.",
    "ServiceM8 vs Jobber in 2026: the honest comparison for Aussie solar & electrical tradies. Pricing, features, and what actually works.",
    # Verdict-led
    "ServiceM8 wins for compliance-heavy crews; Jobber wins for client experience. 2026 pricing and feature comparison for Aussie trades.",
    "Not sure between ServiceM8 and Jobber? Here's the 2026 comparison for Australian solar & electrical businesses, with real pricing.",
    # Australian-specific
    "The Australian solar & electrical comparison: ServiceM8 vs Jobber 2026. CCEW compliance, Xero sync, and mobile workflow — side by side.",
    # Emphatic/stakes
    "ServiceM8 vs Jobber 2026: save up to $10/mo per user without losing compliance features. Full comparison for Aussie trades.",
    # Short/punchy
    "ServiceM8 vs Jobber 2026: pricing, compliance, workflow — the verdict for Australian solar & electrical tradies.",
]

INTENT_Q = {
    "intent": {
        "type": "choice",
        "instructions": "What search intent does this page target?",
        "criteria": {
            "lookup": "Looking for specific data, rates, steps",
            "compliance": "Understanding a legal requirement",
            "comparison": "Choosing between products/services",
            "strategy": "Business growth advice",
        },
    }
}

SCORE_Q = {
    "title_score": {
        "type": "score",
        "instructions": "Rate the title 1-5: keyword-intent match (comparison query), specificity (numbers/entities), decides or implies an answer, 50-65 chars, uses the searcher's words",
        "criteria": ["Very poor", "Poor", "Average", "Good", "Excellent"],
    },
    "meta_score": {
        "type": "score",
        "instructions": "Rate the meta description 1-5: opens with the decision/differentiator, has a dollar figure or concrete fact, front-loaded hook, 120-160 chars, no fear-mongering",
        "criteria": ["Very poor", "Poor", "Average", "Good", "Excellent"],
    },
}


def run():
    print(f"SLUG: {SLUG}")
    print(f"CURRENT: {CURRENT_TITLE[:60]} | {CURRENT_META[:60]}")
    print(f"\nScoring {len(TITLE_VARIANTS) * len(META_VARIANTS)} title×meta combos via Jev…\n")

    scores = []
    for ti, title in enumerate(TITLE_VARIANTS):
        for mi, meta in enumerate(META_VARIANTS):
            state = f"Title: {title}\nMeta: {meta}"
            q = dict(SCORE_Q)
            res = jev_classify(state, q, timeout=20)
            if "_error" in res:
                print(f"  ERROR on T{ti} M{mi}: {res['_error'][:80]}")
                continue
            ts = res.get("title_score", {}).get("score") or 0
            ms = res.get("meta_score", {}).get("score") or 0
            total = ts + ms
            scores.append((total, ts, ms, title, meta))
            print(f"  T{ti} M{mi}: {total:.1f} (t={ts:.1f} m={ms:.1f}) | {title[:45]}")

    if not scores:
        print("No scores — Jev unavailable?")
        return

    scores.sort(key=lambda s: -s[0])
    print("\n=== TOP 3 by Jev score ===")
    for i, (total, ts, ms, title, meta) in enumerate(scores[:3]):
        print(f"\n#{i+1} ({total:.1f} = t{ts:.1f} m{ms:.1f})")
        print(f"  T: {title}")
        print(f"  M: {meta}")

    # ── Proper single-elimination bracket: top-3 finalists + current ───────
    print("\n=== SINGLE-ELIMINATION BRACKET (winner advances, 3 rounds) ===")
    fmt = lambda s: s[3][:50]
    current = (0, 0, 0, CURRENT_TITLE, CURRENT_META)

    def jev_duel(a, b):
        """Head-to-head click preference. Returns a-or-b and probabilities."""
        state = (
            f"Which title+meta would an Australian solar or electrical tradie most likely CLICK "
            f"in a search results page for 'servicem8 vs jobber'?\n\n"
            f"Option A:\nTitle: {a[3]}\nMeta: {a[4]}\n\n"
            f"Option B:\nTitle: {b[3]}\nMeta: {b[4]}"
        )
        res = jev_classify(state, {
            "pick": {
                "type": "choice",
                "instructions": "Which option would get more clicks from an Aussie tradie searching 'servicem8 vs jobber'?",
                "criteria": {"a": "Option A is stronger", "b": "Option B is stronger"},
            }
        }, timeout=20)
        pick = res.get("pick", {}).get("choice")
        probs = res.get("pick", {}).get("probabilities", {})
        pa = round(probs.get("a", 0.5), 3)
        pb = round(probs.get("b", 0.5), 3)
        print(f"  [{fmt(a)}] vs [{fmt(b)}] → {'A' if pick=='a' else 'B'} (A={pa}, B={pb})")
        return (a if pick == "a" else b), pa, pb

    # Semifinal 2: challenger (top-3) vs CURRENT (reigning)
    challenger = scores[2]  # top of last seed
    w2, _, _ = jev_duel(challenger, current)
    # Semifinal 1: top two seeds face each other
    w1, _, _ = jev_duel(scores[0], scores[1])
    print(f"\n  Semifinal winners:\n    #{1}: {fmt(w1)}\n    #{2}: {fmt(w2)}")

    # Final
    print("\n=== FINAL ===")
    champ, pa, pb = jev_duel(w1, w2)
    beats_current = champ is not current
    print(f"\nCHAMPION ({'NEW' if beats_current else 'CURRENT'}):")
    print(f"  T: {champ[3]}")
    print(f"  M: {champ[4]}")


if __name__ == "__main__":
    run()