# -*- coding: utf-8 -*-
"""
Noventrax Solutions — static site generator.
Produces every page of the site as plain HTML files sharing css/style.css
and js/main.js. Run: python3 generate.py
"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://noventraxsolutions.in"

# ---------------------------------------------------------------------------
# ICONS (small original line-icon set, hand-authored, 24x24 viewBox)
# ---------------------------------------------------------------------------
ICONS = {
  "code": '<path d="M8 5 2 12l6 7M16 5l6 7-6 7M13 3 11 21" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
  "enterprise": '<path d="M4 21V7l8-4 8 4v14M4 21h16M9 21v-6h6v6M9 11h.01M15 11h.01M9 7h.01M15 7h.01" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
  "globe": '<circle cx="12" cy="12" r="9" stroke-width="1.6"/><path d="M3 12h18M12 3c2.7 2.6 4 5.6 4 9s-1.3 6.4-4 9c-2.7-2.6-4-5.6-4-9s1.3-6.4 4-9Z" stroke-width="1.6"/>',
  "mobile": '<rect x="7" y="2" width="10" height="20" rx="2" stroke-width="1.6"/><path d="M11 18h2" stroke-width="1.6" stroke-linecap="round"/>',
  "brain": '<path d="M9 3a3 3 0 0 0-3 3v.3A3 3 0 0 0 4 9v1a3 3 0 0 0 1 2.2V14a3 3 0 0 0 3 3h1v2a2 2 0 0 0 4 0v-2h1a3 3 0 0 0 3-3v-1.8A3 3 0 0 0 18 10V9a3 3 0 0 0-2-2.8V6a3 3 0 0 0-3-3h-1v0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
  "layers": '<path d="m12 3 9 5-9 5-9-5 9-5Z" stroke-width="1.6" stroke-linejoin="round"/><path d="m3 14 9 5 9-5M3 10.5l9 5 9-5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
  "cloud": '<path d="M7 18a4.5 4.5 0 0 1-.6-8.96A5.5 5.5 0 0 1 17 8.5a4 4 0 0 1-.6 7.5H7Z" stroke-width="1.6" stroke-linejoin="round"/>',
  "shield": '<path d="M12 3 5 6v6c0 4.5 3 7.7 7 9 4-1.3 7-4.5 7-9V6l-7-3Z" stroke-width="1.6" stroke-linejoin="round"/><path d="m9.5 12 1.8 1.8 3.2-3.6" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
  "palette": '<circle cx="12" cy="12" r="9" stroke-width="1.6"/><circle cx="9" cy="10" r="1" fill="currentColor"/><circle cx="13" cy="8" r="1" fill="currentColor"/><circle cx="16" cy="11" r="1" fill="currentColor"/><path d="M12 21a9 9 0 0 1 0-18c1 0 2 .8 2 2s-1 1.4-1 2.5S14 9 15 9h1a4 4 0 0 1 4 4c0 4.4-3.6 8-8 8Z" stroke-width="1.6"/>',
  "check-shield": '<path d="M12 3 5 6v6c0 4.5 3 7.7 7 9 4-1.3 7-4.5 7-9V6l-7-3Z" stroke-width="1.6" stroke-linejoin="round"/>',
  "chart": '<path d="M4 20V10M11 20V4M18 20v-7" stroke-width="1.8" stroke-linecap="round"/><path d="M2 20h20" stroke-width="1.6" stroke-linecap="round"/>',
  "database": '<ellipse cx="12" cy="5.5" rx="8" ry="3" stroke-width="1.6"/><path d="M4 5.5V18c0 1.7 3.6 3 8 3s8-1.3 8-3V5.5" stroke-width="1.6"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" stroke-width="1.6"/>',
  "compass": '<circle cx="12" cy="12" r="9" stroke-width="1.6"/><path d="m15 9-2 6-6 2 2-6 6-2Z" stroke-width="1.6" stroke-linejoin="round"/>',
  "transform": '<path d="M4 7h11a3 3 0 0 1 3 3v1M20 17H9a3 3 0 0 1-3-3v-1" stroke-width="1.6" stroke-linecap="round"/><path d="m17 4 3 3-3 3M7 14l-3 3 3 3" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
  "plug": '<path d="M9 3v5M15 3v5M6 8h12l-1 4a5 5 0 0 1-5 4h0a5 5 0 0 1-5-4L6 8Z" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 16v5" stroke-width="1.6" stroke-linecap="round"/>',
  "stack": '<rect x="4" y="4" width="7" height="7" rx="1.2" stroke-width="1.6"/><rect x="13" y="4" width="7" height="7" rx="1.2" stroke-width="1.6"/><rect x="4" y="13" width="7" height="7" rx="1.2" stroke-width="1.6"/><rect x="13" y="13" width="7" height="7" rx="1.2" stroke-width="1.6"/>',
  "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 18l3 3 6.5-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2-2 2.6-2.6Z" stroke-width="1.6" stroke-linejoin="round"/>',
  "target": '<circle cx="12" cy="12" r="9" stroke-width="1.6"/><circle cx="12" cy="12" r="5" stroke-width="1.6"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/>',
  "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="12" r="3" stroke-width="1.6"/>',
  "arrow-right": '<path d="M4 12h16M13 5l7 7-7 7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
  "plus": '<path d="M12 5v14M5 12h14" stroke-width="1.8" stroke-linecap="round"/>',
  "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-8.9 8.4c-1.3 0-2.4-.2-3.5-.7L3 21l1.8-5.4A8.4 8.4 0 1 1 21 11.5Z" stroke-width="1.6" stroke-linejoin="round"/>',
  "close": '<path d="M6 6l12 12M18 6 6 18" stroke-width="1.8" stroke-linecap="round"/>',
  "menu": '<path d="M4 7h16M4 12h16M4 17h16" stroke-width="1.8" stroke-linecap="round"/>',
  "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3" stroke-width="1.4"/><path d="M7.5 10v6M7.5 7.5v.01M11.5 16v-3.6c0-1.4 1-2.4 2.2-2.4 1.2 0 1.8 1 1.8 2.4V16" stroke-width="1.4" stroke-linecap="round"/>',
  "github": '<path d="M12 2a10 10 0 0 0-3.2 19.5c.5.1.7-.2.7-.5v-1.8c-2.8.6-3.4-1.3-3.4-1.3-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.5 2.3 1.1 2.9.8.1-.7.4-1.1.6-1.4-2.2-.3-4.6-1.1-4.6-4.9 0-1.1.4-2 1-2.7-.1-.3-.5-1.3.1-2.7 0 0 .8-.3 2.7 1a9 9 0 0 1 4.9 0c1.9-1.3 2.7-1 2.7-1 .6 1.4.2 2.4.1 2.7.6.7 1 1.6 1 2.7 0 3.8-2.4 4.6-4.6 4.9.4.3.7.9.7 1.9v2.8c0 .3.2.6.7.5A10 10 0 0 0 12 2Z" stroke-width="1.2" stroke-linejoin="round"/>',
  "x-twitter": '<path d="m4 4 7.5 9.1L4.4 20H6.9l5.9-6.4L17.6 20H20l-8-9.7L19.2 4h-2.5l-5.4 5.9L6.4 4H4Z" stroke-width="0" fill="currentColor"/>',
  "facebook": '<path d="M14 9h3V6h-3c-1.7 0-3 1.3-3 3v2H9v3h2v6h3v-6h2.5l.5-3H14V9.5c0-.3.2-.5.5-.5Z" stroke-width="0" fill="currentColor"/>',
  "instagram": '<rect x="3" y="3" width="18" height="18" rx="5" stroke-width="1.4"/><circle cx="12" cy="12" r="3.6" stroke-width="1.4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor"/>',
  "youtube": '<rect x="2.5" y="5.5" width="19" height="13" rx="3" stroke-width="1.4"/><path d="m10.5 9.5 5 2.5-5 2.5v-5Z" fill="currentColor" stroke-width="0"/>',
}

def icon(name, cls=""):
    body = ICONS.get(name, ICONS["code"])
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="{cls}" aria-hidden="true">{body}</svg>'

def brand_mark():
    return """<svg viewBox="0 0 64 64" fill="none" aria-hidden="true">
      <defs>
        <linearGradient id="bmg" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
          <stop offset="0" stop-color="#c94456"/>
          <stop offset="1" stop-color="#7a1f2b"/>
        </linearGradient>
      </defs>
      <path d="M14 50V14L38 50V14" stroke="url(#bmg)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="14" cy="14" r="3.6" fill="#0b0d10" stroke="url(#bmg)" stroke-width="2.2"/>
      <circle cx="14" cy="50" r="3.6" fill="#0b0d10" stroke="url(#bmg)" stroke-width="2.2"/>
      <circle cx="38" cy="14" r="3.6" fill="#0b0d10" stroke="url(#bmg)" stroke-width="2.2"/>
      <circle cx="38" cy="50" r="3.6" fill="#0b0d10" stroke="url(#bmg)" stroke-width="2.2"/>
    </svg>"""

# ---------------------------------------------------------------------------
# NAV / FOOTER DATA
# ---------------------------------------------------------------------------
NAV_LINKS = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("technologies.html", "Technologies"),
    ("portfolio.html", "Portfolio"),
    ("process.html", "Process"),
    ("industries.html", "Industries"),
    ("faq.html", "FAQ"),
]

SOCIALS = [
    ("linkedin", "https://www.linkedin.com/company/noventrax-solutions"),
    ("github", "https://github.com/noventrax-solutions"),
    ("x-twitter", "https://x.com/noventrax"),
    ("facebook", "https://www.facebook.com/noventraxsolutions"),
    ("instagram", "https://www.instagram.com/noventrax.solutions"),
    ("youtube", "https://www.youtube.com/@noventraxsolutions"),
]

FOOTER_SERVICES = [
    ("service-custom-software-development.html", "Custom Software Development"),
    ("service-ai-solutions.html", "Artificial Intelligence Solutions"),
    ("service-cloud-solutions.html", "Cloud Solutions"),
    ("service-cybersecurity-services.html", "Cybersecurity Services"),
    ("service-data-analytics.html", "Data Analytics"),
    ("services.html", "View all services →"),
]

FOOTER_COMPANY = [
    ("about.html", "About Us"),
    ("process.html", "Our Process"),
    ("industries.html", "Industries"),
    ("portfolio.html", "Portfolio"),
    ("faq.html", "FAQ"),
    ("contact.html", "Contact"),
]

FOOTER_LEGAL = [
    ("privacy.html", "Privacy Policy"),
    ("terms.html", "Terms & Conditions"),
    ("cookies.html", "Cookie Policy"),
]

CONTACT_INFO = {
    "phone": "+91 93464 94520",
    "email": "info@noventraxsolutions.in",
    "address": "7-8 Bethsamane, Vijayawada, Andhra Pradesh 521227",
}

# ---------------------------------------------------------------------------
# SHARED TEMPLATE PIECES
# ---------------------------------------------------------------------------

def head(title, description, path, ld_json=None):
    canonical = f"{SITE_URL}/{path}"
    ld = ld_json or ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} | Noventrax Solutions</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#07080a">

<meta property="og:type" content="website">
<meta property="og:title" content="{title} | Noventrax Solutions">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Noventrax Solutions">
<meta property="og:image" content="{SITE_URL}/assets/icons/logo-mark.svg">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} | Noventrax Solutions">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE_URL}/assets/icons/logo-mark.svg">

<link rel="icon" type="image/svg+xml" href="assets/icons/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
{ld}
</head>
"""

def loader():
    return """
<div id="loader" aria-hidden="true">
  <svg class="mark" viewBox="0 0 64 64" fill="none">
    <path d="M14 50V14L38 50V14" stroke="#c94456" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</div>
<div class="lattice-bg"><svg></svg></div>
<div class="grain"></div>
"""

def header_nav(active):
    links = ""
    for href, label in NAV_LINKS:
        cls = " active" if href == active else ""
        links += f'<a href="{href}" class="{cls.strip()}">{label}</a>\n'
    return f"""
<a class="skip-link" href="#main">Skip to content</a>
<header class="site">
  <div class="container nav-row">
    <a href="index.html" class="brand">
      {brand_mark()}
      Noventrax<span style="color:var(--ember-glow)">.</span>
    </a>
    <nav class="primary" id="primary-nav">
      {links}
      <a href="contact.html" class="nav-cta">Start a Project</a>
    </nav>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="primary-nav">
      {icon("menu")}
    </button>
  </div>
</header>
"""

def chat_widget():
    return f"""
<button class="chat-launcher" aria-label="Open live chat" aria-expanded="false">
  {icon("chat")}
</button>
<div class="chat-panel" role="dialog" aria-label="Live chat">
  <div class="chat-head">
    <span class="chat-dot"></span>
    <div>
      <div style="color:var(--text-hi);font-size:.88rem;font-weight:600;">Noventrax Concierge</div>
      <div style="font-size:.75rem;color:var(--text-faint);">Typically replies in minutes</div>
    </div>
    <button class="chat-close" aria-label="Close chat" style="margin-left:auto;background:none;border:none;color:var(--text-mute);cursor:pointer;">{icon("close")}</button>
  </div>
  <div class="chat-body">
    <div class="chat-bubble">Hi 👋 — this is a placeholder concierge widget. Tell us about your project and a solutions engineer will reach out.</div>
  </div>
  <form class="chat-input-row" data-demo>
    <input type="text" placeholder="Type a message…" aria-label="Message">
    <button type="submit" aria-label="Send">{icon("arrow-right")}</button>
  </form>
</div>
"""

def footer():
    social_html = "".join(
        f'<a href="{url}" aria-label="{name.replace("-", " ").title()}" target="_blank" rel="noopener">{icon(name)}</a>'
        for name, url in SOCIALS
    )
    def col(items):
        return "".join(f'<a href="{href}">{label}</a>' for href, label in items)
    return f"""
<footer class="site">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <a href="index.html" class="brand" style="margin-bottom:16px;">{brand_mark()} Noventrax<span style="color:var(--ember-glow)">.</span></a>
        <p style="max-width:34ch;color:var(--text-mute);font-size:.92rem;">Engineering the systems the future runs on — for startups, enterprises, and governments worldwide.</p>
        <div class="social-row" style="margin-top:20px;">{social_html}</div>
      </div>
      <div class="footer-col"><h4>Services</h4>{col(FOOTER_SERVICES)}</div>
      <div class="footer-col"><h4>Company</h4>{col(FOOTER_COMPANY)}</div>
      <div class="footer-col">
        <h4>Contact</h4>
        <a href="tel:{CONTACT_INFO['phone'].replace(' ', '').replace('(', '').replace(')', '')}">{CONTACT_INFO['phone']}</a>
        <a href="mailto:{CONTACT_INFO['email']}">{CONTACT_INFO['email']}</a>
        <span style="display:block;color:var(--text-mute);font-size:.88rem;line-height:1.6;">{CONTACT_INFO['address']}</span>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 Noventrax Solutions, Inc. All rights reserved.</p>
      <div style="display:flex;gap:20px;flex-wrap:wrap;">
        {"".join(f'<a href="{href}" style="font-size:.82rem;color:var(--text-faint);">{label}</a>' for href, label in FOOTER_LEGAL)}
      </div>
    </div>
  </div>
</footer>
"""

def page(title, description, path, active, body, extra_head=""):
    doc = head(title, description, path, extra_head)
    doc += "<body>\n"
    doc += loader()
    doc += header_nav(active)
    doc += '<main id="main">\n'
    doc += body
    doc += "\n</main>\n"
    doc += footer()
    doc += chat_widget()
    doc += '<script src="js/main.js"></script>\n</body>\n</html>'
    return doc


def write(path, content):
    full = os.path.join(ROOT, path)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def section_head(eyebrow, title, desc="", center=False):
    cls = "section-head center" if center else "section-head"
    d = f'<p style="color:var(--text-mute)">{desc}</p>' if desc else ""
    return f"""<div class="{cls}">
      <span class="eyebrow">{eyebrow}</span>
      <h2>{title}</h2>
      {d}
    </div>"""


def breadcrumb(label):
    return f"""<div class="breadcrumbs"><a href="index.html">Home</a> / {label}</div>"""

# ---------------------------------------------------------------------------
# SERVICES DATA
# ---------------------------------------------------------------------------
SERVICES = [
  dict(slug="custom-software-development", name="Custom Software Development", icon="code",
    tagline="Software built around your workflow, not the other way around.",
    summary="We design and build bespoke applications from the ground up — replacing spreadsheets, brittle scripts, and off-the-shelf tools that no longer fit how your business actually runs.",
    capabilities=[
      "Requirements discovery and technical scoping with measurable success criteria",
      "Architecture design for maintainability, not just launch-day speed",
      "Full-stack build across web, service, and data layers",
      "Automated testing pipelines baked in from sprint one",
      "Documentation and knowledge transfer so the system outlives any one team",
    ],
    deliverables=["Working software in 2-week increments", "Source code with full ownership", "Architecture decision records", "CI/CD pipeline", "Runbook and handover docs"],
    tech=["Node.js","Python","Go","PostgreSQL","React","Kubernetes"]),

  dict(slug="enterprise-software-development", name="Enterprise Software Development", icon="enterprise",
    tagline="Systems that hold up under real organizational weight.",
    summary="For organizations running on legacy platforms or fragmented internal tools, we build enterprise-grade systems engineered for scale, governance, and long operational life spans.",
    capabilities=[
      "Legacy modernization and phased migration planning",
      "Role-based access, audit trails, and compliance-ready architecture",
      "Integration with ERP, HRIS, and financial systems already in place",
      "High-availability and disaster-recovery design",
      "Change management support for large user populations",
    ],
    deliverables=["Modernization roadmap", "Enterprise system with SSO/RBAC", "Integration layer", "Compliance documentation", "Training materials"],
    tech=["Java",".NET","SAP integration","Oracle","Azure","Terraform"]),

  dict(slug="web-development", name="Web Development", icon="globe",
    tagline="Fast, accessible, and built to convert.",
    summary="From marketing sites to complex web applications, we build performant, SEO-ready, accessible web experiences on modern frameworks that your team can extend for years.",
    capabilities=[
      "Marketing sites, portals, and web applications",
      "Core Web Vitals and Lighthouse-driven performance budgets",
      "WCAG-aligned accessible markup and interaction patterns",
      "Headless CMS and content-model design",
      "Progressive Web App capability where useful",
    ],
    deliverables=["Responsive website or web app", "CMS with editor training", "SEO and analytics setup", "Performance report", "Deployment pipeline"],
    tech=["React","Next.js","TypeScript","Tailwind","Vercel","Contentful"]),

  dict(slug="mobile-app-development", name="Mobile App Development", icon="mobile",
    tagline="Native-feeling apps for iOS, Android, and both at once.",
    summary="We design and build mobile applications that feel native, perform well on mid-range devices, and ship through both app stores without last-minute surprises.",
    capabilities=[
      "Native iOS (Swift) and Android (Kotlin) development",
      "Cross-platform builds with React Native where it fits the brief",
      "Offline-first data sync and push notification infrastructure",
      "App Store and Play Store submission and compliance review",
      "Analytics and crash reporting instrumentation",
    ],
    deliverables=["Published app on App Store / Play Store", "Source code and CI pipeline", "Design system for future features", "Crash and performance monitoring", "App Store optimization notes"],
    tech=["Swift","Kotlin","React Native","Firebase","GraphQL","Fastlane"]),

  dict(slug="ai-solutions", name="Artificial Intelligence Solutions", icon="brain",
    tagline="Applied AI that earns its place in production.",
    summary="We scope, build, and operate AI systems — from LLM-powered assistants to computer vision pipelines — with the evaluation, guardrails, and monitoring that production use actually requires.",
    capabilities=[
      "Use-case scoping and feasibility assessment before any build begins",
      "LLM application design: retrieval, agents, and tool orchestration",
      "Computer vision and document intelligence pipelines",
      "Evaluation harnesses and guardrails for reliability and safety",
      "Cost and latency optimization for production-scale inference",
    ],
    deliverables=["Feasibility and ROI assessment", "Production AI service or feature", "Evaluation suite and dashboards", "Monitoring and alerting", "Model/vendor comparison report"],
    tech=["Python","PyTorch","Vector databases","LangChain","AWS Bedrock","Kubernetes"]),

  dict(slug="machine-learning-solutions", name="Machine Learning Solutions", icon="chart",
    tagline="Models trained on your data, tuned for your metrics.",
    summary="We build custom machine learning systems for forecasting, classification, recommendation, and anomaly detection — engineered around the metric your business actually cares about.",
    capabilities=[
      "Data pipeline design and feature engineering",
      "Model selection, training, and hyperparameter tuning",
      "Rigorous offline evaluation before any production rollout",
      "MLOps: versioning, retraining triggers, and drift monitoring",
      "A/B testing frameworks for measuring real-world lift",
    ],
    deliverables=["Trained and validated model", "Feature pipeline", "MLOps deployment stack", "Drift and performance monitoring", "Model card and documentation"],
    tech=["Python","scikit-learn","TensorFlow","MLflow","Airflow","Snowflake"]),

  dict(slug="cloud-solutions", name="Cloud Solutions", icon="cloud",
    tagline="Infrastructure that scales without babysitting.",
    summary="We design, migrate, and operate cloud infrastructure across AWS, Azure, and GCP — built for cost efficiency, resilience, and the kind of scaling that doesn't page you at 3 a.m.",
    capabilities=[
      "Cloud architecture design and multi-cloud strategy",
      "Migration from on-premise or legacy hosting with minimal downtime",
      "Infrastructure as code for repeatable, auditable environments",
      "Autoscaling, load balancing, and cost governance",
      "Observability stack: logging, metrics, tracing, alerting",
    ],
    deliverables=["Cloud architecture blueprint", "Migrated production environment", "IaC repository", "Cost optimization report", "24/7 monitoring dashboard"],
    tech=["AWS","Azure","GCP","Terraform","Kubernetes","Datadog"]),

  dict(slug="cybersecurity-services", name="Cybersecurity Services", icon="shield",
    tagline="Security built in, not bolted on afterward.",
    summary="We assess, harden, and continuously monitor systems against real-world threats — combining penetration testing, secure architecture review, and compliance-aligned controls.",
    capabilities=[
      "Penetration testing and vulnerability assessment",
      "Secure architecture and code review",
      "Identity, access management, and zero-trust design",
      "Compliance alignment: SOC 2, ISO 27001, HIPAA, GDPR",
      "Incident response planning and tabletop exercises",
    ],
    deliverables=["Security assessment report", "Remediation roadmap", "Hardened infrastructure configuration", "Compliance readiness documentation", "Incident response runbook"],
    tech=["OWASP","Burp Suite","AWS GuardDuty","Vault","SIEM tooling","Wireshark"]),

  dict(slug="ui-ux-design", name="UI/UX Design", icon="palette",
    tagline="Interfaces people navigate without thinking about it.",
    summary="We research, prototype, and design interfaces grounded in how your users actually work — validated with real testing, not internal opinion, before a single line of production code is written.",
    capabilities=[
      "User research, interviews, and journey mapping",
      "Wireframing, prototyping, and usability testing",
      "Design systems built for consistency at scale",
      "Accessibility-first interaction and visual design",
      "Handoff-ready specs for engineering teams",
    ],
    deliverables=["User research findings", "Interactive prototype", "Complete design system", "Accessibility audit", "Developer-ready design specs"],
    tech=["Figma","Framer","Storybook","Maze","Zeroheight","After Effects"]),

  dict(slug="software-testing-qa", name="Software Testing & QA", icon="check-shield",
    tagline="Confidence before it ships, not after.",
    summary="We build test strategy and automation into the delivery pipeline itself — catching regressions before release rather than in a support ticket after it.",
    capabilities=[
      "Test strategy design across unit, integration, and end-to-end layers",
      "Automated regression suites integrated into CI/CD",
      "Performance, load, and stress testing",
      "Manual exploratory testing for edge cases automation misses",
      "Accessibility and cross-device compatibility testing",
    ],
    deliverables=["Test strategy document", "Automated test suite", "Performance test report", "Bug tracking and triage setup", "Release readiness checklist"],
    tech=["Playwright","Selenium","Cypress","JMeter","Jest","TestRail"]),

  dict(slug="data-analytics", name="Data Analytics", icon="chart",
    tagline="Dashboards people actually check every morning.",
    summary="We turn scattered operational data into dashboards and reporting your leadership team trusts enough to make decisions from — without a data team of their own.",
    capabilities=[
      "Data source audit and metric definition alignment",
      "ETL pipeline design for reliable, deduplicated reporting",
      "Executive and operational dashboard design",
      "Self-serve analytics enablement for non-technical teams",
      "Ongoing data quality monitoring and alerting",
    ],
    deliverables=["Metric definitions and data dictionary", "ETL pipeline", "Interactive dashboards", "Self-serve reporting layer", "Data quality monitoring"],
    tech=["dbt","Snowflake","Looker","Power BI","Airbyte","SQL"]),

  dict(slug="data-engineering", name="Data Engineering", icon="database",
    tagline="Pipelines that don't break the moment volume grows.",
    summary="We build the data infrastructure underneath analytics and AI — ingestion, transformation, and storage systems designed to hold up as data volume and complexity grow.",
    capabilities=[
      "Batch and streaming pipeline architecture",
      "Data warehouse and lakehouse design",
      "Schema governance and data contract enforcement",
      "Pipeline orchestration, retries, and failure alerting",
      "Cost-aware storage and compute tiering",
    ],
    deliverables=["Data platform architecture", "Production ingestion and transformation pipelines", "Data catalog", "Orchestration and monitoring setup", "Runbook for on-call handling"],
    tech=["Apache Kafka","Spark","Airflow","Snowflake","dbt","AWS Glue"]),

  dict(slug="it-consulting", name="IT Consulting", icon="compass",
    tagline="An outside read on decisions that are hard to see from inside.",
    summary="We provide independent technical assessment and strategic direction — vendor selection, architecture review, technology roadmaps — for teams that need clarity before committing budget.",
    capabilities=[
      "Technology stack and vendor evaluation",
      "Architecture and system health assessments",
      "IT roadmap and budget planning",
      "Build-vs-buy decision frameworks",
      "Technical due diligence for M&A and investment",
    ],
    deliverables=["Technical assessment report", "Vendor comparison matrix", "IT roadmap with cost estimates", "Risk register", "Executive presentation"],
    tech=["Enterprise architecture frameworks","ITIL","Cloud cost tooling","Gap analysis models"]),

  dict(slug="digital-transformation", name="Digital Transformation", icon="transform",
    tagline="Moving the whole organization onto systems that fit today's work.",
    summary="We help organizations replace manual processes and disconnected tools with integrated digital systems — planned around real adoption, not just a technology swap.",
    capabilities=[
      "Process mapping and digitization opportunity assessment",
      "Change management and staff enablement planning",
      "System integration across departments and vendors",
      "Phased rollout to manage organizational risk",
      "Post-launch adoption measurement",
    ],
    deliverables=["Transformation roadmap", "Integrated digital workflows", "Change management plan", "Training program", "Adoption metrics dashboard"],
    tech=["Workflow automation platforms","RPA","API middleware","Low-code tooling"]),

  dict(slug="api-development-integration", name="API Development & Integration", icon="plug",
    tagline="Systems that talk to each other without duct tape.",
    summary="We design, build, and document APIs — and connect the systems you already run — so data moves between platforms reliably instead of through manual exports and re-uploads.",
    capabilities=[
      "REST and GraphQL API design and versioning strategy",
      "Third-party integrations: payments, CRM, ERP, logistics",
      "Webhook and event-driven architecture",
      "API security: authentication, rate limiting, key management",
      "Developer documentation and SDK generation",
    ],
    deliverables=["Production API with versioned documentation", "Integration middleware", "API security review", "Rate limiting and monitoring setup", "Postman/OpenAPI collection"],
    tech=["REST","GraphQL","OpenAPI","Kong","Stripe/Twilio-class integrations","Node.js"]),

  dict(slug="saas-development", name="SaaS Development", icon="stack",
    tagline="Multi-tenant products built to scale from ten users to ten thousand.",
    summary="We build SaaS products end to end — multi-tenant architecture, billing, onboarding, and the operational tooling needed to run a subscription business, not just a working prototype.",
    capabilities=[
      "Multi-tenant architecture and data isolation strategy",
      "Subscription billing, metering, and plan management",
      "Self-serve onboarding and account administration",
      "Usage analytics and churn signal instrumentation",
      "Scalable infrastructure ready for usage spikes",
    ],
    deliverables=["Production multi-tenant SaaS application", "Billing and subscription system", "Admin and customer-facing dashboards", "Onboarding flow", "Usage analytics setup"],
    tech=["Node.js","PostgreSQL","Stripe Billing","Redis","Kubernetes","Auth0"]),

  dict(slug="maintenance-support", name="Maintenance & Support", icon="wrench",
    tagline="Systems that keep working after launch day.",
    summary="We keep production systems healthy long after the initial build — monitoring, patching, incident response, and steady incremental improvement under a predictable support agreement.",
    capabilities=[
      "Proactive monitoring and uptime management",
      "Security patching and dependency updates",
      "Bug triage and resolution under defined SLAs",
      "Incremental feature development and refactoring",
      "Regular health reports and roadmap check-ins",
    ],
    deliverables=["SLA-backed support agreement", "Monitoring and alerting setup", "Monthly health and performance report", "Patch and dependency update log", "Incident postmortems when needed"],
    tech=["Datadog","PagerDuty","Sentry","GitHub Actions","Renovate","Grafana"]),
]

SERVICES_BY_SLUG = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------------------
# SERVICE DETAIL PAGES
# ---------------------------------------------------------------------------
def build_service_page(s):
    slug = s["slug"]
    path = f"service-{slug}.html"
    others = [x for x in SERVICES if x["slug"] != slug][:3]
    ld = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "{html.escape(s['name'])}",
  "provider": {{"@type": "Organization", "name": "Noventrax Solutions", "url": "{SITE_URL}"}},
  "areaServed": "Worldwide",
  "description": "{html.escape(s['summary'])}"
}}
</script>"""
    body = f"""
<section class="page-hero container">
  {breadcrumb(f'<a href="services.html">Services</a> / {s["name"]}')}
  <div class="grid grid-2" style="align-items:center;gap:48px;">
    <div class="reveal">
      <span class="eyebrow">Service</span>
      <h1>{s['name']}</h1>
      <p class="lead" style="max-width:52ch;font-size:1.15rem;">{s['tagline']}</p>
      <p style="max-width:56ch;">{s['summary']}</p>
      <div class="hero-actions">
        <a href="contact.html" class="btn btn-primary">Talk to an engineer {icon('arrow-right')}</a>
        <a href="portfolio.html" class="btn btn-ghost">See related work</a>
      </div>
    </div>
    <div class="card tilt reveal" style="padding:36px;">
      <div class="icon-wrap" style="width:56px;height:56px;">{icon(s['icon'])}</div>
      <h3>What's included</h3>
      <ul style="padding-left:1.1em;color:var(--text);">
        {"".join(f"<li style='margin-bottom:.6em;'>{c}</li>" for c in s['capabilities'][:3])}
      </ul>
    </div>
  </div>
</section>

<section class="section container">
  {section_head("Capabilities", "How we approach " + s['name'].lower())}
  <div class="grid grid-2">
    {"".join(f'''<div class="card reveal">
      <div class="icon-wrap">{icon("check-shield")}</div>
      <p style="color:var(--text-hi);font-weight:500;">{c}</p>
    </div>''' for c in s['capabilities'])}
  </div>
</section>

<section class="section container" style="padding-top:0;">
  <div class="grid grid-2" style="gap:48px;">
    <div class="reveal">
      {section_head("Deliverables", "What you walk away with")}
      <ul style="padding-left:1.2em;">
        {"".join(f"<li style='margin-bottom:.6em;'>{d}</li>" for d in s['deliverables'])}
      </ul>
    </div>
    <div class="reveal">
      {section_head("Toolchain", "Representative technologies")}
      <div>{"".join(f'<span class="tag">{t}</span>' for t in s['tech'])}</div>
      <div class="divider"></div>
      <p style="color:var(--text-mute);font-size:.9rem;">Exact tooling is chosen per engagement based on your existing stack, team skills, and long-term maintenance plans — never picked to suit our preferences over yours.</p>
    </div>
  </div>
</section>

<section class="section container">
  {section_head("Explore more", "Related services", center=True)}
  <div class="grid grid-3">
    {"".join(f'''<a href="service-{o['slug']}.html" class="card reveal" style="display:block;">
      <div class="icon-wrap">{icon(o['icon'])}</div>
      <h3>{o['name']}</h3>
      <p style="font-size:.92rem;">{o['tagline']}</p>
    </a>''' for o in others)}
  </div>
</section>

<section class="section container">
  <div class="card" style="text-align:center;padding:56px 32px;">
    <h2>Ready to talk about {s['name'].lower()}?</h2>
    <p style="max-width:52ch;margin:0 auto 1.5em;">Tell us where things stand today. We'll respond with a scoped point of view — not a generic sales deck.</p>
    <a href="contact.html" class="btn btn-primary">Start a conversation {icon('arrow-right')}</a>
  </div>
</section>
"""
    write(path, page(s["name"], s["summary"][:155], path, "services.html", body, ld))


for s in SERVICES:
    build_service_page(s)

print(f"Generated {len(SERVICES)} service pages")

# ---------------------------------------------------------------------------
# SERVICES OVERVIEW PAGE
# ---------------------------------------------------------------------------
def build_services_index():
    path = "services.html"
    cards = "".join(f'''
    <a href="service-{s['slug']}.html" class="card tilt reveal" style="display:block;">
      <div class="icon-wrap">{icon(s['icon'])}</div>
      <h3>{s['name']}</h3>
      <p style="font-size:.92rem;">{s['tagline']}</p>
      <span style="color:var(--ember-glow);font-size:.85rem;font-family:var(--f-mono);display:inline-flex;align-items:center;gap:.4em;">Learn more {icon("arrow-right", "")}</span>
    </a>''' for s in SERVICES)

    body = f"""
<section class="page-hero container">
  {breadcrumb("Services")}
  <span class="eyebrow reveal">Full-spectrum delivery</span>
  <h1 class="reveal">Seventeen disciplines. One accountable team.</h1>
  <p class="lead reveal">From first line of code to the on-call rotation years later, Noventrax covers the full lifecycle of enterprise software — so you're not stitching together five vendors to get one system live.</p>
</section>

<section class="section container">
  <div class="grid grid-3">
    {cards}
  </div>
</section>

<section class="section container">
  <div class="card" style="text-align:center;padding:56px 32px;">
    <h2>Not sure which service you need?</h2>
    <p style="max-width:52ch;margin:0 auto 1.5em;">Most engagements start as a conversation, not a scope document. Tell us what's slowing you down and we'll map it to the right discipline.</p>
    <a href="contact.html" class="btn btn-primary">Book a consultation {icon('arrow-right')}</a>
  </div>
</section>
"""
    write(path, page("Services", "Seventeen enterprise software disciplines delivered by one accountable team — from custom development to AI, cloud, and cybersecurity.", path, "services.html", body))

build_services_index()
print("Generated services.html")

# ---------------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------------
def hero_visual():
    return """
<div class="firefly-hero" id="fireflyHero">
  <canvas id="fireflyCanvas" aria-hidden="true"></canvas>
  <div class="n-glyph" tabindex="0" aria-label="Noventrax">
    <svg viewBox="0 0 64 64" fill="none">
      <path d="M14 50V14L38 50V14" stroke="#f2f0ee" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
</div>
"""

def build_home():
    path = "index.html"

    service_teasers = SERVICES[:6]
    service_cards = "".join(f'''
    <a href="service-{s['slug']}.html" class="card tilt reveal" style="display:block;">
      <div class="icon-wrap">{icon(s['icon'])}</div>
      <h3>{s['name']}</h3>
      <p style="font-size:.92rem;">{s['tagline']}</p>
    </a>''' for s in service_teasers)

    tech_names = ["React","Node.js","Python","AWS","Kubernetes","PostgreSQL","TypeScript","Go",
                  "TensorFlow","Terraform","GraphQL","Azure","Docker","Snowflake","Kafka","Swift"]
    marquee = "".join(f"<span>{t}</span>" for t in tech_names)

    body = f"""
<section class="hero container">
  <div class="hero-copy reveal">
    <span class="eyebrow">Enterprise software · AI · Cloud · Security</span>
    <h1>Engineering the systems the future runs on.</h1>
    <p class="lead">Noventrax Solutions designs, builds, and operates the software backbone for startups, enterprises, and governments across 30+ countries — with the rigor of critical infrastructure and the speed of a product studio.</p>
    <div class="hero-actions">
      <a href="contact.html" class="btn btn-primary">Start a project {icon('arrow-right')}</a>
      <a href="portfolio.html" class="btn btn-ghost">View our work</a>
    </div>
    <div class="hero-stats">
      <div class="stat"><b>180+</b><span>Systems shipped</span></div>
      <div class="stat"><b>30+</b><span>Countries served</span></div>
      <div class="stat"><b>99.95%</b><span>Avg. platform uptime</span></div>
      <div class="stat"><b>11 yrs</b><span>In continuous operation</span></div>
    </div>
  </div>
  <div class="hero-visual reveal">{hero_visual()}</div>
</section>

<div class="marquee"><div class="marquee-track">{marquee}</div></div>

<section class="section container">
  {section_head("What we do", "One partner across the full software lifecycle", "Seventeen disciplines, coordinated by one team that stays accountable from architecture through years of production support.")}
  <div class="grid grid-3">
    {service_cards}
  </div>
  <div style="text-align:center;margin-top:40px;">
    <a href="services.html" class="btn btn-ghost">View all 17 services {icon('arrow-right')}</a>
  </div>
</section>

<section class="section container" style="padding-top:0;">
  <div class="grid grid-2" style="gap:56px;align-items:center;">
    <div class="reveal">
      {section_head("Why Noventrax", "Built like infrastructure, shipped like a product")}
      <p>Most software vendors optimize for one or the other. We treat reliability as a feature from day one — audited architecture, automated testing, and observability are part of the build, not an afterthought bolted on after an incident.</p>
      <ul style="padding-left:1.2em;">
        <li style="margin-bottom:.6em;">Senior engineers on every engagement — no bait-and-switch staffing</li>
        <li style="margin-bottom:.6em;">Fixed-scope or dedicated-team models, whichever fits your risk profile</li>
        <li style="margin-bottom:.6em;">Security and compliance considered from the first architecture diagram</li>
      </ul>
      <a href="about.html" class="btn btn-ghost" style="margin-top:1rem;">More about Noventrax {icon('arrow-right')}</a>
    </div>
    <div class="card reveal" style="padding:0;overflow:hidden;">
      <div style="padding:36px;">
        <div class="icon-wrap">{icon('target')}</div>
        <h3>Our commitment</h3>
        <p>Every engagement starts with a scoped point of view, not a generic proposal — and ends with documentation and ownership that's genuinely yours.</p>
      </div>
    </div>
  </div>
</section>

<section class="section container">
  {section_head("Process", "How an engagement actually runs", center=True)}
  <div class="process-line reveal" style="max-width:720px;margin:0 auto;">
    <div class="process-step" data-index="1"><h3>Discover</h3><p>We map the problem, constraints, and success metrics before proposing a single line of architecture.</p></div>
    <div class="process-step" data-index="2"><h3>Design</h3><p>Architecture, UX, and technical plan reviewed with your team before build begins.</p></div>
    <div class="process-step" data-index="3"><h3>Build</h3><p>Two-week iterations, shipped to a staging environment your team can see and test.</p></div>
    <div class="process-step" data-index="4"><h3>Operate</h3><p>Launch support, monitoring, and a clear path to long-term maintenance or internal handover.</p></div>
  </div>
  <div style="text-align:center;margin-top:40px;">
    <a href="process.html" class="btn btn-ghost">See our full process {icon('arrow-right')}</a>
  </div>
</section>

<section class="section container">
  {section_head("Industries", "Domain depth where it matters", center=True)}
  <div class="grid grid-4">
    <div class="card reveal"><span class="tag badge-industry">Healthcare</span><p style="font-size:.9rem;">HIPAA-aware systems for providers and health-tech platforms.</p></div>
    <div class="card reveal"><span class="tag badge-industry">Financial Services</span><p style="font-size:.9rem;">Core banking, payments, and risk systems built for auditability.</p></div>
    <div class="card reveal"><span class="tag badge-industry">Logistics</span><p style="font-size:.9rem;">Fleet, warehouse, and supply-chain platforms at global scale.</p></div>
    <div class="card reveal"><span class="tag badge-industry">Government</span><p style="font-size:.9rem;">Citizen-facing and internal systems built to public-sector standards.</p></div>
  </div>
  <div style="text-align:center;margin-top:40px;">
    <a href="industries.html" class="btn btn-ghost">See all industries {icon('arrow-right')}</a>
  </div>
</section>

<section class="section container">
  {section_head("Client voices", "In their words", center=True)}
  <div class="testimonial-empty reveal">
    {icon('chat')}
    <p>We're building this section out with the clients we're working with right now. Real testimonials will appear here soon — no filler quotes in the meantime.</p>
  </div>
</section>

<section class="section container">
  <div class="card" style="text-align:center;padding:64px 32px;background:linear-gradient(135deg, var(--glass-bg), rgba(122,31,43,.08));">
    <h2>Tell us what you're building.</h2>
    <p style="max-width:52ch;margin:0 auto 1.5em;">Thirty minutes with a senior engineer — not a salesperson — is usually enough to know if we're the right fit.</p>
    <a href="contact.html" class="btn btn-primary">Book a free consultation {icon('arrow-right')}</a>
  </div>
</section>
"""
    ld = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Noventrax Solutions",
  "url": "https://noventraxsolutions.in",
  "logo": "https://noventraxsolutions.in/assets/icons/logo-mark.svg",
  "sameAs": [
    "https://www.linkedin.com/company/noventrax-solutions",
    "https://github.com/noventrax-solutions",
    "https://x.com/noventrax"
  ],
  "description": "Enterprise software, AI, and cloud engineering partner serving startups, enterprises, and governments worldwide."
}
</script>"""
    write(path, page("Enterprise Software, AI & Cloud Engineering", "Noventrax Solutions designs, builds, and operates enterprise software, AI, and cloud systems for startups, enterprises, and governments worldwide.", path, "index.html", body, ld))

build_home()
print("Generated index.html")

# ---------------------------------------------------------------------------
# TEAM DATA + AVATAR GENERATOR
# ---------------------------------------------------------------------------
TEAM = [
  dict(name="Elena Marsh", role="Chief Executive Officer",
       bio="Elena spent a decade leading platform engineering at two enterprise SaaS companies before founding Noventrax in 2015. She still reviews architecture diagrams personally on every engagement over seven figures.",
       skills=["Enterprise Strategy","Systems Architecture","Client Governance"], seed="EM", hue=352),
  dict(name="Rajiv Nandan", role="Chief Technology Officer",
       bio="Rajiv leads technical direction across every active engagement, with a background in distributed systems at cloud infrastructure providers. He set the engineering standards Noventrax teams still build against today.",
       skills=["Distributed Systems","Cloud Architecture","Engineering Standards"], seed="RN", hue=8),
  dict(name="Amara Solis", role="VP of Artificial Intelligence",
       bio="Amara built and shipped applied-ML systems in fraud detection and logistics forecasting before joining Noventrax to lead the AI practice, with a focus on evaluation rigor over demo polish.",
       skills=["Applied ML","LLM Systems","Evaluation & Safety"], seed="AS", hue=350),
  dict(name="Devon Okafor", role="VP of Cloud & Security",
       bio="Devon has led infrastructure and security teams through three SOC 2 audits and one national-scale cloud migration, and now sets cloud and security architecture standards firm-wide.",
       skills=["Cloud Infrastructure","Security Architecture","Compliance"], seed="DO", hue=355),
  dict(name="Naomi Chen", role="VP of Design",
       bio="Naomi leads the design practice with a research-first approach, having previously run UX for two fintech products used by millions of daily active users.",
       skills=["Product Design","User Research","Design Systems"], seed="NC", hue=6),
  dict(name="Marcus Webb", role="VP of Client Delivery",
       bio="Marcus keeps every engagement on scope and on schedule, translating between client stakeholders and engineering teams so nothing gets lost in either direction.",
       skills=["Delivery Management","Stakeholder Alignment","Program Governance"], seed="MW", hue=354),
]

def avatar_svg(seed, hue):
    return f"""<svg viewBox="0 0 120 120" fill="none" role="img" aria-label="Portrait placeholder for {seed}">
      <defs>
        <linearGradient id="av-{seed}" x1="0" y1="0" x2="120" y2="120" gradientUnits="userSpaceOnUse">
          <stop offset="0" stop-color="hsl({hue} 45% 22%)"/>
          <stop offset="1" stop-color="hsl({hue} 60% 12%)"/>
        </linearGradient>
      </defs>
      <rect width="120" height="120" rx="20" fill="url(#av-{seed})"/>
      <circle cx="60" cy="48" r="20" fill="rgba(255,255,255,0.14)"/>
      <path d="M24 100c4-20 16-30 36-30s32 10 36 30" fill="rgba(255,255,255,0.14)"/>
      <text x="60" y="66" text-anchor="middle" font-family="Space Grotesk, sans-serif" font-size="22" fill="rgba(255,255,255,0.55)" font-weight="600" dy="30">{seed}</text>
    </svg>"""

# ---------------------------------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------------------------------
def build_about():
    path = "about.html"
    team_cards = "".join(f'''
    <div class="card reveal">
      <div style="width:64px;height:64px;border-radius:14px;overflow:hidden;margin-bottom:18px;">{avatar_svg(m['seed'], m['hue'])}</div>
      <h3>{m['name']}</h3>
      <p style="color:var(--ember-glow);font-size:.85rem;font-family:var(--f-mono);margin-bottom:12px;">{m['role']}</p>
      <p style="font-size:.92rem;">{m['bio']}</p>
      <div>{"".join(f'<span class="tag">{sk}</span>' for sk in m['skills'])}</div>
    </div>''' for m in TEAM)

    body = f"""
<section class="page-hero container">
  {breadcrumb("About")}
  <span class="eyebrow reveal">About Noventrax</span>
  <h1 class="reveal">A systems company that happens to write software.</h1>
  <p class="lead reveal">We started as a systems-integration consultancy for mid-sized manufacturers in 2015. Eleven years later, we're a full-spectrum engineering partner working with organizations on five continents — but the instinct that started the company hasn't changed: build things that keep working long after the invoice is paid.</p>
</section>

<section class="section container">
  <div class="grid grid-2" style="gap:56px;">
    <div class="card reveal">
      <div class="icon-wrap">{icon('target')}</div>
      <h3>Mission</h3>
      <p>To give ambitious organizations the software backbone they need to move faster than the market changes — engineered with the rigor of critical infrastructure and the speed of a product studio.</p>
    </div>
    <div class="card reveal">
      <div class="icon-wrap">{icon('eye')}</div>
      <h3>Vision</h3>
      <p>A world where every institution, from three-person startups to national governments, can operate on software as dependable as the systems that run power grids and payment networks.</p>
    </div>
  </div>
</section>

<section class="section container" style="padding-top:0;">
  <div class="grid grid-2" style="gap:56px;align-items:center;">
    <div class="reveal">
      {section_head("Our story", "From systems integration to full-stack partner")}
      <p>Noventrax was founded in San Francisco in 2015 by a small team of infrastructure engineers who kept getting pulled into projects other vendors had left half-finished — enterprise integrations, migrations, and platforms that worked in the demo but buckled under real usage.</p>
      <p>What started as a systems-integration consultancy grew, engagement by engagement, into a full-spectrum software partner: product design, custom development, AI, cloud infrastructure, and security under one accountable roof. Today, teams in San Francisco, Austin, and Amsterdam support clients across more than thirty countries, with the same founding principle intact — scope honestly, build for the long run, and stay accountable after launch day.</p>
    </div>
    <div class="card reveal tilt" style="padding:0;overflow:hidden;">
      <svg viewBox="0 0 400 300" style="width:100%;display:block;">
        <rect width="400" height="300" fill="#0b0d10"/>
        <g stroke="rgba(122,31,43,.4)" stroke-width="1">
          <line x1="40" y1="250" x2="360" y2="250"/>
          <line x1="80" y1="250" x2="80" y2="60"/>
          <line x1="160" y1="250" x2="160" y2="100"/>
          <line x1="240" y1="250" x2="240" y2="40"/>
          <line x1="320" y1="250" x2="320" y2="120"/>
        </g>
        <circle cx="80" cy="60" r="5" fill="#c94456"/>
        <circle cx="160" cy="100" r="5" fill="#c94456"/>
        <circle cx="240" cy="40" r="5" fill="#c94456"/>
        <circle cx="320" cy="120" r="5" fill="#c94456"/>
        <text x="200" y="280" text-anchor="middle" fill="#8b8d93" font-family="JetBrains Mono, monospace" font-size="12">2015 → 2026, growth by engagement</text>
      </svg>
    </div>
  </div>
</section>

<section class="section container">
  {section_head("Leadership", "The people who stay accountable for delivery", center=True)}
  <div class="grid grid-3">
    {team_cards}
  </div>
</section>

<section class="section container">
  <div class="card" style="text-align:center;padding:56px 32px;">
    <h2>Want to work with us?</h2>
    <p style="max-width:50ch;margin:0 auto 1.5em;">We're always glad to talk shop, even before there's a formal scope on the table.</p>
    <a href="contact.html" class="btn btn-primary">Get in touch {icon('arrow-right')}</a>
  </div>
</section>
"""
    write(path, page("About Us", "Noventrax Solutions is a full-spectrum enterprise software partner founded in 2015 — meet our story, mission, and leadership team.", path, "about.html", body))

build_about()
print("Generated about.html")

# ---------------------------------------------------------------------------
# TECHNOLOGIES PAGE
# ---------------------------------------------------------------------------
TECH_GROUPS = [
  ("Frontend", "code", ["React","Next.js","Vue","TypeScript","Tailwind CSS","Svelte"]),
  ("Backend", "layers", ["Node.js","Python","Go","Java",".NET","Ruby on Rails"]),
  ("Mobile", "mobile", ["Swift","Kotlin","React Native","Flutter"]),
  ("Data & AI", "brain", ["PyTorch","TensorFlow","LangChain","Vector databases","Apache Spark","dbt"]),
  ("Cloud & DevOps", "cloud", ["AWS","Azure","Google Cloud","Kubernetes","Terraform","Docker"]),
  ("Databases", "database", ["PostgreSQL","MongoDB","Redis","Snowflake","MySQL","Elasticsearch"]),
  ("Security", "shield", ["OWASP tooling","HashiCorp Vault","AWS GuardDuty","Okta","Auth0"]),
  ("Integrations", "plug", ["Stripe","Twilio","Salesforce","SAP","Workday","REST/GraphQL"]),
]

def build_technologies():
    path = "technologies.html"
    groups_html = "".join(f'''
    <div class="card reveal">
      <div class="icon-wrap">{icon(gicon)}</div>
      <h3>{gname}</h3>
      <div>{"".join(f'<span class="tag">{t}</span>' for t in items)}</div>
    </div>''' for gname, gicon, items in TECH_GROUPS)

    body = f"""
<section class="page-hero container">
  {breadcrumb("Technologies")}
  <span class="eyebrow reveal">Toolchain</span>
  <h1 class="reveal">Technology chosen for the problem, not the trend.</h1>
  <p class="lead reveal">We stay deliberately polyglot. Every engagement gets a stack chosen for your team's skills, your scale, and a ten-year maintenance horizon — not whatever happens to be newest this quarter.</p>
</section>

<section class="section container">
  <div class="grid grid-3">
    {groups_html}
  </div>
</section>

<section class="section container" style="padding-top:0;">
  {section_head("How we choose", "Three questions before any technology gets picked")}
  <div class="grid grid-3">
    <div class="card reveal"><div class="icon-wrap">{icon('wrench')}</div><h3>Can your team maintain it?</h3><p style="font-size:.92rem;">We won't hand back a system built on tools nobody on your team can operate.</p></div>
    <div class="card reveal"><div class="icon-wrap">{icon('chart')}</div><h3>Does it fit the scale?</h3><p style="font-size:.92rem;">We size infrastructure to actual load, not hypothetical hockey-stick growth.</p></div>
    <div class="card reveal"><div class="icon-wrap">{icon('shield')}</div><h3>Is it still supported in five years?</h3><p style="font-size:.92rem;">We avoid dead-end frameworks and vendor lock-in you can't unwind later.</p></div>
  </div>
</section>

<section class="section container">
  <div class="card" style="text-align:center;padding:56px 32px;">
    <h2>Have a stack already in place?</h2>
    <p style="max-width:52ch;margin:0 auto 1.5em;">We're comfortable extending an existing codebase, not just starting from a blank repository.</p>
    <a href="contact.html" class="btn btn-primary">Discuss your stack {icon('arrow-right')}</a>
  </div>
</section>
"""
    write(path, page("Technologies", "The frontend, backend, cloud, data, AI, and security technologies Noventrax Solutions uses to build enterprise software.", path, "technologies.html", body))

build_technologies()
print("Generated technologies.html")

# ---------------------------------------------------------------------------
# PORTFOLIO PAGE
# ---------------------------------------------------------------------------
PROJECTS = [
  dict(name="Meridian Health OS", industry="Healthcare", icon="check-shield",
       overview="A unified patient-record and scheduling platform built for a 40-clinic regional healthcare network, replacing six disconnected legacy systems.",
       tech=["React","Node.js","PostgreSQL","HL7/FHIR"],
       impact="Cut average patient check-in time from 11 minutes to 3, and eliminated duplicate-record errors across clinics."),
  dict(name="Ledgerline ERP", industry="Manufacturing", icon="enterprise",
       overview="A custom ERP core for a mid-sized industrial manufacturer, unifying inventory, procurement, and production scheduling.",
       tech=["Java","Oracle","Kafka","Power BI"],
       impact="Reduced inventory discrepancies by 74% and cut monthly close time from 9 days to 2."),
  dict(name="Cursive CRM", industry="Professional Services", icon="stack",
       overview="A vertical CRM purpose-built for multi-office law firms, with matter tracking, billing, and compliance workflows baked in.",
       tech=["TypeScript","PostgreSQL","Redis","Stripe Billing"],
       impact="Adopted by 1,200+ daily active users across 60 firms within the first year of launch."),
  dict(name="Northgate Hospital Management", industry="Healthcare", icon="database",
       overview="An integrated hospital management system covering admissions, bed management, pharmacy, and billing for a public hospital group.",
       tech=[".NET","SQL Server","Azure","HL7"],
       impact="Brought bed-occupancy visibility from a manual whiteboard process to real-time dashboards across 5 hospitals."),
  dict(name="Ferrovia Core Banking", industry="Financial Services", icon="shield",
       overview="A modernized core banking layer for a regional bank migrating off a 20-year-old mainframe system.",
       tech=["Java","Kubernetes","PostgreSQL","Vault"],
       impact="Completed a phased migration with zero unplanned downtime across 400,000 customer accounts."),
  dict(name="Waypoint Logistics Platform", industry="Logistics", icon="globe",
       overview="A fleet routing and warehouse management platform for a cross-border freight operator serving 14 countries.",
       tech=["Go","React","PostgreSQL","AWS"],
       impact="Reduced average delivery routing time by 31% and cut fuel costs by an estimated 12%."),
  dict(name="Cartwell Commerce", industry="Retail", icon="layers",
       overview="A headless e-commerce platform for a multi-brand retail group, unifying inventory across 200+ storefronts.",
       tech=["Next.js","GraphQL","Shopify Plus","Snowflake"],
       impact="Supported a Black Friday traffic spike of 18x baseline with zero downtime."),
  dict(name="Solace SaaS Suite", industry="B2B SaaS", icon="stack",
       overview="A multi-tenant workforce-scheduling SaaS product built from zero to first paying customer in five months.",
       tech=["Node.js","PostgreSQL","Stripe Billing","Kubernetes"],
       impact="Scaled from 3 to 4,000 tenant organizations within eighteen months of launch."),
  dict(name="Aegis Mobile Banking", industry="Financial Services", icon="mobile",
       overview="A consumer mobile banking app with biometric authentication and real-time fraud alerts for a digital-first bank.",
       tech=["Swift","Kotlin","AWS","GraphQL"],
       impact="Reached a 4.8-star average rating across both app stores within the first quarter."),
  dict(name="Civica Permitting Portal", industry="Government", icon="enterprise",
       overview="A citizen-facing permitting and licensing portal for a metropolitan government, replacing an in-person-only process.",
       tech=["React","Node.js","PostgreSQL","Azure Gov"],
       impact="Moved 82% of permit applications online within the first year, cutting average approval time by half."),
]

def build_portfolio():
    path = "portfolio.html"
    cards = "".join(f'''
    <div class="card reveal">
      <span class="tag badge-industry">{p['industry']}</span>
      <h3 style="margin-top:14px;">{p['name']}</h3>
      <p style="font-size:.92rem;">{p['overview']}</p>
      <div style="margin-bottom:14px;">{"".join(f'<span class="tag">{t}</span>' for t in p['tech'])}</div>
      <p style="font-size:.88rem;color:var(--text-hi);border-top:1px solid var(--line);padding-top:14px;"><strong style="color:var(--ember-glow);">Impact — </strong>{p['impact']}</p>
    </div>''' for p in PROJECTS)

    body = f"""
<section class="page-hero container">
  {breadcrumb("Portfolio")}
  <span class="eyebrow reveal">Selected work</span>
  <h1 class="reveal">Ten systems, ten different kinds of pressure.</h1>
  <p class="lead reveal">Representative engagements across healthcare, banking, logistics, government, and SaaS — each built to hold up under the specific load its industry puts on software.</p>
</section>

<section class="section container">
  <div class="grid grid-3">
    {cards}
  </div>
</section>

<section class="section container">
  <div class="card" style="text-align:center;padding:56px 32px;">
    <h2>Want a similar system for your team?</h2>
    <p style="max-width:52ch;margin:0 auto 1.5em;">Tell us about your industry and constraints — we'll point to the closest relevant experience.</p>
    <a href="contact.html" class="btn btn-primary">Start the conversation {icon('arrow-right')}</a>
  </div>
</section>
"""
    write(path, page("Portfolio", "Representative Noventrax Solutions projects across healthcare, banking, logistics, government, and SaaS.", path, "portfolio.html", body))

build_portfolio()
print("Generated portfolio.html")

# ---------------------------------------------------------------------------
# PROCESS PAGE
# ---------------------------------------------------------------------------
PROCESS_STEPS = [
  ("Discover", "target", "We start with your problem, not our solution. Stakeholder interviews, current-state review, and constraint-mapping produce a written scope with measurable success criteria before any design work begins.", ["Stakeholder interviews","Current-system audit","Success metrics defined","Risk and constraint log"]),
  ("Design", "palette", "Architecture, data model, and UX are designed together and reviewed with your team before a single line of production code is written — so surprises surface on a whiteboard, not in a sprint retro.", ["System architecture diagram","UX prototypes and testing","Technical design review","Fixed-scope or T&M agreement"]),
  ("Build", "code", "Work ships in two-week increments to a staging environment your team can see and use throughout. Automated testing and code review are part of every merge, not a phase at the end.", ["Two-week delivery cycles","Continuous staging deploys","Automated test coverage","Weekly progress demos"]),
  ("Test", "check-shield", "Before anything reaches production, it goes through structured QA — functional, performance, security, and accessibility — with issues triaged and fixed inside the same sprint where possible.", ["Functional & regression testing","Load and performance testing","Security review","Accessibility audit"]),
  ("Launch", "cloud", "We plan the rollout around your organization's risk tolerance — phased, canary, or full cutover — with a rollback plan defined before go-live, not improvised during it.", ["Rollout plan and rollback plan","Production monitoring live", "Team training and documentation","Go-live support window"]),
  ("Operate", "wrench", "Most engagements continue into a support relationship: monitoring, patching, incremental features, and a monthly check-in — or a clean handover if you're bringing it in-house.", ["SLA-backed support option","Monthly health reports","Incremental roadmap", "Full internal handover path"]),
]

def build_process():
    path = "process.html"
    steps_html = "".join(f'''
    <div class="process-step reveal" data-index="{i+1}">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
        <div class="icon-wrap" style="margin-bottom:0;width:36px;height:36px;">{icon(pi)}</div>
        <h3 style="margin:0;">{name}</h3>
      </div>
      <p>{desc}</p>
      <div>{"".join(f'<span class="tag">{d}</span>' for d in deliv)}</div>
    </div>''' for i, (name, pi, desc, deliv) in enumerate(PROCESS_STEPS))

    body = f"""
<section class="page-hero container">
  {breadcrumb("Our Process")}
  <span class="eyebrow reveal">How we work</span>
  <h1 class="reveal">A six-stage process, run the same way every time.</h1>
  <p class="lead reveal">No two engagements look identical, but every one moves through the same six stages — so you always know what happens next and why.</p>
</section>

<section class="section container">
  <div class="process-line">
    {steps_html}
  </div>
</section>

<section class="section container" style="padding-top:0;">
  {section_head("Engagement models", "Two ways to work with us", center=True)}
  <div class="grid grid-2">
    <div class="card reveal">
      <div class="icon-wrap">{icon('target')}</div>
      <h3>Fixed-scope project</h3>
      <p>Defined deliverables, timeline, and price — best when requirements are well understood and change is expected to be limited.</p>
    </div>
    <div class="card reveal">
      <div class="icon-wrap">{icon('layers')}</div>
      <h3>Dedicated team</h3>
      <p>A senior team embedded with your organization on a rolling basis — best for ongoing product development or evolving priorities.</p>
    </div>
  </div>
</section>

<section class="section container">
  <div class="card" style="text-align:center;padding:56px 32px;">
    <h2>Ready to see this in motion?</h2>
    <p style="max-width:52ch;margin:0 auto 1.5em;">The first stage — Discover — starts with a single conversation, no commitment attached.</p>
    <a href="contact.html" class="btn btn-primary">Book a discovery call {icon('arrow-right')}</a>
  </div>
</section>
"""
    write(path, page("Our Process", "The six-stage delivery process Noventrax Solutions uses on every engagement, from discovery through long-term operation.", path, "process.html", body))

build_process()
print("Generated process.html")

# ---------------------------------------------------------------------------
# INDUSTRIES PAGE
# ---------------------------------------------------------------------------
INDUSTRIES = [
  ("Healthcare", "check-shield", "HIPAA-aware platforms for providers, payers, and health-tech products — from patient records to clinical scheduling.", ["EHR/EMR systems","Patient portals","Clinical scheduling","Telehealth platforms"]),
  ("Financial Services", "shield", "Core banking, payments, and risk systems built for auditability, and engineered to survive regulatory scrutiny.", ["Core banking modernization","Payments infrastructure","Risk & compliance tooling","Fraud detection"]),
  ("Manufacturing", "enterprise", "ERP, inventory, and production-floor systems that connect the shop floor to the front office in real time.", ["ERP systems","Inventory & procurement","Production scheduling","IoT/SCADA integration"]),
  ("Logistics & Supply Chain", "globe", "Routing, fleet, and warehouse platforms engineered for the operational pressure of real-time global logistics.", ["Fleet management","Warehouse management","Route optimization","Freight visibility platforms"]),
  ("Retail & E-commerce", "layers", "Headless commerce and inventory systems built to handle traffic spikes without falling over.", ["Headless commerce","Inventory unification","Loyalty platforms","POS integration"]),
  ("Government & Public Sector", "target", "Citizen-facing and internal systems built to public-sector procurement, security, and accessibility standards.", ["Citizen service portals","Permitting & licensing","Case management","Accessibility-compliant systems"]),
  ("SaaS & Technology", "stack", "Multi-tenant product architecture, billing, and scaling infrastructure for software companies at every stage.", ["Multi-tenant SaaS builds","Billing & subscription systems","Platform scaling","Developer APIs"]),
  ("Professional Services", "compass", "Vertical CRM, billing, and workflow systems purpose-built for law firms, agencies, and consultancies.", ["Vertical CRM","Matter/project tracking","Time & billing systems","Client portals"]),
]

def build_industries():
    path = "industries.html"
    cards = "".join(f'''
    <div class="card reveal">
      <div class="icon-wrap">{icon(ic)}</div>
      <h3>{name}</h3>
      <p style="font-size:.92rem;">{desc}</p>
      <div>{"".join(f'<span class="tag">{u}</span>' for u in uses)}</div>
    </div>''' for name, ic, desc, uses in INDUSTRIES)

    body = f"""
<section class="page-hero container">
  {breadcrumb("Industries")}
  <span class="eyebrow reveal">Domain depth</span>
  <h1 class="reveal">Software that respects the industry it runs in.</h1>
  <p class="lead reveal">Regulatory pressure, data sensitivity, and operational risk look different in a hospital than in a warehouse. We build with that context from the first architecture conversation.</p>
</section>

<section class="section container">
  <div class="grid grid-3">
    {cards}
  </div>
</section>

<section class="section container">
  <div class="card" style="text-align:center;padding:56px 32px;">
    <h2>Don't see your industry?</h2>
    <p style="max-width:52ch;margin:0 auto 1.5em;">Most of what matters — compliance, integration, scale — transfers across sectors. Tell us more about your context.</p>
    <a href="contact.html" class="btn btn-primary">Tell us about your industry {icon('arrow-right')}</a>
  </div>
</section>
"""
    write(path, page("Industries", "The healthcare, financial services, manufacturing, logistics, retail, government, and SaaS industries Noventrax Solutions serves.", path, "industries.html", body))

build_industries()
print("Generated industries.html")

# ---------------------------------------------------------------------------
# FAQ PAGE
# ---------------------------------------------------------------------------
FAQS = [
  ("How long does a typical engagement take?", "It depends heavily on scope. A focused MVP build usually runs 8-14 weeks; a full enterprise platform replacement can run 6-12 months. We give you a specific estimate after the Discover stage, not before."),
  ("Do you work with startups, or only large enterprises?", "Both, and everything in between — the process just flexes. Startups often start with a fixed-scope MVP; enterprises more often start with a dedicated team and a phased roadmap."),
  ("Who owns the code and IP once the project is done?", "You do, in full. Source code, documentation, and design assets transfer to you at project close under a standard IP assignment in every contract."),
  ("Can you work with our existing engineering team?", "Yes — many engagements are hybrid, with our team embedded alongside yours rather than fully separate. We adapt to your existing tools and workflows rather than requiring you to adopt ours."),
  ("What happens after launch?", "Most clients move into a Maintenance & Support agreement — monitoring, patching, and incremental improvements under an SLA. Others prefer a full internal handover, which we document thoroughly to support."),
  ("How do you handle security and compliance?", "Security review is part of the Design and Test stages on every engagement, not an optional add-on. For regulated industries (healthcare, finance, government) we scope compliance requirements — HIPAA, SOC 2, GDPR — from day one."),
  ("Do you sign NDAs before scoping calls?", "Yes, as a matter of course. We're glad to sign your standard NDA, or provide ours, before any detailed discussion of your systems or data."),
  ("What does pricing typically look like?", "Fixed-scope projects are quoted after Discover, based on defined deliverables. Dedicated-team engagements are billed on a monthly retainer per engineer. We'll walk you through both models on your first call."),
  ("Can you take over a project another vendor started?", "Regularly. We start with a technical audit of the existing codebase before committing to a plan — sometimes that means continuing the existing architecture, sometimes it means a partial rebuild."),
  ("Do you offer ongoing support outside business hours?", "Yes, SLA-backed support plans include defined response times for critical incidents outside standard hours. Exact coverage windows are set per contract based on your operational needs."),
]

def build_faq():
    path = "faq.html"
    items = "".join(f'''
    <div class="faq-item">
      <button class="faq-q" aria-expanded="false">{q}{icon('plus')}</button>
      <div class="faq-a"><p>{a}</p></div>
    </div>''' for q, a in FAQS)

    body = f"""
<section class="page-hero container">
  {breadcrumb("FAQ")}
  <span class="eyebrow reveal">Frequently asked</span>
  <h1 class="reveal">Questions we hear on almost every first call.</h1>
  <p class="lead reveal">If yours isn't answered here, it's a good excuse to reach out directly.</p>
</section>

<section class="section container" style="padding-top:0;max-width:820px;">
  <div class="faq-list reveal">
    {items}
  </div>
</section>

<section class="section container">
  <div class="card" style="text-align:center;padding:56px 32px;">
    <h2>Still have questions?</h2>
    <p style="max-width:52ch;margin:0 auto 1.5em;">A short call is usually faster than an email thread — and there's no obligation attached.</p>
    <a href="contact.html" class="btn btn-primary">Ask us directly {icon('arrow-right')}</a>
  </div>
</section>
"""
    write(path, page("FAQ", "Answers to the most common questions about working with Noventrax Solutions — pricing, timelines, IP ownership, and support.", path, "faq.html", body))

build_faq()
print("Generated faq.html")

# ---------------------------------------------------------------------------
# CONTACT PAGE
# ---------------------------------------------------------------------------
def build_contact():
    path = "contact.html"
    service_options = "".join(f'<option value="{s["slug"]}">{s["name"]}</option>' for s in SERVICES)

    body = f"""
<section class="page-hero container">
  {breadcrumb("Contact")}
  <span class="eyebrow reveal">Get in touch</span>
  <h1 class="reveal">Let's talk about what you're building.</h1>
  <p class="lead reveal">Reach out directly, or fill in a project brief below — both go to the same team, and both get a real reply, not an autoresponder.</p>
</section>

<section class="section container" style="padding-top:0;">
  <div class="grid grid-3" style="margin-bottom:56px;">
    <div class="card reveal">
      <div class="icon-wrap">{icon('chat')}</div>
      <h3>Phone</h3>
      <p><a href="tel:{CONTACT_INFO['phone'].replace(' ', '').replace('(', '').replace(')', '')}" style="color:var(--text-hi);">{CONTACT_INFO['phone']}</a></p>
      <p style="font-size:.85rem;color:var(--text-mute);">Mon–Fri, 8am–6pm PT</p>
    </div>
    <div class="card reveal">
      <div class="icon-wrap">{icon('plug')}</div>
      <h3>Email</h3>
      <p><a href="mailto:{CONTACT_INFO['email']}" style="color:var(--text-hi);">{CONTACT_INFO['email']}</a></p>
      <p style="font-size:.85rem;color:var(--text-mute);">Replies within one business day</p>
    </div>
    <div class="card reveal">
      <div class="icon-wrap">{icon('globe')}</div>
      <h3>Office</h3>
      <p style="color:var(--text-hi);">{CONTACT_INFO['address']}</p>
      <p style="font-size:.85rem;color:var(--text-mute);">Additional teams in Austin & Amsterdam</p>
    </div>
  </div>

  <div class="grid grid-2" style="gap:40px;align-items:start;">
    <div class="card reveal">
      <h3>General inquiry</h3>
      <p style="font-size:.9rem;">Questions about services, careers-adjacent partnerships, or anything else.</p>
      <div class="form-success">Thanks — your message has been received. We'll be in touch shortly.</div>
      <form data-validate novalidate>
        <div class="form-field">
          <label for="c-name">Full name</label>
          <input id="c-name" name="name" type="text" required>
          <span class="field-error">Please enter your name.</span>
        </div>
        <div class="form-field">
          <label for="c-email">Email</label>
          <input id="c-email" name="email" type="email" required>
          <span class="field-error">Please enter a valid email address.</span>
        </div>
        <div class="form-field">
          <label for="c-subject">Subject</label>
          <input id="c-subject" name="subject" type="text" required>
          <span class="field-error">Please enter a subject.</span>
        </div>
        <div class="form-field">
          <label for="c-message">Message</label>
          <textarea id="c-message" name="message" required></textarea>
          <span class="field-error">Please enter a message.</span>
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center;">Send message</button>
        <p class="form-note">This is a placeholder form for demonstration; no data is transmitted to a live backend.</p>
      </form>
    </div>

    <div class="card reveal">
      <h3>Book a consultation</h3>
      <p style="font-size:.9rem;">Tell us about your project and preferred service area — we'll follow up to schedule a call.</p>
      <div class="form-success">Thanks — your consultation request has been received. We'll follow up to schedule a time.</div>
      <form data-validate novalidate>
        <div class="form-field">
          <label for="q-name">Full name</label>
          <input id="q-name" name="name" type="text" required>
          <span class="field-error">Please enter your name.</span>
        </div>
        <div class="form-field">
          <label for="q-company">Company</label>
          <input id="q-company" name="company" type="text" required>
          <span class="field-error">Please enter your company name.</span>
        </div>
        <div class="form-field">
          <label for="q-email">Work email</label>
          <input id="q-email" name="email" type="email" required>
          <span class="field-error">Please enter a valid email address.</span>
        </div>
        <div class="form-field">
          <label for="q-service">Service of interest</label>
          <select id="q-service" name="service">
            {service_options}
          </select>
        </div>
        <div class="form-field">
          <label for="q-brief">Project brief</label>
          <textarea id="q-brief" name="brief" required></textarea>
          <span class="field-error">Please share a few details about your project.</span>
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center;">Request consultation</button>
        <p class="form-note">This is a placeholder form for demonstration; no data is transmitted to a live backend.</p>
      </form>
    </div>
  </div>
</section>
"""
    write(path, page("Contact", "Get in touch with Noventrax Solutions — general inquiries, project briefs, and consultation requests.", path, "contact.html", body))

build_contact()
print("Generated contact.html")

# ---------------------------------------------------------------------------
# LEGAL PAGES
# ---------------------------------------------------------------------------
def legal_page(path, title, active, intro, sections):
    body_sections = "".join(f"<h2>{h}</h2>{p}" for h, p in sections)
    body = f"""
<section class="page-hero container">
  {breadcrumb(title)}
  <span class="eyebrow">Legal</span>
  <h1>{title}</h1>
  <p class="lead" style="max-width:60ch;">{intro}</p>
</section>
<section class="section container legal-content" style="max-width:820px;padding-top:0;">
  <p style="color:var(--text-faint);font-family:var(--f-mono);font-size:.85rem;">Last updated: July 1, 2026</p>
  {body_sections}
</section>
"""
    write(path, page(title, intro[:155], path, active, body))

def build_privacy():
    sections = [
      ("Information We Collect", "<p>We collect information you provide directly — such as your name, email address, company, and project details submitted through our contact and consultation forms — along with standard technical data like IP address, browser type, and pages visited, collected via cookies and analytics tools.</p>"),
      ("How We Use Information", "<p>We use collected information to respond to inquiries, deliver requested services, improve our website and offerings, and comply with legal obligations. We do not sell personal information to third parties.</p>"),
      ("Data Sharing", "<p>We may share information with service providers who support our operations (such as hosting and analytics providers) under confidentiality obligations, or when required by law.</p>"),
      ("Data Retention", "<p>We retain personal information only as long as necessary for the purposes described in this policy, or as required by applicable law.</p>"),
      ("Your Rights", "<ul><li>Access, correct, or delete your personal information</li><li>Object to or restrict certain processing</li><li>Withdraw consent where processing is based on consent</li><li>Request a copy of your data in a portable format</li></ul>"),
      ("International Transfers", "<p>As a global company, information may be processed in countries other than your own, under appropriate safeguards.</p>"),
      ("Contact Us", f"<p>Questions about this policy can be directed to <a href='mailto:{CONTACT_INFO['email']}' style='color:var(--ember-glow);'>{CONTACT_INFO['email']}</a>.</p>"),
    ]
    legal_page("privacy.html", "Privacy Policy", "privacy.html",
      "How Noventrax Solutions collects, uses, and protects personal information across our website and services.", sections)

def build_terms():
    sections = [
      ("Acceptance of Terms", "<p>By accessing or using the Noventrax Solutions website, you agree to be bound by these Terms & Conditions. If you do not agree, please discontinue use of the site.</p>"),
      ("Use of Services", "<p>Our website and its content are provided for informational purposes about our services. Engagement for actual project delivery is governed separately by a signed statement of work or master services agreement.</p>"),
      ("Intellectual Property", "<p>All content on this website — including text, graphics, logos, and design — is the property of Noventrax Solutions, Inc. unless otherwise noted, and may not be reproduced without permission.</p>"),
      ("Client Deliverables", "<p>Ownership of code, designs, and other deliverables produced under a signed engagement transfers to the client as specified in that engagement's contract, typically upon final payment.</p>"),
      ("Limitation of Liability", "<p>To the fullest extent permitted by law, Noventrax Solutions is not liable for indirect, incidental, or consequential damages arising from use of this website.</p>"),
      ("Governing Law", "<p>These terms are governed by the laws of the State of California, without regard to conflict-of-law principles.</p>"),
      ("Changes to These Terms", "<p>We may update these terms periodically. Continued use of the website after changes constitutes acceptance of the revised terms.</p>"),
    ]
    legal_page("terms.html", "Terms & Conditions", "terms.html",
      "The terms governing use of the Noventrax Solutions website and general engagement principles.", sections)

def build_cookies():
    sections = [
      ("What Are Cookies", "<p>Cookies are small text files stored on your device that help websites function and collect analytics about how visitors use them.</p>"),
      ("Types of Cookies We Use", "<ul><li><strong>Essential cookies</strong> — required for core site functionality</li><li><strong>Analytics cookies</strong> — help us understand site usage to improve content</li><li><strong>Preference cookies</strong> — remember settings like navigation state</li></ul>"),
      ("Managing Cookies", "<p>Most browsers let you refuse or delete cookies through their settings. Disabling essential cookies may affect site functionality.</p>"),
      ("Third-Party Cookies", "<p>Some cookies may be set by third-party analytics providers we use to understand aggregate site traffic. These providers have their own privacy practices.</p>"),
      ("Contact Us", f"<p>Questions about our cookie use can be directed to <a href='mailto:{CONTACT_INFO['email']}' style='color:var(--ember-glow);'>{CONTACT_INFO['email']}</a>.</p>"),
    ]
    legal_page("cookies.html", "Cookie Policy", "cookies.html",
      "How Noventrax Solutions uses cookies and similar technologies on this website.", sections)

build_privacy(); build_terms(); build_cookies()
print("Generated legal pages")

# ---------------------------------------------------------------------------
# 404 PAGE
# ---------------------------------------------------------------------------
def build_404():
    path = "404.html"
    body = f"""
<section class="container error-page">
  <div class="reveal">
    <div class="error-code">404</div>
    <h2>This system doesn't exist — yet.</h2>
    <p style="max-width:44ch;margin:0 auto 1.5em;color:var(--text-mute);">The page you're looking for may have moved, been renamed, or never existed. Let's get you back on track.</p>
    <div class="hero-actions" style="justify-content:center;">
      <a href="index.html" class="btn btn-primary">Back to home {icon('arrow-right')}</a>
      <a href="contact.html" class="btn btn-ghost">Contact us</a>
    </div>
  </div>
</section>
"""
    write(path, page("Page Not Found", "The page you're looking for could not be found on the Noventrax Solutions website.", path, "", body))

build_404()
print("Generated 404.html")
