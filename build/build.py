#!/usr/bin/env python3
"""Build every Prime.Health page. Usage: python3 build/build.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import layout as L  # noqa: E402
import tools_pages  # noqa: E402
import guides  # noqa: E402
import pages  # noqa: E402
import legal  # noqa: E402


def load_json(rel, default):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def main():
    news = load_json("data/news.json", {"updated": "", "items": []})
    videos = load_json("data/videos.json", {"updated": "", "items": [], "channels": []})
    feeds = load_json("data/feeds.json", {"youtube": []})
    guide_list = guides.load(os.path.join(ROOT, "content", "guides"))
    ctx = {"news": news, "videos": videos, "feeds": feeds, "guides": guide_list,
           "tools": tools_pages.TOOLS, "cats": tools_pages.CATS}

    all_pages = []
    all_pages += pages.build(ctx)
    all_pages += tools_pages.build(ctx)
    all_pages += guides.build(ctx)
    all_pages += legal.build(ctx)

    sitemap, search = [], []
    for pg in all_pages:
        html = L.render(pg) if not pg.get("raw") else pg["raw"]
        out = os.path.join(ROOT, pg["path"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        if pg.get("sitemap", True):
            sitemap.append((L.canonical(pg["path"]), pg.get("lastmod", "2026-11-11"), pg.get("priority", "0.6")))
        if pg.get("search", True):
            search.append({"t": pg.get("search_title", pg["title"]), "u": pg["path"].replace("index.html", ""),
                           "d": pg["desc"], "k": pg.get("kind", "Page")})

    urls = "\n".join(f"  <url><loc>{u}</loc><lastmod>{m}</lastmod><priority>{pr}</priority></url>"
                     for u, m, pr in sitemap)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n")
    with open(os.path.join(ROOT, "search-index.json"), "w", encoding="utf-8") as f:
        json.dump(search, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Built {len(all_pages)} pages, {len(sitemap)} sitemap URLs.")


if __name__ == "__main__":
    main()
