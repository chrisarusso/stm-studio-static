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
├── layouts/
│   ├── Base.astro      # Base layout with GA, meta tags
│   └── BlogPost.astro  # Blog post layout (extends Base)
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

## Layouts

### Base Layout
All new pages should use `Base.astro` which includes:
- Google Analytics (`G-0Z29ZWLNB4`)
- Meta tags (title, description, Open Graph)
- Favicon

```astro
---
import Base from '../layouts/Base.astro';
---

<Base title="Page Title" description="Optional description">
  <main>
    Your content here
  </main>
</Base>
```

### BlogPost Layout
For explorations and thoughts:

```astro
---
import BlogPost from '../layouts/BlogPost.astro';
---

<BlogPost
  title="Your Post Title"
  description="Brief description"
  pubDate={new Date('2025-01-29')}
  type="exploration"
>
  <p>Your content here...</p>
</BlogPost>
```

## Adding New Blog Posts

For simple markdown posts, create in `src/content/explorations/`:

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
They have Google Analytics hardcoded inline - this is fine.

For **new pages**, use the `Base.astro` or `BlogPost.astro` layouts.

To convert an existing HTML page to Astro:
1. Rename `.html` to `.astro`
2. Wrap content with `<Base>` or `<BlogPost>` layout
3. Remove the inline GA code (layout handles it)

---

## E2E Tests (Form Verification)

Tests verify the HubSpot contact form works and notification emails are received.

```bash
# Install dependencies
cd tests/e2e
pip install -r requirements.txt
playwright install chromium

# Run tests
pytest test_contact_form.py -v

# Run with visible browser
pytest test_contact_form.py -v --headed

# Skip email verification
VERIFY_EMAIL=false pytest test_contact_form.py -v

# Manual test with browser
python test_contact_form.py
```

**Requirements:**
- Gmail API credentials (reuses savaslabs.com-website/tests/e2e/credentials.json)
- HubSpot form notification configured to send to 987car@gmail.com
