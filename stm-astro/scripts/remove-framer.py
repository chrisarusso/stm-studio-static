#!/usr/bin/env python3
"""
Remove Framer dependencies from HTML files.
Converts the site to pure static HTML/CSS without JavaScript hydration.
"""

import re
import os
import sys
from pathlib import Path


def remove_framer_scripts(html: str) -> str:
    """Remove all Framer-related script tags."""

    # Remove Framer events/analytics script
    html = re.sub(
        r'<script[^>]*src="https://events\.framer\.com[^"]*"[^>]*></script>\s*',
        '',
        html
    )

    # Remove Framer main bundle script
    html = re.sub(
        r'<script[^>]*data-framer-bundle="main"[^>]*src="https://framerusercontent\.com[^"]*"[^>]*></script>\s*',
        '',
        html
    )

    # Remove framer/appear script blocks (including content)
    html = re.sub(
        r'<script[^>]*type="framer/appear"[^>]*>.*?</script>\s*',
        '',
        html,
        flags=re.DOTALL
    )

    # Remove framer appear animation script
    html = re.sub(
        r'<script[^>]*data-framer-appear-animation[^>]*>.*?</script>\s*',
        '',
        html,
        flags=re.DOTALL
    )

    # Remove inline Framer link handler script (starts with IIFE and contains hydrated check)
    html = re.sub(
        r'<script>\(?\(\)=>\{function \w+\(\)\{function \w+\([^)]*\)\{[^}]*createElement\("a"\).*?this\.dataset\.hydrated.*?</script>\s*',
        '',
        html,
        flags=re.DOTALL
    )

    # Remove inline Framer breakpoint sizes script
    html = re.sub(
        r'<script>\(?\(\)=>\{function \w+\(\)\{for\(let \w+ of document\.querySelectorAll\("\[data-framer-original-sizes\]"\).*?</script>\s*',
        '',
        html,
        flags=re.DOTALL
    )

    # Remove inline Framer animator script (contains transformPerspective)
    html = re.sub(
        r'<script>var animator=\(\(\)=>\{var \w+=\["transformPerspective".*?</script>\s*',
        '',
        html,
        flags=re.DOTALL
    )

    return html


def remove_framer_meta_tags(html: str) -> str:
    """Remove Framer-specific meta tags."""

    # Remove framer-search-index meta
    html = re.sub(
        r'<meta\s+name="framer-search-index"[^>]*>\s*',
        '',
        html
    )

    # Remove framer generator meta (replace with our own)
    html = re.sub(
        r'<meta\s+name="generator"\s+content="Framer[^"]*">\s*',
        '<meta name="generator" content="Astro">\n    ',
        html
    )

    return html


def remove_framer_preloads(html: str) -> str:
    """Remove modulepreload links for Framer JS chunks."""

    # Remove modulepreload links for .mjs files from framerusercontent
    html = re.sub(
        r'<link[^>]*rel="modulepreload"[^>]*href="https://framerusercontent\.com[^"]*\.mjs"[^>]*>\s*',
        '',
        html
    )

    return html


def remove_hydration_attributes(html: str) -> str:
    """Remove data-framer-hydrate-v2 and similar hydration attributes."""

    # Remove data-framer-hydrate-v2 (the main hydration trigger)
    html = re.sub(
        r'\s*data-framer-hydrate-v2?="[^"]*"',
        '',
        html
    )

    # Remove data-framer-ssr-released-at
    html = re.sub(
        r'\s*data-framer-ssr-released-at="[^"]*"',
        '',
        html
    )

    # Remove data-framer-page-optimized-at
    html = re.sub(
        r'\s*data-framer-page-optimized-at="[^"]*"',
        '',
        html
    )

    # Remove data-fid (Framer analytics ID)
    html = re.sub(
        r'\s*data-fid="[^"]*"',
        '',
        html
    )

    # Remove data-no-nt
    html = re.sub(
        r'\s*data-no-nt\b',
        '',
        html
    )

    return html


def clean_framer_comments(html: str) -> str:
    """Update or remove Framer-related comments."""

    # Update the "Built with Framer" comment
    html = re.sub(
        r'<!-- ✨ Built with Framer • https://www\.framer\.com/ -->',
        '<!-- Built with Astro - Originally exported from Framer -->',
        html
    )

    # Remove HTML comments that are just <!--$--> (React hydration markers)
    html = re.sub(r'<!--\$-->', '', html)
    html = re.sub(r'<!--/\$-->', '', html)

    return html


def fix_appear_animations(html: str) -> str:
    """
    Fix elements that were meant to animate in with JavaScript.
    Without the animation script, these elements have opacity:0.001 and are invisible.
    """

    # Fix inline style opacity:0.001 to opacity:1
    # This pattern matches style attributes containing opacity:0.001
    html = re.sub(
        r'(style="[^"]*?)opacity:0\.001;?',
        r'\1opacity:1;',
        html
    )

    # Remove transform offsets that were for animation (translateY(64px), translateY(-10px), etc.)
    # These transforms were meant to animate elements sliding in
    html = re.sub(
        r'(style="[^"]*?)transform:translateX\([^)]+\)\s*translateY\([^)]+\)\s*(scale\([^)]+\))?\s*(rotate\([^)]+\))?;?',
        r'\1',
        html
    )

    # Clean up will-change:transform since we're not animating
    html = re.sub(
        r'(style="[^"]*?)will-change:transform;?',
        r'\1',
        html
    )

    # Clean up any double semicolons or trailing semicolons before quote
    html = re.sub(r';{2,}', ';', html)
    html = re.sub(r';\s*"', '"', html)
    html = re.sub(r'style="\s*"', '', html)  # Remove empty style attributes

    return html


def process_html_file(filepath: Path) -> bool:
    """Process a single HTML file to remove Framer dependencies."""

    print(f"Processing: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    html = original

    # Apply all transformations
    html = remove_framer_scripts(html)
    html = remove_framer_meta_tags(html)
    html = remove_framer_preloads(html)
    html = remove_hydration_attributes(html)
    html = clean_framer_comments(html)
    html = fix_appear_animations(html)

    # Clean up multiple blank lines
    html = re.sub(r'\n{3,}', '\n\n', html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  -> Updated")
        return True
    else:
        print(f"  -> No changes needed")
        return False


def main():
    # Find all HTML files in src/pages
    pages_dir = Path(__file__).parent.parent / 'src' / 'pages'

    if not pages_dir.exists():
        print(f"Error: {pages_dir} does not exist")
        sys.exit(1)

    html_files = list(pages_dir.rglob('*.html'))

    if not html_files:
        print("No HTML files found")
        sys.exit(1)

    print(f"Found {len(html_files)} HTML files\n")

    modified_count = 0
    for filepath in sorted(html_files):
        if process_html_file(filepath):
            modified_count += 1

    print(f"\n{'='*50}")
    print(f"Done! Modified {modified_count} of {len(html_files)} files")


if __name__ == '__main__':
    main()
