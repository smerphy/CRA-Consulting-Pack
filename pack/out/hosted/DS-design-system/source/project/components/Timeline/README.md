# Timeline

The programme Gantt: phase bars on a month scale, milestone diamonds with ID and date, a teal "today" line and a dashed ink line at the fixed deadline.

**Encoding**
| Element | Spec |
|---|---|
| Month scale | months as 3-letter labels, year at January; 1px `text-primary` rule under the scale; hairline `rule` at each quarter |
| Phase bar | 14px tall, `radius-sm`. Planned `viz-2` (navy), current `action` (teal), complete `viz-6` (grey). Open-ended phases run to the edge with a square end |
| Milestone | 12px diamond: planned `text-primary`, complete `action`, at risk `rag-amber` **plus the words "At risk"** in its label. Label: ID in bold and date; ≤ 18 characters per line |
| Today | 2px `action` line with a teal flag "Today 31 Oct 2026" |
| Deadline | 2px dashed `text-primary` line with an ink flag (e.g. "11 Dec 2027") |

**Rules**
- Rows are phases or workstreams, labelled with ID and name; small text under the name gives the dates.
- One milestone row per Gantt is enough for board level; SteerCo packs may add milestones to phase rows.
- Never colour bars by RAG; status goes in the milestone label or a RagPill column.
- Position by date: x = (date − scale start) ÷ (scale end − scale start) × track width.

**You provide** the scale start and end, phases with dates and state, milestones with ID, date and status, today's date, the deadline.

**Web** — rows are `adv-gantt__label` + `adv-gantt__track` pairs inside `adv-gantt`; bars, diamonds and lines are absolutely positioned with `left` / `width` in %:
```html
<div class="adv-gantt__track"><div class="adv-gantt__bar adv-gantt__bar--current" style="left:12.5%;width:9.6%"></div></div>
<div class="adv-gantt__ms adv-gantt__ms--risk" style="left:30.9%"></div>
```

**Slides** — each row is a `position:relative` div (≤ 24 pinned children) of fixed width; bars are painted divs at `left`/`width` in px; diamonds are 20px painted squares with `transform:rotate(45deg)`; labels are 24px `<p>`s. At 1240px for 16 months, one month is 77.5px.
