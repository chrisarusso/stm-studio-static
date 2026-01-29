# STM Studio - Astro Version

Static site for stm.studio built with [Astro](https://astro.build).

## Structure

```
src/
├── pages/              # HTML/Astro pages (existing Framer export)
│   ├── index.html      # Homepage
│   ├── philosophy.html # Philosophy page
│   └── explorations/   # Article pages
├── content/
│   └── explorations/   # Future blog posts (Markdown)
└── layouts/            # Shared layouts (to be created)
public/
└── robots.txt
```

## Commands

| Command           | Action                                      |
| :---------------- | :------------------------------------------ |
| `npm install`     | Install dependencies                        |
| `npm run dev`     | Start dev server at `localhost:4321`        |
| `npm run build`   | Build production site to `./dist/`          |
| `npm run preview` | Preview build locally before deploying      |

## Adding New Blog Posts

1. Create a new `.md` file in `src/content/explorations/`
2. Add frontmatter:

```markdown
---
title: "Your Post Title"
description: "Brief description"
pubDate: 2025-01-29
type: exploration  # or 'thought'
draft: false
---

Your content here...
```

## Migration Notes

The existing HTML files from Framer are preserved as-is in `src/pages/`.
To fully convert to Astro components:

1. Rename `.html` to `.astro`
2. Extract common elements to layouts
3. Convert static content to use content collections

This allows incremental migration while keeping the site functional.
