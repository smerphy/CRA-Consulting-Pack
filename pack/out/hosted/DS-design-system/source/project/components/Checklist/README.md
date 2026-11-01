# Checklist

A ruled list of checks with a square box per item — done, open or blocked — each with its owner (a role) and due date.

**States** (`data-state` on the `<li>`)
- `done`: box filled `action` with a white check; text stays legible in `text-body` (never struck through).
- `open`: empty 1.5px `rule-strong` box.
- `blocked`: dashed `text-danger` box, and the word "Blocked:" with the reason in the meta column — never colour alone.

**Anatomy** — box (18px, `radius-sm`) · item text (a verifiable statement, `text-primary`) with an optional status line in `<small>` · meta column right: owner role, due date, or the blocker.

**Rules**
- Write items as checkable facts ("Technical file complete for this product version"), not tasks ("Work on documentation").
- Owners are roles; dates follow the date rule (3 Dec 2027).
- For survey and audit instruments, keep the checklist order identical to the question IDs.

**You provide** items, state, owner, due date or blocker.

**Web**
```html
<ul class="adv-checklist">
  <li data-state="done"><span class="adv-checklist__box" aria-hidden="true"><svg class="adv-icon" viewBox="0 0 24 24"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg></span><span class="adv-checklist__text">Cybersecurity risk assessment signed<small>Done</small></span><span class="adv-checklist__meta">Product security officer</span></li>
  <li data-state="blocked"><span class="adv-checklist__box" aria-hidden="true"></span><span class="adv-checklist__text">Notified-body certificate received<small>Blocked</small></span><span class="adv-checklist__meta"><b>Blocked:</b> no body designated</span></li>
</ul>
```
Interactive checklists use real `<input type="checkbox">` with a `<label>`; keep this visual.

**Slides** — rows with `<x-icon name="CheckCircle" style="color:#0F6E6A;width:48px;height:48px">` for done and an empty 32px square div with `border:2px solid #56667E` for open; text 28px.

**Claude Docs** — a task list (`- [x]` / `- [ ]`) with "— owner, due date" after each item.
