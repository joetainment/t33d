Naming-Conventions
==================

Rules for naming files and folders in the t33d project. This document covers
separators, ordering, date schemes, and numeric prefixes.

See also:
- [[Style-Guide]] -- overall philosophy and document index
- [[Capitalization-in-Filenames-and-Headings]] -- title case and brand name rules


---

Word Separators in Filenames [FIRM]
====================================

**Use dashes (`-`) instead of spaces.**

Dashes are the standard word separator for files and folders. Spaces cause
problems in shells, URLs, and some tools. Underscores are common in code
but read poorly in rendered titles where tools replace separators with spaces.
Dashes are the most widely used convention for human-readable filenames.

```
✓  Naming-Conventions.md
✓  Scripting-and-Tools/
✗  Naming Conventions.md
✗  naming_conventions.md
```


Double-Dash Separator [SOFT]
============================

**Use `--` to separate structurally distinct parts of a filename.**
**Use `----` to separate structurally distinct sections of a filename that already contains the above-mentioned double dashes. (This should only be required in rare cases.)**

A single dash separates words within a phrase. A double dash separates major
components of a filename -- typically a prefix (ordering number or date) from
the title proper, or occasionally two clearly distinct title segments.

```
✓  01--Getting-Started.md        (number prefix -- title)
✓  2026-02-28--Meeting-Notes.md  (date prefix -- title)
✗  01-Getting-Started.md         (ambiguous: is "01" part of the title?)
```

This is a t33d-specific convention. The double-dash creates an unambiguous
visual and parseable boundary that a single dash cannot reliably provide,
especially since titles themselves contain dashes.

When needing separators, in order to separate entire already separated sections of the file name, more dashes in a row are used as larger separators, but use of this should be rare. The usual limit is 4 dashes; in very rare cases 8 might be okay. This is often used when there is an old file name we want to preserve one-to-one, but also want to use our new naming scheme.

**Potential issue to note with tools:** Some tools that replace dashes with
spaces for display will render the markdown  `01--Getting-Started`  as  `01  Getting Started`
meaning the output will contain a double space. In our case, this often looks better in the end result anyway, as the extra spaces increase readability and separation in the title the same way the dashes did in the filename. So, these extra spaces aren't necessarily a bad thing.
The double dashes converting to double spaces is a known occurrence. In the event it ever causes problems in a particular name, just avoid putting more than one dash continuously in that filename, dropping whatever additional dashes would normally be added.


---

Numeric Ordering [SOFT]
=======================

**Use zero-padded numeric prefixes followed by `--` when sequence matters.**

```
00--Index.md
01--Introduction.md
02--Setup.md
03--Core-Concepts.md
```

Rules:

- Always zero-pad to at least two digits (`01`, not `1`). The reason is that
  filesystems and tools sort filenames alphabetically, not numerically -- without
  padding, `10` sorts before `2` because `1` < `2` as a character. Zero-padding
  ensures lexicographic sort order matches intended numeric order. Use three digits
  (`001`) only if the folder will contain more than 99 items, which should be rare
  and may signal the folder needs splitting.
- Every file in an ordered folder should have a number prefix. Mixed
  ordered/unordered files in the same folder are confusing.
- The **same number may be shared** across multiple files when their relative
  order genuinely doesn't matter. Files sharing a number will sort
  alphabetically among themselves, which is acceptable.

```
01--Introduction.md
02--Setup-Mac.md        ← these two are
02--Setup-Windows.md    ← interchangeable order
03--First-Steps.md
```

- `00` is reserved for index, overview, or meta files that should always
  sort first within the folder regardless of content type. It is kept
  separate from `01` so that an index can always be added or removed
  without forcing a renumber of the remaining files.

**When not to use numeric ordering:** If you don't have a reason to read or
process the files in a specific sequence, don't add numbers. Alphabetical
order by meaningful title is cleaner and lower maintenance. Renumbering
is tedious and error-prone.


---

Date-Based Ordering [SOFT]
==========================

**Use ISO 8601 date prefixes followed by `--` when files are ordered by date.**

```
2026-02-28--Meeting-Notes.md
2026-03-01--Sprint-Kickoff.md
2026-03-15--Review-and-Retro.md
```

Date-prefixed files sort chronologically in any file browser automatically,
which is the primary advantage over numeric prefixes for time-series content.

Date Format
-----------

Use the ISO 8601 extended date format: `YYYY-MM-DD`

```
✓  2026-02-28
✗  28-02-2026   (ambiguous, non-standard)
✗  02-28-2026   (US format, ambiguous internationally)
✗  20260228     (basic format -- compact but harder to read)
```

Datetime Format [SOFT]
----------------------

When time precision is needed (rare -- log files, timestamped exports, etc.),
append the time in **basic format** (no colons, since colons are forbidden in
Windows filenames) directly after the date, separated by `T`:

```
2026-02-28T134500--Export-Draft.md
```

Breakdown: `YYYY-MM-DD` + `T` + `HHmmss` (hours, minutes, seconds, no separators)

This is a hybrid of ISO 8601 extended (date part) and basic (time part).
The reason this specific form emerged as the de facto standard for filenames
is straightforward: ISO 8601 extended format (`2026-02-28T13:45:00`) is the
most human-readable form, but colons are illegal in Windows filenames. The
basic format (`20260228T134500`) is legal everywhere but sacrifices the
readability of the date. The hybrid keeps the dashes in the date -- where they
add the most readability -- and drops the colons in the time -- where the
compactness is least harmful. The result sorts correctly, is cross-platform
legal, is immediately parseable by anyone familiar with ISO 8601, and is
the form you'll find recommended in documentation conventions, archival naming
standards, and developer tooling guides that address this constraint.

If second precision is unnecessary, hours and minutes alone are acceptable:

```
2026-02-28T1345--Export-Draft.md
```

Do not use colons in the time part of file or folder names under any circumstances -- they are
illegal in Windows filenames and will cause cross-platform issues.

```
✗  2026-02-28T13:45:00--Export-Draft.md   (colons -- Windows illegal)
✗  2026-02-28-T134500--Export-Draft.md    (dash before T -- non-standard)
✓  2026-02-28T134500--Export-Draft.md     (correct)
```


---

Choosing Between Numeric and Date Prefixes
==========================================

| Situation                                | Use            |
|------------------------------------------|----------------|
| Tutorial steps, ordered lessons          | `01--`, `02--` |
| Meeting notes, journals, logs            | `2026-02-28--` |
| Versioned drafts or exports              | `2026-02-28T1345--` |
| Reference docs with no inherent order    | No prefix      |
| Folder index / overview file             | `00--` or just `FolderName.md` |


In many cases, the numbers or the times/dates will be used as suffixes instead of prefixes, and the same logic generally applies there.




---

Folder Notes and README Files [FIRM]
=====================================

Each folder's canonical entry point is a file named after the folder itself:

```
Scripting/
    Scripting.md       ← canonical folder note (edit this)
    README.md          ← autogenerated copy for GitHub (do not edit)
```

`README.md` files are generated by `generate_readmes.py` and should not be
edited directly. They are mirrors of the folder note with an autogenerated
header prepended.

See [[Style-Guide]] for the autogeneration policy.


---

Summary of Separator Rules
===========================

| Pattern                        | Meaning                              |
|--------------------------------|--------------------------------------|
| `Word-Word`                    | Words within a phrase                |
| `Prefix--Title-Words`          | Structural boundary (number or date) |
| `2026-02-28--Title`            | Date-ordered file                    |
| `2026-02-28T134500--Title`     | Datetime-ordered file (rare)         |
| `01--Title`                    | Numerically ordered file             |
| `00--Title`                    | Index / always-first file            |