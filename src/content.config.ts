import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
	// Load Markdown and MDX files in the `src/content/blog/` directory.
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	// Type-check frontmatter using a schema
	schema: z.object({
		title: z.string(),
		description: z.string(),
		// Transform string to Date object
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		heroImage: z.string().optional(),
		canonicalURL: z.string().optional(),
		category: z.string().optional(),
		// Slug of a visual guide to embed (renders <ExplodedDiagram> after the hero)
		diagram: z.string().optional(),
		faq: z.array(z.object({
			question: z.string(),
			answer: z.string(),
		})).optional(),
	}),
});

const visualGuides = defineCollection({
	loader: glob({ base: './src/content/visual-guides', pattern: '**/*.md' }),
	schema: z.object({
		title: z.string(),
		description: z.string(),
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		image: z.string(),               // /diagrams/[slug].svg
		imageAlt: z.string(),
		poster: z.string().optional(),   // /diagrams/[slug].png (og:image + fallback)
		aspectRatio: z.number(),          // width / height — reserves space, zero CLS
		caption: z.string().optional(),
		hotspots: z.array(z.object({
			id: z.string(),
			label: z.string(),
			note: z.string(),
			x: z.number(),                 // % of diagram width (0–100)
			y: z.number(),                 // % of diagram height (0–100)
			href: z.string().optional(),
			hrefLabel: z.string().optional(),
			external: z.boolean().optional(),
		})),
		cta: z.object({
			text: z.string(),
			href: z.string(),
			label: z.string(),
			external: z.boolean().optional(),
		}).optional(),
		faq: z.array(z.object({
			question: z.string(),
			answer: z.string(),
		})).optional(),
		related: z.array(z.string()).optional(),  // blog slugs to link
	}),
});

export const collections = { blog, visualGuides };
