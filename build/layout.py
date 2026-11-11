"""Shared layout for every Prime.Health page. Standard library only."""
import html as _html
import json

SITE_URL = "https://prime.health"
NAME = "Prime.Health"
TAGLINE = "Know your numbers. Live in your prime."
ADS_TAG = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'
           '?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>')
CONTACT_URL = "https://web.works/contact"
BANNER = ("Contact, if you are interested in this website / domain name / "
          "Sponsorship / Advertisement / Partnership")
FONTS = ("https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700"
         "&family=Public+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap")
V = "3"  # asset version for cache busting

NAV = [
    ("tools/", "Tools", "tools"),
    ("prime-score.html", "Prime Score", "score"),
    ("guides/", "Guides", "guides"),
    ("videos.html", "Videos", "videos"),
    ("pulse.html", "Health Pulse", "pulse"),
    ("challenge.html", "Challenge", "challenge"),
    ("support.html", "Support", "support"),
]

LOGO = ('<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="7"/>'
        '<path d="M3 18h6.5l2.5-6 4 12 3.5-15 3 9h6.5"/></svg>')


def esc(s):
    return _html.escape(str(s), quote=True)


def prefix(path):
    return "../" * path.count("/")


def home_href(p):
    return p or "./"


def canonical(path):
    if path == "index.html":
        return SITE_URL + "/"
    if path.endswith("/index.html"):
        return SITE_URL + "/" + path[: -len("index.html")]
    return SITE_URL + "/" + path


def ad(slot, fmt="auto"):
    """Manual ad container. Stays hidden until an ad-unit ID is set in CONFIG.adSlots."""
    return f'<div class="ad-slot" data-ad="{slot}" data-format="{fmt}"><span class="ad-label">Advertisement</span></div>'


def crumbs_html(p, crumbs):
    items = [f'<li><a href="{home_href(p)}">Home</a></li>']
    for i, (label, href) in enumerate(crumbs):
        if i == len(crumbs) - 1 or not href:
            items.append(f'<li aria-current="page">{esc(label)}</li>')
        else:
            items.append(f'<li><a href="{p}{href}">{esc(label)}</a></li>')
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(items) + "</ol></nav>"


def crumbs_schema(path, crumbs):
    elems = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"}]
    for i, (label, href) in enumerate(crumbs, start=2):
        url = canonical(href + "index.html" if href and href.endswith("/") else (href or path))
        elems.append({"@type": "ListItem", "position": i, "name": label, "item": url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elems}


ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": NAME,
    "url": SITE_URL + "/",
    "logo": SITE_URL + "/favicon.svg",
    "description": "Free, evidence-based health calculators, guides and the Prime Score.",
}


def newsletter_form(source):
    return f'''<form class="news-form" data-form="Newsletter signup" data-success="You're on the list. The next Prime Numbers email is on its way." novalidate>
  <label class="sr" for="nl-{source}">Email address</label>
  <input id="nl-{source}" name="email" type="email" autocomplete="email" placeholder="you@example.com" required>
  <input type="hidden" name="list" value="The Prime Numbers weekly"><input type="hidden" name="source" value="{source}">
  <input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
  <button class="btn btn-primary" type="submit">Subscribe</button>
</form>'''


def lead_box(p, source, heading="Get your free 30-day Prime Plan",
             text="Tell us your goal and we'll email a 30-day plan built around your numbers: weekly targets, a simple training split and the checks worth booking."):
    return f'''<section class="lead-box" aria-labelledby="lb-{source}">
  <div class="lead-copy"><h2 id="lb-{source}">{heading}</h2><p>{text}</p>
  <p class="fine">Free. One email a week. Unsubscribe any time. <a href="{p}privacy-policy.html">Privacy</a></p></div>
  <form class="lead-form" data-form="Quick plan request" data-success="Done. Check your inbox for your Prime Plan within 24 hours. Want a sharper plan? &lt;a href=&quot;{p}get-your-plan.html&quot;&gt;Answer 4 quick questions&lt;/a&gt;." novalidate>
    <label for="lg-{source}">Main goal</label>
    <select id="lg-{source}" name="goal" required>
      <option value="">Choose one</option><option>Lose fat</option><option>Build strength and muscle</option><option>Sleep better</option>
      <option>Lower blood pressure or blood sugar</option><option>More energy</option><option>A full healthspan check-up</option>
    </select>
    <label for="le-{source}">Email</label>
    <input id="le-{source}" name="email" type="email" autocomplete="email" placeholder="you@example.com" required>
    <label class="check"><input type="checkbox" name="consent" value="Agreed to privacy policy" required> I agree to the privacy policy.</label>
    <input type="hidden" name="source" value="{source}"><input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
    <button class="btn btn-primary btn-block" type="submit">Email me my plan</button>
  </form>
</section>'''


def header(p, active):
    items = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ""
        items.append(f'<li><a href="{p}{href}"{cur}>{label}</a></li>')
    nav = "".join(items)
    return f'''<a class="skip" href="#main">Skip to content</a>
<a class="topbar" href="{CONTACT_URL}" target="_blank" rel="noopener">{BANNER}</a>
<header class="site-header">
  <div class="wrap hdr">
    <a class="logo" href="{home_href(p)}" aria-label="Prime.Health home">{LOGO}<span class="logo-word">Prime<b>.</b>Health</span></a>
    <nav class="main-nav" id="mainNav" aria-label="Main"><ul>{nav}</ul>
      <a class="btn btn-primary nav-cta-m" href="{p}get-your-plan.html">Get my free plan</a></nav>
    <div class="hdr-actions">
      <button class="icon-btn" id="searchOpen" type="button" aria-label="Search the site (press /)"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></button>
      <button class="icon-btn" id="themeToggle" type="button" aria-label="Switch light or dark theme"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>
      <a class="btn btn-primary nav-cta" href="{p}get-your-plan.html">Get my free plan</a>
      <button class="icon-btn menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="mainNav" aria-label="Open menu"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
</header>'''


def footer(p):
    def col(title, links):
        lis = "".join(f'<li><a href="{p}{h}">{t}</a></li>' for h, t in links)
        return f'<div class="fcol"><h2>{title}</h2><ul>{lis}</ul></div>'
    cols = "".join([
        col("Popular tools", [("tools/bmi.html", "BMI & BMI Prime"), ("tools/calories.html", "Calorie calculator"),
                              ("tools/blood-pressure.html", "Blood pressure checker"), ("tools/heart-rate-zones.html", "Heart rate zones"),
                              ("tools/due-date.html", "Due date calculator"), ("tools/", "All 26 tools")]),
        col("Learn", [("guides/prime-numbers.html", "Your 8 Prime Numbers"), ("guides/", "All guides"), ("prime-score.html", "Prime Score"),
                      ("pulse.html", "Health Pulse"), ("videos.html", "Videos"), ("my-numbers.html", "My Numbers")]),
        col("Get involved", [("get-your-plan.html", "Free 30-day plan"), ("challenge.html", "Prime 30 Challenge"), ("support.html", "Support us"),
                             ("advertise.html", "Advertise & partner"), ("careers.html", "Careers")]),
        col("Company", [("about.html", "About"), ("editorial-policy.html", "Editorial policy"), ("contact.html", "Contact"),
                        ("trademark.html", "Trademark & copyright"), ("accessibility.html", "Accessibility")]),
        col("Legal", [("privacy-policy.html", "Privacy policy"), ("cookie-policy.html", "Cookie policy"), ("terms.html", "Terms of use"),
                      ("medical-disclaimer.html", "Medical disclaimer")]),
    ])
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="f-top">
      <div class="f-brand"><a class="logo" href="{home_href(p)}">{LOGO}<span class="logo-word">Prime<b>.</b>Health</span></a>
        <p>{TAGLINE} Free calculators and plain-language guides for the numbers that shape your healthspan.</p></div>
      <div class="f-news"><h2>The Prime Numbers, weekly</h2><p>One number, one action, one study worth knowing. Every Monday.</p>{newsletter_form("footer")}</div>
    </div>
    <div class="f-cols">{cols}</div>
    <div class="f-legal">
      <p><strong>Medical disclaimer:</strong> Prime.Health provides general information for education. It is not medical advice, diagnosis or treatment. Always talk with a qualified health professional about your health. In an emergency, call your local emergency number.</p>
      <p><strong>Trademark notice:</strong> Prime.Health is an independent website. It is not affiliated with, sponsored or endorsed by any company, clinic or product using the names “Prime Health”, “PrimeHealth” or “Prime Healthcare”. Third-party names and marks belong to their owners. <a href="{p}trademark.html">Full disclosure</a></p>
      <p>© <span data-year>2026</span> Prime.Health. All rights reserved. <a href="{CONTACT_URL}" target="_blank" rel="noopener">Buy, sponsor or partner with this website</a></p>
    </div>
  </div>
</footer>
<dialog class="search-dialog" id="searchDialog" aria-label="Search Prime.Health">
  <form method="dialog" class="search-form" role="search"><label class="sr" for="searchInput">Search</label>
    <input id="searchInput" type="search" placeholder="Search tools and guides, e.g. blood pressure" autocomplete="off">
    <button class="icon-btn" value="close" aria-label="Close search"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button></form>
  <ul class="search-results" id="searchResults"></ul>
</dialog>'''


def render(page):
    path = page["path"]
    p = prefix(path)
    title = page["title"]
    full_title = title if NAME in title else f"{title} | {NAME}"
    desc = page["desc"]
    canon = canonical(path)
    ads = page.get("ads", True)
    robots = page.get("robots", "index,follow,max-image-preview:large")
    schema = [ORG]
    if page.get("crumbs"):
        schema.append(crumbs_schema(path, page["crumbs"]))
    schema += page.get("schema", [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    scripts = "".join(f'<script src="{p}assets/js/{s}?v={V}" defer></script>' for s in page.get("scripts", ()))
    crumbs = crumbs_html(p, page["crumbs"]) if page.get("crumbs") else ""
    og_img = SITE_URL + "/assets/img/og.png"
    body_attrs = f' class="{page["body_class"]}"' if page.get("body_class") else ""
    slidein = ' data-slidein="1"' if page.get("slidein", True) else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{robots}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="{page.get("og_type", "website")}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#10333A">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{p}assets/img/icon-180.png">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{p}assets/css/style.css?v={V}">
<script>try{{var t=localStorage.getItem('ph:theme');if(t)document.documentElement.dataset.theme=JSON.parse(t)}}catch(e){{}}</script>
{ADS_TAG if ads else ""}
{ld}
{page.get("head_extra", "")}
</head>
<body{body_attrs} data-root="{p}"{slidein}>
{header(p, page.get("active", ""))}
<main id="main">
{('<div class="wrap">' + crumbs + '</div>') if crumbs else ""}
{page["main"]}
</main>
{footer(p)}
<script src="{p}assets/js/main.js?v={V}" defer></script>
{scripts}
</body>
</html>
'''


def rbar_static(lo, hi, mn, mx, label):
    """A static reference bar showing a target zone (used in lab-report rows)."""
    left = (lo - mn) / (mx - mn) * 100
    width = (hi - lo) / (mx - mn) * 100
    return (f'<div class="zone" role="img" aria-label="{esc(label)}"><span class="zone-fill" '
            f'style="left:{left:.1f}%;width:{width:.1f}%"></span></div>')
