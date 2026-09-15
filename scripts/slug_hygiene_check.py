#!/usr/bin/env python3
"""Pre-PR slug-hygiene gate for TradieAutomate content.

Catches the three classes of self-inflicted SEO damage BEFORE a PR opens:

1. RENAMED without redirect  — GSC keeps impressions on old URLs; clicks 404.
   Detects: any URL that Google knows (from dashboard.json GSC rows) but that
   has no source file AND no netlify.toml redirect → needs a 301.

2. DELETED but still linked  — internal links pointing at a slug with no
   source file and no redirect (fresh 404s from consolidation).
   Detects: grep every .md/.astro for /blog/<slug> links, cross-check slug
   against live source files + netlify.toml redirect sources.

3. STALE source with redirect — a source file exists while its URL 301s
   elsewhere (pollutes the sitemap with a redirecting URL).
   Detects: source slug appears as a redirect source in netlify.toml.

Exit code: 0 = clean, 1 = issues found (block the PR).
"""
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BLOG = REPO / "src" / "content" / "blog"
NETLIFY = REPO / "netlify.toml"
DASHBOARD = Path(os.environ.get("HOME") or "") / "tradieautomate" / "dashboard.json"


def load_redirect_map():
    if not NETLIFY.exists():
        return {}
    text = NETLIFY.read_text()
    blocks = re.findall(r"\[\[redirects\]\](.*?)(?=\n\[\[redirects\]\]|\Z)", text, re.S)
    out = {}
    for b in blocks:
        m_from = re.search(r'from\s*=\s*"([^"]+)"', b)
        m_to = re.search(r'to\s*=\s*"([^"]+)"', b)
        if m_from and m_to:
            out[m_from.group(1).rstrip("/")] = m_to.group(1).rstrip("/")
    return out


def load_gsc_slugs():
    """Slugs Google served impressions for (28d), from the live dashboard."""
    if not DASHBOARD.exists():
        return set()
    import json
    try:
        data = json.loads(DASHBOARD.read_text())
        slugs = set()
        for p in data.get("gsc", {}).get("pages", []):
            s = p.get("slug", "")
            if s:
                slugs.add(s)
        return slugs
    except Exception:
        return set()


def load_internal_links():
    """Every /blog/<slug> link across content + pages."""
    links = set()
    pat = re.compile(r"\(/blog/([a-z0-9-]+?)/?\)")
    for root in (BLOG, REPO / "src" / "pages"):
        if not root.exists():
            continue
        for f in root.rglob("*"):
            if f.suffix in (".md", ".mdx", ".astro") and f.is_file():
                try:
                    links.update(pat.findall(f.read_text(errors="ignore")))
                except Exception:
                    pass
    return links


def main():
    issues = []
    redirects = load_redirect_map()
    live_slugs = {f.stem for f in BLOG.glob("*.md")}
    redirect_sources = {k.rsplit("/", 1)[-1] for k in redirects}

    # Non-blog pages that legitimately exist outside /blog/ (about, services,
    # tools, calculators, playbook, etc.) — never flag these as renames.
    non_blog = set()
    pages_dir = REPO / "src" / "pages"
    if pages_dir.exists():
        for f in pages_dir.rglob("*"):
            if f.suffix == ".astro" and f.is_file():
                rel = f.relative_to(pages_dir)
                stem = rel.with_suffix("").as_posix()
                # Directory index -> the dir name (tradie-brain/index.astro -> tradie-brain)
                if stem.endswith("/index"):
                    stem = stem[: -len("/index")]
                # index.astro at root -> homepage, skip
                if stem in ("", "index"):
                    continue
                non_blog.add(stem)
                non_blog.add(stem.rsplit("/", 1)[-1])

    # 1. Google-known slugs with no source and no redirect = renamed without 301
    gsc = load_gsc_slugs()
    for slug in sorted(gsc):
        slug = slug.removesuffix(".html")  # GSC sometimes reports 'foo.html'
        if slug in non_blog or slug == "index":
            continue  # legit standalone page (services, tools, homepage, etc.)
        if slug not in live_slugs and slug not in redirect_sources:
            issues.append(f"[RENAME-NO-301] '{slug}' has GSC impressions but no source file and no redirect — add a 301 in netlify.toml")

    # 2. Internal links to dead slugs (no source, no redirect)
    for slug in sorted(load_internal_links()):
        if slug in non_blog:
            continue
        if slug not in live_slugs and slug not in redirect_sources:
            issues.append(f"[DEAD-LINK] '/blog/{slug}/' is linked internally but has no source file and no redirect")

    # 3. Stale source: file exists but its URL redirects AWAY to a DIFFERENT
    #    article (consolidation). Trailing-slash self-redirects (/slug -> /slug/)
    #    are canonicalisation, not consolidation — skip those.
    for slug in sorted(live_slugs):
        if slug in redirect_sources:
            target = redirects.get(f"/blog/{slug}")
            if target and target.rstrip("/") != f"/blog/{slug}":
                issues.append(f"[STALE-SOURCE] '{slug}.md' exists but netlify.toml redirects its URL to '{target}' — delete the source, keep the redirect")

    if issues:
        print(f"🚫 slug-hygiene gate FAILED — {len(issues)} issue(s):\n")
        for i in issues:
            print(f"  • {i}")
        print("\nFix these before opening the PR (add 301s, repoint links, or delete stale sources).")
        return 1
    print("✅ slug-hygiene gate passed — no renamed-without-301, dead links, or stale sources.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
