#!/usr/bin/env node
// D01 Board briefing deck -> native, editable PowerPoint.
//
// Method: each slide's HTML (source/project/slides/*.html) is rendered in headless Chromium with the
// same harness CSS that produced the reference PDF, at 1920x1080. The rendered DOM is walked and every
// element becomes a native PowerPoint object at its measured position: text blocks become text boxes
// (runs keep font, size, weight, colour, letter-spacing), backgrounds and borders become rectangles and
// lines, rotated squares become diamonds, CSS grids that are tables become native tables, and the four
// data charts become native PowerPoint bar charts with their data. Speaker notes come from each slide's
// <aside>. 1920 px = 13.333 in, so 1 px = 1/144 in and 1 px of type = 0.5 pt.
//
// Usage: node pack/engine/pptx/d01_build.js [out.pptx]
// Env:   D01_FONT_DIR  folder holding local.css + woff2 files for Inter, Source Serif 4, JetBrains Mono
//        (the same fonts the PDF was rendered with; without them Chromium measures with fallbacks).
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const pptxgen = require('pptxgenjs');
const JSZip = require(require.resolve('jszip', { paths: [path.dirname(fs.realpathSync(require.resolve('pptxgenjs')))] }));

const REPO = path.resolve(__dirname, '..', '..', '..');
const DECK_DIR = path.join(REPO, 'pack', 'out', 'hosted', 'D01-board-deck');
const SRC = path.join(DECK_DIR, 'source', 'project');
const OUT = process.argv[2] || path.join(DECK_DIR, 'D01 - Board briefing deck.pptx');
const FONT_DIR = process.env.D01_FONT_DIR || path.join(__dirname, 'fonts');

const PX = 1 / 144;            // inches per CSS px
const PT = 0.5;                // points per CSS px
const inch = v => +(v * PX).toFixed(4);

// Same harness as the PDF renderer (hosted-render/render.js).
const SLIDE_CSS = `
html,body{margin:0;padding:0;background:#fff}
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
x-shape{display:block;flex:none}
x-shape[kind="arrow-right"]{clip-path:polygon(0 30%,60% 30%,60% 0,100% 50%,60% 100%,60% 70%,0 70%)}
x-shape[kind="arrow-left"]{clip-path:polygon(100% 30%,40% 30%,40% 0,0 50%,40% 100%,40% 70%,100% 70%)}
x-shape[kind="arrow-down"]{clip-path:polygon(30% 0,70% 0,70% 60%,100% 60%,50% 100%,0 60%,30% 60%)}
x-shape[kind="arrow-up"]{clip-path:polygon(30% 100%,70% 100%,70% 40%,100% 40%,50% 0,0 40%,30% 40%)}
x-shape[kind="ellipse"]{border-radius:50%}
x-shape[kind="diamond"]{clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%)}
`;

// ---- Per-slide configuration: native tables and charts --------------------------------------------
const GRID = 'div[style*="display:grid"]';
const SLIDE_CFG = {
  decisions: { tables: [GRID] },
  portfolio: { tables: [GRID] },
  baseline: { tables: [GRID] },
  legacy: { tables: [GRID] },
  appA: { tables: [GRID] },
  appB: { tables: [GRID] },
  constraint: {
    chart: {
      kind: 'col', plot: 'div[style*="height:344px"]', items: 'div[style*="height:344px"] > div',
      bar: ':scope > div', value: ':scope > p', dropValues: true,
      name: 'EU revenue, EUR m', labels: ['Default', 'Class I', 'Class II'], values: [338.3, 395.7, 72.6],
      colors: ['8A94A6', 'C2410C', 'C2410C'], labelColors: ['0E1A2B', 'C2410C', 'C2410C'], fmt: '0.0', labelPx: 28,
    },
  },
  stakes: {
    chart: {
      kind: 'hbar', items: 'section > div > div:first-child > div[style*="align-items:center"]',
      bar: ':scope > div[style*="background"]', value: ':scope > p:last-child', dropValues: true,
      name: 'EUR m', labels: ['EU revenue needing a notified body, per year', 'Maximum fine, tier 1', 'Maximum fine, tier 2', 'Maximum fine, tier 3'],
      values: [468, 30, 24, 12], colors: ['C2410C', '8A94A6', '8A94A6', '8A94A6'],
      labelColors: ['C2410C', '0E1A2B', '0E1A2B', '0E1A2B'], fmt: '"  "0', labelPx: 24, rightPad: 120,
    },
  },
  market: {
    chart: {
      kind: 'hbar', items: 'section > div > div:first-child > div[style*="align-items:center"]',
      bar: ':scope > div[style*="background"]', value: ':scope > p:last-child', dropValues: true,
      name: '% of respondents',
      labels: ['German companies that know what the CRA means for them (Bitkom)', 'CRA-aware respondents unaware of the penalties (Linux Foundation)',
        'German industrial firms expecting longer development (ONEKEY)', 'Respondents citing SBOM completeness as a challenge (ENISA)'],
      values: [29, 56, 60, 62], colors: ['0F6E6A', '8A94A6', '8A94A6', '8A94A6'],
      labelColors: ['0F6E6A', '0E1A2B', '0E1A2B', '0E1A2B'], fmt: '"  "0"%"', fmts: { 2: '"  >"0"%"' }, labelPx: 24, rightPad: 120,
    },
  },
  investment: {
    chart: {
      kind: 'waterfall', items: 'section > div > div:first-child > div[style*="align-items:center"]',
      bar: ':scope > div > div', value: ':scope > div > p', dropValues: false,
      name: 'One-off cost, EUR k',
      labels: ['Secure engineering', 'Shared platforms', 'Programme & governance', 'Conformity & market access', 'Documentation & evidence',
        'Reporting & PSIRT', 'People & change', 'Supply chain', 'Contingency, 15%', 'Total, incl. contingency'],
      values: [4389, 955, 938, 613, 520, 400, 140, 90, 1207, 9251], color: '8A94A6', totalColor: '0F6E6A', dashedIdx: 8, totalIdx: 9,
    },
  },
};

// ---- In-page extraction ----------------------------------------------------------------------------
function pageExtract(cfg) {
  const sec = document.querySelector('section');
  const O = sec.getBoundingClientRect();
  const R = el => { const r = el.getBoundingClientRect(); return { x: r.left - O.left, y: r.top - O.top, w: r.width, h: r.height }; };
  const hex = c => {
    const m = (c || '').match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(s => parseFloat(s));
    if (p.length === 4 && p[3] === 0) return null;
    return p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
  };
  const INLINE = new Set(['B', 'STRONG', 'SPAN', 'I', 'EM', 'BR', 'A', 'SUB', 'SUP', 'CODE']);
  const isTextBlock = el => {
    if (INLINE.has(el.tagName)) return false;
    let hasText = false;
    for (const n of el.childNodes) {
      if (n.nodeType === 3) { if (n.textContent.trim()) hasText = true; }
      else if (n.nodeType === 1) { if (!INLINE.has(n.tagName)) return false; if (n.textContent.trim() || n.tagName === 'BR') hasText = true; }
    }
    return hasText;
  };
  const sides = ['Top', 'Right', 'Bottom', 'Left'];
  const boxInfo = (el, cs) => {
    const b = {};
    for (const s of sides) {
      const w = parseFloat(cs['border' + s + 'Width']) || 0, st = cs['border' + s + 'Style'];
      b[s] = (w > 0 && st !== 'none' && st !== 'hidden') ? { w, style: st, color: hex(cs['border' + s + 'Color']) } : null;
    }
    const uni = sides.every(s => b[s] && b.Top && b[s].w === b.Top.w && b[s].style === b.Top.style && b[s].color === b.Top.color);
    return { fill: hex(cs.backgroundColor), b, uniform: uni ? b.Top : null, radius: parseFloat(cs.borderTopLeftRadius) || 0,
      pad: sides.map(s => parseFloat(cs['padding' + s]) || 0) };
  };
  const font = cs => cs.fontFamily.split(',')[0].trim().replace(/^['"]|['"]$/g, '');
  const lineH = cs => cs.lineHeight === 'normal' ? parseFloat(cs.fontSize) * 1.2 : parseFloat(cs.lineHeight);
  const para = el => {
    const cs = getComputedStyle(el);
    const runs = [];
    let br = false;
    const visit = (node, ecs) => {
      for (const n of node.childNodes) {
        if (n.nodeType === 3) {
          let t = n.textContent.replace(/\s+/g, ' ');
          if (ecs.textTransform === 'uppercase') t = t.toUpperCase();
          if (!t) continue;
          const ls = ecs.letterSpacing === 'normal' ? 0 : parseFloat(ecs.letterSpacing) || 0;
          runs.push({ text: t, font: font(ecs), px: parseFloat(ecs.fontSize), bold: (parseInt(ecs.fontWeight, 10) || 400) >= 600,
            italic: ecs.fontStyle === 'italic', color: hex(ecs.color), ls, br });
          br = false;
        } else if (n.nodeType === 1) {
          if (n.tagName === 'BR') { br = true; continue; }
          visit(n, getComputedStyle(n));
        }
      }
    };
    visit(el, cs);
    // trim whitespace at line starts / ends
    for (let i = 0; i < runs.length; i++) {
      if (i === 0 || runs[i].br) runs[i].text = runs[i].text.replace(/^ /, '');
      if (i === runs.length - 1 || runs[i + 1].br) runs[i].text = runs[i].text.replace(/ $/, '');
    }
    // Source Serif 4 renders here with automatic optical sizing (opsz = px size, display cut); PowerPoint uses the
    // default text cut, which sets wider. Compensate with letter-spacing so line lengths match.
    if (/Source Serif/.test(cs.fontFamily) && cs.fontOpticalSizing !== 'none') {
      const probe = el.cloneNode(true);
      probe.style.cssText += ';position:absolute;left:0;top:0;width:auto;max-width:none;white-space:nowrap;visibility:hidden;padding:0;border:0';
      probe.querySelectorAll('br').forEach(b => b.replaceWith(document.createTextNode(' ')));
      sec.appendChild(probe);
      const w1 = probe.getBoundingClientRect().width;
      // what PowerPoint draws: the default optical size, at the regular or bold static weight
      probe.style.fontOpticalSizing = 'none';
      probe.style.fontWeight = (parseInt(cs.fontWeight, 10) || 400) >= 600 ? '700' : '400';
      probe.querySelectorAll('*').forEach(e => { e.style.fontOpticalSizing = 'none'; e.style.fontWeight = (parseInt(getComputedStyle(e).fontWeight, 10) || 400) >= 600 ? '700' : '400'; });
      const w0 = probe.getBoundingClientRect().width;
      probe.remove();
      const n = runs.reduce((k, r) => k + r.text.length, 0);
      if (n && w0 > w1) runs.forEach(r => { if (/Source Serif/.test(r.font)) r.ls += (w1 - w0) / n; });
    }
    const ta = cs.textAlign;
    const align = ta === 'center' ? 'center' : (ta === 'right' || ta === 'end') ? 'right' : ta === 'justify' ? 'justify' : 'left';
    return { align, lh: lineH(cs), px: parseFloat(cs.fontSize), runs: runs.filter(r => r.text || r.br) };
  };
  const contentRect = (r, bi) => {
    const bw = s => (bi.b[s] ? bi.b[s].w : 0);
    return { x: r.x + bi.pad[3] + bw('Left'), y: r.y + bi.pad[0] + bw('Top'),
      w: r.w - bi.pad[1] - bi.pad[3] - bw('Left') - bw('Right'), h: r.h - bi.pad[0] - bi.pad[2] - bw('Top') - bw('Bottom') };
  };
  const lines = (el) => {
    // number of rendered lines of a text block
    const range = document.createRange(); range.selectNodeContents(el);
    const tops = new Set([...range.getClientRects()].map(q => Math.round(q.top)));
    return Math.max(1, tops.size);
  };
  const wrapSlack = (el, box) => {
    // how much wider the box can be without changing where the browser wrapped any line
    const toks = [];
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    let prevEndsSpace = true;
    for (let n = tw.nextNode(); n; n = tw.nextNode()) {
      const t = n.textContent; const re = /[^\s-]+-?|-/g; let m;
      while ((m = re.exec(t))) {
        const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
        const q = rg.getClientRects()[0]; if (!q) continue;
        const sp = m.index === 0 ? prevEndsSpace : /\s/.test(t[m.index - 1]);
        toks.push({ l: q.left - O.left, r: q.right - O.left, top: Math.round(q.top), sp, px: parseFloat(getComputedStyle(n.parentElement).fontSize) });
      }
      if (t.length) prevEndsSpace = /\s$/.test(t);
    }
    let allowed = Infinity;
    for (let i = 0; i + 1 < toks.length; i++) {
      if (Math.abs(toks[i + 1].top - toks[i].top) < 4) continue;
      const need = toks[i].r + (toks[i + 1].sp ? 0.28 * toks[i + 1].px : 0) + (toks[i + 1].r - toks[i + 1].l) - (box.x + box.w);
      allowed = Math.min(allowed, need);
    }
    return allowed;
  };

  const items = [];
  const skip = new Set();
  const tag = new Map(); // element -> row index for chart rows
  let chart = null;
  if (cfg.chart) {
    const c = cfg.chart;
    const rows = [...sec.querySelectorAll(c.items)];
    chart = { kind: c.kind, rows: [] };
    if (c.plot) chart.plot = R(sec.querySelector(c.plot));
    rows.forEach((row, i) => {
      const bar = row.querySelector(c.bar), val = row.querySelector(c.value);
      skip.add(bar); if (c.dropValues && val) skip.add(val);
      if (c.kind === 'col') skip.add(row);
      row.querySelectorAll('*').forEach(e => tag.set(e, i)); tag.set(row, i);
      chart.rows.push({ row: R(row), bar: R(bar), value: val ? R(val) : null });
    });
  }
  const tables = new Set();
  (cfg.tables || []).forEach(s => sec.querySelectorAll(s).forEach(e => tables.add(e)));

  const pushBox = (r, bi, rowTag) => {
    if (r.w <= 0 || r.h <= 0) return;
    if (bi.fill || bi.uniform) {
      items.push({ t: 'rect', ...r, fill: bi.fill, line: bi.uniform, radius: bi.radius, row: rowTag });
    }
    if (!bi.uniform) {
      for (const s of sides) {
        const b = bi.b[s]; if (!b) continue;
        const dashed = b.style === 'dashed' || b.style === 'dotted';
        let x = r.x, y = r.y, w = r.w, h = r.h;
        if (s === 'Top') h = b.w; if (s === 'Bottom') { y = r.y + r.h - b.w; h = b.w; }
        if (s === 'Left') w = b.w; if (s === 'Right') { x = r.x + r.w - b.w; w = b.w; }
        if (dashed) {
          const horiz = s === 'Top' || s === 'Bottom';
          items.push({ t: 'line', x1: horiz ? x : x + w / 2, y1: horiz ? y + h / 2 : y, x2: horiz ? x + w : x + w / 2, y2: horiz ? y + h / 2 : y + h,
            color: b.color, w: b.w, dash: b.style, row: rowTag });
        } else items.push({ t: 'rect', x, y, w, h, fill: b.color, row: rowTag });
      }
    }
  };

  const tableOf = (grid) => {
    const gcs = getComputedStyle(grid);
    const gr = R(grid);
    const cols = gcs.gridTemplateColumns.split(' ').map(parseFloat);
    const colGap = parseFloat(gcs.columnGap) || 0, rowGap = parseFloat(gcs.rowGap) || 0;
    const cells = [...grid.children].map(c => {
      const cs = getComputedStyle(c); const bi = boxInfo(c, cs); const r = R(c);
      let blocks;
      if (isTextBlock(c)) blocks = [{ rect: contentRect(r, bi), para: para(c) }];
      else blocks = [...c.querySelectorAll('*')].filter(e => isTextBlock(e) && !e.parentElement.closest('p,h1,h2,h3')).map(e => {
        const ebi = boxInfo(e, getComputedStyle(e));
        return { rect: contentRect(R(e), ebi), para: para(e) };
      });
      return { rect: r, fill: bi.fill, b: bi.b, pad: bi.pad, blocks };
    });
    return { t: 'table', ...gr, cols, colGap, rowGap, cells };
  };

  const walk = (el) => {
    if (skip.has(el)) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || el.tagName === 'ASIDE') return;
    if (tables.has(el)) { items.push(tableOf(el)); return; }
    const r = R(el);
    const rowTag = tag.has(el) ? tag.get(el) : undefined;
    const bi = boxInfo(el, cs);
    if (el.tagName === 'X-SHAPE') { items.push({ t: 'shape', kind: el.getAttribute('kind'), ...r, fill: bi.fill, row: rowTag }); return; }
    if (cs.transform && cs.transform !== 'none') {
      const m = cs.transform.match(/matrix\(([^)]+)\)/);
      const [a, b] = m ? m[1].split(',').map(parseFloat) : [1, 0];
      const ang = Math.round(Math.atan2(b, a) * 180 / Math.PI);
      if (Math.abs(ang) === 45 && Math.abs(el.offsetWidth - el.offsetHeight) < 1) {
        items.push({ t: 'shape', kind: 'diamond', ...r, fill: bi.fill, row: rowTag });
      } else {
        const cx = r.x + r.w / 2, cy = r.y + r.h / 2, w = el.offsetWidth, h = el.offsetHeight;
        items.push({ t: 'rect', x: cx - w / 2, y: cy - h / 2, w, h, fill: bi.fill, rot: ang, row: rowTag });
      }
      return;
    }
    if (isTextBlock(el)) {
      const p = para(el);
      const cr = contentRect(r, bi);
      const nl = lines(el);
      p.slack = nl > 1 ? wrapSlack(el, cr) : Infinity;
      if (bi.fill || bi.uniform) {
        items.push({ t: 'text', ...r, fill: bi.fill, line: bi.uniform, radius: bi.radius, inset: [cr.y - r.y, r.x + r.w - cr.x - cr.w, r.y + r.h - cr.y - cr.h, cr.x - r.x],
          paras: [p], lines: nl, valign: 'middle', row: rowTag });
      } else {
        pushBox(r, bi, rowTag);
        items.push({ t: 'text', ...cr, paras: [p], lines: nl, row: rowTag, tag: el.tagName });
      }
      return;
    }
    if (el !== sec) pushBox(r, bi, rowTag);
    for (const c of el.children) walk(c);
  };
  walk(sec);
  const aside = sec.querySelector('aside');
  return {
    bg: hex(getComputedStyle(sec).backgroundColor) || 'FFFFFF',
    notes: aside ? aside.textContent.replace(/\s+/g, ' ').trim() : '',
    items, chart,
  };
}

// ---- Builder -------------------------------------------------------------------------------------
const FONT_MAP = { 'Source Serif 4': 'Source Serif 4', Inter: 'Inter', 'JetBrains Mono': 'JetBrains Mono' };

function runsFor(p, extra = {}) {
  // pptxgenjs text runs for one paragraph; a <br> becomes a soft line break inside the paragraph
  const out = [];
  p.runs.forEach((r, i) => {
    const o = {
      fontFace: FONT_MAP[r.font] || r.font, fontSize: +(r.px * PT).toFixed(2), bold: r.bold, italic: r.italic, color: r.color || '000000',
      align: p.align, ...extra,
    };
    if (r.ls) o.charSpacing = +(r.ls * PT).toFixed(2);
    if (r.br && i > 0) o.softBreakBefore = true;
    out.push({ text: r.text, options: o });
  });
  return out;
}

function lineSpacingOpts(p, single) {
  // exact line spacing reproduces the HTML line boxes; very tall single lines are centred instead
  if (single && p.lh > p.px * 1.7) return { lineSpacingMultiple: 1.0, _center: true };
  return { lineSpacing: +(p.lh * PT).toFixed(2) };
}

function addTextItem(slide, it, dy = 0) {
  const p = it.paras[0];
  const single = it.lines <= 1;
  const ls = lineSpacingOpts(p, single);
  const center = ls._center; delete ls._center;
  const runs = runsFor(p, ls);
  if (!runs.length) return;
  let { x, y, w, h } = it; y += dy;
  const opts = { isTextBox: true, margin: 0, valign: it.valign || (center ? 'middle' : 'top'), fit: 'none' };
  if (it.tag === 'H1' || it.tag === 'H2') opts.objectName = 'Title';
  if (it.fill || it.line) {
    // text inside a filled / outlined box: one native shape carrying the text
    opts.shape = it.radius >= 6 ? 'roundRect' : 'rect';
    if (opts.shape === 'roundRect') opts.rectRadius = inch(Math.min(it.radius, Math.min(w, h) / 2));
    if (it.fill) opts.fill = { color: it.fill };
    if (it.line) opts.line = { color: it.line.color, width: it.line.w * PT, dashType: it.line.style === 'dashed' ? 'dash' : 'solid' };
    const [t, r, b, l] = it.inset;
    opts.margin = [l * PT, r * PT, b * PT, t * PT].map(v => +v.toFixed(2)); // pptxgenjs order: L, R, B, T (points)
    opts.wrap = !single;
    if (single) { opts.valign = 'middle'; }
    Object.assign(opts, { x: inch(x), y: inch(y), w: inch(w), h: inch(h) });
    slide.addText(runs, opts);
    return;
  }
  // free text: leave slack so substitute fonts do not wrap or clip
  let slack = Math.max(10, w * 0.06);
  if (!single) slack = Math.max(0, Math.min(slack, (p.slack || 0) - Math.max(4, w * 0.02)));
  if (single) {
    // short labels never wrap; wide lines (titles, notes) may wrap if a substitute font is wider
    opts.wrap = w >= 800;
    if (opts.wrap) h += p.lh * 0.5;
    if (p.align === 'left' || p.align === 'justify') w += slack;
    else if (p.align === 'right') { x -= slack; w += slack; }
    else { x -= slack / 2; w += slack; }
  } else {
    opts.wrap = true;
    if (p.align === 'left' || p.align === 'justify') w += slack;
    else if (p.align === 'right') { x -= slack; w += slack; }
    else { x -= slack / 2; w += slack; }
    h += p.lh * 0.5;
  }
  if (x + w > 1920 - 8) w = 1920 - 8 - x;
  Object.assign(opts, { x: inch(x), y: inch(y), w: inch(w), h: inch(Math.max(h, p.lh)) });
  slide.addText(runs, opts);
}

function addRect(slide, pres, it, dy = 0) {
  const o = { x: inch(it.x), y: inch(it.y + dy), w: inch(Math.max(it.w, 0.5)), h: inch(Math.max(it.h, 0.5)) };
  let shape = pres.shapes.RECTANGLE;
  if (it.radius >= 6) { shape = pres.shapes.ROUNDED_RECTANGLE; o.rectRadius = inch(Math.min(it.radius, Math.min(it.w, it.h) / 2)); }
  o.fill = it.fill ? { color: it.fill } : { type: 'none' };
  if (it.line) {
    // HTML borders sit inside the box; PowerPoint strokes straddle the edge, so inset by half the stroke
    const bw = it.line.w;
    o.x = inch(it.x + bw / 2); o.y = inch(it.y + dy + bw / 2); o.w = inch(it.w - bw); o.h = inch(it.h - bw);
    o.line = { color: it.line.color, width: bw * PT, dashType: it.line.style === 'dashed' ? 'dash' : it.line.style === 'dotted' ? 'sysDot' : 'solid' };
  } else o.line = { type: 'none' };
  if (it.rot) o.rotate = it.rot;
  slide.addShape(shape, o);
}

function addLine(slide, pres, it, dy = 0) {
  const x = Math.min(it.x1, it.x2), y = Math.min(it.y1, it.y2);
  slide.addShape(pres.shapes.LINE, {
    x: inch(x), y: inch(y + dy), w: inch(Math.abs(it.x2 - it.x1)), h: inch(Math.abs(it.y2 - it.y1)),
    line: { color: it.color, width: it.w * PT, dashType: it.dash === 'dotted' ? 'sysDot' : 'dash' },
  });
}

function addShapeItem(slide, pres, it, dy = 0) {
  const kinds = { diamond: pres.shapes.DIAMOND, 'arrow-right': pres.shapes.RIGHT_ARROW, 'arrow-left': pres.shapes.LEFT_ARROW,
    'arrow-down': pres.shapes.DOWN_ARROW, 'arrow-up': pres.shapes.UP_ARROW, ellipse: pres.shapes.OVAL };
  slide.addShape(kinds[it.kind] || pres.shapes.RECTANGLE, {
    x: inch(it.x), y: inch(it.y + dy), w: inch(it.w), h: inch(it.h), fill: { color: it.fill || '56667E' }, line: { type: 'none' },
  });
}

// ---- Native tables from CSS grids --------------------------------------------------------------------
function addTable(slide, it, bg) {
  const near = (a, b, t = 3) => Math.abs(a - b) <= t;
  // column tracks
  const starts = []; let acc = it.x;
  it.cols.forEach((w, i) => { starts.push(acc); acc += w + it.colGap; });
  const colOf = x => { let best = 0; starts.forEach((s, i) => { if (x >= s - 3) best = i; }); return best; };
  // rows by top coordinate
  const tops = [];
  it.cells.forEach(c => { if (!tops.some(t => near(t, c.rect.y))) tops.push(c.rect.y); });
  tops.sort((a, b) => a - b);
  const rowOf = y => tops.findIndex(t => near(t, y));
  const nR = tops.length;
  const rowBottom = tops.map((t, i) => Math.max(...it.cells.filter(c => rowOf(c.rect.y) === i).map(c => c.rect.y + c.rect.h)));
  // grid cells
  const grid = Array.from({ length: nR }, () => Array(it.cols.length).fill(null));
  it.cells.forEach(c => { const r = rowOf(c.rect.y), k = colOf(c.rect.x); grid[r][k] = c; });

  // sub-columns: a cell holding two side-by-side text blocks (label + figure) splits its column in two
  const split = it.cols.map((w, k) => {
    let sx = null;
    grid.forEach(row => {
      const c = row[k]; if (!c || c.blocks.length < 2) return;
      const lefts = c.blocks.map(b => b.rect.x);
      if (Math.max(...lefts) - Math.min(...lefts) > 20) {
        const second = Math.max(...lefts); const s = second - 18;
        sx = sx === null ? s : Math.min(sx, s);
      }
    });
    return sx;
  });
  const spacers = it.colGap > 8;
  // physical columns
  const phys = []; // {k, sub, w}
  it.cols.forEach((w, k) => {
    let x0 = starts[k], x1 = starts[k] + w;
    if (!spacers && it.colGap) { x0 -= k > 0 ? it.colGap / 2 : 0; x1 += k < it.cols.length - 1 ? it.colGap / 2 : 0; }
    if (split[k] !== null) { phys.push({ k, sub: 0, w: split[k] - x0 }); phys.push({ k, sub: 1, w: x1 - split[k] }); }
    else phys.push({ k, sub: -1, w: x1 - x0 });
    if (spacers && k < it.cols.length - 1) phys.push({ k: -1, sub: -1, w: it.colGap });
  });
  // row heights (boundaries mid-gap)
  const rowH = tops.map((t, i) => {
    const y0 = i === 0 ? t : (rowBottom[i - 1] + t) / 2;
    const y1 = i === nR - 1 ? rowBottom[i] : (rowBottom[i] + tops[i + 1]) / 2;
    return y1 - y0;
  });

  const NONE = { type: 'none' };
  const bspec = b => (b ? { type: b.style === 'dashed' ? 'dash' : 'solid', pt: +(b.w * PT).toFixed(2), color: b.color } : null);
  const gapLine = (w) => (w ? { type: 'solid', pt: +(w * PT).toFixed(2), color: bg } : null);
  const pick = (...bs) => bs.filter(Boolean).sort((a, b) => b.pt - a.pt)[0] || NONE;

  const mkCell = (c, opts) => {
    const paras = [];
    let prevBottom = null;
    (opts.blocks || []).forEach(b => {
      const extra = { lineSpacing: +(b.para.lh * PT).toFixed(2) };
      if (prevBottom !== null) extra.paraSpaceBefore = +(Math.max(0, b.rect.y - prevBottom) * PT).toFixed(2);
      const rs = runsFor(b.para, extra);
      if (paras.length && rs.length) paras[paras.length - 1].options.breakLine = true;
      paras.push(...rs);
      prevBottom = b.rect.y + b.rect.h;
    });
    return { text: paras.length ? paras : '', options: opts.o };
  };

  const rows = [];
  for (let r = 0; r < nR; r++) {
    const row = [];
    let skipNext = false;
    phys.forEach((pc, pi) => {
      if (skipNext) { skipNext = false; return; }
      const c = pc.k >= 0 ? grid[r][pc.k] : null;
      const o = { valign: 'top', margin: [0, 0, 0, 0] };
      if (c && c.fill) o.fill = { color: c.fill };
      // borders: merge this cell's edges with the neighbours' and the grid gaps
      const above = r > 0 && pc.k >= 0 ? grid[r - 1][pc.k] : null, below = r < nR - 1 && pc.k >= 0 ? grid[r + 1][pc.k] : null;
      const top = c ? pick(bspec(c.b.Top), above && bspec(above.b.Bottom), r > 0 && !spacers ? gapLine(it.rowGap) : null) : NONE;
      const bot = c ? pick(bspec(c.b.Bottom), below && bspec(below.b.Top), r < nR - 1 ? gapLine(it.rowGap) : null) : NONE;
      let left = NONE, right = NONE;
      if (c && !spacers && it.colGap) {
        if (pc.k > 0 && pc.sub <= 0) left = gapLine(it.colGap);
        if (pc.k < it.cols.length - 1 && pc.sub !== 0) right = gapLine(it.colGap);
      }
      if (c && c.b.Left && pc.sub <= 0) left = bspec(c.b.Left);
      if (c && c.b.Right && pc.sub !== 0) right = bspec(c.b.Right);
      o.border = [top, right, bot, left];
      const pad = c ? c.pad : [0, 0, 0, 0];
      const m = [pad[0], pad[1], pad[2], pad[3]];
      if (!c) { row.push({ text: '', options: o }); return; }
      let blocks = c.blocks;
      if (pc.sub === 0) {
        const lefts = blocks.map(b => b.rect.x);
        const twoParts = blocks.length >= 2 && Math.max(...lefts) - Math.min(...lefts) > 20;
        if (twoParts) {
          const sx = split[pc.k];
          const A = blocks.filter(b => b.rect.x < sx), B = blocks.filter(b => b.rect.x >= sx);
          o.margin = [m[0], 6, m[2], m[3]].map(v => inch(v));
          row.push(mkCell(c, { blocks: A, o }));
          const o2 = { ...o, border: [top, right, bot, NONE], margin: [m[0], m[1], m[2], 6].map(v => inch(v)) };
          o.border = [top, NONE, bot, left];
          row.push(mkCell(c, { blocks: B, o: o2 }));
          skipNext = true; return;
        }
        // single block in a split column: figures go right, everything else spans both
        const rightAligned = blocks.length === 1 && blocks[0].para.align === 'right';
        if (rightAligned) {
          row.push({ text: '', options: { ...o, border: [top, NONE, bot, left] } });
          const o2 = { ...o, border: [top, right, bot, NONE], margin: [m[0], m[1], m[2], 6].map(v => inch(v)) };
          row.push(mkCell(c, { blocks, o: o2 }));
          skipNext = true; return;
        }
        o.colspan = 2; o.margin = m.map(v => inch(v));
        row.push(mkCell(c, { blocks, o }));
        skipNext = true; return;
      }
      o.margin = m.map(v => inch(v));
      row.push(mkCell(c, { blocks, o }));
    });
    rows.push(row);
  }
  slide.addTable(rows, {
    x: inch(it.x), y: inch(it.y), w: inch(phys.reduce((s, p) => s + p.w, 0)),
    colW: phys.map(p => inch(p.w)), rowH: rowH.map(h => inch(h)), autoPage: false, margin: 0,
  });
}

// ---- Native charts -----------------------------------------------------------------------------------
const chartFixes = []; // per chart, in creation order: XML post-processing (per-point labels and fills)

function addChart(slide, pres, cfg, ex, shifts) {
  const c = cfg.chart, rows = ex.chart.rows;
  const lbl = { dataLabelFontFace: 'Inter', dataLabelFontSize: +(c.labelPx * PT || 12), dataLabelFontBold: true, dataLabelColor: '0E1A2B' };
  const quiet = {
    showLegend: false, showTitle: false, catAxisHidden: true, valAxisHidden: true,
    valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, valAxisLineShow: false, catAxisLineShow: false,
    layout: { x: 0, y: 0, w: 1, h: 1 }, plotArea: { fill: { color: ex.bg, transparency: 100 } },
  };
  if (c.kind === 'col') {
    const plot = ex.chart.plot;
    const b0 = rows[0].bar, b1 = rows[1].bar;
    const pitch = b1.x - b0.x, gap = pitch - b0.w;
    const scale = b0.h / c.values[0];
    const x = b0.x - gap / 2, w = pitch * rows.length;
    const h = plot.h - 1; // above the axis rule
    slide.addChart(pres.charts.BAR, [{ name: c.name, labels: c.labels, values: c.values }], {
      x: inch(x), y: inch(plot.y), w: inch(w), h: inch(h), barDir: 'col', barGapWidthPct: Math.round(gap / b0.w * 100),
      chartColors: c.colors, valAxisMinVal: 0, valAxisMaxVal: +(h / scale).toFixed(1),
      showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: c.fmt, ...lbl, ...quiet,
      altText: `${c.name}: ` + c.labels.map((l, i) => `${l} ${c.values[i]}`).join('; '),
    });
    chartFixes.push({ points: c.labelColors.map((col, i) => ({ idx: i, labelColor: col })) });
    return;
  }
  // horizontal bars: categories evenly spaced, row labels moved onto the category centres
  const n = rows.length;
  const centres = rows.map(r => r.bar.y + r.bar.h / 2);
  const pitch = (centres[n - 1] - centres[0]) / (n - 1);
  const top = centres[0] - pitch / 2;
  rows.forEach((r, i) => { shifts[i] = (top + pitch * (i + 0.5)) - centres[i]; });
  const barH = rows[0].bar.h;
  const gapPct = Math.round((pitch - barH) / barH * 100);
  if (c.kind === 'hbar') {
    const x0 = rows[0].bar.x;
    const scale = rows[0].bar.w / c.values[0];
    const w = Math.max(...rows.map(r => r.bar.w)) + c.rightPad;
    slide.addChart(pres.charts.BAR, [{ name: c.name, labels: c.labels, values: c.values }], {
      x: inch(x0), y: inch(top), w: inch(w), h: inch(pitch * n), barDir: 'bar', barGapWidthPct: gapPct, catAxisOrientation: 'maxMin',
      chartColors: c.colors, valAxisMinVal: 0, valAxisMaxVal: +(w / scale).toFixed(2),
      showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: c.fmt, ...lbl, ...quiet,
      altText: `${c.name}: ` + c.labels.map((l, i) => `${l} ${c.values[i]}`).join('; '),
    });
    chartFixes.push({ points: c.labelColors.map((col, i) => ({ idx: i, labelColor: col, fmt: (c.fmts || {})[i] })) });
    return;
  }
  // waterfall: invisible offset series + visible cost series (stacked)
  const x0 = Math.min(...rows.map(r => r.bar.x));
  const scale = rows[0].bar.w / c.values[0];
  const offsets = c.values.map((v, i) => (i === c.totalIdx ? 0 : c.values.slice(0, i).reduce((s, q) => s + q, 0)));
  const w = 700;
  slide.addChart(pres.charts.BAR, [
    { name: 'Offset (hidden spacer)', labels: c.labels, values: offsets },
    { name: c.name, labels: c.labels, values: c.values },
  ], {
    x: inch(x0), y: inch(top), w: inch(w), h: inch(pitch * n), barDir: 'bar', barGrouping: 'stacked', barGapWidthPct: gapPct,
    catAxisOrientation: 'maxMin', chartColors: [ex.bg, c.color], valAxisMinVal: 0, valAxisMaxVal: +(w / scale).toFixed(0), ...quiet,
    altText: `${c.name}: ` + c.labels.map((l, i) => `${l} ${c.values[i]}`).join('; '),
  });
  chartFixes.push({ hideSeries: 0, series: 1, points: [
    { idx: c.dashedIdx, noFill: true, line: { color: c.color, w: 1, dash: 'dash' } },
    { idx: c.totalIdx, fill: c.totalColor },
  ] });
}

async function postProcess(file) {
  if (!chartFixes.length) return;
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const names = Object.keys(zip.files).filter(n => /^ppt\/charts\/chart\d+\.xml$/.test(n))
    .sort((a, b) => parseInt(a.match(/(\d+)\.xml/)[1], 10) - parseInt(b.match(/(\d+)\.xml/)[1], 10));
  if (names.length !== chartFixes.length) throw new Error(`chart count mismatch ${names.length} vs ${chartFixes.length}`);
  for (let ci = 0; ci < names.length; ci++) {
    const fix = chartFixes[ci];
    let xml = await zip.file(names[ci]).async('string');
    const sers = xml.split('<c:ser>');
    const edit = (si, fn) => { sers[si + 1] = fn(sers[si + 1]); };
    if (fix.hideSeries !== undefined) {
      edit(fix.hideSeries, s => s.replace(/<c:spPr>[\s\S]*?<\/c:spPr>/, '<c:spPr><a:noFill/><a:ln><a:noFill/></a:ln></c:spPr>')
        .replace(/<c:dPt>[\s\S]*?<\/c:dPt>/g, ''));
    }
    const si = fix.series || 0;
    edit(si, s => {
      // per-point fills
      const fills = fix.points.filter(p => p.fill || p.noFill);
      if (fills.length) {
        s = s.replace(/<c:dPt>[\s\S]*?<\/c:dPt>/g, m => (fills.some(p => m.includes(`<c:idx val="${p.idx}"/>`)) ? '' : m));
        const dpts = fills.map(p => {
          const ln = p.line ? `<a:ln w="${Math.round(p.line.w * 12700)}"><a:solidFill><a:srgbClr val="${p.line.color}"/></a:solidFill><a:prstDash val="${p.line.dash}"/></a:ln>` : '<a:ln><a:noFill/></a:ln>';
          const fill = p.noFill ? '<a:noFill/>' : `<a:solidFill><a:srgbClr val="${p.fill}"/></a:solidFill>`;
          return `<c:dPt><c:idx val="${p.idx}"/><c:invertIfNegative val="0"/><c:bubble3D val="0"/><c:spPr>${fill}${ln}</c:spPr></c:dPt>`;
        }).join('');
        // dPt elements follow c:spPr / c:invertIfNegative of the series
        if (/<c:invertIfNegative val="0"\/>/.test(s)) s = s.replace(/(<c:invertIfNegative val="0"\/>)/, `$1${dpts}`);
        else s = s.replace(/(<\/c:spPr>)/, `$1${dpts}`);
      }
      // per-point data labels (colour, number format)
      const labs = fix.points.filter(p => p.labelColor || p.fmt);
      if (labs.length && s.includes('<c:dLbls>')) {
        const base = s.match(/<c:dLbls>([\s\S]*?)<\/c:dLbls>/)[1];
        const fmt0 = (base.match(/<c:numFmt [^>]*\/>/) || [''])[0];
        const tx0 = (base.match(/<c:txPr>[\s\S]*?<\/c:txPr>/) || [''])[0];
        const pos = (base.match(/<c:dLblPos [^>]*\/>/) || [''])[0];
        const dl = labs.map(p => {
          const fmt = p.fmt ? `<c:numFmt formatCode="${p.fmt.replace(/"/g, '&quot;').replace(/>/g, '&gt;')}" sourceLinked="0"/>` : fmt0;
          const tx = p.labelColor ? tx0.replace(/<a:srgbClr val="[0-9A-Fa-f]{6}"\/>/, `<a:srgbClr val="${p.labelColor}"/>`) : tx0;
          return `<c:dLbl><c:idx val="${p.idx}"/>${fmt}<c:spPr><a:noFill/><a:ln><a:noFill/></a:ln></c:spPr>${tx}${pos}` +
            '<c:showLegendKey val="0"/><c:showVal val="1"/><c:showCatName val="0"/><c:showSerName val="0"/><c:showPercent val="0"/><c:showBubbleSize val="0"/></c:dLbl>';
        }).join('');
        s = s.replace('<c:dLbls>', '<c:dLbls>' + dl);
      }
      return s;
    });
    xml = sers.join('<c:ser>');
    zip.file(names[ci], xml);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
}

// ---- Main ------------------------------------------------------------------------------------------
(async () => {
  const deck = JSON.parse(fs.readFileSync(path.join(SRC, 'deck.json'), 'utf8'));
  const ids = deck.order;
  const sectionStart = {};
  Object.values(deck.sections || {}).forEach(s => { sectionStart[s.start] = s.description; });
  let fontCss = '';
  try {
    fontCss = fs.readFileSync(path.join(FONT_DIR, 'local.css'), 'utf8').replace(/url\((f\d+\.woff2)\)/g, (m, f) => `url(file://${FONT_DIR}/${f})`);
  } catch (e) { console.warn('fonts not found; measuring with fallback fonts'); }

  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await ctx.route(/^https?:/, r => r.abort());
  const page = await ctx.newPage();
  const extracted = [];
  const tmpHtml = path.join(require('os').tmpdir(), `d01_slide_${process.pid}.html`);
  for (const id of ids) {
    const h = fs.readFileSync(path.join(SRC, 'slides', id + '.html'), 'utf8');
    fs.writeFileSync(tmpHtml, `<!doctype html><html><head><meta charset="utf-8"><style>${fontCss}${SLIDE_CSS}</style></head><body>${h}</body></html>`);
    await page.goto('file://' + tmpHtml, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(50);
    const loaded = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family).filter((v, i, a) => a.indexOf(v) === i).join(','));
    if (!/Inter/.test(loaded)) console.warn(id, 'web fonts not loaded:', loaded);
    extracted.push(await page.evaluate(pageExtract, SLIDE_CFG[id] || {}));
  }
  await browser.close();
  try { fs.unlinkSync(tmpHtml); } catch (e) { /* ignore */ }

  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE';
  pres.title = deck.title;
  pres.subject = 'Project Rampart: CRA board briefing (illustrative)';
  pres.author = 'Advisory';
  pres.company = 'Advisory';
  pres.theme = { headFontFace: 'Source Serif 4', bodyFontFace: 'Inter' };

  let section = null;
  extracted.forEach((ex, i) => {
    const id = ids[i];
    if (sectionStart[id]) { section = sectionStart[id]; pres.addSection({ title: section }); }
    const slide = pres.addSlide(section ? { sectionTitle: section } : undefined);
    slide.background = { color: ex.bg };
    const cfg = SLIDE_CFG[id] || {};
    const shifts = {};
    let chartAdded = false;
    const placeChart = () => { if (cfg.chart && !chartAdded) { addChart(slide, pres, cfg, ex, shifts); chartAdded = true; } };
    if (cfg.chart && cfg.chart.kind !== 'col') placeChart(); // computes row shifts before the labels are placed
    for (const it of ex.items) {
      const dy = it.row !== undefined && shifts[it.row] ? shifts[it.row] : 0;
      if (it.t === 'text') addTextItem(slide, it, dy);
      else if (it.t === 'rect') addRect(slide, pres, it, dy);
      else if (it.t === 'line') addLine(slide, pres, it, dy);
      else if (it.t === 'shape') addShapeItem(slide, pres, it, dy);
      else if (it.t === 'table') addTable(slide, it, ex.bg);
    }
    placeChart();
    slide.addNotes(ex.notes || ' ');
  });
  await pres.writeFile({ fileName: OUT });
  await postProcess(OUT);
  console.log('wrote', OUT, ids.length, 'slides,', chartFixes.length, 'charts');
})().catch(e => { console.error(e); process.exit(1); });
