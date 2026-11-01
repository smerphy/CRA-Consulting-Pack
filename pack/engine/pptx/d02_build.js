// D02 SteerCo pack -> native, editable PowerPoint.
//
// Method: each slide's HTML is rendered in headless Chromium at 1920x1080 with the same harness
// as the reference PDF (render.js: same fonts and slide CSS). The rendered DOM is walked and every
// element is re-emitted as a native PowerPoint object at its measured position:
//   p/h1/h2           -> text boxes (runs keep font, size, weight, colour, letter-spacing)
//   backgrounds       -> rectangles / rounded rectangles (pills keep their text inside)
//   borders           -> line shapes
//   row/column grids  -> native tables (RAG pills inside cells are overlaid as rounded shapes)
//   data charts       -> native PowerPoint charts (readiness bars, market-access stacked bar,
//                        budget cumulative line) with their data
// Speaker notes come from each slide's <aside>.
//
// Usage: node pack/engine/pptx/d02_build.js
// Coordinates: 1920 px = 13.333 in, so 1 px = 1/144 in = 0.5 pt.
'use strict';
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');
const PptxGenJS = require('pptxgenjs');

const ROOT = path.resolve(__dirname, '..', '..', '..');
const DECK_DIR = path.join(ROOT, 'pack', 'out', 'hosted', 'D02-steerco-pack');
const SRC = path.join(DECK_DIR, 'source', 'project');
const OUT_FILE = process.env.D02_OUT || path.join(DECK_DIR, 'D02 - SteerCo pack.pptx');
const FONTDIR = process.env.FONTDIR ||
  path.join(__dirname, 'fonts');

// Static font files that PowerPoint/LibreOffice use; text is letter-spaced to match browser widths.
const STATIC_FACES = [
  ['StaticSerif', '400', '/root/.fonts/SourceSerif4-Regular.ttf'],
  ['StaticSerif', '700', '/root/.fonts/SourceSerif4-Bold.ttf'],
  ['StaticInter', '400', '/usr/share/fonts/opentype/inter/Inter-Regular.otf'],
  ['StaticInter', '700', '/usr/share/fonts/opentype/inter/Inter-Bold.otf'],
  ['StaticMono', '400', '/root/.fonts/JetBrainsMono-Regular.ttf'],
  ['StaticMono', '700', '/root/.fonts/JetBrainsMono-Bold.ttf'],
];
const PX = 1 / 144;          // inches per CSS px
const PT = 0.5;              // points per CSS px

// Same slide CSS as the PDF harness (render.js).
const SLIDE_CSS = `
html,body{margin:0;padding:0;background:#fff}
.page{width:1920px;height:1080px;position:relative;overflow:hidden}
section{width:1920px;height:1080px;position:relative;box-sizing:border-box;overflow:hidden;display:flex;flex-direction:column}
section *{box-sizing:border-box;margin:0}
section div{display:flex;flex-direction:column;min-width:0;min-height:0}
section h1{font-size:96px;font-weight:600;line-height:1.1}
section h2{font-size:64px;font-weight:600;line-height:1.15}
section h3{font-size:44px;font-weight:600;line-height:1.2}
section p{font-size:32px;line-height:1.4}
section ul,section ol{padding-left:1.1em}
section table{border-collapse:collapse;width:100%}
section td,section th{border:1px solid #C5CDD8;padding:0.35em 0.6em;text-align:left;vertical-align:top;font-weight:inherit}
section aside{display:none}
section a{color:inherit}
`;

function fontCss() {
  const f = path.join(FONTDIR, 'local.css');
  if (!fs.existsSync(f)) return '';
  return fs.readFileSync(f, 'utf8').replace(/url\((f\d+\.woff2)\)/g, (m, x) => `url(file://${FONTDIR}/${x})`);
}

function decode(s) {
  return s.replace(/<br\s*\/?>/g, ' ').replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
    .replace(/&#(\d+);/g, (m, n) => String.fromCodePoint(+n)).replace(/\s+/g, ' ').trim();
}

// ---------------------------------------------------------------------------------------------
// Browser side: per-slide preparation (charts) and the generic DOM walk.
// ---------------------------------------------------------------------------------------------
function browserExtract(args) {
  const { idx, slideId } = args;
  const page = document.querySelectorAll('.page')[idx];
  const section = page.querySelector('section');
  const P = page.getBoundingClientRect();
  const R = el => { const r = el.getBoundingClientRect(); return { x: r.left - P.left, y: r.top - P.top, w: r.width, h: r.height }; };
  const items = [];
  const hex = c => {
    if (!c) return null;
    const m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(',').map(s => parseFloat(s));
    if (p.length === 4 && p[3] === 0) return null;
    return p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
  };
  const fam = f => f.split(',')[0].replace(/['"]/g, '').trim();
  const px = v => parseFloat(v) || 0;
  const isText = el => /^(P|H1|H2|H3|H4)$/.test(el.tagName);
  const skip = new Set();
  const charts = [];

  // ---- metric compensation ----
  // PowerPoint renders with the static font files (no optical sizes, Bold for 600), so the same
  // text can come out wider or narrower than in the browser. Measure both and return the extra
  // letter-spacing (px per character) that makes the static rendering as wide as the browser's.
  const STATIC = { 'Source Serif 4': 'StaticSerif', Inter: 'StaticInter', 'JetBrains Mono': 'StaticMono' };
  let probe = document.getElementById('__probe');
  if (!probe) { probe = document.createElement('span'); probe.id = '__probe'; probe.style.cssText = 'position:absolute;left:-9999px;top:0;white-space:pre;letter-spacing:0'; document.body.appendChild(probe); }
  function metricAdj(t, st, f, bold) {
    const txt = t.trim();
    if (!STATIC[f] || txt.length < 2) return 0;
    probe.textContent = txt;
    probe.style.fontSize = st.fontSize; probe.style.fontStyle = st.fontStyle; probe.style.textTransform = st.textTransform;
    probe.style.fontFamily = `"${f}"`; probe.style.fontWeight = st.fontWeight; probe.style.fontVariantNumeric = st.fontVariantNumeric;
    const wb = probe.getBoundingClientRect().width;
    probe.style.fontFamily = STATIC[f]; probe.style.fontWeight = bold ? '700' : '400';
    const ws = probe.getBoundingClientRect().width;
    const lim = px(st.fontSize) * 0.08;
    // the serif's display optical size is much narrower than its static text cut; close most of
    // the gap but keep the static glyphs from touching
    const k = f === 'Source Serif 4' ? 0.75 : 1;
    return Math.max(-lim, Math.min(lim, k * (wb - ws) / txt.length));
  }

  // ---- runs of a text element ----
  function runsOf(el) {
    const out = [];
    const walk = n => {
      if (n.nodeType === 3) {
        const st = getComputedStyle(n.parentElement);
        let t = n.data.replace(/\s+/g, ' ');
        if (st.textTransform === 'uppercase') t = t.toUpperCase();
        const f = fam(st.fontFamily), bold = parseInt(st.fontWeight, 10) >= 600;
        const ls = st.letterSpacing === 'normal' ? 0 : px(st.letterSpacing);
        out.push({
          text: t, font: f, size: px(st.fontSize), bold,
          italic: st.fontStyle === 'italic', color: hex(st.color), ls, adj: metricAdj(t, st, f, bold),
        });
      } else if (n.nodeType === 1) {
        if (n.tagName === 'BR') { out.push({ br: true }); return; }
        n.childNodes.forEach(walk);
      }
    };
    el.childNodes.forEach(walk);
    // merge identical styles, trim ends
    const m = [];
    for (const r of out) {
      const l = m[m.length - 1];
      if (l && !l.br && !r.br && l.font === r.font && l.size === r.size && l.bold === r.bold && l.italic === r.italic && l.color === r.color && l.ls === r.ls) {
        const a = l.text.trim().length, b2 = r.text.trim().length;
        l.adj = a + b2 ? (l.adj * a + r.adj * b2) / (a + b2) : 0; l.text += r.text;
      }
      else m.push({ ...r });
    }
    if (m.length && !m[0].br) m[0].text = m[0].text.replace(/^\s+/, '');
    if (m.length && !m[m.length - 1].br) m[m.length - 1].text = m[m.length - 1].text.replace(/\s+$/, '');
    return m.filter(r => r.br || r.text.length);
  }
  function lineInfo(el) {
    const rg = document.createRange(); rg.selectNodeContents(el);
    const rs = [...rg.getClientRects()].filter(r => r.width > 0.5);
    const tops = [];
    rs.forEach(r => { const c = r.top + r.height / 2; if (!tops.some(t => Math.abs(t - c) < 6)) tops.push(c); });
    const l = Math.min(...rs.map(r => r.left)), rr = Math.max(...rs.map(r => r.right));
    return { lines: tops.length, textW: rs.length ? rr - l : 0, textX: rs.length ? l - P.left : 0 };
  }
  function para(el) {
    const st = getComputedStyle(el);
    let align = st.textAlign; if (align === 'start') align = 'left'; if (align === 'end') align = 'right';
    return { runs: runsOf(el), align, lh: px(st.lineHeight) || px(st.fontSize) * 1.2 };
  }
  function textItem(el) {
    const st = getComputedStyle(el); const r = R(el);
    const pad = [px(st.paddingTop), px(st.paddingRight), px(st.paddingBottom), px(st.paddingLeft)];
    const li = lineInfo(el);
    return { t: 'text', ...r, bT: px(st.borderTopWidth), pad, fill: hex(st.backgroundColor), radius: px(st.borderTopRightRadius), ...para(el), ...li, tag: el.tagName };
  }
  function borderItems(el, r, st) {
    const out = [];
    const sides = ['Top', 'Right', 'Bottom', 'Left'].map(s => ({ s, w: px(st['border' + s + 'Width']), st: st['border' + s + 'Style'], c: hex(st['border' + s + 'Color']) }));
    const all = sides.every(b => b.w > 0 && b.st !== 'none' && b.c === sides[0].c && b.w === sides[0].w);
    if (all) return { outline: { w: sides[0].w, c: sides[0].c, dash: sides[0].st } };
    for (const b of sides) {
      if (!(b.w > 0) || b.st === 'none' || !b.c) continue;
      const d = b.st === 'dashed' ? 'dash' : b.st === 'dotted' ? 'sysDot' : 'solid';
      if (b.s === 'Top') out.push({ t: 'line', x1: r.x, y1: r.y + b.w / 2, x2: r.x + r.w, y2: r.y + b.w / 2, w: b.w, c: b.c, dash: d });
      if (b.s === 'Bottom') out.push({ t: 'line', x1: r.x, y1: r.y + r.h - b.w / 2, x2: r.x + r.w, y2: r.y + r.h - b.w / 2, w: b.w, c: b.c, dash: d });
      if (b.s === 'Left') out.push({ t: 'line', x1: r.x + b.w / 2, y1: r.y, x2: r.x + b.w / 2, y2: r.y + r.h, w: b.w, c: b.c, dash: d });
      if (b.s === 'Right') out.push({ t: 'line', x1: r.x + r.w - b.w / 2, y1: r.y, x2: r.x + r.w - b.w / 2, y2: r.y + r.h, w: b.w, c: b.c, dash: d });
    }
    return { lines: out };
  }
  const isPill = el => isText(el) && !!hex(getComputedStyle(el).backgroundColor);

  // ---- table detection: a column of >=3 flex rows with the same >=3 aligned cells ----
  function tableOf(el) {
    if (el.tagName !== 'DIV') return null;
    const st = getComputedStyle(el);
    if (st.flexDirection !== 'column' || st.display !== 'flex') return null;
    const rows = [...el.children];
    if (rows.length < 3) return null;
    if (!rows.every(r => r.tagName === 'DIV' && getComputedStyle(r).flexDirection === 'row')) return null;
    const n = rows[0].children.length;
    if (n < 3 || !rows.every(r => r.children.length === n)) return null;
    const lefts0 = [...rows[0].children].map(c => R(c).x);
    for (const r of rows) {
      const cells = [...r.children];
      for (let i = 0; i < n; i++) {
        const c = cells[i];
        if (Math.abs(R(c).x - lefts0[i]) > 3) return null;
        if (!c.textContent.trim()) return null;
        if ([c, ...c.querySelectorAll('*')].some(d => getComputedStyle(d).position === 'absolute')) return null;
        if (!isText(c) && hex(getComputedStyle(c).backgroundColor)) return null;
      }
    }
    // build the table
    const T = R(el);
    const r0 = rows[0], rr0 = R(r0), c0 = [...r0.children].map(R);
    const colStart = c0.map((c, i) => (i === 0 ? rr0.x : c.x));
    const colEnd = c0.map((c, i) => (i === n - 1 ? rr0.x + rr0.w : c0[i + 1].x));
    const colW = colStart.map((s, i) => colEnd[i] - s);
    const pills = [];
    const outRows = rows.map(r => {
      const rs = getComputedStyle(r), rr = R(r);
      const fill = hex(rs.backgroundColor);
      const bt = px(rs.borderTopWidth) > 0 && rs.borderTopStyle !== 'none' ? { w: px(rs.borderTopWidth), c: hex(rs.borderTopColor) } : null;
      const bb = px(rs.borderBottomWidth) > 0 && rs.borderBottomStyle !== 'none' ? { w: px(rs.borderBottomWidth), c: hex(rs.borderBottomColor) } : null;
      const valign = rs.alignItems === 'center' ? 'middle' : 'top';
      const cells = [...r.children].map((c, i) => {
        const cr = R(c);
        const paras = [];
        const leaves = isText(c) ? [c] : [...c.querySelectorAll('p,h1,h2,h3,h4')];
        for (const l of leaves) {
          if (isPill(l)) { pills.push(textItem(l)); continue; }
          paras.push(para(l));
        }
        const cf = !isText(c) ? hex(getComputedStyle(c).backgroundColor) : null;
        return {
          paras, fill: cf || fill,
          mar: [px(rs.paddingTop), Math.max(0, colEnd[i] - (cr.x + cr.w)), px(rs.paddingBottom), Math.max(0, cr.x - colStart[i])],
          valign,
        };
      });
      return { h: rr.h, cells, bt, bb };
    });
    return { t: 'table', x: rr0.x, y: T.y, w: rr0.w, colW, rows: outRows, pills };
  }

  // ---- per-slide chart preparation ----
  function barRowsAfter(captionText) {
    const cap = [...section.querySelectorAll('p')].find(p => p.textContent.trim() === captionText);
    const rows = [];
    let n = cap.nextElementSibling;
    while (n) {
      if (n.tagName === 'DIV' && n.children.length === 3 && isText(n.children[0]) && !isText(n.children[1]) && hex(getComputedStyle(n.children[1]).backgroundColor)) rows.push(n);
      n = n.nextElementSibling;
    }
    return rows;
  }
  function barChart(caption, name) {
    const rows = barRowsAfter(caption);
    const rr = rows.map(R);
    const labelR = R(rows[0].children[0]);
    const bars = rows.map(r => r.children[1]);
    const br = bars.map(R);
    const values = rows.map(r => parseFloat(r.children[2].textContent));
    const pxPerUnit = br[0].w / values[0];
    const x = rr[0].x, w = Math.max(...rr.map(r => r.w)) + 40;
    const pitch = (rr[rr.length - 1].y - rr[0].y) / (rr.length - 1);
    const y0 = rr[0].y + rr[0].h / 2 - pitch / 2;
    const h = pitch * rows.length;
    const plotX = br[0].x - x;
    const max = Math.floor((w - plotX - 44) / pxPerUnit / 5) * 5;
    rows.forEach(r => skip.add(r));
    const lab = rows[0].children[0], ls = getComputedStyle(lab);
    const val = rows[0].children[2], vs = getComputedStyle(val);
    charts.push({
      _anchorEl: rows[0].parentElement, t: 'chart', kind: 'hbar', name, x, y: y0, w, h, plotX, plotW: max * pxPerUnit, max,
      labels: rows.map(r => r.children[0].textContent.trim()), values,
      colors: bars.map(b => hex(getComputedStyle(b).backgroundColor)),
      gap: Math.round((pitch - br[0].h) / br[0].h * 100),
      labelColor: hex(ls.color), labelSize: px(ls.fontSize), valColor: hex(vs.color), valSize: px(vs.fontSize),
    });
  }
  if (slideId === 'readiness') {
    barChart('By domain, % of target', 'Readiness by domain');
    barChart('By family, % of target', 'Readiness by family');
  }
  if (slideId === 'market-access') {
    // The stacked route bar: four absolutely positioned segment divs (height 56px).
    const box = [...section.querySelectorAll('div')].find(d => d.style.position === 'relative' && d.style.height === '152px');
    const segs = [...box.children].filter(d => d.tagName === 'DIV' && d.style.height === '56px');
    const segR = segs.map(R);
    const labels = [...box.children].filter(p => p.tagName === 'P' && Math.abs(R(p).y - (segR[0].y + 12)) < 2);
    const names = ['Module H', 'B+C', 'Module A', 'Class I if H3 and EG-700 (SD2)'];
    const values = labels.map(p => parseFloat(p.textContent.replace(/.*EUR\s*/, '')));
    segs.forEach(s => skip.add(s));
    const x = segR[0].x, y = segR[0].y, w = segR[3].x + segR[3].w - x, h = segR[0].h;
    charts.push({ _anchorEl: box, t: 'chart', kind: 'stack', name: 'EU revenue by conformity route', x, y, w, h, names, values, colors: segs.map(s => hex(getComputedStyle(s).backgroundColor)) });
  }
  if (slideId === 'budget') {
    const svg = section.querySelector('svg');
    const sr = R(svg);
    skip.add(svg);
    const box = svg.parentElement;
    // y-axis and x-axis tick labels are drawn by the chart itself
    // (month labels stay as text boxes: only every third month is labelled, which LibreOffice
    // cannot reproduce from a chart's label interval)
    [...box.querySelectorAll('p')].forEach(p => { if (/^\d+$/.test(p.textContent.trim())) skip.add(p); });
    // plan values from the polyline (svg y 424 = 0, 24 = 10; 40 px per EUR 1m)
    const pts = svg.querySelector('polyline').getAttribute('points').trim().split(/\s+/).map(s => s.split(',').map(Number));
    const plan = pts.map(([, yy]) => Math.round((424 - yy) / 40 * 100) / 100);
    const months = []; const mn = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    for (let i = 0; i < pts.length; i++) { const m = (9 + i) % 12, yv = 2026 + Math.floor((9 + i) / 12); months.push(mn[m] + ' ' + yv); }
    // labelled values from the copy: plan 0.38 in Oct 2026 and 9.25 in Dec 2027; actual 0.41
    plan[0] = 0.38; plan[plan.length - 1] = 9.25;
    const actual = plan.map(() => null); actual[0] = 0.41;
    // annotation shapes from the SVG (not gridlines/axis, not the polyline)
    const ann = [];
    svg.querySelectorAll('line').forEach(l => {
      const g = n => Number(l.getAttribute(n));
      const st = l.getAttribute('stroke');
      if (g('y1') === g('y2') && g('x1') === 64 && st !== '#56667E') return; // gridline (drawn by the chart)
      ann.push({ t: 'line', x1: sr.x + g('x1'), y1: sr.y + g('y1'), x2: sr.x + g('x2'), y2: sr.y + g('y2'), w: Number(l.getAttribute('stroke-width')), c: st.replace('#', '').toUpperCase(), dash: l.getAttribute('stroke-dasharray') ? 'sysDash' : 'solid' });
    });
    charts.push({
      _anchorEl: box, t: 'chart', kind: 'line', name: 'Cumulative spend, EUR m', x: sr.x, y: sr.y, w: sr.w, h: sr.h,
      // plot area (inner): categories every 64 px from x=88; value 0..10 from y=424..24
      plot: { x: 56, y: 24, w: 960, h: 400 }, months, plan, actual, ann,
      circles: [...svg.querySelectorAll('circle')].map(c => ({ cx: sr.x + Number(c.getAttribute('cx')), cy: sr.y + Number(c.getAttribute('cy')), r: Number(c.getAttribute('r')), fill: c.getAttribute('fill').replace('#', '').toUpperCase(), stroke: (c.getAttribute('stroke') || '').replace('#', '').toUpperCase(), sw: Number(c.getAttribute('stroke-width') || 0) })),
    });
  }

  // ---- generic walk ----
  const anchors = new Map();
  for (const ch of charts) { const a = ch._anchorEl; delete ch._anchorEl; if (!anchors.has(a)) anchors.set(a, []); anchors.get(a).push(ch); }
  function walk(el) {
    if (skip.has(el)) return;
    const st = getComputedStyle(el);
    if (st.display === 'none' || st.visibility === 'hidden') return;
    if (el.tagName === 'svg') return;
    const r = R(el);
    if (isText(el)) {
      const ti = textItem(el);
      const b = borderItems(el, r, st);
      if (b.outline) ti.outline = b.outline;
      items.push(ti);
      if (b.lines) items.push(...b.lines);
      return;
    }
    const tb = tableOf(el);
    if (tb) { items.push(tb); items.push(...tb.pills); delete tb.pills; return; }
    if (el !== section) {
      const fill = hex(st.backgroundColor);
      const b = borderItems(el, r, st);
      if ((fill || b.outline) && r.w > 0.1 && (r.h > 0.1 || b.outline)) {
        const rad = [st.borderTopLeftRadius, st.borderTopRightRadius, st.borderBottomRightRadius, st.borderBottomLeftRadius].map(px);
        items.push({ t: 'rect', ...r, fill, radius: Math.max(...rad), radii: rad, outline: b.outline || null });
      }
      if (b.lines) items.push(...b.lines);
    }
    // charts are emitted at the container that holds them, under any overlaid labels
    if (anchors.has(el)) for (const ch of anchors.get(el)) { ch._done = true; items.push(ch); }
    for (const c of el.children) walk(c);
  }
  walk(section);
  for (const ch of charts) if (!ch._done) items.push(ch);
  const aside = section.querySelector('aside');
  return { bg: hex(getComputedStyle(section).backgroundColor), items, notes: aside ? aside.textContent.replace(/\s+/g, ' ').trim() : '' };
}

// ---------------------------------------------------------------------------------------------
// Node side: emit PptxGenJS objects.
// ---------------------------------------------------------------------------------------------
const FONT_MAP = { 'Source Serif 4': 'Source Serif 4', Inter: 'Inter', 'JetBrains Mono': 'JetBrains Mono' };
const fontName = f => FONT_MAP[f] || 'Inter';
const inch = v => Math.round(v * PX * 10000) / 10000;

function runObjs(paras, extra = {}) {
  const out = [];
  paras.forEach((p, pi) => {
    const rs = p.runs.length ? p.runs : [{ text: '', font: 'Inter', size: 24, color: '26364D', bold: false, italic: false, ls: 0 }];
    rs.forEach((r, ri) => {
      if (r.br) { // soft line break inside a paragraph
        out.push({ text: '', options: { softBreakBefore: true } });
        return;
      }
      const o = {
        fontFace: fontName(r.font), fontSize: r.size * PT, bold: r.bold, italic: r.italic, color: r.color || '26364D',
        align: p.align === 'justify' ? 'left' : p.align,
        lineSpacing: Math.round(p.lh * PT * 100) / 100,
        paraSpaceBefore: 0, paraSpaceAfter: 0,
        ...extra,
      };
      const sp = (r.ls || 0) + (r.adj || 0);
      if (Math.abs(sp) >= 0.02) o.charSpacing = Math.round(sp * PT * 100) / 100;
      if (ri === rs.length - 1 && pi < paras.length - 1) o.breakLine = true;
      out.push({ text: r.text, options: o });
    });
  });
  return out;
}

let objCount = 0;
const oname = k => `${k} ${++objCount}`;

function emitText(pres, slide, it) {
  const isPill = !!it.fill;
  let x = it.x, w = it.w;
  // Slack for font substitution and Inter Bold vs SemiBold: widen single-line labels.
  const single = it.lines <= 1;
  if (!isPill && single && it.textW > 0) {
    const need = it.textW * 1.10 + it.pad[1] + it.pad[3];
    if (need > w) {
      const add = need - w;
      if (it.align === 'right') x -= add; else if (it.align === 'center') x -= add / 2;
      w += add;
    }
  }
  // multi-line serif titles: 2% extra measure (the static serif is only partly compensated)
  if (!isPill && !single && it.align === 'left' && /^H[1-3]$/.test(it.tag)) w *= 1.02;
  if (isPill) { const add = Math.max(0, it.textW * 0.06); x -= add / 2; w += add; }
  let y = it.y, h = it.h;
  if (!isPill && single) { y = it.y + it.pad[0] + (it.bT || 0); h = it.lh + it.pad[0] + it.pad[2]; y -= it.pad[0]; }
  const opts = {
    x: inch(x), y: inch(y), w: inch(w), h: inch(h),
    margin: [it.pad[3] * PT, it.pad[1] * PT, it.pad[2] * PT, it.pad[0] * PT],
    valign: isPill || single ? 'middle' : 'top',
    isTextBox: true, fit: 'none', wrap: !(single || isPill),
    objectName: oname(isPill ? 'Pill' : it.tag === 'H1' || it.tag === 'H2' ? 'Title' : 'Text'),
  };
  if (isPill) {
    opts.shape = it.radius > 0 ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE;
    opts.fill = { color: it.fill };
    if (it.radius > 0) opts.rectRadius = inch(Math.min(it.radius, it.h / 2, w / 2));
    delete opts.isTextBox;
  }
  if (it.outline) opts.line = { color: it.outline.c, width: it.outline.w * PT };
  // single-line text: centre the glyphs in the CSS line box, as the browser does
  const paras = [{ runs: it.runs, align: it.align, lh: it.lh }];
  const runs = runObjs(paras, single || isPill ? { lineSpacing: undefined } : {});
  runs.forEach(r => { if (r.options && r.options.lineSpacing === undefined) delete r.options.lineSpacing; });
  slide.addText(runs, opts);
}

function emitRect(pres, slide, it) {
  const r = it.radius;
  const o = { x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(Math.max(it.h, 0.5)), objectName: oname('Shape') };
  o.fill = it.fill ? { color: it.fill } : { type: 'none' };
  if (it.outline) o.line = { color: it.outline.c, width: it.outline.w * PT, dashType: it.outline.dash === 'dashed' ? 'dash' : 'solid' };
  else o.line = { type: 'none' };
  let shape = pres.shapes.RECTANGLE;
  if (r > 0.5) {
    const uniform = it.radii.every(v => Math.abs(v - r) < 0.5);
    if (uniform || r >= Math.min(it.w, it.h) / 2) { shape = pres.shapes.ROUNDED_RECTANGLE; o.rectRadius = inch(Math.min(r, it.w / 2, it.h / 2)); }
  }
  slide.addShape(shape, o);
}

function emitLine(pres, slide, it) {
  const x = Math.min(it.x1, it.x2), y = Math.min(it.y1, it.y2);
  const w = Math.abs(it.x2 - it.x1), h = Math.abs(it.y2 - it.y1);
  const o = { x: inch(x), y: inch(y), w: inch(w), h: inch(h), line: { color: it.c, width: it.w * PT, dashType: it.dash === 'sysDash' ? 'sysDash' : it.dash }, objectName: oname('Line') };
  // direction: pptx lines go top-left -> bottom-right unless flipped
  if ((it.x2 - it.x1) * (it.y2 - it.y1) < 0) o.flipV = true;
  slide.addShape(pres.shapes.LINE, o);
}

function emitTable(pres, slide, it) {
  const rows = it.rows.map((row, ri) => row.cells.map(c => {
    const border = [
      row.bt ? { type: 'solid', pt: row.bt.w * PT, color: row.bt.c } : (ri > 0 && it.rows[ri - 1].bb ? { type: 'solid', pt: it.rows[ri - 1].bb.w * PT, color: it.rows[ri - 1].bb.c } : { type: 'none' }),
      { type: 'none' },
      row.bb ? { type: 'solid', pt: row.bb.w * PT, color: row.bb.c } : (ri < it.rows.length - 1 && it.rows[ri + 1].bt ? { type: 'solid', pt: it.rows[ri + 1].bt.w * PT, color: it.rows[ri + 1].bt.c } : { type: 'none' }),
      { type: 'none' },
    ];
    const opts = {
      margin: c.mar.map(v => Math.round(v * PX * 10000) / 10000), valign: c.valign, border,
    };
    if (c.fill) opts.fill = { color: c.fill };
    const text = c.paras.length ? runObjs(c.paras) : [{ text: '', options: { fontFace: 'Inter', fontSize: 12 } }];
    return { text, options: opts };
  }));
  slide.addTable(rows, {
    x: inch(it.x), y: inch(it.y), w: inch(it.w), colW: it.colW.map(inch), rowH: it.rows.map(r => inch(r.h)),
    autoPage: false, objectName: oname('Table'),
  });
}

function emitChart(pres, slide, it) {
  const AX = { fontFace: 'Inter' };
  if (it.kind === 'hbar') {
    const fw = it.w, fh = it.h;
    slide.addChart(pres.charts.BAR, [{ name: it.name, labels: it.labels, values: it.values }], {
      x: inch(it.x), y: inch(it.y), w: inch(fw), h: inch(fh), objectName: oname('Chart ' + it.name),
      barDir: 'bar', barGapWidthPct: it.gap, chartColors: it.colors,
      layout: { x: it.plotX / fw, y: 0, w: it.plotW / fw, h: 1 },
      catAxisOrientation: 'maxMin', catAxisLabelColor: it.labelColor, catAxisLabelFontSize: it.labelSize * PT, catAxisLabelFontFace: AX.fontFace,
      catAxisLineShow: false, catAxisMajorTickMark: 'none',
      valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: it.max, valGridLine: { style: 'none' }, catGridLine: { style: 'none' },
      showValue: true, dataLabelPosition: 'outEnd', dataLabelColor: it.valColor, dataLabelFontSize: it.valSize * PT, dataLabelFontBold: true, dataLabelFontFace: AX.fontFace,
      showLegend: false, showTitle: false, plotArea: { fill: { color: 'FAFAF7', transparency: 100 } },
    });
  } else if (it.kind === 'stack') {
    slide.addChart(pres.charts.BAR, it.names.map((n, i) => ({ name: n, labels: ['EU revenue'], values: [it.values[i]] })), {
      x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h), objectName: oname('Chart ' + it.name),
      barDir: 'bar', barGrouping: 'stacked', barGapWidthPct: 0, chartColors: it.colors,
      dataBorder: { pt: 1, color: 'FAFAF7' },
      layout: { x: 0, y: 0, w: 1, h: 1 },
      catAxisHidden: true, valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: it.values.reduce((a, b) => a + b, 0),
      valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showValue: false, showLegend: false, showTitle: false,
    });
  } else if (it.kind === 'line') {
    const p = it.plot;
    slide.addChart(pres.charts.LINE, [
      { name: 'Plan (cumulative, incl. contingency)', labels: it.months, values: it.plan },
      { name: 'Actual', labels: it.months, values: it.actual },
    ], {
      x: inch(it.x), y: inch(it.y), w: inch(it.w), h: inch(it.h), objectName: oname('Chart ' + it.name),
      layout: { x: p.x / it.w, y: p.y / it.h, w: p.w / it.h * it.h / it.w, h: p.h / it.h },
      chartColors: ['1F3A5F', '0F6E6A'], lineSize: 1.5, lineDataSymbol: 'none', lineDataSymbolSize: 7,
      valAxisMinVal: 0, valAxisMaxVal: 10, valAxisMajorUnit: 2, valAxisLabelColor: '56667E', valAxisLabelFontSize: 12, valAxisLabelFontFace: 'Inter',
      valAxisLineShow: false, valGridLine: { color: 'C5CDD8', size: 0.5 }, catGridLine: { style: 'none' },
      catAxisHidden: true,
      showLegend: false, showTitle: false, showValue: false,
    });
    for (const a of it.ann) emitLine(pres, slide, a);
    for (const c of it.circles) {
      const o = { x: inch(c.cx - c.r), y: inch(c.cy - c.r), w: inch(2 * c.r), h: inch(2 * c.r), fill: { color: c.fill }, objectName: oname('Marker') };
      o.line = c.stroke ? { color: c.stroke, width: c.sw * PT } : { type: 'none' };
      slide.addShape(pres.shapes.OVAL, o);
    }
  }
}

// pptxgenjs writes <c:tickLblSkip> after <c:noMultiLvlLbl>, which breaks the CT_CatAx sequence
// (PowerPoint and LibreOffice then ignore the label interval). Move it into schema order.
function fixChartXml(file) {
  const py = `
import sys, zipfile, re, shutil, os
src = sys.argv[1]; tmp = src + '.tmp'
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for item in zi.infolist():
        data = zi.read(item.filename)
        if item.filename.startswith('ppt/charts/chart') and item.filename.endswith('.xml'):
            x = data.decode('utf-8')
            x = re.sub(r'(<c:noMultiLvlLbl val="[01]"/>)\\s*(<c:tickLblSkip val="\\d+"/>)', r'\\2\\1', x)
            data = x.encode('utf-8')
        zo.writestr(item, data)
shutil.move(tmp, src)
`;
  require('child_process').execFileSync('python3', ['-c', py, file], { stdio: 'inherit' });
}

async function main() {
  const deck = JSON.parse(fs.readFileSync(path.join(SRC, 'deck.json'), 'utf8'));
  const ids = deck.order;
  ids.forEach(id => { if (!/^[A-Za-z0-9_-]{1,64}$/.test(id)) throw new Error('bad id ' + id); });
  const slidesHtml = ids.map(id => fs.readFileSync(path.join(SRC, 'slides', id + '.html'), 'utf8'));
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>${fontCss()}${SLIDE_CSS}</style></head><body>${slidesHtml.map((h, i) => `<div class="page" data-i="${i}">${h}</div>`).join('\n')}</body></html>`;
  const tmp = path.join(require('os').tmpdir(), 'd02_build_doc.html');
  fs.writeFileSync(tmp, html);

  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await ctx.route(/^https?:/, r => r.abort());
  const page = await ctx.newPage();
  await page.goto('file://' + tmp, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(async faces => {
    for (const [fam, w, file] of faces) {
      const ff = new FontFace(fam, `url(file://${file})`, { weight: w });
      document.fonts.add(await ff.load());
    }
  }, STATIC_FACES.filter(f => fs.existsSync(f[2])));
  await page.waitForTimeout(300);
  const data = [];
  for (let i = 0; i < ids.length; i++) data.push(await page.evaluate(browserExtract, { idx: i, slideId: ids[i] }));
  await browser.close();
  if (process.env.D02_DUMP) fs.writeFileSync(process.env.D02_DUMP, JSON.stringify(data, null, 1));

  const pres = new PptxGenJS();
  pres.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5 in
  pres.title = deck.title;
  pres.subject = 'Project Rampart steering committee pack (illustrative)';
  pres.author = 'Advisory';
  pres.theme = { headFontFace: 'Source Serif 4', bodyFontFace: 'Inter' };
  const sectionStarts = {};
  Object.values(deck.sections || {}).forEach(s => { sectionStarts[s.start] = s.description; });
  const sectionTitles = { cover: 'Status', kpis: 'Performance', milestones: 'Delivery', risks: 'Risks and decisions', 'a1-workstreams': 'Appendix' };
  let curSection = null;
  ids.forEach((id, i) => {
    if (sectionStarts[id]) { curSection = sectionTitles[id] || id; pres.addSection({ title: curSection }); }
    const d = data[i];
    const slide = pres.addSlide(curSection ? { sectionTitle: curSection } : {});
    slide.background = { color: d.bg || 'FAFAF7' };
    for (const it of d.items) {
      if (it.t === 'text') emitText(pres, slide, it);
      else if (it.t === 'rect') emitRect(pres, slide, it);
      else if (it.t === 'line') emitLine(pres, slide, it);
      else if (it.t === 'table') emitTable(pres, slide, it);
      else if (it.t === 'chart') emitChart(pres, slide, it);
    }
    const notes = d.notes || decode((slidesHtml[i].match(/<aside>([\s\S]*?)<\/aside>/) || [, ''])[1]);
    slide.addNotes(notes);
  });
  await pres.writeFile({ fileName: OUT_FILE });
  fixChartXml(OUT_FILE);
  console.log('wrote', OUT_FILE, ids.length, 'slides');
}

main().catch(e => { console.error(e); process.exit(1); });
