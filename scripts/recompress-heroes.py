#!/usr/bin/env python3
"""
Recompress oversized TradieAutomate hero images in public/.

Scans public/hero-*.jpg and public/hero-*.webp, recompresses any over the
size ceilings (JPG 200KB, WebP 100KB) using a quality-decrement loop until
they land comfortably under target (JPG ~180KB, WebP ~95KB). This is for the
SITE-WIDE backlog / periodic audit, not for a single new article.

Usage (run from repo root where public/ lives):
    python3 scripts/recompress-heroes.py          # dry run — report only
    python3 scripts/recompress-heroes.py --apply  # actually rewrite files

Note: this rewrites in place. Dimensions are preserved (heroes are already
1536x1024). Only files OVER the ceiling are touched.
"""
import argparse, glob, os, sys
from PIL import Image

JPG_LIMIT = 200_000
JPG_TARGET = 180_000
WEBP_LIMIT = 100_000
WEBP_TARGET = 90_000


def recompress(src, kind):
    img = Image.open(src).convert('RGB')
    if kind == 'jpg':
        target = JPG_TARGET
        q = 85
        while q >= 40:
            img.save(src, 'jpeg', quality=q, optimize=True)
            if os.path.getsize(src) < target:
                break
            q -= 3
    else:
        target = WEBP_TARGET
        q = 75
        while q >= 40:
            img.save(src, 'webp', quality=q)
            if os.path.getsize(src) < target:
                break
            q -= 3
    return os.path.getsize(src)


def main():
    apply = '--apply' in sys.argv
    report = []
    for kind, limit in (('jpg', JPG_LIMIT), ('webp', WEBP_LIMIT)):
        for src in glob.glob(f'public/hero-*.{kind}'):
            sz = os.path.getsize(src)
            if sz > limit:
                slug = os.path.splitext(os.path.basename(src))[0][5:]
                report.append((slug, kind, sz, None))
    if not report:
        print('No oversized heroes found.')
        return

    print(f"{'APPLYING' if apply else 'DRY RUN'} — {len(report)} oversized file(s)")
    results = []
    for slug, kind, sz, _ in sorted(report, key=lambda r: -r[2]):
        src = f'public/hero-{slug}.{kind}'
        if apply:
            new = recompress(src, kind)
            results.append((slug, kind, sz, new))
            print(f'  {slug:58s} {kind}  {sz//1024:>5}KB -> {new//1024:>5}KB')
        else:
            print(f'  {slug:58s} {kind}  {sz//1024:>5}KB  (over limit)')

    if apply:
        still_over = [(s, k, o, n) for s, k, o, n in results if n >= (JPG_LIMIT if k == 'jpg' else WEBP_LIMIT)]
        if still_over:
            print(f'\n⚠ {len(still_over)} file(s) still over ceiling after recompress — inspect manually:')
            for s, k, o, n in still_over:
                print(f'  {s}.{k}: {n//1024}KB')
        else:
            print(f'\n✅ All {len(results)} file(s) now under ceiling.')


if __name__ == '__main__':
    main()
