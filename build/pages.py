"""Home and core interactive pages."""
import datetime

import layout as L
from layout import esc, ad, lead_box, rbar_static
from tools_pages import BY, CATS, TOOLS, calc_form, faq_html, faq_schema, unit_toggle, field
from tf import HEIGHT, WEIGHT
import pages_more


def ecg_path():
    d = "M0 80"
    for b in range(6):
        x = b * 320
        d += (f" L{x + 60} 80 Q{x + 70} 68 {x + 80} 80 L{x + 96} 80 L{x + 101} 90 L{x + 109} 14 L{x + 117} 104"
              f" L{x + 123} 80 L{x + 152} 80 Q{x + 172} 60 {x + 192} 80 L{x + 320} 80")
    return d


def fmt_date(s):
    try:
        return datetime.date.fromisoformat(s[:10]).strftime("%b %-d, %Y")
    except Exception:
        return ""


def video_cards(items, root, limit=None):
    out = []
    for v in items[:limit] if limit else items:
        out.append(f'''<div class="video-card" data-cat="{esc(v.get("topic", ""))}"><button class="yt" type="button" data-id="{esc(v["id"])}" aria-label="Play: {esc(v["title"])}">
<img src="https://i.ytimg.com/vi/{esc(v["id"])}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"></button>
<h3>{esc(v["title"])}</h3><p>{esc(v.get("channel", ""))}{(" | " + fmt_date(v.get("date", ""))) if v.get("date") else ""}</p></div>''')
    return "".join(out)


def pulse_items(items, limit=None):
    out = []
    for n in items[:limit] if limit else items:
        out.append(f'<li class="pulse-item" data-cat="{esc(n.get("source", ""))}"><time datetime="{esc(n.get("date", ""))}">{fmt_date(n.get("date", ""))}</time>'
                   f'<div><a href="{esc(n["link"])}" target="_blank" rel="noopener nofollow">{esc(n["title"])}</a><span class="src">{esc(n.get("source", ""))}</span></div></li>')
    return "".join(out)


NUMBERS = [
    ("Blood pressure", "Force of blood on artery walls", "below 120/80", (90, 120, 80, 200), "tools/blood-pressure.html"),
    ("A1C", "Three-month blood sugar average", "below 5.7%", (4, 5.7, 4, 12), "tools/a1c.html"),
    ("Non-HDL cholesterol", "Particles that build plaque", "below 130 mg/dL", (70, 130, 70, 260), "tools/cholesterol.html"),
    ("Waist-to-height", "Belly-fat check", "below 0.50", (0.4, 0.5, 0.3, 0.8), "tools/waist-to-height.html"),
    ("BMI Prime", "BMI divided by 25", "0.74–1.00", (0.74, 1.0, 0.5, 1.8), "tools/bmi.html"),
    ("VO₂ max", "Aerobic fitness", "higher every year", (38, 70, 15, 70), "tools/vo2max.html"),
    ("Sleep", "Nightly average", "7–9 hours", (7, 9, 3, 11), "tools/sleep-debt.html"),
    ("Daily steps", "Weekly average", "7,000 or more", (7000, 15000, 0, 15000), "tools/steps.html"),
]

HOME_FAQ = [
    ("Is Prime.Health free?", "Yes. Every calculator, guide and the Prime Score are free with no sign-up. The site is funded by advertising, sponsorship and reader support."),
    ("Do you store what I type into the calculators?", "No. Calculations run in your browser. If you press Save to My Numbers, results are stored only on your device. We only receive information you choose to send through a form."),
    ("Where do the formulas and ranges come from?", "From clinical guidelines and peer-reviewed research, such as the 2025 AHA/ACC blood pressure guideline, the American Diabetes Association and the U.S. Preventive Services Task Force. Every tool lists its sources."),
    ("Can Prime.Health diagnose a condition?", "No. The tools are educational and help you understand your numbers. Diagnosis and treatment need a qualified health professional."),
    ("Is Prime.Health affiliated with other companies called Prime Health?", "No. Prime.Health is an independent website with no connection to any company, clinic or product using a similar name. See our trademark disclosure."),
]


def home(ctx):
    p = ""
    quick_tool = dict(BY["bmi"], fields=[HEIGHT, WEIGHT], cta="Check my BMI Prime")
    quick = calc_form(quick_tool, heading="Your BMI Prime in 10 seconds", compact=True)
    rows = "".join(
        f'<div class="report-row"><div><h3>{n}</h3><p>{d}</p></div><div class="report-target">{t}</div>'
        f'{rbar_static(z[0], z[1], z[2], z[3], n + " target zone " + t)}<a class="btn btn-ghost btn-sm" href="{u}">Check yours</a></div>'
        for n, d, t, z, u in NUMBERS)
    groups = []
    for key, name, blurb in CATS:
        ts = [t for t in TOOLS if t["cat"] == key][:4]
        items = "".join(f'<li><a href="tools/{t["slug"]}.html">{t["short"]}<span>{t["blurb"]}</span></a></li>' for t in ts)
        groups.append(f'<section class="tool-group"><h3>{name}</h3><ul>{items}</ul></section>')
    guides = "".join(f'<li><a href="guides/{g["slug"]}.html"><h3>{g["title"]}</h3><p>{g["desc"]}</p><p class="post-meta">{g.get("read", 6)} min read</p></a></li>' for g in ctx["guides"][:6])
    vids = ctx["videos"].get("items", [])
    video_block = (f'<div class="video-grid">{video_cards(vids, p, 3)}</div>' if vids else
                   '<p>Fresh videos from leading health channels load here automatically every day.</p>')
    news = ctx["news"].get("items", [])
    news_block = (f'<ul class="pulse-list">{pulse_items(news, 6)}</ul>' if news else '<p>Headlines from public health and research agencies refresh here every day.</p>')
    main = f'''<section class="hero ecg-paper">
<div class="wrap hero-grid">
  <div class="hero-copy">
    <h1>Know your numbers.<br>Live in your prime.</h1>
    <p class="lede">{len(TOOLS)} free calculators, a 3-minute Prime Score and plain-language guides for the eight numbers that shape how long and how well you live.</p>
    <div class="hero-cta"><a class="btn btn-signal" href="prime-score.html">Get my Prime Score</a><a class="btn btn-ghost" href="tools/">Browse all tools</a></div>
    <ul class="hero-facts"><li>No sign-up</li><li>Sources on every page</li><li>Your entries stay on your device</li></ul>
  </div>
  <div class="panel quick">{quick}</div>
</div>
<svg class="ecg-trace" viewBox="0 0 1600 120" preserveAspectRatio="xMinYMid slice" aria-hidden="true"><path pathLength="3200" d="{ecg_path()}"/></svg>
</section>

<section class="section"><div class="wrap">
  <div class="section-head"><div><h2>The eight numbers worth knowing</h2><p>Each one is measurable, linked in large studies to heart disease, diabetes and lifespan, and moves when you change how you live.</p></div>
  <a class="btn btn-ghost" href="guides/prime-numbers.html">Read the guide</a></div>
  <div class="report" role="table" aria-label="Prime Numbers and targets">
    <div class="report-row report-head" role="row"><span>Measure</span><span>Prime target</span><span>Target zone</span><span></span></div>
    {rows}
  </div>
</div></section>

<section class="section section-sunk"><div class="wrap score-band">
  <div><h2>One score for your healthspan</h2><p class="lede">The Prime Score turns eight pillars into a single 0–100 number, shows where you stand on each and names the two changes that would lift it most.</p>
  <a class="btn btn-primary" href="prime-score.html">Take the Prime Score</a></div>
  <ul class="pillars"><li>Move<small>activity minutes</small></li><li>Fuel<small>diet quality</small></li><li>Smoke-free<small>nicotine</small></li><li>Sleep<small>hours a night</small></li>
  <li>Weight<small>BMI</small></li><li>Blood pressure<small>mm Hg</small></li><li>Blood sugar<small>A1C</small></li><li>Cholesterol<small>non-HDL</small></li></ul>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><div><h2>Tools by goal</h2><p>Every calculator shows its formula, the guideline behind the ranges and its limits.</p></div><a class="btn btn-ghost" href="tools/">All {len(TOOLS)} tools</a></div>
  <div class="tool-groups">{"".join(groups)}</div>
</div></section>

{('<div class="wrap">' + ad("top") + '</div>')}

<section class="section-tight"><div class="wrap today">
  <div data-observance><h3>This month</h3><p>Loading this month's health focus.</p></div>
  <div><h3>Today's one-minute action</h3><p data-tip>Take a 10-minute walk after your largest meal.</p><a class="btn btn-ghost btn-sm" href="my-numbers.html">Open My Numbers</a></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><div><h2>Guides</h2><p>Evidence-based explainers that end with the tools to act on them.</p></div><a class="btn btn-ghost" href="guides/">All guides</a></div>
  <ul class="post-list">{guides}</ul>
</div></section>

<section class="section section-sunk"><div class="wrap grid-2">
  <div><div class="section-head"><h2>Watch and learn</h2><a class="btn btn-ghost btn-sm" href="videos.html">Video library</a></div>{video_block}</div>
  <div><div class="section-head"><h2>Health Pulse</h2><a class="btn btn-ghost btn-sm" href="pulse.html">All headlines</a></div>{news_block}</div>
</div></section>

<div class="wrap">{lead_box(p, "home")}</div>

<section class="section-tight"><div class="wrap grid-3">
  <div class="box"><h3>Keep Prime.Health free</h3><p>Reader support pays for medical review, new tools and monthly prizes.</p><a class="btn btn-primary btn-sm" href="support.html">Support us</a></div>
  <div class="box"><h3>Prime 30 Challenge</h3><p>Pick one habit, track 30 days, and enter the monthly prize draw.</p><a class="btn btn-primary btn-sm" href="challenge.html">Join this month</a></div>
  <div class="box"><h3>Advertise or partner</h3><p>Sponsor a tool, the newsletter or a challenge prize. Clinics and coaches can join our partner network.</p><a class="btn btn-primary btn-sm" href="advertise.html">Work with us</a></div>
</div></section>

<section class="section"><div class="wrap"><h2>Questions</h2>{faq_html(HOME_FAQ)}</div></section>'''
    schema = [{"@context": "https://schema.org", "@type": "WebSite", "name": L.NAME, "url": L.SITE_URL + "/", "description": L.TAGLINE},
              faq_schema(HOME_FAQ)]
    return {"path": "index.html", "title": "Prime.Health: Free Health Calculators, Prime Score & Guides",
            "desc": "Know your numbers. Live in your prime. Free, evidence-based health calculators (BMI Prime, blood pressure, A1C, VO2 max, calories), the 3-minute Prime Score and plain-language guides.",
            "main": main, "active": "", "schema": schema, "scripts": ("tools.js",), "kind": "Home", "priority": "1.0"}


# ------------------------------------------------------------------ Prime Score
def choice(name, opts, req=True):
    r = " required" if req else ""
    return '<div class="choice-grid">' + "".join(
        f'<label class="choice"><input type="radio" name="{name}" value="{v}"{r}><span>{t}{f"<small>{s}</small>" if s else ""}</span></label>' for v, t, s in opts) + "</div>"


def nav_btns(first=False, last_label=None):
    back = '<span></span>' if first else '<button class="btn btn-ghost" type="button" data-back>Back</button>'
    nxt = f'<button class="btn btn-primary" type="submit">{last_label}</button>' if last_label else '<button class="btn btn-primary" type="button" data-next>Next</button>'
    return f'<div class="step-nav">{back}{nxt}</div>'


def prime_score(ctx):
    p = ""
    diet_q = lambda n, q, o: f'<p style="font-weight:600;margin:16px 0 8px">{q}</p>' + choice(n, o)
    steps = [
        ('Move', 'In a typical week, how many minutes of moderate or vigorous activity do you do?', 'Brisk walking, cycling, sport and workouts all count.',
         choice("move", [("0", "None", ""), ("20", "1–29 minutes", ""), ("40", "30–59 minutes", ""), ("60", "60–89 minutes", ""), ("80", "90–119 minutes", ""), ("90", "120–149 minutes", ""), ("100", "150 minutes or more", "")]), True),
        ('Fuel', 'Four quick questions about a typical day', 'Pick the closest answer.',
         diet_q("d1", "Servings of vegetables and fruit per day", [("0", "0–1", ""), ("1", "2–3", ""), ("2", "4", ""), ("3", "5 or more", "")]) +
         diet_q("d2", "Whole grains, beans, nuts or seeds", [("0", "Rarely", ""), ("1", "Some days", ""), ("2", "Most days", ""), ("3", "Every day", "")]) +
         diet_q("d3", "Sugary drinks per week", [("0", "7 or more", ""), ("1", "3–6", ""), ("2", "1–2", ""), ("3", "None", "")]) +
         diet_q("d4", "Fast-food or ultra-processed meals per week", [("0", "7 or more", ""), ("1", "4–6", ""), ("2", "1–3", ""), ("3", "Rarely", "")]), False),
        ('Smoke-free', 'Do you smoke or vape nicotine?', 'Cigarettes, e-cigarettes and other inhaled nicotine.',
         choice("nicotine", [("100", "Never", ""), ("75", "Quit 5+ years ago", ""), ("50", "Quit 1–5 years ago", ""), ("25", "Quit within the last year", ""), ("0", "Yes, currently", "")]), True),
        ('Sleep', 'On average, how many hours do you sleep a night?', 'Count actual sleep, not time in bed.',
         choice("sleep", [("0", "Under 4", ""), ("20", "4 to under 5", ""), ("40", "5 to under 6", ""), ("70", "6 to under 7", ""), ("100", "7 to under 9", ""), ("90", "9 to under 10", ""), ("40", "10 or more", "")]), True),
        ('Weight', 'Your height and weight', 'Used only to calculate BMI on this device. Leave blank to skip this pillar.',
         f'<div style="margin-bottom:12px">{unit_toggle()}</div><div class="fields">{field(dict(HEIGHT, opt=True))}{field(dict(WEIGHT, opt=True))}</div>', False),
        ('Blood pressure', 'What was your most recent blood pressure?', 'Pick “Not sure” if you have not measured it in the past year.',
         choice("bp", [("100", "Below 120/80", ""), ("75", "120–129 / below 80", ""), ("50", "130–139 or 80–89", ""), ("25", "140–159 or 90–99", ""), ("0", "160+ or 100+", ""), ("na", "Not sure", "")]) +
         '<label class="check"><input type="checkbox" name="bpmed"> I take blood pressure medicine</label>', False),
        ('Blood sugar', 'What do you know about your blood sugar?', 'From your latest A1C or fasting glucose test.',
         choice("glucose", [("100", "Normal", "A1C below 5.7% / fasting below 100"), ("60", "Prediabetes range", "A1C 5.7–6.4%"), ("40", "Diabetes, A1C below 7%", ""), ("30", "Diabetes, A1C 7–7.9%", ""), ("20", "Diabetes, A1C 8–8.9%", ""), ("10", "Diabetes, A1C 9–9.9%", ""), ("0", "Diabetes, A1C 10% or more", ""), ("na", "Not sure", "")]), True),
        ('Cholesterol', 'What is your non-HDL cholesterol?', 'Total cholesterol minus HDL, in mg/dL. In mmol/L: below 3.4, 3.4–4.1, 4.1–4.9, 4.9–5.7, 5.7+.',
         choice("chol", [("100", "Below 130", ""), ("60", "130–159", ""), ("40", "160–189", ""), ("20", "190–219", ""), ("0", "220 or more", ""), ("na", "Not sure", "")]) +
         '<label class="check"><input type="checkbox" name="cholmed"> I take cholesterol-lowering medicine</label>', False),
    ]
    fs = []
    for i, (pill, q, hint, body, auto) in enumerate(steps):
        last = i == len(steps) - 1
        fs.append(f'<fieldset class="step" data-auto="{1 if auto else 0}"{" hidden" if i else ""}><legend>{q}</legend><p class="hint">{pill}. {hint}</p>{body}'
                  f'{nav_btns(first=(i == 0), last_label=("See my Prime Score" if last else None))}</fieldset>')
    main = f'''<div class="wrap">
<header class="page-head" style="max-width:760px;margin:0 auto"><h1>Your Prime Score</h1>
<p class="lede">Eight questions, about three minutes. Get one 0–100 score for your healthspan, a bar for each pillar and the two changes that would lift it most.</p>
<div class="meta-row"><span>Free, no sign-up</span><span>Answers stay on your device</span><span>Inspired by the AHA Life’s Essential 8 approach</span></div></header>
<form class="panel funnel" id="primeScore" data-steps>
  <p class="step-count" aria-live="polite">Step 1 of 8</p><div class="progress-track"><span></span></div>
  {"".join(fs)}
</form>
<div id="scoreOut" class="score-out" hidden tabindex="-1"></div>
<div id="scoreLead" class="score-out" hidden>
  <section class="lead-box" aria-labelledby="sl-h"><div class="lead-copy"><h2 id="sl-h">Get your Prime Plan by email</h2>
  <p>A 30-day plan built around your two biggest wins: weekly targets, simple routines and the checks worth booking.</p><p class="fine">Free. Unsubscribe any time. <a href="privacy-policy.html">Privacy</a></p></div>
  <form class="lead-form" data-form="Prime Score plan request" data-success="Your Prime Plan request is in. Look for it in your inbox within one business day." novalidate>
    <label for="sl-name">First name</label><input id="sl-name" name="name" autocomplete="given-name" required>
    <label for="sl-email">Email</label><input id="sl-email" name="email" type="email" autocomplete="email" required>
    <input type="hidden" name="prime_score"><input type="hidden" name="pillars"><input type="hidden" name="focus">
    <label class="check"><input type="checkbox" name="consent" value="Agreed to privacy policy" required> I agree to the privacy policy.</label>
    <label class="check"><input type="checkbox" name="partner_match" value="Yes"> Also match me with a vetted coach or testing partner (optional).</label>
    <input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
    <button class="btn btn-primary btn-block" type="submit">Email me my plan</button>
  </form></section>
</div>
{ad("footer")}
</div>'''
    return {"path": "prime-score.html", "title": "Prime Score: Your Healthspan in One Number (3-Minute Check)",
            "desc": "Answer eight questions to get your free Prime Score: a 0–100 healthspan score across activity, diet, nicotine, sleep, weight, blood pressure, blood sugar and cholesterol.",
            "main": main, "active": "score", "crumbs": [("Prime Score", "")], "scripts": ("tools.js", "score.js"), "kind": "Tool", "priority": "0.9", "slidein": False}


# ------------------------------------------------------------------ Lead funnel
COUNTRIES = ["United States", "Canada", "United Kingdom", "Australia", "India", "Ireland", "New Zealand", "Germany", "France", "Netherlands", "Sweden",
             "Singapore", "United Arab Emirates", "South Africa", "Philippines", "Sri Lanka", "Mexico", "Brazil", "Other"]


def get_plan(ctx):
    def checks(name, opts):
        return '<div class="choice-grid">' + "".join(f'<label class="choice"><input type="checkbox" name="{name}" value="{esc(t)}"><span>{t}<small>{s}</small></span></label>' for t, s in opts) + "</div>"
    countries = "".join(f"<option>{c}</option>" for c in COUNTRIES)
    main = f'''<div class="wrap">
<header class="page-head" style="max-width:760px;margin:0 auto;text-align:center"><h1>Get your free 30-day Prime Plan</h1>
<p class="lede" style="margin-inline:auto">Answer four quick questions. We'll email a plan built around your goal: weekly targets, a simple training split, meals that fit and the checks worth booking.</p></header>
<form class="panel funnel" data-form="Prime Plan request" data-steps data-success="Your plan request is in. Expect your 30-day Prime Plan in your inbox within one business day. While you wait, &lt;a href=&quot;prime-score.html&quot;&gt;take the Prime Score&lt;/a&gt; so we can sharpen it." novalidate>
  <p class="step-count" aria-live="polite">Step 1 of 5</p><div class="progress-track"><span></span></div>
  <fieldset class="step" data-auto="1"><legend>What is your main goal?</legend><p class="hint">Pick the one that matters most right now.</p>
    {choice("goal", [("Lose fat", "Lose fat", "Steady, sustainable loss"), ("Build strength", "Build strength and muscle", "Two to four sessions a week"), ("Sleep better", "Sleep better", "Fall asleep and stay asleep"),
                      ("Lower BP or blood sugar", "Lower blood pressure or blood sugar", "Move your numbers"), ("More energy", "More energy", "Feel better day to day"), ("Healthspan check-up", "A full healthspan check-up", "Know where you stand")])}
    {nav_btns(first=True)}</fieldset>
  <fieldset class="step" hidden><legend>A little about you</legend><p class="hint">So the plan fits your stage of life.</p>
    <p style="font-weight:600;margin:0 0 8px">Age</p>{choice("age_band", [("18–29", "18–29", ""), ("30–39", "30–39", ""), ("40–49", "40–49", ""), ("50–59", "50–59", ""), ("60–69", "60–69", ""), ("70+", "70 or older", "")])}
    <p style="font-weight:600;margin:16px 0 8px">Sex</p>{choice("sex", [("Female", "Female", ""), ("Male", "Male", ""), ("Prefer not to say", "Prefer not to say", "")], req=False)}
    {nav_btns()}</fieldset>
  <fieldset class="step" data-auto="1" hidden><legend>What usually gets in the way?</legend><p class="hint">Your plan will design around it.</p>
    {choice("obstacle", [("Time", "Time", "Busy days"), ("Motivation", "Motivation", "Starting is easy, keeping going is not"), ("Knowing what to do", "Knowing what to do", "Too much conflicting advice"),
                          ("Pain or injury", "Pain or injury", "Need a gentle start"), ("Cost", "Cost", "Keep it cheap or free"), ("Night shifts or irregular hours", "Shift work or irregular hours", "Odd schedules")])}
    {nav_btns()}</fieldset>
  <fieldset class="step" hidden><legend>What help would you like?</legend><p class="hint">Pick any that apply.</p>
    {checks("help", [("Free email plan", "The 30-day Prime Plan"), ("A coach", "1:1 health or fitness coaching"), ("Lab testing", "Blood tests and health check-ups"),
                      ("A dietitian", "Nutrition support"), ("App and device picks", "Trackers, scales, BP cuffs"), ("Just tips", "The weekly Prime Numbers email")])}
    <label for="gp-when" style="margin-top:16px">When do you want to start?</label>
    <select id="gp-when" name="timeline"><option>This week</option><option>This month</option><option>Just exploring</option></select>
    {nav_btns()}</fieldset>
  <fieldset class="step" hidden><legend>Where should we send your plan?</legend><p class="hint">One plan email, then the weekly Prime Numbers if you want it.</p>
    <div class="fields">
      <div class="field"><label for="gp-name">First name</label><input id="gp-name" name="name" autocomplete="given-name" required></div>
      <div class="field"><label for="gp-email">Email</label><input id="gp-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="gp-country">Country</label><select id="gp-country" name="country" required><option value="">Choose</option>{countries}</select></div>
      <div class="field"><label for="gp-phone">Phone <span class="fine">(optional, for partner calls only)</span></label><input id="gp-phone" name="phone" type="tel" autocomplete="tel"></div>
    </div>
    <label class="check"><input type="checkbox" name="consent" value="Agreed to privacy policy" required> I agree to the <a href="privacy-policy.html" target="_blank">privacy policy</a> and to receive my plan by email.</label>
    <label class="check"><input type="checkbox" name="partner_match" value="Yes"> Match me with a vetted coach, dietitian or testing partner. I agree Prime.Health may share my request with them (optional).</label>
    <label class="check"><input type="checkbox" name="newsletter" value="Yes" checked> Send me The Prime Numbers weekly email.</label>
    <input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
    {nav_btns(last_label="Send my free plan")}</fieldset>
  <ul class="trust-row"><li>Free</li><li>No spam</li><li>Unsubscribe any time</li><li>Shared only with your permission</li></ul>
</form>
<section class="section-tight"><div class="grid-3">
  <div class="box"><h3>What you get</h3><ul><li>Four weekly targets tied to your goal</li><li>A simple training split you can do at home</li><li>Meal templates with protein and fibre targets</li><li>The checks and tests worth booking</li></ul></div>
  <div class="box"><h3>How it works</h3><p>Your answers shape the plan. Nothing is sold. If you tick partner matching, we connect you with one vetted professional, and only then.</p></div>
  <div class="box"><h3>For clinics and coaches</h3><p>Want to receive matched requests from people ready to act?</p><a class="btn btn-ghost btn-sm" href="advertise.html#partners">Join the partner network</a></div>
</div></section>
</div>'''
    return {"path": "get-your-plan.html", "title": "Get Your Free 30-Day Prime Plan", "desc": "Answer four quick questions and get a free 30-day health plan built around your goal: fat loss, strength, sleep, blood pressure, blood sugar or a full healthspan check-up.",
            "main": main, "active": "", "crumbs": [("Free 30-day plan", "")], "kind": "Page", "priority": "0.9", "slidein": False}


def my_numbers(ctx):
    main = '''<div class="wrap">
<header class="page-head"><h1>My Numbers</h1><p class="lede">Every result you save from a calculator or the Prime Score, in one place. Stored only in this browser on this device.</p></header>
<div class="panel" style="padding:24px"><div id="myNumbers"><p>Loading your saved numbers.</p></div>
<div class="res-actions"><button class="btn btn-ghost btn-sm" id="exportNumbers" type="button">Download as file</button><button class="btn btn-ghost btn-sm" id="clearNumbers" type="button">Remove all</button></div></div>
<section class="section-tight grid-2"><div><h2>Your targets at a glance</h2><p>Blood pressure below 120/80. A1C below 5.7%. Non-HDL cholesterol below 130 mg/dL. Waist below half your height. BMI Prime 0.74–1.00. VO₂ max rising. Sleep 7–9 hours. Steps 7,000+.</p><a class="btn btn-primary" href="guides/prime-numbers.html">Why these targets</a></div>
<div><h2>Privacy</h2><p>Nothing here is sent to us. Clearing your browser data or using another device starts fresh. Download the file to keep a copy.</p></div></section>
</div>'''
    return {"path": "my-numbers.html", "title": "My Numbers: Your Saved Health Results", "desc": "See all the health numbers you have saved from Prime.Health calculators and the Prime Score, stored privately on your device.",
            "main": main, "crumbs": [("My Numbers", "")], "kind": "Page", "robots": "noindex,follow", "sitemap": False, "priority": "0.3"}


def videos(ctx):
    v = ctx["videos"]
    items = v.get("items", [])
    topics = sorted({i.get("topic", "") for i in items if i.get("topic")})
    chans = ctx["feeds"].get("youtube", [])
    clist = "".join(f'<li><a href="https://www.youtube.com/@{esc(c["handle"])}" target="_blank" rel="noopener">{esc(c["name"])}<small>{esc(c.get("topic", ""))}</small></a></li>' for c in chans)
    filt = ('<div class="filter-row" data-filter-group="#videoGrid" aria-label="Filter videos by topic"><button type="button" data-filter="all" aria-pressed="true">All</button>' +
            "".join(f'<button type="button" data-filter="{esc(t)}" aria-pressed="false">{esc(t)}</button>' for t in topics) + "</div>") if topics else ""
    grid = f'{filt}<div class="video-grid" id="videoGrid">{video_cards(items, "")}</div>' if items else '<div class="empty"><p>The newest videos from the channels below load here automatically each day.</p></div>'
    upd = f'<span>Refreshed {fmt_date(v.get("updated", ""))}</span>' if v.get("updated") else ""
    main = f'''<div class="wrap">
<header class="page-head"><h1>Health video library</h1><p class="lede">The latest videos from respected health, fitness and science channels, refreshed automatically every day. Videos load only when you press play.</p>
<div class="meta-row">{upd}<span>Click to play, privacy-enhanced mode</span></div></header>
{grid}
{ad("top")}
<section class="section-tight"><h2>Channels we follow</h2><ul class="channel-list">{clist}</ul>
<p class="fine">Videos are produced by third parties and embedded from YouTube. Inclusion is not an endorsement of every claim; check advice against our guides and your clinician. Want your channel considered? <a href="contact.html">Contact us</a>.</p></section>
</div>'''
    return {"path": "videos.html", "title": "Health Video Library: Fitness, Sleep, Nutrition & Prevention", "desc": "Watch the latest videos on exercise, sleep, nutrition, heart health and longevity from respected channels, refreshed daily.",
            "main": main, "active": "videos", "crumbs": [("Videos", "")], "kind": "Hub", "lastmod": (v.get("updated") or "2026-11-11")[:10], "priority": "0.6"}


def pulse(ctx):
    n = ctx["news"]
    items = n.get("items", [])
    sources = sorted({i.get("source", "") for i in items if i.get("source")})
    filt = ('<div class="filter-row" data-filter-group="#pulseList" aria-label="Filter by source"><button type="button" data-filter="all" aria-pressed="true">All sources</button>' +
            "".join(f'<button type="button" data-filter="{esc(s)}" aria-pressed="false">{esc(s)}</button>' for s in sources) + "</div>") if sources else ""
    body = f'{filt}<ul class="pulse-list" id="pulseList">{pulse_items(items)}</ul>' if items else '<div class="empty"><p>Headlines refresh automatically every day. Check back shortly.</p></div>'
    upd = f'<span>Refreshed {fmt_date(n.get("updated", ""))}</span>' if n.get("updated") else ""
    main = f'''<div class="wrap">
<header class="page-head"><h1>Health Pulse</h1><p class="lede">Today's health and medical research headlines from public agencies and research news services, updated automatically every day. We link to the original source.</p>
<div class="meta-row">{upd}<span>{len(items)} headlines</span><span>Sources: {len(sources) or "multiple"}</span></div></header>
<div class="tool-layout"><div>
<div class="callout"><b>Read headlines like a scientist.</b> Is it a human trial or a mouse study? Absolute or relative risk? Our <a href="guides/health-news.html">health news checklist</a> takes 30 seconds.</div>
{body}
</div>
<aside class="side"><div class="side-box"><h2>Turn news into numbers</h2><ul><li><a href="tools/blood-pressure.html">Blood pressure checker</a></li><li><a href="tools/a1c.html">A1C converter</a></li><li><a href="tools/screenings.html">Screening planner</a></li><li><a href="prime-score.html">Prime Score</a></li></ul></div>
<div class="side-box"><h2>The Prime Numbers, weekly</h2><p>The one study worth knowing each week, explained.</p>{L.newsletter_form("pulse")}</div>{ad("sidebar")}</aside>
</div></div>'''
    return {"path": "pulse.html", "title": "Health Pulse: Today's Health and Medical Research News", "desc": "Daily health and medical research headlines from NIH, WHO, FDA, CDC and leading research news services, refreshed automatically with links to the original sources.",
            "main": main, "active": "pulse", "crumbs": [("Health Pulse", "")], "kind": "Hub", "lastmod": (n.get("updated") or "2026-11-11")[:10], "priority": "0.6"}


def build(ctx):
    return [home(ctx), prime_score(ctx), get_plan(ctx), my_numbers(ctx), videos(ctx), pulse(ctx)] + pages_more.build(ctx)
