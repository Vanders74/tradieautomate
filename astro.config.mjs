// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import fs from 'node:fs';
import path from 'node:path';

// Per-page lastmod for the sitemap.
//
// The old config used `lastmod: new Date()`, which stamped EVERY url with the
// build time on every deploy. Google ignores a lastmod signal that claims the
// whole site changed daily — and a discounted lastmod is one less reason to
// recrawl. We now read each article's real updatedDate (falling back to
// pubDate) and omit lastmod entirely for pages with no real date, rather than
// publishing a false one.
const BLOG_DIR = './src/content/blog';

function buildLastmodMap() {
  const map = new Map();
  let files = [];
  try {
    files = fs.readdirSync(BLOG_DIR);
  } catch {
    return map;
  }
  for (const f of files) {
    if (!f.endsWith('.md')) continue;
    const txt = fs.readFileSync(path.join(BLOG_DIR, f), 'utf8');
    const fm = txt.split('---')[1] || '';
    const pick = (key) => {
      const m = fm.match(new RegExp(`^${key}:\\s*['"]?([^'"\\n]+)`, 'm'));
      return m ? m[1].trim() : null;
    };
    const raw = pick('updatedDate') || pick('pubDate');
    if (!raw) continue;
    const d = new Date(raw);
    if (Number.isNaN(d.getTime())) continue;
    map.set(`/blog/${f.slice(0, -3)}/`, d.toISOString());
  }
  return map;
}

const LASTMOD = buildLastmodMap();

// https://astro.build/config
export default defineConfig({
  site: 'https://tradieautomate.com',
  trailingSlash: 'always',
  markdown: {
    // CRITICAL: smartypants (default ON) converts straight quotes to curly
    // ones INSIDE raw HTML <script> blocks in markdown content. That turns
    // valid JS into a SyntaxError — the Plan Finder widget and every
    // yt-facade video script silently died because of this. Keep quotes
    // untouched so inline scripts survive the build intact.
    smartypants: false,
  },
  integrations: [
    mdx(),
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      serialize(item) {
        try {
          const p = new URL(item.url).pathname;
          const real = LASTMOD.get(p);
          if (real) {
            item.lastmod = real;
          } else {
            // No truthful date available — omit rather than lie.
            delete item.lastmod;
          }
        } catch {
          delete item.lastmod;
        }
        return item;
      },
    }),
  ],
  redirects: {
    // 301 redirect: old SM8 review → canonical 2026 version
    // Preserves any existing backlinks/rankings for the old URL
    '/blog/servicem8-review': {
      status: 301,
      destination: '/blog/servicem8-review-2026',
    },
    '/blog/servicem8-review/': {
      status: 301,
      destination: '/blog/servicem8-review-2026/',
    },
  },
});
