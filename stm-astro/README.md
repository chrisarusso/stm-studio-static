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

---

## TODO: Google Analytics

Currently, Google Analytics (`G-0Z29ZWLNB4`) is hardcoded in each HTML file's `<head>`.

When converting to proper Astro layouts, centralize this:

1. Create `src/layouts/Base.astro` with the gtag snippet
2. Or use `@astrojs/partytown` for better performance (moves analytics to web worker)
3. Consider environment-based loading (don't track in dev)

Example centralized approach:
```astro
// src/layouts/Base.astro
---
const GA_ID = 'G-0Z29ZWLNB4';
---
<html>
<head>
  <script async src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '{GA_ID}');
  </script>
</head>
```
