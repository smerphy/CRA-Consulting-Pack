# RiskMatrix

A 5 × 5 likelihood-by-impact grid with risk IDs placed as dark markers; zones are pale RAG tints so the IDs, not the colours, carry the reading.

**Scoring** — score = likelihood × impact, each 1–5. Zones: Low 1–4 (`rag-green-100`), Medium 5–11 (`rag-amber-100`), High 12–25 (`rag-red-100`). Keep these thresholds across the pack so ratings match the risk register.

**Anatomy**
- Likelihood on the vertical axis (5 at the top), impact on the horizontal (5 at the right); axis titles in `eyebrow` style, tick numbers in `text-muted`.
- Cells: 64px tall, 3px gaps, `radius-sm`.
- Markers: risk IDs (R01 …) in mono 12px on a `text-primary` capsule with `bg-page` text — the one place `radius-full` is used outside status. Several risks in one cell wrap.
- Trend (rising, falling) belongs in the register table beside the matrix, not on the marker.
- Legend under the grid with the three zones and their score ranges.
- `role="img"` with an `aria-label` that names the high risks.

**You provide** each risk's ID, likelihood and impact, and the register table it summarises.

**Web**
```html
<div class="adv-risk__cell adv-risk__cell--high"><span class="adv-risk__marker">R01</span></div>
```
Grid: 2 label columns + 5 cells per row, rows from likelihood 5 down to 1, then the impact ticks and title (see preview).

**Slides** — a grid of painted divs: `display:grid;grid-template-columns:repeat(5, 160px);gap:6px`; cells 104px tall with `background:#FEE4E2` (high), `#FEF0C7` (medium), `#D1FADF` (low); markers are `<p>` pills `background:#0E1A2B;color:#FAFAF7;font-size:24px;padding:0px 12px;border-radius:999px`. Put axis titles as 24px `<p>` labels.

**Don't** colour markers by rating (the zone already says it), use more than three zones, or plot risks without IDs.
