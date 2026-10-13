// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

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
      lastmod: new Date(),
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
