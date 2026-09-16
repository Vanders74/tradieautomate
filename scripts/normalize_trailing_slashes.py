#!/usr/bin/env python3
"""Normalize internal markdown links to trailing-slash canonical form.

Fixes: [text](/blog/slug) -> [text](/blog/slug/)
       [text](/blog/slug#anchor) -> [text](/blog/slug/#anchor)  (keeps anchor)
       [text](/blog/slug?x=1) -> [text](/blog/slug/?x=1)        (keeps query)

Leaves untouched: external URLs, already-slashed links, root-relative
non-blog paths (/services, /tools, /playbook, /compliance-checklist —
these are also canonicalized by Netlify but fixing 1,273 blog links is
the high-value batch; only blog links are in scope here).

Why: 1,273 internal no-slash /blog/ links make Google re-discover the
no-slash variants, which 301 to the slash canonical, which GSC reports as
"pages with redirect". Normalizing the internal graph to the canonical
form stops the redirects at the source.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "src"

# [text](/blog/slug)  — optional #anchor or ?query after slug
LINK_RE = re.compile(r"(\]\(/blog/[a-z0-9\-]+)([#?][^)]*)?\)")


def normalize(text: str) -> str:
    def repl(m):
        path, suffix = m.group(1), m.group(2) or ""
        return f"{path}/{suffix})"
    return LINK_RE.sub(repl, text)


def main():
    changed = 0
    total = 0
    for f in SRC.rglob("*"):
        if f.suffix not in (".md", ".mdx", ".astro"):
            continue
        orig = f.read_text(errors="ignore")
        new = normalize(orig)
        if new != orig:
            n = len(LINK_RE.findall(orig))
            f.write_text(new)
            changed += 1
            total += n
            print(f"  {n:4d} links  {f.relative_to(REPO)}")
    print(f"\nDone: {total} links normalized across {changed} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
