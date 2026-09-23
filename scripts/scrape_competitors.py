#!/usr/bin/env python3
"""Build competitor title/meta database from SERP for our top queries.
Stores to repo/scripts/competitor_metas.json for the cron to reference."""
import json, os, sys, time
from urllib.parse import quote_plus
from urllib.request import urlopen, Request

QUERIES = [
    "ccew",
    "automate tradie business",
    "job management software for electricians",
    "business automation for tradies",
    "servicem8 update 2026",
    "servicem8 new features",
    "electrical job management software",
    "servicem8",
    "job management software for electrical contractor",
    "tradify vs servicem8",
    "software for electricians",
    "electrician software",
    "licensed electrical contractor qld",
    "certificate of electrical safety victoria",
    "electrical compliance certificate nsw",
    "ces victoria certificate of electrical safety",
    "certificate of electrical safety vic",
    "rcd safety switch requirements",
    "nsw electrical contractor licence",
    "qld electrical contractor licence",
]

DB = {}

for qtext in QUERIES:
    print(f"Query: {qtext}")
    try:
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(qtext)}"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8", errors="replace")
        
        # Parse result blocks - DDG uses class="result" with <h2><a> for titles
        import re
        results = []
        # Find result blocks
        blocks = re.findall(r'<div class="result[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>', html, re.DOTALL)
        for block in blocks[:10]:
            # Title
            tm = re.search(r'<a[^>]*class="result__a"[^>]*>(.*?)</a>', block, re.DOTALL)
            title = re.sub(r'<[^>]+>', '', tm.group(1)).strip() if tm else ""
            # URL
            um = re.search(r'href="([^"]+)"[^>]*class="result__a"', block, re.DOTALL)
            url = um.group(1) if um else ""
            # Snippet
            sm = re.search(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', block, re.DOTALL)
            snippet = re.sub(r'<[^>]+>', '', sm.group(1)).strip() if sm else ""
            if title:
                results.append({"title": title, "url": url[:120], "snippet": snippet[:200]})
        
        DB[qtext] = results
        print(f"  Found {len(results)} results")
    except Exception as e:
        print(f"  Error: {e}")
        DB[qtext] = []
    time.sleep(0.5)

# Save
path = os.path.expanduser("~/tradieautomate/repo/scripts/competitor_metas.json")
with open(path, "w") as f:
    json.dump(DB, f, indent=1)
print(f"\nSaved {len(DB)} queries to {path}")

# Summary
for q, res in DB.items():
    if res:
        print(f"\n{q}:")
        for r in res[:3]:
            print(f"  T: {r['title'][:70]}")
            print(f"  D: {r['snippet'][:100]}")
            print(f"  U: {r['url'][:60]}")