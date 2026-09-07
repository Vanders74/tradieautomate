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
		// Mobile-first key-concepts summary rendered after the title ("The Breakdown")
		breakdown: z.array(z.object({
			title: z.string(),
			summary: z.string(),
			href: z.string().optional(),
			hrefLabel: z.string().optional(),
			external: z.boolean().optional(),
		})).optional(),
		faq: z.array(z.object({
			question: z.string(),
			answer: z.string(),
		})).optional(),
	}),
});

export const collections = { blog };
