# LineChart

Line conventions: the focus series thick and teal, the comparator thinner in navy, end labels instead of a legend, hairline gridlines, and a teal today line.

**Rules**
- Use for one or two series over time. More than three lines: split into small multiples.
- Focus series (actuals, the client): 3px `viz-1`, round joins, a dot on the latest point with its value. Comparator (plan, benchmark): 2px `viz-2`. A third series, if any: 2px `viz-6`.
- Label each line at its end with name and latest value (`lbl`, 600); no legend box.
- Y axis: 4–6 gridlines in `rule`, tick labels `text-muted` with units in the axis title ("EUR m, cumulative"); start at zero for amounts. X axis: months or quarters, year at January.
- Today: 2px `action` line labelled "Today". Targets and thresholds: 1.5px dashed `text-primary` line labelled with value and date.
- Actuals stop at today; plans may run on. Do not draw forecast and actual in the same style.
- Accessibility: the `<svg>` has `role="img"` and an `aria-label` stating the message.

**You provide** the series (dates, values), which series is the focus, the unit, today, any target, the source.

**Web** — an inline SVG with classes from bundle.css:
```html
<svg class="adv-line-chart" viewBox="0 0 720 300" role="img" aria-label="Cumulative spend is EUR 0.41m against a plan of EUR 0.38m">
  <line class="grid" x1="56" y1="40" x2="680" y2="40"/>
  <polyline class="s-context" points="56,251 98,231 …"/>
  <circle class="pt-focus" cx="56" cy="250" r="5"/>
  <text class="lbl" x="684" y="44">Plan EUR 9.25m</text>
</svg>
```
Classes: `grid`, `axis`, `tick`, `s-focus`, `s-context`, `pt-focus`, `pt-context`, `lbl`, `lbl-focus`, `lbl-muted`, `today`, `target`.

**Slides** — draw lines in an `<svg aria-label>` with no `<text>` (fonts do not load inside slide SVGs) and pin 24px `<p>` labels over it; stroke 4px focus, 3px comparator at slide scale.
