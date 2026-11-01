# MaturityRating

A maturity level 0–4 drawn as a Harvey ball (quarters filled) or four dots, always next to the number or level name.

**Use** in dense tables and one-pagers where a heatmap would be too loud: capability assessments, option comparisons, "how ready is each domain". In colour-coded grids use HeatmapCell instead; never mix both in one exhibit.

**Scale** (the readiness diagnostic's): 0 Not started · 1 Initial · 2 Defined · 3 Implemented (target) · 4 Assured. Averages (2.15) show the level reached — the value rounded down — and print the value beside the mark.

**Anatomy**
- Harvey ball: 18px circle (28px `--lg`), 1.5px ring and fill in `text-primary`; level n fills n quarters clockwise from 12 o'clock.
- Dots: four 10px dots; filled `text-primary`, empty 1.5px `rule-strong` ring.
- Monochrome by design: the mark shows quantity; RAG colours stay reserved for status.

**You provide** the level (0–4) or the average, and the label.

**Web**
```html
<span class="adv-harvey adv-harvey--3" role="img" aria-label="Level 3 of 4"></span>
<span class="adv-dots" role="img" aria-label="2 of 4"><span class="on"></span><span class="on"></span><span></span><span></span></span>
<span class="adv-rating"><span class="adv-harvey adv-harvey--2" aria-hidden="true"></span>Art 14 reporting · 2.15</span>
```

**Slides** — an inline SVG per level, 48px, beside a 24px label. Level 2 (half):
```html
<svg width="48" height="48" viewBox="0 0 48 48" aria-label="Level 2 of 4"><circle cx="24" cy="24" r="21" fill="none" stroke="#0E1A2B" stroke-width="3"/><path d="M24 24V3A21 21 0 0 1 24 45Z" fill="#0E1A2B"/></svg>
```
Level 1: `d="M24 24V3A21 21 0 0 1 45 24Z"`; level 3: `d="M24 24V3A21 21 0 1 1 3 24Z"`; level 4: a filled circle; level 0: the ring only.

**Don't** use half-quarters, colour the fill, or show a mark without its number in a data exhibit.
