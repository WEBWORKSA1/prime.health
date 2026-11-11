"""Render the tools index and one page per calculator."""
import layout as L
from tools_a import TOOLS_A
from tools_b import TOOLS_B

CATS = [
    ("body", "Body composition", "Weight, waist and body fat"),
    ("heart", "Heart & metabolic", "Blood pressure, blood sugar and cholesterol"),
    ("fitness", "Fitness", "Heart rate, VO₂ max, strength and running"),
    ("nutrition", "Nutrition", "Calories, macros, protein, water and caffeine"),
    ("sleep", "Sleep", "Sleep cycles and sleep debt"),
    ("women", "Women’s health", "Pregnancy dating and cycle tracking"),
    ("prevention", "Prevention", "Screenings due at your age"),
]
TOOLS = TOOLS_A + TOOLS_B
BY = {t["slug"]: t for t in TOOLS}
UNIT_TYPES = {"height", "weight", "len", "dist", "load"}
UPDATED = "2026-11-11"


def _num(fid, name, ph, unit, mn="", mx="", step="any", aria="", value=""):
    idattr = f' id="{fid}"' if fid else ""
    a = f' aria-label="{L.esc(aria)}"' if aria else ""
    mm = (f' min="{mn}"' if mn != "" else "") + (f' max="{mx}"' if mx != "" else "")
    val = f' value="{value}"' if value != "" else ""
    u = f"<span>{unit}</span>" if unit else ""
    return (f'<div class="inp"><input{idattr} name="{name}" type="number" inputmode="decimal" step="{step}"{mm}'
            f' placeholder="{ph}"{val}{a}>{u}</div>')


def field(f):
    i, t, lab = f["id"], f["type"], f["label"]
    fid = "f-" + i
    wide = ' style="grid-column:1/-1"' if f.get("wide") else ""
    show = f' data-show-if="{f["show"]}"' if f.get("show") else ""
    opt = ' <span class="fine">(optional)</span>' if f.get("opt") else ""
    hlp = f'<p class="help">{f["help"]}</p>' if f.get("help") else ""
    head = f'<label for="{fid}">{lab}{opt}</label>'
    if t == "height":
        body = (f'<div class="u-metric">{_num(fid, i + "_cm", f.get("ph", "170"), "cm", 50, 250)}</div>'
                f'<div class="u-imperial inp-row">{_num("", i + "_ft", "5", "ft", 1, 8, 1, lab + " in feet")}'
                f'{_num("", i + "_in", "7", "in", 0, 11.9, "any", lab + " in inches")}</div>')
    elif t == "weight":
        body = (f'<div class="u-metric">{_num(fid, i + "_kg", f.get("ph", "70"), "kg", 20, 350)}</div>'
                f'<div class="u-imperial">{_num("", i + "_lb", f.get("ph_i", "155"), "lb", 45, 770, "any", lab + " in pounds")}</div>')
    elif t == "len":
        body = (f'<div class="u-metric">{_num(fid, i + "_cm", f.get("ph", "85"), "cm", 10, 250)}</div>'
                f'<div class="u-imperial">{_num("", i + "_in", f.get("ph_i", "33"), "in", 4, 100, "any", lab + " in inches")}</div>')
    elif t == "dist":
        body = (f'<div class="u-metric">{_num(fid, i + "_km", f.get("ph", "2.4"), "km", 0.1, 500)}</div>'
                f'<div class="u-imperial">{_num("", i + "_mi", f.get("ph_i", "1.5"), "mi", 0.1, 300, "any", lab + " in miles")}</div>')
    elif t == "load":
        body = (f'<div class="inp"><input id="{fid}" name="{i}" type="number" inputmode="decimal" step="any" min="1" placeholder="{f.get("ph", "80")}">'
                '<span><span class="u-metric">kg</span><span class="u-imperial">lb</span></span></div>')
    elif t == "num":
        body = _num(fid, i, f.get("ph", ""), f.get("unit", ""), f.get("min", ""), f.get("max", ""), f.get("step", "any"), value=f.get("default", ""))
    elif t == "select":
        opts = "".join(f'<option value="{v}"{" selected" if str(v) == str(f.get("default", "")) else ""}>{L.esc(x)}</option>' for v, x in f["options"])
        body = f'<select id="{fid}" name="{i}">{opts}</select>'
    elif t == "radio":
        opts = "".join(f'<label><input type="radio" name="{i}" value="{v}"{" checked" if str(v) == str(f.get("default", "")) else ""}><span>{x}</span></label>' for v, x in f["options"])
        return (f'<fieldset class="field" data-field="{i}" data-type="radio"{show}{wide}><legend>{lab}{opt}</legend>'
                f'<div class="pills">{opts}</div>{hlp}</fieldset>')
    elif t == "check":
        return (f'<div class="field" data-field="{i}" data-type="check"{show}{wide}><label class="check"><input type="checkbox" name="{i}"> {lab}</label>{hlp}</div>')
    elif t in ("date", "time"):
        val = f' value="{f["default"]}"' if f.get("default") else ""
        body = f'<input id="{fid}" name="{i}" type="{t}"{val}>'
    else:
        raise ValueError(t)
    return f'<div class="field" data-field="{i}" data-type="{t}"{show}{wide}>{head}{body}{hlp}</div>'


def unit_toggle():
    return ('<div class="seg-toggle unit-toggle" role="group" aria-label="Units">'
            '<button type="button" data-units="metric" aria-pressed="true">Metric</button>'
            '<button type="button" data-units="imperial" aria-pressed="false">US units</button></div>')


def calc_form(t, heading=None, compact=False):
    has_units = any(f["type"] in UNIT_TYPES for f in t["fields"])
    fields = "".join(field(f) for f in t["fields"])
    c = " data-compact" if compact else ""
    return (f'<form class="calc" data-tool="{t["slug"]}"{c} novalidate>'
            f'<div class="calc-top"><h2>{heading or t["short"]}</h2>{unit_toggle() if has_units else ""}</div>'
            f'<div class="fields">{fields}</div>'
            f'<div class="calc-actions"><button class="btn btn-primary" type="submit">{t.get("cta", "Calculate")}</button>'
            f'{"" if compact else "<button class=\"btn btn-ghost\" type=\"reset\">Clear</button>"}</div>'
            f'<div class="result" aria-live="polite" tabindex="-1" hidden></div></form>')


def byline(p):
    return (f'<div class="byline">{L.LOGO}<div><b>Prime.Health editorial team</b><br>Built from the formulas and guidelines listed under '
            f'Sources and checked against them before publishing. <a href="{p}editorial-policy.html">How we research</a>. '
            f'General information only, not a substitute for professional advice. <a href="{p}medical-disclaimer.html">Medical disclaimer</a>.</div></div>')


def sources_html(srcs):
    items = []
    for s in srcs:
        label, url = s if isinstance(s, tuple) else (s, "")
        items.append(f'<li><a href="{url}" target="_blank" rel="noopener">{label}</a></li>' if url else f"<li>{label}</li>")
    return '<div class="sources"><ol>' + "".join(items) + "</ol></div>"


def faq_html(faq):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq) + "</div>"


def faq_schema(faq):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]}


def tool_page(t, ctx):
    p = "../"
    gmap = {g["slug"]: g for g in ctx["guides"]}
    related = "".join(f'<li><a href="{p}tools/{s}.html">{BY[s]["name"]}</a></li>' for s in t.get("related", []) if s in BY)
    rguides = "".join(f'<li><a href="{p}guides/{s}.html">{gmap[s]["title"]}</a></li>' for s in t.get("guides", []) if s in gmap)
    side = f'''<aside class="side" aria-label="Related">
  <div class="side-box"><h2>Related tools</h2><ul>{related}</ul></div>
  {f'<div class="side-box"><h2>Read next</h2><ul>{rguides}</ul></div>' if rguides else ""}
  <div class="side-box"><h2>Your Prime Score</h2><p>Eight questions, three minutes, one number for your healthspan.</p><a class="btn btn-primary btn-block" href="{p}prime-score.html">Get my score</a></div>
  {L.ad("sidebar")}
</aside>'''
    main = f'''<div class="wrap">
<header class="page-head"><h1>{t["h1"]}</h1><p class="lede">{t["lede"]}</p>
<div class="meta-row"><span>Updated November 11, 2026</span><span>Free, no sign-up</span><span>Your entries stay on your device</span></div></header>
<div class="tool-layout">
<div class="tool-main">
<section class="panel calc-panel" aria-label="{L.esc(t["short"])}">{calc_form(t)}</section>
{L.ad("result")}
<article class="prose">
<h2 id="how">How it works</h2>{t["how"]}
<h2 id="reading">Reading your result</h2>{t["read"]}
<h2 id="limits">Limits to keep in mind</h2>{t["limits"]}
{L.ad("inArticle")}
<h2 id="faq">Questions people ask</h2>{faq_html(t["faq"])}
<h2 id="sources">Sources</h2>{sources_html(t["sources"])}
</article>
{byline(p)}
</div>
{side}
</div>
{L.lead_box(p, "tool-" + t["slug"])}
</div>'''
    schema = [{"@context": "https://schema.org", "@type": "WebApplication", "name": t["name"], "url": L.canonical(f"tools/{t['slug']}.html"),
               "applicationCategory": "HealthApplication", "operatingSystem": "Any", "description": t["desc"],
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
              faq_schema(t["faq"])]
    return {"path": f"tools/{t['slug']}.html", "title": t["title"], "desc": t["desc"], "main": main, "active": "tools",
            "crumbs": [("Tools", "tools/"), (t["short"], "")], "schema": schema, "scripts": ("tools.js",),
            "kind": "Tool", "search_title": t["name"], "lastmod": UPDATED, "priority": "0.8"}


def index_page(ctx):
    p = "../"
    groups = []
    for key, name, blurb in CATS:
        items = "".join(f'<li><a href="{t["slug"]}.html"><b>{t["name"]}</b><span>{t["blurb"]}</span></a></li>' for t in TOOLS if t["cat"] == key)
        groups.append(f'<section class="tool-group" id="{key}"><h2 class="h3" style="font-size:1.5rem">{name}</h2><p class="fine">{blurb}</p><ul>{items}</ul></section>')
    jump = "".join(f'<a class="btn btn-ghost btn-sm" href="#{k}">{n}</a>' for k, n, _ in CATS)
    main = f'''<div class="wrap">
<header class="page-head"><h1>{len(TOOLS)} free health calculators</h1>
<p class="lede">Every tool shows its formula, the guideline behind the ranges and what the number cannot tell you. Metric and US units. Nothing you type leaves your device.</p>
<div class="filter-row" style="gap:8px">{jump}</div></header>
<div class="tool-groups tool-index">{"".join(groups)}</div>
{L.ad("top")}
<section class="section-tight"><div class="score-band"><div><h2>Not sure where to start?</h2><p class="lede">The Prime Score rolls eight of these numbers into one 0–100 score and tells you which two changes would move it most.</p></div>
<div><a class="btn btn-signal" href="{p}prime-score.html">Take the 3-minute Prime Score</a> <a class="btn btn-ghost" href="{p}my-numbers.html">Open My Numbers</a></div></div></section>
{L.lead_box(p, "tools-index")}
</div>'''
    schema = [{"@context": "https://schema.org", "@type": "ItemList", "name": "Prime.Health calculators",
               "itemListElement": [{"@type": "ListItem", "position": n + 1, "url": L.canonical(f"tools/{t['slug']}.html"), "name": t["name"]} for n, t in enumerate(TOOLS)]}]
    return {"path": "tools/index.html", "title": "Free Health Calculators: BMI, Calories, Blood Pressure & More",
            "desc": f"{len(TOOLS)} free, evidence-based health calculators with formulas and sources: BMI Prime, TDEE, macros, blood pressure, A1C, heart-rate zones, VO2 max, sleep, due date and more.",
            "main": main, "active": "tools", "crumbs": [("Tools", "")], "schema": schema, "kind": "Hub", "priority": "0.9", "lastmod": UPDATED}


def build(ctx):
    return [index_page(ctx)] + [tool_page(t, ctx) for t in TOOLS]
