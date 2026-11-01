# Tag

Small square-cornered labels for categories — business unit, product class, wave, route, IDs — and removable filter chips. Square means category; round means status (RagPill).

| Variant | Class | Use |
|---|---|---|
| Neutral | `adv-tag` | Business units, domains: `bg-subtle`, `text-body` |
| Accent | `adv-tag--accent` | The category the page is about (Class I, Class II): `bg-emphasis`, `text-accent` |
| Outline | `adv-tag--outline` | Waves, routes, filters: 1px `rule-strong` inset |
| ID | `adv-tag--id` | K07, R01, BD3: mono |
| Removable | `adv-tag__remove` inside | Active filters; 24px remove button with an `aria-label` |

**Rules** — 24px tall, `radius-sm` 2px, 12px 500; one or two words; never RAG colours; never more than one accent tag per item.

**You provide** text, variant, and for chips the remove action.

**Web**
```html
<span class="adv-tag adv-tag--accent">Class I</span>
<span class="adv-tag adv-tag--outline">Wave 1<button class="adv-tag__remove" type="button" aria-label="Remove filter Wave 1">×</button></span>
```

**Slides** — `<p style="align-self:start;background:#EEF1F5;color:#26364D;font-size:24px;line-height:32px;font-weight:500;padding:0px 12px;border-radius:2px">Wave 1</p>`; accent: `background:#DCEFEC;color:#0A5753`.
