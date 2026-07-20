#!/usr/bin/env python3
"""Friday Affiliate Health Check
Scans all content for affiliate links, reports gaps, counts, and trends.
Pulls next blue sky idea from Obsidian vault, marks it as shown.
Runs as a cron job every Friday 5pm. Stdout is delivered to Shane.
"""

import os
import re
from datetime import datetime
from collections import defaultdict

BLOG_DIR = os.path.expanduser("~/tradieautomate/repo/src/content/blog")
PAGES_DIR = os.path.expanduser("~/tradieautomate/repo/src/pages")
OBSIDIAN_VAULT = os.path.expanduser("~/Desktop/MyObsidianVault/Projects/TradieAutomate")
BLUE_SKY_FILE = os.path.join(OBSIDIAN_VAULT, "Blue Sky Ideas.md")

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


def pick_blue_sky_idea():
    """Read Obsidian blue sky file, pick next proposed idea, mark it shown."""
    if not os.path.exists(BLUE_SKY_FILE):
        return None, None

    with open(BLUE_SKY_FILE) as f:
        content = f.read()

    # Find next proposed idea
    pattern = r'### (.+?)\n- \*\*Status:\*\* 🆕 proposed'
    match = re.search(pattern, content)
    if not match:
        return "No proposed ideas remaining. Add new ones to Blue Sky Ideas.md.", None

    idea_name = match.group(1).strip()
    today = datetime.now().strftime("%d %b %Y")

    # Mark as shown
    content = content.replace(
        f"### {idea_name}\n- **Status:** 🆕 proposed",
        f"### {idea_name}\n- **Status:** 📤 shown",
    )

    # Update first shown if blank
    if f"### {idea_name}\n- **Status:** 📤 shown\n- **First shown:** —" in content:
        content = content.replace(
            f"### {idea_name}\n- **Status:** 📤 shown\n- **First shown:** —",
            f"### {idea_name}\n- **Status:** 📤 shown\n- **First shown:** {today}",
        )

    # Increment shown count
    shown_count_pattern = rf'(### {re.escape(idea_name)}\n.*?\n- \*\*Shown count:\*\* )(\d+)'
    count_match = re.search(shown_count_pattern, content, re.DOTALL)
    if count_match:
        new_count = int(count_match.group(2)) + 1
        content = content[:count_match.start(2)] + str(new_count) + content[count_match.end(2):]

    # Get description
    desc_pattern = rf'### {re.escape(idea_name)}\n.*?\n- \*\*Description:\*\* (.+?)(?:\n\n|\n###|\n---|\Z)'
    desc_match = re.search(desc_pattern, content, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else "No description."

    # Update the log table
    log_entry = f"| {idea_name} | {today} | {count_match and int(count_match.group(2)) + 1 or 1} | {today} | — |"
    if "| Fate |" in content:
        # Check if this idea already has a log entry
        if f"| {idea_name} |" in content.split("## Shown Ideas Log")[1] if "## Shown Ideas Log" in content else False:
            # Update existing log entry
            old_log = re.search(rf'\| {re.escape(idea_name)} \| (.+?) \|', content.split("## Shown Ideas Log")[1])
            if old_log:
                parts = old_log.group(1).split("|")
                shown_count = int(parts[1].strip()) + 1
                new_log = f"| {idea_name} | {parts[0].strip()} | {shown_count} | {today} | — |"
                content = content.replace(old_log.group(0), new_log)
        else:
            # Add new log entry before the closing
            content = content.replace("| Fate |\n", f"| Fate |\n{log_entry}\n")

    # Write back
    with open(BLUE_SKY_FILE, "w") as f:
        f.write(content)

    return idea_name, description


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
        print(f"⚠️  {without_utm} links missing UTM tracking.")

    # Blue sky idea from Obsidian
    idea_name, description = pick_blue_sky_idea()
    if idea_name:
        print()
        print(f"🎯 BLUE SKY: {idea_name}")
        print(f"   {description}")
        print(f"   → Full list + status: Obsidian/Projects/TradieAutomate/Blue Sky Ideas.md")


if __name__ == "__main__":
    main()
