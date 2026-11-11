/* Prime.Health — calculator engine. Every formula is documented on its tool page. */
(() => {
  'use strict';
  const PH = window.PH || { store: { get: (k, d) => d, set() {} }, copy: async () => false, esc: s => String(s), root: '' };
  const { store } = PH;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const LB = 0.45359237, IN = 2.54, MI = 1.609344;
  let units = store.get('units', /^en-US$/i.test(navigator.language || '') ? 'imperial' : 'metric');
  const imp = () => units === 'imperial';

  const nudge = v => Number(v) + (v >= 0 ? 1e-9 : -1e-9);
  const fx = (v, d) => nudge(v).toLocaleString(undefined, { minimumFractionDigits: d, maximumFractionDigits: d });
  const r0 = v => Math.round(nudge(v)).toLocaleString();
  const r1 = v => fx(v, 1);
  const r2 = v => fx(v, 2);
  const kg = v => imp() ? `${r1(v / LB)} lb` : `${r1(v)} kg`;
  const cmf = v => imp() ? `${r1(v / IN)} in` : `${r1(v)} cm`;
  const good = (...a) => a.every(v => Number.isFinite(v) && v > 0);
  const err = m => ({ error: m });
  const cat = (v, bands) => bands.find(b => v < b[0]) || bands[bands.length - 1];
  const parseDate = s => { const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || ''); return m ? new Date(+m[1], +m[2] - 1, +m[3]) : null; };
  const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
  const today = () => { const t = new Date(); return new Date(t.getFullYear(), t.getMonth(), t.getDate()); };
  const dayDiff = (a, b) => Math.round((a - b) / 864e5);
  const fdate = d => d.toLocaleDateString(undefined, { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });
  const parseTime = s => { const m = /^(\d{1,2}):(\d{2})/.exec(s || ''); return m ? (+m[1]) * 60 + (+m[2]) : NaN; };
  const ftime = mins => { const t = ((Math.round(mins) % 1440) + 1440) % 1440; return new Date(2000, 0, 1, Math.floor(t / 60), t % 60).toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' }); };
  const hm = h => { const t = Math.round(Math.abs(h) * 60); return `${Math.floor(t / 60)} h ${String(t % 60).padStart(2, '0')} min`; };
  const clock = s => { s = Math.round(s); const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60; return (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(x).padStart(2, '0'); };
  const mifflin = v => 10 * v.weight + 6.25 * v.height - 5 * v.age + (v.sex === 'm' ? 5 : -161);
  const needBasics = v => (!v.sex ? 'Choose your sex.' : !good(v.age) ? 'Enter your age.' : !good(v.height) ? 'Enter your height.' : !good(v.weight) ? 'Enter your weight.' : v.age < 18 ? 'This calculator is for adults 18 and over.' : '');

  /* ---------- read inputs (always returns metric) ---------- */
  const num = el => (el && el.value !== '' ? parseFloat(String(el.value).replace(',', '.')) : NaN);
  function read(form) {
    const o = {};
    $$('[data-field]', form).forEach(w => {
      const id = w.dataset.field, t = w.dataset.type, q = n => w.querySelector(`[name="${n}"]`);
      switch (t) {
        case 'height':
          if (imp()) { const f = q(id + '_ft'), i = q(id + '_in'); o[id] = (f.value === '' && i.value === '') ? NaN : ((num(f) || 0) * 12 + (num(i) || 0)) * IN; }
          else o[id] = num(q(id + '_cm'));
          break;
        case 'weight': o[id] = imp() ? num(q(id + '_lb')) * LB : num(q(id + '_kg')); break;
        case 'len': o[id] = imp() ? num(q(id + '_in')) * IN : num(q(id + '_cm')); break;
        case 'dist': o[id] = imp() ? num(q(id + '_mi')) * MI : num(q(id + '_km')); break;
        case 'radio': { const c = w.querySelector('input:checked'); o[id] = c ? c.value : ''; break; }
        case 'check': o[id] = !!(w.querySelector('input') && w.querySelector('input').checked); break;
        case 'select': o[id] = w.querySelector('select').value; break;
        case 'date': case 'time': o[id] = w.querySelector('input').value; break;
        default: o[id] = num(w.querySelector('input'));
      }
    });
    return o;
  }

  /* ---------- reference-range bar ---------- */
  function bar(b) {
    const span = b.max - b.min;
    const pct = x => ((Math.max(b.min, Math.min(b.max, x)) - b.min) / span) * 100;
    let prev = b.min, segs = '';
    for (const [to, tone, name] of b.bands) {
      if (prev >= b.max) break;
      const end = Math.min(to, b.max), w = pct(end) - pct(prev);
      if (w > 0) segs += `<span class="seg bg-${tone}" style="width:${w}%"><em>${name || ''}</em></span>`;
      prev = end;
    }
    const fmt = b.fmt || r1, c = cat(b.value, b.bands), lab = b.hideVerdict ? '' : (c[2] || '');
    return `<div class="rbar" role="img" aria-label="${PH.esc(b.label)}: ${PH.esc(fmt(b.value))}${lab ? ', ' + PH.esc(lab) : ''}">` +
      `<div class="rbar-head"><b>${b.label}</b><span class="tone-${c[1]}">${lab}</span></div>` +
      `<div class="rbar-track">${segs}<div class="rbar-marker" data-pos="${pct(b.value).toFixed(2)}"><span>${fmt(b.value)}</span></div></div><div class="rbar-scale"></div></div>`;
  }
  const placeMarkers = scope => requestAnimationFrame(() => requestAnimationFrame(() => $$('.rbar-marker', scope).forEach(m => {
    const p = +m.dataset.pos; m.style.left = p + '%'; m.style.transform = `translateX(${p < 8 ? -12 : p > 92 ? -88 : -50}%)`;
  })));

  /* ---------- calculators ---------- */
  const T = {
    bmi(v) {
      if (!good(v.height, v.weight)) return err('Enter your height and weight.');
      const m = v.height / 100, b = v.weight / (m * m), asian = v.asian;
      if (b < 8 || b > 90) return err('Check your entries: that BMI is outside the possible range.');
      const bands = asian ? [[18.5, 'low', 'Underweight'], [23, 'ok', 'Healthy'], [27.5, 'warn', 'Increased risk'], [99, 'high', 'High risk']]
        : [[18.5, 'low', 'Underweight'], [25, 'ok', 'Healthy'], [30, 'warn', 'Overweight'], [99, 'high', 'Obesity']];
      const c = cat(b, bands);
      let name = c[2];
      if (!asian && b >= 30) name = b >= 40 ? 'Obesity class III' : b >= 35 ? 'Obesity class II' : 'Obesity class I';
      const hi = asian ? 22.9 : 24.9, lo = 18.5;
      const prime = b / 25;
      const stats = [['BMI Prime', r2(prime)], ['Healthy weight for your height', `${kg(lo * m * m)} – ${kg(hi * m * m)}`]];
      if (b > hi + 0.05) stats.push(['Change to reach the healthy range', `−${kg(v.weight - hi * m * m)}`]);
      if (b < lo) stats.push(['Change to reach the healthy range', `+${kg(lo * m * m - v.weight)}`]);
      return {
        big: { value: r1(b), unit: 'kg/m²', label: 'Your BMI', verdict: name, tone: c[1] },
        bars: [
          { label: 'BMI', value: b, min: 12, max: 45, bands },
          { label: 'BMI Prime (BMI ÷ 25)', value: prime, min: 0.5, max: 1.8, fmt: r2,
            bands: asian ? [[0.74, 'low', 'Under'], [0.92, 'ok', 'Prime range'], [1.1, 'warn', 'Above'], [9, 'high', 'High']] : [[0.74, 'low', 'Under'], [1.0, 'ok', 'Prime range'], [1.2, 'warn', 'Over'], [9, 'high', 'Obese']] }
        ],
        stats,
        note: 'BMI cannot tell muscle from fat. Pair it with your waist-to-height ratio for a sharper picture.',
        save: { key: 'bmi', label: 'BMI', display: `${r1(b)} (BMI Prime ${r2(prime)})`, target: asian ? '18.5–22.9' : '18.5–24.9 (Prime 0.74–1.00)' }
      };
    },

    calories(v) {
      const e = needBasics(v); if (e) return err(e);
      const bmr = mifflin(v), f = parseFloat(v.activity) || 1.2, tdee = bmr * f, floor = v.sex === 'f' ? 1200 : 1500;
      const rows = [['Maintain current weight', tdee], ['Lose about 0.25 kg (0.5 lb) a week', tdee - 275], ['Lose about 0.5 kg (1 lb) a week', tdee - 550], ['Gain about 0.25 kg (0.5 lb) a week', tdee + 275]];
      const low = rows.some(r => r[1] < floor);
      return {
        big: { value: r0(tdee), unit: 'kcal/day', label: 'Estimated maintenance calories (TDEE)' },
        stats: [['Basal metabolic rate (BMR)', `${r0(bmr)} kcal/day`], ['Activity multiplier', `× ${f}`], ['Per meal, 3 meals', `${r0(tdee / 3)} kcal`]],
        table: { head: ['Goal', 'Calories per day'], rows: rows.map((r, i) => ({ cells: [r[0], r0(r[1]) + (r[1] < floor ? ' *' : '')], cls: i === 0 ? 'is-hl' : '' })) },
        note: (low ? `* Below ${floor} kcal a day it is hard to meet nutrient needs without professional guidance. ` : '') + 'Equations land within about 10% for most adults. Track your weight for 2–3 weeks and adjust by 100–200 kcal.',
        save: { key: 'tdee', label: 'Maintenance calories', display: `${r0(tdee)} kcal/day` }
      };
    },

    bmr(v) {
      const e = needBasics(v); if (e) return err(e);
      const m = mifflin(v);
      const hb = v.sex === 'm' ? 88.362 + 13.397 * v.weight + 4.799 * v.height - 5.677 * v.age : 447.593 + 9.247 * v.weight + 3.098 * v.height - 4.330 * v.age;
      const rows = [{ cells: ['Mifflin-St Jeor (recommended)', r0(m)], cls: 'is-hl' }, ['Harris-Benedict, revised 1984', r0(hb)]];
      if (good(v.bodyfat) && v.bodyfat < 70) rows.push(['Katch-McArdle (uses your body fat)', r0(370 + 21.6 * v.weight * (1 - v.bodyfat / 100))]);
      return {
        big: { value: r0(m), unit: 'kcal/day', label: 'Your basal metabolic rate' },
        stats: [['Per hour at complete rest', `${r1(m / 24)} kcal`], ['Daily needs if lightly active (×1.375)', `${r0(m * 1.375)} kcal`]],
        table: { head: ['Equation', 'BMR (kcal/day)'], rows },
        note: 'BMR is the energy your body burns at complete rest. Use the calorie calculator to add your activity.',
        save: { key: 'bmr', label: 'BMR', display: `${r0(m)} kcal/day` }
      };
    },

    macros(v) {
      const e = needBasics(v); if (e) return err(e);
      const tdee = mifflin(v) * (parseFloat(v.activity) || 1.2);
      const adj = { lose: -500, maintain: 0, gain: 300 }[v.goal] || 0;
      const kcal = Math.max(tdee + adj, v.sex === 'f' ? 1200 : 1500);
      const st = { balanced: [1.6, 0.30], lowcarb: [1.8, 0.40], highcarb: [1.4, 0.22] }[v.style] || [1.6, 0.30];
      const m = v.height / 100, bmi = v.weight / (m * m), refW = bmi > 30 ? 27.5 * m * m : v.weight;
      let P = st[0] * refW, F = (kcal * st[1]) / 9, C = (kcal - P * 4 - F * 9) / 4;
      if (C < 50) { C = 50; F = Math.max(20, (kcal - P * 4 - C * 4) / 9); }
      const tot = P * 4 + C * 4 + F * 9;
      const pc = x => (x / tot) * 100;
      return {
        big: { value: r0(kcal), unit: 'kcal/day', label: `Daily target to ${v.goal === 'lose' ? 'lose fat' : v.goal === 'gain' ? 'gain' : 'maintain'}` },
        split: [{ label: 'Protein', pct: pc(P * 4), tone: 'ok' }, { label: 'Carbs', pct: pc(C * 4), tone: 'warn' }, { label: 'Fat', pct: pc(F * 9), tone: 'low' }],
        table: { head: ['Macro', 'Grams per day', 'Per meal (3)', 'Per meal (4)'], rows: [['Protein', `${r0(P)} g`, `${r0(P / 3)} g`, `${r0(P / 4)} g`], ['Carbohydrate', `${r0(C)} g`, `${r0(C / 3)} g`, `${r0(C / 4)} g`], ['Fat', `${r0(F)} g`, `${r0(F / 3)} g`, `${r0(F / 4)} g`]] },
        stats: [['Maintenance (TDEE)', `${r0(tdee)} kcal`], ['Protein per kg body weight', `${r1(P / v.weight)} g/kg`]],
        note: (bmi > 30 ? 'Protein is set from a reference weight (BMI 27.5) because total-weight targets overshoot at higher BMIs. ' : '') + 'Fibre target: about 14 g per 1,000 kcal.',
        save: { key: 'macros', label: 'Macro targets', display: `${r0(kcal)} kcal: P ${r0(P)} g, C ${r0(C)} g, F ${r0(F)} g` }
      };
    },

    protein(v) {
      if (!good(v.weight)) return err('Enter your weight.');
      if (!good(v.age)) return err('Enter your age.');
      const R = { general: [0.8, 1.0], active: [1.2, 1.6], build: [1.6, 2.2], cut: [1.6, 2.4] };
      let [lo, hi] = R[v.goal] || R.general;
      if (v.age >= 65 && v.goal === 'general') { lo = 1.0; hi = 1.2; }
      const w = v.weight, mid = (lo + hi) / 2;
      const perKgLabel = imp() ? `${r2(lo * LB)}–${r2(hi * LB)} g per lb` : `${r1(lo)}–${r1(hi)} g per kg`;
      return {
        big: { value: `${r0(lo * w)}–${r0(hi * w)}`, unit: 'g/day', label: 'Your daily protein target' },
        bars: [{ label: 'Target intensity (g per kg)', value: mid, min: 0.6, max: 2.6, fmt: r1, bands: [[0.8, 'low', 'Below RDA'], [1.2, 'ok', 'Baseline'], [1.6, 'ok', 'Active'], [2.2, 'ok', 'Muscle gain'], [9, 'warn', 'Very high']] }],
        stats: [['Per meal, 4 meals', `${r0(lo * w / 4)}–${r0(hi * w / 4)} g`], ['Per-meal amount that maximizes muscle building', `about ${r0(0.4 * w)} g`], ['Range used', perKgLabel]],
        note: 'If you have kidney disease, ask your clinician before raising protein. Spread intake across meals; most people under-eat protein at breakfast.',
        save: { key: 'protein', label: 'Protein target', display: `${r0(lo * w)}–${r0(hi * w)} g/day` }
      };
    },

    'body-fat'(v) {
      const f = v.sex === 'f';
      if (!v.sex) return err('Choose your sex.');
      if (!good(v.height, v.neck, v.waist) || (f && !good(v.hip))) return err(f ? 'Enter height, neck, waist and hip.' : 'Enter height, neck and waist.');
      if (v.waist <= v.neck) return err('Waist must be larger than neck. Re-measure using the instructions below.');
      const L = Math.log10;
      const bf = f ? 495 / (1.29579 - 0.35004 * L(v.waist + v.hip - v.neck) + 0.22100 * L(v.height)) - 450
        : 495 / (1.0324 - 0.19077 * L(v.waist - v.neck) + 0.15456 * L(v.height)) - 450;
      if (!(bf > 2 && bf < 65)) return err('Those measurements give an implausible result. Re-measure at the points described below.');
      const bands = f ? [[14, 'low', 'Essential'], [21, 'ok', 'Athletes'], [25, 'ok', 'Fitness'], [32, 'warn', 'Average'], [99, 'high', 'Obese']]
        : [[6, 'low', 'Essential'], [14, 'ok', 'Athletes'], [18, 'ok', 'Fitness'], [25, 'warn', 'Average'], [99, 'high', 'Obese']];
      const c = cat(bf, bands);
      const stats = [];
      if (good(v.weight)) { stats.push(['Fat mass', kg(v.weight * bf / 100)], ['Lean mass', kg(v.weight * (1 - bf / 100))]); }
      stats.push(['Method', 'U.S. Navy circumference']);
      return {
        big: { value: r1(bf), unit: '%', label: 'Estimated body fat', verdict: c[2] + ' range', tone: c[1] },
        bars: [{ label: 'Body fat (ACE categories)', value: bf, min: 2, max: 45, bands }],
        stats,
        note: 'Tape methods are usually within 3–4 percentage points of lab methods. Measure the same way each time and track the trend.',
        save: { key: 'bodyfat', label: 'Body fat', display: `${r1(bf)}%`, target: f ? '21–31%' : '14–24%' }
      };
    },

    'ideal-weight'(v) {
      if (!v.sex) return err('Choose your sex.');
      if (!good(v.height)) return err('Enter your height.');
      const x = v.height / IN - 60, mm = v.sex === 'm';
      const F = [['Devine (1974)', mm ? 50 + 2.3 * x : 45.5 + 2.3 * x], ['Robinson (1983)', mm ? 52 + 1.9 * x : 49 + 1.7 * x], ['Miller (1983)', mm ? 56.2 + 1.41 * x : 53.1 + 1.36 * x], ['Hamwi (1964)', mm ? 48 + 2.7 * x : 45.5 + 2.2 * x]];
      const vals = F.map(r => r[1]), lo = Math.min(...vals), hi = Math.max(...vals), m = v.height / 100;
      return {
        big: { value: imp() ? `${r0(lo / LB)}–${r0(hi / LB)}` : `${r0(lo)}–${r0(hi)}`, unit: imp() ? 'lb' : 'kg', label: 'Ideal weight range across four formulas' },
        table: { head: ['Formula', 'Ideal weight'], rows: F.map(r => [r[0], kg(r[1])]) },
        stats: [['Healthy BMI range for your height (18.5–24.9)', `${kg(18.5 * m * m)} – ${kg(24.9 * m * m)}`]],
        note: (x < 0 ? 'These formulas were built for heights of 5 ft (152 cm) and above, so treat results below that height with caution. ' : '') + 'The formulas come from drug-dosing research, not health outcomes. The healthy BMI range is the better target for most adults.'
      };
    },

    'waist-to-height'(v) {
      if (!good(v.waist, v.height)) return err('Enter your waist and height.');
      const r = v.waist / v.height;
      if (r < 0.25 || r > 1.2) return err('Check your entries: use the same unit for both and measure the waist at the midpoint described below.');
      const bands = [[0.4, 'low', 'Below 0.4'], [0.5, 'ok', 'Healthy'], [0.6, 'warn', 'Increased risk'], [9, 'high', 'High risk']];
      const c = cat(r, bands);
      return {
        big: { value: r2(r), unit: '', label: 'Your waist-to-height ratio', verdict: c[2], tone: c[1] },
        bars: [{ label: 'Waist-to-height ratio', value: r, min: 0.3, max: 0.8, fmt: r2, bands }],
        stats: [['Keep your waist below', cmf(v.height / 2)], ['Difference from 0.5', r >= 0.5 ? `−${cmf(v.waist - v.height / 2)}` : 'Already below 0.5']],
        note: 'The simple rule: keep your waist to less than half your height.',
        save: { key: 'whtr', label: 'Waist-to-height ratio', display: r2(r), target: 'below 0.50' }
      };
    },

    'waist-to-hip'(v) {
      if (!v.sex) return err('Choose your sex.');
      if (!good(v.waist, v.hip)) return err('Enter your waist and hip.');
      const r = v.waist / v.hip, f = v.sex === 'f', thr = f ? 0.85 : 0.90;
      const rb = [[thr, 'ok', 'Below WHO cut-off'], [9, 'high', 'Above WHO cut-off']];
      const wb = f ? [[80, 'ok', 'Low'], [88, 'warn', 'Increased'], [999, 'high', 'Substantially increased']] : [[94, 'ok', 'Low'], [102, 'warn', 'Increased'], [999, 'high', 'Substantially increased']];
      const c = cat(r, rb);
      return {
        big: { value: r2(r), unit: '', label: 'Your waist-to-hip ratio', verdict: c[2], tone: c[1] },
        bars: [{ label: 'Waist-to-hip ratio', value: r, min: 0.6, max: 1.2, fmt: r2, bands: rb }, { label: 'Waist circumference (WHO)', value: v.waist, min: 50, max: 150, fmt: cmf, bands: wb }],
        stats: [['WHO cut-off for your sex', r2(thr)]],
        save: { key: 'whr', label: 'Waist-to-hip ratio', display: r2(r), target: `below ${r2(thr)}` }
      };
    },

    'heart-rate-zones'(v) {
      if (!good(v.age) || v.age < 15 || v.age > 100) return err('Enter an age between 15 and 100.');
      const max = v.method === 'classic' ? 220 - v.age : 208 - 0.7 * v.age;
      const rest = good(v.rhr) && v.rhr >= 30 && v.rhr < 120 ? v.rhr : NaN;
      const at = p => (Number.isFinite(rest) ? rest + (max - rest) * p : max * p);
      const Z = [[0.5, 0.6, 'Zone 1', 'Very light: warm-up, recovery'], [0.6, 0.7, 'Zone 2', 'Light: conversational pace, builds aerobic base'], [0.7, 0.8, 'Zone 3', 'Moderate: steady, talking gets harder'], [0.8, 0.9, 'Zone 4', 'Hard: threshold intervals'], [0.9, 1.0, 'Zone 5', 'Maximal: short, all-out efforts']];
      const res = {
        big: { value: r0(max), unit: 'bpm', label: `Estimated maximum heart rate (${v.method === 'classic' ? '220 − age' : 'Tanaka: 208 − 0.7 × age'})` },
        table: { head: ['Zone', 'Heart rate', 'Feel and purpose'], rows: Z.map(z => ({ cells: [z[2], `${r0(at(z[0]))}–${r0(at(z[1]))} bpm`, z[3]], cls: z[2] === 'Zone 2' ? 'is-hl' : '' })) },
        stats: [['Method', Number.isFinite(rest) ? 'Karvonen (heart-rate reserve)' : 'Percent of maximum'], ['Zone 2 range', `${r0(at(0.6))}–${r0(at(0.7))} bpm`]],
        note: 'Formulas can miss your true maximum by 10 bpm or more. If a zone feels wrong, trust the talk test: in Zone 2 you can speak in full sentences.',
        save: { key: 'z2', label: 'Zone 2 heart rate', display: `${r0(at(0.6))}–${r0(at(0.7))} bpm` }
      };
      if (Number.isFinite(rest)) res.bars = [{ label: 'Resting heart rate', value: rest, min: 35, max: 110, fmt: r0, bands: [[60, 'ok', 'Below 60'], [80, 'ok', '60–79'], [100, 'warn', '80–99'], [999, 'high', '100+']] }];
      return res;
    },

    vo2max(v) {
      let vo2, how;
      if (v.method === 'cooper') {
        if (!good(v.dist)) return err('Enter the distance you covered in 12 minutes.');
        vo2 = (v.dist * 1000 - 504.9) / 44.73; how = 'Cooper 12-minute run test';
      } else {
        if (!good(v.rhr)) return err('Enter your resting heart rate.');
        const max = good(v.hrmax) ? v.hrmax : good(v.age) ? 208 - 0.7 * v.age : NaN;
        if (!Number.isFinite(max)) return err('Enter your age or your measured maximum heart rate.');
        vo2 = 15.3 * max / v.rhr; how = 'Uth–Sørensen heart-rate ratio';
      }
      if (!(vo2 > 10 && vo2 < 95)) return err('That result is outside a plausible range. Check your entries.');
      const mets = vo2 / 3.5;
      return {
        big: { value: r1(vo2), unit: 'mL/kg/min', label: 'Estimated VO₂ max' },
        bars: [{ label: 'VO₂ max (higher is better)', value: vo2, min: 15, max: 70, hideVerdict: true, bands: [[70, 'neutral', '']] }],
        stats: [['Fitness in METs', r1(mets)], ['Next milestone (+1 MET)', `${r1(vo2 + 3.5)} mL/kg/min`], ['Method', how]],
        note: 'In a large meta-analysis, each 1-MET gain in fitness was linked to about 13% lower risk of death from any cause. Estimates can differ from a lab test by 10% or more.',
        save: { key: 'vo2', label: 'VO₂ max (est.)', display: `${r1(vo2)} mL/kg/min`, target: 'higher every year' }
      };
    },

    'blood-pressure'(v) {
      const pairs = [[v.s1, v.d1], [v.s2, v.d2], [v.s3, v.d3]].filter(p => good(p[0], p[1]));
      if (!pairs.length) return err('Enter at least one reading (top and bottom number).');
      if (pairs.some(p => p[0] <= p[1])) return err('The top (systolic) number must be higher than the bottom (diastolic).');
      if (pairs.some(p => p[0] < 60 || p[0] > 260 || p[1] < 30 || p[1] > 160)) return err('Check your entries: a reading looks out of range.');
      const s = pairs.reduce((a, p) => a + p[0], 0) / pairs.length, d = pairs.reduce((a, p) => a + p[1], 0) / pairs.length;
      let tone, name;
      if (s > 180 || d > 120) [tone, name] = ['crit', 'Severe range'];
      else if (s >= 140 || d >= 90) [tone, name] = ['high', 'Stage 2 hypertension'];
      else if (s >= 130 || d >= 80) [tone, name] = ['warn2', 'Stage 1 hypertension'];
      else if (s >= 120) [tone, name] = ['warn', 'Elevated'];
      else if (s < 90 || d < 60) [tone, name] = ['low', 'Low reading'];
      else [tone, name] = ['ok', 'Normal'];
      const res = {
        big: { value: `${r0(s)}/${r0(d)}`, unit: 'mm Hg', label: pairs.length > 1 ? `Average of ${pairs.length} readings` : 'Your reading', verdict: name, tone },
        bars: [
          { label: 'Systolic (top number)', value: s, min: 80, max: 200, fmt: r0, bands: [[90, 'low', 'Low'], [120, 'ok', 'Normal'], [130, 'warn', 'Elevated'], [140, 'warn2', 'Stage 1'], [181, 'high', 'Stage 2'], [999, 'crit', 'Severe']] },
          { label: 'Diastolic (bottom number)', value: d, min: 40, max: 130, fmt: r0, bands: [[60, 'low', 'Low'], [80, 'ok', 'Normal'], [90, 'warn2', 'Stage 1'], [121, 'high', 'Stage 2'], [999, 'crit', 'Severe']] }
        ],
        stats: [['Category uses', 'the higher of the two numbers'], ['Readings averaged', String(pairs.length)]],
        note: 'One reading is not a diagnosis. Guidelines confirm high blood pressure with readings averaged over several days, ideally at home or with a 24-hour monitor.',
        save: { key: 'bp', label: 'Blood pressure', display: `${r0(s)}/${r0(d)} mm Hg`, target: 'below 120/80' }
      };
      if (tone === 'crit') res.alert = 'This is in the severe range. Rest for 5 minutes and measure again. If it stays above 180/120, contact your doctor right away. If you also have chest pain, shortness of breath, back pain, numbness or weakness, a change in vision or trouble speaking, call your local emergency number now.';
      if (tone === 'low') res.note = 'Low readings matter mainly if you feel dizzy, faint or unwell. If so, talk to a clinician. ' + res.note;
      return res;
    },

    a1c(v) {
      let a;
      if (v.dir === 'eag') {
        if (!good(v.eag)) return err('Enter your average glucose.');
        const mg = v.gunit === 'mmol' ? v.eag * 18.016 : v.eag;
        a = (mg + 46.7) / 28.7;
      } else {
        if (!good(v.a1c)) return err('Enter your A1C.');
        a = v.a1c;
      }
      if (a < 3 || a > 20) return err('That A1C is outside the measurable range. Check your entry.');
      const eag = 28.7 * a - 46.7, ifcc = (a - 2.15) * 10.929;
      const bands = [[5.7, 'ok', 'Below prediabetes range'], [6.5, 'warn', 'Prediabetes range'], [99, 'high', 'Diabetes range']];
      const c = cat(a, bands);
      return {
        big: { value: r1(a), unit: '%', label: 'A1C', verdict: c[2], tone: c[1] },
        bars: [{ label: 'A1C (ADA ranges)', value: a, min: 4, max: 12, bands }],
        stats: [['Estimated average glucose', `${r0(eag)} mg/dL`], ['In mmol/L', `${r1(eag / 18.016)} mmol/L`], ['IFCC units', `${r0(ifcc)} mmol/mol`]],
        note: 'A single home or lab result does not diagnose diabetes; clinicians confirm with a repeat test. Anaemia, kidney disease and some haemoglobin variants can skew A1C.',
        save: { key: 'a1c', label: 'A1C', display: `${r1(a)}%`, target: 'below 5.7%' }
      };
    },

    cholesterol(v) {
      if (!good(v.tc, v.hdl)) return err('Enter total cholesterol and HDL.');
      const k = v.unit === 'mmol' ? 38.67 : 1, tgk = v.unit === 'mmol' ? 88.57 : 1;
      const tc = v.tc * k, hdl = v.hdl * k, ldl = good(v.ldl) ? v.ldl * k : NaN, tg = good(v.tg) ? v.tg * tgk : NaN;
      if (hdl >= tc) return err('HDL must be lower than total cholesterol.');
      if (tc < 70 || tc > 600) return err('Check your entries and the unit selected.');
      const fmt = x => (v.unit === 'mmol' ? `${r1(x / 38.67)} mmol/L` : `${r0(x)} mg/dL`);
      const non = tc - hdl, ratio = tc / hdl;
      const nb = [[130, 'ok', 'Desirable'], [160, 'warn', 'Above desirable'], [190, 'warn2', 'Borderline high'], [220, 'high', 'High'], [9999, 'crit', 'Very high']];
      const c = cat(non, nb);
      const hdlLow = v.sex === 'f' ? 50 : 40;
      const bars = [{ label: 'Non-HDL cholesterol', value: non, min: 70, max: 260, fmt, bands: nb },
        { label: 'HDL cholesterol', value: hdl, min: 20, max: 100, fmt, bands: [[hdlLow, 'high', 'Low'], [60, 'ok', 'Acceptable'], [999, 'ok', 'Protective']] }];
      if (Number.isFinite(ldl)) bars.push({ label: 'LDL cholesterol', value: ldl, min: 40, max: 230, fmt, bands: [[100, 'ok', 'Optimal'], [130, 'ok', 'Near optimal'], [160, 'warn', 'Borderline high'], [190, 'high', 'High'], [9999, 'crit', 'Very high']] });
      const stats = [['Total/HDL ratio', `${r1(ratio)} (aim below 5; ideal below 3.5)`]];
      if (Number.isFinite(tg)) stats.push(['Triglycerides', `${v.unit === 'mmol' ? r1(tg / 88.57) + ' mmol/L' : r0(tg) + ' mg/dL'}: ${tg < 150 ? 'normal' : tg < 200 ? 'borderline high' : tg < 500 ? 'high' : 'very high'}`]);
      const res = {
        big: { value: v.unit === 'mmol' ? r1(non / 38.67) : r0(non), unit: v.unit === 'mmol' ? 'mmol/L' : 'mg/dL', label: 'Non-HDL cholesterol', verdict: c[2], tone: c[1] },
        bars, stats,
        note: 'Non-HDL cholesterol counts every artery-clogging particle, so many experts prefer it to LDL alone. Your clinician combines it with blood pressure, age and other factors to estimate risk.',
        save: { key: 'nonhdl', label: 'Non-HDL cholesterol', display: fmt(non), target: 'below 130 mg/dL (3.4 mmol/L)' }
      };
      if ((Number.isFinite(ldl) && ldl >= 190) || non >= 220) res.alert = 'Levels this high can signal an inherited cholesterol disorder. Share this result with a clinician.';
      return res;
    },

    metabolic(v) {
      if (!v.sex) return err('Choose your sex.');
      const mmol = v.unit === 'mmol', f = v.sex === 'f', asian = v.pop === 'asian';
      const tg = good(v.tg) ? v.tg * (mmol ? 88.57 : 1) : NaN, hdl = good(v.hdl) ? v.hdl * (mmol ? 38.67 : 1) : NaN, fg = good(v.fg) ? v.fg * (mmol ? 18.016 : 1) : NaN;
      const wcut = asian ? (f ? 80 : 90) : (f ? 88 : 102);
      const lab = (x, k) => (mmol ? `${r1(x / k)} mmol/L` : `${r0(x)} mg/dL`);
      const C = [
        ['Waist', good(v.waist) ? cmf(v.waist) : '', `${cmf(wcut)} or more`, good(v.waist) ? v.waist >= wcut : null],
        ['Triglycerides', Number.isFinite(tg) ? lab(tg, 88.57) : (v.lipidmed ? 'On treatment' : ''), `${mmol ? '1.7 mmol/L' : '150 mg/dL'} or more, or on treatment`, v.lipidmed ? true : Number.isFinite(tg) ? tg >= 150 : null],
        ['HDL cholesterol', Number.isFinite(hdl) ? lab(hdl, 38.67) : (v.lipidmed ? 'On treatment' : ''), `below ${f ? (mmol ? '1.3 mmol/L' : '50 mg/dL') : (mmol ? '1.0 mmol/L' : '40 mg/dL')}, or on treatment`, v.lipidmed ? true : Number.isFinite(hdl) ? hdl < (f ? 50 : 40) : null],
        ['Blood pressure', good(v.sbp, v.dbp) ? `${r0(v.sbp)}/${r0(v.dbp)}` : (v.bpmed ? 'On treatment' : ''), '130/85 or more, or on treatment', v.bpmed ? true : good(v.sbp, v.dbp) ? (v.sbp >= 130 || v.dbp >= 85) : null],
        ['Fasting glucose', Number.isFinite(fg) ? lab(fg, 18.016) : (v.glucmed ? 'On treatment' : ''), `${mmol ? '5.6 mmol/L' : '100 mg/dL'} or more, or on treatment`, v.glucmed ? true : Number.isFinite(fg) ? fg >= 100 : null]
      ];
      const entered = C.filter(c => c[3] !== null).length, met = C.filter(c => c[3] === true).length;
      if (!entered) return err('Enter at least one marker.');
      const tone = met >= 3 ? 'high' : met > 0 ? 'warn' : 'ok';
      const verdict = met >= 3 ? 'Meets the definition of metabolic syndrome' : met > 0 ? 'Some markers outside range' : 'No criteria met';
      return {
        big: { value: `${met} of 5`, unit: '', label: 'Criteria met', verdict, tone },
        bars: [{ label: 'Criteria met', value: met + 0.5, min: 0, max: 5, fmt: () => String(met), hideVerdict: true, bands: [[1, 'ok', '0'], [3, 'warn', '1–2'], [9, 'high', '3+']] }],
        table: { head: ['Marker', 'Your value', 'Counts if', 'Status'], rows: C.map(c => ({ cells: [c[0], c[1] || '—', c[2], c[3] === null ? 'Not entered' : c[3] ? 'Met' : 'Not met'], cls: c[3] ? '' : '' })) },
        note: (entered < 5 ? `You entered ${entered} of 5 markers. An unmeasured marker could still be out of range. ` : '') + 'Three or more criteria define metabolic syndrome (harmonized definition, 2009). Your clinician can confirm with fasting labs.',
        save: { key: 'metabolic', label: 'Metabolic syndrome criteria', display: `${met} of 5 met (${entered} entered)`, target: '0 of 5' }
      };
    },

    water(v) {
      if (!v.sex) return err('Choose your sex.');
      if (!good(v.weight)) return err('Enter your weight.');
      const ex = Number.isFinite(v.exercise) && v.exercise > 0 ? v.exercise : 0;
      let L = v.weight * 0.033 + (ex / 60) * 0.6 + (v.hot ? 0.5 : 0) + (v.status === 'pregnant' ? 0.3 : v.status === 'breastfeeding' ? 0.7 : 0);
      const ref = v.sex === 'm' ? 3.0 : 2.2;
      const show = imp() ? `${r0(L * 33.814)}` : r1(L);
      return {
        big: { value: show, unit: imp() ? 'fl oz/day' : 'litres/day', label: 'Estimated fluid to drink' },
        stats: [['Cups (240 mL)', r1(L / 0.24)], ['500 mL bottles', r1(L / 0.5)], ['Reference intake from drinks (NASEM, ~80% of total)', `${r1(ref)} L`], ['Extra for exercise', ex ? `${r1((ex / 60) * 0.6)} L` : 'none entered']],
        note: 'Food supplies about a fifth of daily water. Pale-yellow urine is a practical check. If you have heart or kidney disease or a fluid limit, follow your clinician.',
        save: { key: 'water', label: 'Daily fluid', display: imp() ? `${r0(L * 33.814)} fl oz` : `${r1(L)} L` }
      };
    },

    sleep(v) {
      const t = parseTime(v.time);
      if (!Number.isFinite(t)) return err('Enter a time.');
      const lat = Number.isFinite(v.latency) && v.latency >= 0 && v.latency < 120 ? v.latency : 15;
      const cyc = v.mode === 'bed' ? [4, 5, 6] : [6, 5, 4];
      const rows = cyc.map(c => {
        const at = v.mode === 'bed' ? t + lat + c * 90 : t - lat - c * 90;
        return { cells: [`${c} cycles`, `${r1(c * 1.5)} h`, ftime(at)], cls: c === 5 ? 'is-hl' : '' };
      });
      const best = v.mode === 'bed' ? t + lat + 5 * 90 : t - lat - 5 * 90;
      return {
        big: { value: ftime(best), unit: '', label: v.mode === 'bed' ? 'Wake up at (5 full cycles)' : 'Go to bed at (5 full cycles)' },
        table: { head: ['Sleep cycles', 'Sleep time', v.mode === 'bed' ? 'Wake up at' : 'Be in bed by'], rows },
        note: `Includes ${r0(lat)} minutes to fall asleep. Adults need at least 7 hours; 4 cycles (6 h) falls short. Cycles vary from about 70 to 120 minutes, so treat these times as a guide.`
      };
    },

    'sleep-debt'(v) {
      const need = Number.isFinite(v.need) && v.need >= 6 && v.need <= 10 ? v.need : 8;
      const n = [v.n1, v.n2, v.n3, v.n4, v.n5, v.n6, v.n7].filter(x => Number.isFinite(x) && x >= 0 && x <= 16);
      if (n.length < 3) return err('Enter hours for at least 3 nights.');
      const avg = n.reduce((a, b) => a + b, 0) / n.length, debt = n.reduce((a, b) => a + (need - b), 0);
      const bands = [[6, 'high', 'Short'], [7, 'warn', 'Below 7 h'], [9, 'ok', 'Recommended'], [99, 'warn', 'Long']];
      return {
        big: { value: debt > 0 ? hm(debt) : '0 h', unit: '', label: `Sleep debt over ${n.length} nights`, verdict: debt > 0 ? 'Behind on sleep' : 'No debt', tone: debt > 3 ? 'high' : debt > 0 ? 'warn' : 'ok' },
        bars: [{ label: 'Average sleep per night', value: avg, min: 3, max: 11, fmt: x => `${r1(x)} h`, bands }],
        stats: [['Average per night', hm(avg)], ['Your nightly need', `${r1(need)} h`], ['Nights to repay at +45 min/night', debt > 0 ? String(Math.ceil(debt / 0.75)) : '0']],
        note: 'Repay gradually: go to bed 30–60 minutes earlier rather than sleeping in for hours, which shifts your body clock.',
        save: { key: 'sleep', label: 'Average sleep', display: `${r1(avg)} h/night`, target: '7–9 h' }
      };
    },

    'calories-burned'(v) {
      const met = parseFloat(v.activity);
      if (!good(v.weight)) return err('Enter your weight.');
      if (!good(v.minutes)) return err('Enter the duration in minutes.');
      const per = mets => mets * 3.5 * v.weight / 200;
      const kc = per(met) * v.minutes;
      const cmp = [['Brisk walking (3.5 mph)', 4.3], ['Cycling, moderate', 8.0], ['Running, 6 mph', 9.8], ['Swimming laps, moderate', 5.8], ['Strength training, moderate', 3.5]];
      return {
        big: { value: r0(kc), unit: 'kcal', label: `Burned in ${r0(v.minutes)} minutes` },
        stats: [['Per hour at this pace', `${r0(per(met) * 60)} kcal`], ['Intensity', `${r1(met)} METs`], ['Above resting (net)', `${r0((met - 1) * 3.5 * v.weight / 200 * v.minutes)} kcal`]],
        table: { head: [`Same ${r0(v.minutes)} minutes doing…`, 'Calories'], rows: cmp.map(c => [c[0], `${r0(per(c[1]) * v.minutes)} kcal`]) },
        note: 'MET values are averages from the Compendium of Physical Activities. Fitness, terrain and effort shift real burn by 10–20% or more.'
      };
    },

    steps(v) {
      if (!good(v.steps)) return err('Enter your steps.');
      if (!good(v.height)) return err('Enter your height.');
      if (!v.sex) return err('Choose your sex.');
      const stride = v.height * (v.sex === 'm' ? 0.415 : 0.413) / 100;
      const km = v.steps * stride / 1000;
      const P = { casual: [4.8, 3.5], brisk: [5.6, 4.3], fast: [6.4, 5.0] }[v.pace] || [4.8, 3.5];
      const mins = km / P[0] * 60;
      const kc = good(v.weight) ? P[1] * 3.5 * v.weight / 200 * mins : NaN;
      const bands = [[4000, 'high', 'Low'], [7000, 'warn', 'Building'], [10000, 'ok', '7,000+'], [99999, 'ok', 'Very active']];
      const c = cat(v.steps, bands);
      return {
        big: { value: imp() ? r1(km / MI) : r1(km), unit: imp() ? 'miles' : 'km', label: `Distance for ${r0(v.steps)} steps` },
        bars: [{ label: 'Daily steps', value: v.steps, min: 0, max: 15000, fmt: r0, bands }],
        stats: [['Walking time', `${r0(mins)} min`], ['Calories (gross)', Number.isFinite(kc) ? `${r0(kc)} kcal` : 'add weight'], ['Estimated stride', cmf(stride * 100)], ['Steps to 7,000', v.steps >= 7000 ? 'reached' : r0(7000 - v.steps)]],
        note: `Verdict: ${c[2]}. A 2025 meta-analysis of 57 studies linked about 7,000 steps a day with 47% lower risk of death from any cause compared with 2,000.`,
        save: { key: 'steps', label: 'Daily steps', display: r0(v.steps), target: '7,000+' }
      };
    },

    'one-rep-max'(v) {
      if (!good(v.load)) return err('Enter the weight you lifted.');
      if (!good(v.reps) || v.reps > 20) return err('Enter reps between 1 and 20.');
      const w = v.load, r = Math.round(v.reps), u = imp() ? 'lb' : 'kg';
      const ep = r === 1 ? w : w * (1 + r / 30), br = r === 1 ? w : w * 36 / (37 - r), lo = r === 1 ? w : w * Math.pow(r, 0.10);
      const orm = (ep + br + lo) / 3;
      const pct = [[100, 1], [95, 2], [90, 4], [85, 6], [80, 8], [75, 10], [70, 12], [65, 15], [60, 20]];
      return {
        big: { value: r1(orm), unit: u, label: 'Estimated one-rep max (average of 3 formulas)' },
        stats: [['Epley', `${r1(ep)} ${u}`], ['Brzycki', `${r1(br)} ${u}`], ['Lombardi', `${r1(lo)} ${u}`]],
        table: { head: ['% of 1RM', 'Load', 'Typical reps'], rows: pct.map(p => [`${p[0]}%`, `${r1(orm * p[0] / 100)} ${u}`, String(p[1])]) },
        note: (r > 10 ? 'Estimates get less reliable above 10 reps. ' : '') + 'Test true maxes only with good technique and a spotter.'
      };
    },

    pace(v) {
      const km = v.preset === 'custom' ? v.dist : parseFloat(v.preset);
      if (!good(km)) return err('Choose or enter a distance.');
      const secs = (v.hh || 0) * 3600 + (v.mm || 0) * 60 + (v.ss || 0);
      if (!(secs > 0)) return err('Enter your time.');
      const perKm = secs / km, perMi = secs / (km / MI), kmh = km / (secs / 3600);
      const R = [['5K', 5], ['10K', 10], ['Half marathon', 21.0975], ['Marathon', 42.195]];
      return {
        big: { value: clock(imp() ? perMi : perKm), unit: imp() ? 'min/mile' : 'min/km', label: 'Your average pace' },
        stats: [['Pace per km', `${clock(perKm)} min`], ['Pace per mile', `${clock(perMi)} min`], ['Speed', `${r1(kmh)} km/h (${r1(kmh / MI)} mph)`]],
        table: { head: ['Race', 'Predicted time (Riegel)'], rows: R.map(x => ({ cells: [x[0], clock(secs * Math.pow(x[1] / km, 1.06))], cls: Math.abs(x[1] - km) < 0.01 ? 'is-hl' : '' })) },
        note: 'Riegel predictions assume training suited to the longer distance. Most runners slow more than predicted at the marathon.'
      };
    },

    'due-date'(v) {
      const d = parseDate(v.date);
      if (!d) return err('Enter a date.');
      const cyc = Number.isFinite(v.cycle) && v.cycle >= 21 && v.cycle <= 45 ? v.cycle : 28;
      const lmp = v.method === 'conception' ? addDays(d, -14) : addDays(d, cyc - 28);
      const edd = addDays(lmp, 280), ga = dayDiff(today(), lmp);
      if (ga < 0) return err('That date is in the future.');
      if (ga > 44 * 7) return err('That date is more than 44 weeks ago. Check the date.');
      const wk = Math.floor(ga / 7), dy = ga % 7, tri = ga < 14 * 7 ? 'First trimester' : ga < 28 * 7 ? 'Second trimester' : 'Third trimester';
      const M = [[13 * 7 + 6, 'End of first trimester'], [18 * 7, 'Anatomy scan window opens (18–22 weeks)'], [24 * 7, 'Glucose screening window (24–28 weeks)'], [28 * 7, 'Third trimester begins'], [37 * 7, 'Early term (37 weeks)'], [39 * 7, 'Full term (39 weeks)'], [280, 'Estimated due date (40 weeks)'], [41 * 7, 'Late term (41 weeks)']];
      return {
        big: { value: edd.toLocaleDateString(undefined, { month: 'long', day: 'numeric', year: 'numeric' }), unit: '', label: 'Estimated due date' },
        stats: [['How far along today', `${wk} weeks, ${dy} days`], ['Trimester', tri], ['Days to go', String(Math.max(0, dayDiff(edd, today())))]],
        table: { head: ['Milestone', 'Date'], rows: M.map(m => ({ cells: [m[1], fdate(addDays(lmp, m[0]))], cls: m[0] < ga ? 'is-past' : '' })) },
        note: 'Only a small share of babies arrive on the due date; most come within two weeks either side. An early ultrasound gives the most accurate date.'
      };
    },

    ovulation(v) {
      const d = parseDate(v.date);
      if (!d) return err('Enter the first day of your last period.');
      const cyc = Number.isFinite(v.cycle) && v.cycle >= 21 && v.cycle <= 45 ? Math.round(v.cycle) : 28;
      const rows = [0, 1, 2].map(i => {
        const start = addDays(d, i * cyc), ov = addDays(start, cyc - 14);
        return [fdate(start), `${addDays(ov, -5).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })} – ${addDays(ov, 1).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}`, fdate(ov)];
      });
      const ov0 = addDays(d, cyc - 14);
      return {
        big: { value: ov0.toLocaleDateString(undefined, { month: 'long', day: 'numeric' }), unit: '', label: 'Estimated ovulation day' },
        stats: [['Most fertile days', `${addDays(ov0, -2).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })} – ${ov0.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}`], ['Next period expected', fdate(addDays(d, cyc))]],
        table: { head: ['Cycle starts', 'Fertile window', 'Ovulation (est.)'], rows },
        note: 'This uses the average 14-day luteal phase. Ovulation varies cycle to cycle; LH test strips or temperature tracking sharpen the estimate. Do not use this as contraception.'
      };
    },

    caffeine(v) {
      const C = [['coffee', 95], ['espresso', 63], ['blacktea', 47], ['greentea', 28], ['cola', 34], ['energy', 80], ['preworkout', 200], ['chocolate', 20]];
      const tot = C.reduce((a, [k, mg]) => a + (Number.isFinite(v[k]) && v[k] > 0 ? v[k] * mg : 0), 0);
      if (!(tot > 0)) return err('Enter at least one drink or food.');
      const lim = v.pregnant ? 200 : 400;
      const res = {
        big: { value: r0(tot), unit: 'mg', label: 'Caffeine today', verdict: tot <= lim ? 'Within the daily limit' : 'Above the daily limit', tone: tot <= lim ? 'ok' : 'high' },
        bars: [{ label: `Daily caffeine (limit ${lim} mg)`, value: tot, min: 0, max: 800, fmt: r0, bands: [[lim + 0.5, 'ok', 'Within limit'], [9999, 'high', 'Above limit']] }],
        stats: [['Daily limit used', `${r0(tot / lim * 100)}%`], ['Limit applied', v.pregnant ? '200 mg (pregnancy)' : '400 mg (healthy adults)']],
        note: 'Caffeine content varies widely by brand and brew. Half-life averages about 5 hours but ranges from roughly 2 to 10.',
        save: { key: 'caffeine', label: 'Caffeine', display: `${r0(tot)} mg/day`, target: `≤ ${lim} mg` }
      };
      const a = parseTime(v.last), b = parseTime(v.bed);
      if (Number.isFinite(a) && Number.isFinite(b)) {
        const hrs = (((b - a) % 1440) + 1440) % 1440 / 60;
        res.stats.push(['Still in your system at bedtime (upper estimate)', `${r0(tot * Math.pow(0.5, hrs / 5))} mg`]);
      }
      return res;
    },

    screenings(v) {
      if (!good(v.age) || v.age < 18 || v.age > 100) return err('Enter an age between 18 and 100.');
      if (!v.sex) return err('Choose your sex at birth.');
      const a = v.age, f = v.sex === 'f', m = v.sex === 'm', smk = v.smoke, py = Number.isFinite(v.packyears) ? v.packyears : NaN, quit = Number.isFinite(v.quit) ? v.quit : 0;
      const due = [], talk = [];
      const add = (list, cond, name, detail, tag) => { if (cond) list.push({ name, detail, tag }); };
      add(due, true, 'Blood pressure check', a >= 40 ? 'Every year.' : 'Every 3–5 years if normal and no risk factors; yearly if at higher risk.', 'USPSTF A');
      add(due, true, 'Depression screening', 'At routine visits.', 'USPSTF B');
      add(due, a <= 64, 'Anxiety screening', 'At routine visits.', 'USPSTF B');
      add(due, true, 'Unhealthy alcohol use screening', 'At routine visits.', 'USPSTF B');
      add(due, smk === 'current', 'Tobacco cessation support', 'Every visit: counselling plus approved medicines.', 'USPSTF A');
      add(due, a <= 65, 'HIV test', 'At least once; more often if at higher risk.', 'USPSTF A');
      add(due, a <= 79, 'Hepatitis C test', 'Once in adulthood.', 'USPSTF B');
      add(due, a >= 35 && a <= 70 && v.overweight, 'Prediabetes and type 2 diabetes test', 'Every 3 years if normal.', 'USPSTF B');
      add(due, a >= 40 && a <= 75, 'Cholesterol and 10-year heart-risk check', 'Used to decide on statins; repeat every 4–6 years or as advised.', 'USPSTF B');
      add(due, a >= 45 && a <= 75, 'Colorectal cancer screening', 'Stool test every 1–3 years, or colonoscopy every 10 years.', a >= 50 ? 'USPSTF A' : 'USPSTF B');
      add(due, f && a >= 40 && a <= 74, 'Breast cancer screening (mammogram)', 'Every 2 years.', 'USPSTF B');
      add(due, f && a >= 21 && a <= 65, 'Cervical cancer screening', a < 30 ? 'Pap test every 3 years.' : 'Pap every 3 years, HPV test every 5 years, or both every 5 years.', 'USPSTF A');
      const lungAge = a >= 50 && a <= 80, smoker = smk === 'current' || (smk === 'former' && quit <= 15);
      add(due, lungAge && smoker && py >= 20, 'Lung cancer screening (low-dose CT)', 'Every year while you qualify.', 'USPSTF B');
      add(talk, lungAge && smoker && !Number.isFinite(py), 'Lung cancer screening', 'You may qualify if you have 20 or more pack-years. Pack-years = packs per day × years smoked.', 'Check');
      add(due, m && a >= 65 && a <= 75 && smk !== 'never', 'Abdominal aortic aneurysm ultrasound', 'Once.', 'USPSTF B');
      add(due, f && a >= 65, 'Osteoporosis screening (bone density)', 'As advised by your clinician.', 'USPSTF B');
      add(talk, f && a >= 50 && a < 65, 'Bone density test', 'Recommended before 65 if you are postmenopausal with risk factors.', 'USPSTF B');
      add(due, a >= 65, 'Falls prevention exercise', 'Balance and strength training to cut fall risk.', 'USPSTF B');
      add(talk, m && a >= 55 && a <= 69, 'Prostate cancer (PSA) screening', 'An individual decision; weigh benefits and harms with your clinician.', 'USPSTF C');
      add(talk, a >= 76 && a <= 85, 'Colorectal screening after 75', 'Selective; depends on your health and past screening.', 'USPSTF C');
      add(talk, a >= 35 && !v.overweight, 'Diabetes test', 'The American Diabetes Association advises testing all adults from age 35.', 'ADA');
      return {
        big: { value: String(due.length), unit: due.length === 1 ? 'check' : 'checks', label: 'Recommended for you now' },
        groups: [{ title: 'Recommended for your age and history', items: due }].concat(talk.length ? [{ title: 'Talk with your clinician about', items: talk }] : []).concat([{ title: 'Vaccines', items: [{ name: 'Adult vaccine schedule', detail: 'Ask which vaccines are due for your age and health. See your national immunization schedule.', tag: 'Check' }] }]),
        note: 'Based on U.S. Preventive Services Task Force recommendations for people without symptoms. Programs differ by country, and family history can mean earlier or more frequent tests.',
        save: { key: 'screenings', label: 'Screenings due', display: `${due.length} recommended`, target: 'all up to date' }
      };
    }
  };

  /* ---------- render ---------- */
  function render(res, out, tool, compact) {
    out.hidden = false;
    if (res.error) { out.innerHTML = `<p class="res-error" role="alert">${res.error}</p>`; return; }
    const B = res.big;
    let h = `<div class="res-head"><div class="res-big tone-${B.tone || 'ink'}"><span class="res-num">${B.value}</span>${B.unit ? `<span class="res-unit">${B.unit}</span>` : ''}</div><p class="res-label">${B.label}</p>${B.verdict ? `<p class="res-verdict tone-${B.tone || 'ink'}">${B.verdict}</p>` : ''}</div>`;
    if (res.alert) h += `<div class="res-alert" role="alert">${res.alert}</div>`;
    (compact ? (res.bars || []).slice(0, 2) : (res.bars || [])).forEach(b => { h += bar(b); });
    if (compact) {
      const s = res.stats && res.stats[1] ? `${res.stats[1][0]}: <b>${res.stats[1][1]}</b>. ` : '';
      h += `<p class="res-note">${s}<a href="${PH.root}tools/${tool}.html">See the full breakdown</a></p>`;
    } else {
      if (res.split) h += `<div class="split" role="img" aria-label="${res.split.map(s => `${s.label} ${Math.round(s.pct)}%`).join(', ')}">${res.split.map(s => `<span class="bg-${s.tone}" style="width:${s.pct}%">${s.label} ${Math.round(s.pct)}%</span>`).join('')}</div>`;
      if (res.stats) h += `<dl class="res-stats">${res.stats.map(([k, x]) => `<div><dt>${k}</dt><dd>${x}</dd></div>`).join('')}</dl>`;
      if (res.table) h += `<div class="table-scroll"><table class="res-table"><thead><tr>${res.table.head.map(x => `<th scope="col">${x}</th>`).join('')}</tr></thead><tbody>${res.table.rows.map(r => `<tr${r.cls ? ` class="${r.cls}"` : ''}>${(r.cells || r).map(x => `<td>${x}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
      (res.groups || []).forEach(g => { h += `<div class="res-group"><h3>${g.title}</h3><ul>${g.items.length ? g.items.map(i => `<li><b>${i.name}</b><span class="tag">${i.tag || ''}</span><small>${i.detail || ''}</small></li>`).join('') : '<li>Nothing extra right now.</li>'}</ul></div>`; });
      if (res.note) h += `<p class="res-note">${res.note}</p>`;
      h += `<div class="res-actions">${res.save ? '<button type="button" class="btn btn-primary btn-sm" data-act="save">Save to My Numbers</button>' : ''}<button type="button" class="btn btn-ghost btn-sm" data-act="copy">Copy result</button><button type="button" class="btn btn-ghost btn-sm" data-act="print">Print</button></div>`;
    }
    out.innerHTML = h;
    out._res = res;
    placeMarkers(out);
  }

  function saveNumber(res, tool) {
    const s = res.save; if (!s) return;
    const all = store.get('numbers', {});
    all[s.key] = { label: s.label, display: s.display, target: s.target || '', date: new Date().toISOString(), url: `tools/${tool}.html` };
    store.set('numbers', all);
  }

  /* ---------- init ---------- */
  const syncUnits = () => {
    document.body.classList.toggle('units-imperial', imp());
    $$('.unit-toggle button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.units === units)));
  };
  syncUnits();
  $$('.unit-toggle').forEach(t => t.addEventListener('click', e => {
    const b = e.target.closest('button[data-units]'); if (!b || b.dataset.units === units) return;
    units = b.dataset.units; store.set('units', units); syncUnits();
    $$('form.calc .result').forEach(o => { o.hidden = true; o.innerHTML = ''; });
  }));

  $$('form.calc').forEach(form => {
    const tool = form.dataset.tool, out = form.querySelector('.result');
    const compact = form.hasAttribute('data-compact');
    const cond = () => {
      const vals = read(form);
      $$('[data-show-if]', form).forEach(el => { const [k, x] = el.dataset.showIf.split('='); el.hidden = String(vals[k]) !== x; });
    };
    form.addEventListener('change', cond); cond();
    form.addEventListener('reset', () => { if (out) { out.hidden = true; out.innerHTML = ''; } setTimeout(cond, 0); });
    form.addEventListener('submit', e => {
      e.preventDefault();
      const fn = T[tool]; if (!fn || !out) return;
      let res;
      try { res = fn(read(form)); } catch (x) { console.error(x); res = err('Check your entries and try again.'); }
      render(res, out, tool, compact);
      if (!res.error && !compact) out.focus({ preventScroll: true });
      if (!res.error && compact && res.save) saveNumber(res, tool);
    });
    out?.addEventListener('click', async e => {
      const a = e.target.closest('[data-act]'); if (!a || !out._res) return;
      const r = out._res;
      if (a.dataset.act === 'save') { saveNumber(r, tool); a.textContent = 'Saved'; a.disabled = true; a.insertAdjacentHTML('afterend', ` <a class="btn btn-ghost btn-sm" href="${PH.root}my-numbers.html">View My Numbers</a>`); }
      if (a.dataset.act === 'copy') { const ok = await PH.copy(`${r.big.label}: ${r.big.value}${r.big.unit ? ' ' + r.big.unit : ''}${r.big.verdict ? ' (' + r.big.verdict + ')' : ''}. Calculated at ${location.href}`); a.textContent = ok ? 'Copied' : 'Copy failed'; }
      if (a.dataset.act === 'print') window.print();
    });
  });

  window.PHT = { bar, placeMarkers, read, imp, kg, r0, r1, r2, LB, IN };
})();
