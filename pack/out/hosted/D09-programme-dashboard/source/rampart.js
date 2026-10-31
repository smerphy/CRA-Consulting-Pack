/* Project Rampart programme dashboard: calculations and drawings.
   Every figure on the page is read from a dataset or a calculation defined here. */
(() => {
  'use strict';
  const D = window.dash;
  const NA = '—';
  const NS = 'http://www.w3.org/2000/svg';
  const [TEAL, NAVY, STEEL] = D.colors;
  const CLASS_COLOR = { Default: STEEL, 'Class I': TEAL, 'Class II': NAVY };
  const MUTED = 'var(--cds-chart-muted)';
  const SIGNAL = 'var(--rp-signal)';
  const INK = 'var(--color-fg)';
  const INK_MUTED = 'var(--color-fg-muted)';
  const PANEL = 'var(--color-panel)';
  const WASH = 'color-mix(in srgb, var(--color-fg) 6%, var(--color-panel))';
  const tint = (c, pct) => `color-mix(in srgb, ${c} ${pct}%, var(--color-panel))`;
  // Fixed reference chosen for the programme: spend tolerance from K11 ("Within +/-10% of plan").
  const TOLERANCE = 0.1;
  // Risk-matrix zones from the Advisory Design System: High 12-25, Medium 5-11, Low 1-4.
  const RISK_HIGH = 12;
  const RISK_MEDIUM = 5;

  /* ---------------- calculations ---------------- */
  D.calc('kpi_rag_counts', {
    inputs: ['kpis'],
    title: 'KPIs by RAG status',
    description: 'Counts the SteerCo KPIs in each RAG status.',
    fn: (kpis) => ['Green', 'Amber', 'Red'].map((rag) => ({ rag, kpis: kpis.filter((k) => k.rag === rag).length })),
  });
  D.calc('ws_rag_counts', {
    inputs: ['workstreams'],
    title: 'Workstreams by RAG status',
    description: 'Counts the workstreams in each RAG status.',
    fn: (workstreams) => ['Green', 'Amber', 'Red'].map((rag) => ({ rag, workstreams: workstreams.filter((w) => w.rag === rag).length })),
  });
  D.calc('milestone_status_counts', {
    inputs: ['milestones'],
    title: 'Milestones by status',
    description: 'Counts the milestones in each status.',
    fn: (milestones) => ['Complete', 'On track', 'At risk', 'Planned', 'Fixed'].map((status) => ({ status, milestones: milestones.filter((m) => m.status === status).length })),
  });
  D.calc('nb_need', {
    inputs: ['families'],
    title: 'Families needing a notified body',
    description: 'Counts the product families whose CRA class needs a notified body and sums their EU revenue (EUR m).',
    fn: (families) => {
      const nb = families.filter((f) => f.needs_nb === true || f.needs_nb === 'true');
      return [{ families: nb.length, eu_revenue_m: Math.round(nb.reduce((s, f) => s + Number(f.eu_revenue_m), 0) * 10) / 10 }];
    },
  });
  D.calc('hbs_class_i', {
    inputs: ['families'],
    title: 'Class I home products readiness',
    description: 'Average readiness index of the Home & Building Solutions families in Class I (each family answers the same diagnostic questions).',
    fn: (families) => {
      const seg = families.filter((f) => f.bu === 'HBS' && f.class_group === 'Class I');
      return [{ families: seg.length, readiness: seg.reduce((s, f) => s + Number(f.readiness), 0) / seg.length }];
    },
  });
  D.calc('tasks_due', {
    inputs: ['mobilisation_plan'],
    title: 'Tasks due by 30 Nov 2026',
    description: 'Mobilisation-plan tasks that end on or before 30 Nov 2026, earliest first.',
    fn: (mobilisation_plan) => mobilisation_plan
      .filter((t) => t.end_iso <= '2026-11-30')
      .sort((a, b) => a.end_iso.localeCompare(b.end_iso) || a.id.localeCompare(b.id))
      .map((t) => ({ ...t, due_by: '30 Nov 2026' })),
  });
  D.calc('spend_variance', {
    inputs: ['spend'],
    title: 'Spend against plan to date',
    description: 'Cumulative actual less cumulative plan for the latest month with an actual, in EUR and as a share of plan.',
    fn: (spend) => spend
      .filter((m) => m.cumulative_actual !== null && m.cumulative_actual !== undefined && m.cumulative_actual !== '')
      .slice(-1)
      .map((m) => {
        const actual = Number(m.cumulative_actual);
        const plan = Number(m.cumulative_plan);
        return { month: m.month, actual, plan, variance: actual - plan, variance_share: (actual - plan) / plan };
      }),
  });
  D.calc('budget_bars', {
    inputs: ['budget_workstreams', 'budget_totals'],
    title: 'One-off budget with contingency',
    description: 'Base-case one-off cost per workstream to Dec 2027, plus contingency as its own line (EUR).',
    fn: (budget_workstreams, budget_totals) => [
      ...budget_workstreams.map((w) => ({ line: w.workstream, one_off: Number(w.one_off), kind: 'Workstream' })),
      { line: 'Contingency', one_off: Number(budget_totals[0].contingency_q4_2026) + Number(budget_totals[0].contingency_2027), kind: 'Contingency' },
    ],
  });

  /* ---------------- formatting ---------------- */
  const num = (v) => (v === null || v === undefined || v === '' ? null : Number.isFinite(Number(v)) ? Number(v) : null);
  const isNum = (v) => num(v) !== null;
  // Round half to even, matching the figures in the programme's data summary (38.5% shows as 38%).
  const halfEven = (x) => {
    const f = Math.floor(x);
    const d = x - f;
    if (Math.abs(d - 0.5) < 1e-9) return f % 2 === 0 ? f : f + 1;
    return Math.round(x);
  };
  const eur = (v) => (Math.abs(v) >= 1e6 ? 'EUR ' + (v / 1e6).toFixed(2) + 'm' : 'EUR ' + halfEven(v / 1e3) + 'k');
  const F = {
    text: (v) => (v === null || v === undefined || v === '' ? NA : String(v)),
    int: (v) => (isNum(v) ? d3.format(',')(num(v)) : NA),
    num1: (v) => (isNum(v) ? num(v).toFixed(1) : NA),
    level: (v) => (isNum(v) ? num(v).toFixed(2) : NA),
    pct: (v) => (isNum(v) ? halfEven(num(v) * 100) + '%' : NA),
    pct2: (v) => (isNum(v) ? (num(v) * 100).toFixed(2) + '%' : NA),
    spct1: (v) => (isNum(v) ? (num(v) >= 0 ? '+' : '−') + Math.abs(num(v) * 100).toFixed(1) + '%' : NA),
    eur: (v) => (isNum(v) ? eur(num(v)) : NA),
    seur: (v) => (isNum(v) ? (num(v) >= 0 ? '+' : '−') + eur(Math.abs(num(v))) : NA),
    eurm: (v) => (isNum(v) ? 'EUR ' + halfEven(num(v)) + 'm' : NA),
    eurbn: (v) => (isNum(v) ? 'EUR ' + (num(v) / 1e9).toFixed(1) + 'bn' : NA),
    prose: (v) => (v === null || v === undefined || v === '' ? NA : String(v).replace(/>=/g, '≥').replace(/<=/g, '≤').replace(/\+\/-/g, '±')),
    yesno: (v) => (v === true || v === 'true' ? 'Yes' : v === false || v === 'false' ? 'No' : NA),
  };
  const fmtMonth = d3.utcFormat('%b %Y');
  const utc = (iso) => new Date(String(iso).slice(0, 10) + 'T00:00:00Z');

  /* ---------------- data access ---------------- */
  const rowsOf = (id) => {
    const d = D.data(id);
    return d && d.status === 'ok' && Array.isArray(d.data) ? d.data : null;
  };
  const statusOf = (ids) => {
    const st = ids.map((id) => D.data(id).status);
    if (st.every((s) => s === 'ok')) return 'ok';
    if (st.some((s) => s === 'error' || s === 'missing' || s === 'declined' || s === 'connect')) return 'error';
    return 'loading';
  };
  const parseWhere = (s) => s.split('&').filter(Boolean).map((p) => {
    const i = p.indexOf('=');
    return [decodeURIComponent(p.slice(0, i)), decodeURIComponent(p.slice(i + 1))];
  });
  const findRow = (rows, el) => {
    if (el.dataset.where) {
      const c = parseWhere(el.dataset.where);
      return rows.find((r) => c.every(([k, v]) => String(r[k]) === v));
    }
    if (el.dataset.row !== undefined) return rows[Number(el.dataset.row)];
    return rows[0];
  };
  // A chart's box: empty while loading, one line when a source fails, true when every source is ready.
  const ready = (el, ids) => {
    const st = statusOf(ids);
    el.classList.toggle('dash-skeleton', st === 'loading');
    el.classList.toggle('rp-failed', st === 'error');
    if (st === 'ok') return true;
    el.replaceChildren();
    if (st === 'error') el.textContent = 'Failed to load';
    return false;
  };

  /* ---------------- chips ---------------- */
  const TONE = {
    Green: 'ok', Amber: 'warn', Red: 'bad', High: 'bad', Medium: 'warn', Low: 'ok',
    Complete: 'done', 'On track': 'ok', 'At risk': 'warn', Planned: 'plan', Fixed: 'fixed',
    'In progress': 'active', 'Not started': 'plan', 'For decision': 'active',
  };
  const toneOf = (v) => TONE[v] || (String(v).startsWith('Endorsed') ? 'done' : 'plan');
  const chip = (el, v, size) => {
    el.className = 'rp-chip rp-chip--' + toneOf(v) + (size ? ' rp-chip--' + size : '');
    const dot = document.createElement('span');
    dot.className = 'rp-chip__dot';
    dot.setAttribute('aria-hidden', 'true');
    el.replaceChildren(dot, document.createTextNode(String(v)));
  };
  const TREND = { Rising: '↑', Falling: '↓', Stable: '→', New: '•' };

  /* ---------------- generic drawings: values, chips, tables ---------------- */
  D.draw('v', (el) => {
    const id = el.dataset.source;
    const st = statusOf([id]);
    el.classList.toggle('dash-skeleton', st === 'loading');
    if (st !== 'ok') { el.textContent = NA; return; }
    const row = findRow(rowsOf(id), el);
    const val = row ? row[el.dataset.field] : undefined;
    el.textContent = (F[el.dataset.fmt] || F.text)(val);
  });

  D.draw('rag', (el) => {
    const id = el.dataset.source;
    const st = statusOf([id]);
    if (st !== 'ok') { el.className = 'rp-chip' + (el.dataset.size ? ' rp-chip--' + el.dataset.size : '') + (st === 'loading' ? ' dash-skeleton' : ''); el.textContent = NA; return; }
    const row = findRow(rowsOf(id), el);
    const val = row ? row[el.dataset.field] : undefined;
    if (val === undefined || val === null || val === '') { el.textContent = NA; return; }
    chip(el, val, el.dataset.size);
  });

  D.draw('c-tol', (el) => { el.textContent = '±' + Math.round(TOLERANCE * 100) + '%'; });

  const sorter = (spec) => {
    const keys = spec.split(',').map((k) => k.trim()).filter(Boolean).map((k) => (k[0] === '-' ? [k.slice(1), -1] : [k, 1]));
    return (a, b) => {
      for (const [k, dir] of keys) {
        const x = a[k];
        const y = b[k];
        if (x === y) continue;
        if (x === null || x === undefined) return 1;
        if (y === null || y === undefined) return -1;
        const c = typeof x === 'number' && typeof y === 'number' ? x - y
          : typeof x === 'boolean' ? Number(x) - Number(y)
            : String(x).localeCompare(String(y), 'en', { numeric: true });
        if (c) return c * dir;
      }
      return 0;
    };
  };
  const cell = (td, v, fmt) => {
    if (fmt === 'rag') {
      if (v === null || v === undefined || v === '') { td.textContent = NA; return; }
      const s = document.createElement('span');
      chip(s, v);
      td.append(s);
      return;
    }
    if (fmt === 'trend') { td.textContent = (TREND[v] ? TREND[v] + ' ' : '') + F.text(v); return; }
    td.textContent = (F[fmt] || F.text)(v);
  };
  D.draw('tbl', (tbody) => {
    const table = tbody.closest('table');
    if (!table) return;
    const id = table.dataset.source;
    const st = statusOf([id]);
    tbody.replaceChildren();
    table.classList.toggle('dash-skeleton', st === 'loading');
    if (st !== 'ok') return;
    let rows = rowsOf(id).slice();
    if (table.dataset.subset) {
      const c = parseWhere(table.dataset.subset);
      rows = rows.filter((r) => c.every(([k, v]) => String(r[k]) === v));
    }
    if (table.dataset.sort) rows.sort(sorter(table.dataset.sort));
    const off = Number(table.dataset.offset || 0);
    const lim = table.dataset.limit ? Number(table.dataset.limit) : Infinity;
    rows = rows.slice(off, off + lim);
    const cols = [...table.querySelectorAll('thead th')].map((th) => ({
      field: th.dataset.field,
      fmt: th.dataset.fmt || 'text',
      cls: [th.className, th.dataset.cls || ''].join(' ').trim(),
    }));
    const key = table.dataset.rowKey;
    for (const r of rows) {
      const tr = document.createElement('tr');
      tr.dataset.key = String(r[key]);
      for (const c of cols) {
        const td = document.createElement('td');
        if (c.cls) td.className = c.cls;
        cell(td, r[c.field], c.fmt);
        tr.append(td);
      }
      tbody.append(tr);
    }
  });

  D.draw('ragbar', (el) => {
    const id = el.dataset.source;
    if (!ready(el, [id])) return;
    const rows = rowsOf(id);
    const key = Object.keys(rows[0] || {}).find((k) => k !== 'rag');
    const bar = document.createElement('div');
    bar.className = 'rp-ragbar';
    for (const r of rows) {
      const n = num(r[key]);
      if (!n) continue;
      const s = document.createElement('span');
      s.className = 'rp-ragbar__seg rp-ragbar__seg--' + toneOf(r.rag);
      s.style.flexGrow = String(n);
      bar.append(s);
    }
    el.replaceChildren(bar);
    el.setAttribute('aria-label', rows.map((r) => r[key] + ' ' + r.rag).join(', '));
  });

  /* ---------------- chart kit ---------------- */
  const svgEl = (tag, attrs, parent) => {
    const e = document.createElementNS(NS, tag);
    if (attrs) for (const [k, v] of Object.entries(attrs)) if (v !== null && v !== undefined) e.setAttribute(k, v);
    if (parent) parent.append(e);
    return e;
  };
  const paint = (e, fill, stroke) => { if (fill) e.style.fill = fill; if (stroke) e.style.stroke = stroke; return e; };
  const txt = (parent, x, y, s, anchor, cls) => {
    const t = svgEl('text', { x, y, 'text-anchor': anchor || 'start', class: cls || null }, parent);
    t.textContent = s;
    return t;
  };
  const diamond = (cx, cy, r) => `M${cx},${cy - r}L${cx + r},${cy}L${cx},${cy + r}L${cx - r},${cy}Z`;
  // Horizontal bar with a rounded data end and a square baseline.
  const hbarPath = (x0, y0, w, h, r) => {
    const rr = Math.max(0, Math.min(r, h / 2, w));
    return `M${x0},${y0}h${Math.max(0, w - rr)}a${rr},${rr} 0 0 1 ${rr},${rr}v${h - 2 * rr}a${rr},${rr} 0 0 1 ${-rr},${rr}h${-Math.max(0, w - rr)}z`;
  };
  const makeTip = (host, box) => ({
    show(head, lines, x, y, note) {
      box.replaceChildren();
      if (head) { const h = document.createElement('div'); h.className = 'rp-tip__h'; h.textContent = head; box.append(h); }
      for (const l of lines || []) {
        const row = document.createElement('div');
        row.className = 'rp-tip__r';
        if (l.color) { const k = document.createElement('span'); k.className = 'rp-tip__k'; k.style.color = l.color; row.append(k); }
        const b = document.createElement('b'); b.textContent = l.value; row.append(b);
        if (l.label) { const s = document.createElement('span'); s.textContent = l.label; row.append(s); }
        box.append(row);
      }
      if (note) { const n = document.createElement('div'); n.className = 'rp-tip__note'; n.textContent = note; box.append(n); }
      box.hidden = false;
      const hw = host.clientWidth;
      const bw = box.offsetWidth;
      const bh = box.offsetHeight;
      let left = x + 14;
      if (left + bw > hw) left = x - 14 - bw;
      if (left < 0) left = Math.max(0, Math.min(hw - bw, x - bw / 2));
      let top = y - bh - 10;
      if (top < 0) top = y + 14;
      box.style.left = Math.round(left) + 'px';
      box.style.top = Math.round(top) + 'px';
    },
    hide() { box.hidden = true; },
  });
  // Builds the drawing's SVG at the element's own width, with a text measurer and a tooltip.
  const stage = (el, height) => {
    const W = Math.max(260, Math.floor(el.clientWidth || 600));
    const svg = svgEl('svg', { width: '100%', viewBox: `0 0 ${W} ${height}`, focusable: 'false' });
    const box = document.createElement('div');
    box.className = 'rp-tip';
    box.setAttribute('role', 'status');
    box.hidden = true;
    el.replaceChildren(svg, box);
    const probe = svgEl('text', { x: 0, y: -50 }, svg);
    const S = {
      el, svg, W, H: height, tip: makeTip(el, box),
      measure(s, cls) { probe.setAttribute('class', cls || ''); probe.textContent = s; return probe.getComputedTextLength(); },
      setH(h) { S.H = h; svg.setAttribute('viewBox', `0 0 ${W} ${h}`); el.style.minHeight = h + 'px'; },
      done() { probe.remove(); },
      toSvg(ev) { const r = svg.getBoundingClientRect(); const k = W / (r.width || W); return { x: (ev.clientX - r.left) * k, y: (ev.clientY - r.top) * k }; },
    };
    S.setH(height);
    return S;
  };
  // Keeps in-chart labels from meeting each other or the drawing's edges.
  const Labels = (S) => {
    const boxes = [];
    const over = (a, b) => a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
    return {
      box(x, y, w, anchor, h = 16) { const x0 = anchor === 'end' ? x - w : anchor === 'middle' ? x - w / 2 : x; return { x: x0, y: y - 12, w, h }; },
      fits(b) { return b.x >= 0 && b.x + b.w <= S.W && b.y >= 0 && b.y + b.h <= S.H && !boxes.some((o) => over(o, b)); },
      add(b) { boxes.push(b); },
      place(parent, x, y, s, anchor, cls) {
        const b = this.box(x, y, S.measure(s, cls), anchor);
        if (!this.fits(b)) return null;
        boxes.push(b);
        return txt(parent, x, y, s, anchor, ((cls || '') + ' rp-halo').trim());
      },
    };
  };
  // Axis labels along x: centred on their ticks, kept inside the drawing, skipped where they would meet.
  const xLabels = (S, g, items, y, L) => {
    let right = -Infinity;
    for (const it of items) {
      const w = S.measure(it.text);
      let anchor = 'middle';
      let tx = it.x;
      let x0 = it.x - w / 2;
      if (x0 < 0) { anchor = 'start'; tx = 0; x0 = 0; }
      if (x0 + w > S.W) { anchor = 'end'; tx = S.W; x0 = S.W - w; }
      if (x0 < right + 10) continue;
      const b = { x: x0, y: y - 12, w, h: 16 };
      if (L && !L.fits(b)) continue;
      if (L) L.add(b);
      right = x0 + w;
      txt(g, tx, y, it.text, anchor);
    }
  };
  // Pointer and keyboard reading of a chart: `pick` finds the item under the pointer, arrows step through items.
  const interact = (S, items, pick, highlight, start) => {
    const el = S.el;
    let cur = -1;
    const show = (i) => {
      if (i < 0 || i >= items.length) return;
      cur = i;
      const it = items[i];
      if (highlight) highlight(i);
      S.tip.show(it.head, it.lines, it.x, it.y, it.note);
    };
    const hide = () => { cur = -1; if (highlight) highlight(-1); S.tip.hide(); };
    S.svg.onpointermove = (ev) => { const p = S.toSvg(ev); const i = pick(p.x, p.y); if (i < 0) hide(); else if (i !== cur) show(i); };
    S.svg.onpointerleave = hide;
    el.tabIndex = 0;
    el.onfocus = () => show(cur >= 0 ? cur : start || 0);
    el.onblur = hide;
    el.onkeydown = (ev) => {
      if (ev.key === 'ArrowRight' || ev.key === 'ArrowDown') { ev.preventDefault(); show(Math.min(items.length - 1, cur + 1)); }
      else if (ev.key === 'ArrowLeft' || ev.key === 'ArrowUp') { ev.preventDefault(); show(Math.max(0, cur - 1)); }
      else if (ev.key === 'Escape') hide();
    };
  };
  const nearestX = (items, x, maxD) => {
    let best = -1;
    let bd = Infinity;
    items.forEach((it, i) => { const d = Math.abs(it.x - x); if (d < bd) { bd = d; best = i; } });
    return bd <= (maxD === undefined ? Infinity : maxD) ? best : -1;
  };

  /* ---------------- ranked horizontal bars ---------------- */
  // items: {label, value, text, color, head, lines, note}; o: {max, ref: {value, label}}
  const hbars = (el, items, o) => {
    const S = stage(el, 200);
    const W = S.W;
    const labelW = d3.max(items, (it) => S.measure(it.label)) || 0;
    const valueW = d3.max(items, (it) => S.measure(it.text, 'rp-t-strong')) || 0;
    const side = W >= 440 && labelW <= W * 0.42;
    const ml = side ? Math.ceil(labelW) + 14 : 0;
    const mr = Math.ceil(valueW) + 10;
    const mt = o.ref ? 26 : 4;
    const rowH = side ? 26 : 40;
    const barH = 12;
    const H = mt + items.length * rowH + 4;
    S.setH(H);
    const x = d3.scaleLinear([0, o.max], [ml, W - mr]);
    const g = svgEl('g', null, S.svg);
    const L = Labels(S);
    if (side) svgEl('line', { class: 'rp-axis-line', x1: ml, x2: ml, y1: mt - 2, y2: H - 2 }, g);
    const barY = (i) => mt + i * rowH + (side ? (rowH - barH) / 2 : rowH - barH - 6);
    const bars = items.map((it, i) => {
      const y0 = barY(i);
      if (side) L.place(g, ml - 10, y0 + barH - 2, it.label, 'end', 'rp-t-ink');
      else L.place(g, 0, y0 - 5, it.label, 'start', 'rp-t-ink');
      const w = Math.max(1, x(it.value) - ml);
      const p = paint(svgEl('path', { d: hbarPath(ml, y0, w, barH, 2), class: 'rp-anim' }, g), it.color);
      L.place(g, ml + w + 6, y0 + barH - 2, it.text, 'start', 'rp-t-strong');
      return p;
    });
    if (o.ref) {
      const rx = x(o.ref.value);
      svgEl('line', { class: 'rp-ref', x1: rx, x2: rx, y1: mt - 8, y2: H - 2 }, g);
      const s = o.ref.label;
      const w = S.measure(s);
      const anchor = rx + w / 2 > W ? 'end' : rx - w / 2 < 0 ? 'start' : 'middle';
      L.place(g, anchor === 'end' ? W : anchor === 'start' ? 0 : rx, 13, s, anchor);
    }
    S.done();
    const pts = items.map((it, i) => ({ ...it, x: Math.min(W - 40, x(it.value)), y: barY(i), y0: mt + i * rowH, y1: mt + (i + 1) * rowH }));
    interact(S, pts, (px, py) => pts.findIndex((p) => py >= p.y0 && py < p.y1),
      (k) => bars.forEach((b, i) => { b.style.opacity = k < 0 || k === i ? '1' : '0.45'; }));
  };

  D.draw('ch-domains', (el) => {
    if (!ready(el, ['domains', 'readiness_plan'])) return;
    const rows = rowsOf('domains').map((r) => ({ ...r, v: num(r.readiness) })).sort((a, b) => b.v - a.v || String(a.id).localeCompare(String(b.id), 'en', { numeric: true }));
    const target = rowsOf('readiness_plan').find((r) => isNum(r.target));
    const best = rows[0].id;
    const worst = rows[rows.length - 1].id;
    hbars(el, rows.map((r) => ({
      label: r.domain,
      value: r.v,
      text: F.pct(r.v),
      color: r.id === worst ? SIGNAL : r.id === best ? TEAL : MUTED,
      head: r.name,
      lines: [{ value: F.pct(r.v), label: 'readiness index' }, { value: F.level(r.avg_level), label: 'average level on the 0–4 scale' }],
      note: r.id === worst ? 'Binding constraint' : r.id === best ? 'Strongest domain' : '',
    })), { max: 1, ref: target ? { value: num(target.target), label: target.month + ' target ' + F.pct(target.target) } : null });
  });

  D.draw('ch-families', (el) => {
    if (!ready(el, ['families', 'kpis'])) return;
    const k01 = rowsOf('kpis').find((k) => k.id === 'K01');
    const rows = rowsOf('families').map((r) => ({ ...r, v: num(r.readiness) })).sort((a, b) => b.v - a.v || String(a.family).localeCompare(String(b.family)));
    const prov = (r) => r.provisional === true || r.provisional === 'true';
    hbars(el, rows.map((r) => ({
      label: r.family + (prov(r) ? '*' : ''),
      value: r.v,
      text: F.pct(r.v),
      color: CLASS_COLOR[r.class_group] || MUTED,
      head: r.family,
      lines: [
        { value: F.pct(r.v), label: 'readiness index', color: CLASS_COLOR[r.class_group] },
        { value: r.cra_class, label: '' },
        { value: r.route, label: 'route' },
        { value: F.num1(r.eu_revenue_m), label: 'EUR m EU revenue' },
      ],
      note: r.bu + ' · ' + r.wave,
    })), { max: 1, ref: k01 ? { value: num(k01.value), label: 'Portfolio ' + F.pct(k01.value) } : null });
  });

  D.draw('ch-budget', (el) => {
    if (!ready(el, ['budget_bars'])) return;
    const rows = rowsOf('budget_bars').map((r) => ({ ...r, v: num(r.one_off) }));
    const total = d3.sum(rows, (r) => r.v);
    rows.sort((a, b) => (a.kind === 'Contingency') - (b.kind === 'Contingency') || b.v - a.v);
    hbars(el, rows.map((r) => ({
      label: r.line,
      value: r.v,
      text: F.eur(r.v),
      color: r.kind === 'Contingency' ? MUTED : TEAL,
      head: r.line,
      lines: [{ value: F.eur(r.v), label: 'one-off to Dec 2027' }, { value: F.pct(r.v / total), label: 'of the one-off total' }],
    })), { max: d3.max(rows, (r) => r.v) * 1.02, ref: null });
  });

  /* ---------------- line charts ---------------- */
  D.draw('ch-readiness', (el) => {
    if (!ready(el, ['readiness_plan'])) return;
    const rows = rowsOf('readiness_plan').map((r) => ({ ...r, d: utc(r.month_iso), plan: num(r.plan), actual: num(r.actual), target: num(r.target) }));
    const H = 236;
    const S = stage(el, H);
    const W = S.W;
    const ticks = [0, 0.25, 0.5, 0.75, 1];
    const last = rows[rows.length - 1];
    const endText = F.pct(last.plan) + ' plan';
    const ml = Math.ceil(d3.max(ticks, (t) => S.measure(F.pct(t)))) + 10;
    const mr = Math.ceil(S.measure(endText, 'rp-t-strong')) + 14;
    const mt = 10;
    const mb = 26;
    const x = d3.scaleUtc([rows[0].d, last.d], [ml, W - mr]);
    const y = d3.scaleLinear([0, 1], [H - mb, mt]);
    const g = svgEl('g', null, S.svg);
    const L = Labels(S);
    for (const t of ticks) {
      svgEl('line', { class: t === 0 ? 'rp-axis-line' : 'rp-grid-line', x1: ml, x2: W - mr, y1: y(t), y2: y(t) }, g);
      L.add({ x: 0, y: y(t) - 8, w: ml - 6, h: 14 });
      txt(g, ml - 8, y(t) + 4, F.pct(t), 'end');
    }
    xLabels(S, g, rows.filter((r, i) => i % 3 === 0).map((r) => ({ x: x(r.d), text: fmtMonth(r.d) })), H - 6, L);
    paint(svgEl('path', { d: d3.area().x((r) => x(r.d)).y0(y(0)).y1((r) => y(r.plan))(rows) }, g), tint(NAVY, 7));
    paint(svgEl('path', { d: d3.line().x((r) => x(r.d)).y((r) => y(r.plan))(rows), fill: 'none', 'stroke-width': 2, 'stroke-dasharray': '5 4' }, g), null, NAVY);
    for (const r of rows.filter((q) => q.target !== null)) {
      paint(svgEl('path', { d: diamond(x(r.d), y(r.target), 6), 'stroke-width': 1.5 }, g), PANEL, INK);
    }
    paint(svgEl('circle', { cx: x(last.d), cy: y(last.plan), r: 3.5 }, g), NAVY);
    L.place(g, x(last.d) + 8, y(last.plan) + 4, endText, 'start', 'rp-t-strong');
    for (const r of rows.filter((q) => q.actual !== null)) {
      const cx = x(r.d);
      const cy = y(r.actual);
      paint(svgEl('circle', { cx, cy, r: 5.5, 'stroke-width': 2 }, g), TEAL, PANEL);
      const s = F.pct(r.actual) + ' actual';
      if (!L.place(g, cx + 10, cy + 18, s, 'start', 'rp-t-strong')) L.place(g, cx + 10, cy - 10, s, 'start', 'rp-t-strong');
    }
    const cross = svgEl('line', { class: 'rp-cross', y1: mt, y2: H - mb, visibility: 'hidden' }, g);
    const hot = paint(svgEl('circle', { r: 4, 'stroke-width': 2, visibility: 'hidden' }, g), NAVY, PANEL);
    S.done();
    const items = rows.map((r) => {
      const lines = [{ value: F.pct(r.plan), label: 'plan', color: NAVY }];
      if (r.actual !== null) lines.push({ value: F.pct(r.actual), label: 'actual', color: TEAL });
      if (r.target !== null) lines.push({ value: F.pct(r.target), label: 'target', color: INK });
      return { x: x(r.d), y: y(r.plan), head: r.month, lines };
    });
    interact(S, items, (px) => (px < ml - 4 || px > W - mr + 4 ? -1 : nearestX(items, px)), (i) => {
      const vis = i < 0 ? 'hidden' : 'visible';
      cross.setAttribute('visibility', vis);
      hot.setAttribute('visibility', vis);
      if (i >= 0) { cross.setAttribute('x1', items[i].x); cross.setAttribute('x2', items[i].x); hot.setAttribute('cx', items[i].x); hot.setAttribute('cy', items[i].y); }
    }, rows.findIndex((r) => r.actual !== null));
  });

  D.draw('ch-sbom', (el) => {
    if (!ready(el, ['sbom_coverage'])) return;
    const rows = rowsOf('sbom_coverage').map((r) => ({ ...r, d: utc(r.month_iso), v: num(r.coverage) })).sort((a, b) => a.d - b.d);
    const measured = rows.filter((r) => r.basis !== 'Plan');
    const lastMeasured = measured[measured.length - 1];
    const plan = [lastMeasured, ...rows.filter((r) => r.basis === 'Plan')].filter(Boolean);
    const H = 236;
    const S = stage(el, H);
    const W = S.W;
    const ticks = [0, 0.25, 0.5, 0.75, 1];
    const last = rows[rows.length - 1];
    const endText = F.pct(last.v);
    const ml = Math.ceil(d3.max(ticks, (t) => S.measure(F.pct(t)))) + 10;
    const mr = Math.ceil(S.measure(endText, 'rp-t-strong')) + 14;
    const mt = 10;
    const mb = 26;
    const x = d3.scaleUtc([rows[0].d, last.d], [ml, W - mr]);
    const y = d3.scaleLinear([0, 1], [H - mb, mt]);
    const g = svgEl('g', null, S.svg);
    const L = Labels(S);
    for (const t of ticks) {
      svgEl('line', { class: t === 0 ? 'rp-axis-line' : 'rp-grid-line', x1: ml, x2: W - mr, y1: y(t), y2: y(t) }, g);
      L.add({ x: 0, y: y(t) - 8, w: ml - 6, h: 14 });
      txt(g, ml - 8, y(t) + 4, F.pct(t), 'end');
    }
    const step = W < 420 ? 3 : 2;
    xLabels(S, g, rows.filter((r, i) => i % step === 0).map((r) => ({ x: x(r.d), text: fmtMonth(r.d) })), H - 6, L);
    paint(svgEl('path', { d: d3.line().x((r) => x(r.d)).y((r) => y(r.v))(plan), fill: 'none', 'stroke-width': 2, 'stroke-dasharray': '5 4' }, g), null, NAVY);
    paint(svgEl('circle', { cx: x(last.d), cy: y(last.v), r: 3.5 }, g), NAVY);
    L.place(g, x(last.d) + 8, y(last.v) + 4, endText, 'start', 'rp-t-strong');
    paint(svgEl('path', { d: d3.line().x((r) => x(r.d)).y((r) => y(r.v))(measured), fill: 'none', 'stroke-width': 2, 'stroke-linecap': 'round' }, g), null, TEAL);
    for (const r of measured) {
      const cx = x(r.d);
      const cy = y(r.v);
      paint(svgEl('circle', { cx, cy, r: 5, 'stroke-width': 2 }, g), TEAL, PANEL);
      const s = F.pct(r.v);
      if (!L.place(g, cx, cy - 12, s, 'middle', 'rp-t-strong')) L.place(g, cx + 9, cy + 16, s, 'start', 'rp-t-strong');
    }
    const cross = svgEl('line', { class: 'rp-cross', y1: mt, y2: H - mb, visibility: 'hidden' }, g);
    S.done();
    const items = rows.map((r) => ({ x: x(r.d), y: y(r.v), head: r.month, lines: [{ value: F.pct(r.v), label: r.basis.toLowerCase(), color: r.basis === 'Plan' ? NAVY : TEAL }] }));
    interact(S, items, (px) => (px < ml - 4 || px > W - mr + 4 ? -1 : nearestX(items, px)), (i) => {
      cross.setAttribute('visibility', i < 0 ? 'hidden' : 'visible');
      if (i >= 0) { cross.setAttribute('x1', items[i].x); cross.setAttribute('x2', items[i].x); }
    }, rows.indexOf(lastMeasured));
  });

  D.draw('ch-spend', (el) => {
    if (!ready(el, ['spend'])) return;
    const rows = rowsOf('spend').map((r) => ({ ...r, d: utc(r.month_iso), plan: num(r.cumulative_plan), actual: num(r.cumulative_actual) })).sort((a, b) => a.d - b.d);
    const H = 246;
    const S = stage(el, H);
    const W = S.W;
    const top = d3.max(rows, (r) => Math.max(r.plan * (1 + TOLERANCE), r.actual || 0));
    const stepY = d3.tickIncrement(0, top, 4) > 0 ? d3.tickIncrement(0, top, 4) : top / 4;
    const yMax = Math.ceil(top / stepY) * stepY;
    const ticks = d3.range(0, yMax + stepY / 2, stepY);
    const tickText = (t) => (t === 0 ? '0' : d3.format('~g')(t / 1e6) + 'm');
    const last = rows[rows.length - 1];
    const endText = F.eur(last.plan);
    const ml = Math.ceil(d3.max(ticks, (t) => S.measure(tickText(t)))) + 10;
    const mr = Math.ceil(S.measure(endText, 'rp-t-strong')) + 14;
    const mt = 10;
    const mb = 26;
    const x = d3.scaleUtc([rows[0].d, last.d], [ml, W - mr]);
    const y = d3.scaleLinear([0, yMax], [H - mb, mt]);
    const g = svgEl('g', null, S.svg);
    const L = Labels(S);
    for (const t of ticks) {
      svgEl('line', { class: t === 0 ? 'rp-axis-line' : 'rp-grid-line', x1: ml, x2: W - mr, y1: y(t), y2: y(t) }, g);
      L.add({ x: 0, y: y(t) - 8, w: ml - 6, h: 14 });
      txt(g, ml - 8, y(t) + 4, tickText(t), 'end');
    }
    xLabels(S, g, rows.filter((r, i) => i % 3 === 0).map((r) => ({ x: x(r.d), text: fmtMonth(r.d) })), H - 6, L);
    paint(svgEl('path', { d: d3.area().x((r) => x(r.d)).y0((r) => y(r.plan * (1 - TOLERANCE))).y1((r) => y(r.plan * (1 + TOLERANCE)))(rows) }, g), tint(NAVY, 14));
    paint(svgEl('path', { d: d3.line().x((r) => x(r.d)).y((r) => y(r.plan))(rows), fill: 'none', 'stroke-width': 2, 'stroke-dasharray': '5 4' }, g), null, NAVY);
    paint(svgEl('circle', { cx: x(last.d), cy: y(last.plan), r: 3.5 }, g), NAVY);
    L.place(g, x(last.d) + 8, y(last.plan) + 4, endText, 'start', 'rp-t-strong');
    for (const r of rows.filter((q) => q.actual !== null)) {
      const cx = x(r.d);
      const cy = y(r.actual);
      paint(svgEl('circle', { cx, cy, r: 5.5, 'stroke-width': 2 }, g), TEAL, PANEL);
      const s = F.eur(r.actual) + ' actual';
      if (!L.place(g, cx + 10, cy - 10, s, 'start', 'rp-t-strong')) L.place(g, cx + 10, cy + 18, s, 'start', 'rp-t-strong');
    }
    const cross = svgEl('line', { class: 'rp-cross', y1: mt, y2: H - mb, visibility: 'hidden' }, g);
    const hot = paint(svgEl('circle', { r: 4, 'stroke-width': 2, visibility: 'hidden' }, g), NAVY, PANEL);
    S.done();
    const items = rows.map((r) => {
      const lines = [{ value: F.eur(r.plan), label: 'cumulative plan', color: NAVY }];
      if (r.actual !== null) lines.push({ value: F.eur(r.actual), label: 'cumulative actual', color: TEAL });
      return { x: x(r.d), y: y(r.plan), head: r.month, lines, note: 'Tolerance ' + F.eur(r.plan * (1 - TOLERANCE)) + ' to ' + F.eur(r.plan * (1 + TOLERANCE)) };
    });
    interact(S, items, (px) => (px < ml - 4 || px > W - mr + 4 ? -1 : nearestX(items, px)), (i) => {
      const vis = i < 0 ? 'hidden' : 'visible';
      cross.setAttribute('visibility', vis);
      hot.setAttribute('visibility', vis);
      if (i >= 0) { cross.setAttribute('x1', items[i].x); cross.setAttribute('x2', items[i].x); hot.setAttribute('cx', items[i].x); hot.setAttribute('cy', items[i].y); }
    }, Math.max(0, rows.findIndex((r) => r.actual !== null)));
  });

  /* ---------------- bullet: spend to date ---------------- */
  D.draw('ch-variance', (el) => {
    if (!ready(el, ['spend_variance'])) return;
    const r = rowsOf('spend_variance')[0];
    if (!r) { el.replaceChildren(); return; }
    const a = num(r.actual);
    const p = num(r.plan);
    const H = 84;
    const S = stage(el, H);
    const W = S.W;
    const x = d3.scaleLinear([0, Math.max(a, p * (1 + TOLERANCE)) * 1.1], [0, W]);
    const g = svgEl('g', null, S.svg);
    const L = Labels(S);
    paint(svgEl('rect', { x: 0, y: 30, width: W, height: 18, rx: 2 }, g), WASH);
    paint(svgEl('rect', { x: x(p * (1 - TOLERANCE)), y: 26, width: x(p * (1 + TOLERANCE)) - x(p * (1 - TOLERANCE)), height: 26 }, g), tint(NAVY, 18));
    paint(svgEl('path', { d: hbarPath(0, 34, x(a), 10, 2) }, g), TEAL);
    svgEl('line', { x1: x(p), x2: x(p), y1: 22, y2: 56, 'stroke-width': 2 }, g).style.stroke = INK;
    const place = (cx, cy, s) => {
      const w = S.measure(s);
      const anchor = cx - w / 2 < 0 ? 'start' : cx + w / 2 > W ? 'end' : 'middle';
      return L.place(g, anchor === 'start' ? 0 : anchor === 'end' ? W : cx, cy, s, anchor);
    };
    place(x(p), 14, 'Plan ' + F.eur(p));
    place(x(a), 72, 'Actual ' + F.eur(a));
    S.done();
    const items = [{ x: x(a), y: 34, head: r.month, lines: [{ value: F.eur(a), label: 'actual', color: TEAL }, { value: F.eur(p), label: 'plan', color: INK }, { value: F.spct1(r.variance_share), label: 'against plan' }], note: 'Tolerance ' + F.eur(p * (1 - TOLERANCE)) + ' to ' + F.eur(p * (1 + TOLERANCE)) }];
    interact(S, items, (px, py) => (py >= 18 && py <= 60 ? 0 : -1), null, 0);
  });

  /* ---------------- dot plot: cost scenarios ---------------- */
  D.draw('ch-scenarios', (el) => {
    if (!ready(el, ['scenarios'])) return;
    const rows = rowsOf('scenarios').map((r) => ({ ...r, v: num(r.one_off_total) })).sort((a, b) => a.v - b.v);
    const H = 86;
    const S = stage(el, H);
    const W = S.W;
    const lo = (Math.floor(d3.min(rows, (r) => r.v) / 1e6) - 1) * 1e6;
    const hi = (Math.ceil(d3.max(rows, (r) => r.v) / 1e6) + 1) * 1e6;
    const x = d3.scaleLinear([lo, hi], [12, W - 12]);
    const g = svgEl('g', null, S.svg);
    const L = Labels(S);
    const cy = 24;
    svgEl('line', { class: 'rp-grid-line', x1: 12, x2: W - 12, y1: cy, y2: cy }, g);
    paint(svgEl('line', { x1: x(rows[0].v), x2: x(rows[rows.length - 1].v), y1: cy, y2: cy, 'stroke-width': 3, 'stroke-linecap': 'round' }, g), null, MUTED);
    rows.forEach((r) => {
      const base = r.scenario === 'Base';
      paint(svgEl('circle', { cx: x(r.v), cy, r: base ? 7 : 5.5, 'stroke-width': 2 }, g), base ? TEAL : INK_MUTED, PANEL);
    });
    for (const r of rows) {
      const s = r.scenario + ' ' + F.eur(r.v);
      const cls = r.scenario === 'Base' ? 'rp-t-strong' : 'rp-t-ink';
      const w = S.measure(s, cls);
      const cx = x(r.v);
      const anchor = cx - w / 2 < 0 ? 'start' : cx + w / 2 > W ? 'end' : 'middle';
      const tx = anchor === 'start' ? 0 : anchor === 'end' ? W : cx;
      if (!L.place(g, tx, 52, s, anchor, cls)) L.place(g, tx, 70, s, anchor, cls);
    }
    S.done();
    const items = rows.map((r) => ({ x: x(r.v), y: cy, head: r.scenario + ' scenario', lines: [{ value: F.eur(r.v), label: 'one-off to Dec 2027' }, { value: F.eur(num(r.run_2028)), label: 'a year from 2028' }], note: r.description }));
    interact(S, items, (px, py) => (py > 44 ? -1 : nearestX(items, px, 24)), null, rows.findIndex((r) => r.scenario === 'Base'));
  });

  /* ---------------- tall segmented bar: EU revenue by class ---------------- */
  const textOn = (fillEl) => {
    const m = /rgba?\(([^)]+)\)/.exec(getComputedStyle(fillEl).fill || '');
    if (!m) return '#FFFFFF';
    const [r, gg, b] = m[1].split(',').map((v) => Number(v) / 255);
    const lin = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
    const lum = 0.2126 * lin(r) + 0.7152 * lin(gg) + 0.0722 * lin(b);
    return 1.05 / (lum + 0.05) >= (lum + 0.05) / 0.0602 ? '#FFFFFF' : '#0E1A2B';
  };
  D.draw('ch-revenue', (el) => {
    if (!ready(el, ['revenue_by_class'])) return;
    const order = ['Default', 'Class I', 'Class II'];
    const all = rowsOf('revenue_by_class');
    const rows = order.map((k) => all.find((r) => r.class === k)).filter(Boolean).map((r) => ({ ...r, v: num(r.eu_revenue_m), nb: r.needs_nb === true || r.needs_nb === 'true' }));
    const total = d3.sum(rows, (r) => r.v);
    const H = 92;
    const S = stage(el, H);
    const W = S.W;
    const x = d3.scaleLinear([0, total], [0, W]);
    const g = svgEl('g', null, S.svg);
    const L = Labels(S);
    const barY = 30;
    const barH = 28;
    let x0 = 0;
    const blocks = rows.map((r, i) => {
      const w = Math.max(2, x(r.v) - (i < rows.length - 1 ? 2 : 0));
      const rect = paint(svgEl('rect', { x: x0, y: barY, width: w, height: barH, rx: 4, class: 'rp-anim' }, g), CLASS_COLOR[r.class]);
      const b = { r, x0, w, rect };
      x0 += x(r.v);
      return b;
    });
    for (const b of blocks) {
      const s = F.eurm(b.r.v);
      const tw = S.measure(s, 'rp-t-inv');
      if (tw + 16 <= b.w) {
        const t = txt(g, b.x0 + 8, barY + barH / 2 + 4, s, 'start', 'rp-t-inv');
        t.style.fill = textOn(b.rect);
        L.add({ x: b.x0 + 8, y: barY, w: tw, h: barH });
      } else {
        const anchor = b.x0 + b.w - tw < 0 ? 'start' : 'end';
        L.place(g, anchor === 'end' ? Math.min(W, b.x0 + b.w) : b.x0, barY + barH + 16, s, anchor, 'rp-t-strong');
      }
    }
    const nb = blocks.filter((b) => b.r.nb);
    if (nb.length) {
      const bx0 = nb[0].x0;
      const bx1 = nb[nb.length - 1].x0 + nb[nb.length - 1].w;
      paint(svgEl('path', { d: `M${bx0 + 1},${barY - 4}V${barY - 10}H${bx1 - 1}V${barY - 4}`, fill: 'none', 'stroke-width': 1.5 }, g), null, SIGNAL);
      const s = 'Needs a notified body';
      const w = S.measure(s, 'rp-t-signal');
      const mid = (bx0 + bx1) / 2;
      const anchor = mid + w / 2 > W ? 'end' : 'middle';
      L.place(g, anchor === 'end' ? W : mid, barY - 15, s, anchor, 'rp-t-signal');
    }
    S.done();
    const items = blocks.map((b) => ({
      x: b.x0 + b.w / 2, y: barY, x0: b.x0, x1: b.x0 + b.w,
      head: b.r.class,
      lines: [{ value: F.eurm(b.r.v), label: 'EU revenue', color: CLASS_COLOR[b.r.class] }, { value: F.int(b.r.families), label: Number(b.r.families) === 1 ? 'family' : 'families' }, { value: F.eurm(b.r.revenue_m), label: 'group revenue' }],
      note: b.r.nb ? 'Needs a notified body' : 'Self-assessment (Module A) available',
    }));
    interact(S, items, (px, py) => (py < barY - 18 || py > barY + barH + 4 ? -1 : items.findIndex((it) => px >= it.x0 && px <= it.x1 + 2)), (k) => {
      blocks.forEach((b, i) => { b.rect.style.opacity = k < 0 || k === i ? '1' : '0.55'; });
    }, 1);
  });

  /* ---------------- timeline: phases and milestones ---------------- */
  const MS_STYLE = {
    Complete: { fill: TEAL, stroke: TEAL },
    'On track': { fill: PANEL, stroke: TEAL },
    'At risk': { fill: 'var(--color-warn)', stroke: 'var(--color-warn)' },
    Planned: { fill: PANEL, stroke: INK_MUTED },
    Fixed: { fill: INK, stroke: INK },
  };
  const PHASE_COLOR = { Complete: TEAL, 'In progress': NAVY, Planned: MUTED };
  D.draw('ch-plan', (el) => {
    if (!ready(el, ['phases', 'milestones', 'programme_status'])) return;
    const status = rowsOf('programme_status')[0] || {};
    const phases = rowsOf('phases').map((p) => ({ ...p, s: utc(p.start_iso), e: p.end_iso ? utc(p.end_iso) : null }));
    const ms = rowsOf('milestones').map((m) => ({ ...m, d: utc(m.date_iso) })).sort((a, b) => a.d - b.d || String(a.id).localeCompare(String(b.id), 'en', { numeric: true }));
    const asAt = status.data_as_at_iso ? utc(status.data_as_at_iso) : null;
    const d0 = d3.utcMonth.floor(d3.min(phases, (p) => p.s));
    const d1 = d3.utcMonth.offset(d3.utcMonth.floor(d3.max([...phases.map((p) => p.e || p.s), ...ms.map((m) => m.d)])), 1);
    const S = stage(el, 300);
    const W = S.W;
    const x = d3.scaleUtc([d0, d1], [0, W - 4]);
    const R = 6;
    const lanes = [];
    for (const m of ms) {
      m.cx = x(m.d);
      let li = lanes.findIndex((lastX) => m.cx - lastX >= 2 * R + 4);
      if (li < 0) { li = lanes.length; lanes.push(-Infinity); }
      lanes[li] = m.cx;
      m.lane = li;
    }
    const laneH = 16;
    const msTop = 26;
    const rowsTop = msTop + lanes.length * laneH + 10;
    const rowH = 36;
    const axisY = rowsTop + phases.length * rowH + 2;
    const H = axisY + 20;
    S.setH(H);
    const g = svgEl('g', null, S.svg);
    const L = Labels(S);
    const ticks = d3.utcMonth.every(3).range(d0, d1);
    for (const t of ticks) svgEl('line', { class: 'rp-grid-line', x1: x(t), x2: x(t), y1: msTop - 4, y2: axisY }, g);
    svgEl('line', { class: 'rp-axis-line', x1: 0, x2: W - 4, y1: axisY, y2: axisY }, g);
    if (asAt) {
      const ax = x(asAt);
      svgEl('line', { x1: ax, x2: ax, y1: 16, y2: axisY, 'stroke-width': 1.5 }, g).style.stroke = INK;
      const s = 'Data date ' + (status.data_as_at || '');
      if (!L.place(g, ax + 6, 13, s, 'start', 'rp-t-ink')) L.place(g, ax - 6, 13, s, 'end', 'rp-t-ink');
    }
    // phases
    const phaseBars = phases.map((p, i) => {
      const y0 = rowsTop + i * rowH;
      const name = p.id + ' ' + p.phase;
      const dates = p.e ? p.start + ' – ' + p.end : 'from ' + p.start + ', ongoing';
      const full = name + '  ·  ' + dates;
      if (S.measure(full, 'rp-t-ink') <= W - 4) L.place(g, 0, y0 + 12, full, 'start', 'rp-t-ink');
      else L.place(g, 0, y0 + 12, name, 'start', 'rp-t-ink');
      const xs = x(p.s);
      const xe = p.e ? x(p.e) : W - 4;
      const bar = paint(svgEl('rect', { x: xs, y: y0 + 18, width: Math.max(8, xe - xs), height: 10, rx: 2, class: 'rp-anim' }, g), PHASE_COLOR[p.status] || MUTED);
      return { p, bar, y0, xs, xe, dates };
    });
    // milestones
    const marks = ms.map((m) => {
      const cy = msTop + m.lane * laneH + laneH / 2;
      const st = MS_STYLE[m.status] || MS_STYLE.Planned;
      const dm = paint(svgEl('path', { d: diamond(m.cx, cy, R), 'stroke-width': 1.75 }, g), st.fill, st.stroke);
      L.add({ x: m.cx - R, y: cy - R, w: 2 * R, h: 2 * R });
      return { m, dm, cy };
    });
    for (const k of marks.filter((q) => q.m.status === 'At risk')) {
      if (!L.place(g, k.m.cx + R + 4, k.cy + 4, k.m.id, 'start', 'rp-t-strong')) L.place(g, k.m.cx - R - 4, k.cy + 4, k.m.id, 'end', 'rp-t-strong');
    }
    xLabels(S, g, ticks.map((t) => ({ x: x(t), text: fmtMonth(t) })), H - 4, L);
    S.done();
    const items = [
      ...marks.map((k) => ({ kind: 'm', x: k.m.cx, y: k.cy, head: k.m.id + ' · ' + k.m.date, lines: [{ value: k.m.status, label: '' }], note: k.m.milestone })),
      ...phaseBars.map((b) => ({ kind: 'p', x: (b.xs + Math.min(b.xe, W - 4)) / 2, y: b.y0 + 18, y0: b.y0, y1: b.y0 + rowH, head: b.p.id + ' ' + b.p.phase, lines: [{ value: b.p.status, label: '' }, { value: b.dates, label: '' }], note: 'Gate: ' + b.p.gate })),
    ];
    const nMarks = marks.length;
    interact(S, items, (px, py) => {
      if (py < rowsTop - 4) {
        const near = marks.map((k, i) => ({ i, d: Math.hypot(k.m.cx - px, k.cy - py) })).sort((a, b) => a.d - b.d)[0];
        return near && near.d <= 14 ? near.i : -1;
      }
      const j = phaseBars.findIndex((b) => py >= b.y0 && py < b.y0 + rowH);
      return j < 0 ? -1 : nMarks + j;
    }, (i) => {
      marks.forEach((k, j) => { k.dm.style.opacity = i < 0 || i === j || i >= nMarks ? '1' : '0.4'; });
      phaseBars.forEach((b, j) => { b.bar.style.opacity = i < nMarks || i === nMarks + j ? '1' : '0.45'; });
    }, Math.max(0, ms.findIndex((m) => m.status === 'At risk')));
  });

  /* ---------------- risk matrix ---------------- */
  D.draw('matrix', (el) => {
    if (!ready(el, ['risks'])) return;
    const risks = rowsOf('risks').map((r) => ({ ...r, l: num(r.likelihood), i: num(r.impact), s: num(r.score) }));
    const band = (s) => (s >= RISK_HIGH ? 'high' : s >= RISK_MEDIUM ? 'medium' : 'low');
    const div = (cls, text) => { const d = document.createElement('div'); d.className = cls; if (text !== undefined) d.textContent = text; return d; };
    const wrap = div('rp-mx__wrap');
    const tipBox = div('rp-tip');
    tipBox.setAttribute('role', 'status');
    tipBox.hidden = true;
    const tip = makeTip(wrap, tipBox);
    wrap.append(div('rp-mx__ylab', 'Likelihood ↑'));
    const grid = div('rp-mx');
    for (let l = 5; l >= 1; l -= 1) {
      grid.append(div('rp-mx__ax', String(l)));
      for (let i = 1; i <= 5; i += 1) {
        const c = div('rp-mx__cell rp-mx__cell--' + band(l * i));
        const here = risks.filter((r) => r.l === l && r.i === i).sort((a, b) => b.s - a.s || String(a.id).localeCompare(String(b.id)));
        c.setAttribute('aria-label', 'Likelihood ' + l + ', impact ' + i + (here.length ? ': ' + here.map((r) => r.id).join(', ') : ''));
        for (const r of here) {
          const ch = document.createElement('span');
          ch.className = 'rp-mx__chip';
          ch.tabIndex = 0;
          ch.textContent = r.id + (TREND[r.trend] ? ' ' + TREND[r.trend] : '');
          ch.setAttribute('aria-label', r.id + ' ' + r.risk + ': score ' + r.s + ', ' + r.rating + ', ' + r.trend);
          const show = () => {
            const wr = wrap.getBoundingClientRect();
            const cr = ch.getBoundingClientRect();
            tip.show(r.id + ' · ' + r.rating, [{ value: F.int(r.s), label: 'score (likelihood ' + r.l + ' × impact ' + r.i + ')' }, { value: r.trend, label: 'trend' }], cr.left - wr.left + cr.width / 2, cr.top - wr.top, r.risk + ' — ' + r.owner);
          };
          ch.onpointerenter = show;
          ch.onfocus = show;
          ch.onpointerleave = () => tip.hide();
          ch.onblur = () => tip.hide();
          c.append(ch);
        }
        grid.append(c);
      }
    }
    grid.append(div('rp-mx__ax', ''));
    for (let i = 1; i <= 5; i += 1) grid.append(div('rp-mx__ax', String(i)));
    wrap.append(grid);
    const titles = div('rp-mx__titles');
    titles.append(div('', ''), div('', 'Impact →'));
    wrap.append(titles, tipBox);
    const legend = div('rp-legend');
    const item = (cls, text) => { const s = document.createElement('span'); const i = document.createElement('i'); i.className = 'rp-sw ' + cls; s.append(i, document.createTextNode(text)); return s; };
    legend.append(item('rp-mx__cell--high', 'High: score ' + RISK_HIGH + '–25'), item('rp-mx__cell--medium', 'Medium: ' + RISK_MEDIUM + '–' + (RISK_HIGH - 1)), item('rp-mx__cell--low', 'Low: 1–' + (RISK_MEDIUM - 1)));
    el.replaceChildren(wrap, legend);
  });

  /* ---------------- page wiring: status stripe, section links ---------------- */
  D.onData(() => {
    const rows = rowsOf('programme_status');
    const tone = rows && rows[0] ? { Green: 'ok', Amber: 'warn', Red: 'bad' }[rows[0].overall_rag] : null;
    document.querySelectorAll('.rp-strip__cell--rag').forEach((c) => {
      c.classList.toggle('rp-tone-ok', tone === 'ok');
      c.classList.toggle('rp-tone-warn', tone === 'warn');
      c.classList.toggle('rp-tone-bad', tone === 'bad');
    });
  });
  const go = (el) => {
    const smooth = !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    el.scrollIntoView({ behavior: smooth ? 'smooth' : 'auto', block: 'start' });
    D.setLink(el.id);
  };
  document.querySelectorAll('.rp-nav button[data-target]').forEach((b) => {
    b.addEventListener('click', () => { const t = document.getElementById(b.dataset.target); if (t) go(t); });
  });
  let linked = false;
  D.onData(() => {
    if (linked) return;
    const id = decodeURIComponent(location.hash.slice(1));
    const named = id ? document.getElementById(id) : null;
    if (!named || !named.closest('.rp')) { linked = true; return; }
    if (statusOf(['kpis', 'programme_status']) !== 'ok') return;
    linked = true;
    requestAnimationFrame(() => named.scrollIntoView());
  });
  if ('IntersectionObserver' in window) {
    let current = null;
    let armed = false;
    const io = new IntersectionObserver((entries) => {
      if (!armed) { armed = true; return; }
      for (const e of entries) {
        if (e.isIntersecting && e.target.id !== current) { current = e.target.id; D.setLink(current); }
      }
    }, { root: document, rootMargin: '-45% 0px -50% 0px' });
    document.querySelectorAll('.rp [data-sec]').forEach((s) => io.observe(s));
  }
})();
