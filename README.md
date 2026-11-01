# CRA Readiness Programme Pack

White-label consulting pack for the EU Cyber Resilience Act (Regulation (EU) 2024/2847), populated with an illustrative fictional client (Example Group, "Project Rampart"). All client figures are illustrative. Regulatory facts are verified to 30 Oct 2026 (notified-body status to 8 Sep 2026). Not legal advice.

## Deliverables

| ID | Deliverable | Where it lives |
|---|---|---|
| D01 | Board briefing deck (22 slides) | `pack/out/hosted/D01-board-deck/` (PDF, PPTX, notes, source); published artifact |
| D02 | SteerCo pack (15 slides, monthly template) | `pack/out/hosted/D02-steerco-pack/`; published artifact |
| D03 | Engineering training deck (24 slides) | `pack/out/hosted/D03-training-deck/`; published artifact |
| D04 | Two one-pagers (CRA, Project Rampart) | `pack/out/hosted/D04-one-pagers/` (PDF, source); published artifact |
| D05 | Communications pack (9 tabs) | `pack/out/hosted/D05-communication-pack/` (Word, Markdown, PDF); published doc |
| D06 | Research report, State of CRA readiness 2026 | `pack/out/hosted/D06-research-report/`; published doc |
| D07 | Survey instruments (8 tabs) | `pack/out/hosted/D07-survey-instruments/`; published doc |
| D08 | Readiness diagnostic | `pack/out/diagnostic/index.html` and published artifact |
| D09 | Programme dashboard | `pack/out/hosted/D09-programme-dashboard/` (source, 21 datasets, PDF snapshot); published artifact |
| D10 | Business case and cost model | `pack/out/excel/` |
| D11 | Obligations register and programme tracker | `pack/out/excel/` |
| D13 | Product classifier (scope, class, conformity routes, SKU register) | `pack/out/classifier/index.html` and published artifact |
| D14 | Compliance templates kit (10 fill-in templates) | `pack/out/hosted/D14-compliance-templates-kit/`; published doc |
| D15 | Framework crosswalk (CRA vs NIS2, ISO 27001, IEC 62443, EN 18031, EN 303 645, NIST SSDF) | `pack/out/crosswalk/` (page + CSV), data `pack/data/crosswalk.json`, published artifact |
| D12 | Portal (index of everything) | `pack/out/portal/index.html` and published artifact |
| D16 | CRA Enterprise Edition (hyperscaler): programme case, evidence from the pipeline, Article 14 at volume, portfolio classification, open-source strategy, global control set, Official Journal verification, legal positions, Google outside-in appendix | `pack/enterprise/` (papers, code, models, data); published doc |
| D17 | Global product security control set (EU, UK, US, Japan, Singapore, Australia) | `pack/enterprise/global-control-set/site/`; published artifact |
| DS | Advisory design system | `pack/out/hosted/DS-design-system/` (tokens, CSS, components); published artifact |
| KB | CRA knowledge base (4 tabs) | `reports/` (source) and `pack/out/hosted/KB-knowledge-base/` (Word, Markdown, PDF); published doc |

Everything hosted on claude.ai is also copied into `pack/out/hosted/` (exported 1 Nov 2026): decks and one-pagers as PDF plus source, docs as Word, Markdown and PDF per tab, the dashboard as source, data and a snapshot. The claude.ai versions stay the live, editable copies; re-export after editing them. Deck PPTX files are fully editable (native text, shapes, tables and charts, with speaker notes), rebuilt from the slide source by `pack/engine/pptx/d0N_build.js`; they use the design fonts Source Serif 4, Inter and JetBrains Mono (free on Google Fonts), so install those for exact line breaks.

## Layout

- `pack/data/` — single source of truth: `pack_data.json` and `DATA_SUMMARY.md`
- `pack/build_data.py` — generates both data files (wrapper around `pack/engine/build.py`)
- `pack/clients/` — client intakes; `pack/reskin.py` and `pack/engine/` — the re-skin pipeline
- `pack/BRIEF.md`, `pack/briefs/` — master brief and one brief per deliverable, plus the independent QA brief
- `pack/out/` — Excel workbooks, portal, diagnostic and classifier HTML, `urls.json`
- `reports/` — CRA knowledge base: `sections/` (16), `guides/corporate/`, `guides/application/`, `verification.md` (its corrections override the sections), `digest.md`; `EU CRA engineering compliance.md` is the same material as one document
- `research_notes/` — raw research notes behind the knowledge base

## Rebuild the data

```
python3 pack/build_data.py
```

Deterministic (seeded): re-running reproduces `pack_data.json` and `DATA_SUMMARY.md` byte for byte. Change client numbers in `pack/clients/example-group/client.yaml` (regulatory content in `pack/engine/build.py`), then rerun; every deliverable takes its figures from the output.

## Re-skin for a new client

1. Copy the blank intake: `cp -r pack/clients/_template pack/clients/<slug>`, then fill `client.yaml` (every key is commented; `pack/clients/northwind-devices/` is a complete worked example).
2. Run `python3 pack/reskin.py pack/clients/<slug>/client.yaml` (options: `--out dist/<slug>`, `--skip-excel`). The intake is validated first, with a message per problem.
3. Optional: add `workbook_text.json` beside the intake for client narrative the Excel workbooks use (decision rationales, issue next steps, notes); without it they fall back to generic text. Example Group's is in `pack/clients/example-group/`.
4. Regenerated into `dist/<slug>/`: `data/` (pack_data.json, DATA_SUMMARY.md), `excel/` (D10, D11), `diagnostic/` (D08), `portal/` (D12) and `classifier/` (D13, presets from the client's families).
5. Hosted decks, docs, one-pagers and the dashboard cannot be regenerated locally: `RESKIN.md` lists every value to change in each (reference → client), how to update each artifact type and in what order; `reskin_values.json` holds the same mapping for a Claude session. Put the new artifact URLs in `pack/clients/<slug>/urls.json` and rerun so the portal links them (until then it shows "To be produced for this client").
6. Limits: the programme window is fixed to Q4 2026–Dec 2027 by the cost model periods; regulatory content (facts, diagnostic questions, classifier categories, knowledge base, D06 research) is shared and dated 30 Oct 2026.
7. Regression: `python3 -m pytest pack/tests` checks that Example Group still renders byte for byte. After editing the reference portal or classifier in `pack/out/`, run `python3 pack/engine/make_templates.py`.

## Design notes

- Notified-body status in the pack data and deliverables is dated "at checks to 8 Sep 2026" (the last verified NANDO check; the knowledge base states it as at 30 Oct 2026). Recheck NANDO before each client issue and update `build_data.py`.
- D11 holds ten conformity-assessment rows (notified-body routes) at "Not started" by design: they cannot progress until a CRA notified body is designated and contracted. Clear a row's "Status hold" cell to release it once its body is contracted.
- The staff pulse (D07) needs works council sign-off by 6 Nov 2026 before its 23 Nov launch; the comms calendar (D05) carries the same gate.

## Rebuild the editable decks

`node pack/engine/pptx/d01_build.js` (likewise `d02_build.js`, `d03_build.js`) rebuilds each deck's PPTX from `pack/out/hosted/<deck>/source/` using Playwright and PptxGenJS (`npm i pptxgenjs` if missing). Web fonts are vendored in `pack/engine/pptx/fonts/` (SIL Open Font License). D02's line-break tuning also uses static Source Serif 4, Inter and JetBrains Mono files from `~/.fonts` or `/usr/share/fonts` when present.
