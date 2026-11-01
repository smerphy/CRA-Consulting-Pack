# Brief: CRA Compliance Templates Kit — tab writers

You are filling tabs of an existing Claude Doc, "CRA Compliance Templates Kit" (doc id 6f51a9f5-dd89-43b9-84cd-43602edd3c37, link https://claude.ai/artifact/EkH2mzWezJ1c24mVLFSZA6). The user is watching the doc fill. The kit is part of a white-label CRA consulting pack (repo /home/claude/cra-consulting-pack). Audience: a manufacturer's compliance lead, product security officer, engineering and legal, who will copy each template per product and fill it in. It must be usable as-is: a consultant hands it to a client.

## Tools
Load the `anthropic-skills:docs` skill first, then ToolSearch "select:mcp__Claude_Docs__update,mcp__Claude_Docs__guide,mcp__Claude_Docs__read" and read guide topic.index once (skip topic.charts/diagram; these are text templates). Fill each tab with ONE `update` call per tab: ref {"object":"node","id":"<tab body id>"}, engine "prose", container {"kind":"project","id":"6f51a9f5-dd89-43b9-84cd-43602edd3c37"}, payload {"ops":[{"op":"replace","target":{"kind":"blocks","ids":["<pending id>"]},"with":{"as":"markdown","from":{"kind":"inline","content":"<markdown>"}}}]}. The tab already has its H1 title; do NOT repeat it — start your markdown with the lead paragraph. If a tab is too long for one call, fill the first part replacing the pending block, then append the rest with an insert ({"op":"insert","target":{"kind":"root"},"side":"end",...}). Do not use "as":"markdown" code fences for the tab's own text; use ```markdown or ```text code blocks only for copy-paste artefacts such as the security.txt file or a notification body if that helps.

## Sources (facts only from here; never invent law)
- Knowledge base sections: reports/sections/*.md (03 scope, 05 roles, 06 classification, 07 Annex I Part I, 08 Annex I Part II, 09 reporting, 10 conformity & documentation, 12 open source, 13 interplay)
- Implementation guides: reports/guides/application/*.md (03 risk assessment, 06 SBOM, 07 updates, 08 vulnerability handling, 10 reporting runbook, 11 documentation set, 12 conformity prep, 13 worked example) and reports/guides/corporate/*.md (06 supply chain, 07 reporting governance, 08 evidence)
- reports/verification.md — its corrections OVERRIDE the sections.
- Illustrative example data: pack/data/pack_data.json → client.product_families (use L2 Smart Lock: Class I, Annex III Class I item 17, Home & Building Solutions, check its support_period_years, rdps, route fields) and DATA_SUMMARY.md. Example Group is fictional.
Cite the article / annex point next to each field (e.g. "Annex V pt 3", "Art 13(8)"). Quote statutory wording only where the KB quotes it. KB article and annex wording was checked against the Official Journal text on 1 Nov 2026 (pack/enterprise/oj-verification); do not add "confirm the OJ wording" caveats to verified quotations such as Annex V pt 3 "provider". Where the KB says something is unverified, disputed or dependent on a future act, say so in one line. Facts as at 30 Oct 2026; notified-body status "at checks to 8 Sep 2026".

## Shape of every tab (consistent across the kit)
1. Lead paragraph (2-3 sentences): what this document is, the legal basis, when it is needed, where it is filed.
2. "## At a glance" — a two-column pipe table with rows: Legal basis · Needed for · Owner (a role, e.g. Product security officer) · Approver · When to create · When to update · Retention · Feeds (other kit templates by number, e.g. "Template 4, Annex VII pt 3").
3. "## How to complete" — a short numbered list (4-7 steps).
4. "## Template" — the fill-in template itself. Use pipe tables with columns like | Field | What to enter | Basis | Example: L2 Smart Lock (illustrative) |. Placeholders in [square brackets]. Example cells give a realistic, specific illustrative entry for the L2 Smart Lock; label the column "(illustrative)". Where the artefact is prose (a declaration, a policy, a clause, a notice), give ready-to-adapt wording with [placeholders] in a ```text code block or as normal paragraphs, plus a field table if useful.
5. "## Common mistakes" — 3-5 bullets drawn from the KB (pitfalls guides).
6. Final line in italics: "Template N · v1.0 · 31 Oct 2026 · Not legal advice; confirm wording against the Official Journal text before use."

Style: British English; short plain sentences (<25 words); no em-dash asides, no emoji, no filler, no "This template outlines". Tables over prose. Do not name real people or real companies as the client. No claims of "certified" or "fully compliant". Keep each tab focused: roughly 600-1,400 words.

## Report back
Per tab: done / not done, and anything you could not source. Under 150 words.
