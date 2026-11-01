# RagPill

Status shown twice — in colour and in a word — as a solid pill for summaries or a dot plus label for dense tables.

**Use** for programme, workstream, KPI, milestone and action status. RAG colours mean status only; never use them for categories, emphasis or decoration.

**Vocabulary** — pick one set per deliverable and keep it:
| Colour | Word | Or |
|---|---|---|
| `rag-green` `#027A48` | Green | On track · Complete |
| `rag-amber` `#B54708` | Amber | At risk |
| `rag-red` `#B42318` | Red | Off track · Decision needed |
| `rag-grey` `#8A94A6` | Grey | Not started · Planned |

**Variants**
- Solid pill (`adv-rag adv-rag--amber`): KPI tiles, status summaries, slide headers. White text on red, amber and green (6.6, 5.4, 5.4:1); `ink-900` on grey (5.7:1) — never white on grey.
- Large (`adv-rag--lg`): the overall programme status ("Programme: Amber").
- Dot (`adv-rag-dot adv-rag-dot--red`): tables with many rows; the word stays in `text-primary`, so it reads in both themes.

**You provide** the status and, where space allows, the reason beside it ("Red — no notified body designated").

**Web**
```html
<span class="adv-rag adv-rag--red">Red</span>
<span class="adv-rag-dot adv-rag-dot--green">Green</span>
```

**Slides** — a pill is a `<p>` with background, padding and radius; put it in a row `<div>` (or give it `align-self:start`) so it hugs its text:
```html
<p style="align-self:start;background:#B54708;color:#FFFFFF;font-size:24px;line-height:32px;font-weight:600;padding:4px 20px;border-radius:999px">Amber</p>
```
Grey: `background:#8A94A6;color:#0E1A2B`. In slide tables (no pills in cells) write the word in the status colour; Grey as `#56667E`.

**Spreadsheets** — fill the cell with the status colour, white bold text (ink-900 on grey), and the word.

**Don't** show a coloured shape without its word, invent extra colours (no "light green"), or colour a whole row by status.
