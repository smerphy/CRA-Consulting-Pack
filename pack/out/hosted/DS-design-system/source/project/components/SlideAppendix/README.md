# SlideAppendix

The reference slide: still an action title, but the body is a dense, sourced table that readers consult rather than watch.

**Use for** detail behind a main-deck claim (KPI definitions, cost lines, fact bases). Number appendix pages A1, A2 … and put "Appendix · A2 · topic" in the tracker in `ink-500` (not teal) so readers see they have left the storyline.

**Anatomy**
- Table: Inter 24px / 32px (the floor), `ink-700`, `border:1px solid #C5CDD8` (hairline rules). Header row `background:#EEF1F5`, header cells 600 `ink-900`. Set `width:N%` on every header cell.
- Numbers right-aligned (`text-align:right` on every cell of the column), tabular, units in the header.
- Status columns: the word, coloured `rag-red` `#B42318`, `rag-amber` `#B54708` or `rag-green` `#027A48`; Grey as `ink-500` text. Slide tables cannot hold pills.
- Totals: a final row with `background:#EEF1F5` and the totals in `<b>`.
- Capacity: about 8 rows of one line under a two-line title. More rows: split across A2, A3 and say so in the source line.

**You provide** title, columns, rows, source, appendix number.

**Frame rules (every master)** — 1920 × 1080 canvas; `padding:128px 128px 160px`; inline styles only (px and hex; no classes, `var()`, `em`/`rem` sizes or `margin`); nothing under 24px; the deck declares the three `faces` from the README. Keep the tracker, title, source line and footer exactly where they are and change the words; footer left = engagement · deliverable · date, right = classification · page. Speaker notes go in the closing `<aside>`.

## Markup

```html
<section id="appendix-kpis" style="background:#FAFAF7;color:#26364D;font-family:Inter, Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:40px">
<p style="position:absolute;left:128px;top:64px;width:1664px;font-size:24px;line-height:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#56667E">Appendix · A2 · KPI detail</p>
<h2 style="font-family:'Source Serif 4', Georgia, serif;font-size:56px;line-height:64px;font-weight:500;letter-spacing:-0.5px;color:#0E1A2B">Signed SBOMs are the only Red KPI; all three reporting KPIs are Green</h2>
<table style="font-size:24px;line-height:32px;color:#26364D;border:1px solid #C5CDD8">
<tr style="background:#EEF1F5"><th style="width:7%;font-weight:600;color:#0E1A2B">ID</th><th style="width:37%;font-weight:600;color:#0E1A2B">KPI</th><th style="width:15%;font-weight:600;color:#0E1A2B;text-align:right">Value</th><th style="width:29%;font-weight:600;color:#0E1A2B">Target</th><th style="width:12%;font-weight:600;color:#0E1A2B">RAG</th></tr>
<tr><td>K01</td><td>Portfolio readiness index</td><td style="text-align:right">44%</td><td>70% by Jun 2027; 90% by Nov 2027</td><td style="color:#B54708">Amber</td></tr>
<tr><td>K02</td><td>Families with final scope and class decision</td><td style="text-align:right">11 / 13</td><td>13 / 13 by 18 Dec 2026</td><td style="color:#B54708">Amber</td></tr>
<tr><td>K03</td><td>Class I/II families with route and notified-body plan</td><td style="text-align:right">5 / 7</td><td>7 / 7 by 19 Nov 2026</td><td style="color:#B54708">Amber</td></tr>
<tr><td>K04</td><td>SRP Assigned Representatives registered</td><td style="text-align:right">3</td><td>≥ 2 at all times</td><td style="color:#027A48">Green</td></tr>
<tr><td>K05</td><td>Art 14 drill: time to early warning</td><td style="text-align:right">9h 40m</td><td>&lt; 24h incl. weekends</td><td style="color:#027A48">Green</td></tr>
<tr><td>K06</td><td>Art 14 cases assessed (reportable / not reportable)</td><td style="text-align:right">0 / 4</td><td>100% decided with UTC timeline</td><td style="color:#027A48">Green</td></tr>
<tr><td>K07</td><td>Releases with signed SBOM (last 30 days)</td><td style="text-align:right">38% (9 / 24)</td><td>100% by 31 Mar 2027</td><td style="color:#B42318">Red</td></tr>
</table>
<div style="flex:1"></div>
<p style="font-size:24px;line-height:32px;color:#56667E">Source: Programme KPI register, SteerCo #1, as at 30 Oct 2026; K08–K12 on A3; Illustrative</p>
<div style="position:absolute;left:128px;bottom:64px;width:1664px;display:flex;flex-direction:row;justify-content:space-between;border-top:1px solid #C5CDD8;padding:16px 0px 0px 0px">
<p style="font-size:24px;line-height:32px;color:#56667E">Project Rampart · Board briefing · 19 Nov 2026</p>
<p style="font-size:24px;line-height:32px;color:#56667E">Illustrative · <b>A2</b></p>
</div>
<aside>Reference only; not presented. K06 reads reportable / not reportable.</aside>
</section>
```
