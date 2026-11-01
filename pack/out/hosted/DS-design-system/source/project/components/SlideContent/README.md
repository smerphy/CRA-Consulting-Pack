# SlideContent

The base master every content slide starts from: tracker label, action title, one body zone, source line and footer, in fixed positions.

**Use for** any slide that makes one argument in words, optionally with a Key insight panel. All other content masters are this master with a different body.

**Anatomy (1920 × 1080)**
| Zone | Spec |
|---|---|
| Tracker | pinned `top:64px; left:128px`; Inter 24px / 32px, 600, 3px tracking, uppercase, `accent-700`. Write "01 · Reporting is already law" (section number · section name); the style uppercases it. |
| Action title | first flow child at y 128; Source Serif 4 56px / 64px, 500, `ink-900`, −0.5px tracking; one sentence, the so-what, ≤ ~15 words, max two lines, no full stop. Keep dates and amounts on one line with non-breaking spaces (`11&#160;Dec&#160;2027`, `EUR&#160;9.3m`). |
| Body | `flex:1` row, 48px under the title. Text: Inter 28px / 40px, `ink-700`; ≤ 5 bullets, ≤ 2 lines each; lead each bullet with a bold phrase. Key insight panel: `accent-100` ground, 40px padding, radius 4px, `align-self:start` so it hugs its text, label 24px `accent-700` uppercase. |
| Source line | last flow child, ends at y 920; Inter 24px / 32px, `ink-500`; one line (≈ 125 characters max). "Source: …; Illustrative". |
| Footer | pinned `bottom:64px`, 1px `ink-300` top rule, 16px gap; engagement · deliverable · date left; classification · **page** right; Inter 24px `ink-500`. |

Budget: the body zone is 536px tall under a two-line title, 600px under a one-line title. If it does not fit, split the slide; never shrink type below 24px.

**You provide** tracker text, action title, body, source line, footer text, page number.

**Frame rules (every master)** — 1920 × 1080 canvas; `padding:128px 128px 160px`; inline styles only (px and hex; no classes, `var()`, `em`/`rem` sizes or `margin`); nothing under 24px; the deck declares the three `faces` from the README. Keep the tracker, title, source line and footer exactly where they are and change the words; footer left = engagement · deliverable · date, right = classification · page. Speaker notes go in the closing `<aside>`.

## Markup

```html
<section id="reporting-law" style="background:#FAFAF7;color:#26364D;font-family:Inter, Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:48px">
<p style="position:absolute;left:128px;top:64px;width:1664px;font-size:24px;line-height:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#0A5753">01 · Reporting is already law</p>
<h2 style="font-family:'Source Serif 4', Georgia, serif;font-size:56px;line-height:64px;font-weight:500;letter-spacing:-0.5px;color:#0E1A2B">Every in-scope product is already on a 24-hour reporting clock, legacy lines included</h2>
<div style="flex:1;display:flex;flex-direction:row;gap:40px">
<ul style="flex:2;font-size:28px;line-height:40px;color:#26364D">
<li><b>Since 11 Sep 2026.</b> Article 14 applies to every in-scope product, including those placed on the market before 11 Dec 2027.</li>
<li><b>24 hours, 72 hours, 14 days.</b> Early warning, notification and final report for an actively exploited vulnerability.</li>
<li><b>One route.</b> Reports go through ENISA’s Single Reporting Platform to Germany’s coordinator CSIRT.</li>
<li><b>Tested once.</b> The first drill filed its early warning in 9h 40m on 22 Oct 2026.</li>
</ul>
<div style="flex:1;align-self:start;display:flex;flex-direction:column;gap:16px;background:#DCEFEC;padding:40px;border-radius:4px">
<p style="font-size:24px;line-height:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#0A5753">Key insight</p>
<p style="font-size:28px;line-height:40px;color:#0E1A2B">Reporting is the most ready domain at 72%, but two people hold most PSIRT knowledge. Fund the PSIRT lead and analyst now.</p>
</div>
</div>
<p style="font-size:24px;line-height:32px;color:#56667E">Source: CRA Arts 14 and 71; ENISA; drill record (22 Oct 2026); readiness diagnostic (28 Oct 2026); Illustrative</p>
<div style="position:absolute;left:128px;bottom:64px;width:1664px;display:flex;flex-direction:row;justify-content:space-between;border-top:1px solid #C5CDD8;padding:16px 0px 0px 0px">
<p style="font-size:24px;line-height:32px;color:#56667E">Project Rampart · Board briefing · 19 Nov 2026</p>
<p style="font-size:24px;line-height:32px;color:#56667E">Illustrative · <b>4</b></p>
</div>
<aside>One message: reporting is live today. Cover the clock, the route and the drill result, then hand over to market access.</aside>
</section>
```
