# DS Advisory Design System: export

Offline copy of **Advisory Design System (white-label)**
(https://claude.ai/artifact/9AGwnwfY3RVENQQayi6ixN), a claude.ai artifact made from the Design
System type. Exported 1 Nov 2026 from the live version (1793480104-267c; last change 31 Oct 2026).

## Contents

| Path | What it is |
|---|---|
| `source/project/README.md` | The brand book: how to build decks, canvases, Docs, dashboards, web pages and workbooks with the system; content and visual foundations; iconography; accessibility; do and don't. Start here. |
| `source/project/tokens.json` | The tokens (52 colours in light and dark themes, type styles, spacing, radius, shadow, border, layout). |
| `source/project/design-system.json` | The system's index (title, namespace `Advisory`, last change). |
| `source/project/guides/web-css.md` | Guide for hand-built HTML pages, with a pasteable CSS token block. |
| `source/project/components/bundle.css` | Stylesheet for every component class (prefix `adv-`). |
| `source/project/components/<Name>/README.md` and `preview.html` | Usage rules and reference rendering for 35 components, including the 9 slide masters (`Slide*`). `Cover/` has only the cover preview. |
| `design-tokens.css` | `tokens.json` as plain CSS custom properties (aliases resolved, light on `:root`, dark by `prefers-color-scheme` or `data-theme="dark"`), plus the type-style classes. Generated for this export; its values match the token block in `guides/web-css.md` exactly. |

Paths under `source/` are the artifact's own published paths.

## Not exported

- The Design System type's own files (`index.html` page shell, `SKILL.md`, `artifact-type/…`
  runtime, references and demo). They are the type's, not this system's content.
- Uploaded assets: the asset store is empty. The system has no logo, icon or image files, and
  no font files: Inter, Source Serif 4 and JetBrains Mono are loaded from Google Fonts.
- Files the type generates in the browser (`tokens.css`, `api/` cards, `manifest.json`) are not
  published, so there is nothing to copy; `design-tokens.css` stands in for `tokens.css`.

The `preview.html` files expect the type's preview frame, which preloads the token CSS,
`bundle.css` and the fonts. To view one on its own, add
`<link rel="stylesheet" href="../../../../design-tokens.css">` and
`<link rel="stylesheet" href="../bundle.css">` to its `<head>`.
