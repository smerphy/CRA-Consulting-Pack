# SlideDivider

The section divider: a large serif section number, the section's message as a sentence, and a four-step tracker showing where the audience is.

**Use for** the start of each storyline section (pillar). Not for decks under ten slides.

**Anatomy**
- Top margin: "Section 2 of 4" (24px label, `#A3AFC0`).
- Numeral: Source Serif 4, 200px, 500, `accent-400`. Section numerals are display type, so they are the one place numbers are set in the serif.
- Section message: Source Serif 4, 96px / 104px, `paper` — a sentence that states the pillar ("Market access is the binding constraint"), max two lines.
- Lead: Inter 32px / 44px, `ink-300`, one sentence with the evidence.
- Tracker row: one cell per section, 4px top rule (`accent-400` and `paper` 600 text for the current section; `ink-700` rule and `#A3AFC0` text for the others). Keep the labels identical on every divider.
- `data-section` on the `<section>` carries the section's one-sentence description for the Slides outline.

**You provide** section number, message, lead, the list of section labels, which one is current.

**Frame rules (every master)** — 1920 × 1080 canvas; `padding:128px 128px 160px`; inline styles only (px and hex; no classes, `var()`, `em`/`rem` sizes or `margin`); nothing under 24px; the deck declares the three `faces` from the README. Keep the tracker, title, source line and footer exactly where they are and change the words; footer left = engagement · deliverable · date, right = classification · page. Speaker notes go in the closing `<aside>`.

## Markup

```html
<section id="section-2" data-section="Market access is the binding constraint" style="background:#0E1A2B;color:#FAFAF7;font-family:Inter, Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:32px">
<p style="position:absolute;left:128px;top:64px;width:1664px;font-size:24px;line-height:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#A3AFC0">Section 2 of 4</p>
<div style="flex:1"></div>
<p style="font-family:'Source Serif 4', Georgia, serif;font-size:200px;line-height:200px;font-weight:500;color:#2E9C93">02</p>
<h2 style="font-family:'Source Serif 4', Georgia, serif;font-size:96px;line-height:104px;font-weight:500;letter-spacing:-1px;color:#FAFAF7;width:1500px">Market access is the binding constraint</h2>
<p style="font-size:32px;line-height:44px;color:#C5CDD8;width:1300px">Seven of thirteen families need a notified body or a cited harmonised standard; neither exists today.</p>
<div style="flex:1"></div>
<div style="display:flex;flex-direction:row;gap:40px">
<div style="flex:1;border-top:4px solid #26364D;padding:16px 0px 0px 0px"><p style="font-size:24px;line-height:32px;color:#A3AFC0">01 Reporting is already law</p></div>
<div style="flex:1;border-top:4px solid #2E9C93;padding:16px 0px 0px 0px"><p style="font-size:24px;line-height:32px;font-weight:600;color:#FAFAF7">02 Market access</p></div>
<div style="flex:1;border-top:4px solid #26364D;padding:16px 0px 0px 0px"><p style="font-size:24px;line-height:32px;color:#A3AFC0">03 Evidence system</p></div>
<div style="flex:1;border-top:4px solid #26364D;padding:16px 0px 0px 0px"><p style="font-size:24px;line-height:32px;color:#A3AFC0">04 Programme and decisions</p></div>
</div>
<div style="position:absolute;left:128px;bottom:64px;width:1664px;display:flex;flex-direction:row;justify-content:space-between;border-top:1px solid #26364D;padding:16px 0px 0px 0px">
<p style="font-size:24px;line-height:32px;color:#A3AFC0">Project Rampart · Board briefing · 19 Nov 2026</p>
<p style="font-size:24px;line-height:32px;color:#A3AFC0">Illustrative · <b>6</b></p>
</div>
<aside>Pause here. One sentence: reporting is under control; market access is what can stop sales on 11 Dec 2027.</aside>
</section>
```
