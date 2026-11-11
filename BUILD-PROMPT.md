# Prime.Health — Phase-wise Build Prompt

Use these prompts in order. Each phase is self-contained, builds on the previous one, and ends with a
concrete acceptance check. The finished site in this repo is the reference implementation.

---

## Phase 0 — Concept and positioning (decided)

**Idea:** Prime.Health is a free, evidence-based *health-numbers* platform. Tagline: **"Know your numbers.
Live in your prime."** It owns the eight measurable numbers that best predict healthspan (blood pressure,
A1C, non-HDL cholesterol, waist-to-height ratio, BMI Prime, VO2 max, sleep hours, daily steps) and gives
visitors a calculator, a target range and a plain-language guide for each one, plus a 3-minute
**Prime Score** that rolls them into one 0–100 number.

**Why this beats a generic health blog (the logic):**
1. A new domain cannot outrank Healthline, Mayo Clinic or Cleveland Clinic on condition articles
   ("diabetes symptoms"). Google weights YMYL authority heavily there.
2. Calculator queries (BMI, calorie, TDEE, macro, due date, ovulation, heart-rate zone, one-rep max) are
   evergreen, high-volume and ranked mostly on usefulness. Calculator.net and Omni Calculator built huge
   traffic this way.
3. Tools produce multi-page sessions (result → related tool → guide), which multiplies ad impressions.
4. Health and wellness AdSense RPM sits around $6–15 in tier-1 markets (2026 benchmarks), well above
   general lifestyle content.
5. A quiz funnel (Prime Score) is the proven lead engine of Noom, Levels, Precision Nutrition and
   mindbodygreen. Leads monetize through coaching, testing, telehealth and fitness partners.
6. Brand fit: "BMI Prime" is a real metric (BMI ÷ 25) and "your prime numbers" is a native hook.

**Revenue model (assumptions, month 12 target):** 100k sessions × 2.4 pages = 240k pageviews × $8 blended
RPM ≈ $1.9k/month AdSense. Lead revenue: 2–3% session-to-lead conversion = 2,000–3,000 opt-ins/month,
sold or rev-shared with vetted partners. Plus sponsorships (sponsored tool, newsletter, challenge prizes)
and donations. Bold path: turn the Prime Score into a pay-per-lead marketplace for preventive testing,
longevity clinics and coaches. Safe path: tools + AdSense + newsletter only.

**Audience:** adults 25–65, data-curious, wearable owners, people starting a health reset.

---

## Phase 1 — Research synthesis

Prompt: *"Study the 38 health sites in RESEARCH.md. Extract every feature worth adopting: tools,
quizzes, lead magnets and CTA wording, trust signals, monetization, content types and layout patterns.
Produce a feature matrix and a must-have list for Prime.Health."*

Must-haves extracted: calculator hub grouped by goal; per-tool explainer + FAQ + sources; quiz funnel
with a personalized result; free lead magnet ("30-day plan"); newsletter in footer and inline;
medical disclaimer + editorial policy + sources on every page; click-to-load video library;
auto-updated news desk; donation tiers with impact framing; contest with official rules; partner and
advertiser intake; careers/talent pool; dark mode; site search; privacy-first local storage.

---

## Phase 2 — Information architecture

Prompt: *"Create the sitemap and URL plan for a static site served from GitHub Pages (main branch,
root). All internal links must be relative so the site works at webworksa1.github.io/prime.health/
and at prime.health."*

```
/                       Home
/tools/                 26 calculators grouped: Body, Heart & metabolic, Fitness, Nutrition, Sleep,
                        Women's health, Prevention
/tools/<slug>.html      One page per calculator
/prime-score.html       8-pillar quiz → score, bars, actions, lead capture
/get-your-plan.html     Dedicated 5-step lead funnel (free 30-day Prime Plan + partner match)
/my-numbers.html        Local dashboard of saved results
/guides/ + 13 guides    Long-form, sourced
/videos.html            Auto-refreshed video library (YouTube RSS)
/pulse.html             Auto-refreshed Health Pulse headlines (RSS)
/challenge.html         Prime 30 Challenge (contest + prizes + rules + tracker)
/support.html           Donations, pledges, sponsorship tiers
/advertise.html         Advertising, sponsorship, partnerships, lead-partner program
/careers.html           Roles + talent pool application
/about, /contact, /editorial-policy, /medical-disclaimer, /privacy-policy, /cookie-policy,
/terms, /trademark, /accessibility, /404
/ads.txt /robots.txt /sitemap.xml /search-index.json /site.webmanifest
```

---

## Phase 3 — Design system

Prompt: *"Design a distinctive identity grounded in the subject: lab reports and ECG paper. No stock
photos, no cream-and-terracotta, no generic SaaS cards."*

- Palette: ink `#10333A` (text, primary buttons), paper `#FBFCFB`, panel `#FFFFFF`, rule `#D9E2E0`,
  ECG paper `#F7E1DA` with grid `#EEC3B6`, trace red `#D2334A` (brand signal only).
  Range semantics: below `#3B6FB6`, in range `#2E7D57`, borderline `#C98A12`, high `#C2412D`.
  Full dark theme.
- Type: **Barlow Condensed** (headlines and every numeric readout, tabular figures — reads like a
  vitals monitor) + **Public Sans** (body; the typeface of public-health design systems).
- Signature component: the **reference-range bar** from lab reports — coloured bands, a marker that
  slides to the visitor's value, the value printed on the marker.
- Hero: ECG-paper ground, one ECG trace that draws once on load (respects reduced motion), and a live
  BMI Prime quick check.
- Lists of tools and numbers are lab-report rows, not card grids. Small radii (4–6px), real hierarchy.
- Accessibility: skip link, visible focus, 4.5:1 contrast, labels on every input, aria-live results.

---

## Phase 4 — Templates and global chrome

Prompt: *"Write a dependency-free Python generator (build/) that renders every page from shared layout
functions. Every page gets the same head, top banner, header, footer and scripts."*

Requirements on **every** page:
- In `<head>`: `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>`
  (omit only on the 404 page; Google disallows ads on error pages).
- Top banner, first element in the body, linking to `https://web.works/contact`:
  "Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership".
- Unique title, meta description, canonical (`https://prime.health/...`), Open Graph, Twitter card,
  JSON-LD (Organization, WebSite, BreadcrumbList, MedicalWebPage/Article/FAQPage where relevant).
- Header: logo, nav, search ("/" shortcut), theme toggle, "Get my free plan" CTA, mobile drawer.
- Footer: newsletter form, link columns, medical disclaimer line, trademark line, auto year.
- Ad slots are empty containers that only render when an ad-unit ID is set in `CONFIG.adSlots`;
  never adjacent to buttons or form controls; labelled "Advertisement".

---

## Phase 5 — Calculator engine and 26 tools

Prompt: *"Build one calculator engine (assets/js/tools.js) with a global metric/imperial toggle,
validation, an aria-live result panel, range bars, stat lists, tables, Save to My Numbers, copy and
print. Then implement these tools, each on its own page with How it works (formula), Reading your
result, Limits, FAQ and Sources."*

Body: BMI + BMI Prime (standard and Asian cut-offs), body fat (US Navy), waist-to-height, waist-to-hip +
WHO waist bands, ideal weight (Devine/Robinson/Miller/Hamwi). Heart & metabolic: blood pressure (2025
ACC/AHA categories, averages up to 3 readings, severe-reading warning), A1C ↔ eAG (ADA ranges, IFCC),
cholesterol (non-HDL, ratios, LDL bands), metabolic syndrome check (harmonized 5 criteria, unit switch).
Fitness: heart-rate zones (Tanaka/220-age, Karvonen), VO2 max (Uth resting-HR and Cooper 12-minute),
one-rep max (Epley/Brzycki/Lombardi), running pace + Riegel race predictions, steps → distance/calories,
calories burned (MET). Nutrition: calories/TDEE (Mifflin-St Jeor), BMR (Mifflin, Harris-Benedict
revised, Katch-McArdle), macros, protein, water, caffeine (with bedtime carry-over). Sleep: sleep cycles,
sleep debt. Women's health: due date (LMP/conception, cycle-adjusted, milestones), ovulation (3 cycles).
Prevention: preventive screening planner (USPSTF A/B recommendations by age, sex and smoking history).

Acceptance: every formula unit-tested against a hand calculation; no result without valid inputs.

---

## Phase 6 — Prime Score and My Numbers

Prompt: *"Build an 8-question quiz (Move, Fuel, Smoke-free, Sleep, Weight, Blood pressure, Blood sugar,
Cholesterol) scored 0–100 per pillar using published Life's Essential 8-style thresholds (credit the
AHA framework, state no affiliation). Unknown labs are excluded from the average and flagged 'measure
it'. Show overall score, 8 bars, the two biggest wins with links, then an optional 'Email me my Prime
Plan' form carrying the scores. Save to My Numbers."*

My Numbers: localStorage dashboard of every saved result with date, target and link back; export as
JSON, clear all. Nothing leaves the device unless the visitor submits a form.

---

## Phase 7 — Content (AdSense-grade, YMYL-safe)

Prompt: *"Write 13 original guides (700–1,000 words each) in plain language, citing primary sources
(WHO, CDC, NIH, USPSTF, ACC/AHA, ADA, NASEM, peer-reviewed meta-analyses). No cures, no supplement or
drug promotion, no diagnosis. Each guide: TOC, key takeaways, sections, related tools, FAQ, sources,
last-updated date."*

Guides: Your 8 Prime Numbers; VO2 max & Zone 2; Strength training for healthspan; Protein needs;
Sleep; Blood pressure (2025 guideline); Metabolic health; Steps per day (7,000-step evidence);
Preventive screenings by age; Eating for your prime (fiber, plants, Mediterranean pattern); Stress &
recovery; Alcohol and health; How to read health news.

---

## Phase 8 — Lead generation (dedicated, high-converting)

Prompt: *"Build /get-your-plan.html as a 5-step funnel with a progress bar: goal → age & sex →
biggest obstacle → help wanted (free plan, coach, testing partner, dietitian, app picks) → contact
(name, email, country, optional phone) with two consents: required privacy consent and an optional,
separate consent to be matched with a vetted partner (CASL/GDPR-friendly). Capture UTM parameters,
source page and Prime Score. Show an instant thank-you with next steps."*

Also: inline lead box on home, guides and tools; a non-blocking slide-in (after 50% scroll or 40 s,
once per 7 days, never on form pages); B2B partner intake on /advertise.html.

**Email rule:** every form posts to FormSubmit via AJAX using the site inbox, which is stored XOR-encoded
in main.js and decoded only at submit time. The address never appears in HTML, JS, JSON or docs in
plain text. "Email us" links build a mailto only at click time. Fallback on network failure: a
prefilled mailto.

---

## Phase 9 — Donations, sponsorship, contests, careers, advertising

Prompt: *"Support page: one-time/monthly toggle, tiers ($5, $15, $50, $250, custom), impact framing
for operations, promotion and marketing, hiring talent, contests and prizes, planned allocation chart,
one-click pay buttons driven by CONFIG.payLinks, and a pledge form fallback. State clearly that
Prime.Health is not a registered charity and gifts are not tax-deductible."*

- Challenge: Prime 30 Challenge (monthly habit tracks), entry form, local 30-day tracker, prize
  sponsorship CTA, official rules (no purchase necessary, 18+, skill-testing question for Canadian
  winners, Quebec note, void where prohibited, privacy).
- Careers: medical reviewers (MD/NP/RN/RD), health writers, video creator, community & contest manager,
  partnerships, front-end, SEO; application form; talent pool.
- Advertise: audience, placements (sponsored tool, newsletter, challenge prizes, display, lead
  partners), ad standards, inquiry form; link to web.works/contact.

---

## Phase 10 — Self-updating automation

Prompt: *"Add scripts/update_feeds.py (standard library only) that pulls health headlines from public RSS
feeds (NIH, WHO, FDA, CDC, ScienceDaily, EurekAlert!, MedicalXpress, Harvard Health) and the latest
videos from YouTube channel RSS feeds (resolve @handles to channel IDs; no API key). Store titles and
links only. Add .github/workflows/build.yml: on push and daily cron, refresh feeds, rebuild all HTML,
sitemap and search index, commit to main and request a Pages build."*

Client-side: daily tip by day of year, health observance of the month, auto copyright year.

---

## Phase 11 — AdSense and legal compliance

Prompt: *"Make the site approval-ready."* Checklist: 40+ substantive original pages; About, Contact,
Privacy (Google cookies, DoubleClick, opt-out links, FormSubmit, localStorage, YouTube no-cookie),
Cookie policy, Terms, Medical disclaimer, Editorial policy, Accessibility, **Trademark & copyright
disclosure** (independent site; not affiliated with any "Prime Health", "PrimeHealth" or "Prime
Healthcare" entity; third-party marks belong to their owners; the brand is always written
"Prime.Health"); ads.txt; no ads on error pages; no misleading health claims; no prohibited
pharmaceutical promotion; Google certified CMP for EEA/UK.

---

## Phase 12 — QA, deploy, grow

- QA: link crawl, HTML validity, Lighthouse ≥ 90, keyboard pass, 360px mobile pass, formula tests,
  grep confirms the inbox never appears in plain text.
- Deploy: push to `main` of `WEBWORKSA1/prime.health`; Settings → Pages → main / root.
- Custom domain + HTTPS, Search Console sitemap, then AdSense application.
- Growth (next 90 days): one new tool or guide per week; programmatic pages ("BMI for 5'8\" male"),
  Spanish and French editions, newsletter, Pinterest pins of range-bar graphics, partner outreach.
