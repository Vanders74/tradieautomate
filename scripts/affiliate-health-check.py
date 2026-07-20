#!/usr/bin/env python3
"""Friday Affiliate Health Check
Scans all content for affiliate links, reports gaps, counts, and trends.
Runs as a cron job every Friday 5pm. Stdout is delivered to Shane.
"""

import os
import re
from datetime import datetime
from collections import defaultdict

BLOG_DIR = os.path.expanduser("~/tradieautomate/repo/src/content/blog")
PAGES_DIR = os.path.expanduser("~/tradieautomate/repo/src/pages")

AFFILIATE_DOMAINS = {
    "servicem8.com": "ServiceM8",
}

def scan_links(content, filepath):
    """Find all markdown links in content."""
    links = []
    # Match [text](url) and bare URLs with ref=tradieautomate
    pattern = r'\[([^\]]*)\]\((https?://[^\s\)]+)\)'
    for match in re.finditer(pattern, content):
        text, url = match.group(1), match.group(2)
        for domain, name in AFFILIATE_DOMAINS.items():
            if domain in url and "ref=tradieautomate" in url:
                has_utm = "utm_source" in url
                links.append({
                    "file": filepath,
                    "domain": domain,
                    "name": name,
                    "url": url,
                    "has_utm": has_utm,
                    "text": text,
                })
    return links


def main():
    all_links = []
    files_scanned = 0
    file_link_counts = defaultdict(int)

    for root_dir in [BLOG_DIR, PAGES_DIR]:
        if not os.path.exists(root_dir):
            continue
        for dirpath, _, filenames in os.walk(root_dir):
            for fn in filenames:
                if fn.endswith((".md", ".astro")):
                    filepath = os.path.join(dirpath, fn)
                    files_scanned += 1
                    try:
                        with open(filepath) as f:
                            content = f.read()
                        links = scan_links(content, filepath)
                        if links:
                            file_link_counts[filepath] = len(links)
                        all_links.extend(links)
                    except Exception:
                        pass

    # Stats
    total = len(all_links)
    with_utm = sum(1 for l in all_links if l["has_utm"])
    without_utm = total - with_utm
    domains = defaultdict(int)
    for l in all_links:
        domains[l["name"]] += 1

    # Top linked files
    top_files = sorted(file_link_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    now = datetime.now().strftime("%A %d %b %Y %H:%M AEST")

    print(f"🔗 Affiliate Link Health Check — {now}")
    print()
    print(f"Files scanned:  {files_scanned}")
    print(f"Affiliate links: {total}")
    print(f"UTM tracked:    {with_utm}/{total} ({int(with_utm/total*100) if total else 0}%)")
    print(f"Missing UTM:     {without_utm}")
    print()

    print("By domain:")
    for name, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * min(count // 5, 20)
        print(f"  {name:15s} {count:4d} {bar}")

    print()
    print("Top 5 linked articles:")
    for fp, count in top_files:
        short = fp.replace(str(BLOG_DIR) + "/", "").replace(str(PAGES_DIR) + "/", "")
        print(f"  {count:3d} links — {short}")

    if without_utm > 0:
        print()
        print(f"⚠️  {without_utm} links missing UTM tracking — run the affiliate UTM script.")

    # Blue sky idea — rotates each week based on even/odd week number
    week = datetime.now().isocalendar()[1]
    ideas = [
        "🎯 BLUE SKY: Xero affiliate. Every ServiceM8 article mentions Xero integration. Natural next program. $5-10 per signup. Estimate: 2-5 conversions/week from existing traffic.",
        "🎯 BLUE SKY: Insurance comparison. Every licensing guide mentions $5M-$20M PL insurance. Partner with a trade insurer for quote referrals. Higher commission per lead than software.",
        "🎯 BLUE SKY: Trade equipment reviews. Multimeters, testers, thermal cameras — every sparky buys them. Amazon AU affiliate links on comparison articles. Low effort, passive.",
        "🎯 BLUE SKY: TradieAutomate becomes Wirecutter for trades. Expand affiliate across Xero, MYOB, Tradify, insurance, equipment. One trust source for every contractor purchase decision.",
    ]
    print()
    print(ideas[week % len(ideas)])


if __name__ == "__main__":
    main()
