#!/usr/bin/env python3
"""Workflow 5: Index-Coverage Sanity Check

Compares the current built page count against the previous build.
Alerts if pages dropped out of the build. Runs after every npm run build.

Usage:
    python3 index_check.py              # Compare + alert
    python3 index_check.py --record      # Save current count without alerting
"""

import sys
import os
import json

SITEMAP = "/Users/shane/tradieautomate/repo/dist/sitemap-index.xml"
STATE_FILE = "/Users/shane/tradieautomate/repo/.hermes/bonsai/build_state.json"


def count_pages():
    """Count pages in the built sitemap files.

    sitemap-index.xml only references sub-sitemaps; the actual page URLs
    live in sitemap-*.xml. Read every sub-sitemap and total their <loc> count.
    """
    import re
    dist_dir = os.path.dirname(SITEMAP)
    if not os.path.isdir(dist_dir):
        return 0, None

    locs = []
    for fn in sorted(os.listdir(dist_dir)):
        if not (fn.startswith("sitemap-") and fn.endswith(".xml")):
            continue  # skip sitemap-index.xml and rss.xml
        with open(os.path.join(dist_dir, fn)) as f:
            content = f.read()
        locs.extend(re.findall(r'<loc>(.*?)</loc>', content))

    return len(locs), locs[:5]


def save_state(count):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"build_count": count, "recorded_at": str(__import__('datetime').datetime.now())}, f, indent=2)
    print(f"📝 Recorded build state: {count} pages")


def load_state():
    if not os.path.exists(STATE_FILE):
        return 0
    with open(STATE_FILE) as f:
        data = json.load(f)
    return data.get("build_count", 0)


def main():
    current_count, sample_urls = count_pages()
    
    if current_count == 0:
        print("❌ No built pages found. Run npm run build first.")
        return

    previous_count = load_state()
    
    print(f"📊 Built pages: {current_count}")
    print(f"📊 Previous build: {previous_count}")
    
    diff = current_count - previous_count
    
    if "--record" in sys.argv:
        save_state(current_count)
        return
    
    if previous_count == 0:
        print(f"📝 First run — recording baseline ({current_count} pages)")
        save_state(current_count)
        return
    
    if diff == 0:
        print(f"✅ Index stable: {current_count} pages (no change)")
    elif diff > 0:
        print(f"📈 Index grew: +{diff} pages (now {current_count})")
        print(f"   Sample new pages:")
        for url in (sample_urls or [])[:3]:
            print(f"     {url}")
    elif diff < 0:
        print(f"❌🚨 INDEX DROP: -{abs(diff)} pages LOST (was {previous_count}, now {current_count})")
        if sample_urls:
            print(f"   Remaining pages (sample):")
            for url in sample_urls[:5]:
                print(f"     {url}")
        print(f"\n   Action needed: check what dropped out of the build")
    
    # Always update to new count
    save_state(current_count)


if __name__ == "__main__":
    main()