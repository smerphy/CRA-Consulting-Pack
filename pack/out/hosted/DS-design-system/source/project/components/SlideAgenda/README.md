# SlideAgenda

The agenda as the storyline: one row per section, each with a serif numeral, the section's message and its proof point.

**Use for** slide 3 of a board or SteerCo deck, and again before each section as a tracker. Four to six rows.

**Anatomy**
- Title: an action title that states what the meeting achieves ("Four messages lead to five decisions …"), never just "Agenda" — the word Agenda goes in the tracker.
- Rows: 1px `ink-300` rule above each row and below the last; 24px vertical padding; numeral Source Serif 4 56px `accent-600` in a 102px column; message Inter 32px / 40px 600 `ink-900`; proof line 24px `ink-500`.
- Tracker variant (before a section): give the current row `background:#DCEFEC` and keep it teal; set the other rows' numerals to `#56667E`. Keep row text identical to the opening agenda.
- No source line unless the rows carry numbers that need one.

**You provide** the title, and per row a number, a message and one proof line.

**Frame rules (every master)** — 1920 × 1080 canvas; `padding:128px 128px 160px`; inline styles only (px and hex; no classes, `var()`, `em`/`rem` sizes or `margin`); nothing under 24px; the deck declares the three `faces` from the README. Keep the tracker, title, source line and footer exactly where they are and change the words; footer left = engagement · deliverable · date, right = classification · page. Speaker notes go in the closing `<aside>`.

## Markup

```html
<section id="agenda" style="background:#FAFAF7;color:#26364D;font-family:Inter, Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:48px">
<p style="position:absolute;left:128px;top:64px;width:1664px;font-size:24px;line-height:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#0A5753">Agenda</p>
<h2 style="font-family:'Source Serif 4', Georgia, serif;font-size:56px;line-height:64px;font-weight:500;letter-spacing:-0.5px;color:#0E1A2B">Four messages lead to five decisions for the board on 19&#160;Nov&#160;2026</h2>
<div style="display:flex;flex-direction:column">
<div style="display:flex;flex-direction:row;align-items:center;gap:40px;border-top:1px solid #C5CDD8;padding:24px 0px">
<p style="width:102px;font-family:'Source Serif 4', Georgia, serif;font-size:56px;line-height:64px;font-weight:500;color:#0F6E6A">01</p>
<div style="flex:1;display:flex;flex-direction:column;gap:4px"><p style="font-size:32px;line-height:40px;font-weight:600;color:#0E1A2B">Reporting is already law</p><p style="font-size:24px;line-height:32px;color:#56667E">Every in-scope product is on a 24-hour clock today</p></div>
</div>
<div style="display:flex;flex-direction:row;align-items:center;gap:40px;border-top:1px solid #C5CDD8;padding:24px 0px">
<p style="width:102px;font-family:'Source Serif 4', Georgia, serif;font-size:56px;line-height:64px;font-weight:500;color:#0F6E6A">02</p>
<div style="flex:1;display:flex;flex-direction:column;gap:4px"><p style="font-size:32px;line-height:40px;font-weight:600;color:#0E1A2B">Market access is the binding constraint</p><p style="font-size:24px;line-height:32px;color:#56667E">EUR 468m of EU revenue needs a notified body that does not yet exist</p></div>
</div>
<div style="display:flex;flex-direction:row;align-items:center;gap:40px;border-top:1px solid #C5CDD8;padding:24px 0px">
<p style="width:102px;font-family:'Source Serif 4', Georgia, serif;font-size:56px;line-height:64px;font-weight:500;color:#0F6E6A">03</p>
<div style="flex:1;display:flex;flex-direction:column;gap:4px"><p style="font-size:32px;line-height:40px;font-weight:600;color:#0E1A2B">Compliance is an evidence system, not a project</p><p style="font-size:24px;line-height:32px;color:#56667E">Proof per product version, kept for ten years</p></div>
</div>
<div style="display:flex;flex-direction:row;align-items:center;gap:40px;border-top:1px solid #C5CDD8;border-bottom:1px solid #C5CDD8;padding:24px 0px">
<p style="width:102px;font-family:'Source Serif 4', Georgia, serif;font-size:56px;line-height:64px;font-weight:500;color:#0F6E6A">04</p>
<div style="flex:1;display:flex;flex-direction:column;gap:4px"><p style="font-size:32px;line-height:40px;font-weight:600;color:#0E1A2B">Programme, cost and decisions</p><p style="font-size:24px;line-height:32px;color:#56667E">EUR 9.3m to Dec 2027, EUR 1.8m a year to run, five decisions today</p></div>
</div>
</div>
<div style="flex:1"></div>
<div style="position:absolute;left:128px;bottom:64px;width:1664px;display:flex;flex-direction:row;justify-content:space-between;border-top:1px solid #C5CDD8;padding:16px 0px 0px 0px">
<p style="font-size:24px;line-height:32px;color:#56667E">Project Rampart · Board briefing · 19 Nov 2026</p>
<p style="font-size:24px;line-height:32px;color:#56667E">Illustrative · <b>3</b></p>
</div>
<aside>Each row is one pillar of the storyline; the last row carries the ask.</aside>
</section>
```
