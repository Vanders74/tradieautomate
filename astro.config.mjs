// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://tradieautomate.com',
  integrations: [mdx(), sitemap()],
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
