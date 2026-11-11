"""Editorial, legal, trademark, accessibility and 404 pages."""
import layout as L

UPDATED = "November 11, 2026"


def doc(path, title, desc, h1, body, crumb, kind="Policy", robots=None):
    main = f'<div class="wrap"><article class="prose" style="padding-bottom:30px"><h1>{h1}</h1><p class="fine">Last updated {UPDATED}</p>{body}</article></div>'
    pg = {"path": path, "title": title, "desc": desc, "main": main, "crumbs": [(crumb, "")], "kind": kind, "priority": "0.3", "slidein": False}
    if robots:
        pg["robots"] = robots
    return pg


EDITORIAL = """
<p>Prime.Health publishes health calculators and guides that people use to make real decisions. These standards explain how we earn that trust.</p>
<h2 id="sources">How we choose sources</h2><p>We rank evidence in this order and cite it on every page:</p>
<ol><li>Clinical practice guidelines from major bodies (for example WHO, CDC, NIH, U.S. Preventive Services Task Force, American Heart Association and American College of Cardiology, American Diabetes Association, NICE).</li>
<li>Systematic reviews and meta-analyses in peer-reviewed journals.</li><li>Large randomised controlled trials.</li><li>Large prospective cohort studies, clearly described as observational.</li></ol>
<p>We avoid press releases as primary sources, do not rely on single small studies for advice, and say plainly when evidence is limited or mixed.</p>
<h2 id="calculators">Calculators</h2><p>Every calculator states its formula, the guideline behind its ranges, and its limits. Results are estimates for education, not diagnoses. Calculations run in your browser.</p>
<h2 id="writing">Writing standards</h2><ul><li>Plain language, short sentences and defined terms.</li><li>Absolute numbers alongside relative risks when we can.</li><li>No promises of cures, no fear-based headlines and no promotion of unproven treatments.</li><li>Clear signposting to professional care, including when symptoms need urgent attention.</li></ul>
<h2 id="review">Review and updates</h2><p>Each page shows the date it was last updated. We review every page at least once a year and promptly when a major guideline changes. Licensed clinicians are being recruited as medical reviewers (see <a href="careers.html">Careers</a>); when a page has been clinically reviewed, the reviewer's name, credentials and review date will appear on it.</p>
<h2 id="ai">Use of software and AI</h2><p>We use software tools, including AI writing assistants, to help research, draft and check content. A human editor checks every page against its cited sources before publishing, and we do not publish personalised medical advice.</p>
<h2 id="independence">Independence from advertisers</h2><p>Advertising and sponsorship are clearly labelled and kept separate from editorial content. Sponsors cannot change formulas, results, rankings or wording. We do not accept advertising that conflicts with our <a href="advertise.html#standards">advertising standards</a>.</p>
<h2 id="automated">Automated feeds</h2><p>Health Pulse and the video library refresh automatically from public sources. We show headlines and titles with links to the original, and inclusion is not endorsement.</p>
<h2 id="corrections">Corrections</h2><p>Found an error? Tell us through the <a href="contact.html">contact form</a> (topic: correction). We review every report, fix verified errors quickly and note significant corrections on the page.</p>
"""

DISCLAIMER = """
<p><b>Prime.Health does not provide medical advice.</b> All content, including calculators, the Prime Score, guides, videos and news, is for general information and education only. It is not a substitute for professional medical advice, diagnosis or treatment.</p>
<h2 id="no-relationship">No clinician-patient relationship</h2><p>Using this website does not create a doctor-patient or any other professional relationship. Always seek the advice of your physician or another qualified health provider with any questions about a medical condition, and never disregard professional advice or delay seeking it because of something you read here.</p>
<h2 id="emergencies">Emergencies</h2><p>If you think you may have a medical emergency, call your local emergency number immediately. In the U.S. and Canada call 911. If you are in crisis or thinking about harming yourself, call or text 988 in the U.S. and Canada, or contact local emergency services.</p>
<h2 id="calculators">Calculators and scores</h2><p>Calculator results and the Prime Score are estimates based on published formulas and population averages. They can be inaccurate for individuals, may not apply to children, pregnancy, older adults or people with medical conditions, and are not diagnostic. Discuss results with a professional before making changes to medication, diet or exercise.</p>
<h2 id="third-party">Third-party content</h2><p>Videos and news headlines come from third parties. We do not control and are not responsible for their content. Links are provided for convenience and do not imply endorsement.</p>
<h2 id="accuracy">Accuracy</h2><p>We work to keep information accurate and current, but medical knowledge changes and errors can occur. Information is provided “as is” without warranties of any kind.</p>
"""

PRIVACY = """
<p>This policy explains what information Prime.Health (“we”) collects, how we use it and your choices. We designed the site to collect as little as possible.</p>
<h2 id="summary">Summary</h2><ul><li>Calculators and the Prime Score run in your browser. We do not receive what you type unless you submit a form.</li><li>Saved numbers, theme and unit settings are stored in your browser's local storage on your device.</li>
<li>Forms you submit (plan requests, newsletter, contact, pledges, challenge entries, job applications, advertising inquiries) are delivered to our inbox through a form-processing service.</li>
<li>Google AdSense may use cookies to serve and measure ads.</li><li>We do not sell personal information. We share a plan request with a partner only if you tick the partner-matching consent box.</li></ul>
<h2 id="collect">Information we collect</h2>
<p><b>Information you give us:</b> name, email, country, optional phone number, answers in the plan form, Prime Score summary (if you choose to send it), messages, pledge details and application materials.</p>
<p><b>Collected automatically:</b> our host (GitHub Pages) and service providers process technical data such as IP address, browser type and pages requested to deliver and secure the site. Advertising partners may collect device identifiers and cookie data as described below. The form records the page you submitted from and any campaign tags in the link you followed.</p>
<h2 id="use">How we use information</h2><ul><li>To send the plan, newsletter or reply you asked for.</li><li>To run the challenge, process pledges and review applications.</li><li>To connect you with a vetted professional, only if you opt in to partner matching.</li><li>To keep the site secure, fix problems and improve content.</li><li>To show advertising that funds the free service.</li></ul>
<h2 id="processors">Service providers</h2><ul><li><b>FormSubmit</b> (formsubmit.co) relays form submissions to our inbox.</li><li><b>GitHub Pages</b> hosts the website.</li><li><b>Google</b> provides AdSense advertising, Google Fonts and, when you press play, YouTube video embeds in privacy-enhanced mode (youtube-nocookie.com).</li><li>Payment providers you choose on the Support page (for example Stripe or PayPal) process payments under their own privacy policies; we never receive full card details.</li></ul>
<h2 id="advertising">Advertising and cookies</h2>
<p>Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to this and other sites on the internet. You may opt out of personalised advertising by visiting <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a> or <a href="https://www.youronlinechoices.eu/" target="_blank" rel="noopener">youronlinechoices.eu</a>. Learn <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses information from sites that use its services</a>. Visitors in the European Economic Area, the UK and Switzerland are shown a consent message through Google's certified consent management platform. See our <a href="cookie-policy.html">cookie policy</a>.</p>
<h2 id="sharing">Sharing</h2><p>We share personal information only with the service providers above, with a vetted partner when you explicitly ask to be matched, when required by law, or to protect rights and safety. If the website is sold or transferred, information may transfer to the new owner under this policy.</p>
<h2 id="retention">Retention</h2><p>We keep form submissions for as long as needed for the purpose you submitted them, typically up to 24 months, unless the law requires longer. Newsletter data is kept until you unsubscribe.</p>
<h2 id="rights">Your rights</h2><p>Depending on where you live (for example under the GDPR, UK GDPR, Canada's PIPEDA, Quebec's Law 25 or U.S. state laws such as the CCPA/CPRA), you may have rights to access, correct, delete or port your data, to withdraw consent and to object to certain processing. To exercise them, use the <a href="contact.html">contact form</a> with the topic “Privacy request”. The person in charge of the protection of personal information can be reached the same way. You may also complain to your local data protection authority.</p>
<h2 id="children">Children</h2><p>Prime.Health is intended for adults. We do not knowingly collect personal information from children under 16. Contests are open to adults 18 and over.</p>
<h2 id="security">Security and international transfer</h2><p>The site is served over HTTPS. Our providers may process data in the United States, Canada and other countries with appropriate safeguards.</p>
<h2 id="changes">Changes</h2><p>We will post any changes on this page and update the date above.</p>
"""

COOKIES = """
<p>This policy explains how Prime.Health uses cookies and similar technologies such as local storage.</p>
<h2 id="what">What we use</h2>
<table><thead><tr><th>Type</th><th>Purpose</th><th>Set by</th></tr></thead><tbody>
<tr><td>Local storage: preferences</td><td>Remembers theme, units, cookie notice and offer dismissal</td><td>Prime.Health (stays on your device)</td></tr>
<tr><td>Local storage: My Numbers</td><td>Keeps results you choose to save, and your challenge tracker</td><td>Prime.Health (stays on your device)</td></tr>
<tr><td>Advertising cookies</td><td>Serve, personalise (where permitted) and measure ads; limit ad frequency; prevent fraud</td><td>Google and its partners</td></tr>
<tr><td>Video (on play only)</td><td>Play embedded videos in privacy-enhanced mode</td><td>YouTube (Google)</td></tr></tbody></table>
<p>We do not use analytics cookies at this time.</p>
<h2 id="control">Your choices</h2><ul><li>Visitors in the EEA, UK and Switzerland can accept, reject or customise advertising cookies through the consent message shown by Google's certified consent platform.</li>
<li>Manage personalised ads at <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>.</li>
<li>Block or delete cookies and site data in your browser settings. Clearing site data also removes My Numbers.</li></ul>
<p>More detail is in our <a href="privacy-policy.html">privacy policy</a>.</p>
"""

TERMS = """
<p>By using Prime.Health (the “Site”) you agree to these terms. If you do not agree, please do not use the Site.</p>
<h2 id="use">Use of the Site</h2><p>You may use the Site for personal, non-commercial purposes. Do not misuse it, attempt to disrupt it, scrape it at scale, or use it for unlawful purposes.</p>
<h2 id="medical">Not medical advice</h2><p>The Site provides general information only. Read the <a href="medical-disclaimer.html">medical disclaimer</a>; it forms part of these terms.</p>
<h2 id="ip">Intellectual property</h2><p>Text, design, graphics, calculators and code on the Site are owned by Prime.Health or its licensors and protected by copyright. You may share links and quote brief excerpts with attribution and a link back. Trademark and copyright details are in our <a href="trademark.html">trademark and copyright disclosure</a>.</p>
<h2 id="submissions">Your submissions</h2><p>You are responsible for information you submit. By sending feedback or ideas you allow us to use them without obligation.</p>
<h2 id="contests">Contests, pledges and partners</h2><p>Contests are governed by their <a href="challenge.html#rules">official rules</a>. Contributions on the Support page are voluntary, not tax-deductible and generally non-refundable, except where required by law or in case of error; contact us within 14 days. Partner professionals are independent; we do not provide or supervise their services.</p>
<h2 id="links">Third-party links and content</h2><p>We are not responsible for third-party websites, videos, news or advertisements.</p>
<h2 id="liability">Disclaimers and limitation of liability</h2><p>The Site is provided “as is” and “as available”. To the fullest extent permitted by law, Prime.Health disclaims all warranties and is not liable for indirect, incidental or consequential damages arising from use of the Site. Nothing in these terms limits liability that cannot be limited by law.</p>
<h2 id="law">Governing law</h2><p>These terms are governed by the laws of the Province of Quebec and the federal laws of Canada applicable there, without regard to conflict-of-law rules, unless the law of your place of residence requires otherwise.</p>
<h2 id="changes">Changes</h2><p>We may update these terms. Continued use after changes means you accept them.</p>
"""

TRADEMARK = """
<h2 id="independent">Independent website</h2><p>Prime.Health is an independent health information website. It is <b>not affiliated with, sponsored by, endorsed by or connected to</b> any company, hospital system, clinic, insurer, product or service that uses the names “Prime Health”, “PrimeHealth”, “Prime Healthcare” or any similar name or mark, or any other trademark owner whose names may appear on this site.</p>
<h2 id="our-name">Our name</h2><p>Our name is always written “Prime.Health”, as a domain name, with its own logo. It describes the site's subject, health in your prime, and is not used to suggest any association with other businesses. If you believe any content on this site infringes your rights, please contact us and we will review it promptly.</p>
<h2 id="third-party">Third-party marks</h2><p>All third-party names, trademarks and logos mentioned on Prime.Health (for example names of organisations, guidelines, studies, products, devices or YouTube channels) are the property of their respective owners. They are used for identification and reference only. Their use does not imply endorsement by or affiliation with those owners. “Life's Essential 8” is a mark of the American Heart Association; the Prime Score is independently developed and not endorsed by the AHA.</p>
<h2 id="copyright">Copyright</h2><p>© 2026 Prime.Health. All original text, graphics, calculators, code and the overall design of this site are protected by copyright. Formulas and clinical thresholds are cited from public scientific sources and remain the work of their authors. Headlines and video titles shown in Health Pulse and the video library belong to their publishers and link to the original sources. Embedded videos are provided by YouTube under its terms.</p>
<h2 id="notices">Notices and takedown</h2><p>To report a trademark or copyright concern, use the <a href="contact.html">contact form</a> with your name, the material concerned, its location on this site, and a statement of your rights. For questions about acquiring the website or domain name, use <a href="https://web.works/contact" target="_blank" rel="noopener">web.works/contact</a>.</p>
"""

ACCESS = """
<p>We want Prime.Health to work for everyone. We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.2 at level AA.</p>
<h2 id="features">What we do</h2><ul><li>Keyboard access to every control, with visible focus and a skip-to-content link.</li><li>Labels on every form field and live announcements for calculator results.</li>
<li>Text contrast designed for at least 4.5:1, plus a dark theme.</li><li>Charts and range bars include text alternatives with the value and category.</li><li>Animations respect the reduced-motion setting.</li><li>Pages work when zoomed to 200% and on small screens.</li></ul>
<h2 id="known">Known limitations</h2><p>Embedded third-party videos may not meet every criterion, and some older PDFs we link to are outside our control.</p>
<h2 id="feedback">Feedback</h2><p>If anything is hard to use, tell us through the <a href="contact.html">contact form</a>. We aim to respond within two business days.</p>
"""

BASE_SCRIPT = ("<script>document.write('<base href=\"'+(location.pathname.indexOf('/prime.health/')===0?'/prime.health/':'/')+'\">')</script>")


def not_found():
    main = '''<div class="wrap" style="padding:60px 20px;text-align:center"><h1>That page has flatlined</h1>
<p class="lede" style="margin-inline:auto">The address may be mistyped or the page may have moved. Try the search, or start from one of these.</p>
<p><a class="btn btn-primary" href="./">Home</a> <a class="btn btn-ghost" href="tools/">All tools</a> <a class="btn btn-ghost" href="prime-score.html">Prime Score</a> <a class="btn btn-ghost" href="guides/">Guides</a></p></div>'''
    return {"path": "404.html", "title": "Page not found", "desc": "This page could not be found.", "main": main, "ads": False, "robots": "noindex,follow",
            "sitemap": False, "search": False, "head_first": BASE_SCRIPT, "slidein": False}


def build(ctx):
    return [
        doc("editorial-policy.html", "Editorial Policy", "How Prime.Health chooses sources, builds calculators, reviews content, handles AI tools, separates advertising and corrects errors.", "Editorial policy", EDITORIAL, "Editorial policy"),
        doc("medical-disclaimer.html", "Medical Disclaimer", "Prime.Health provides general health information for education. It is not medical advice, diagnosis or treatment.", "Medical disclaimer", DISCLAIMER, "Medical disclaimer"),
        doc("privacy-policy.html", "Privacy Policy", "What Prime.Health collects, how forms and advertising cookies work, and your privacy rights.", "Privacy policy", PRIVACY, "Privacy policy"),
        doc("cookie-policy.html", "Cookie Policy", "How Prime.Health uses local storage and Google advertising cookies, and how to control them.", "Cookie policy", COOKIES, "Cookie policy"),
        doc("terms.html", "Terms of Use", "The terms that govern your use of Prime.Health.", "Terms of use", TERMS, "Terms of use"),
        doc("trademark.html", "Trademark and Copyright Disclosure", "Prime.Health is independent and not affiliated with any company using the names Prime Health, PrimeHealth or Prime Healthcare. Copyright and third-party mark notices.", "Trademark and copyright disclosure", TRADEMARK, "Trademark & copyright"),
        doc("accessibility.html", "Accessibility Statement", "Prime.Health aims to meet WCAG 2.2 AA. Features, known limitations and how to give feedback.", "Accessibility statement", ACCESS, "Accessibility"),
        not_found(),
    ]
