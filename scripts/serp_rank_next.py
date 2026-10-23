#!/usr/bin/env python3
"""SERP rank monitor queue helper.

The keyword list is a fixed rotation (keyword_queue.txt, one "N|keyword" per
line). State lives in serp_state.json:

    {"next_index": 2, "cycle": 1, "updated": "2026-10-23"}

`next_index` is 1-based into the file. When it runs past the last keyword the
rotation wraps to 1 and `cycle` increments, so the list never runs dry.

Usage:
    python3 scripts/serp_rank_next.py            # print next keyword, advance state
    python3 scripts/serp_rank_next.py --peek     # print next keyword, do NOT advance
    python3 scripts/serp_rank_next.py --reset    # reset to keyword 1 / cycle 1
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "keyword_queue.txt"
STATE = ROOT / "serp_state.json"


def load_queue():
    items = []
    for raw in QUEUE.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        if "|" in raw:
            raw = raw.split("|", 1)[1]
        items.append(raw.strip())
    if not items:
        sys.exit("keyword_queue.txt is empty")
    return items


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"next_index": 1, "cycle": 1}


def save_state(state):
    state["updated"] = date.today().isoformat()
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--peek", action="store_true")
    ap.add_argument("--reset", action="store_true")
    args = ap.parse_args()

    items = load_queue()
    state = {"next_index": 1, "cycle": 1} if args.reset else load_state()

    idx = int(state.get("next_index", 1))
    cycle = int(state.get("cycle", 1))
    if idx < 1 or idx > len(items):
        idx, cycle = 1, cycle + 1  # wrap the rotation

    keyword = items[idx - 1]
    print(f"{idx}|{cycle}|{keyword}")

    if not args.peek:
        nxt = idx + 1
        if nxt > len(items):
            nxt, cycle = 1, cycle + 1
        state.update({"next_index": nxt, "cycle": cycle, "last_keyword": keyword})
        save_state(state)


if __name__ == "__main__":
    main()
