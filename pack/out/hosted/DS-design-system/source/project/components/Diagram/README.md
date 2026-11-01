# Diagram

Diagrams instead of pictures: numbered boxes, thin connectors and words, with the one step the message is about outlined in teal.

**Use** for processes (the reporting clock), sequences (three waves), structures (who signs what) and choices (conformity routes). If a diagram needs a legend to be understood, simplify it.

**Anatomy**
- Steps: `bg-surface` boxes, 1px `rule`, `radius-md`, 16px padding; a mono step number (01 …), the key value in `heading-2` serif (24h, 72h), a bold label, one line of detail in `text-muted`.
- Focus: one step at most, outlined 2px `action`, its value in `text-emphasis`. Use `signal` only for a step that is the binding constraint.
- Connectors: 1.5px `text-muted` arrows (`arrow-right` icon) or lines; straight or right-angled, never curved swooshes; no connector without a direction.
- Reading order left to right, then top to bottom; on phones the flow stacks and arrows turn down.
- Caption and source like any exhibit; `role="img"` with an `aria-label` that tells the sequence.

**You provide** steps (number, value, label, detail), the focus step, caption, source.

**Web**
```html
<div class="adv-flow" role="img" aria-label="…">
  <div class="adv-flow__step adv-flow__step--focus"><span class="adv-flow__n">02</span><span class="heading-2 adv-flow__time">24h</span><span class="adv-flow__what">Early warning</span><span class="adv-flow__detail">Through ENISA’s Single Reporting Platform</span></div>
  <div class="adv-flow__arrow" aria-hidden="true"><svg class="adv-icon" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg></div>
</div>
```

**Slides** — a flex row of painted divs (`background:#FFFFFF;border:1px solid #C5CDD8;border-radius:4px;padding:32px`), the focus box `border:2px solid #0F6E6A`; values in Source Serif 4 56px; between boxes an `<x-connector style="width:64px;color:#56667E">` or `<x-shape kind="arrow-right" style="width:48px;height:24px;background:#56667E">`.

**Don't** use stock photos, people, clip art, 3D, gradients or icons in place of words.
