# Brief D09 — Programme Dashboard (Dashboard artifact)

**Title:** "Project Rampart — Programme Dashboard"
**Create from:** `Artifact` quickstart with intent "other" (it should direct you to the Dashboard type, `type_url: https://claude.ai/artifact/GZLZthZ2sQjn7T16skfdeF`); publish with the type_url, title and `auto_open: "after_first_write"`; follow the instructions the type returns (how data is stored and how charts are declared). Load the `dataviz` skill before designing charts.

**Purpose:** the live management view the sponsor and SteerCo open every week — the "management update" that is always current. Status as at 30 Oct 2026 (SteerCo #1). All client data illustrative; say so in the header/subtitle. Every number shows where it came from (the type requires this: use the `source` fields in DATA_SUMMARY.md, e.g. "Readiness diagnostic, 28 Oct 2026", "Finance", "SRP roster").

**Data:** `/home/claude/pack/data/pack_data.json` — `programme` (overall RAG and status line, workstreams with RAG, milestones, phases, waves, mobilisation_plan), `kpis` (K01-K12), `kpi_trajectories` (readiness plan by month with Oct 2026 actual; SBOM coverage plan/actual), `cost_model` (monthly_plan cumulative, actual_to_date, base_totals, by_workstream, scenarios), `diagnostic` (portfolio index, domain readiness index, family readiness, BU and class indices), `risks` (R01-R10 with likelihood/impact), `issues`, `decisions`, `client` (families, classes, EU revenue needing a notified body EUR 468m), `meta` (days to 11 Dec 2027 = 406 from 31 Oct 2026).

**Layout (scroll story, top to bottom):**
1. Header strip: overall RAG Amber with the status sentence; countdown "406 days to full application (11 Dec 2027)"; Art 14 "live since 11 Sep 2026"; "Illustrative — Example Group".
2. KPI tiles (K01-K12) with value, target, RAG, trend.
3. Readiness: portfolio index 44% vs plan trajectory to 93% by Dec 2027 (line: actual point + plan); domain readiness bars (Art 14 reporting 72% best; Conformity & access 16% worst); family readiness ranked bars coloured by class.
4. Market access: EU revenue by class (Default EUR 338m; Class I EUR 396m; Class II EUR 73m) with "EUR 468m needs a notified body"; route per family table (Module A / B+C / H); notified-body status line (none designated at checks to 8 Sep 2026; 3 candidates shortlisted).
5. Delivery: workstream RAG table (WS1-WS8 with notes); milestones table (M0-M14 with status); next-30-days tasks from the mobilisation plan (due by 30 Nov 2026).
6. Money: cumulative spend plan vs actual (Oct actual EUR 410k vs plan EUR 384k); base one-off EUR 9.25m by workstream; scenarios low/base/high EUR 7.93m / 9.25m / 11.42m; run EUR 1.84m/yr.
7. Risk: 5x5 risk matrix (or a scored bar) with R01-R10, top five listed with owners and mitigations; open issues I01-I03; decisions SD1-SD4 and board asks BD1-BD5.
8. Footer: data as at 30 Oct 2026; regulatory facts verified to 30 Oct 2026; "Prepared by [Advisor]".

**Style:** apply the brand tokens from BRIEF.md (fonts, ink/paper, teal accent, RAG colours, categorical palette order) as far as the Dashboard type allows. Calm, dense, executive.

**Verify:** after publishing, read/screenshot the dashboard, check every number against DATA_SUMMARY.md, fix any chart that misreads. Report the URL.
