# CRA Readiness Programme Pack

White-label consulting pack for the EU Cyber Resilience Act (Regulation (EU) 2024/2847), populated with an illustrative fictional client (Example Group, "Project Rampart"). All client figures are illustrative. Regulatory facts are verified to 30 Oct 2026 (notified-body status to 8 Sep 2026). Not legal advice.

## Deliverables

| ID | Deliverable | Where it lives |
|---|---|---|
| D01 | Board briefing deck (22 slides) | Published artifact, see `pack/out/urls.json` |
| D02 | SteerCo pack (15 slides, monthly template) | Published artifact |
| D03 | Engineering training deck (24 slides) | Published artifact |
| D04 | Two one-pagers (CRA, Project Rampart) | Published artifact |
| D05 | Communications pack (9 tabs) | Published doc |
| D06 | Research report, State of CRA readiness 2026 | Published doc |
| D07 | Survey instruments (8 tabs) | Published doc |
| D08 | Readiness diagnostic | `pack/out/diagnostic/index.html` and published artifact |
| D09 | Programme dashboard | Published artifact |
| D10 | Business case and cost model | `pack/out/excel/` |
| D11 | Obligations register and programme tracker | `pack/out/excel/` |
| D12 | Portal (index of everything) | `pack/out/portal/index.html` and published artifact |
| DS | Advisory design system | Published artifact |

Decks, docs and the dashboard are hosted on claude.ai, so the repo holds their briefs and the data behind them, not the files.

## Layout

- `pack/data/` — single source of truth: `pack_data.json` and `DATA_SUMMARY.md`
- `pack/build_data.py` — generates both data files
- `pack/BRIEF.md`, `pack/briefs/` — master brief and one brief per deliverable, plus the independent QA brief
- `pack/out/` — Excel workbooks, portal and diagnostic HTML, `urls.json`
- `reports/` — CRA knowledge base: `sections/` (16), `guides/corporate/`, `guides/application/`, `verification.md` (its corrections override the sections), `digest.md`; `EU CRA engineering compliance.md` is the same material as one document
- `research_notes/` — raw research notes behind the knowledge base

## Rebuild the data

```
python3 pack/build_data.py
```

Deterministic (seeded): re-running reproduces `pack_data.json` and `DATA_SUMMARY.md` byte for byte. Change numbers in `build_data.py` only, then rerun; every deliverable takes its figures from the output.

## Known open items

- Two status sentences say "no notified body is designated" in the present tense (`overall_status` and the WS7 note in `build_data.py`). Date them "as at 8 Sep 2026" and republish the dashboard and decks that quote them.
- Works council sign-off date (6 Nov) in D07 is not reconciled against T30 in D05.
- Ten tracker rows in D11 are held at "Not started"; clear the "Status hold" cell to release them.
