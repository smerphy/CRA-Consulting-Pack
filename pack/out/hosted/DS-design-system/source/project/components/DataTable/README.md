# DataTable

The table style for every deliverable: hairline rules, no zebra striping, right-aligned tabular numbers, units in the header, bold totals.

**Rules**
- Header: `eyebrow`-sized (12px, 600, uppercase, tracked) in `text-muted`, with a 1px `text-primary` rule beneath.
- Rows: 14px / 20px `text-body`, 10px × 12px padding, 1px `rule` between rows. No zebra, no vertical rules, no cell fills except a highlighted row (`bg-emphasis`).
- Row headers (`<th scope="row">`): 500 weight, `text-primary`.
- Numbers: class `num` — right-aligned, tabular figures, no wrapping. Same precision down a column; units in the column header ("EUR k", "%"), never in cells. A dash (–) for not applicable, never 0.
- Subtotal: 600. Total: 700 with a 2px `text-primary` rule above. Contingency or memo rows: `muted`.
- Sort by the value the title talks about unless rows have a natural order. Wrap wide tables in `adv-table-wrap` (scrolls inside its box on phones).
- Status cells: RagPill (dot variant in long tables). IDs: `id` class (mono, muted).
- Always under an exhibit caption with a source line (ExhibitCaption).

**You provide** columns with units, rows, the sort, subtotal and total rows, the source.

**Web**
```html
<table class="adv-table">
  <thead><tr><th scope="col">Workstream</th><th scope="col" class="num">One-off</th><th scope="col" class="num">Run a year</th></tr></thead>
  <tbody>
    <tr><th scope="row">Secure engineering</th><td class="num">4,389</td><td class="num">660</td></tr>
    <tr class="subtotal"><th scope="row">Subtotal</th><td class="num">8,045</td><td class="num">1,844</td></tr>
    <tr class="total"><th scope="row">Total</th><td class="num">9,251</td><td class="num">1,844</td></tr>
  </tbody>
</table>
```
Row classes: `subtotal`, `total`, `highlight`, `muted`.

**Slides** — see SlideAppendix: 24px text, `border:1px solid #C5CDD8` (the Slides type rules every cell), header row `background:#EEF1F5`, `width:N%` on every header cell, `text-align:right` on numeric columns, totals in `<b>` on a `#EEF1F5` row.

**Docs** — a markdown table with the units in the header, numbers right-aligned (`---:`), totals in bold, caption above and source below.

**Spreadsheets** — header row `ink-900` fill with white bold text; thousands separators; totals bold with a top border.
