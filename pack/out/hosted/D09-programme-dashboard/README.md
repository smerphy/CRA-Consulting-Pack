# D09 Programme dashboard: export

Offline copy of the hosted dashboard **Project Rampart — Programme Dashboard**
(https://claude.ai/artifact/KbSnPXQmoZmjuEDroY8eP5), a claude.ai artifact made from the
Dashboard type. Exported 1 Nov 2026 from the live version (1793459187-3123). Example Group is a
fictional client and every client figure is illustrative.

## How the live dashboard is put together

The live artifact's own content is held in its shared database, not in published files. The
Dashboard type supplies the page shell, toolbar, Sources panel and the `dash` runtime
(`artifact-type/app.js`, `app.css`); those files belong to the type and are not exported here.

| Live database document | Exported as | What it is |
|---|---|---|
| `files/index.html` | `source/index.html` | The page: an HTML fragment the type mounts inside `<div id="dash-root">`. Every figure is a `data-draw` placeholder marked with `data-source` / `data-field` / `data-where`. |
| `files/rampart.css` | `source/rampart.css` | Page styles (classes prefixed `rp-`). Uses the type's theme tokens (`--color-*`, `--cds-*`). |
| `files/rampart.js` | `source/rampart.js` | Calculations (`dash.calc`) and drawings (`dash.draw`): every chart, table and number. Needs d3 v7 and the `dash` global. |
| `datasets/<id>` (21 documents) | `meta/datasets.json` | Each dataset's title, description, source, `updated` stamp and `fixed: true`. |
| Attached file each dataset points to (`/_blob/<id>`) | `data/<id>.json` (+ `data/<id>.csv`) | The rows the page reads. JSON is byte-for-byte the uploaded file; CSV is the same rows flattened (columns in first-seen order). |
| `dash/meta` | `meta/dash-meta.json` | Dashboard title. |
| `dash/look` | `meta/dash-look.json` | Theme the type applies: light and dark colours, chart palette, fonts, sizes and corners, from the Advisory Design System. |

All 21 datasets are attached files marked `fixed: true`: there are no live connector queries,
so nothing refreshes. Three further JSON uploads in the artifact's asset store are earlier
versions that no dataset references any more; they were not exported. Per-viewer documents
under `data/users/` (page checks and run logs) are runtime state, not content, and were not
exported.

### Calculations defined in `rampart.js`

These have no data file; the page computes them from the datasets above:
`kpi_rag_counts` (kpis), `ws_rag_counts` (workstreams), `milestone_status_counts` (milestones),
`nb_need` and `hbs_class_i` (families), `tasks_due` (mobilisation_plan, tasks ending by 30 Nov 2026),
`spend_variance` (spend), `budget_bars` (budget_workstreams + budget_totals).

## Datasets and where they come from in `pack/data/pack_data.json`

Every dataset was derived from the programme pack data (v1.0). Column names were reshaped for the
page (for example `name` to `workstream`, ISO date columns added), so rows match on content,
not on keys.

| Dataset | Rows | Source in pack_data.json |
|---|---|---|
| `programme_status` | 1 | `programme.overall_rag`, `overall_status`, `kickoff`; `meta` (issue date, SteerCo #1, board date, days to full application) |
| `kpis` | 12 | `kpis` (identical rows) |
| `workstreams` | 8 | `programme.workstreams` |
| `milestones` | 15 | `programme.milestones` |
| `phases` | 7 | `programme.phases` |
| `mobilisation_plan` | 30 | `programme.mobilisation_plan` |
| `risks` | 10 | `risks` |
| `issues` | 3 | `issues` |
| `decisions` | 9 | `decisions.steerco_1` + `decisions.board` (board asks shown as Proposed) |
| `families` | 13 | `client.product_families` + `diagnostic.family_readiness_index` |
| `client_profile` | 1 | `client` (+ `client.counts`, `exposure.fine_tiers[0]`) |
| `revenue_by_class` | 3 | `client.revenue_by_class_m`, `client.eu_revenue_by_class_m`, `client.counts` |
| `domains` | 10 | `diagnostic.domains`, `domain_average_level`, `domain_readiness_index` |
| `readiness_segments` | 7 | `diagnostic.bu_readiness_index`, `class_readiness_index`, `portfolio_readiness_index` |
| `readiness_plan` | 15 | `kpi_trajectories.readiness_index_plan` (+ Oct 2026 actual, targets) |
| `sbom_coverage` | 7 | `kpi_trajectories.sbom_coverage_plan_and_actual` |
| `spend` | 15 | `cost_model.monthly_plan` + `cost_model.actual_to_date` |
| `budget_totals` | 1 | `cost_model.base_totals`, `one_off_pct_of_revenue`, `run_pct_of_revenue`, `engineering_fte_years` |
| `budget_workstreams` | 8 | `cost_model.by_workstream` |
| `scenarios` | 3 | `cost_model.scenarios` (low, base, high totals) |
| `reg_facts` | 6 | `facts` F02, F03, F04, F07, F08, F15 (regulatory facts, verified to 30 Oct 2026; notified-body count checks to 8 Sep 2026) |

## Static snapshot

- `snapshot.png`: full page at 1360px wide, 2x pixel density, light theme.
- `D09 - Programme dashboard.pdf`: the same render as one tall PDF page.

These were rendered locally in headless Chromium from the exported `source/` and `data/` files.
The Dashboard type's runtime cannot run outside claude.ai, so the render used a minimal stand-in
for its documented `dash` API (data, calc, draw, onData, colors), d3 7.9.0, the Inter, Source
Serif 4 and JetBrains Mono fonts, and theme tokens taken from `meta/dash-look.json`. Every
figure, chart and table is drawn by the page's own `rampart.js` from the exported data; the
render reported no script errors and no unfilled values. What differs from the live page: the
type's toolbar and Sources panel are absent, tooltips and section links are not interactive,
and a few type tokens with no value in the look (chart grid, axis and muted grey) were
approximated from the design system.

## Viewing or rebuilding

To see the live dashboard, open the artifact link above. To rebuild it elsewhere, use
`data/*.csv` or `data/*.json` as the data and `source/` as the reference for layout, calculations
and chart design; the page code expects the Dashboard type's `dash` API and will not run on its
own in a browser.
