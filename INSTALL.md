# Installation Guide

## Requirements

- No runtime dependencies. This is a static HTML/CSS/JS site.
- Optional, only if you want to regenerate pages from `generate.py`: **Python 3.8+** (no external packages required — the generator uses only the standard library).

## Running locally

### Option 1 — Open directly
Double-click `index.html`, or open it in a browser via `File > Open`. Nearly everything will work, but some browsers restrict certain features (like `fetch`) for `file://` pages, so Option 2 is recommended.

### Option 2 — Local static server (recommended)
```bash
cd noventrax
python3 -m http.server 8080
```
Then open `http://localhost:8080` in your browser.

Alternative servers that work equally well:
```bash
npx serve .
# or
php -S localhost:8080
```

## Regenerating the site from source data

The entire site is produced by `generate.py`. If you edit copy, add a service, add a team member, or add a portfolio project inside that file, regenerate the affected pages with:

```bash
python3 generate.py
```

This overwrites the `.html` files in place based on the data structures and templates defined in the script. Static assets (`css/`, `js/`, `assets/`) are not touched by the generator and can be edited directly.

## Fonts

The site loads Space Grotesk, Inter, and JetBrains Mono from Google Fonts via a `<link>` tag in every page's `<head>`. This requires an internet connection at runtime. If you need a fully offline build:

1. Download the three font families as `.woff2` files.
2. Add `@font-face` declarations at the top of `css/style.css` pointing to local files.
3. Remove the Google Fonts `<link>` tags from `generate.py`'s `head()` function (or from each HTML file directly) and regenerate.

## Browser support

Tested against current versions of Chrome, Edge, Firefox, and Safari on Windows, macOS, iOS, and Android. The site uses only widely supported CSS (Grid, custom properties, `backdrop-filter` with graceful degradation) and vanilla JS (`IntersectionObserver`, standard DOM APIs).
