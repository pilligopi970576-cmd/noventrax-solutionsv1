# Noventrax Solutions — Corporate Website

A production-ready, dark-mode, fully responsive marketing website for **Noventrax Solutions**, a fictional enterprise software, AI, and cloud engineering company. Built with plain HTML, CSS, and vanilla JavaScript — no build step, no framework, no dependencies required to run it.

## ✨ What's included

- **30 pages**: Home, About, Services overview + 17 individual service pages, Technologies, Portfolio, Process, Industries, FAQ, Contact, Privacy Policy, Terms & Conditions, Cookie Policy, and a custom 404.
- **Design system**: CSS custom properties for color, type, radius, and spacing — see `css/style.css`.
- **Signature visual language**: an original "node lattice" motif (SVG) used in the logo, hero graphic, and background texture — representing systems, integration, and networks.
- **Interactions**: premium loading screen, scroll-reveal animations, 3D card tilt, cursor glow, animated tech marquee, FAQ accordion, mobile navigation, live-chat widget (placeholder), and client-side form validation — all in `js/main.js`, with `prefers-reduced-motion` respected throughout.
- **SEO**: per-page meta tags, Open Graph, Twitter Card, JSON-LD (`Organization` and `Service` schema), canonical URLs, `robots.txt`, and `sitemap.xml`.
- **Accessibility**: semantic HTML, skip-to-content link, visible focus states, keyboard-operable navigation and accordion, alt text and ARIA labels throughout.
- **Generator script**: `generate.py` — the entire site is produced from this single Python script, which makes future content edits (e.g. adding a service or team member) fast and consistent. You do not need to run it again unless you want to regenerate the site from the data structures inside it.

## 📁 Folder structure

```
noventrax/
├── index.html                     Home
├── about.html
├── services.html                  Services overview
├── service-*.html                 17 individual service pages
├── technologies.html
├── portfolio.html
├── process.html
├── industries.html
├── faq.html
├── contact.html
├── privacy.html
├── terms.html
├── cookies.html
├── 404.html
├── css/style.css                  Full design system
├── js/main.js                     All interactions
├── assets/icons/                  Logo, favicon, loader mark (SVG)
├── generate.py                    Site generator / content source of truth
├── robots.txt
├── sitemap.xml
├── .env.example                   Placeholder for future backend integration
├── INSTALL.md
├── DEPLOY.md
└── LICENSE
```

## 🚀 Quick start

This is a static site — there is nothing to build or compile.

```bash
# Option A: just open it
open index.html

# Option B: serve it locally (recommended, so relative paths behave like production)
python3 -m http.server 8080
# then visit http://localhost:8080
```

See `INSTALL.md` for more detail and `DEPLOY.md` for GitHub Pages / Netlify / Vercel deployment steps.

## 🎨 Editing content

All page content is generated from Python data structures at the top of `generate.py` (e.g. `SERVICES`, `TEAM`, `PROJECTS`, `INDUSTRIES`, `FAQS`). To change copy:

1. Edit the relevant list/dict in `generate.py`.
2. Run `python3 generate.py` to regenerate the affected HTML file(s).
3. Commit the updated `.html` files (the generator output **is** the deployed site — there's no separate build step in production).

If you'd rather hand-edit an individual HTML file directly going forward, that's fine too — just be aware future `generate.py` runs will overwrite hand-edits to that file.

## 🔧 Design tokens

All colors, type, radii, and spacing live as CSS custom properties at the top of `css/style.css`, so the whole visual identity can be re-themed from one place.

## 📄 License

See `LICENSE`. Placeholder company name, team members, testimonials, and contact details are fictional and provided as a content template — replace with real information before using this as an actual company site.
