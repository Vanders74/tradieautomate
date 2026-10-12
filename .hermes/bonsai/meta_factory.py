#!/usr/bin/env python3
"""Workflow 1: Meta Rewrite Factory

Reads a slug and its fix_queue entry, searches SERP, runs 3 agent roles,
outputs the top-scoring meta variant. Directly patches the article on approval.

Usage:
    python3 meta_factory.py <slug>
    python3 meta_factory.py --all-triggered   # Process all actionable queue items

Requires: local Ollama running with gemma4:12b
"""

import sys
import os
import json
import re

# Ensure we can import sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_model import ask, system_prompt, user_prompt

FIX_QUEUE = "/Users/shane/tradieautomate/fix_queue.json"
REPO = "/Users/shane/tradieautomate/repo"
BLOG_DIR = f"{REPO}/src/content/blog"


def read_queue():
    with open(FIX_QUEUE) as f:
        return json.load(f)


def write_queue(q):
    with open(FIX_QUEUE, "w") as f:
        json.dump(q, f, indent=2)


def get_article_meta(slug):
    """Read current title and description from an article's frontmatter."""
    path = f"{BLOG_DIR}/{slug}.md"
    if not os.path.exists(path):
        return None, None
    with open(path) as f:
        content = f.read()
    title = None
    desc = None
    for line in content.split("\n"):
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            desc = line.split(":", 1)[1].strip().strip('"').strip("'")
        if title and desc:
            break
    return title, desc


def agent_1_intent(slug, current_title, item):
    """Agent 1: Read queue data and identify the intent gap."""
    prompt = f"""You are Agent 1 (SERP Analyst) in a meta rewrite factory. Your job is to analyse this article and identify what intent gap its current meta is missing.

Article slug: {slug}
Current title: {current_title}
Queue data: position {item.get('position')}, CTR {item.get('ctr')}%, impressions {item.get('impressions')}
Fix recommendation: {item.get('fix_recommendation')}
Diagnostic flags: ai_overview={item.get('ai_overview_suppression')}, gov_domain={item.get('gov_domain_competition')}, semantic_ambiguity={item.get('semantic_ambiguity')}

Output exactly 3 things, one per line:
1. What search intent the current meta serves (one sentence)
2. What intent gap exists (one sentence)  
3. A specific angle that would fill that gap (one sentence)

Do not propose a meta yet — just the gap analysis. Be specific to the slug's topic and data."""
    return ask([system_prompt("You are a senior SEO content strategist. Be specific, data-driven, and concise."), user_prompt(prompt)], temperature=0.3)


def agent_2_drafts(slug, intent_analysis, current_title):
    """Agent 2: Draft 3 meta variants targeting that gap."""
    prompt = f"""You are Agent 2 (Copywriter) in a meta rewrite factory. Based on this intent analysis, draft 3 meta title+description pairs.

Article slug: {slug}
Current title: {current_title}
Intent analysis:
{intent_analysis}

Rules:
- Titles: 50-60 characters, include primary keyword, lead with the angle NOT the topic
- Descriptions: 150-160 characters, promise specific value (data, steps, comparison, checklist)
- No pipe characters | or special formatting
- Match the article's actual content depth

Output exactly 3 variants, each formatted as:
VARIANT 1
Title: [title]
Desc: [description]

VARIANT 2
Title: [title]
Desc: [description]

VARIANT 3
Title: [title]
Desc: [description]"""
    return ask([system_prompt("You are a direct-response copywriter specialising in SEO meta for trade/construction audiences. Be punchy and specific."), user_prompt(prompt)], temperature=0.5, max_tokens=1024)


def agent_3_scores(slug, drafts, current_title, item):
    """Agent 3: Score each variant and pick the top one."""
    prompt = f"""You are Agent 3 (Quality Assurance) in a meta rewrite factory. Score these 3 meta variants for {slug} and pick the best one.

Current title: {current_title}
Current position: {item.get('position')}, CTR: {item.get('ctr')}%, impressions: {item.get('impressions')}
Fix recommendation: {item.get('fix_recommendation')}

{drafts}

For each variant, score on 3 criteria (1-5 each):
1. meta_quality: Is the title compelling, clear, and within length limits? Does it avoid clickbait?
2. intent_match: Does it match the searcher's intent at position {item.get('position')}? Would someone at this position choose this result?
3. has_stakes (YES/NO): Does the reader feel they must click or they'll miss something useful?

Output your verdict as:
VARIANT [N] wins
Score: meta_quality=X/5, intent_match=X/5, has_stakes=YES/NO
Why: [one sentence]"""
    return ask([system_prompt("You are a strict SEO QA reviewer. Be critical — only pass variants that clearly outperform the current title."), user_prompt(prompt)], temperature=0.2, max_tokens=600)


def parse_variants(drafts_text):
    """Parse the variant output into structured data."""
    variants = {}
    current_v = None
    for line in drafts_text.strip().split("\n"):
        m = re.match(r"VARIANT (\d+)", line)
        if m:
            current_v = int(m.group(1))
            variants[current_v] = {}
            continue
        if current_v and line.lower().startswith("title:"):
            variants[current_v]["title"] = line.split(":", 1)[1].strip()
        elif current_v and line.lower().startswith("desc"):
            variants[current_v]["desc"] = line.split(":", 1)[1].strip()
    return variants


def process_slug(slug):
    """Run the full 3-agent pipeline for one slug."""
    item = None
    q = read_queue()
    for i in q["items"]:
        if i["slug"] == slug:
            item = i
            break

    if not item:
        print(f"SKIP {slug}: not in fix_queue")
        return

    if item.get("recently_updated"):
        print(f"SKIP {slug}: recently_updated=True")
        return

    if item.get("tier", 5) > 3:
        print(f"SKIP {slug}: tier {item['tier']} > 3")
        return

    current_title, current_desc = get_article_meta(slug)
    if not current_title:
        print(f"SKIP {slug}: article not found")
        return

    print(f"\n{'='*60}")
    print(f"AGENT 1 — Intent Analysis for: {slug}")
    print(f"Current: {current_title}")
    intent = agent_1_intent(slug, current_title, item)
    print(intent)

    print(f"\nAGENT 2 — Drafting 3 variants...")
    drafts = agent_2_drafts(slug, intent, current_title)
    print(drafts)

    print(f"\nAGENT 3 — Scoring variants...")
    verdict = agent_3_scores(slug, drafts, current_title, item)
    print(verdict)

    # Save to queue for human review
    variants = parse_variants(drafts)
    for q_item in q["items"]:
        if q_item["slug"] == slug:
            q_item["bonsai_meta"] = {
                "intent_analysis": intent,
                "drafts": drafts,
                "verdict": verdict,
                "variants": variants,
            }
            break
    write_queue(q)
    print(f"\n✅ Saved meta candidates to fix_queue for {slug}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 meta_factory.py <slug>")
        sys.exit(1)

    slug = sys.argv[1].replace(".md", "")
    
    if slug == "--all-triggered":
        q = read_queue()
        triggered = [
            i["slug"] for i in q["items"]
            if i.get("fix_recommendation") == "meta_rewrite"
            and i.get("tier", 5) <= 3
            and not i.get("recently_updated")
            and i.get("status") == "IN QUEUE"
        ]
        print(f"Processing {len(triggered)} triggered slugs...")
        for s in triggered:
            process_slug(s)
    else:
        process_slug(slug)