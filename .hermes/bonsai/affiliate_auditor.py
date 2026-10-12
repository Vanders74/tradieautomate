#!/usr/bin/env python3
"""Workflow 4: Affiliate CTA Auditor

Reads an article and identifies every natural CTA point, checks if each has
an affiliate link, and drafts missing anchor text + placement. Runs per-PR.

Usage:
    python3 affiliate_auditor.py <slug>
    python3 affiliate_auditor.py --all-articles   # Scan articles without affiliate links
"""

import sys
import os
import json
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_model import ask, system_prompt, user_prompt

REPO = "/Users/shane/tradieautomate/repo"
BLOG_DIR = f"{REPO}/src/content/blog"
SERVICEM8_PATTERN = r"servicem8\.com"


def list_articles():
    """List all blog article slugs."""
    slugs = []
    for f in os.listdir(BLOG_DIR):
        if f.endswith(".md") and not f.startswith("_"):
            slugs.append(f.replace(".md", ""))
    return slugs


def has_affiliate_link(slug):
    """Check if an article already contains ServiceM8 affiliate links."""
    path = f"{BLOG_DIR}/{slug}.md"
    if not os.path.exists(path):
        return False
    with open(path) as f:
        content = f.read()
    return bool(re.search(SERVICEM8_PATTERN, content, re.IGNORECASE))


def read_article(slug):
    """Read article content."""
    path = f"{BLOG_DIR}/{slug}.md"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return f.read()


def audit_article(slug, content, has_links):
    """Run 3-agent audit on one article."""
    link_status = "ALREADY HAS ServiceM8 affiliate links" if has_links else "NO affiliate links found"
    
    agent1 = f"""You are Agent 1 (Content Reader). Read this article and identify every natural point where a trade software recommendation or CTA would help the reader.

Article slug: {slug}
{link_status}
Content preview:
{content[:5000]}

List exactly 3-5 natural CTA points from the article. For each:
- Quote the surrounding sentence (up to 50 chars)
- State what software category would be relevant (job management, CRM, quoting, accounting, etc.)
- Rate the commercial intent HIGH/MED/LOW"""
    
    a1 = ask([system_prompt("You read trade blog content and identify commercial opportunities. Be specific about CTA placement, not generic."), user_prompt(agent1)], temperature=0.3, max_tokens=800)

    agent2 = f"""You are Agent 2 (Affiliate Checker). Based on these CTA points, identify which ones are missing or weak ServiceM8 affiliate links.

Article slug: {slug}
{link_status}

CTA points identified:
{a1}

For each point:
- If already linked to ServiceM8: mark EXISTS
- If not linked but could be: write the missing anchor text (max 8 words) and the context sentence where it fits
- If not relevant to ServiceM8: mark SKIP (and suggest which service it IS relevant to)
- Be honest — don't force ServiceM8 into irrelevant sections"""
    a2 = ask([system_prompt("You verify affiliate link placement. Only recommend links where ServiceM8 is genuinely relevant — don't force it."), user_prompt(agent2)], temperature=0.3, max_tokens=800)

    agent3 = f"""You are Agent 3 (Copywriter). Draft the final recommended CTA block(s) for this page.

Article slug: {slug}
{link_status}

Findings:
{a2}

Output exactly:
1. Insert after: [quote the nearest heading or sentence marker — be specific]
2. CTA text: [the recommended anchor text]
3. CTA link: [servicem8.com/...?ref=tradieautomate with relevant UTM]

If no changes needed, output: NO CHANGES NEEDED"""
    a3 = ask([system_prompt("You write concise affiliate CTAs for Australian trade audiences. Direct, no fluff. Anchor text should be action-oriented."), user_prompt(agent3)], temperature=0.4, max_tokens=600)

    return a1, a2, a3


def main(target_slug=None):
    if target_slug:
        slugs = [target_slug]
    else:
        slugs = list_articles()

    results = []
    for slug in slugs:
        content = read_article(slug)
        if not content:
            continue
        
        has_links = has_affiliate_link(slug)
        a1, a2, a3 = audit_article(slug, content, has_links)
        
        print(f"\n{'='*60}")
        print(f"Article: {slug} {'🔗' if has_links else '❌ missing'}")
        print(f"\nAgent 1 — Natural CTA points:")
        print(a1[:400])
        print(f"\nAgent 2 — Affiliate check:")
        print(a2[:400])
        print(f"\nAgent 3 — Recommended CTAs:")
        print(a3)
        
        if not has_links and "NO CHANGES NEEDED" not in a3:
            results.append({"slug": slug, "recommendation": a3})
        
        if target_slug:
            break  # Single article mode

    if target_slug and results:
        print(f"\n{'='*60}")
        print("SUMMARY: Missing affiliate CTAs found — add these manually via PR.")
        for r in results:
            print(f"\n  → {r['slug']}:")
            print(f"    {r['recommendation'][:300]}")
    elif not target_slug:
        linked = sum(1 for s in slugs if has_affiliate_link(s))
        total = len(slugs)
        print(f"\n{'='*60}")
        print(f"Site audit: {linked}/{total} articles have ServiceM8 affiliate links")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] != "--all-articles":
        slug = sys.argv[1].replace(".md", "")
        main(slug)
    else:
        # --all-articles or no args: scan a sample
        main()