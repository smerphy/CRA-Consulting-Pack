# Using the Advisory Design System (for slide and design builders)

- Design system artifact: https://claude.ai/artifact/9AGwnwfY3RVENQQayi6ixN ("Advisory Design System (white-label)", Design System type). Namespace/install folder: `advisory`.
- Read `project/README.md` and `project/tokens.json` from it with the Artifact tool (`action: "read"`, `url` = the design system URL, `path` = "project/README.md" etc.; or list its files with `action: "list"`, `scope: "files"`, `url` = the design system URL). Its content is being published now; if a file is not served yet, draft your content first and retry later.
- When creating your Slides/Design artifact, attach/apply this design system exactly as the type's instructions describe (the create result lists the design systems; pick this one).
- Fonts (Google): Source Serif 4 (titles, weight 500), Inter (body and all numbers), JetBrains Mono (IDs).
- Slide grid: 1920x1080, 128px margins, tracker label pinned top at 64px, action title 56px serif, body 28px, nothing smaller than 24px, footer pinned bottom at 64px.
- Key hexes: paper #FAFAF7, ink-900 #0E1A2B, ink-700 #26364D, ink-500 #56667E, ink-300 #C5CDD8, accent-600 #0F6E6A, accent-400 #2E9C93 (on dark), accent-100 #DCEFEC, signal #C2410C (binding constraint only). RAG red #B42318, amber #B54708, green #027A48.
- 9 slide masters and 26 components exist (title, section divider, action-title content, two-column, chart, big number, quote/callout, agenda, appendix; RAG pill, KPI tile, heatmap cell, risk matrix, Gantt bar, tables, callouts...). Use them rather than inventing new styles.
