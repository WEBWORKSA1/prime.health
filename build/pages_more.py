"""Support, challenge, advertise, careers, about and contact pages."""
import layout as L
from layout import esc, ad

HP = '<input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">'
CONSENT = '<label class="check"><input type="checkbox" name="consent" value="Agreed to privacy policy" required> I agree to the <a href="privacy-policy.html" target="_blank">privacy policy</a>.</label>'


def inp(id_, label, type_="text", req=True, ac="", ph="", name=None):
    r = " required" if req else ""
    a = f' autocomplete="{ac}"' if ac else ""
    p = f' placeholder="{ph}"' if ph else ""
    opt = "" if req else ' <span class="fine">(optional)</span>'
    return f'<div class="field"><label for="{id_}">{label}{opt}</label><input id="{id_}" name="{name or id_.split("-", 1)[1]}" type="{type_}"{a}{p}{r}></div>'


def sel(id_, label, opts, req=True, name=None):
    r = " required" if req else ""
    o = '<option value="">Choose</option>' + "".join(f"<option>{esc(x)}</option>" for x in opts)
    return f'<div class="field"><label for="{id_}">{label}</label><select id="{id_}" name="{name or id_.split("-", 1)[1]}"{r}>{o}</select></div>'


def area(id_, label, req=True, ph=""):
    r = " required" if req else ""
    return f'<div class="field" style="grid-column:1/-1"><label for="{id_}">{label}</label><textarea id="{id_}" name="{id_.split("-", 1)[1]}" placeholder="{ph}"{r}></textarea></div>'


# ------------------------------------------------------------------ Support / donations
def support(ctx):
    alloc = [("Content and medical review", 35, "ok"), ("Operations, hosting and tools", 20, "low"), ("Promotion and marketing", 20, "warn"), ("Hiring talent", 15, "warn2"), ("Contests and prizes", 10, "high")]
    bar = "".join(f'<span class="bg-{t}" style="width:{w}%">{w}%</span>' for _, w, t in alloc)
    legend = "".join(f'<li><i class="bg-{t}"></i>{n}: {w}%</li>' for n, w, t in alloc)
    amounts = "".join(f'<button type="button" data-amount="{a}" aria-pressed="false">${a}<small>{s}</small></button>'
                      for a, s in [(5, "Supporter"), (15, "Ally"), (50, "Champion"), (250, "Patron")])
    main = f'''<div class="wrap">
<header class="page-head"><h1>Keep Prime.Health free for everyone</h1>
<p class="lede">No paywalls, no sign-ups, no selling your data. Reader support funds medical review, new tools, the monthly challenge prizes and the people who build it all.</p></header>
<div class="grid-2">
<section class="panel give" aria-labelledby="give-h"><h2 id="give-h">Choose your support</h2>
  <div class="seg-toggle" role="group" aria-label="Frequency"><button type="button" data-freq="monthly" aria-pressed="true">Monthly</button><button type="button" data-freq="once" aria-pressed="false">One time</button></div>
  <div class="amounts">{amounts}<div class="field" style="margin:0"><label class="sr" for="customAmount">Other amount in dollars</label><input id="customAmount" type="number" min="1" step="1" inputmode="numeric" placeholder="Other $" style="min-height:64px;text-align:center;font-weight:700"></div></div>
  <p>You are giving <b id="giveSummary">$15 per month</b>.</p>
  <button class="btn btn-signal btn-block" id="giveGo" type="button">Continue</button>
  <div id="giveOut" aria-live="polite"></div>
  <p class="fine" style="margin-top:14px">Prime.Health is an independent publication, not a registered charity. Contributions are not tax-deductible. Payments are processed by the provider you choose; we never see your card details.</p>
</section>
<section><h2>Where your support goes</h2><p>Planned allocation of reader contributions:</p><div class="alloc" role="img" aria-label="Allocation: {", ".join(f"{n} {w}%" for n, w, _ in alloc)}">{bar}</div><ul class="legend-list">{legend}</ul>
<h3 style="margin-top:24px">What each level makes possible</h3>
<ul><li><b>$5 a month</b> keeps a calculator online and maintained for a month.</li><li><b>$15 a month</b> funds the daily news and video refresh.</li><li><b>$50</b> pays for a clinician's review of one guide.</li><li><b>$250</b> funds a month of Prime 30 Challenge prizes.</li></ul>
</section>
</div>

<section class="section" id="pledge-section"><div class="grid-2">
<div><h2>Pledge your support</h2><p>Prefer a bank transfer or an invoice, or want to give in another currency? Leave a pledge and we'll send a secure payment link or invoice within one business day.</p>
<ul><li>Name supporters on our thank-you wall (optional)</li><li>Monthly impact update by email</li><li>Cancel any time</li></ul></div>
<form class="panel" id="pledge" style="padding:24px" data-form="Donation pledge" data-success="Thank you. We'll email your secure payment link within one business day." novalidate>
  <div class="fields">{inp("pl-name", "Name", ac="name")}{inp("pl-email", "Email", "email", ac="email")}
  <div class="field"><label for="pl-amount">Amount</label><input id="pl-amount" name="amount" value="$15" required></div>
  <div class="field"><label for="pl-freq">Frequency</label><select id="pl-freq" name="frequency"><option value="monthly">Monthly</option><option value="once">One time</option></select></div>
  {area("pl-message", "Message (optional)", req=False)}</div>
  <label class="check"><input type="checkbox" name="public_thanks" value="Yes"> Thank me by name on the supporters wall</label>
  {CONSENT}{HP}<button class="btn btn-primary btn-block" type="submit">Send my pledge</button>
</form></div></section>

<section class="section-tight"><h2>Sponsorship tiers for organisations</h2><p>Mission-aligned brands, clinics and employers can fund Prime.Health and reach a health-motivated audience. All sponsorships follow our <a href="advertise.html#standards">advertising standards</a>.</p>
<div class="tiers">
  <div class="tier"><h3>Community sponsor</h3><p class="price">from $250<small>/mo</small></p><ul><li>Logo on the supporters page</li><li>Thank-you in the weekly email</li></ul></div>
  <div class="tier"><h3>Challenge sponsor</h3><p class="price">from $500<small>/mo</small></p><ul><li>Fund the monthly prize pool</li><li>Named on the challenge page and rules</li></ul></div>
  <div class="tier"><h3>Tool sponsor</h3><p class="price">from $750<small>/mo</small></p><ul><li>“Sponsored by” line on one calculator</li><li>No influence on formulas or results</li></ul></div>
  <div class="tier"><h3>Founding partner</h3><p class="price">custom</p><ul><li>Category exclusivity</li><li>Co-created guide series</li></ul></div>
</div>
<p style="margin-top:18px"><a class="btn btn-primary" href="advertise.html">Discuss a sponsorship</a> <a class="btn btn-ghost" href="{L.CONTACT_URL}" target="_blank" rel="noopener">Domain, sponsorship and partnership inquiries</a></p></section>

<section class="section-tight grid-3">
  <div class="box"><h3>Share a tool</h3><p>Send a calculator to someone who would use it. Word of mouth is our best marketing.</p></div>
  <div class="box"><h3>Join the team</h3><p>Clinicians, writers, video makers and developers: we're hiring freelancers.</p><a class="btn btn-ghost btn-sm" href="careers.html">See roles</a></div>
  <div class="box"><h3>Sponsor a prize</h3><p>Put your product in front of motivated people finishing a 30-day habit.</p><a class="btn btn-ghost btn-sm" href="challenge.html#prizes">Challenge prizes</a></div>
</section>
</div>'''
    return {"path": "support.html", "title": "Support Prime.Health: Donate or Sponsor", "desc": "Help keep Prime.Health free. Give monthly or once, pledge by invoice, or sponsor tools, the newsletter and challenge prizes.",
            "main": main, "active": "support", "crumbs": [("Support", "")], "kind": "Page", "slidein": False, "ads": True}


# ------------------------------------------------------------------ Challenge / contests
def challenge(ctx):
    tracks = [("7K Steps Daily", "Average 7,000+ steps every day", "tools/steps.html"), ("Seven-Hour Sleep", "At least 7 hours of sleep on 25+ nights", "tools/sleep-debt.html"),
              ("Protein Every Meal", "25 g+ protein at breakfast, lunch and dinner", "tools/protein.html"), ("Move After Meals", "A 10-minute walk after your two biggest meals", "guides/metabolic-health.html"),
              ("Strength Twice a Week", "Eight strength sessions in 30 days", "guides/strength-training.html"), ("Alcohol-Free 30", "No alcohol for 30 days", "guides/alcohol.html")]
    tl = "".join(f'<div class="box"><h3>{n}</h3><p>{d}</p><a class="btn btn-ghost btn-sm" href="{u}">Tool or guide</a></div>' for n, d, u in tracks)
    opts = "".join(f"<option>{n}</option>" for n, _, _ in tracks)
    main = f'''<div class="wrap">
<header class="page-head"><h1>The Prime 30 Challenge</h1><p class="lede">Pick one habit. Track it for 30 days. Finish and you're entered into this month's prize draw. Free to enter, open to adults 18+.</p>
<div class="hero-cta" style="margin-top:10px"><a class="btn btn-signal" href="#enter">Enter this month</a><a class="btn btn-ghost" href="#rules">Official rules</a></div></header>

<section class="section-tight"><h2>How it works</h2><ol>
<li><b>Enter</b> with your name, email and chosen track before the 5th of the month.</li><li><b>Track</b> each day below. Your check-ins stay on this device.</li>
<li><b>Finish</b> by sending your completion form in the last 3 days of the month, with your day count and a one-line takeaway.</li>
<li><b>Win</b>: completers are entered into a random draw; selected entrants answer a skill-testing question before prizes are awarded.</li></ol></section>

<section class="section-tight"><h2>Choose a track</h2><div class="grid-3">{tl}</div></section>

<section class="section-tight panel" style="padding:24px"><h2>Your 30-day tracker</h2><p>Tap a day when you hit your target. Saved in this browser only.</p><div class="tracker" aria-label="30-day tracker"></div><p id="trackerStatus" aria-live="polite"></p></section>

<section class="section" id="enter"><div class="grid-2">
<div><h2>Enter this month</h2><p>One entry per person per month. You'll get a reminder email at the halfway point and a completion form near the end of the month.</p>
<h3 id="prizes" style="margin-top:26px">Prizes</h3><p>Each month's prize pool is funded by sponsors and reader support and is announced on this page at the start of the month. Typical prizes include fitness trackers, home blood pressure monitors, gift cards and coaching sessions.</p>
<p><a class="btn btn-ghost btn-sm" href="advertise.html">Sponsor a prize</a> <a class="btn btn-ghost btn-sm" href="support.html">Fund the prize pool</a></p>
<h3>Winners</h3><p>Winners are listed here, with their permission, within 14 days of each draw.</p></div>
<form class="panel" style="padding:24px" data-form="Prime 30 Challenge entry" data-success="You're in. Your tracker is above. We'll email you at the halfway point." novalidate>
  <div class="fields">{inp("ch-name", "Full name", ac="name")}{inp("ch-email", "Email", "email", ac="email")}
  {inp("ch-country", "Country", ac="country-name")}{inp("ch-region", "Province or state", ac="address-level1")}
  <div class="field" style="grid-column:1/-1"><label for="ch-track">Track</label><select id="ch-track" name="track" required><option value="">Choose</option>{opts}</select></div></div>
  <label class="check"><input type="checkbox" name="adult" value="18+" required> I am 18 or older.</label>
  <label class="check"><input type="checkbox" name="rules" value="Accepted" required> I accept the <a href="#rules">official rules</a>.</label>
  {CONSENT}{HP}<button class="btn btn-primary btn-block" type="submit">Enter the challenge</button>
</form></div></section>

<section class="section-tight rules" id="rules"><h2>Official rules</h2>
<ol>
<li><b>Sponsor.</b> The Prime 30 Challenge (“the Contest”) is run by Prime.Health. Prize sponsors, where any, are named on this page each month.</li>
<li><b>No purchase necessary.</b> A purchase or donation does not increase your chances of winning.</li>
<li><b>Eligibility.</b> Open to legal residents of jurisdictions where the Contest is not prohibited, aged 18 or older (or the age of majority where they live, if higher). Employees and contractors of Prime.Health and prize sponsors, and their immediate families, are not eligible. Void where prohibited or restricted by law.</li>
<li><b>Entry period.</b> Each monthly Contest runs from the first to the last day of the calendar month. Entries must be received by 11:59 p.m. Eastern Time on the 5th; completion forms by 11:59 p.m. Eastern Time on the last day of the month.</li>
<li><b>How to qualify.</b> Submit one entry form and one completion form reporting at least 25 of 30 days on your chosen track. Completion is self-reported and on your honour.</li>
<li><b>Selection.</b> Winners are selected by random draw from all eligible completers within 7 days after the month ends. Odds depend on the number of eligible completers.</li>
<li><b>Skill-testing question.</b> Before being declared a winner, a selected entrant must correctly answer, without assistance, a time-limited mathematical skill-testing question, as required for residents of Canada and applied to all entrants.</li>
<li><b>Notification.</b> Selected entrants are notified by email and must respond within 7 days, or an alternate may be drawn.</li>
<li><b>Prizes.</b> Prizes are as described on this page for that month, are not transferable and have no cash alternative unless stated. Prime.Health may substitute a prize of equal or greater value. Winners are responsible for any taxes.</li>
<li><b>Quebec residents.</b> Any litigation respecting the conduct or organisation of a publicity contest may be submitted to the Régie des alcools, des courses et des jeux. Any litigation respecting the awarding of a prize may be submitted to the Régie only for the purpose of helping the parties reach a settlement.</li>
<li><b>Health.</b> Choose a track suitable for your health. Ask a clinician before starting a new exercise or diet routine if you have a medical condition, are pregnant or are unsure.</li>
<li><b>Privacy.</b> Entry data is used to run the Contest and as described in our <a href="privacy-policy.html">privacy policy</a>. Winners' first names and regions may be published with their consent.</li>
<li><b>General.</b> Prime.Health may cancel, suspend or modify the Contest if fraud, technical failure or other factors impair its integrity. Decisions of Prime.Health are final.</li>
</ol></section>
{ad("footer")}
</div>'''
    return {"path": "challenge.html", "title": "Prime 30 Challenge: Track One Habit for 30 Days and Win Prizes", "desc": "Join the free Prime 30 Challenge. Choose steps, sleep, protein, strength or alcohol-free, track 30 days and enter the monthly prize draw.",
            "main": main, "active": "challenge", "crumbs": [("Challenge", "")], "kind": "Page", "slidein": False}


# ------------------------------------------------------------------ Advertise / partner
def advertise(ctx):
    interests = ["Sponsored calculator", "Newsletter sponsorship", "Challenge prize sponsorship", "Display advertising", "Lead partner network (clinics, coaches, labs)",
                 "Content partnership", "Acquire this website or domain", "Other"]
    budgets = ["Under $500/month", "$500–$2,000/month", "$2,000–$10,000/month", "$10,000+/month", "One-off project", "Not sure yet"]
    main = f'''<div class="wrap">
<header class="page-head"><h1>Advertise, sponsor or partner with Prime.Health</h1>
<p class="lede">Reach people at the moment they check their blood pressure, plan their training or decide to book a screening. Every placement is clearly labelled and kept apart from our editorial content.</p>
<p><a class="btn btn-signal" href="#inquire">Start a conversation</a> <a class="btn btn-ghost" href="{L.CONTACT_URL}" target="_blank" rel="noopener">Domain and acquisition inquiries</a></p></header>

<section class="section-tight"><h2>Why Prime.Health</h2><div class="grid-3">
<div class="box"><h3>High-intent moments</h3><p>Visitors arrive with a specific health question and leave with a number and a next step.</p></div>
<div class="box"><h3>Evergreen inventory</h3><p>Calculator traffic is steady year-round, with peaks in January, spring and pre-summer.</p></div>
<div class="box"><h3>Brand-safe context</h3><p>Evidence-based content, sources on every page, no sensational headlines.</p></div></div></section>

<section class="section-tight"><h2>Placements</h2><div class="tiers">
<div class="tier"><h3>Sponsored calculator</h3><p>A “sponsored by” line and a relevant offer on one tool. Formulas and results are never influenced.</p></div>
<div class="tier"><h3>Newsletter</h3><p>A single sponsor slot in The Prime Numbers weekly email.</p></div>
<div class="tier"><h3>Challenge prizes</h3><p>Fund the monthly Prime 30 prize pool and be named in the rules and winner posts.</p></div>
<div class="tier"><h3>Display</h3><p>Programmatic display through Google AdSense; direct campaigns by arrangement.</p></div>
</div></section>

<section class="section-tight" id="partners"><h2>Lead partner network</h2>
<p>Clinics, health coaches, registered dietitians, physiotherapists and accredited lab-testing services can receive requests from visitors who explicitly ask to be matched with a professional. We share a request only when the visitor ticks the partner-matching consent box. Partners are vetted for licensing, insurance and advertising standards, and pay per qualified, consented request.</p></section>

<section class="section-tight" id="standards"><h2>Advertising standards</h2><ul>
<li>All paid content is labelled “Advertisement” or “Sponsored”.</li><li>Sponsors have no control over editorial content, formulas, rankings or results.</li>
<li>We do not accept ads for unapproved drugs or supplements making disease claims, “miracle” weight-loss products, tobacco or vaping, gambling or anything that conflicts with Google publisher policies.</li>
<li>Health claims in sponsored material must be truthful and supported by evidence.</li></ul></section>

<section class="section" id="inquire"><div class="grid-2">
<div><h2>Tell us what you have in mind</h2><p>We reply within two business days with availability and options. For acquiring the Prime.Health website or domain, sponsorship or partnership, you can also use <a href="{L.CONTACT_URL}" target="_blank" rel="noopener">web.works/contact</a>.</p></div>
<form class="panel" style="padding:24px" data-form="Advertising and partnership inquiry" data-success="Thanks. We'll reply within two business days." novalidate>
<div class="fields">{inp("ad-name", "Name", ac="name")}{inp("ad-company", "Company or organisation", ac="organization")}{inp("ad-email", "Work email", "email", ac="email")}{inp("ad-website", "Website", "url", req=False, ph="https://")}
{sel("ad-interest", "Interested in", interests)}{sel("ad-budget", "Budget", budgets, req=False)}{area("ad-message", "Message")}</div>
{CONSENT}{HP}<button class="btn btn-primary btn-block" type="submit">Send inquiry</button></form></div></section>
</div>'''
    return {"path": "advertise.html", "title": "Advertise, Sponsor or Partner with Prime.Health", "desc": "Sponsored calculators, newsletter sponsorship, challenge prizes, display and a consent-based lead partner network for clinics, coaches and labs.",
            "main": main, "crumbs": [("Advertise & partner", "")], "kind": "Page", "slidein": False}


# ------------------------------------------------------------------ Careers
ROLES = [
    ("Medical reviewer (MD, DO, NP, RN or RD)", "Freelance, remote", "Review guides and calculator explainers for clinical accuracy and sign off with your name and credentials. 2–6 hours a month.", "Active licence in good standing; plain-language skills."),
    ("Health and science writer", "Freelance, remote", "Write and update evidence-based guides from guidelines and systematic reviews.", "Published health writing; comfort reading research papers."),
    ("Video creator and editor", "Freelance, remote", "Turn our tools and guides into short explainers and walkthroughs for YouTube and social.", "Portfolio of explainer or fitness content."),
    ("Community and contest manager", "Part-time, remote", "Run the monthly Prime 30 Challenge, prize fulfilment and the newsletter.", "Community or email marketing experience; reliable follow-through."),
    ("Partnerships and ad sales", "Commission-based, remote", "Sign sponsors and build the lead partner network of clinics, coaches and labs.", "Health, wellness or media sales experience."),
    ("Front-end developer", "Contract, remote", "Build new calculators and improve performance and accessibility on a static site.", "HTML, CSS, vanilla JavaScript; accessibility know-how."),
    ("SEO and growth specialist", "Contract, remote", "Grow organic traffic with technical SEO, programmatic pages and outreach.", "Proven organic growth on content or tool sites."),
]


def careers(ctx):
    rl = "".join(f'<div class="role"><h3>{t}</h3><p><span class="tag">{k}</span></p><p>{d}</p><p class="fine"><b>You bring:</b> {r}</p></div>' for t, k, d, r in ROLES)
    opts = [t for t, *_ in ROLES] + ["General talent pool"]
    main = f'''<div class="wrap">
<header class="page-head"><h1>Work with Prime.Health</h1><p class="lede">We're a small, remote team building the clearest health-numbers resource on the web. We hire freelancers and contractors worldwide and pay on time.</p></header>
<div class="tool-layout"><div><h2>Open roles</h2>{rl}</div>
<aside class="side"><div class="side-box"><h2>How we work</h2><ul><li><a href="editorial-policy.html">Our editorial standards</a></li><li><a href="about.html">About Prime.Health</a></li><li><a href="support.html">How we're funded</a></li></ul></div></aside></div>
<section class="section" id="apply"><div class="grid-2"><div><h2>Apply or join the talent pool</h2><p>Share a short note and links to your work. We reply to every application within ten business days.</p></div>
<form class="panel" style="padding:24px" data-form="Job application" data-success="Application received. We'll reply within ten business days." novalidate>
<div class="fields">{inp("jb-name", "Full name", ac="name")}{inp("jb-email", "Email", "email", ac="email")}{sel("jb-role", "Role", opts)}{inp("jb-location", "City and country", ac="address-level2")}
{inp("jb-portfolio", "Portfolio or work samples (URL)", "url", ph="https://")}{inp("jb-linkedin", "LinkedIn (URL)", "url", req=False, ph="https://")}
{sel("jb-availability", "Availability", ["A few hours a month", "Up to 10 hours a week", "10–20 hours a week", "20+ hours a week"])}{area("jb-message", "Why you, in a few lines")}</div>
{CONSENT}{HP}<button class="btn btn-primary btn-block" type="submit">Send application</button></form></div></section>
</div>'''
    schema = [{"@context": "https://schema.org", "@type": "ItemList", "name": "Open roles at Prime.Health", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t} for i, (t, *_) in enumerate(ROLES)]}]
    return {"path": "careers.html", "title": "Careers at Prime.Health: Remote Health Writing, Review, Video and Growth Roles", "desc": "Freelance and contract roles for medical reviewers, health writers, video creators, community managers, partnerships, developers and SEO.",
            "main": main, "crumbs": [("Careers", "")], "schema": schema, "kind": "Page", "slidein": False}


# ------------------------------------------------------------------ About + contact
def about(ctx):
    n_tools, n_guides = len(ctx["tools"]), len(ctx["guides"])
    main = f'''<div class="wrap"><div class="prose">
<h1>About Prime.Health</h1>
<p class="lede">Prime.Health helps people understand and improve the numbers that shape how long and how well they live.</p>
<div class="stat-strip" style="margin:24px 0"><div><b>{n_tools}</b><span>free calculators</span></div><div><b>{n_guides}</b><span>evidence-based guides</span></div><div><b>8</b><span>Prime Numbers</span></div><div><b>0</b><span>sign-ups required</span></div></div>
<h2 id="mission">Our mission</h2><p>Health advice is everywhere; clear, trustworthy numbers are not. We turn clinical guidelines and research into free tools and plain-language guides so anyone can see where they stand, what to change and when to talk to a professional.</p>
<h2 id="what">What we publish</h2><ul><li><a href="tools/">Calculators</a> that show their formulas, ranges and limits.</li><li>The <a href="prime-score.html">Prime Score</a>, a 3-minute healthspan check.</li>
<li><a href="guides/">Guides</a> grounded in guidelines and systematic reviews.</li><li><a href="pulse.html">Health Pulse</a> and a <a href="videos.html">video library</a> refreshed daily from reputable sources.</li></ul>
<h2 id="principles">Principles</h2><ul><li><b>Evidence first.</b> Every page lists its sources. See our <a href="editorial-policy.html">editorial policy</a>.</li><li><b>Privacy by design.</b> Calculations run in your browser; saved numbers stay on your device.</li>
<li><b>No diagnosis.</b> We help you understand numbers; clinicians diagnose and treat.</li><li><b>Independence.</b> Advertisers and sponsors never influence content or results.</li></ul>
<h2 id="money">How we're funded</h2><p>Display advertising (Google AdSense), clearly labelled sponsorships, a consent-based partner network that connects visitors who ask for help with vetted professionals, and reader <a href="support.html">support</a>. We do not sell personal data.</p>
<h2 id="independent">Independent</h2><p>Prime.Health is an independent website. It is not affiliated with any hospital, clinic, insurer or company using a similar name. See our <a href="trademark.html">trademark and copyright disclosure</a>.</p>
<h2 id="contact">Get in touch</h2><p>Questions, corrections or ideas: <a href="contact.html">contact us</a>. For acquiring this website or domain, sponsorship, advertising or partnership: <a href="{L.CONTACT_URL}" target="_blank" rel="noopener">web.works/contact</a>.</p>
</div></div>'''
    return {"path": "about.html", "title": "About Prime.Health", "desc": "Prime.Health turns clinical guidelines and research into free health calculators, the Prime Score and plain-language guides. Learn our mission and principles.",
            "main": main, "crumbs": [("About", "")], "kind": "Page",
            "schema": [{"@context": "https://schema.org", "@type": "AboutPage", "name": "About Prime.Health", "url": L.canonical("about.html")}]}


def contact(ctx):
    topics = ["General question", "Correction or feedback on content", "Calculator problem", "Prime Plan or newsletter", "Challenge or prizes", "Press", "Privacy request", "Other"]
    main = f'''<div class="wrap">
<header class="page-head"><h1>Contact Prime.Health</h1><p class="lede">Send us a message and we'll reply within two business days. We can't give personal medical advice; for urgent health concerns, contact a clinician or your local emergency number.</p></header>
<div class="grid-2">
<form class="panel" style="padding:24px" data-form="Contact form" data-success="Thanks. Your message is in and we'll reply within two business days." novalidate>
<div class="fields">{inp("ct-name", "Name", ac="name")}{inp("ct-email", "Email", "email", ac="email")}{sel("ct-topic", "Topic", topics)}{area("ct-message", "Message")}</div>
{CONSENT}{HP}<button class="btn btn-primary btn-block" type="submit">Send message</button></form>
<div>
<div class="box"><h2 style="font-size:1.5rem">Prefer email?</h2><p>Open a new message in your email app.</p><a class="btn btn-ghost" href="contact.html" data-mail="Prime.Health inquiry">Email us</a></div>
<div class="box" style="margin-top:18px"><h2 style="font-size:1.5rem">Website, domain, sponsorship or partnership</h2><p>Interested in acquiring this website or the domain name, or in sponsorship, advertising or partnership?</p><a class="btn btn-primary" href="{L.CONTACT_URL}" target="_blank" rel="noopener">Contact via web.works</a></div>
<div class="box" style="margin-top:18px"><h2 style="font-size:1.5rem">Advertisers and clinics</h2><p>Use the <a href="advertise.html#inquire">advertising and partner form</a> for faster routing.</p></div>
</div></div></div>'''
    return {"path": "contact.html", "title": "Contact Prime.Health", "desc": "Contact Prime.Health with questions, corrections, partnership or press inquiries.",
            "main": main, "crumbs": [("Contact", "")], "kind": "Page", "slidein": False,
            "schema": [{"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact Prime.Health", "url": L.canonical("contact.html")}]}


def build(ctx):
    return [support(ctx), challenge(ctx), advertise(ctx), careers(ctx), about(ctx), contact(ctx)]
