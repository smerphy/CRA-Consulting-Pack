# Button

Three emphasis levels: primary (solid teal, once per view, for the thing the page is for), secondary (outline), tertiary (teal text).

| Variant | Class | Look | Use |
|---|---|---|---|
| Primary | `adv-btn--primary` | `action` fill, `text-on-action` (6.1:1 light, 5.2:1 dark); hover `action-hover` | Submit, Start, Approve — one per view |
| Secondary | `adv-btn--secondary` | `bg-surface`, 1px `rule-strong` border, `text-primary` | Save draft, Export, Cancel |
| Tertiary | `adv-btn--tertiary` | no border, `text-accent`; hover `bg-emphasis` | View guidance, Show all |

**Sizes** — `--sm` 32px (dense tables only), default 40px, `--lg` 48px (primary calls on landing pages and phones; meets the 44px target).

**Rules**
- Labels: verb first, sentence case, two or three words, no full stop ("Submit assessment").
- Radius `radius-md` 4px; weight 600; icons only for direction (→) or download, 16px, after the label.
- Disabled: `bg-subtle` with `text-muted`; say why nearby ("Answer all 40 questions to submit").
- Focus: the 2px `focus` outline with 2px offset (from bundle.css). Use `<button>` for actions and `<a class="adv-btn">` for navigation.
- Never a red "danger" button; destructive actions are secondary buttons with an explicit label ("Delete response").

**You provide** label, variant, size, type or href.

**Web**
```html
<button class="adv-btn adv-btn--primary" type="button">Submit assessment</button>
<button class="adv-btn adv-btn--secondary" type="button">Save draft</button>
<a class="adv-btn adv-btn--tertiary" href="…">View guidance</a>
```
