/* Prime.Health — site script. No dependencies. */
const CONFIG = {
  adClient: 'ca-pub-6620975821265271',
  // Paste AdSense ad-unit slot IDs after approval. Empty = slot stays hidden (auto ads still run).
  adSlots: { top: '', result: '', inArticle: '', sidebar: '', footer: '' },
  // Optional FormSubmit alias (shown after you activate the form). Replaces the encoded inbox.
  formAlias: '',
  // One-click donation links. Any filled link shows as a button on the Support page.
  payLinks: { stripe: '', paypal: '', buymeacoffee: '', kofi: '' },
  contactUrl: 'https://web.works/contact'
};

(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const store = {
    get(k, d) { try { const v = localStorage.getItem('ph:' + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('ph:' + k, JSON.stringify(v)); } catch (e) { /* storage off */ } },
    del(k) { try { localStorage.removeItem('ph:' + k); } catch (e) { /* ignore */ } }
  };
  const ROOT = document.body.dataset.root || '';
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  // Inbox is stored encoded and decoded only when a message is sent. Never rendered on the page.
  const _e = [70, 68, 72, 5, 71, 66, 74, 70, 76, 107, 26, 74, 88, 64, 89, 68, 92, 73, 78, 92];
  const inbox = () => _e.map(c => String.fromCharCode(c ^ 0x2B)).reverse().join('');

  const copy = async text => {
    try { await navigator.clipboard.writeText(text); return true; } catch (e) {
      const t = document.createElement('textarea'); t.value = text; document.body.appendChild(t); t.select();
      let ok = false; try { ok = document.execCommand('copy'); } catch (er) { ok = false; } t.remove(); return ok;
    }
  };

  window.PH = { CONFIG, store, copy, esc, root: ROOT };

  /* theme */
  const html = document.documentElement;
  $('#themeToggle')?.addEventListener('click', () => {
    const cur = html.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = cur === 'dark' ? 'light' : 'dark';
    html.dataset.theme = next; store.set('theme', next);
  });

  /* mobile menu */
  const menuBtn = $('#menuBtn'), nav = $('#mainNav');
  menuBtn?.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav?.classList.contains('open')) { nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); menuBtn.focus(); } });

  /* year */
  $$('[data-year]').forEach(n => { n.textContent = new Date().getFullYear(); });

  /* UTM capture */
  try {
    const q = new URLSearchParams(location.search); const utm = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'ref'].forEach(k => { if (q.get(k)) utm[k] = q.get(k); });
    if (Object.keys(utm).length) sessionStorage.setItem('ph:utm', JSON.stringify(utm));
    if (!sessionStorage.getItem('ph:landing')) sessionStorage.setItem('ph:landing', location.pathname);
  } catch (e) { /* ignore */ }

  /* search */
  const dlg = $('#searchDialog'), sIn = $('#searchInput'), sOut = $('#searchResults');
  let index = null;
  const openSearch = async () => {
    if (!dlg) return;
    if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
    sIn.focus();
    if (!index) { try { index = await (await fetch(ROOT + 'search-index.json')).json(); } catch (e) { index = []; } }
    runSearch();
  };
  const runSearch = () => {
    const q = (sIn.value || '').trim().toLowerCase();
    if (!index) return;
    const words = q.split(/\s+/).filter(Boolean);
    const scored = index.map(it => {
      const t = it.t.toLowerCase(), d = (it.d || '').toLowerCase();
      let s = 0; words.forEach(w => { if (t.includes(w)) s += 3; if (d.includes(w)) s += 1; });
      if (!words.length) s = it.k === 'Tool' ? 1 : 0;
      return [s, it];
    }).filter(x => x[0] > 0).sort((a, b) => b[0] - a[0]).slice(0, 12);
    sOut.innerHTML = scored.length ? scored.map(([, it]) => `<li><a href="${ROOT}${esc(it.u)}">${esc(it.t.replace(/ \| Prime\.Health$/, ''))}<small>${esc(it.k)}: ${esc(it.d)}</small></a></li>`).join('')
      : '<li class="empty">No match. Try "sleep", "protein" or "blood pressure".</li>';
  };
  $('#searchOpen')?.addEventListener('click', openSearch);
  sIn?.addEventListener('input', runSearch);
  document.addEventListener('keydown', e => {
    const tag = (e.target.tagName || '').toLowerCase();
    if (e.key === '/' && !['input', 'textarea', 'select'].includes(tag) && !e.target.isContentEditable) { e.preventDefault(); openSearch(); }
  });
  dlg?.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });

  /* ads: render manual slots only when an ad-unit ID is configured */
  $$('.ad-slot').forEach(slot => {
    const id = CONFIG.adSlots[slot.dataset.ad];
    if (!id) { slot.remove(); return; }
    slot.classList.add('is-live');
    const ins = document.createElement('ins');
    ins.className = 'adsbygoogle'; ins.style.display = 'block';
    ins.setAttribute('data-ad-client', CONFIG.adClient); ins.setAttribute('data-ad-slot', id);
    ins.setAttribute('data-ad-format', slot.dataset.format || 'auto'); ins.setAttribute('data-full-width-responsive', 'true');
    slot.appendChild(ins);
    try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) { /* blocked */ }
  });

  /* mail links: built only at click time */
  $$('[data-mail]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    const subj = encodeURIComponent(a.dataset.mail || 'Prime.Health inquiry');
    location.href = 'mailto:' + inbox() + '?subject=' + subj;
  }));

  /* forms (FormSubmit AJAX) */
  const collect = form => {
    const fd = new FormData(form), data = {};
    for (const [k, v] of fd.entries()) {
      if (k === '_honey') continue;
      const val = typeof v === 'string' ? v.trim() : v.name;
      if (val === '') continue;
      data[k] = data[k] ? data[k] + ', ' + val : val;
    }
    return data;
  };
  const send = async (form) => {
    const hp = form.querySelector('[name=_honey]');
    if (hp && hp.value) return true; // bot
    const data = collect(form);
    const name = form.dataset.form || 'Website form';
    data._subject = `[Prime.Health] ${name}`;
    data._template = 'table';
    data._captcha = 'false';
    data.form = name;
    data.page = location.href;
    data.submitted = new Date().toISOString();
    try { const u = sessionStorage.getItem('ph:utm'); if (u) Object.assign(data, JSON.parse(u)); data.landing = sessionStorage.getItem('ph:landing') || ''; } catch (e) { /* ignore */ }
    const score = store.get('score', null); if (score && !data.prime_score) data.prime_score = String(score.overall);
    const endpoint = 'https://formsubmit.co/ajax/' + (CONFIG.formAlias || inbox());
    const res = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return true;
  };
  const fallback = (form, err) => {
    let box = form.querySelector('.form-error');
    if (!box) { box = document.createElement('p'); box.className = 'form-error'; box.setAttribute('role', 'alert'); form.appendChild(box); }
    box.innerHTML = 'We could not send that just now. <button type="button" class="link-btn">Send it by email instead</button>.';
    box.querySelector('button').addEventListener('click', () => {
      const data = collect(form);
      const body = Object.entries(data).map(([k, v]) => `${k}: ${v}`).join('\n');
      location.href = 'mailto:' + inbox() + '?subject=' + encodeURIComponent('[Prime.Health] ' + (form.dataset.form || 'Form')) + '&body=' + encodeURIComponent(body);
    });
    console.warn('Form send failed', err);
  };
  const validate = scope => {
    const fields = $$('input,select,textarea', scope).filter(f => !f.disabled && f.type !== 'hidden' && !f.closest('[hidden]'));
    for (const f of fields) { if (!f.checkValidity()) { f.reportValidity(); f.focus(); return false; } }
    return true;
  };
  $$('form[data-form]').forEach(form => {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (!validate(form)) return;
      const btn = form.querySelector('[type=submit]');
      const label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      try {
        await send(form);
        const msg = form.dataset.success || 'Thanks. We received your message and will reply within two business days.';
        const done = document.createElement('div');
        done.className = 'form-success'; done.setAttribute('role', 'status'); done.tabIndex = -1;
        done.innerHTML = `<h3>Received</h3><p>${msg}</p>`;
        form.replaceWith(done); done.focus();
      } catch (err) {
        if (btn) { btn.disabled = false; btn.textContent = label; }
        fallback(form, err);
      }
    });
  });

  /* multi-step forms */
  $$('form[data-steps]').forEach(form => {
    const steps = $$('.step', form), bar = $('.progress-track span', form), count = $('.step-count', form);
    let i = 0;
    const show = n => {
      i = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach((s, k) => { s.hidden = k !== i; });
      if (bar) bar.style.width = ((i + 1) / steps.length * 100) + '%';
      if (count) count.textContent = `Step ${i + 1} of ${steps.length}`;
      const first = steps[i].querySelector('input:not([type=hidden]),select,textarea');
      if (n !== 0 || form.dataset.touched) first?.focus({ preventScroll: true });
      form.dataset.touched = '1';
    };
    form.addEventListener('click', e => {
      const nxt = e.target.closest('[data-next]'), back = e.target.closest('[data-back]');
      if (nxt) { e.preventDefault(); if (validate(steps[i])) { show(i + 1); form.scrollIntoView({ block: 'start', behavior: 'smooth' }); } }
      if (back) { e.preventDefault(); show(i - 1); }
    });
    // auto-advance on single-choice radios
    form.addEventListener('change', e => {
      if (e.target.type === 'radio' && e.target.closest('.step')?.dataset.auto === '1') setTimeout(() => { if (validate(steps[i])) show(i + 1); }, 180);
    });
    show(0);
  });

  /* YouTube click-to-load */
  document.addEventListener('click', e => {
    const b = e.target.closest('.yt[data-id]');
    if (!b || b.querySelector('iframe')) return;
    const f = document.createElement('iframe');
    f.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(b.dataset.id)}?autoplay=1&rel=0`;
    f.title = b.getAttribute('aria-label') || 'YouTube video';
    f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    f.allowFullscreen = true; b.appendChild(f);
  });

  /* filters (pulse, videos) */
  $$('[data-filter-group]').forEach(group => {
    const target = $(group.dataset.filterGroup);
    group.addEventListener('click', e => {
      const btn = e.target.closest('button[data-filter]'); if (!btn) return;
      $$('button', group).forEach(b => b.setAttribute('aria-pressed', String(b === btn)));
      const f = btn.dataset.filter;
      $$('[data-cat]', target).forEach(it => { it.hidden = f !== 'all' && it.dataset.cat !== f; });
    });
  });

  /* daily tip + monthly observance */
  const TIPS = [
    'Take a 10-minute walk after your largest meal. Post-meal walks blunt blood-sugar spikes.',
    'Measure your waist today. Keep it under half your height.',
    'Add one palm-sized portion of protein to breakfast.',
    'Set a fixed wake-up time for the next 7 days, weekends included.',
    'Check your blood pressure twice, 1 minute apart, and average the readings.',
    'Swap one sugary drink for water or sparkling water today.',
    'Do two sets of push-ups and squats while the kettle boils.',
    'Aim for 30 g of fibre: beans, oats, berries and vegetables get you there.',
    'Try 20 minutes of Zone 2: a pace where you can talk but not sing.',
    'Put your phone outside the bedroom tonight.',
    'Stand up and move for 2 minutes every half hour you sit.',
    'Book any screening you are due for. Use the screening planner to check.',
    'Get 10 minutes of outdoor light within an hour of waking.',
    'Eat a vegetable you have not eaten this week.',
    'Carry something heavy for 60 seconds. Grip strength tracks with healthy ageing.',
    'Keep caffeine to before 2 pm if sleep is a struggle.',
    'Write down three things that went well today. It is a small, studied stress buffer.',
    'Climb the stairs instead of the lift for every trip today.',
    'Drink a glass of water with every meal.',
    'Call or meet a friend. Social connection is a health number too.',
    'Practise 5 minutes of slow breathing: in for 4, out for 6.',
    'Plan two strength sessions for this week and put them in your calendar.',
    'Choose olive oil, nuts or seeds as your main added fats today.',
    'Take your resting pulse before getting out of bed. Note it for the week.',
    'Have one alcohol-free day more this week than last week.',
    'Stretch your hips and calves for 5 minutes before bed.',
    'Add 1,000 steps to your daily average this week.',
    'Cook one meal at home instead of ordering in.',
    'Check your sleep debt with the calculator and pay back 30 minutes tonight.',
    'Balance on one leg while brushing your teeth.'
  ];
  const OBS = [
    ['January', 'Cervical Health Awareness Month', 'tools/screenings.html', 'Check which screenings are due for you'],
    ['February', 'Heart Month', 'tools/blood-pressure.html', 'Check your blood pressure category'],
    ['March', 'Nutrition Month and Colorectal Cancer Awareness Month', 'tools/screenings.html', 'See if colorectal screening is due'],
    ['April', 'Stress Awareness Month', 'guides/stress-recovery.html', 'Read the stress and recovery guide'],
    ['May', 'Mental Health Awareness Month and May Measurement Month', 'tools/blood-pressure.html', 'Measure and log your blood pressure'],
    ['June', 'Men’s Health Month', 'prime-score.html', 'Take the 3-minute Prime Score'],
    ['July', 'UV Safety Month', 'tools/water.html', 'Work out your hot-weather water needs'],
    ['August', 'Immunization Awareness Month', 'tools/screenings.html', 'Review your preventive care checklist'],
    ['September', 'Healthy Aging Month', 'guides/strength-training.html', 'Start a two-day strength routine'],
    ['October', 'Breast Cancer Awareness Month', 'tools/screenings.html', 'Check when mammograms are recommended'],
    ['November', 'Diabetes Awareness Month', 'tools/a1c.html', 'Convert your A1C and see your range'],
    ['December', 'Holiday season: sleep and alcohol check-in', 'tools/sleep-debt.html', 'Measure your sleep debt']
  ];
  const now = new Date();
  const doy = Math.floor((now - new Date(now.getFullYear(), 0, 0)) / 864e5);
  $$('[data-tip]').forEach(n => { n.textContent = TIPS[doy % TIPS.length]; });
  $$('[data-observance]').forEach(n => {
    const o = OBS[now.getMonth()];
    n.innerHTML = `<h3>${esc(o[0])}: ${esc(o[1])}</h3><p>Use this month as your prompt to act on one number.</p><a class="btn btn-ghost btn-sm" href="${ROOT}${o[2]}">${esc(o[3])}</a>`;
  });

  /* support page: amount, frequency, pay links or pledge */
  const give = $('.give');
  if (give) {
    let amount = 15, freq = 'monthly';
    const custom = $('#customAmount', give), out = $('#giveOut', give);
    const sync = () => {
      $$('[data-amount]', give).forEach(b => b.setAttribute('aria-pressed', String(Number(b.dataset.amount) === amount && !custom.value)));
      $$('[data-freq]', give).forEach(b => b.setAttribute('aria-pressed', String(b.dataset.freq === freq)));
      $('#giveSummary', give).textContent = `$${amount} ${freq === 'monthly' ? 'per month' : 'one time'}`;
    };
    give.addEventListener('click', e => {
      const a = e.target.closest('[data-amount]'), f = e.target.closest('[data-freq]');
      if (a) { amount = Number(a.dataset.amount); custom.value = ''; sync(); }
      if (f) { freq = f.dataset.freq; sync(); }
    });
    custom?.addEventListener('input', () => { const v = Math.round(Number(custom.value)); if (v > 0) amount = v; sync(); });
    $('#giveGo', give)?.addEventListener('click', () => {
      const names = { stripe: 'Pay by card (Stripe)', paypal: 'PayPal', buymeacoffee: 'Buy Me a Coffee', kofi: 'Ko-fi' };
      const links = Object.entries(CONFIG.payLinks).filter(([, u]) => u);
      if (links.length) {
        out.innerHTML = `<p>Choose how to give <b>$${amount} ${freq === 'monthly' ? 'per month' : 'once'}</b>:</p><div class="pay-options">` +
          links.map(([k, u]) => `<a class="btn btn-primary" href="${esc(u)}" target="_blank" rel="noopener">${names[k] || k}</a>`).join('') + '</div>';
      } else {
        const pf = $('#pledge');
        if (pf) { pf.querySelector('[name=amount]').value = '$' + amount; pf.querySelector('[name=frequency]').value = freq; pf.scrollIntoView({ behavior: 'smooth', block: 'start' }); setTimeout(() => pf.querySelector('[name=name]')?.focus(), 400); }
        out.innerHTML = '<p>Secure online checkout opens soon. Leave your pledge below and we will send a payment link within one business day.</p>';
      }
    });
    sync();
  }

  /* challenge tracker */
  const tracker = $('.tracker');
  if (tracker) {
    const key = 'challenge:' + now.getFullYear() + '-' + (now.getMonth() + 1);
    const saved = store.get(key, []);
    tracker.innerHTML = Array.from({ length: 30 }, (_, k) => `<label><input type="checkbox" value="${k + 1}" ${saved.includes(k + 1) ? 'checked' : ''} aria-label="Day ${k + 1}"><span>${k + 1}</span></label>`).join('');
    const status = $('#trackerStatus');
    const upd = () => { const v = $$('input:checked', tracker).map(i => Number(i.value)); store.set(key, v); if (status) status.textContent = `${v.length} of 30 days done this month.`; };
    tracker.addEventListener('change', upd); upd();
  }

  /* My Numbers dashboard */
  const mine = $('#myNumbers');
  if (mine) {
    const draw = () => {
      const nums = store.get('numbers', {});
      const keys = Object.keys(nums);
      if (!keys.length) { mine.innerHTML = `<div class="empty"><p>No saved numbers yet. Run any calculator and press <b>Save to My Numbers</b>.</p><a class="btn btn-primary" href="${ROOT}tools/">Open the tools</a></div>`; return; }
      mine.innerHTML = '<ul class="my-list">' + keys.sort((a, b) => (nums[b].date || '').localeCompare(nums[a].date || '')).map(k => {
        const n = nums[k];
        return `<li><div><span>${esc(n.label)}</span><br><b>${esc(n.display)}</b></div><a class="btn btn-ghost btn-sm" href="${ROOT}${esc(n.url || 'tools/')}">Recheck</a><button class="btn btn-ghost btn-sm" data-del="${esc(k)}" type="button">Remove</button><small>${n.target ? 'Prime target: ' + esc(n.target) + '. ' : ''}Saved ${esc(new Date(n.date).toLocaleDateString())}</small></li>`;
      }).join('') + '</ul>';
    };
    mine.addEventListener('click', e => { const d = e.target.closest('[data-del]'); if (d) { const n = store.get('numbers', {}); delete n[d.dataset.del]; store.set('numbers', n); draw(); } });
    $('#exportNumbers')?.addEventListener('click', () => {
      const blob = new Blob([JSON.stringify({ numbers: store.get('numbers', {}), score: store.get('score', null) }, null, 2)], { type: 'application/json' });
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'my-prime-numbers.json'; a.click(); URL.revokeObjectURL(a.href);
    });
    $('#clearNumbers')?.addEventListener('click', () => { if (confirm('Remove all saved numbers from this device?')) { store.del('numbers'); store.del('score'); draw(); } });
    draw();
  }

  /* guide: reading progress + TOC highlight */
  const art = $('.prose[data-article]');
  if (art) {
    const bar = document.createElement('div'); bar.className = 'progress'; document.body.appendChild(bar);
    const links = $$('.toc a');
    const heads = links.map(a => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
    const onScroll = () => {
      const r = art.getBoundingClientRect(); const h = r.height - innerHeight;
      bar.style.width = Math.max(0, Math.min(100, (-r.top / (h > 0 ? h : 1)) * 100)) + '%';
      let cur = heads[0];
      heads.forEach(hd => { if (hd.getBoundingClientRect().top < 120) cur = hd; });
      links.forEach(a => a.classList.toggle('is-active', cur && a.getAttribute('href') === '#' + cur.id));
    };
    addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }

  /* slide-in plan offer: once per 7 days, never on form pages */
  if (document.body.dataset.slidein === '1') {
    const last = store.get('slidein', 0);
    if (Date.now() - last > 7 * 864e5) {
      let shown = false;
      const show = () => {
        if (shown) return; shown = true;
        const el = document.createElement('aside'); el.className = 'slidein'; el.setAttribute('aria-label', 'Free plan offer');
        el.innerHTML = `<button class="icon-btn x" type="button" aria-label="Close"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button><h2>Your free 30-day Prime Plan</h2><p>Four questions, then a plan built around your numbers lands in your inbox.</p><a class="btn btn-signal btn-block" href="${ROOT}get-your-plan.html">Build my plan</a>`;
        document.body.appendChild(el); requestAnimationFrame(() => el.classList.add('show'));
        el.querySelector('.x').addEventListener('click', () => { el.classList.remove('show'); store.set('slidein', Date.now()); setTimeout(() => el.remove(), 400); });
        el.querySelector('a').addEventListener('click', () => store.set('slidein', Date.now()));
      };
      setTimeout(show, 40000);
      addEventListener('scroll', () => { const d = document.documentElement; if ((d.scrollTop + innerHeight) / d.scrollHeight > 0.55) show(); }, { passive: true });
    }
  }

  /* cookie notice */
  if (!store.get('cookieok', false)) {
    const c = document.createElement('div'); c.className = 'cookie'; c.setAttribute('role', 'region'); c.setAttribute('aria-label', 'Cookie notice');
    c.innerHTML = `<p style="margin:0">We use cookies for ads and to remember your settings. Your calculator results stay on your device. <a href="${ROOT}cookie-policy.html">Cookie policy</a></p><button class="btn btn-sm" type="button">OK</button>`;
    document.body.appendChild(c);
    c.querySelector('button').addEventListener('click', () => { store.set('cookieok', true); c.remove(); });
  }
})();
