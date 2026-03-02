Heading Style
=============

T33D convention for heading syntax in Markdown documents.

See also:
- [[Style-Guide]] -- overall conventions index
- [[Naming-Conventions]] -- file and folder naming rules


---





Rules
======


Never mix ATX and setext syntax on the same heading [FIRM]
-----------------------------------------------------------

Each heading uses one syntax only. These are the two correct forms:

```
My Heading          <- setext H1
==========

My Heading          <- setext H2
----------

# My Heading        <- ATX H1
## My Heading       <- ATX H2
### My Heading      <- ATX H3 (and deeper)
```

These are wrong -- hash prefix combined with setext underline:

```
✗  # My Heading
   ==============

✗  ## My Heading
   --------------
```




Heading hierarchy [FIRM]
------------------------------------

H1 is a major section heading. H2 is a section within it. H3 is a
subsection, H4 a sub-subsection, and so on. H1 is not reserved for
the document title -- it is used throughout the document wherever a
new major section begins.

The **first H1** is a special case: it typically shares the document's
filename and serves as the opening "about this document" entry point
before the main content starts. It is a heading like any other, just
conventionally used this way.

If a visually distinct styled title is needed -- something separate
from the heading hierarchy -- use HTML for it, leaving the heading
levels clean and unambiguous.

A typical document structure looks like:

```
My-Document-Name            <- first H1, same as filename, intro/about
================

Brief summary of what this document covers.

---

First Major Section         <- H1 again, main content begins
===================

Section Name                <- H2
------------

### Subsection              <- H3

#### Detail                 <- H4

---

Second Major Section        <- H1 again
====================

...
```

When a styled HTML title is used instead of the first H1, use both
`class=` and `style=` on the same element:

```html
<div class="doc-title" style="font-size:2.2em; font-weight:900;
padding-bottom:0.3em; border-bottom:2px solid;">My Document Title</div>

First Major Section
===================

Section Name
------------

### Subsection
```

General renderers (GitHub, most Markdown tools) apply the inline
`style=` directly. Obsidian strips inline styles in Reading View but
keeps the `class=`, so the CSS snippet below picks it up:

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

One element, two hooks -- styled everywhere.






Preferred syntax for H1 and H2: setext [SOFT]
-----------------------------------------------------

The setext underline creates a strong visual separator in plain text,
which matters when notes are read in terminals, diff views, or basic
editors. H3 and deeper always use ATX hash prefixes.

This is the `setext_with_atx` convention -- a named valid mode in
markdownlint.

ATX-only (Option B below) is also acceptable. Many documents in the
project will use ATX for H1 and H2, especially shorter notes or those
where deep heading nesting is the primary concern.





Section separators: `---` thematic breaks [SOFT]
------------------------------------------------------

A `---` line between sections -- placed at the end of the outgoing
section, before the next heading -- is encouraged where a strong visual
break is wanted. It renders as a horizontal rule and is unambiguous:

```
...end of content of previous section.

---



Next Section
--------------

Content here.
```


This pairs naturally with either setext or ATX headings and carries
no risk of setext confusion (blank lines on both sides make the parse
unambiguous).


No non-ASCII characters in document structure [FIRM]
-------------------------------------------------------------

Document templates and structural boilerplate must be writable on a
standard US keyboard. Non-ASCII characters (e.g. Unicode box-drawing
characters like `─────`) must not be used for separators or decoration.
See [[Em-Dashes]] for the same principle applied to em dashes.

---





Background and Reasoning
==========================

The following explains the options considered and why the rules above
were chosen. Most readers can skip this.


The two heading syntaxes
------------------------

**Setext style** (underline with `=` or `-`):

```
My Heading
==========

Subheading
----------
```

**ATX style** (hash prefix):

```
# My Heading
## Subheading
### Deeper Section
```

Setext only covers H1 and H2. ATX covers H1 through H6. Any document
using H3 or deeper must use ATX for those levels regardless of what it
uses for H1/H2.


The core tension
----------------

ATX headings have low visual weight in plain text -- a line starting
with `##` reads almost like surrounding paragraph text. Setext headings
create an unmissable horizontal band. For T33D, plain-text readability
matters: notes are read in terminals, diff views, and basic editors,
not only through rendered output.

But T33D documents make heavy use of H3 and H4, which require ATX
regardless. And some tools (Prettier, linters) auto-convert setext to
ATX, creating unwanted diffs.


Options considered
------------------

**Option A -- setext H1/H2, ATX H3+ (preferred)**

The only hybrid with formal recognition. markdownlint names it
`setext_with_atx`. Pandoc can output it. Chosen because plain-text
visual weight at the top levels is worth the mixed syntax.

**Option B -- ATX only (also acceptable)**

Perfectly consistent. Widely recommended by Google's style guide,
Prettier, and most linters. Weak plain-text readability at H1/H2 is
the only downside. Acceptable in T33D, especially when combined with
`---` section separators.

**Option C -- `---` thematic break before the heading (fine, selective)**

A `---` before a heading closes the previous section with a visible
horizontal rule. Not a heading style itself -- a section separator.
Compatible with both Options A and B.

**Option D -- Unicode box-drawing underlines (ruled out)**

Characters like `─────` (U+2500) avoid the `<hr>` problem of `---` but
produce a plain `<p>` element in rendered HTML and require non-ASCII
input. Ruled out by the non-ASCII constraint.


Summary
-------

| Option | Plain-text readability | Rendered output | Consistency | Tooling |
|--------|----------------------|-----------------|-------------|---------|
| A (setext H1/H2 + ATX H3+) | High for top levels | Clean | Mixed | markdownlint named mode |
| B (ATX only) | Low | Clean | Full | Strongly preferred everywhere |
| C (`---` section separator) | High where used | Clean `<hr>` | ATX | Standard |
| D (Unicode box-drawing) | High | Broken `<p>` | ATX | None -- ruled out |

Note on Obsidian Live Preview
------------------------------

Setext headings render with partially visible underline characters in
Obsidian's Live Preview mode. This is a known Obsidian limitation, not
a Markdown spec issue. Source Mode is unaffected. The plain-text benefit
was considered worth the Live Preview quirk.
