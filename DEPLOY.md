# Deployment Guide

This site is a static bundle of HTML, CSS, JS, and SVG — it deploys to any static host with no build step.

## GitHub Pages

1. Push this folder's contents to the root of a GitHub repository (or a `docs/` folder, or a `gh-pages` branch).
2. In the repo settings, go to **Pages** and set the source to that branch/folder.
3. GitHub will publish at `https://<username>.github.io/<repo>/`.
4. To use a custom domain: add a `CNAME` file containing your domain (e.g. `www.noventrax.com`) to the repo root, and point your domain's DNS `A`/`CNAME` records at GitHub Pages per [GitHub's custom domain docs].

## Netlify

1. Drag-and-drop the project folder into the Netlify dashboard, **or** connect the GitHub repo.
2. Build command: *(leave blank — there is no build step)*.
3. Publish directory: `/` (repo root).
4. Add your custom domain under **Domain settings** and follow Netlify's DNS instructions.

## Vercel

1. Import the GitHub repository in the Vercel dashboard.
2. Framework preset: **Other** / static.
3. Build command: *(none)*. Output directory: `/`.
4. Add your custom domain under **Project Settings → Domains**.

## Any other static host (S3 + CloudFront, Cloudflare Pages, Firebase Hosting, etc.)

Upload the contents of this folder as-is. Ensure:
- `index.html` is set as the default document.
- `404.html` is configured as the custom error page for unmatched routes.
- HTTPS is enabled (all major static hosts provide this by default).

## Connecting a custom domain

1. Register/point your domain's DNS to your chosen host (see host-specific steps above).
2. Update `SITE_URL` in `generate.py` to your live domain, then run `python3 generate.py` to regenerate canonical URLs, Open Graph tags, and `sitemap.xml` with the correct domain.
3. Update the `Sitemap:` line in `robots.txt` to match.

## Post-deploy checklist

- [ ] Verify all internal links resolve (no broken navigation)
- [ ] Confirm `robots.txt` and `sitemap.xml` are reachable at the domain root
- [ ] Submit the sitemap to Google Search Console / Bing Webmaster Tools
- [ ] Run a Lighthouse audit against the live URL (not localhost) for accurate Performance/SEO scores
- [ ] Replace placeholder contact details, social links, and team bios with real information
- [ ] Wire the contact and consultation forms to a real backend or form service (see `.env.example`) — they currently validate client-side only and do not submit anywhere
