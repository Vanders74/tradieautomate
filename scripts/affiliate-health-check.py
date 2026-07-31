#!/usr/bin/env python3
"""Friday Affiliate Health Check — Data Layer
Scans all content for affiliate links, reports gaps, counts, and trends.
Stdout is fed as context to the cron agent which generates the blue sky idea.
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
    links = []
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

    total = len(all_links)
    with_utm = sum(1 for l in all_links if l["has_utm"])
    without_utm = total - with_utm
    domains = defaultdict(int)
    for l in all_links:
        domains[l["name"]] += 1

    top_files = sorted(file_link_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    now = datetime.now().strftime("%A %d %b %Y %H:%M AEST")

    print(f"Files scanned: {files_scanned}")
    print(f"Affiliate links: {total}")
    print(f"UTM tracked: {with_utm}/{total}")
    print(f"Missing UTM: {without_utm}")
    for name, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
        print(f"Domain: {name} = {count} links")
    print("Top linked:")
    for fp, count in top_files:
        short = fp.replace(str(BLOG_DIR) + "/", "")
        print(f"  {count}x — {short}")


if __name__ == "__main__":
    main()
