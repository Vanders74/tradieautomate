#!/usr/bin/env python3
"""Workflow 2: Competitor Gap Filler

Replaces the old gap radar cron. Reads a keyword + competitor URL,
extracts competitor coverage, maps against TA's article, and writes
the missing section grounded in the competitor's angle.

Usage:
    python3 gap_filler.py <keyword> <competitor_url> <ta_slug>
    python3 gap_filler.py --from-queue  # Process one queued keyword
"""

import sys
import os
import json
import urllib.request
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_model import ask, system_prompt, user_prompt

GAP_DIR = "/Users/shane/tradieautomate/seo/competitor-gaps"
GAP_QUEUE = "/Users/shane/tradieautomate/seo/gap-queue-state.json"
REPO = "/Users/shane/tradieautomate/repo"


def fetch_page(url):
    """Fetch a URL and return clean text (headings + body preview)."""
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        )
        resp = urllib.request.urlopen(req, timeout=20)
        html = resp.read().decode("utf-8", errors="replace")

        # Simple extraction: get heading text and first 3000 chars of body
        import re
        headings = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', html, re.IGNORECASE | re.DOTALL)
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.IGNORECASE | re.DOTALL)
        body = body_match.group(1)[:5000] if body_match else html[:5000]
        body_clean = re.sub(r'<[^>]+>', ' ', body)
        body_clean = re.sub(r'\s+', ' ', body_clean).strip()

        return {
            "headings": [re.sub(r'<[^>]+>', '', h).strip() for h in headings if h.strip()],
            "body_preview": body_clean[:3000],
        }
    except Exception as e:
        return {"error": str(e)}


def read_ta_article(slug):
    """Read TA article and extract structure."""
    path = f"{REPO}/src/content/blog/{slug}.md"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        content = f.read()

    headings = []
    for line in content.split("\n"):
        if line.startswith("## ") or line.startswith("## "):
            headings.append(line.strip("# "))
    return {"headings": headings, "content_preview": content[:3000]}


def write_gap_report(keyword, competitor_url, ta_slug, report):
    """Write the gap report to the correct directory."""
    os.makedirs(GAP_DIR, exist_ok=True)
    safe = ta_slug.replace("/", "-")
    path = f"{GAP_DIR}/{safe}.md"
    with open(path, "w") as f:
        f.write(f"""---
title: "Competitor Gap Report — {keyword}"
keyword: "{keyword}"
slug: "{ta_slug}"
competitor: "{competitor_url}"
reportDate: "{__import__('datetime').datetime.now().strftime('%Y-%m-%d')}"
---

{report}
""")
    return path


def process_keyword(keyword, competitor_url, ta_slug, comp_text_path=None):
    """Full 3-agent pipeline for one keyword.

    comp_text_path: optional path to a pre-fetched competitor text file
    (used when direct fetch is blocked, e.g. HTTP 403). Headings are
    extracted from markdown-style '#'/'-' lines; whole text becomes the preview.
    """
    print(f"\n{'='*60}")
    print(f"GAP: {ta_slug} ← {keyword} ({competitor_url})")

    # Fetch competitor page
    if comp_text_path and os.path.exists(comp_text_path):
        import re
        with open(comp_text_path) as f:
            raw = f.read()
        headings = re.findall(r'^#{1,4}\s+(.*)$', raw, re.MULTILINE)
        comp = {
            "headings": [h.strip() for h in headings if h.strip()],
            "body_preview": re.sub(r'\s+', ' ', raw).strip()[:3000],
        }
        print(f"  Using pre-fetched competitor text: {comp_text_path} ({len(comp['headings'])} headings)")
    else:
        comp = fetch_page(competitor_url)
        if comp.get("error"):
            print(f"  ERROR fetching competitor: {comp['error']}")
            return

    # Read TA article
    ta = read_ta_article(ta_slug)
    if ta is None:
        print(f"  ERROR: TA article not found: {ta_slug}")
        return

    print(f"  Competitor headings: {len(comp['headings'])}")
    print(f"  TA sections: {len(ta['headings'])}")

    # Agent 1: Extract competitor's coverage structure
    agent1 = f"""You are Agent 1 (Content Auditor). Analyse this competitor page's coverage for '{keyword}'.

Competitor headings:
{json.dumps(comp['headings'][:20], indent=2)}

Competitor body preview:
{comp['body_preview'][:2000]}

TA article '{ta_slug}' existing sections:
{json.dumps(ta['headings'][:20], indent=2)}

Identify 2-3 specific structural gaps: things the competitor covers that TA doesn't, or covers differently. For each gap, state the competitor's angle in one sentence."""
    a1 = ask([system_prompt("You are a content auditor comparing competitor vs TA coverage. Be specific about what the competitor covers differently."), user_prompt(agent1)], temperature=0.3)
    print(f"  Agent 1: Gaps identified")

    # Agent 2: Map gaps
    agent2 = f"""You are Agent 2 (Content Strategist). Based on these gaps, decide which ONE gap is most valuable to fill.

Gaps identified:
{a1}

TA article: {ta_slug}
TA existing content:
{ta['content_preview'][:2000]}

Output your decision as:
MOST VALUABLE GAP: [one sentence describing the gap]
RATIONALE: [why this gap drives search traffic or conversions for TA readers]
ANGLE: [how to cover it better than the competitor — TA's unique angle]"""
    a2 = ask([system_prompt("You are a content strategist. Pick gaps by business value, not novelty."), user_prompt(agent2)], temperature=0.3)
    print(f"  Agent 2: Gap selected")

    # Agent 3: Write the missing section
    agent3 = f"""You are Agent 3 (Copywriter). Write a ~200-word section filling the identified content gap for TA's article '{ta_slug}'.

Gaps identified: {a1}
Gap selected: {a2}

TA existing content context:
{ta['content_preview'][:2000]}

Write a section ready to insert into the TA article:
- Heading: H2 level, keyword-inclusive
- Body: ~200 words, grounded facts, actionable
- Tone: practical trade audience (electrician/solar installer)
- Unique angle: what the competitor misses
- No markdown fences, no fluff"""
    a3 = ask([system_prompt("You write practical, grounded content for Australian trade businesses. No fluff, no sales pitch — just useful information that a tradie would read and act on."), user_prompt(agent3)], temperature=0.4, max_tokens=1200)
    print(f"  Agent 3: Section written")

    # Assemble report
    report = f"""## Gap Analysis

Keyword: {keyword}
Competitor: {competitor_url}
TA Article: {ta_slug}

### Agent 1 — Coverage Audit
{a1}

### Agent 2 — Gap Selection
{a2}

### Agent 3 — Missing Section
{a3}

---

## Suggested Insertion
Find the most natural insertion point in `src/content/blog/{ta_slug}.md` and add:

{a3}
"""
    path = write_gap_report(keyword, competitor_url, ta_slug, report)
    print(f"  ✅ Report written: {path}")


def queue_next():
    """Print the next slug/query to process as JSON for the cron agent.

    The cron has web tools and does the Google search to find the top
    competitor URL; this script cannot search the web. So:
      1. Cron runs: python3 gap_filler.py --queue-next
      2. Script prints {"slug": ..., "query": ...} for the next queue item
      3. Cron searches Google for the query, picks the top competitor URL
      4. Cron runs: python3 gap_filler.py <query> <competitor_url> <slug>
      5. Cron increments gap-queue-state.json index
    """
    if not os.path.exists(GAP_QUEUE):
        print(json.dumps({"error": "no gap queue state"}))
        return

    with open(GAP_QUEUE) as f:
        queue = json.load(f)

    idx = queue.get("index", 0)
    print(json.dumps({"index": idx, "last_processed": queue.get("last_processed", "")}))


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        comp_text = sys.argv[4] if len(sys.argv) > 4 else None
        process_keyword(sys.argv[1], sys.argv[2], sys.argv[3], comp_text)
    elif len(sys.argv) == 2 and sys.argv[1] == "--queue-next":
        queue_next()
    else:
        print("Usage:")
        print("  python3 gap_filler.py <keyword> <competitor_url> <ta_slug> [competitor_text_file]")
        print("  python3 gap_filler.py --queue-next")