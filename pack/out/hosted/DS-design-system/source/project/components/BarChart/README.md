# BarChart

Bar conventions: sorted horizontal bars with one focus bar, a 100% stacked bar with a brace for the gated share, and clustered columns for scenarios — all directly labelled.

**Horizontal bars** (default; long labels, rankings)
- Sort descending unless the categories have a natural order. Labels right-aligned against the bars; values at the bar ends, 600, tabular.
- Context bars `viz-6`; the bar the title names `viz-1` teal — or `signal` if it is the binding constraint, as in the preview. Its label turns bold.
- 20px bars with 8px gaps on the web; 32px with 12px on slides. Start at zero; no axis line needed when every bar is labelled.

**Stacked 100% bar** (composition)
- Segments in a meaningful order (here Default, then Class I, then Class II), coloured `viz-6` for the part outside the message and `viz-1`, `viz-2` for the parts in it. Labels inside if they fit (white on `viz-1`/`viz-2` in light theme; `ink-900` on `viz-3`, `viz-4`, `viz-6`), otherwise beneath.
- A brace (2px `text-primary` rule with a bold label) groups the segments the title talks about.

**Clustered columns** (a few categories × two series)
- At most two series and five categories; series in `viz-1` (focus) and `viz-2`; values above the columns; a legend only because two series share each category.
- Never dual axes; never 3D; never stacked and clustered in one chart.

**You provide** categories, values, units, the focus category or series, the source.

**Web** (horizontal)
```html
<div class="adv-bars">
  <span class="adv-bars__label">Art 14 reporting</span>
  <div class="adv-bars__track"><div class="adv-bars__bar" style="width:72%"></div><span class="adv-bars__value">72</span></div>
  <span class="adv-bars__label adv-bars__label--focus">Conformity and access</span>
  <div class="adv-bars__track"><div class="adv-bars__bar adv-bars__bar--constraint" style="width:16%"></div><span class="adv-bars__value adv-bars__value--constraint">16</span></div>
</div>
```
Fills for any series: `adv-fill-viz-1` … `adv-fill-viz-6` (each sets a readable label colour).

**Slides** — SlideChart carries a paste-ready ten-bar chart built from painted divs (8px per point).
