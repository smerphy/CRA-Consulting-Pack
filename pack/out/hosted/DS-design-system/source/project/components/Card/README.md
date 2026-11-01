# Card

A hairline-bordered surface that groups one item — a pillar, a deliverable, a decision — with eyebrow, title, short text and a meta row.

**Variants**
- Default `adv-card`: `bg-surface`, 1px `rule`, `radius-lg` 6px, 24px padding, no shadow.
- Link card `a.adv-card`: the whole card is the link; hover darkens the border to `rule-strong`; a `adv-card__cta` ("Open →") in `text-accent` in the meta row.
- Inverse `adv-card--inverse`: `bg-inverse` with `text-on-inverse` and `accent-on-inverse` — for decisions only, at most one per row.

**Anatomy** — eyebrow (`eyebrow`, `text-accent`: ID · type) · title (`heading-4`, a sentence or a name) · text (`body-small`, ≤ 3 lines) · meta row after a hairline (audience, date, status).

**Rules** — cards in a row share a height (grid stretch) and a structure; no icons as decoration, no images, no coloured top or left borders, no shadows. Three or four per row at 1200px; one per row on phones.

**You provide** eyebrow, title, text, meta, href for link cards.

**Web**
```html
<a class="adv-card" href="…">
  <p class="eyebrow">D05 · Claude Doc</p>
  <h3 class="heading-4 adv-card__title">Communication pack</h3>
  <p class="body-small">Messages, audiences and channels for 22 stakeholder groups.</p>
  <div class="adv-card__meta"><span>Sponsor, comms</span><span class="adv-card__cta">Open →</span></div>
</a>
```

**Slides** — `background:#FFFFFF;border:1px solid #C5CDD8;border-radius:6px;padding:40px` with 24px label, 32px 600 title, 28px text.
