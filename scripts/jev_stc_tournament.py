#!/usr/bin/env python3
"""JEV Meta Tournament for stc-claim-process-solar-installers-australia."""
import json, sys, os
sys.path.insert(0, os.path.expanduser("~/tradieautomate/repo/scripts"))
from jev_classify import jev_classify

SLUG = "stc-claim-process-solar-installers-australia"
CURRENT_TITLE = "STC Claim Process: Step-by-Step Guide for Australian Solar Installers (2026)"
CURRENT_META = "How to lodge STC claims as an Australian solar installer — eligibility, calculation, customer declarations, lodgement process, common errors that trigger audits, and how to manage it at scale."

# ── 10 title variants × 10 meta variants ──────────────────────────────────
TITLE_VARIANTS = [
    # Pattern C: Action Guide
    "STC Claim Process 2026: Step-by-Step Guide — 12-Month Deadline, $40/Certificate Value & Audit Traps",
    # Pattern D: Question Hook
    "How to Lodge STC Claims in 2026? Complete Guide for Australian Solar Installers",
    # Pattern E: Year + Cost/Rules
    "STC Claim Process 2026: 12-Month Deadline, Eligibility Rules & Lodgement Steps",
    # Pattern B: Year + Feature
    "STC Claim Process 2026 | Eligibility, Calculation, Lodgement & Avoiding CER Audits",
    # Pattern C variant
    "STC Claims for Solar Installers: The Complete 2026 Process — Eligibility, Lodgement & Record-Keeping",
    # Pattern D variant
    "What's the STC Claim Process in 2026? Deadlines, Dollar Value & Avoiding CER Audits",
    # Pattern C variant  
    "Solar STC Claims 2026: How to Lodge, Calculate & Avoid CER Audit Triggers",
    # Action-oriented
    "STC Claim Process Australia 2026: From Installation to Payment — Every Step Covered",
    # Pattern E variant
    "STC Claim Process for Solar Installers: 12-Month Deadline, CER Compliance & Step-by-Step Guide",
    # Pattern C variant
    "STC Claim Process 2026: Deadlines, Zone Calculator & Steps to Avoid CER Audits",
]

META_VARIANTS = [
    # 1 — data-led, front-loaded
    "Lodge STC claims within 12 months of installation — $40+/certificate, zone-rated calculator, customer declaration required. Complete step-by-step for Aussie solar installers.",
    # 2 — step count
    "STC claim process in 6 steps: confirm eligibility, calculate certificates (zone × kW), get the customer declaration signed, lodge via REC Registry within 12 months. $40+/STC.",
    # 3 — deadline-led, stakes
    "Missing the 12-month STC deadline costs you $40+/certificate. Exact process: eligibility checks, zone calculator, audit-proof record-keeping for solar installers.",
    # 4 — newbie-friendly
    "New to STC claims? Here's the 2026 process: CEC accreditation checks, zone-rated certificate calculation, customer declarations, and REC Registry lodgement — in plain English.",
    # 5 — deadline + CER risk
    "STC claims 2026: $40+/certificate at risk if you miss the 12-month deadline or trigger a CER audit. Full lodgement process for Australian solar installers.",
    # 6 — how-to led
    "How to lodge STC claims in 2026: eligibility rules, kW-to-certificate calculation, signed customer declarations, and REC Registry lodgement within 12 months.",
    # 7 — value-led
    "Save $40+/STC with a clean lodgement process: eligibility checks, zone calculator, 12-month deadline — what every Australian solar installer needs to know.",
    # 8 — comprehensive
    "STC claim process from start to finish: confirm CEC accreditation, calculate zone-rated certificates, lodge within 12 months, keep audit-ready records.",
    # 9 — audit-risk led
    "The STC claim process explained: 12-month deadline, $40/STC market rate, customer declaration rules, and the CER audit triggers every solar installer should know.",
    # 10 — practitioner-led
    "Lodge STCs like a pro: 12-month window, zone-based certificate calculation, customer declaration before lodgement, and audit-proof record-keeping for Aussie solar businesses.",
]

SCORE_Q = {
    "title_score": {
        "type": "score",
        "instructions": "Rate the title 1-5: keyword-intent match (how-to/lookup query for STC claim process), specificity (numbers/deadlines/entities), decides or implies an answer, 50-65 chars, uses the searcher's words",
        "criteria": ["Very poor", "Poor", "Average", "Good", "Excellent"],
    },
    "meta_score": {
        "type": "score",
        "instructions": "Rate the meta description 1-5: opens with the decision/deadline/dollar figure, has a dollar amount or concrete deadline, front-loaded hook, 120-160 chars, no fear-mongering",
        "criteria": ["Very poor", "Poor", "Average", "Good", "Excellent"],
    },
}

DUEL_Q = {
    "pick": {
        "type": "choice",
        "instructions": "Which option would get more clicks from an Australian solar installer searching 'stc claim process'?",
        "criteria": {"a": "Option A is stronger", "b": "Option B is stronger"},
    }
}

def run():
    print(f"SLUG: {SLUG}")
    print(f"CURRENT: {CURRENT_TITLE[:60]} | {CURRENT_META[:60]}\n")
    print(f"Scoring {len(TITLE_VARIANTS) * len(META_VARIANTS)} title×meta combos via Jev…\n")

    scores = []
    for ti, title in enumerate(TITLE_VARIANTS):
        for mi, meta in enumerate(META_VARIANTS):
            state = f"Title: {title}\nMeta: {meta}"
            res = jev_classify(state, dict(SCORE_Q), timeout=25)
            if "_error" in res:
                print(f"  ERROR on T{ti} M{mi}: {res['_error'][:80]}")
                continue
            ts = res.get("title_score", {}).get("score") or 0
            ms = res.get("meta_score", {}).get("score") or 0
            total = ts + ms
            scores.append((total, ts, ms, title, meta))
            print(f"  T{ti} M{mi}: {total:.1f} (t={ts:.1f} m={ms:.1f}) | {title[:50]}")

    if not scores:
        print("No scores — Jev unavailable?")
        return None

    scores.sort(key=lambda s: -s[0])
    print("\n=== TOP 3 by Jev score ===")
    for i, (total, ts, ms, title, meta) in enumerate(scores[:3]):
        print(f"\n#{i+1} ({total:.1f} = t{ts:.1f} m{ms:.1f})")
        print(f"  T: {title}")
        print(f"  M: {meta}")

    # ── Single-elimination bracket ────────────────────────────────────────
    print("\n=== SINGLE-ELIMINATION BRACKET ===")
    fmt = lambda s: s[3][:55]
    current = (0, 0, 0, CURRENT_TITLE, CURRENT_META)

    def jev_duel(a, b, round_name=""):
        state = (
            f"Which title+meta would an Australian solar installer most likely CLICK "
            f"in a search results page for 'stc claim process'?\n\n"
            f"Option A:\nTitle: {a[3]}\nMeta: {a[4]}\n\n"
            f"Option B:\nTitle: {b[3]}\nMeta: {b[4]}"
        )
        res = jev_classify(state, dict(DUEL_Q), timeout=20)
        pick = res.get("pick", {}).get("choice")
        probs = res.get("pick", {}).get("probabilities", {})
        pa = round(probs.get("a", 0.5), 3)
        pb = round(probs.get("b", 0.5), 3)
        print(f"  {round_name}: [{fmt(a)[:45]}] vs [{fmt(b)[:45]}] → {'A' if pick=='a' else 'B'} (A={pa}, B={pb})")
        return (a if pick == "a" else b), pa, pb

    # Semifinal 1: top seeds 1 vs 2
    w1, p1a, p1b = jev_duel(scores[0], scores[1], "SF1")
    # Semifinal 2: seed 3 vs current
    w2, p2a, p2b = jev_duel(scores[2], current, "SF2")
    
    print(f"\n  Semifinal winners:\n    SF1: {fmt(w1)[:50]}\n    SF2: {fmt(w2)[:50]}")

    # Final
    print("\n=== FINAL ===")
    champ, pa, pb = jev_duel(w1, w2, "FINAL")
    beats_current = champ is not current
    print(f"\nCHAMPION ({'NEW' if beats_current else 'CURRENT'}):")
    print(f"  T: {champ[3]}")
    print(f"  M: {champ[4]}")
    print(f"  Probabilities: A={pa}, B={pb}")

    # ── Run final head-to-head 3 times ─────────────────────────────────────
    if beats_current:
        print("\n=== BEST-OF-3 CONFIRMATION ===")
        champ_wins = 0
        current_wins = 0
        for rnd in range(3):
            state = (
                f"Which title+meta would an Australian solar installer most likely CLICK "
                f"in a search results page for 'stc claim process'?\n\n"
                f"Option A:\nTitle: {champ[3]}\nMeta: {champ[4]}\n\n"
                f"Option B:\nTitle: {current[3]}\nMeta: {current[4]}"
            )
            res = jev_classify(state, dict(DUEL_Q), timeout=20)
            pick = res.get("pick", {}).get("choice")
            probs = res.get("pick", {}).get("probabilities", {})
            pa = round(probs.get("a", 0.5), 3)
            pb = round(probs.get("b", 0.5), 3)
            if pick == "a":
                champ_wins += 1
            else:
                current_wins += 1
            print(f"  Round {rnd+1}: {'CHAMPION' if pick=='a' else 'CURRENT'} wins (A={pa}, B={pb})")
        
        if champ_wins >= 2:
            print(f"\n✅ Champion wins {champ_wins}/3 — adopting NEW meta")
        else:
            print(f"\n❌ Champion only wins {champ_wins}/3 — current meta holds")
            beats_current = False

    result = {
        "slug": SLUG,
        "champion": {
            "title": champ[3],
            "meta": champ[4],
            "beats_current": beats_current
        },
        "top3": [{"title": s[3], "meta": s[4], "score": s[0]} for s in scores[:3]],
    }
    with open("/tmp/jev_stc_result.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResult saved to /tmp/jev_stc_result.json")
    return result

if __name__ == "__main__":
    run()