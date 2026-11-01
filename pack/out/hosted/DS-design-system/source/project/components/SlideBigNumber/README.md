# SlideBigNumber

One number, set huge, completed by a sentence: the number and the sentence together are the action title.

**Use for** the two or three numbers the audience must remember (EUR 468m, 406 days, EUR 9.3m). Never two big numbers on one slide.

**Anatomy**
- Number: Inter 200px / 200px, 600, −6px tracking, tabular figures, `accent-600`. Use `signal` `#C2410C` only if the number is the binding constraint itself, and then nowhere else on the slide. Keep it to ≤ 9 characters.
- Sentence: Source Serif 4 56px / 64px, `ink-900`, starting lower-case where it completes the number ("of EU revenue needs …"), max two lines, no full stop.
- Support row: three facts after a 1px `ink-300` rule — value Inter 32px 600 `ink-900`, label 24px `ink-500`. They answer the obvious follow-up questions; they do not add new messages.
- Spacers above and below centre the block; the source line stays at the bottom.

**You provide** the number (formatted per the number rules), the sentence, three supporting facts, the source.

**Frame rules (every master)** — 1920 × 1080 canvas; `padding:128px 128px 160px`; inline styles only (px and hex; no classes, `var()`, `em`/`rem` sizes or `margin`); nothing under 24px; the deck declares the three `faces` from the README. Keep the tracker, title, source line and footer exactly where they are and change the words; footer left = engagement · deliverable · date, right = classification · page. Speaker notes go in the closing `<aside>`.

## Markup

```html
<section id="revenue-at-stake" style="background:#FAFAF7;color:#26364D;font-family:Inter, Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:32px">
<p style="position:absolute;left:128px;top:64px;width:1664px;font-size:24px;line-height:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#0A5753">02 · Market access</p>
<div style="flex:1"></div>
<p style="font-size:200px;line-height:200px;font-weight:600;letter-spacing:-6px;color:#0F6E6A;font-variant-numeric:tabular-nums">EUR 468m</p>
<h2 style="font-family:'Source Serif 4', Georgia, serif;font-size:56px;line-height:64px;font-weight:500;letter-spacing:-0.5px;color:#0E1A2B;width:1400px">of EU revenue needs a notified body to stay on sale after 11&#160;Dec&#160;2027</h2>
<div style="display:flex;flex-direction:row;gap:40px;border-top:1px solid #C5CDD8;padding:32px 0px 0px 0px">
<div style="flex:1;display:flex;flex-direction:column;gap:8px"><p style="font-size:32px;line-height:40px;font-weight:600;color:#0E1A2B;font-variant-numeric:tabular-nums">39%</p><p style="font-size:24px;line-height:32px;color:#56667E">of group revenue of EUR 1.2bn</p></div>
<div style="flex:1;display:flex;flex-direction:column;gap:8px"><p style="font-size:32px;line-height:40px;font-weight:600;color:#0E1A2B;font-variant-numeric:tabular-nums">7 of 13</p><p style="font-size:24px;line-height:32px;color:#56667E">product families are Class I or Class II</p></div>
<div style="flex:1;display:flex;flex-direction:column;gap:8px"><p style="font-size:32px;line-height:40px;font-weight:600;color:#0E1A2B;font-variant-numeric:tabular-nums">0</p><p style="font-size:24px;line-height:32px;color:#56667E">CRA notified bodies verifiably designated (checks to 8 Sep 2026)</p></div>
</div>
<div style="flex:1"></div>
<p style="font-size:24px;line-height:32px;color:#56667E">Source: Example Group portfolio and revenue data (illustrative); European Commission, NANDO checks to 8 Sep 2026</p>
<div style="position:absolute;left:128px;bottom:64px;width:1664px;display:flex;flex-direction:row;justify-content:space-between;border-top:1px solid #C5CDD8;padding:16px 0px 0px 0px">
<p style="font-size:24px;line-height:32px;color:#56667E">Project Rampart · Board briefing · 19 Nov 2026</p>
<p style="font-size:24px;line-height:32px;color:#56667E">Illustrative · <b>8</b></p>
</div>
<aside>Say the number, then the sentence, then stop. The three facts below answer the obvious questions.</aside>
</section>
```
