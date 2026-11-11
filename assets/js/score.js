/* Prime.Health — Prime Score (8 pillars, 0–100). Thresholds follow the published Life's Essential 8 approach. */
(() => {
  'use strict';
  const form = document.getElementById('primeScore');
  if (!form || !window.PHT) return;
  const PH = window.PH, PHT = window.PHT, R = PH.root;
  const out = document.getElementById('scoreOut');
  const pick = n => { const c = form.querySelector(`input[name="${n}"]:checked`); return c ? c.value : ''; };
  const PILLARS = {
    move: ['Move', 'Build toward 150 minutes of moderate activity a week. Brisk walking counts.', [['Heart rate zones', 'tools/heart-rate-zones.html'], ['Steps per day guide', 'guides/walking-steps.html']]],
    fuel: ['Fuel', 'Add one serving of vegetables or fruit a day and swap sugary drinks for water.', [['Eating for your prime', 'guides/nutrition-patterns.html'], ['Macro calculator', 'tools/macros.html']]],
    nicotine: ['Smoke-free', 'Quitting is the single biggest win available. Pair counselling with approved medicines.', [['Free quit support (smokefree.gov)', 'https://smokefree.gov/']]],
    sleep: ['Sleep', 'Aim for 7–9 hours with a fixed wake-up time, seven days a week.', [['Sleep guide', 'guides/sleep.html'], ['Sleep cycle calculator', 'tools/sleep.html']]],
    weight: ['Weight', 'Track your waist, not just the scale. Keep it under half your height.', [['Waist-to-height ratio', 'tools/waist-to-height.html'], ['Metabolic health guide', 'guides/metabolic-health.html']]],
    bp: ['Blood pressure', 'Measure at home for a week and average the readings. Below 120/80 is the target.', [['Blood pressure checker', 'tools/blood-pressure.html'], ['Blood pressure guide', 'guides/blood-pressure.html']]],
    glucose: ['Blood sugar', 'Ask for an A1C at your next check-up; a 10-minute walk after meals helps.', [['A1C converter', 'tools/a1c.html'], ['Metabolic health guide', 'guides/metabolic-health.html']]],
    chol: ['Cholesterol', 'Know your non-HDL number. Fibre, unsaturated fats and activity move it.', [['Cholesterol calculator', 'tools/cholesterol.html'], ['Your 8 Prime Numbers', 'guides/prime-numbers.html']]]
  };
  const link = ([t, u]) => `<a href="${/^https?:/.test(u) ? u : R + u}"${/^https?:/.test(u) ? ' target="_blank" rel="noopener"' : ''}>${t}</a>`;

  form.addEventListener('submit', e => {
    e.preventDefault();
    const s = {};
    const num = v => (v === '' || v === 'na' ? null : Number(v));
    s.move = num(pick('move'));
    const diet = ['d1', 'd2', 'd3', 'd4'].map(k => Number(pick(k) || 0)).reduce((a, b) => a + b, 0);
    s.fuel = diet >= 11 ? 100 : diet >= 9 ? 80 : diet >= 7 ? 50 : diet >= 4 ? 25 : 0;
    s.nicotine = num(pick('nicotine'));
    s.sleep = num(pick('sleep'));
    const v = PHT.read(form);
    if (v.height > 0 && v.weight > 0) {
      const b = v.weight / Math.pow(v.height / 100, 2);
      s.weight = b < 25 ? 100 : b < 30 ? 70 : b < 35 ? 30 : b < 40 ? 15 : 0;
      s._bmi = b;
    } else s.weight = null;
    s.bp = num(pick('bp')); if (s.bp !== null && form.querySelector('[name=bpmed]').checked) s.bp = Math.max(0, s.bp - 20);
    s.glucose = num(pick('glucose'));
    s.chol = num(pick('chol')); if (s.chol !== null && form.querySelector('[name=cholmed]').checked) s.chol = Math.max(0, s.chol - 20);

    const keys = Object.keys(PILLARS);
    const known = keys.filter(k => s[k] !== null && s[k] !== undefined);
    const unknown = keys.filter(k => !known.includes(k));
    if (known.length < 4) { alert('Answer at least four pillars to get a score.'); return; }
    const overall = Math.round(known.reduce((a, k) => a + s[k], 0) / known.length);
    const tone = overall >= 80 ? 'ok' : overall >= 50 ? 'warn' : 'high';
    const verdict = overall >= 80 ? 'High: you are in your prime' : overall >= 50 ? 'Moderate: room to climb' : 'Low: big gains are available';
    const wins = known.slice().sort((a, b) => s[a] - s[b]).filter(k => s[k] < 100).slice(0, 2);
    const bands = [[50, 'high', 'Low'], [80, 'warn', 'Moderate'], [101, 'ok', 'High']];

    let h = `<div class="panel" style="padding:28px"><p class="step-count">Your Prime Score</p><div class="score-dial"><span class="res-num num tone-${tone}">${overall}</span><span class="res-unit">/ 100</span></div><p class="res-verdict tone-${tone}">${verdict}</p>`;
    h += `<p>Based on ${known.length} of 8 pillars.${unknown.length ? ' Measure the missing ones to complete your score.' : ''}</p>`;
    h += '<div class="pillar-bars">' + known.map(k => PHT.bar({ label: PILLARS[k][0], value: s[k], min: 0, max: 100, fmt: x => String(Math.round(x)), bands })).join('') + '</div>';
    if (wins.length) h += '<h2 style="margin-top:28px">Your two biggest wins</h2><div class="wins">' + wins.map(k => `<div><h3>${PILLARS[k][0]}: ${s[k]}/100</h3><p>${PILLARS[k][1]}</p><p>${PILLARS[k][2].map(link).join(' · ')}</p></div>`).join('') + '</div>';
    if (unknown.length) h += '<h2>Measure next</h2><ul>' + unknown.map(k => `<li><b>${PILLARS[k][0]}</b>: ${PILLARS[k][2].map(link).join(', ')}</li>`).join('') + '</ul>';
    h += `<div class="res-actions"><a class="btn btn-ghost btn-sm" href="${R}my-numbers.html">Saved to My Numbers</a><button class="btn btn-ghost btn-sm" type="button" id="scoreCopy">Copy my score</button><button class="btn btn-ghost btn-sm" type="button" id="scoreRedo">Retake</button></div>`;
    h += '<p class="res-note">The Prime Score is an educational self-check inspired by the American Heart Association\'s Life\'s Essential 8 scoring. It is not affiliated with or endorsed by the AHA, and it is not a medical assessment.</p></div>';
    out.innerHTML = h; out.hidden = false;
    PHT.placeMarkers(out);

    const summary = known.map(k => `${PILLARS[k][0]} ${s[k]}`).join(', ');
    PH.store.set('score', { overall, pillars: s, date: new Date().toISOString() });
    const nums = PH.store.get('numbers', {});
    nums.prime = { label: 'Prime Score', display: `${overall}/100`, target: '80+', date: new Date().toISOString(), url: 'prime-score.html' };
    PH.store.set('numbers', nums);

    const lead = document.getElementById('scoreLead');
    if (lead) {
      lead.hidden = false;
      const f = lead.querySelector('form');
      if (f) { f.querySelector('[name=prime_score]').value = String(overall); f.querySelector('[name=pillars]').value = summary; f.querySelector('[name=focus]').value = wins.map(k => PILLARS[k][0]).join(', '); }
    }
    form.hidden = true;
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
    document.getElementById('scoreCopy')?.addEventListener('click', async ev => { const ok = await PH.copy(`My Prime Score is ${overall}/100 (${summary}). Get yours: ${location.href}`); ev.target.textContent = ok ? 'Copied' : 'Copy failed'; });
    document.getElementById('scoreRedo')?.addEventListener('click', () => { out.hidden = true; if (lead) lead.hidden = true; form.hidden = false; form.reset(); form.querySelector('[data-back]'); location.reload(); });
  });
})();
