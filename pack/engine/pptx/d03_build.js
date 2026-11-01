// D03 Engineering training deck -> editable PPTX.
// Loads each slide HTML in headless Chromium with the same harness CSS as the PDF render,
// measures the rendered DOM and emits native PowerPoint objects (text boxes, shapes, tables,
// one native bar chart) at the measured positions, with speaker notes and sections.
// Usage: node pack/engine/pptx/d03_build.js [outFile]
const { chromium } = require('playwright');
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..', '..');
const FOLDER = path.join(ROOT, 'pack', 'out', 'hosted', 'D03-training-deck');
const SRC = path.join(FOLDER, 'source', 'project');
const OUTFILE = process.argv[2] || path.join(FOLDER, 'D03 - Engineering training deck.pptx');
// Web fonts used for the reference PDF (optional; falls back to locally installed fonts).
const FONTDIR = process.env.D03_FONTDIR || path.join(__dirname, 'fonts');
const SKILL_THEME = '/root/.claude/skills/synced/513b31dd-0faa-4eef-a4a6-c81499db4824_8549626d-ad30-4421-930c-b70b7e7d903d/pptx/scripts/apply_theme.js';

const PX = 1 / 144;          // 1920 px = 13.333 in
const PT = 0.5;              // 1 px = 0.5 pt at this scale
const r3 = v => Math.round(v * 1000) / 1000;
const inch = px => r3(px * PX);

const SECTION_TITLES = { s1: '01 · Why it matters', s2: '02 · Design', s3: '03 · Build and release', s4: '04 · Ship and support', s5: '05 · Evidence', s6: '06 · Check and close' };

const THEME = {
  name: 'Advisory',
  headFontFace: 'Source Serif 4',
  bodyFontFace: 'Inter',
  colors: {
    dk1: '0E1A2B', lt1: 'FFFFFF', dk2: '26364D', lt2: 'FAFAF7',
    accent1: '0F6E6A', accent2: '2E9C93', accent3: '0A5753', accent4: '56667E', accent5: 'B54708', accent6: 'B42318',
    hlink: '0F6E6A', folHlink: '0A5753',
  },
};

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
x-shape{display:block;flex:none}
x-icon{display:block;flex:none}
x-icon svg{width:100%;height:100%;display:block}
`;
const ICONS = {
  Warning: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
};

function decode(s) {
  return s.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#(\d+);/g, (m, n) => String.fromCodePoint(+n))
    .replace(/\s+/g, ' ').trim();
}

// ---------------------------------------------------------------- in-page extraction
function extractSlide(sectionId) {
  const sec = document.getElementById(sectionId);
  const S = sec.getBoundingClientRect();
  const items = [];
  const hex = c => {
    const m = c && c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(',').map(s => parseFloat(s));
    const a = p.length > 3 ? p[3] : 1;
    if (a === 0) return null;
    return { hex: p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase(), a };
  };
  const rel = r => ({ x: r.left - S.left, y: r.top - S.top, w: r.width, h: r.height });
  const isInline = n => n.nodeType === 3 || (n.nodeType === 1 && getComputedStyle(n).display.startsWith('inline') && n.tagName !== 'X-ICON');
  const hasText = n => (n.textContent || '').trim().length > 0;
  const firstFont = f => f.split(',')[0].replace(/["']/g, '').trim();

  // --- bar-chart detection: rows of [label p][bar div][value p]
  const charts = [];
  for (const host of sec.querySelectorAll('div')) {
    const rows = [...host.children].filter(c => c.tagName === 'DIV' && c.children.length === 3 &&
      c.children[0].tagName === 'P' && c.children[1].tagName === 'DIV' && !hasText(c.children[1]) &&
      c.children[2].tagName === 'P' && /^\d+(\.\d+)?$/.test(c.children[2].textContent.trim()));
    if (rows.length >= 3) {
      const data = rows.map(r => {
        const bar = r.children[1];
        const bcs = getComputedStyle(bar);
        return {
          label: r.children[0].textContent.trim(), value: parseFloat(r.children[2].textContent),
          color: hex(bcs.backgroundColor).hex, barRect: rel(bar.getBoundingClientRect()),
          labelColor: hex(getComputedStyle(r.children[0]).color).hex,
          valueColor: hex(getComputedStyle(r.children[2]).color).hex,
          rowRect: rel(r.getBoundingClientRect()),
        };
      });
      const lcs = getComputedStyle(rows[0].children[0]);
      const vcs = getComputedStyle(rows[0].children[2]);
      const first = data[0].rowRect, last = data[data.length - 1].rowRect;
      charts.push({
        kind: 'barchart', data,
        rect: { x: first.x, y: first.y, w: first.w, h: last.y + last.h - first.y },
        font: { family: firstFont(lcs.fontFamily), size: parseFloat(lcs.fontSize), color: hex(lcs.color).hex },
        vfont: { family: firstFont(vcs.fontFamily), size: parseFloat(vcs.fontSize), color: hex(vcs.color).hex, bold: parseInt(vcs.fontWeight) >= 600 },
      });
      rows.forEach(r => r.setAttribute('data-skip', '1'));
    }
  }
  items.push(...charts);

  // --- runs collector
  function collectRuns(root) {
    const runs = [];
    const walk = (n, linkHref) => {
      if (n.nodeType === 3) {
        const pe = n.parentElement;
        const cs = getComputedStyle(pe);
        let t = n.textContent;
        const pre = /pre/.test(cs.whiteSpace) && cs.whiteSpace !== 'nowrap';
        if (!pre) t = t.replace(/\s+/g, ' ');
        if (cs.textTransform === 'uppercase') t = t.toUpperCase();
        if (!t) return;
        const c = hex(cs.color);
        runs.push({
          text: t, family: firstFont(cs.fontFamily), size: parseFloat(cs.fontSize),
          bold: parseInt(cs.fontWeight) >= 600, italic: cs.fontStyle === 'italic',
          color: c ? c.hex : '000000', ls: parseFloat(cs.letterSpacing) || 0,
          underline: /underline/.test(cs.textDecorationLine), href: linkHref || null,
        });
      } else if (n.nodeType === 1) {
        if (n.tagName === 'BR') { runs.push({ br: true }); return; }
        if (n.tagName === 'ASIDE') return;
        const href = n.tagName === 'A' ? n.getAttribute('href') : linkHref;
        const block = !isInline(n);
        if (block && runs.length && !runs[runs.length - 1].br) runs.push({ br: true, para: true });
        for (const c of n.childNodes) walk(c, href);
        if (block) runs.push({ br: true, para: true });
      }
    };
    for (const c of root.childNodes) walk(c, null);
    // trim whitespace at line starts / ends and collapse double spaces across runs
    const out = [];
    let atStart = true;
    for (const r of runs) {
      if (r.br) {
        if (out.length && !out[out.length - 1].br) { out[out.length - 1].text = out[out.length - 1].text.replace(/ +$/, ''); }
        if (out.length && !out[out.length - 1].br) out.push(r);
        atStart = true; continue;
      }
      let t = r.text;
      if (atStart) t = t.replace(/^ +/, '');
      else if (out.length && / $/.test(out[out.length - 1].text)) t = t.replace(/^ +/, '');
      if (!t) continue;
      out.push({ ...r, text: t }); atStart = false;
    }
    while (out.length && out[out.length - 1].br) out.pop();
    if (out.length) out[out.length - 1].text = out[out.length - 1].text.replace(/ +$/, '');
    return out;
  }

  const boxOf = (el, cs) => {
    const r = rel(el.getBoundingClientRect());
    const pl = parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth);
    const pr = parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth);
    const pt = parseFloat(cs.paddingTop) + parseFloat(cs.borderTopWidth);
    const pb = parseFloat(cs.paddingBottom) + parseFloat(cs.borderBottomWidth);
    return { r, pl, pr, pt, pb };
  };
  const lineInfo = el => {
    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()].filter(q => q.width > 0.5);
    const tops = [];
    for (const q of rects) if (!tops.some(t => Math.abs(t - q.top) < 4)) tops.push(q.top);
    const br = range.getBoundingClientRect();
    return { lines: tops.length, rect: rel(br) };
  };

  const isTextBlock = el => {
    if (isInline(el)) return false;
    if (!hasText(el)) return false;
    for (const c of el.childNodes) {
      if (c.nodeType === 1 && !isInline(c) && c.tagName !== 'ASIDE') return false;
    }
    return true;
  };

  const textItem = (el, cs, b) => {
    const li = lineInfo(el);
    const align = { start: 'left', left: 'left', right: 'right', center: 'center', end: 'right', justify: 'justify' }[cs.textAlign] || 'left';
    return {
      runs: collectRuns(el), align, lines: li.lines, textRect: li.rect,
      lh: parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2,
      nowrap: cs.whiteSpace === 'nowrap',
      tag: el.tagName,
      box: { x: b.r.x + b.pl, y: b.r.y + b.pt, w: b.r.w - b.pl - b.pr, h: b.r.h - b.pt - b.pb },
      pad: { l: b.pl, r: b.pr, t: b.pt, b: b.pb },
    };
  };

  const shapes = [], texts = [];
  const visit = el => {
    if (el.getAttribute && el.getAttribute('data-skip')) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || el.tagName === 'ASIDE') return;
    if (el.tagName === 'TABLE') { shapes.push(tableItem(el)); return; }
    if (el.tagName === 'X-ICON') {
      shapes.push({ kind: 'icon', name: el.getAttribute('name'), rect: rel(el.getBoundingClientRect()), color: hex(cs.color).hex });
      return;
    }
    if (el !== sec) {
      const b = boxOf(el, cs);
      const bg = hex(cs.backgroundColor);
      const sides = ['Top', 'Right', 'Bottom', 'Left'].map(s => ({
        w: parseFloat(cs['border' + s + 'Width']) || 0, style: cs['border' + s + 'Style'], c: hex(cs['border' + s + 'Color']),
      })).map(s => (s.style === 'none' || !s.c ? { ...s, w: 0 } : s));
      const uniform = sides.every(s => s.w > 0 && s.w === sides[0].w && s.c.hex === sides[0].c.hex && s.style === sides[0].style);
      const radius = parseFloat(cs.borderTopLeftRadius) || 0;
      const allR = ['borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomRightRadius', 'borderBottomLeftRadius'].every(k => parseFloat(cs[k]) === radius);
      const rot = cs.transform && cs.transform !== 'none';
      const tb = isTextBlock(el);
      if (bg || uniform) {
        const sh = { kind: 'box', rect: b.r, fill: bg, line: uniform ? { w: sides[0].w, c: sides[0].c.hex, dash: sides[0].style } : null, radius: allR ? radius : 0, rot: !!rot };
        if (tb) { sh.text = textItem(el, cs, b); }
        shapes.push(sh);
      }
      if (!uniform) {
        sides.forEach((s, i) => {
          if (!s.w) return;
          const r = b.r;
          const rr = [
            { x: r.x, y: r.y, w: r.w, h: s.w }, { x: r.x + r.w - s.w, y: r.y, w: s.w, h: r.h },
            { x: r.x, y: r.y + r.h - s.w, w: r.w, h: s.w }, { x: r.x, y: r.y, w: s.w, h: r.h },
          ][i];
          shapes.push({ kind: 'edge', rect: rr, c: s.c.hex, dash: s.style, vertical: i % 2 === 1, w: s.w });
        });
      }
      if (tb) { if (!(bg || uniform)) texts.push(textItem(el, cs, b)); return; }
    }
    for (const c of el.children) visit(c);
  };

  function tableItem(t) {
    const tcs = getComputedStyle(t);
    const rows = [...t.rows];
    const tr = rel(t.getBoundingClientRect());
    // column boundaries from all cell edges
    const xs = new Set();
    rows.forEach(r => [...r.cells].forEach(c => { const q = rel(c.getBoundingClientRect()); xs.add(Math.round(q.x * 2) / 2); xs.add(Math.round((q.x + q.w) * 2) / 2); }));
    const cols = [...xs].sort((a, b) => a - b);
    const colW = cols.slice(1).map((x, i) => x - cols[i]);
    const tborder = ['Top', 'Right', 'Bottom', 'Left'].map(s => ({ w: parseFloat(tcs['border' + s + 'Width']) || 0, c: hex(tcs['border' + s + 'Color']), style: tcs['border' + s + 'Style'] }));
    const out = rows.map((r, ri) => {
      const rcs = getComputedStyle(r);
      const rbg = hex(rcs.backgroundColor);
      return {
        h: r.getBoundingClientRect().height,
        cells: [...r.cells].map(c => {
          const cs = getComputedStyle(c);
          const q = rel(c.getBoundingClientRect());
          const border = ['Top', 'Right', 'Bottom', 'Left'].map((s, i) => {
            let w = parseFloat(cs['border' + s + 'Width']) || 0; let col = hex(cs['border' + s + 'Color']); let st = cs['border' + s + 'Style'];
            const edge = (i === 0 && ri === 0) || (i === 2 && ri === rows.length - 1) || (i === 3 && Math.abs(q.x - tr.x) < 1) || (i === 1 && Math.abs(q.x + q.w - tr.x - tr.w) < 1);
            if (edge && tborder[i].w > 0 && tborder[i].style !== 'none' && tborder[i].c) { w = Math.max(w, tborder[i].w); col = col || tborder[i].c; st = 'solid'; }
            return st === 'none' || !col || !w ? null : { w, c: col.hex };
          });
          const bg = hex(cs.backgroundColor) || rbg;
          return {
            runs: collectRuns(c), colspan: c.colSpan, rowspan: c.rowSpan,
            fill: bg ? bg.hex : null, border,
            pad: [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].map(parseFloat),
            valign: cs.verticalAlign === 'middle' ? 'middle' : (cs.verticalAlign === 'bottom' ? 'bottom' : 'top'),
            align: { start: 'left', left: 'left', right: 'right', center: 'center', end: 'right' }[cs.textAlign] || 'left',
            lh: parseFloat(cs.lineHeight),
          };
        }),
      };
    });
    return { kind: 'table', rect: tr, colW, rows: out };
  }

  visit(sec);
  items.push(...shapes);
  items.push(...texts.map(t => ({ kind: 'text', ...t })));
  const bg = hex(getComputedStyle(sec).backgroundColor);
  const aside = sec.querySelector('aside');
  return { bg: bg ? bg.hex : 'FFFFFF', items, notes: aside ? aside.textContent.replace(/\s+/g, ' ').trim() : '' };
}

// ---------------------------------------------------------------- PPTX emission
function runOpts(r, lh, extra = {}) {
  const o = {
    fontFace: r.family, fontSize: r.size * PT, bold: r.bold, italic: r.italic, color: r.color,
    lineSpacing: lh * PT, ...extra,
  };
  if (r.ls) o.charSpacing = r.ls * PT;
  if (r.underline) o.underline = { style: 'sng' };
  if (r.href) o.hyperlink = { url: r.href };
  return o;
}

function toTextArr(runs, lh, para = {}) {
  const arr = [];
  let soft = false;
  runs.forEach((r, i) => {
    if (r.br) {
      if (r.para) { if (arr.length) arr[arr.length - 1].options.breakLine = true; soft = false; }
      else soft = true;
      return;
    }
    const o = runOpts(r, lh, para);
    if (soft) { o.softBreakBefore = true; soft = false; }
    arr.push({ text: r.text, options: o });
  });
  return arr;
}

// Text box geometry with slack: single-line text never wraps; multi-line text gets ~2.5% extra width.
function textGeom(t, forceWrap = false) {
  let { x, w } = t.box;
  const y = t.box.y, h = Math.max(t.box.h, t.textRect.h);
  let wrap = true;
  if (!forceWrap && (t.lines <= 1 || t.nowrap)) wrap = false;
  const slack = wrap ? Math.min(Math.max(w * 0.025, 4), 30) : 0;
  if (t.align === 'right') x -= slack; else if (t.align === 'center') x -= slack / 2;
  w += slack;
  return { x, y, w, h, wrap };
}

// Merge consecutive one-line monospace paragraphs (code listings) into one text box;
// left padding becomes leading spaces (one per character advance, 0.6 em for JetBrains Mono).
function mergeCodeLines(items) {
  const out = [];
  const isCode = it => it && it.kind === 'text' && it.nowrap && /mono/i.test((it.runs[0] || {}).family || '') && it.lines <= 1;
  for (const it of items) {
    const prev = out[out.length - 1];
    if (isCode(it) && prev && (prev.kind === 'code' || isCode(prev))) {
      const base = prev.kind === 'code' ? prev : null;
      const left = it.box.x - it.pad.l;
      const ref = base || prev;
      const refLeft = base ? base.left : prev.box.x - prev.pad.l;
      const bottom = base ? base.box.y + base.box.h : prev.box.y + prev.box.h + prev.pad.b;
      if (Math.abs(left - refLeft) < 1 && Math.abs(it.box.y - it.pad.t - bottom) < 2 && it.lh === ref.lh) {
        const code = base || { kind: 'code', left: refLeft, lh: prev.lh, paras: [prev], box: { x: refLeft, y: prev.box.y - prev.pad.t, w: 0, h: 0 } };
        if (!base) out[out.length - 1] = code;
        code.paras.push(it);
        code.box.w = Math.max(...code.paras.map(q => q.box.x + q.box.w - code.left));
        code.box.h = it.box.y + it.box.h + it.pad.b - code.box.y;
        continue;
      }
    }
    out.push(it);
  }
  // convert merged groups into ordinary text items
  return out.map(it => {
    if (it.kind !== 'code') return it;
    const runs = [];
    it.paras.forEach((q, i) => {
      if (i) runs.push({ br: true, para: true });
      const cw = 0.6 * q.runs[0].size;
      const n = Math.round((q.box.x - it.left) / cw);
      q.runs.forEach((r, j) => runs.push(j === 0 && n > 0 ? { ...r, text: ' '.repeat(n) + r.text } : r));
    });
    return { kind: 'text', runs, align: 'left', lines: it.paras.length, nowrap: true, lh: it.lh, tag: 'P',
      textRect: { ...it.box }, box: { ...it.box }, pad: { l: 0, r: 0, t: 0, b: 0 } };
  });
}

function addTextItem(slide, t, extra = {}) {
  const g = textGeom(t);
  const arr = toTextArr(t.runs, t.lh, { align: t.align === 'justify' ? 'left' : t.align });
  if (!arr.length) return;
  slide.addText(arr, {
    x: inch(g.x), y: inch(g.y), w: inch(g.w), h: inch(g.h), margin: 0, valign: 'top', wrap: g.wrap,
    isTextBox: true, fit: 'none', ...extra,
  });
}

function emitBox(pres, slide, s) {
  const r = s.rect;
  let shape = pres.ShapeType.rect;
  const opts = {};
  if (s.rot) shape = pres.ShapeType.diamond;
  else if (s.radius > 0) {
    shape = pres.ShapeType.roundRect;
    opts.rectRadius = r3(Math.min(s.radius, r.h / 2, r.w / 2) * PX);
  }
  let { x, y, w, h } = r;
  if (s.line) { // CSS border sits inside the box; PowerPoint strokes on the edge
    x += s.line.w / 2; y += s.line.w / 2; w -= s.line.w; h -= s.line.w;
    opts.line = { color: s.line.c, width: s.line.w * PT, dashType: s.line.dash === 'dashed' ? 'dash' : (s.line.dash === 'dotted' ? 'sysDot' : 'solid') };
  } else opts.line = { type: 'none' };
  opts.fill = s.fill ? { color: s.fill.hex, transparency: Math.round((1 - s.fill.a) * 100) } : { type: 'none' };
  if (s.text && shape !== pres.ShapeType.rect) {
    // rounded/diamond geometries inset their text rectangle: draw the shape, then a free text box
    slide.addShape(shape, { x: inch(x), y: inch(y), w: inch(w), h: inch(h), ...opts });
    addTextItem(slide, s.text);
  } else if (s.text) {
    const t = s.text;
    const arr = toTextArr(t.runs, t.lh, { align: t.align === 'justify' ? 'left' : t.align });
    const bw = s.line ? s.line.w / 2 : 0;
    slide.addText(arr, {
      shape, x: inch(x), y: inch(y), w: inch(w), h: inch(h), ...opts,
      margin: [t.pad.l - bw, t.pad.r - bw, t.pad.b - bw, t.pad.t - bw].map(v => Math.max(0, v * PT)),
      valign: 'top', wrap: !(t.lines <= 1 || t.nowrap), fit: 'none', isTextBox: true,
    });
  } else {
    slide.addShape(shape, { x: inch(x), y: inch(y), w: inch(w), h: inch(h), ...opts });
  }
}

function emitEdge(pres, slide, e) {
  const r = e.rect;
  if (e.dash === 'dashed' || e.dash === 'dotted') {
    const dashType = e.dash === 'dashed' ? 'dash' : 'sysDot';
    if (e.vertical) slide.addShape(pres.ShapeType.line, { x: inch(r.x + r.w / 2), y: inch(r.y), w: 0, h: inch(r.h), line: { color: e.c, width: e.w * PT, dashType } });
    else slide.addShape(pres.ShapeType.line, { x: inch(r.x), y: inch(r.y + r.h / 2), w: inch(r.w), h: 0, line: { color: e.c, width: e.w * PT, dashType } });
  } else {
    slide.addShape(pres.ShapeType.rect, { x: inch(r.x), y: inch(r.y), w: inch(r.w), h: inch(r.h), fill: { color: e.c }, line: { type: 'none' } });
  }
}

function emitIcon(pres, slide, ic) {
  const r = ic.rect; // Warning: outlined triangle with an exclamation mark, as in the 24-unit SVG
  const u = r.w / 24;
  slide.addShape(pres.ShapeType.triangle, {
    x: inch(r.x + 1.8 * u), y: inch(r.y + 3 * u), w: inch(20.4 * u), h: inch(18 * u),
    fill: { type: 'none' }, line: { color: ic.color, width: 2 * u * PT },
  });
  slide.addShape(pres.ShapeType.line, { x: inch(r.x + 12 * u), y: inch(r.y + 9 * u), w: 0, h: inch(4 * u), line: { color: ic.color, width: 2 * u * PT } });
  slide.addShape(pres.ShapeType.ellipse, { x: inch(r.x + 11 * u), y: inch(r.y + 16 * u), w: inch(2 * u), h: inch(2 * u), fill: { color: ic.color }, line: { type: 'none' } });
}

function emitTable(slide, t) {
  const rows = t.rows.map(row => row.cells.map(c => {
    const arr = toTextArr(c.runs, c.lh, { align: c.align });
    const o = {
      margin: c.pad.map(v => r3(v * PX)), // inches (values < 1)
      valign: c.valign, align: c.align,
      border: c.border.map(b => (b ? { type: 'solid', pt: b.w * PT, color: b.c } : { type: 'none' })),
    };
    if (c.fill) o.fill = { color: c.fill };
    if (c.colspan > 1) o.colspan = c.colspan;
    if (c.rowspan > 1) o.rowspan = c.rowspan;
    return { text: arr.length ? arr : '', options: o };
  }));
  slide.addTable(rows, {
    x: inch(t.rect.x), y: inch(t.rect.y), w: inch(t.rect.w),
    colW: t.colW.map(inch), rowH: t.rows.map(r => inch(r.h)), autoPage: false,
  });
}

function emitBarChart(pres, slide, ch) {
  const d = ch.data;
  const scale = d[0].barRect.w / d[0].value; // px per unit
  const maxV = Math.max(...d.map(v => v.value));
  const plotX = d[0].barRect.x - ch.rect.x;
  const plotW = scale * maxV;
  const band = ch.rect.h / d.length;
  const barH = d[0].barRect.h;
  slide.addChart(pres.ChartType.bar, [{ name: 'Support period (years)', labels: d.map(v => v.label), values: d.map(v => v.value) }], {
    x: inch(ch.rect.x), y: inch(ch.rect.y), w: inch(ch.rect.w), h: inch(ch.rect.h),
    barDir: 'bar', barGapWidthPct: Math.round(((band - barH) / barH) * 100),
    chartColors: d.map(v => v.color),
    layout: { x: r3(plotX / ch.rect.w), y: 0, w: r3(plotW / ch.rect.w), h: 1 },
    catAxisOrientation: 'maxMin', catAxisLabelColor: ch.font.color, catAxisLabelFontFace: ch.font.family,
    catAxisLabelFontSize: ch.font.size * PT, catAxisLineShow: false, catAxisMajorTickMark: 'none',
    catGridLine: { style: 'none' },
    valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: maxV, valGridLine: { style: 'none' }, valAxisLineShow: false,
    showValue: true, dataLabelPosition: 'outEnd', dataLabelColor: ch.vfont.color, dataLabelFontFace: ch.vfont.family,
    dataLabelFontSize: ch.vfont.size * PT, dataLabelFontBold: ch.vfont.bold, dataLabelFormatCode: '0',
    showLegend: false, showTitle: false, plotArea: { fill: { color: 'FFFFFF', transparency: 100 } },
    altText: 'Bar chart: ' + d.map(v => `${v.label} ${v.value}`).join(', '),
  });
}

(async () => {
  const deck = JSON.parse(fs.readFileSync(path.join(SRC, 'deck.json'), 'utf8'));
  const ids = deck.order;
  for (const id of ids) if (!/^[A-Za-z0-9_-]{1,64}$/.test(id)) throw new Error('bad id ' + id);
  let fontCss = '';
  if (fs.existsSync(path.join(FONTDIR, 'local.css'))) {
    fontCss = fs.readFileSync(path.join(FONTDIR, 'local.css'), 'utf8').replace(/url\((f\d+\.woff2)\)/g, (m, f) => `url(file://${FONTDIR}/${f})`);
  } else console.warn('web fonts not found; measuring with installed fonts');
  const body = ids.map(id => `<div class="page">${fs.readFileSync(path.join(SRC, 'slides', id + '.html'), 'utf8')}</div>`).join('\n');
  const tmp = path.join(require('os').tmpdir(), `d03_build_${process.pid}.html`);
  fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset="utf-8"><style>${fontCss}${SLIDE_CSS}</style></head><body>${body}</body></html>`);

  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await ctx.route(/^https?:/, r => r.abort());
  const page = await ctx.newPage();
  await page.goto('file://' + tmp, { waitUntil: 'load' });
  await page.evaluate(icons => document.querySelectorAll('x-icon').forEach(el => { el.innerHTML = icons[el.getAttribute('name')] || ''; }), ICONS);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const slides = [];
  for (const id of ids) slides.push(await page.evaluate(extractSlide, id));
  await browser.close();
  fs.unlinkSync(tmp);
  if (process.env.D03_DUMP) fs.writeFileSync(process.env.D03_DUMP, JSON.stringify(slides, null, 1));

  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE';
  pres.title = deck.title;
  pres.author = 'Advisory';
  pres.subject = 'Project Rampart: CRA engineering training (illustrative)';
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };

  // Title layouts: one per distinct title geometry, so every slide title is a real title placeholder.
  const layouts = {};
  slides.forEach((s, i) => {
    const ti = s.items.findIndex(it => it.kind === 'text' && (it.tag === 'H1' || it.tag === 'H2'));
    if (ti < 0) return;
    const t = s.items[ti];
    const g = textGeom(t, true);
    const r0 = t.runs.find(r => !r.br);
    const key = [g.x, g.y, g.w, r0.family, r0.size, r0.color, s.bg].map(v => (typeof v === 'number' ? Math.round(v) : v)).join('|');
    if (!layouts[key]) {
      const nContent = Object.values(layouts).filter(n => n.startsWith('Advisory Content')).length;
      const name = t.tag === 'H1' ? 'Advisory Cover' : (nContent ? `Advisory Content ${nContent + 1}` : 'Advisory Content');
      layouts[key] = name;
      pres.defineSlideMaster({
        title: name, background: { color: s.bg },
        objects: [{ placeholder: { options: {
          name: 'title', type: 'title', x: inch(g.x), y: inch(g.y), w: inch(g.w), h: inch(Math.max(g.h, t.lh * 2)),
          fontFace: r0.family, fontSize: r0.size * PT, color: r0.color, bold: r0.bold, valign: 'top', margin: 0, align: 'left',
        }, text: '' } }],
      });
    }
    s.titleIdx = ti; s.layout = layouts[key];
  });

  const secStart = {};
  for (const [k, v] of Object.entries(deck.sections || {})) secStart[v.start] = SECTION_TITLES[k] || k;
  let curSection = null;
  slides.forEach((s, i) => {
    if (secStart[ids[i]]) { curSection = secStart[ids[i]]; pres.addSection({ title: curSection }); }
    const slide = pres.addSlide({ masterName: s.layout, sectionTitle: curSection || undefined });
    slide.background = { color: s.bg };
    const titleItem = s.items[s.titleIdx];
    s.items = mergeCodeLines(s.items);
    s.titleIdx = s.items.indexOf(titleItem);
    for (const [j, it] of s.items.entries()) {
      if (it.kind === 'barchart') emitBarChart(pres, slide, it);
      else if (it.kind === 'box') emitBox(pres, slide, it);
      else if (it.kind === 'edge') emitEdge(pres, slide, it);
      else if (it.kind === 'icon') emitIcon(pres, slide, it);
      else if (it.kind === 'table') emitTable(slide, it);
      else if (it.kind === 'text') {
        if (j === s.titleIdx) {
          const arr = toTextArr(it.runs, it.lh, { align: 'left' });
          slide.addText(arr, { placeholder: 'title' });
        } else addTextItem(slide, it);
      }
    }
    slide.addNotes(s.notes || '');
  });

  await pres.writeFile({ fileName: OUTFILE });
  if (fs.existsSync(SKILL_THEME)) {
    const { applyTheme } = require(SKILL_THEME);
    await applyTheme(OUTFILE, THEME);
  }
  console.log('wrote', OUTFILE, slides.length, 'slides', fs.statSync(OUTFILE).size, 'bytes');
})().catch(e => { console.error(e); process.exit(1); });
