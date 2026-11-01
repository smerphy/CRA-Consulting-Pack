# SlideTwoColumn

Two parallel columns under one action title: now vs later, current vs target, option A vs option B.

**Use for** comparisons with the same structure on both sides. If the columns are not parallel, use SlideContent.

**Anatomy**
- Columns: two `flex:1` columns with a 40px gutter (each 812px = 6 grid columns).
- Column head: 4px top rule, 24px gap, then a label (24px, 600, 3px tracking, uppercase) and a heading (Inter 32px / 44px, 600, `ink-900`).
- The column the title is about takes the `accent-600` rule and `accent-700` label; the other takes `ink-900` and `ink-500`. Never two teal rules.
- Bullets: Inter 28px / 40px, `ink-700`, the same number of bullets on both sides where possible.

**You provide** title, two labels, two headings, bullets, source line.

**Frame rules (every master)** — 1920 × 1080 canvas; `padding:128px 128px 160px`; inline styles only (px and hex; no classes, `var()`, `em`/`rem` sizes or `margin`); nothing under 24px; the deck declares the three `faces` from the README. Keep the tracker, title, source line and footer exactly where they are and change the words; footer left = engagement · deliverable · date, right = classification · page. Speaker notes go in the closing `<aside>`.

## Markup

```html
<section id="now-and-later" style="background:#FAFAF7;color:#26364D;font-family:Inter, Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:48px">
<p style="position:absolute;left:128px;top:64px;width:1664px;font-size:24px;line-height:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#0A5753">01 · Reporting is already law</p>
<h2 style="font-family:'Source Serif 4', Georgia, serif;font-size:56px;line-height:64px;font-weight:500;letter-spacing:-0.5px;color:#0E1A2B">Reporting applies now; every other obligation lands on 11&#160;Dec&#160;2027</h2>
<div style="flex:1;display:flex;flex-direction:row;gap:40px">
<div style="flex:1;display:flex;flex-direction:column;gap:24px;border-top:4px solid #0F6E6A;padding:24px 0px 0px 0px">
<p style="font-size:24px;line-height:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#0A5753">Already law · since 11 Sep 2026</p>
<p style="font-size:32px;line-height:44px;font-weight:600;color:#0E1A2B">Article 14 reporting, for every in-scope product</p>
<ul style="font-size:28px;line-height:40px;color:#26364D">
<li>Early warning within 24 hours of awareness</li>
<li>Notification within 72 hours</li>
<li>Final report 14 days after a fix, or 1 month after notification for an incident</li>
<li>Covers products already on the market</li>
</ul>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:24px;border-top:4px solid #0E1A2B;padding:24px 0px 0px 0px">
<p style="font-size:24px;line-height:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#56667E">From 11 Dec 2027</p>
<p style="font-size:32px;line-height:44px;font-weight:600;color:#0E1A2B">Everything else, per product and per version</p>
<ul style="font-size:28px;line-height:40px;color:#26364D">
<li>Annex I essential requirements met and evidenced</li>
<li>Class I needs a cited standard or a notified body; Class II always third-party</li>
<li>Technical file and declaration kept for 10 years</li>
<li>Security updates for the support period, normally at least five years</li>
</ul>
</div>
</div>
<p style="font-size:24px;line-height:32px;color:#56667E">Source: Regulation (EU) 2024/2847, Arts 13, 14, 32 and 71; knowledge base, facts as at 30 Oct 2026</p>
<div style="position:absolute;left:128px;bottom:64px;width:1664px;display:flex;flex-direction:row;justify-content:space-between;border-top:1px solid #C5CDD8;padding:16px 0px 0px 0px">
<p style="font-size:24px;line-height:32px;color:#56667E">Project Rampart · Board briefing · 19 Nov 2026</p>
<p style="font-size:24px;line-height:32px;color:#56667E">Illustrative · <b>5</b></p>
</div>
<aside>Left is today; right is 11 Dec 2027. The teal rule marks what is already law.</aside>
</section>
```
