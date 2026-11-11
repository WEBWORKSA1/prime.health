"""Load guide fragments from content/guides and render guide pages + index."""
import datetime
import json
import os
import re

import layout as L
from tools_pages import BY, faq_html, faq_schema, sources_html, byline


def load(dirpath):
    out = []
    if not os.path.isdir(dirpath):
        return out
    for fn in sorted(os.listdir(dirpath)):
        if not fn.endswith(".html"):
            continue
        with open(os.path.join(dirpath, fn), encoding="utf-8") as f:
            raw = f.read()
        m = re.match(r"\s*<!--META\s*(\{.*?\})\s*-->", raw, re.S)
        if not m:
            continue
        meta = json.loads(m.group(1))
        meta["body"] = raw[m.end():].strip()
        meta.setdefault("slug", fn[:-5])
        out.append(meta)
    out.sort(key=lambda g: g.get("order", 99))
    return out


def nice_date(s):
    try:
        return datetime.date.fromisoformat(s).strftime("%B %-d, %Y")
    except Exception:
        return s


def guide_page(g, ctx):
    p = "../"
    body = g["body"]
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    toc = "".join(f'<li><a href="#{i}">{re.sub("<[^>]+>", "", t)}</a></li>' for i, t in heads)
    toc += '<li><a href="#faq">Questions people ask</a></li><li><a href="#sources">Sources</a></li>'
    parts = re.split(r'(?=<h2 id=)', body)
    if len(parts) > 3:
        parts.insert(3, L.ad("inArticle"))
    body = "".join(parts)
    take = "".join(f"<li>{t}</li>" for t in g.get("takeaways", []))
    srcs = [tuple(s) for s in g.get("sources", [])]
    tools = "".join(f'<a class="btn btn-ghost btn-sm" href="{p}tools/{s}.html">{BY[s]["short"]}</a> ' for s in g.get("tools", []) if s in BY)
    faq = [tuple(x) for x in g.get("faq", [])]
    main = f'''<div class="wrap">
<header class="page-head"><h1>{g["title"]}</h1><p class="lede">{g["desc"]}</p>
<div class="meta-row"><span>Updated {nice_date(g.get("date", ""))}</span><span>{g.get("read", 6)} min read</span><span>{len(srcs)} sources</span></div></header>
<div class="article-layout">
<div>
<aside class="takeaways" aria-label="Key takeaways"><h2>Key takeaways</h2><ul>{take}</ul></aside>
<article class="prose" data-article>
{body}
<h2 id="faq">Questions people ask</h2>{faq_html(faq)}
<h2 id="sources">Sources</h2>{sources_html(srcs)}
</article>
{byline(p)}
{f'<section class="box" style="max-width:var(--measure)"><h2 style="font-size:1.4rem">Check your numbers</h2><p>{tools}</p></section>' if tools else ""}
</div>
<aside class="toc-aside"><div class="side-sticky side"><nav class="toc side-box" aria-label="On this page"><h2>On this page</h2><ol>{toc}</ol></nav>{L.ad("sidebar")}</div></aside>
</div>
{L.lead_box(p, "guide-" + g["slug"])}
</div>'''
    url = L.canonical(f"guides/{g['slug']}.html")
    schema = [{"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
               "datePublished": g.get("date"), "dateModified": g.get("date"), "mainEntityOfPage": url,
               "author": {"@type": "Organization", "name": "Prime.Health editorial team", "url": L.SITE_URL + "/about.html"},
               "publisher": {"@type": "Organization", "name": L.NAME, "logo": {"@type": "ImageObject", "url": L.SITE_URL + "/favicon.svg"}},
               "image": L.SITE_URL + "/assets/img/og.png"}]
    if faq:
        schema.append(faq_schema(faq))
    return {"path": f"guides/{g['slug']}.html", "title": g.get("seo", g["title"]), "desc": g["desc"], "main": main,
            "active": "guides", "crumbs": [("Guides", "guides/"), (g.get("short", g["title"]), "")], "schema": schema,
            "og_type": "article", "kind": "Guide", "search_title": g["title"], "lastmod": g.get("date", "2026-11-11"), "priority": "0.7"}


def index_page(ctx):
    p = "../"
    gl = ctx["guides"]
    items = "".join(f'<li><a href="{g["slug"]}.html"><h3>{g["title"]}</h3><p>{g["desc"]}</p><p class="post-meta">{g.get("read", 6)} min read</p></a></li>' for g in gl)
    main = f'''<div class="wrap">
<header class="page-head"><h1>Guides to the numbers that matter</h1>
<p class="lede">Plain-language explainers built on guidelines and systematic reviews. Each one ends with the calculators that put it into practice and the sources behind every claim.</p></header>
<ul class="post-list">{items}</ul>
{L.ad("top")}
{L.lead_box(p, "guides-index")}
</div>'''
    return {"path": "guides/index.html", "title": "Health Guides: Evidence-Based, Plain-Language", "desc": "Evidence-based guides to blood pressure, metabolic health, VO2 max, strength, protein, sleep, steps, screenings, nutrition, stress and alcohol.",
            "main": main, "active": "guides", "crumbs": [("Guides", "")], "kind": "Hub", "priority": "0.8"}


def build(ctx):
    return [index_page(ctx)] + [guide_page(g, ctx) for g in ctx["guides"]]
