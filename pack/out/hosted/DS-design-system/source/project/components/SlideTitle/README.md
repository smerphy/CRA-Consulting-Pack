# SlideTitle

The cover slide: the deliverable's title as a promise, on an `ink-900` ground, with the wordmark and client logo slot in the top margin.

**Use for** the first slide of every deck. One per deck.

**Anatomy**
- Top margin: `ADVISORY` wordmark top-left (Source Serif 4, 28px, 600, uppercase, 8px tracking, `paper`); client logo slot top-right (320 × 96, 1px dashed `#6B7A90` — 4:1 on `ink-900` — radius 4px). Replace the slot's `<p>` with the client's `<img>` when supplied; never leave "Client logo" in a delivered deck — delete the slot instead.
- A 160 × 4 `accent-400` rule, then the eyebrow (programme · deliverable, 24px, 600, 3px tracking, `accent-400`).
- Title: Source Serif 4, 96px / 104px, 500, `paper`, max two lines. Write it as the promise of the deck ("Keeping our EU market open"), not a topic ("CRA update").
- Subtitle: Inter 32px / 44px, `ink-300`, one sentence, max two lines.
- Footer: client (illustrative) · meeting and date · "Prepared by [Advisor]" left; classification right. Hairline `ink-700`.

**You provide** eyebrow, title, subtitle, meeting and date, classification label, optional client logo.

**Frame rules (every master)** — 1920 × 1080 canvas; `padding:128px 128px 160px`; inline styles only (px and hex; no classes, `var()`, `em`/`rem` sizes or `margin`); nothing under 24px; the deck declares the three `faces` from the README. Keep the tracker, title, source line and footer exactly where they are and change the words; footer left = engagement · deliverable · date, right = classification · page. Speaker notes go in the closing `<aside>`.

## Markup

```html
<section id="cover" style="background:#0E1A2B;color:#FAFAF7;font-family:Inter, Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:32px">
<p style="position:absolute;left:128px;top:64px;width:640px;font-family:'Source Serif 4', Georgia, serif;font-size:28px;line-height:32px;font-weight:600;letter-spacing:8px;text-transform:uppercase;color:#FAFAF7">Advisory</p>
<div style="position:absolute;left:1472px;top:48px;width:320px;height:96px;display:flex;align-items:center;justify-content:center;border:1px dashed #6B7A90;border-radius:4px">
<p style="font-size:24px;line-height:32px;color:#A3AFC0">Client logo</p>
</div>
<div style="flex:1"></div>
<div style="width:160px;height:4px;background:#2E9C93"></div>
<p style="font-size:24px;line-height:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#2E9C93">Project Rampart · Board briefing</p>
<h1 style="font-family:'Source Serif 4', Georgia, serif;font-size:96px;line-height:104px;font-weight:500;letter-spacing:-1px;color:#FAFAF7;width:1400px">Keeping our EU market open</h1>
<p style="font-size:32px;line-height:44px;color:#C5CDD8;width:1240px">What the Cyber Resilience Act requires of Example Group, what readiness costs, and five decisions for the board</p>
<div style="flex:1"></div>
<div style="position:absolute;left:128px;bottom:64px;width:1664px;display:flex;flex-direction:row;justify-content:space-between;border-top:1px solid #26364D;padding:16px 0px 0px 0px">
<p style="font-size:24px;line-height:32px;color:#A3AFC0">Example Group (illustrative) · Board meeting, 19 Nov 2026 · Prepared by [Advisor]</p>
<p style="font-size:24px;line-height:32px;color:#A3AFC0">Illustrative</p>
</div>
<aside>Open with the governing thought in one sentence: the CRA turns product cybersecurity into a licence to sell in the EU, and the board decides five things today.</aside>
</section>
```
