# STM Studio - Static Site

Flattened version of stm.studio, originally built in Framer. Goal: stop paying for Framer hosting while the site is dormant.

## Current State

Static HTML files scraped from the Framer-hosted site (Aug 2025):

```
stm.studio/
├── index.html              # Homepage (238KB - includes inline CSS/JS)
├── philosophy.html         # Philosophy page (102KB)
├── robots.txt
└── explorations/
    ├── can-mobility-be-smarter-in-the-age-of-ai-and-autonomy-certainly.html
    ├── telling-the-story-of-the-u-s-racial-wealth-gap-with-data-visualization.html
    ├── improving-team-success-via-ai-meeting-feedback.html
    └── the-changing-economics-of-digital-product-development.html
```

**Total size:** ~760KB

## GitHub Pages Preview

Once deployed, preview at: https://chrisarusso.github.io/stm-studio-static/stm.studio/

If it looks good, point stm.studio DNS to GitHub Pages to stop paying Framer.

## Future: Framework Migration

The current HTML files are monolithic (inline CSS/JS from Framer). For easier maintenance, consider migrating to a static site generator:

### Recommended: Astro

- **Why:** Great for content sites, supports markdown, zero JS by default, fast builds
- **GitHub Pages:** Built-in adapter, free hosting
- **Migration path:** Extract content from HTML into markdown, use Astro components for layout
- **Docs:** https://astro.build

### Alternatives

| Framework | Pros | Cons |
|-----------|------|------|
| **11ty (Eleventy)** | Simple, flexible, fast | Less opinionated (more decisions) |
| **Hugo** | Extremely fast builds | Go templating has learning curve |
| **Next.js (static export)** | React ecosystem | Overkill for simple content site |

### Migration Steps (when ready)

1. Extract content from HTML files into markdown
2. Set up Astro with a simple template
3. Deploy to GitHub Pages via GitHub Actions
4. Update DNS from Framer to GitHub Pages

## Design Resources

- **STM Branding (Figma):** https://www.figma.com/design/QCLxZEYSwD6YNSmdj2f0hv/-STM--Branding?node-id=158-1247

## HubSpot Form

The Framer site uses a HubSpot form embedded via Framer component. For the static version, use this embed code:

```html
<script charset="utf-8" type="text/javascript" src="//js.hsforms.net/forms/embed/v2.js"></script>
<script>
  hbspt.forms.create({
    region: "na1",
    portalId: "21460480",
    formId: "a324830d-d9a4-4e46-af70-61e4e1731eda"
  });
</script>
```

**Form details:**
- Name: STM contact collection form
- Fields: Email only
- Post-submit: Thank you message

## Local Preview

```bash
cd stm.studio
python -m http.server 8000
# Visit http://localhost:8000
```

## DNS Cutover (when ready)

1. Verify GitHub Pages site matches Framer
2. In DNS provider, update stm.studio:
   - Remove Framer CNAME/A records
   - Add CNAME: `chrisarusso.github.io`
3. In GitHub repo settings, add custom domain: `stm.studio`
4. Cancel Framer subscription

## Known Issues

- **Email form not working:** The static HTML has a Framer component placeholder (`hubspot_form_OLEiFDf49`) but not the actual HubSpot embed. Need to manually add the embed code above to `index.html` before DNS cutover.
