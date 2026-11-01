# KpiTile

One indicator in one tile: label with ID, value, target, trend, RAG pill and source — the unit of every dashboard and SteerCo KPI page.

**Anatomy** (top to bottom)
1. Label: `eyebrow` style in `text-muted`, preceded by the KPI ID in `id` style (mono). Name the measure, not the goal.
2. RAG pill, top-right, with its word.
3. Value: `kpi-value` (Inter 32px 600, tabular), `text-primary`. Add the base in `<small>` ("38% 9 / 24"). Format per the number rules (EUR 0.41m, 9h 40m, 11 / 13).
4. Target: `body-small`, with its date ("Target 100% by 31 Mar 2027").
5. Trend: `body-small` `text-muted`, an arrow (↑ ↓ →) and words ("Up from 21%", "Baseline", "First drill"). Trend is never coloured — direction is not judgement; the pill carries the judgement.
6. Source line after a hairline: `source-line`, with date and "Illustrative".

**Focus** — `adv-kpi--focus` turns the value `text-emphasis` teal. Use it on the one tile the page title talks about.

**You provide** ID, label, value (and base), target with date, trend words, RAG, source.

**Web**
```html
<article class="adv-kpi">
  <div class="adv-kpi__head">
    <p class="eyebrow adv-kpi__label"><span class="id">K07</span>Releases with signed SBOM</p>
    <span class="adv-rag adv-rag--red">Red</span>
  </div>
  <p class="kpi-value adv-kpi__value">38% <small>9 / 24</small></p>
  <p class="body-small adv-kpi__target">Target 100% by 31 Mar 2027</p>
  <p class="body-small adv-kpi__trend">↑ Up from 21%</p>
  <p class="source-line adv-kpi__source">Source: Build pipeline, last 30 days; Illustrative</p>
</article>
```
Lay tiles in `adv-grid` (auto-fit, min 240px): four across at 1200px, one per row on phones.

**Slides** — four tiles across the 1664px content width (386px each, 40px gaps):
```html
<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#FFFFFF;border:1px solid #C5CDD8;border-radius:4px;padding:32px">
<p style="font-size:24px;line-height:32px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#56667E">K07 · Signed SBOMs</p>
<p style="font-size:64px;line-height:72px;font-weight:600;letter-spacing:-1px;color:#0E1A2B;font-variant-numeric:tabular-nums">38%</p>
<p style="font-size:24px;line-height:32px;color:#26364D">Target 100% by 31 Mar 2027</p>
<p style="align-self:start;background:#B42318;color:#FFFFFF;font-size:24px;line-height:32px;font-weight:600;padding:4px 20px;border-radius:999px">Red</p>
</div>
```
Put the source for the whole row in the slide's source line.

**Don't** add sparklines without a time series, colour the value by status, or show a KPI without a target.
