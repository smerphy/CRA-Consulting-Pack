# HeatmapCell

A maturity cell coloured by level 0–4 with its value always printed in it; cells assemble into the readiness heatmap (families × domains).

**Colour by the level reached** — the value rounded down — so a cell shows the target colour only when it meets the target:
| Level | Name | Fill | Number |
|---|---|---|---|
| 0 (0.00–0.99) | Not started | `heat-0` `#B42318` | white (6.6:1) |
| 1 (1.00–1.99) | Initial | `heat-1` `#E07A5F` | `ink-900` (5.9:1) |
| 2 (2.00–2.99) | Defined | `heat-2` `#E9C46A` | `ink-900` (10.5:1) |
| 3 (3.00–3.99) | Implemented — target | `heat-3` `#7FB8A4` | `ink-900` (7.7:1) |
| 4 (4.00) | Assured | `heat-4` `#0F6E6A` | white (6.1:1) |

**Rules**
- Print the value in every cell, at the source's precision (averages 2 dp: 1.75; single answers: 2). Never colour without the number.
- Rows are product families (or BUs), columns are domains in the diagnostic's order; a bold portfolio-average row closes the table above a 2px rule; a right-hand index column (%) in `text-primary`, uncoloured.
- Always show the legend with the level names and mark the target level.
- The heat palette is for maturity only; never reuse it for RAG status or categories.
- One heatmap per exhibit; the action title names the pattern ("Documentation and conformity are red across every family").

**You provide** rows, columns, values, the target level, the index column, the source.

**Web**
```html
<span class="adv-heat adv-heat--1">1.75</span>            <!-- standalone -->
<td class="adv-heat adv-heat--0">0.25</td>               <!-- inside table.adv-heatmap -->
```

**Slides** — slide tables cannot colour cells, so build a grid of `<p>` cells (one element each keeps a 13 × 10 heatmap under the 200-element limit):
```html
<div style="display:grid;grid-template-columns:320px repeat(10, 1fr);gap:4px">
<p style="font-size:24px;line-height:32px;color:#0E1A2B">L2 Smart Lock</p>
<p style="background:#E07A5F;color:#0E1A2B;font-size:24px;line-height:32px;font-weight:600;text-align:center;border-radius:2px">1.75</p>
<p style="background:#B42318;color:#FFFFFF;font-size:24px;line-height:32px;font-weight:600;text-align:center;border-radius:2px">0.25</p>
</div>
```
At 32px rows plus 4px gaps, 13 families and a header fit under a two-line title.

**Spreadsheets** — the same fills via conditional formatting on the floor of the value; keep the numbers visible.
