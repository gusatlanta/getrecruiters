"""Build every GetRecruiters page from this one file.

The pages share one menu and footer, so edit the copy here and rebuild
instead of editing the .html files by hand (a rebuild overwrites them):

    python tools/build_pages.py            # writes into the site folder
    python tools/build_pages.py <folder>   # writes somewhere else (for a test)
"""
import json
import re
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
SITE = "https://www.getrecruiters.com"
JOB_BOARD = "https://host.pcrecruiter.net/pcrbin/jobboard.aspx?uid=Staff%20Financial.npsg"
EMAIL = "gus@stafffinancial.com"
UNS = "https://images.unsplash.com/"

ICONS = {
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "award": '<path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "briefcase": '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
    "receipt": '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 17.5v-11"/>',
    "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "clipboard": '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "pulse": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "hospital": '<path d="M12 6v4"/><path d="M14 14h-4"/><path d="M14 18h-4"/><path d="M14 8h-4"/><path d="M18 12h2a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2h2"/><path d="M18 22V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v18"/>',
    "stethoscope": '<path d="M11 2v2"/><path d="M5 2v2"/><path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/><path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/>',
    "bone": '<path d="M17 10c.7-.7 1.69 0 2.5 0a2.5 2.5 0 1 0 0-5 .5.5 0 0 1-.5-.5 2.5 2.5 0 1 0-5 0c0 .81.7 1.8 0 2.5l-7 7c-.7.7-1.69 0-2.5 0a2.5 2.5 0 0 0 0 5c.28 0 .5.22.5.5a2.5 2.5 0 1 0 5 0c0-.81-.7-1.8 0-2.5Z"/>',
    "activity": '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    "building": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
    "flask": '<path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2"/><path d="M8.5 2h7"/><path d="M7 16h10"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "trending": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "landmark": '<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "video": '<path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "laptop": '<path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "dumbbell": '<path d="M14.4 14.4 9.6 9.6"/><path d="M18.657 21.485a2 2 0 1 1-2.829-2.828l-1.767 1.768a2 2 0 1 1-2.829-2.829l6.364-6.364a2 2 0 1 1 2.829 2.829l-1.768 1.767a2 2 0 1 1 2.828 2.829z"/><path d="m21.5 21.5-1.4-1.4"/><path d="M3.9 3.9 2.5 2.5"/><path d="M6.404 12.768a2 2 0 1 1-2.829-2.829l1.768-1.767a2 2 0 1 1-2.828-2.829l2.828-2.828a2 2 0 1 1 2.829 2.828l1.767-1.768a2 2 0 1 1 2.829 2.829z"/>',
    "server": '<rect width="20" height="8" x="2" y="2" rx="2" ry="2"/><rect width="20" height="8" x="2" y="14" rx="2" ry="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/>',
    "hardhat": '<path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5"/><path d="M14 6a6 6 0 0 1 6 6v3"/><path d="M4 15v-3a6 6 0 0 1 6-6"/><rect x="2" y="15" width="20" height="4" rx="1"/>',
    "calculator": '<rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><line x1="16" x2="16" y1="14" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/>',
    "banknote": '<rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/>',
    "factory": '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
}


def ico(name):
    return ('<svg class="ico" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" >' + ICONS[name] + '</svg>')


def fill(html):
    """Swap [[ico:name]] tokens and site constants into a template string."""
    html = re.sub(r"\[\[ico:([a-z]+)\]\]", lambda m: ico(m.group(1)), html)
    return (html.replace("{{JOB_BOARD}}", JOB_BOARD).replace("{{EMAIL}}", EMAIL)
            .replace("{{SITE}}", SITE).replace("{{UNS}}", UNS))


BRAND = '<img src="img/getrecruiters-logo.png" alt="GetRecruiters Group — powered by NorthPoint" class="brand-logo" width="212" height="58">'

NAV = '''
<!-- ── Navigation ───────────────────────────── -->
<nav class="navbar" id="navbar">
  <div class="container nav-inner">
    <a href="index.html" class="brand" aria-label="GetRecruiters Group — home">
      ''' + BRAND + '''
    </a>
    <div class="nav-menu" id="navMenu">
      <ul class="nav-links" id="navLinks">
        <li><a href="virtual-recruiters.html">Virtual Recruiters</a></li>
        <li><a href="hire-recruiters.html">Hire Recruiters</a></li>
        <li><a href="about.html#industries">Industries</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="partners.html">Partner Program</a></li>
      </ul>
      <div class="nav-ctas">
        <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" class="btn btn-outline-dark">Job Board</a>
        <a href="request-talent.html" class="btn btn-primary">Get a Recruiter</a>
      </div>
    </div>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false" aria-controls="navMenu"><span></span><span></span><span></span></button>
  </div>
</nav>
'''

FOOTER = '''
<!-- ── Footer ─────────────────────────────────── -->
<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="brand-chip" aria-label="GetRecruiters Group — home">
          ''' + BRAND + '''
        </a>
        <p>Dedicated virtual recruiters and recruiter staffing — a division of NorthPoint Search Group, recruiting for 20+ years.</p>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="virtual-recruiters.html">Virtual Recruiters</a></li>
          <li><a href="hire-recruiters.html">Hire Recruiters</a></li>
          <li><a href="about.html#industries">Industries</a></li>
          <li><a href="about.html">About Us</a></li>
          <li><a href="partners.html">Partner Program</a></li>
          <li><a href="{{JOB_BOARD}}" target="_blank" rel="noopener">Job Board ↗</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></li>
          <li><a href="tel:+14042500790">404-250-0790</a></li>
          <li><a href="tel:+16787775627">678-777-5627</a></li>
          <li><a href="contact.html">Send a Message</a></li>
          <li><a href="request-talent.html">Get a Recruiter</a></li>
          <li><span>Atlanta, GA · Serving clients nationwide</span></li>
        </ul>
      </div>
    </div>
    <hr class="footer-divider">
    <div class="footer-bottom">
      <span>&copy; 2026 GetRecruiters Group, a division of NorthPoint Search Group. All rights reserved.</span>
      <a href="contact.html">Privacy &amp; Terms</a>
    </div>
  </div>
</footer>

<script src="js/main.js"></script>
</body>
</html>
'''

ORG = {
    "@type": "Organization",
    "@id": SITE + "/#organization",
    "name": "GetRecruiters Group",
    "alternateName": ["GetRecruiters", "GetRecruiters.com"],
    "url": SITE,
    "logo": {"@type": "ImageObject", "url": SITE + "/img/getrecruiters-logo.png"},
    "description": "GetRecruiters Group, a division of NorthPoint Search Group, provides dedicated virtual recruiters and places recruiters, sourcers, talent acquisition leaders, and HR professionals as temp, temp-to-perm, and direct hire — for data centers, construction and the skilled trades, healthcare, public accounting, financial services, and every other industry.",
    "parentOrganization": {"@type": "Organization", "name": "NorthPoint Search Group"},
    "address": {"@type": "PostalAddress", "addressLocality": "Atlanta", "addressRegion": "GA", "addressCountry": "US"},
    "telephone": ["+1-404-250-0790", "+1-678-777-5627"],
    "email": EMAIL,
    "areaServed": ["United States"],
    "sameAs": [],
}


def head(file, title, desc, extra_schema=None, extra_head=""):
    url = SITE + "/" + ("" if file == "index.html" else file)
    graph = [ORG] + (extra_schema or [])
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">
  <link rel="apple-touch-icon" href="img/favicon-180.png">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="GetRecruiters Group">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/img/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{SITE}/img/og-image.png">
  <meta name="theme-color" content="#0b1f3d">
  <script type="application/ld+json">
{schema}
  </script>
  <link rel="stylesheet" href="css/styles.css">{extra_head}
</head>
<body>
'''


def page_hero(crumb, h1, sub, photo, pos="center"):
    return f'''
<!-- ── Page Hero ──────────────────────────────── -->
<section class="page-hero" style="background-image:url('{UNS}{photo}?auto=format&fit=crop&w=1600&q=80');background-position:{pos};">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Home</a><span>/</span>{crumb}</div>
    <h1>{h1}</h1>
    <p>{sub}</p>
  </div>
</section>
'''


CTA = '''
<!-- ── CTA band ───────────────────────────────── -->
<div class="cta-band">
  <div class="container">
    <h2>{h2}</h2>
    <p>{p}</p>
    <div class="cta-actions">
      <a href="request-talent.html" class="btn btn-white btn-lg">Get a Recruiter</a>
      <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" class="btn btn-outline-white btn-lg">Browse Open Jobs ↗</a>
    </div>
  </div>
</div>
'''


def cta(h2="Ready to Add a Recruiter<br>to Your Team?",
        p="Tell us what you're hiring for — we'll match you with a recruiter who knows your industry."):
    return CTA.replace("{h2}", h2).replace("{p}", p)


ROLES = ["Data Center Recruiter", "Construction &amp; Trades Recruiter", "Healthcare Recruiter",
         "Public Accounting Recruiter", "Financial Services Recruiter", "Technical / IT Recruiter",
         "Executive Recruiter", "Sourcer", "Recruiting Coordinator", "Talent Acquisition Manager",
         "Director / VP of Talent", "HR Generalist &amp; HRBP"]


def role_grid():
    return "\n".join(f'          <div class="specialty-item"><span class="specialty-dot"></span>{s}</div>' for s in ROLES)


INDUSTRIES = [("server", "Data Centers &amp; Mission-Critical"), ("hardhat", "Construction &amp; Skilled Trades"),
              ("stethoscope", "Healthcare"), ("calculator", "Public Accounting &amp; CPA Firms"),
              ("banknote", "Financial Services &amp; Banking"), ("shield", "Insurance"),
              ("factory", "Manufacturing"), ("laptop", "Technology &amp; SaaS"),
              ("scale", "Legal &amp; Professional Services"), ("truck", "Logistics &amp; Distribution"),
              ("trending", "Private Equity &amp; Portfolio Companies"), ("landmark", "Government &amp; Nonprofit")]


def industry_grid():
    return "\n".join(f'      <div class="industry-chip"><span class="industry-icon">[[ico:{i}]]</span>{t}</div>' for i, t in INDUSTRIES)


EOR = '''
<!-- ── EOR band ───────────────────────────────── -->
<div class="eor-band">
  <div class="container">
    <div class="eor-grid">
      <div>
        <span class="section-kicker">Payrolling · Employer of Record</span>
        <h2 class="section-title" style="color:var(--white);">Your Recruiter.<br>Our Payroll.</h2>
        <p style="color:rgba(255,255,255,.75);line-height:1.75;margin-bottom:28px;">GetRecruiters — powered by NorthPoint — acts as the Employer of Record for every temp recruiter. One simple bill rate. Zero HR overhead on your end.</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;">
          <a href="hire-recruiters.html" class="btn btn-white btn-lg">Hire Recruiters</a>
          <a href="request-talent.html" class="btn btn-outline-white btn-lg">Get a Recruiter</a>
        </div>
      </div>
      <div class="eor-features">
        <div class="eor-feature">
          <div class="eor-icon-wrap">[[ico:receipt]]</div>
          <div>
            <h4>Weekly Payroll</h4>
            <p>We payroll your temp recruiters every week and send one clean invoice at your agreed bill rate.</p>
          </div>
        </div>
        <div class="eor-feature">
          <div class="eor-icon-wrap">[[ico:shield]]</div>
          <div>
            <h4>Workers Comp &amp; Insurance</h4>
            <p>Fully covered under our policy. No exposure for your organization.</p>
          </div>
        </div>
        <div class="eor-feature">
          <div class="eor-icon-wrap">[[ico:clipboard]]</div>
          <div>
            <h4>Taxes &amp; Compliance</h4>
            <p>All federal, state, and FICA withholdings handled. W-2 issued at year-end.</p>
          </div>
        </div>
        <div class="eor-feature">
          <div class="eor-icon-wrap">[[ico:refresh]]</div>
          <div>
            <h4>Easy Temp-to-Perm</h4>
            <p>Love your recruiter? Move them to your payroll anytime with a simple conversion agreement.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
'''

EXAMPLE = '''
    <div class="example-callout"{style}>
      <div class="example-icon">[[ico:clipboard]]</div>
      <div>
        <span class="section-kicker">Sample: Screening Questionnaire</span>
        <h4>Data Center Recruiter — your questions, answered before the first call</h4>
        <p>We build every questionnaire with your input. For a data center recruiter, it might look like this — and every résumé arrives with the candidate's answers.</p>
        <ul class="sample-q">
          <li>Which data center or mission-critical builds have you recruited for — hyperscale, colocation, enterprise?</li>
          <li>Which roles did you fill — electricians, controls techs, superintendents, commissioning agents, project managers?</li>
          <li>How many hires did you close last year, and in which markets?</li>
          <li>Which ATS and sourcing tools do you use every day?</li>
        </ul>
      </div>
    </div>'''


def example(style=""):
    return EXAMPLE.replace("{style}", f' style="{style}"' if style else "")


AUDIENCE_STEPS = '''<li><strong>We build your list</strong> — the exact people you want to hire.</li>
        <li><strong>Our AI recruiting assistant writes the letter with you</strong> — then reaches out and invites them to apply for your job.</li>
        <li><strong>Candidates apply and film a video introduction.</strong></li>
        <li><strong>Our AI matches and scores every candidate for you.</strong></li>
        <li><strong>You reach out directly</strong> — or we do it all for you.</li>'''

INCLUDED = ["A dedicated, full-time recruiting professional on your openings",
            "Recruiters who know your industry — data centers, the trades, healthcare, public accounting, financial services, and more",
            "Active and passive sourcing, plus access to our candidate database",
            "Your jobs posted across the major job boards and our private LinkedIn groups",
            "Video introductions from applicants",
            "Screening questionnaire answers with every résumé",
            "Candidate skills testing, plus reference and background check coordination",
            "Works inside your ATS, inbox, and calendar — or runs the search on ours"]

FAQ = [
    ("What is a virtual recruiter?",
     "A dedicated recruiting professional who works your openings as part of your team — sourcing, screening, scheduling interviews, and keeping candidates warm — without you adding a recruiter to your payroll."),
    ("Can we hire a recruiter for our own team instead?",
     "Yes. We place recruiters, sourcers, recruiting coordinators, talent acquisition leaders, and HR professionals as temp, temp-to-perm, or direct hire. Temp recruiters run through our Employer of Record back office, and every direct hire is backed by our replacement guarantee."),
    ("Which industries do your recruiters know?",
     "Demand is strongest right now in data centers and mission-critical construction, the skilled trades, healthcare, public accounting, and financial services — and we recruit recruiters for insurance, manufacturing, technology, legal, logistics, private equity portfolio companies, government, and nonprofits too."),
    ("How quickly will we see candidates?",
     "When you're hiring a recruiter for your team, we deliver a blinded shortlist of pre-screened candidates within 48 to 72 hours. A virtual recruiter starts building your pipeline right after the discovery call."),
    ("Do you work inside our ATS?",
     "Yes. Your virtual recruiter can work inside your ATS, job boards, inbox, and calendar — or run the search on ours and hand you screened candidates."),
    ("Is GetRecruiters part of NorthPoint?",
     "Yes. GetRecruiters Group is a division of NorthPoint Search Group, which has been recruiting for more than 20 years."),
]


def faq_schema():
    strip = lambda s: s.replace("&amp;", "&")
    return [{"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in FAQ]}]


def faq_html():
    items = []
    for q, a in FAQ:
        items.append(f'''      <details itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
        <summary itemprop="name">{q}</summary>
        <div class="faq-a" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><span itemprop="text">{a}</span></div>
      </details>''')
    return "\n".join(items)


# Job titles that count as recruiting / HR roles for the hero card.
HOME_HEAD = '''
  <script>
  /* Recruiting and HR openings from the 100X jobs feed: fills the hero card and adds Google Jobs schema. */
  window.GR_RECRUIT = /(recruit|sourcer|sourcing specialist|talent acquisition|talent partner|human resources|\\bhr\\b|hrbp|people (ops|operations|partner)|onboarding (specialist|coordinator))/i;
  </script>'''

HOME = '''
<!-- ── Hero ─────────────────────────────────── -->
<section class="hero">
  <div class="container hero-grid">
    <div class="hero-inner">
      <span class="hero-kicker">Recruiters On Demand · A Division of NorthPoint</span>
      <h1>Recruiters Who Know<br><em>Your Industry</em></h1>
      <p class="hero-lede">Rent a dedicated virtual recruiter — or hire recruiters for your own team. Data centers, the trades, healthcare, public accounting, financial services, and everywhere else you're hiring.</p>
      <p class="hero-service-line">Virtual Recruiters &nbsp;·&nbsp; Temp &nbsp;·&nbsp; Temp-to-Perm &nbsp;·&nbsp; Direct Hire</p>

      <form class="hero-search-form" action="https://host.pcrecruiter.net/pcrbin/jobboard.aspx" method="get" target="_blank">
        <input type="hidden" name="uid" value="Staff Financial.npsg">
        <div class="hero-search-bar">
          <input type="text" name="keyword" placeholder="Keyword — e.g. Recruiter, Sourcer…" aria-label="Keyword">
          <select name="specialty" aria-label="Specialty">
            <option value="">Select Specialty</option>
            <option value="Recruiter">Recruiter</option>
            <option value="Technical Recruiter">Technical Recruiter</option>
            <option value="Healthcare Recruiter">Healthcare Recruiter</option>
            <option value="Sourcer">Sourcer</option>
            <option value="Recruiting Coordinator">Recruiting Coordinator</option>
            <option value="Talent Acquisition">Talent Acquisition Manager</option>
            <option value="HR">HR Generalist / HRBP</option>
          </select>
          <button type="submit">[[ico:search]] Search Jobs</button>
        </div>
      </form>
      <div class="hero-search-sub">
        <a href="virtual-recruiters.html" class="btn-hero-pill btn-hero-pill--filled">Get a Virtual Recruiter →</a>
        <a href="hire-recruiters.html" class="btn-hero-pill">Hire a Recruiter →</a>
        <a href="tel:+14042500790" class="btn-hero-pill">[[ico:phone]] 404-250-0790</a>
      </div>
    </div>
    <aside class="hero-card" aria-label="Recruiting roles we're filling now">
      <div class="hero-card-head">
        <div>
          <span class="hero-card-kicker">Now Placing</span>
          <h2>Recruiting &amp; HR roles we're filling now</h2>
        </div>
        <span class="live-pill">Hiring now</span>
      </div>
      <div id="heroJobs"><div class="np-empty">Loading positions…</div></div>
      <a class="hero-card-go" href="request-talent.html">Need a Recruiter? Tell Us &rarr;</a>
      <p class="hero-card-fine">Live from our job board. <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" style="color:var(--blue);font-weight:600;">See every opening ↗</a></p>
    </aside>
  </div>
</section>
<script>
(function(){
  var box=document.getElementById('heroJobs');
  function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
  function none(){box.innerHTML='<div class="np-empty">New recruiter searches open every week. <a href="request-talent.html">Tell us what you need →</a></div>';}
  fetch('https://100xrecruiting.com/api/public/jobs?limit=50').then(function(r){return r.json();}).then(function(d){
    var seen={}, jobs=((d&&d.jobs)||[]).filter(function(j){
      var t=(j.title||'').trim(); if(!window.GR_RECRUIT.test(t)||seen[t.toLowerCase()]) return false; seen[t.toLowerCase()]=1; return true;
    }).slice(0,5);
    if(!jobs.length){none();return;}
    box.innerHTML=jobs.map(function(j){
      var meta=[j.location,j.salary].filter(Boolean).join(' · ');
      var url=/^https:\\/\\//.test(j.job_url||'')?j.job_url:'{{JOB_BOARD}}';
      return '<a class="np-job" href="'+esc(url)+'" target="_blank" rel="noopener"><span class="np-job-dot"></span><span>'
        +'<span class="np-job-title">'+esc(j.title)+'</span>'+(meta?'<span class="np-job-meta">'+esc(meta)+'</span>':'')+'</span></a>';
    }).join('');
    var el=document.createElement('script'); el.type='application/ld+json';
    el.text=JSON.stringify({"@context":"https://schema.org","@graph":jobs.map(function(j){
      var loc=(j.location||'Atlanta, GA').split(',');
      return {"@type":"JobPosting","title":j.title,
        "datePosted":j.date_posted||new Date().toISOString().slice(0,10),
        "validThrough":new Date(Date.now()+60*24*60*60*1000).toISOString().slice(0,10),
        "employmentType":"FULL_TIME",
        "hiringOrganization":{"@type":"Organization","name":"GetRecruiters Group","sameAs":"{{SITE}}","logo":"{{SITE}}/img/getrecruiters-logo.png"},
        "jobLocation":{"@type":"Place","address":{"@type":"PostalAddress","addressLocality":(loc[0]||'Atlanta').trim(),"addressRegion":(loc[1]||'GA').trim(),"addressCountry":"US"}},
        "description":"Recruiting role placed by GetRecruiters Group, a division of NorthPoint Search Group. Contact us to learn more.",
        "url":/^https:\\/\\//.test(j.job_url||'')?j.job_url:'{{JOB_BOARD}}'};
    })});
    document.head.appendChild(el);
  }).catch(none);
})();
</script>

<!-- Candidate spotlights (blinded: no name, employer or school), fed from 100xrecruiting.com.
     data-only keeps recruiting and HR candidates only; the strip stays hidden when none match. -->
<div id="hx-spotlights" style="background:#f4f9fb;"></div>
<script src="https://100xrecruiting.com/static/spotlight_ticker.js?v=2" data-target="hx-spotlights" data-theme="light"
        data-only="recruiter,recruiting,sourcer,sourcing,talent acquisition,human resources,hr manager,hr generalist,hr business partner,people operations"
        data-fallback="{{SITE}}/contact.html" defer></script>

<!-- ── Stats strip ───────────────────────────── -->
<div class="hero-stats">
  <div class="container">
    <div class="stats-section-title">A History of Success</div>
    <div class="stats-box">
      <div class="stat-item"><div class="stat-num">105+</div><div class="stat-label">Years Combined Recruiting Experience</div></div>
      <div class="stat-item"><div class="stat-num">20+</div><div class="stat-label">Years Recruiting &amp; Staffing</div></div>
      <div class="stat-item"><div class="stat-num">1,000+</div><div class="stat-label">Candidate Video Intros Filmed</div></div>
      <div class="stat-item"><div class="stat-num">48–72 hrs</div><div class="stat-label">Average Shortlist Delivery</div></div>
    </div>
  </div>
</div>

<!-- ── Service photo cards ───────────────────── -->
<section class="section" style="padding-top:0;">
  <div class="container">
    <div class="service-cards four">

      <a class="svc-card" href="virtual-recruiters.html">
        <div class="svc-card-bg" style="background-image:url('{{UNS}}photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=800&q=80');background-position:center top;"></div>
        <div class="svc-card-overlay"></div>
        <div class="svc-card-body">
          <h3>Virtual Recruiters</h3>
          <p>A dedicated recruiter who works your openings as part of your team — without adding headcount.</p>
          <span class="svc-card-link">Learn More →</span>
        </div>
      </a>

      <a class="svc-card" href="hire-recruiters.html#temp">
        <div class="svc-card-bg" style="background-image:url('{{UNS}}photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80');"></div>
        <div class="svc-card-overlay"></div>
        <div class="svc-card-body">
          <h3>Temp Recruiters</h3>
          <p>Extra recruiting hands for hiring surges, new sites, and big projects — on our payroll.</p>
          <span class="svc-card-link">Learn More →</span>
        </div>
      </a>

      <a class="svc-card" href="hire-recruiters.html#direct">
        <div class="svc-card-bg" style="background-image:url('{{UNS}}photo-1568992687947-868a62a9f521?auto=format&fit=crop&w=800&q=80');"></div>
        <div class="svc-card-overlay"></div>
        <div class="svc-card-body">
          <h3>Direct Hire Recruiters</h3>
          <p>Recruiters, sourcers, and talent leaders placed on your team for the long term.</p>
          <span class="svc-card-link">Learn More →</span>
        </div>
      </a>

      <a class="svc-card" href="virtual-recruiters.html#rpo">
        <div class="svc-card-bg" style="background-image:url('{{UNS}}photo-1557804506-669a67965ba0?auto=format&fit=crop&w=800&q=80');"></div>
        <div class="svc-card-overlay"></div>
        <div class="svc-card-body">
          <h3>RPO &amp; Project Recruiting</h3>
          <p>A whole recruiting team for a new data center, plant, or location — scaled up or down as you need.</p>
          <span class="svc-card-link">Learn More →</span>
        </div>
      </a>

    </div>
  </div>
</section>

<!-- ── Industries ────────────────────────────── -->
<section class="section section-alt" id="industries">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Where Demand Is Hottest</span>
      <h2 class="section-title">Recruiters for Every Industry That's Hiring</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Demand for recruiters is up everywhere — especially in data centers, the skilled trades, healthcare, public accounting, and financial services. We match you with recruiters who already know your world.</p>
    </div>
    <div class="industry-grid">
''' + industry_grid() + '''
    </div>
  </div>
</section>

<!-- ── Virtual recruiter band ────────────────── -->
<section class="section section-dark">
  <div class="container split">
    <div>
      <span class="section-kicker">Virtual Recruiters</span>
      <h2 class="section-title">A Dedicated Recruiter,<br>Working <em>Your</em> Openings</h2>
      <p>Is hiring at the top of your to-do list? Are you sifting through stacks of unqualified résumés — and still not seeing the top talent in the market? A virtual recruiter brings full-time recruiting expertise to your company, so you can get back to growing it.</p>
      <a href="virtual-recruiters.html" class="btn btn-white btn-lg">How Virtual Recruiters Work →</a>
    </div>
    <div class="feature-list">
      <div class="feature">
        <div class="feature-icon">[[ico:users]]</div>
        <div><h4>Dedicated to You</h4><p>A full-time recruiting professional who learns your roles, your hiring managers, and your culture.</p></div>
      </div>
      <div class="feature">
        <div class="feature-icon">[[ico:zap]]</div>
        <div><h4>Pipelines Built Faster</h4><p>Our candidate database, the major job boards, and our private LinkedIn groups — working for you from day one.</p></div>
      </div>
      <div class="feature">
        <div class="feature-icon">[[ico:video]]</div>
        <div><h4>Screened, Tested &amp; on Video</h4><p>Questionnaire answers, skills testing, and a video introduction with every candidate you see.</p></div>
      </div>
    </div>
  </div>
</section>

<!-- ── Build the Perfect Candidate Audience ───── -->
<section class="section section-alt" id="candidate-audience">
  <div class="container split" style="align-items:start;">
    <div>
      <span class="section-kicker">Build the Perfect Candidate Audience</span>
      <h2 class="section-title">The Exact People You Want to Hire — <em>Invited to Apply</em></h2>
      <div class="section-divider"></div>
      <div class="pay-when-hire">[[ico:check]] <span>No upfront cost — you only pay when we're successful: when you hire. <span class="pwh-2">And we can payroll them for you.</span></span></div>
      <p class="section-sub" style="margin-bottom:16px;">We build a list for your HR or recruiting team with the exact people you want to hire. Our AI recruiting assistant writes the letter with you and invites them to apply — then our AI matches and scores every candidate for you.</p>
      <p class="section-sub" style="margin-bottom:28px;">It proactively builds a talent bench for every position on your org chart. You just build out the org chart.</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        <a href="virtual-recruiters.html#audience" class="btn btn-primary">See How It Works →</a>
        <a href="request-talent.html" class="btn btn-outline-dark">Tell Us How We Can Help</a>
      </div>
    </div>
    <div class="panel" style="padding:28px 28px 22px;">
      <ol class="num-steps">
        ''' + AUDIENCE_STEPS + '''
      </ol>
      <div class="audience-extras"><strong class="fee-line">When you hire, pick how you pay: we payroll them for one bill rate — or one flat fee, quoted up front.</strong><br>We can payroll your people as Employer of Record · 401(k) for every hire · Benefits available<br>We help you the entire time — live office hours for any questions · Membership includes our <a href="https://www.skool.com/100xrecruiting" target="_blank" rel="noopener">100X Recruiting community on Skool</a><br><strong>Our AI recruiting assistant comes with a 100% satisfaction guarantee.</strong></div>
    </div>
  </div>
</section>

<!-- ── How it works ──────────────────────────── -->
<section class="section" id="how-it-works">
  <div class="container">
    <span class="section-kicker">Our Process</span>
    <h2 class="section-title">From First Call to Hired</h2>
    <div class="section-divider"></div>
    <p class="section-sub">Whether you rent a recruiter or hire one, it starts the same way.</p>
    <div class="steps-row">
      <div class="step"><div class="step-num">1</div><h4>Discovery Call</h4><p>We learn your openings, hiring managers, ATS, and timeline — not just the job descriptions.</p></div>
      <div class="step"><div class="step-num">2</div><h4>Matched Recruiter</h4><p>We match a recruiter who knows your industry — or start the search for the recruiter you want to hire.</p></div>
      <div class="step"><div class="step-num">3</div><h4>Screened Candidates</h4><p>We build a screening questionnaire with your input, and every résumé arrives with the candidate's answers.</p></div>
      <div class="step"><div class="step-num">4</div><h4>Hired &amp; Guaranteed</h4><p>We manage offers, support onboarding, and back every direct hire with our replacement guarantee.</p></div>
    </div>
''' + example("margin-top:28px;") + '''
  </div>
</section>

<!-- ── Roles ─────────────────────────────────── -->
<section class="section section-alt">
  <div class="container">
    <div class="two-col">
      <div>
        <span class="section-kicker">Recruiting Roles We Fill</span>
        <h2 class="section-title">Every Seat on a<br><span class="accent">Recruiting Team</span></h2>
        <div class="section-divider"></div>
        <p class="section-sub">From sourcers and coordinators to industry recruiters and heads of talent — temp, temp-to-perm, or direct hire.</p>
        <div style="margin-top:28px;"><a href="hire-recruiters.html#titles" class="btn btn-primary">All Recruiting Roles →</a></div>
      </div>
      <div>
        <div class="specialty-grid">
''' + role_grid() + '''
        </div>
      </div>
    </div>
  </div>
</section>
''' + EOR + '''
<!-- ── FAQ ────────────────────────────────────── -->
<section class="section section-alt" aria-label="Frequently asked questions">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Common Questions</span>
      <h2 class="section-title">Everything You Need to Know</h2>
    </div>
    <div class="faq" itemscope itemtype="https://schema.org/FAQPage">
''' + faq_html() + '''
    </div>
  </div>
</section>
''' + cta()


# ───────────────────────────── Virtual recruiters ─────────────────────────────
def check_items(items):
    return "\n".join(f"          <li>{i}</li>" for i in items)


VIRTUAL = page_hero("Virtual Recruiters", "Dedicated <em>Virtual Recruiters</em>",
                    "Experienced recruiters who work your openings as part of your team — so you can hire faster without adding headcount.",
                    "photo-1573496359142-b8d87734a5a2", "center 25%") + '''
<section class="section">
  <div class="container">
    <div class="svc-blocks">
    <div class="svc-block svc-block--top" id="included">
      <div>
        <span class="pill-tag">What's Included</span>
        <h3>Recruiting Expertise, Plugged Into Your Company</h3>
        <p>We've all heard "people are your most important asset" — and they're hard to find. You're busy growing your business, and hiring is critical to your success. A virtual recruiter takes sourcing and screening off your plate.</p>
        <ul class="checklist">
''' + check_items(INCLUDED) + '''
        </ul>
        <a href="request-talent.html" class="btn btn-primary">Get a Virtual Recruiter</a>
      </div>
      <div class="svc-aside">
        <div class="aside-ico">[[ico:target]]</div>
        <h4>Best For</h4>
        <ul>
          <li>Growing companies with no recruiter yet</li>
          <li>HR teams buried in open requisitions</li>
          <li>Hiring surges, new sites, and new data centers</li>
          <li>Hard-to-fill trades, clinical, and finance roles</li>
          <li>Companies tired of paying a fee on every hire</li>
        </ul>
        <div class="fee">
          <div class="fee-label">How It's Priced</div>
          <div class="fee-text">You pay for your recruiter's time, quoted up front after a short call.</div>
        </div>
      </div>
    </div>

    <div class="svc-block svc-block--top" id="rpo">
      <div>
        <span class="pill-tag">RPO &amp; Project Recruiting</span>
        <h3>A Whole Recruiting Team, When You Need One</h3>
        <p>Opening a data center, a plant, or a new market? Our Recruitment Process Outsourcing (RPO) solution gives you a dedicated recruiting team built around your project — ramped up for the push and scaled back when you're staffed.</p>
        <ul class="checklist">
          <li>Scalable — ramp up or down as hiring needs change</li>
          <li>We integrate with your ATS, culture, and hiring process</li>
          <li>Full project staffing from intake to offer</li>
          <li>Dedicated account manager and weekly reporting</li>
          <li>Works alongside your existing HR team</li>
        </ul>
        <a href="request-talent.html" class="btn btn-primary">Tell Us About Your Project</a>
      </div>
      <div class="tool-cards">
        <div class="tool-card">
          <div class="tool-ico">[[ico:clipboard]]</div>
          <div><h4>Customized Screening Questionnaires</h4><p>Role-specific questions built with your input — the candidate's answers come with every résumé.</p></div>
        </div>
        <div class="tool-card">
          <div class="tool-ico">[[ico:video]]</div>
          <div><h4>Video Introductions</h4><p>See how candidates communicate before the first call — not just a PDF.</p>
            <div style="margin-top:14px;"><div class="mini-stat-num">1,000+</div><div class="mini-stat-label">Candidate Video Intros Filmed</div></div></div>
        </div>
        <div class="tool-card">
          <div class="tool-ico">[[ico:wrench]]</div>
          <div><h4>Built Around Your Hiring</h4><p>Your timeline, budget, and team structure — from one recruiter to a full project team.</p></div>
        </div>
      </div>
    </div>
''' + example() + '''

    <div class="svc-block svc-block--dark svc-block--top" id="audience">
      <div class="on-dark">
        <span class="pill-tag">Perfect Candidate Audience</span>
        <h3>Build the Perfect Candidate Audience</h3>
        <div class="pay-when-hire pay-when-hire--dark">[[ico:check]] <span>No upfront cost — you only pay when we're successful: when you hire. <span class="pwh-2">And we can payroll them for you.</span></span></div>
        <p>We build a list for your HR or recruiting team with the exact people you want to hire — then invite them to apply.</p>
        <ol class="num-steps">
        ''' + AUDIENCE_STEPS + '''
        </ol>
        <a href="request-talent.html" class="btn btn-white">Build My Candidate Audience</a>
      </div>
      <div class="svc-aside">
        <div class="aside-ico">[[ico:users]]</div>
        <h4>We Can Handle the Rest</h4>
        <ul class="checklist">
          <li>We payroll your people — our back office is the Employer of Record</li>
          <li>Every hire gets our 401(k) program</li>
          <li>We can even provide benefits</li>
        </ul>
        <div class="fee">
          <div class="fee-label">We Help You the Entire Time</div>
          <div class="fee-text"><strong style="color:var(--white);">And you only pay when we're successful.</strong> Live office hours for any questions — plus membership in our <a href="https://www.skool.com/100xrecruiting" target="_blank" rel="noopener">100X Recruiting community on Skool</a>. Our AI recruiting assistant comes with a 100% satisfaction guarantee.</div>
        </div>
      </div>
    </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <span class="section-kicker">How It Works</span>
    <h2 class="section-title">Your Virtual Recruiter in Four Steps</h2>
    <div class="section-divider"></div>
    <div class="steps-row">
      <div class="step"><div class="step-num">1</div><h4>Discovery Call</h4><p>Your openings, hiring managers, ATS, and what a great hire looks like.</p></div>
      <div class="step"><div class="step-num">2</div><h4>Meet Your Recruiter</h4><p>We match a recruiter who knows your industry and your kind of roles.</p></div>
      <div class="step"><div class="step-num">3</div><h4>They Work Your Reqs</h4><p>Sourcing, screening, scheduling, and follow-up — inside your process.</p></div>
      <div class="step"><div class="step-num">4</div><h4>You Hire</h4><p>Regular updates on every opening, and screened candidates ready to interview.</p></div>
    </div>
  </div>
</section>
''' + cta(h2="Put a Recruiter to Work<br>on Your Openings", p="Tell us what you're hiring for — we'll match you with a recruiter who knows your industry.")


# ───────────────────────────── Hire recruiters ─────────────────────────────
def svc_block(id_, tag, h3, p, items, btn, aside_icon, aside_title, aside_items, fee_label, fee_text, dark=False):
    cls = "svc-block" + (" svc-block--dark" if dark else "")
    btn_cls = "btn btn-white" if dark else "btn btn-primary"
    return f'''
    <div class="{cls}" id="{id_}">
      <div>
        <span class="pill-tag">{tag}</span>
        <h3>{h3}</h3>
        <p>{p}</p>
        <ul class="checklist">
{check_items(items)}
        </ul>
        <a href="request-talent.html" class="{btn_cls}">{btn}</a>
      </div>
      <div class="svc-aside">
        <div class="aside-ico">[[ico:{aside_icon}]]</div>
        <h4>{aside_title}</h4>
        <ul>
{check_items(aside_items)}
        </ul>
        <div class="fee">
          <div class="fee-label">{fee_label}</div>
          <div class="fee-text">{fee_text}</div>
        </div>
      </div>
    </div>'''


TITLE_GROUPS = [
    ("Industry Recruiters", ["Data Center &amp; Mission-Critical Recruiter", "Construction &amp; Skilled Trades Recruiter",
                             "Healthcare Recruiter", "Public Accounting Recruiter",
                             "Financial Services &amp; Banking Recruiter", "Technical / IT Recruiter"]),
    ("Recruiting Team", ["Full-Cycle Corporate Recruiter", "Sourcer / Sourcing Specialist", "Recruiting Coordinator",
                         "High-Volume &amp; Hourly Recruiter", "Campus &amp; Early-Career Recruiter", "Executive Recruiter"]),
    ("Talent Leadership", ["Talent Acquisition Manager", "Director of Talent Acquisition", "VP / Head of Talent",
                           "Recruiting Operations Manager", "Employer Brand Manager", "RPO Program Manager"]),
    ("HR &amp; People", ["HR Generalist", "HR Business Partner", "HR Manager", "People Operations Manager",
                        "Onboarding Specialist", "HR Coordinator"]),
]


def title_groups():
    out = []
    for g, titles in TITLE_GROUPS:
        items = "\n".join(f'          <div class="specialty-item"><span class="specialty-dot"></span>{t}</div>' for t in titles)
        out.append(f'''      <div>
        <h3 style="font-size:1.1rem;margin-bottom:14px;">{g}</h3>
        <div class="specialty-grid" style="grid-template-columns:1fr;">
{items}
        </div>
      </div>''')
    return "\n".join(out)


HIRE = page_hero("Hire Recruiters", "Hire <em>Recruiters</em> for Your Team",
                 "Recruiters, sourcers, talent leaders, and HR pros — as temp, temp-to-perm, or direct hire.",
                 "photo-1568992687947-868a62a9f521") + '''
<section class="section">
  <div class="container">
    <span class="section-kicker">Three Ways to Hire</span>
    <h2 class="section-title">Temp, Temp-to-Perm, or Direct Hire</h2>
    <div class="svc-blocks">''' + svc_block(
    "temp", "Temp", "Temp Recruiters",
    "Need extra recruiting hands for a hiring surge, a new site, or a data center build? Our temp recruiters step in quickly — screened and ready to work your reqs from day one.",
    ["Rapid deployment — often within 48–72 hours", "Assignments from a few weeks to 12+ months",
     "We handle payroll, taxes, and workers' comp", "Recruiters who already know your industry",
     "Scale a whole recruiting team up or down"],
    "Request a Temp Recruiter", "clock", "Best For",
    ["Hiring surges and seasonal peaks", "New plants, sites, and data center builds", "Leave and vacancy coverage",
     "Backlogs of open requisitions", "Pilots before adding headcount"],
    "Fee Structure", "Bill rate per hour — no placement fee") + svc_block(
    "temp-to-perm", "Temp-to-Perm", "Temp-to-Perm Recruiters",
    "Start a recruiter as a temp and move them to your payroll when you're sure of the fit. It lowers the risk for both sides — and works well while headcount approval is in progress.",
    ["Typical temp period of 90–180 days", "They work on your team from day one", "Conversion fee agreed upfront",
     "Ideal when headcount approval is in progress", "They learn your hiring managers before converting"],
    "Explore Temp-to-Perm", "refresh", "Best For",
    ["First recruiter for a growing company", "New positions with evolving scope", "Teams under a hiring freeze",
     "Roles where team fit is critical", "Building a recruiting function from scratch"],
    "Fee Structure", "Bill rate as a temp; reduced conversion fee when you hire them") + svc_block(
    "direct", "Direct Hire", "Direct Hire Recruiters",
    "When you need the right recruiter or talent leader on your team for the long haul, we deliver a curated shortlist of qualified, motivated candidates — fast.",
    ["Deep intake call — roles, hiring managers, ATS, and team", "Active and passive candidate sourcing",
     "Screening questionnaire answers with every résumé", "Reference and background coordination",
     "Offer negotiation and onboarding support", "Replacement guarantee included"],
    "Start a Direct Hire Search", "award", "Best For",
    ["Industry recruiters — data centers, trades, healthcare, accounting, finance", "Talent acquisition managers and directors",
     "Heads of talent and recruiting operations", "Sourcers and recruiting coordinators", "HR generalists and HR business partners"],
    "Fee Structure", "Contingency — fee applies only upon successful placement", dark=True) + '''
    </div>
  </div>
</section>

<section class="section section-alt" id="titles" style="scroll-margin-top:calc(var(--nav-h) + 8px);">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Recruiting Roles We Fill</span>
      <h2 class="section-title">Every Seat on a Recruiting Team</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Industry recruiters, the recruiting team around them, and the leaders who run it.</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:28px;margin-top:40px;">
''' + title_groups() + '''
    </div>
  </div>
</section>
''' + EOR + '''
<section class="section section-dark">
  <div class="container split">
    <div>
      <span class="section-kicker">For Recruiters</span>
      <h2 class="section-title">Your Next Recruiting<br>Role <em>Starts Here</em></h2>
      <p>Recruiters, sourcers, coordinators, and talent leaders: we represent you confidentially and introduce you to companies that are hiring now — many before the role is ever posted.</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" class="btn btn-white btn-lg">Browse Open Jobs ↗</a>
        <a href="contact.html" class="btn btn-outline-white btn-lg">Talk to Us</a>
      </div>
    </div>
    <div class="feature-list">
      <div class="feature"><div class="feature-icon">[[ico:lock]]</div><div><h4>Confidential Representation</h4><p>Your name and employer stay hidden until you say yes to an introduction.</p></div></div>
      <div class="feature"><div class="feature-icon">[[ico:video]]</div><div><h4>Stand Out With a Video Intro</h4><p>Film a short introduction so hiring managers meet you before the first call.</p></div></div>
      <div class="feature"><div class="feature-icon">[[ico:target]]</div><div><h4>Roles That Fit Your Specialty</h4><p>Data centers, trades, healthcare, accounting, finance — we call when it's a real match.</p></div></div>
    </div>
  </div>
</section>
''' + cta(h2="Ready to Hire a Recruiter?", p="Tell us about the role and we'll deliver a shortlist in 48–72 hours.")


# ───────────────────────────── About ─────────────────────────────
def diff(icon, h4, p):
    return f'''      <div class="diff-item">
        <div class="diff-icon">[[ico:{icon}]]</div>
        <div>
          <h4>{h4}</h4>
          <p>{p}</p>
        </div>
      </div>'''


ABOUT = page_hero("About Us", "About GetRecruiters",
                  "A division of NorthPoint Search Group — putting experienced recruiters to work for companies that are hiring.",
                  "photo-1486406146926-c627a92ad1ab") + '''
<section class="section">
  <div class="container">
    <div class="two-col">
      <div>
        <span class="section-kicker">Our Story</span>
        <h2 class="section-title">Recruiting Is What We Do — Now It Works for You</h2>
        <div class="section-divider"></div>
        <p style="color:var(--text-muted);line-height:1.85;margin-bottom:18px;">GetRecruiters Group is a division of NorthPoint Search Group. We've been recruiting for more than 20 years, and we know how hard it is to find great people while you're busy running the business.</p>
        <p style="color:var(--text-muted);line-height:1.85;margin-bottom:18px;">Demand for recruiters is up everywhere — especially in data centers and mission-critical construction, the skilled trades, healthcare, public accounting, and financial services. So we put experienced recruiters on your openings: a dedicated virtual recruiter who works as part of your team, or recruiters you hire onto your own staff.</p>
        <p style="color:var(--text-muted);line-height:1.85;margin-bottom:32px;">Either way, you get recruiters who already know your industry — and a team behind them that has done this thousands of times.</p>
        <div class="mini-stats">
          <div><div class="mini-stat-num">20+</div><div class="mini-stat-label">Years Recruiting</div></div>
          <div><div class="mini-stat-num">105+</div><div class="mini-stat-label">Years Combined Experience</div></div>
          <div><div class="mini-stat-num">1,000+</div><div class="mini-stat-label">Candidate Video Intros</div></div>
        </div>
      </div>
      <div>
        <img class="img-frame" src="{{UNS}}photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=800&q=80" alt="Recruiting team working together" loading="lazy">
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Why GetRecruiters</span>
      <h2 class="section-title">Recruiting Help Done Differently</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Recruiting is all we do — and we bring it to your company two ways.</p>
    </div>
    <div class="diff-grid">
''' + "\n".join([
    diff("target", "Recruiters Who Know Your Industry", "Data centers, the trades, healthcare, public accounting, financial services — we match recruiters who already speak your candidates' language."),
    diff("users", "Rent or Hire — Your Choice", "A dedicated virtual recruiter on your openings, or a recruiter on your own staff as temp, temp-to-perm, or direct hire."),
    diff("zap", "Fast Pipelines", "Our candidate database, the major job boards, and our private LinkedIn groups put candidates in front of you quickly."),
    diff("clipboard", "Custom Screening Questionnaires", "Every résumé arrives with the candidate's answers to your questions — before the first call."),
    diff("video", "Video Introductions", "See how candidates communicate before you spend time on a phone screen."),
    diff("shield", "Guaranteed &amp; Fully Back-Officed", "Every direct hire is backed by our replacement guarantee, and every temp runs through our Employer of Record back office."),
]) + '''
    </div>
  </div>
</section>

<section class="section section-alt" id="industries" style="scroll-margin-top:calc(var(--nav-h) + 8px);padding-top:0;">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Industries</span>
      <h2 class="section-title">Recruiters for Every Industry That's Hiring</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Strongest demand right now: data centers, the skilled trades, healthcare, public accounting, and financial services — and everywhere else.</p>
    </div>
    <div class="industry-grid">
''' + industry_grid() + '''
    </div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div>
      <span class="section-kicker">Our Values</span>
      <h2 class="section-title">What Guides Every Search</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Great recruiters make every other hire easier.</p>
    </div>
    <ul class="checklist">
      <li><strong>Your team first.</strong> Your recruiter works inside your process, with your hiring managers.</li>
      <li><strong>Depth over volume.</strong> A few right-fit candidates beat a stack of maybe-fits every time.</li>
      <li><strong>Discretion.</strong> Confidential searches and blinded profiles protect clients and candidates alike.</li>
      <li><strong>Straight answers.</strong> Honest feedback on the market, pay, and candidates — even when it's not what you hoped to hear.</li>
    </ul>
  </div>
</section>
''' + cta(h2="Let's Work Together", p="Tell us what you're hiring for — we'll take it from there.")


# ───────────────────────────── Request talent ─────────────────────────────
def optin_step(n, title, text):
    return f'''          <div class="optin-step">
            <div class="optin-step-num">{n}</div>
            <div><strong>{title}</strong><span>{text}</span></div>
          </div>'''


REQUEST = '''
<!-- ── Opt-in Hero ────────────────────────────── -->
<section class="optin-hero" style="background-image:url('{{UNS}}photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1600&q=80');">
  <div class="container">
    <div class="hero-badge" style="color:rgba(255,255,255,.85);">For Hiring Managers &amp; HR Leaders</div>
    <h1>Get a <em>Recruiter</em><br>Working for You</h1>
    <p>Tell us what you're hiring for. We'll match you with a virtual recruiter — or start the search for a recruiter to join your team.</p>
  </div>
</section>

<section class="section" style="padding-top:0;background:var(--off-white);">
  <div class="container">
    <div class="optin-layout">
      <div class="optin-pitch">
        <span class="section-label">Why GetRecruiters</span>
        <h2 class="section-title" style="font-size:1.6rem;">What Happens After<br>You Submit</h2>
        <div class="optin-steps">
''' + "\n".join([
    optin_step(1, "Discovery Call (same day)", "We reach out within hours to learn your openings, hiring managers, and timeline."),
    optin_step(2, "Matched Recruiter", "We match a recruiter who knows your industry — or start the search for the one you'll hire."),
    optin_step(3, "Screened Candidates", "Every résumé arrives with answers to your screening questions."),
    optin_step(4, "You Hire. We Back It.", "Every direct hire is backed by our replacement guarantee."),
]) + '''
        </div>
        <div class="optin-box">
          <div class="box-label">Industries We Recruit For</div>
          <div class="tags">
            <span class="tag">Data Centers</span><span class="tag">Construction &amp; Trades</span><span class="tag">Healthcare</span>
            <span class="tag">Public Accounting</span><span class="tag">Financial Services</span><span class="tag">Insurance</span>
            <span class="tag">Manufacturing</span><span class="tag">Technology</span><span class="tag">+ everywhere</span>
          </div>
        </div>
      </div>

      <div class="form-card form-card--lift">
        <h3>Get a Recruiter</h3>
        <p class="form-intro">No commitment required — let's see if we can help.</p>
        <form data-form="getrecruiters-request" action="mailto:{{EMAIL}}" method="POST" enctype="text/plain">
          <div class="form-legend">About You</div>
          <div class="form-row">
            <div class="form-group"><label for="r-first">First Name *</label><input type="text" id="r-first" name="first_name" class="form-control" placeholder="Jane" required></div>
            <div class="form-group"><label for="r-last">Last Name *</label><input type="text" id="r-last" name="last_name" class="form-control" placeholder="Smith" required></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="r-email">Work Email *</label><input type="email" id="r-email" name="email" class="form-control" placeholder="jane@yourcompany.com" required></div>
            <div class="form-group"><label for="r-phone">Phone</label><input type="tel" id="r-phone" name="phone" class="form-control" placeholder="(404) 555-0100"></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="r-company">Company *</label><input type="text" id="r-company" name="company" class="form-control" placeholder="Your company" required></div>
            <div class="form-group"><label for="r-title">Your Title</label><input type="text" id="r-title" name="your_title" class="form-control" placeholder="VP of HR"></div>
          </div>
          <div class="form-legend">What You Need</div>
          <div class="form-row">
            <div class="form-group"><label for="r-type">What do you need? *</label>
              <select id="r-type" name="hire_type" class="form-control" required>
                <option value="" disabled selected>Select</option>
                <option>Dedicated virtual recruiter</option><option>Temp recruiter</option><option>Temp-to-perm recruiter</option>
                <option>Direct hire recruiter or TA leader</option><option>RPO / project recruiting team</option><option>Not sure yet</option>
              </select>
            </div>
            <div class="form-group"><label for="r-industry">Industry</label>
              <select id="r-industry" name="industry" class="form-control">
                <option value="" disabled selected>Select</option>
                <option>Data centers &amp; mission-critical</option><option>Construction &amp; skilled trades</option><option>Healthcare</option>
                <option>Public accounting</option><option>Financial services &amp; banking</option><option>Insurance</option>
                <option>Manufacturing</option><option>Technology</option><option>Legal &amp; professional services</option><option>Other</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="r-role">Roles you're hiring for *</label><input type="text" id="r-role" name="role_title" class="form-control" placeholder="e.g. electricians, superintendents" required></div>
            <div class="form-group"><label for="r-openings">How many openings?</label><input type="text" id="r-openings" name="openings" class="form-control" placeholder="e.g. 15"></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="r-location">Location *</label><input type="text" id="r-location" name="location" class="form-control" placeholder="Atlanta, GA or Remote" required></div>
            <div class="form-group"><label for="r-timeline">Timeline</label>
              <select id="r-timeline" name="timeline" class="form-control">
                <option value="" disabled selected>Select</option>
                <option>ASAP — within 2 weeks</option><option>1 month</option><option>1–3 months</option><option>Planning ahead (3+ months)</option>
              </select>
            </div>
          </div>
          <div class="form-group"><label for="r-notes">Anything else we should know?</label><textarea id="r-notes" name="notes" class="form-control" placeholder="Your ATS, hiring managers, must-haves, budget…"></textarea></div>
          <button type="submit" class="btn btn-primary btn-lg btn-block">Get a Recruiter →</button>
          <p class="form-note">No commitment to submit. We'll reach out within a few hours.</p>
          <div class="alert alert-success">✓ Request received! We'll be in touch within a few hours.</div>
        </form>
      </div>
    </div>
  </div>
</section>

<section style="background:var(--white);padding:48px 0;border-top:1px solid var(--border);">
  <div class="container">
    <div class="stats-box" style="margin:0;">
      <div class="stat-item"><div class="stat-num">48–72 hrs</div><div class="stat-label">Average Shortlist Delivery</div></div>
      <div class="stat-item"><div class="stat-num">1,000+</div><div class="stat-label">Candidate Video Intros Filmed</div></div>
      <div class="stat-item"><div class="stat-num">105+</div><div class="stat-label">Years Combined Experience</div></div>
      <div class="stat-item"><div class="stat-num">20+</div><div class="stat-label">Years Recruiting &amp; Staffing</div></div>
    </div>
  </div>
</section>
'''

# ───────────────────────────── Contact ─────────────────────────────
CONTACT = page_hero("Contact", "Get in Touch",
                    "Whether you need recruiting help, you're a recruiter exploring a move, or you just have a question — we'd love to hear from you.",
                    "photo-1497366216548-37526070297c") + '''
<section class="section">
  <div class="container">
    <div class="contact-grid">
      <div>
        <span class="section-label">Contact Information</span>
        <h2 class="section-title">Let's Start a Conversation</h2>
        <p style="color:var(--text-muted);line-height:1.8;">We typically respond within one business day. For urgent hiring needs, call or email directly and mention your timeline.</p>
        <div class="contact-list">
          <div class="contact-item"><div class="contact-icon">[[ico:phone]]</div><div><div class="contact-label">Phone</div><a href="tel:+14042500790">404-250-0790</a><br><a href="tel:+16787775627">678-777-5627</a></div></div>
          <div class="contact-item"><div class="contact-icon">[[ico:mail]]</div><div><div class="contact-label">Email</div><a href="mailto:{{EMAIL}}">{{EMAIL}}</a></div></div>
          <div class="contact-item"><div class="contact-icon">[[ico:pin]]</div><div><div class="contact-label">Location</div><strong>Atlanta, GA</strong><div class="contact-sub">Serving clients nationwide</div></div></div>
          <div class="contact-item"><div class="contact-icon">[[ico:briefcase]]</div><div><div class="contact-label">Job Board</div><a href="{{JOB_BOARD}}" target="_blank" rel="noopener" style="color:var(--blue);">View Open Positions ↗</a></div></div>
        </div>
        <div class="note-card">
          <h4>Are you a recruiter looking for your next role?</h4>
          <p>Browse current recruiting and HR openings on our job board.</p>
          <a href="{{JOB_BOARD}}" target="_blank" rel="noopener" class="btn btn-primary">Browse Open Jobs ↗</a>
        </div>
      </div>

      <div class="form-card">
        <h3>Send Us a Message</h3>
        <p class="form-intro">We'll get back to you within one business day.</p>
        <form data-form="getrecruiters-contact" action="mailto:{{EMAIL}}" method="POST" enctype="text/plain">
          <div class="form-row">
            <div class="form-group"><label for="m-first">First Name *</label><input type="text" id="m-first" name="first_name" class="form-control" required></div>
            <div class="form-group"><label for="m-last">Last Name *</label><input type="text" id="m-last" name="last_name" class="form-control" required></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="m-email">Email *</label><input type="email" id="m-email" name="email" class="form-control" required></div>
            <div class="form-group"><label for="m-phone">Phone</label><input type="tel" id="m-phone" name="phone" class="form-control"></div>
          </div>
          <div class="form-row">
            <div class="form-group"><label for="m-company">Company</label><input type="text" id="m-company" name="company" class="form-control"></div>
            <div class="form-group"><label for="m-topic">I'm…</label>
              <select id="m-topic" name="topic" class="form-control">
                <option>Looking for recruiting help</option><option>A recruiter looking for a new role</option><option>Interested in the Partner Program</option><option>Something else</option>
              </select>
            </div>
          </div>
          <div class="form-group"><label for="m-message">Message *</label><textarea id="m-message" name="message" class="form-control" required></textarea></div>
          <button type="submit" class="btn btn-primary btn-lg btn-block">Send Message →</button>
          <div class="alert alert-success">✓ Message sent! We'll be in touch within one business day.</div>
        </form>
        <p class="form-note" style="margin-top:20px;">Privacy: we use what you send only to respond to you, and we never sell your information.</p>
      </div>
    </div>
  </div>
</section>
'''

# ───────────────────────────── Partners ─────────────────────────────
def feat(icon, h4, p):
    return f'''      <div class="trio-card">
        <div class="feature-icon">[[ico:{icon}]]</div>
        <h4>{h4}</h4>
        <p>{p}</p>
      </div>'''


def earn(num, h4, p):
    return f'''      <div class="earn-card">
        <div class="earn-num">{num}</div>
        <h4>{h4}</h4>
        <p>{p}</p>
      </div>'''


PARTNERS = page_hero("Partner Program", "Join Our Partner Program",
                     "You know the companies that are hiring. Put those relationships to work — you bring the need, we do all the recruiting, and you get paid.",
                     "photo-1542744173-8e7e53415bb0") + '''
<section class="section">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">For HR Leaders, Consultants &amp; Anyone Whose Network Hires</span>
      <h2 class="section-title">You get the order. We fill it.</h2>
      <div class="section-divider"></div>
      <p class="section-sub">You get paid for every hour someone works.</p>
    </div>
    <div class="trio">
''' + "\n".join([
    feat("handshake", "You get the order", 'Hear "we need recruiting help" from someone in your network — and make the introduction.'),
    feat("search", "We fill it", "We put a virtual recruiter on their openings, or place recruiters on their team — temp, temp-to-perm, or direct hire."),
    feat("receipt", "You get paid", "A referral fee on direct hire placements, and a recurring share of every hour your client's temps work — for the life of the assignment."),
]) + '''
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">What You Earn</span>
      <h2 class="section-title">Simple, generous, recurring.</h2>
      <div class="section-divider"></div>
    </div>
    <div class="earn-grid">
''' + "\n".join([
    earn("10%", "Direct hire placements", "Your client hires direct through us — you earn 10% of the placement fee we collect. Paid when we collect from the client."),
    earn("25%", "Temp net spread", "Your client runs temps or temp-to-perm workers — you earn 25% of the net spread on every hour they bill."),
    earn("Recurring", "While they work", "Temp commissions aren't one-time. They keep paying as long as your client's temps keep billing. Build a book."),
    earn("15th", "Paid every month", "Commissions are calculated on money actually received and paid on the 15th of the following month. Every dollar tracked for you."),
]) + '''
    </div>
  </div>
</section>

<section class="section">
  <div class="container split" style="align-items:start;">
    <div>
      <span class="section-kicker">Who This Is For</span>
      <h2 class="section-title">Anyone whose network hires.</h2>
      <div class="section-divider"></div>
      <p class="section-sub">HR leaders and consultants. CFOs and CPA firm partners. Construction, data center, and healthcare executives. Retired executives — anyone whose network is always hiring. You never become a recruiter; you bring the need and stay the relationship owner, and our team fills it.</p>
    </div>
    <div>
      <span class="section-kicker">How It Works</span>
      <h2 class="section-title">Four simple steps.</h2>
      <ol class="num-steps">
        <li><strong>Apply below</strong> — we review every partner personally and set you up.</li>
        <li><strong>Hear "we need a recruiter"</strong> (or a whole recruiting team for a new site) — send it in.</li>
        <li><strong>We fill it</strong> — a virtual recruiter, or temp, temp-to-perm, or direct hire.</li>
        <li><strong>You're paid on the 15th of the following month</strong> — 10% of the fee on direct hire, 25% of net spread on temps, recurring while the worker bills.</li>
      </ol>
    </div>
  </div>
  <div class="container">
    <p class="fine-print">Net spread = what the client pays, minus worker wages and employer burden (taxes, workers comp, benefits, compliance). Commissions are calculated on payments actually received; refunded or unpaid invoices are reversed. Self-referrals and companies already under agreement with us don't qualify. Earned commissions are never reduced.</p>
  </div>
</section>

<section class="section section-alt" id="apply">
  <div class="container">
    <div class="centered">
      <span class="section-kicker">Apply</span>
      <h2 class="section-title">Become a Partner</h2>
      <div class="section-divider"></div>
      <p class="section-sub">Sixty seconds. We review every application personally and reply within one business day.</p>
    </div>
    <div class="form-card form-narrow">
      <form data-form="getrecruiters-partner" action="mailto:{{EMAIL}}" method="POST" enctype="text/plain">
        <div class="form-row">
          <div class="form-group"><label for="p-name">Your Name *</label><input type="text" id="p-name" name="name" class="form-control" required></div>
          <div class="form-group"><label for="p-company">Company</label><input type="text" id="p-company" name="company" class="form-control"></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label for="p-email">Work Email *</label><input type="email" id="p-email" name="email" class="form-control" required></div>
          <div class="form-group"><label for="p-phone">Phone</label><input type="tel" id="p-phone" name="phone" class="form-control"></div>
        </div>
        <div class="form-group"><label for="p-notes">Tell us about your network</label><textarea id="p-notes" name="notes" class="form-control" placeholder="e.g. HR consultant; I know the people leaders at 40+ Atlanta companies"></textarea></div>
        <button type="submit" class="btn btn-primary btn-lg btn-block">Apply to be a Partner →</button>
        <div class="alert alert-success">✓ Application received. We'll be in touch within one business day.</div>
      </form>
    </div>
  </div>
</section>
'''

PAGES = [
    ("index.html", "Virtual Recruiters &amp; Recruiter Staffing | GetRecruiters Group",
     "Rent a dedicated virtual recruiter or hire recruiters for your team — temp, temp-to-perm, or direct hire. Data centers, trades, healthcare, public accounting, financial services, and more.",
     HOME, faq_schema(), HOME_HEAD),
    ("virtual-recruiters.html", "Dedicated Virtual Recruiters | GetRecruiters Group",
     "A dedicated recruiter who works your openings as part of your team — sourcing, screening, and scheduling — without adding headcount.",
     VIRTUAL, None, ""),
    ("hire-recruiters.html", "Hire Recruiters: Temp, Temp-to-Perm &amp; Direct Hire | GetRecruiters Group",
     "Hire recruiters, sourcers, talent acquisition leaders, and HR pros as temp, temp-to-perm, or direct hire.",
     HIRE, None, ""),
    ("about.html", "About | GetRecruiters Group, a Division of NorthPoint",
     "GetRecruiters Group, a division of NorthPoint Search Group, puts experienced recruiters to work for companies that are hiring.",
     ABOUT, None, ""),
    ("request-talent.html", "Get a Recruiter | GetRecruiters Group",
     "Tell us what you're hiring for and we'll match you with a virtual recruiter or start the search for a recruiter to join your team.",
     REQUEST, None, ""),
    ("contact.html", "Contact | GetRecruiters Group",
     "Call 404-250-0790 or send a message. Virtual recruiters and recruiter staffing from GetRecruiters Group.",
     CONTACT, None, ""),
    ("partners.html", "Partner Program | Refer &amp; Earn | GetRecruiters Group",
     "Refer a company that needs recruiting help — earn 10% on direct hire placements and 25% of temp net spread.",
     PARTNERS, None, ""),
]

if __name__ == "__main__":
    for file, title, desc, body, schema, extra in PAGES:
        html = head(file, title, desc, schema, extra) + NAV + body + FOOTER
        (OUT / file).write_text(fill(html), encoding="utf-8")
        print("wrote", file)
