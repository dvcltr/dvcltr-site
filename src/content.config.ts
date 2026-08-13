import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const status = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/status' }),
  schema: z.object({
    title: z.string(),
    date: z.date(),
    course: z.string().optional(),
    summary: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { status };
