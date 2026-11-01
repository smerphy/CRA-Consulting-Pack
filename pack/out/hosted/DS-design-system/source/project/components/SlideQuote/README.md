# SlideQuote

The statement slide: one sentence on the `accent-600` ground — the governing thought, a verbatim quotation, or the single callout the audience must carry out of the room.

**Use for** the governing thought after the title slide, or one quotation. At most one per deck: it is the deck's only full-colour slide.

**Anatomy**
- Label pinned in the top margin: what this is ("Governing thought", "In their words", "What the regulation says"), 24px, 600, uppercase, `accent-100`.
- Statement: Source Serif 4 96px / 104px, 500, `paper`, max three lines. A statement ends with a full stop.
- 160 × 4 `accent-100` rule, then the supporting sentence: Inter 32px / 44px, `accent-100`.
- Footer on teal: `accent-100` text, `accent-400` hairline.

**Quotation variant**: set the quotation in Source Serif 4 italic 56px / 68px inside curly quotes (“ ”), verbatim and under 15 words, then the attribution as the supporting line: "— Role, organisation type, source and date" (e.g. "— PSIRT lead, interview, 22 Oct 2026; illustrative"). Never invent or improve a quotation; never name individuals; cite regulation by article.

Contrast: `paper` on `accent-600` 5.8:1; `accent-100` on `accent-600` 5.1:1.

**You provide** label, statement or quotation, supporting line or attribution.

**Frame rules (every master)** — 1920 × 1080 canvas; `padding:128px 128px 160px`; inline styles only (px and hex; no classes, `var()`, `em`/`rem` sizes or `margin`); nothing under 24px; the deck declares the three `faces` from the README. Keep the tracker, title, source line and footer exactly where they are and change the words; footer left = engagement · deliverable · date, right = classification · page. Speaker notes go in the closing `<aside>`.

## Markup

```html
<section id="governing-thought" style="background:#0F6E6A;color:#FAFAF7;font-family:Inter, Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:40px">
<p style="position:absolute;left:128px;top:64px;width:1664px;font-size:24px;line-height:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#DCEFEC">Governing thought</p>
<div style="flex:1"></div>
<p style="font-family:'Source Serif 4', Georgia, serif;font-size:96px;line-height:104px;font-weight:500;letter-spacing:-1px;color:#FAFAF7;width:1600px">The CRA turns product cybersecurity into a licence to sell in the EU.</p>
<div style="width:160px;height:4px;background:#DCEFEC"></div>
<p style="font-size:32px;line-height:44px;color:#DCEFEC;width:1400px">Example Group can be ready by 11 Dec 2027, but only if it secures third-party assessment capacity and builds shared compliance infrastructure in the next two quarters.</p>
<div style="flex:1"></div>
<div style="position:absolute;left:128px;bottom:64px;width:1664px;display:flex;flex-direction:row;justify-content:space-between;border-top:1px solid #2E9C93;padding:16px 0px 0px 0px">
<p style="font-size:24px;line-height:32px;color:#DCEFEC">Project Rampart · Board briefing · 19 Nov 2026</p>
<p style="font-size:24px;line-height:32px;color:#DCEFEC">Illustrative · <b>2</b></p>
</div>
<aside>The one statement slide in the deck. Read the first line aloud and let it stand.</aside>
</section>
```
