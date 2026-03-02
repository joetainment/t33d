Example of Header Element For Titles
=====================================

An example of using the HTML `<header>` element as a styled document
title, as an alternative to `<div class="doc-title">`.

See also:
- [[Heading-Style]] -- the heading convention this relates to


---


The Example
===========


Basic form
----------

```html
<header class="doc-title" style="font-size:2.2em; font-weight:900;
padding-bottom:0.3em; border-bottom:2px solid;">My Document Title</header>
```

This renders as a styled title block. The same dual class+style approach
from the `<div>` version applies here:

- Inline `style=` is applied by general renderers (GitHub strips it, but
  other tools use it)
- `class="doc-title"` is picked up by the Obsidian CSS snippet below

The Obsidian CSS snippet is the same one used for `div.doc-title`:

```css
/* .obsidian/snippets/t33d.css */
.doc-title {
    font-size: 2.2em;
    font-weight: 900;
    padding-bottom: 0.3em;
    border-bottom: 2px solid var(--text-normal);
    margin-bottom: 1em;
}
```


Full document example
---------------------

```markdown
<header class="doc-title" style="font-size:2.2em; font-weight:900;
padding-bottom:0.3em; border-bottom:2px solid;">My Document Title</header>

First Major Section
===================

Content here.

---

Second Major Section
====================

Content here.
```


---


Trade-offs vs div
==================


Why `<header>` has an edge
--------------------------

The `<header>` element is a semantic HTML5 sectioning element. It signals
"this is introductory/header content" to browsers, screen readers, and
parsers, whereas `<div>` carries no meaning at all. For a document title,
`<header>` is the more honest choice.

`<header>` is appropriate here because it wraps the introductory identity
of the document -- exactly what it was designed for.


Limitations to be aware of
---------------------------

- `<header>` is a block element with no default visual styling beyond
  display:block. The `style=` attribute is still needed for the visual
  treatment (size, weight, border).
- GitHub strips inline `style=` from `<header>` the same as from `<div>`,
  so the Obsidian CSS fallback is equally necessary.
- `<header>` inside Markdown body content is valid HTML5 -- when not
  inside a `<body>`, it still works as a sectioning element scoped to
  the document.
- Some very minimal Markdown renderers may not pass through `<header>`
  as HTML (they strip all tags). This is the same limitation as `<div>`.


Summary
-------

| Approach                        | Semantic | Visual (Obsidian) | Visual (GitHub) |
|---------------------------------|----------|-------------------|-----------------|
| `<div class+style>`             | None     | Yes (CSS snippet) | Class only      |
| `<header class+style>`          | Yes      | Yes (CSS snippet) | Class only      |
| `# H1` (used as title)          | Yes      | Yes               | Yes             |

`<header>` is strictly better than `<div>` for this use case. The only
reason to prefer `<div>` would be familiarity -- `<div>` is more commonly
seen in Markdown-embedded HTML examples, so it may cause less confusion
for contributors who haven't seen `<header>` used this way.
