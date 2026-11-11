# Prime.Health

**Know your numbers. Live in your prime.** A free, evidence-based health-numbers platform:
26 calculators, the 3-minute Prime Score, 13 plain-language guides, a My Numbers dashboard,
an auto-updating Health Pulse news desk and video library, plus lead generation, support/donations,
a monthly challenge with prizes, careers and advertising pages.

Static site. 100% compatible with GitHub Pages (free plan, `main` branch, root folder).

## How it is built
```
build/               Python generator (no dependencies): layout, pages, tools, legal
content/guides/      Guide articles (HTML fragments with a META header)
assets/css, js       Styles, site script (forms, ads, search, theme), calculators, Prime Score
data/                feeds.json (sources to pull), news.json + videos.json (auto-refreshed)
scripts/             update_feeds.py (RSS + YouTube feeds, no API keys)
.github/workflows/   build.yml: builds the HTML, refreshes news/videos daily, commits to main
```
Every push to `main` that touches sources, and a daily schedule, runs the workflow, which regenerates
all HTML pages, `sitemap.xml` and `search-index.json` and commits them back to `main`.

Run locally: `python3 scripts/update_feeds.py` (optional) then `python3 build/build.py`, then
`python3 -m http.server` and open http://localhost:8000.

## Publish on GitHub Pages
Repo → Settings → Pages → Source: **Deploy from a branch** → Branch `main`, folder `/ (root)` → Save.
Live at https://webworksa1.github.io/prime.health/ within about a minute.

## Custom domain (prime.health)
1. DNS at the registrar: A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
   `185.199.111.153`; AAAA optional; CNAME `www` → `webworksa1.github.io`.
2. Repo → Settings → Pages → Custom domain: `prime.health` → Save → tick **Enforce HTTPS**.
3. Google Search Console: add `prime.health`, submit `https://prime.health/sitemap.xml`.
4. Apply to AdSense with `prime.health` (AdSense does not accept github.io sub-paths).

## Settings (assets/js/main.js → CONFIG)
- `adSlots`: paste AdSense ad-unit slot IDs after approval. Auto ads work without them;
  manual slots stay hidden until filled.
- `payLinks`: paste Stripe Payment Link / PayPal / Buy Me a Coffee / Ko-fi URLs to enable one-click
  donations. Until then, the Support page collects pledges by form.
- `formAlias`: optional FormSubmit alias (see below).

## Forms (lead generation, contact, newsletter, pledges, contest, careers, advertising)
All forms post through FormSubmit to the site inbox. The inbox address is stored XOR-encoded in
`main.js`; it is never written in plain text anywhere on the site or in this repo.
1. After the site is live, submit any form once. FormSubmit emails a one-time **Activate** link to
   the inbox. Click it. (That first submission is used for activation only.)
2. Optional: FormSubmit then offers a random alias string. Paste it into `CONFIG.formAlias` to stop
   using the encoded address at all.

## AdSense checklist
- Publisher ID `ca-pub-6620975821265271` is in every page head (except the 404 page) and in `ads.txt`.
- Privacy, cookie, terms, medical disclaimer, editorial policy, about and contact pages are live.
- In AdSense → Privacy & messaging, publish the GDPR (EEA/UK/CH) consent message: it is Google's
  certified CMP and is required for European traffic.

See `BUILD-PROMPT.md` for the phase-wise build prompt and `RESEARCH.md` for the 38-site research.

© 2026 Prime.Health. Independent website; see `trademark.html` for the trademark and copyright disclosure.
