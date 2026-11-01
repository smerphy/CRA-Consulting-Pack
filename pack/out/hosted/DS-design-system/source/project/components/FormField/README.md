# FormField

A labelled form control — text input, select or textarea — with optional hint and an error message that says how to fix the problem.

**Anatomy**
- Label: 14px 600 `text-primary`, always visible (never placeholder-only); "(optional)" in `text-muted` rather than asterisks on required fields.
- Hint: 13px `text-muted`, between label and control, linked with `aria-describedby`.
- Control: ≥ 44px tall, 1px `rule-strong` border (≥ 3:1 on every ground), `radius-md`, `bg-surface`, 15px text; focus = 2px `focus` outline and border.
- Select: native `<select>` in `adv-select-wrap` (draws the chevron).
- Error: `adv-field--error` turns the border `text-danger`; the message below starts with the warning icon and says what to do ("Enter your role, not your name"); set `aria-invalid="true"`.

**Rules**
- One column on phones; two at most on desktop for short fields.
- Ask for roles, never names, in client instruments; no free-text fields for personal data.
- Validate on submit or blur, not on every keystroke; keep the user's input after an error.

**You provide** label, id, hint, control type, options, error text.

**Web**
```html
<div class="adv-field adv-field--error">
  <label class="adv-field__label" for="role">Respondent role</label>
  <input class="adv-input" id="role" type="text" aria-invalid="true" aria-describedby="role-e">
  <span class="adv-field__error" id="role-e">Enter your role, not your name</span>
</div>
```
