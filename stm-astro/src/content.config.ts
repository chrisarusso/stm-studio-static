import { defineCollection, z } from 'astro:content';

// Define the explorations collection for blog-like posts
const explorations = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    pubDate: z.date(),
    type: z.enum(['exploration', 'thought']).default('exploration'),
    draft: z.boolean().default(false),
  }),
});

export const collections = {
  explorations,
};
