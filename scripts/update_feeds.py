#!/usr/bin/env python3
"""Refresh data/news.json and data/videos.json from public RSS/Atom feeds.

Standard library only. Stores titles, links, sources and dates (never article text).
A source that fails keeps its previous items, so one outage never empties a page.
"""
import datetime
import email.utils
import html
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (compatible; PrimeHealthBot/1.0; +https://prime.health/)"
NOW = datetime.datetime.now(datetime.timezone.utc)


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, text/html;q=0.8, */*;q=0.5"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def clean(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def parse_date(s):
    s = (s or "").strip()
    if not s:
        return ""
    for fn in (lambda x: email.utils.parsedate_to_datetime(x),
               lambda x: datetime.datetime.fromisoformat(x.replace("Z", "+00:00"))):
        try:
            d = fn(s)
            if d.tzinfo is None:
                d = d.replace(tzinfo=datetime.timezone.utc)
            return d.astimezone(datetime.timezone.utc).isoformat()
        except Exception:
            continue
    return ""


def local(tag):
    return tag.rsplit("}", 1)[-1]


def parse_feed(data):
    root = ET.fromstring(data)
    out = []
    for el in root.iter():
        if local(el.tag) not in ("item", "entry"):
            continue
        d = {}
        for ch in el:
            n = local(ch.tag)
            if n == "title":
                d["title"] = clean(ch.text)
            elif n == "link":
                href = ch.get("href")
                if href and ch.get("rel") in (None, "alternate"):
                    d.setdefault("link", href)
                elif (ch.text or "").strip():
                    d.setdefault("link", ch.text.strip())
            elif n in ("pubDate", "published", "date", "updated") and not d.get("date"):
                d["date"] = parse_date(ch.text)
            elif n == "videoId":
                d["vid"] = (ch.text or "").strip()
        if d.get("title") and (d.get("link") or d.get("vid")):
            out.append(d)
    return out


def load(rel, default):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save(rel, obj):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def recent(d, days):
    if not d:
        return True
    try:
        return (NOW - datetime.datetime.fromisoformat(d)).days <= days
    except Exception:
        return True


def update_news(cfg):
    old = load("data/news.json", {"items": []}).get("items", [])
    items, ok = [], []
    for src in cfg.get("news", []):
        try:
            got = [i for i in parse_feed(fetch(src["url"])) if len(i["title"]) >= 15 and i.get("link", "").startswith("http")]
            got = [i for i in got if recent(i.get("date"), 45)][:10]
            for i in got:
                items.append({"title": i["title"][:220], "link": i["link"], "source": src["name"], "date": i.get("date", "")})
            ok.append(src["name"])
            print(f"news ok   {src['name']}: {len(got)}")
        except Exception as e:  # keep previous items for this source
            items += [i for i in old if i.get("source") == src["name"]]
            print(f"news FAIL {src['name']}: {e}")
    seen, uniq = set(), []
    for i in sorted(items, key=lambda x: x.get("date", ""), reverse=True):
        k = (i["link"], i["title"].lower())
        if k in seen or i["title"].lower() in {u["title"].lower() for u in uniq}:
            continue
        seen.add(k)
        uniq.append(i)
    if uniq:
        save("data/news.json", {"updated": NOW.isoformat(), "sources_ok": ok, "items": uniq[:60]})


def resolve_channel(handle):
    page = fetch(f"https://www.youtube.com/@{handle}").decode("utf-8", "ignore")
    for pat in (r'<link rel="canonical" href="https://www\.youtube\.com/channel/(UC[\w-]{22})"',
                r'"externalId":"(UC[\w-]{22})"', r'"channelId":"(UC[\w-]{22})"'):
        m = re.search(pat, page)
        if m:
            return m.group(1)
    raise ValueError("channel id not found")


def update_videos(cfg):
    prev = load("data/videos.json", {"items": [], "channels": []})
    known = {c.get("handle"): c.get("id") for c in prev.get("channels", []) if c.get("id")}
    items, chans = [], []
    for c in cfg.get("youtube", []):
        cid = known.get(c["handle"]) or c.get("id") or ""
        got = None
        for attempt in range(2):
            try:
                if not cid:
                    cid = resolve_channel(c["handle"])
                got = parse_feed(fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"))
                break
            except Exception as e:
                print(f"video retry {c['handle']} ({cid}): {e}")
                cid = ""
        if got is None:
            items += [i for i in prev.get("items", []) if i.get("handle") == c["handle"]]
            chans.append({k: c.get(k, "") for k in ("handle", "name", "topic")} | {"id": known.get(c["handle"], "")})
            print(f"video FAIL {c['handle']}")
            continue
        n = 0
        for v in got:
            if "/shorts/" in v.get("link", "") or not v.get("vid"):
                continue
            items.append({"id": v["vid"], "title": v["title"][:160], "channel": c["name"], "handle": c["handle"], "topic": c.get("topic", ""), "date": v.get("date", "")})
            n += 1
            if n >= 3:
                break
        chans.append({"handle": c["handle"], "name": c["name"], "topic": c.get("topic", ""), "id": cid})
        print(f"video ok   {c['handle']}: {n}")
    items.sort(key=lambda x: x.get("date", ""), reverse=True)
    if items:
        save("data/videos.json", {"updated": NOW.isoformat(), "channels": chans, "items": items[:36]})


def main():
    cfg = load("data/feeds.json", {})
    update_news(cfg)
    update_videos(cfg)


if __name__ == "__main__":
    main()
