Spacing
=======

T33D conventions for blank lines and vertical spacing in Markdown documents.

See also:
- [[Heading-Style]] -- heading syntax and hierarchy
- [[Style-Guide]] -- overall conventions index


---


Rules
=====


Be liberal with blank lines [SOFT]
-----------------------------------

**The goal:** someone paging through the raw source file with PgUp /
PgDn should be able to see the document structure immediately and never
lose their place. Section headings should jump out; content should feel
like it belongs to its section.

Use more blank lines rather than fewer, especially around headings.
Plain-text readability is a first-class concern in T33D -- notes are
read in terminals, diff views, and basic editors, not only through
rendered output. Dense source is harder to scan. Blank lines are free
and have no effect on rendered output.

There is no maximum. If extra spacing makes a section boundary more
obvious in the raw file, add it.


Blank lines around headings [SOFT]
------------------------------------

Leave at least one blank line before and after every heading. For major
headings (H1, H2), two or more blank lines before the heading are
encouraged when the preceding content is dense.

```
...last line of previous content.


My Major Section
================

First line of content here.

---


Next Major Section
==================

...
```

The extra blank lines before H1/H2 headings are especially valuable
because they reinforce the same visual boundary that the setext
underline provides. Together they create an unmissable break in the
plain-text source.


Blank lines within content [FIRM]
-----------------------------------

Standard Markdown requires a blank line to separate paragraphs. Do not
omit it -- adjacent lines without a blank line between them are merged
into a single paragraph by all Markdown parsers.

```
✓  First paragraph.

   Second paragraph.

✗  First paragraph.
   Second paragraph.   <- these render as one paragraph
```


---


Background and Reasoning
=========================


Why this matters
-----------------

Markdown's blank line handling is intentionally permissive: any number
of consecutive blank lines is treated the same as one. This means
extra blank lines in source have no effect on rendered output -- they
are purely for the author reading the raw file.

T33D notes are plain-text files first. A consistent rule of "more is
fine, be generous" means authors never have to second-guess whether a
gap is too large. The rendered output is unaffected either way.


What "liberal" means in practice
----------------------------------

- One blank line after a heading before content: minimum
- Two blank lines before an H1 or H2: common and encouraged
- More than two: fine, especially at the top of a file or after a
  long code block
- Blank lines inside a code block: those are content, not spacing --
  leave them as-is

There is no house style requiring a specific count. The goal is that
when you open the raw file, section boundaries are immediately obvious
without syntax highlighting.
