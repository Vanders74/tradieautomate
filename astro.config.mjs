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

// Tool pages are .astro, so they carry no frontmatter date and previously
// serialized with NO lastmod. That left the two money tools sitting at
// "Discovered - currently not indexed" for 90 days. These dates are the real
// last-substantive-change commits (git log -1 --format=%cI) for each file.
// UPDATE the matching entry whenever a tool page's content changes.
const TOOL_LASTMOD = {
  '/tools/rebate-finder/': '2026-10-26T02:12:00+11:00',
  '/tools/trade-business-valuation/': '2026-10-26T01:26:46+11:00',
  '/tools/admin-cost-calculator/': '2026-10-23T20:31:34+11:00',
  '/tools/solar-savings-calculator/': '2026-10-23T20:31:34+11:00',
  '/tools/ev-charger-quote-calculator/': '2026-10-19T13:28:48+11:00',
  '/tools/solar-quote-calculator/': '2026-08-08T04:48:05+10:00',
  '/tools/': '2026-10-27T04:07:46+11:00',
};

function buildLastmodMap() {
  const map = new Map();
  for (const [p, raw] of Object.entries(TOOL_LASTMOD)) {
    const d = new Date(raw);
    if (!Number.isNaN(d.getTime())) map.set(p, d.toISOString());
  }
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
