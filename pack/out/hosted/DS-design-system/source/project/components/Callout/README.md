# Callout

A labelled box that interrupts the text for one reason only; five kinds, each recognisable by ground and label, never by a coloured left border.

| Kind | Class | Ground · label | Use |
|---|---|---|---|
| Key insight | `adv-callout--insight` | `bg-emphasis` · `text-accent` | The one finding the section exists to make |
| Decision required | `adv-callout--decision` | `bg-inverse` · `accent-on-inverse`, text `text-on-inverse` | An ask of the reader, with its ID (BD1 …), the decision and its cost or date |
| Illustrative data | `adv-callout--illustrative` | `bg-subtle` · `text-muted` | Where client numbers are fictional or modelled |
| Draft · unverified | `adv-callout--draft` | transparent, 1.5px dashed `rule-strong` · `text-body` | Vendor estimates, commentary, anything awaiting a check — say what would verify it |
| Critical | `adv-callout--critical` | `bg-critical` · `text-critical` | The binding constraint or a legal deadline — at most one per page; the only callout that may use the warning icon |

**Anatomy** — label (12px 600 uppercase, optional 16px icon) · title (16px 600, a sentence) · body (`body-small`, ≤ 3 lines). Padding 16 × 24, `radius-md`.

**Rules**
- At most two callouts per page, never two of the same kind side by side.
- The callout restates nothing: it adds the implication, the ask or the caveat.
- Decision required always names who decides and by when.

**You provide** kind, label (with an ID where relevant), title, body.

**Web**
```html
<aside class="adv-callout adv-callout--decision">
  <p class="adv-callout__label">Decision required · BD3</p>
  <p class="adv-callout__title">Authorise notified-body pre-contracting</p>
  <p class="body-small">Pre-assessments with three candidate bodies (up to EUR 60k) and formal contracts by Q1 2027.</p>
</aside>
```

**Slides** — a painted div: Key insight `background:#DCEFEC` (label `#0A5753`), Decision `background:#0E1A2B` (label `#2E9C93`, text `#FAFAF7`), Critical `background:#FFEDD5` (label `#C2410C`, text `#0E1A2B`); `padding:40px;border-radius:4px`; label 24px uppercase 3px tracking; text 28px. See SlideContent.

**Claude Docs** — a block quote whose first line is the bold label: "> **Decision required · BD3** — Authorise notified-body pre-contracting …".
