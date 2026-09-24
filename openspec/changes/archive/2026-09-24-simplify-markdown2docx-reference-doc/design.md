<!-- markdownlint-disable MD013 MD041 -->

## Context

See `proposal.md` for the motivation. The current conversion path runs Pandoc
with `openspec/publics/template.docx`, then rewrites `document.xml`,
`styles.xml`, and `settings.xml` through `scripts/format_docx.py`.

The supplied `.agents/skills/markdown2docx/references/template.docx` already
contains the required A4 page geometry, first/default header and footer parts,
title and heading hierarchy, TOC styles, table and caption styles, and note
styles. A direct Pandoc 3.11 probe confirmed that `--toc`, `--lof`, and `--lot`
emit the three Word field blocks and that YAML `title` metadata maps to the
Word `Title` style. Pandoc uses reference-document styles and section
properties, but does not copy the reference document's sample body as a cover
shell.

## Goals / Non-Goals

**Goals:**

- Make one skill-local DOCX the only style and page-layout authority.
- Perform each conversion with one direct Pandoc process and no tracked
  formatter script.
- Preserve the cover, navigation lists, body-heading page breaks, tables,
  captions, notes, headers, and footers through reference styles and native
  Pandoc output.
- Document the exact boundary among source Markdown, Pandoc, the reference
  DOCX, and deferred Word field refresh.

**Non-Goals:**

- Do not build a general DOCX templating engine or copy arbitrary sample body
  content from the reference document.
- Do not add Microsoft Word or LibreOffice as a mandatory generation
  dependency.
- Do not generate synthetic figures or table captions when the Markdown has no
  corresponding Pandoc figure or captioned-table nodes.
- Do not retain two reference DOCX files or a compatibility wrapper for the old
  formatter command.

## Decisions

### Use the skill-local reference document as the only formatting authority

The canonical asset is
`.agents/skills/markdown2docx/references/template.docx`. The existing
`openspec/publics/template.docx` is deleted after every maintained reference is
updated. Keeping the asset beside `SKILL.md` makes the skill self-contained and
prevents generated public documents from being mixed with conversion assets.

The supplied DOCX is treated as the baseline. During implementation its
effective styles and first/default section properties are normalized only as
needed to satisfy the specification: 10-point body text, a vertically spaced
`Title`, page breaks before `TOC Heading` and `Heading 1`, centered table style,
the intended first/default headers and footers, and `w:updateFields=true`.
No tracked script is retained to perform this normalization at runtime.

Alternative considered: retain the public template and formatter. Rejected
because it preserves duplicated style ownership and the extra Python process.

### Give Pandoc a real title and native navigation-list options

PRD and HLD Markdown templates use a leading YAML metadata block with a
non-empty `title`; their former level-one document-title heading is removed and
body headings are promoted by one level. This lets Pandoc produce a `Title`
paragraph while keeping body chapters as `Heading 1`, without inspecting or
rewriting generated OOXML.

The skill runs one command equivalent to:

```powershell
# Convert canonical Markdown with the skill-local reference and native navigation fields.
pandoc '<input.md>' --from='gfm+implicit_figures' --to=docx --standalone --reference-doc='.agents/skills/markdown2docx/references/template.docx' --toc --toc-depth=6 --lof --lot --metadata='toc-title:目次' --metadata='lof-title:図一覧' --metadata='lot-title:表一覧' --output='<same-basename.docx>'
```

`--toc`, `--lof`, and `--lot` create Word fields. They do not calculate final
entries or page numbers. The reference settings mark fields dirty for refresh;
when Word is available, the existing `Ctrl+A`, `F9`, save workflow remains the
authoritative refresh step. Headless tests verify field instructions and the
update flag instead of claiming to refresh cached page numbers.

Alternative considered: infer the title from the first heading with a Lua or
Python filter. Rejected because YAML metadata is supported by the existing GFM
reader, is explicit, and avoids replacing one custom script with another.

### Document effective behavior rather than duplicating the DOCX

`references/style.md` is a Japanese maintainer guide. It records the final
template's effective values and, for each requested category, identifies the
owner and refresh behavior:

- fonts and styles: named Word style, Latin/East Asian font, size, spacing,
  numbering, and page-break behavior;
- headers and footers: first/default selection, literal text, and fields;
- cover: YAML `title` to Word `Title`, with the reference body explicitly not
  copied by Pandoc;
- TOC, figure list, and table list: generating flag, heading, field code,
  source-content prerequisite, and refresh procedure.

The DOCX remains normative for binary formatting values; `style.md` is the
reviewable inventory and maintenance contract. Any template change must update
the inventory in the same change.

### Replace formatter assertions with output-contract tests

The conversion regression test calls `pandoc` directly for PRD and HLD using
the documented flags. It compares source hashes and inspects the generated
package for the `Title` paragraph, representative IDs, three navigation field
codes, field-update setting, required styles, page-break rules, table style,
and repeating table headers. Repository searches assert that neither the old
template path nor `format_docx.py` remains in maintained files.

Structural checks are deterministic in CI. A local apply/verify pass also
renders representative documents and inspects every page when an approved
DOCX renderer is available; rendering is evidence in addition to, not a
replacement for, package inspection.

## Quality Attribute Design

- **QR-001 Functional suitability:** Native Pandoc fields and explicit YAML
  titles replace formatter-generated front matter. Evidence is two successful
  conversions with representative identifiers and all required field codes.
- **QR-002 Compatibility:** Word style IDs and OOXML section/header/footer
  relationships remain the compatibility boundary. Evidence is package
  inspection plus rendered PRD and HLD pages.
- **QR-003 Maintainability:** One template and zero runtime formatter scripts
  eliminate parallel style definitions. Evidence is tracked-file and reference
  search.
- **QR-004 Reliability:** Literal-path validation happens before conversion,
  output is accepted only when non-empty, and source SHA-256 is compared before
  and after. Failure tests verify unchanged sources.
- **QR-005 Performance efficiency:** Each document uses one renderer process.
  Tests log elapsed time but set no document-duration service level.
- **QR-006 Usability:** `style.md` maps all eight requested categories to their
  controlling style or field behavior. Evidence is checklist review against
  the final DOCX package.

## Lifecycle, Migration and Operations

- **Transition:** Migrate PRD/HLD authoring assets and maintained Markdown to
  YAML titles before switching the conversion command. Update all callers,
  tests, and documentation in the same commit set.
- **Operation:** A conversion validates paths and title metadata, records the
  source hash, invokes Pandoc once, validates the output, optionally refreshes
  fields in Word, and reports the absolute output path.
- **Support:** `style.md` is the first troubleshooting reference; package
  inspection distinguishes template defects from stale Word fields.
- **Maintenance:** Template and style inventory changes are reviewed together,
  and representative conversions protect the public contract.
- **Disposal:** Remove the formatter and public template only after a full
  repository reference search and direct-conversion tests pass.

## Risks / Trade-offs

- **[Risk] Pandoc does not copy the reference document's sample cover body.**
  → Use YAML title metadata and `Title`/`TOC Heading` style page breaks; state
  this boundary explicitly in `style.md`.
- **[Risk] TOC, figure-list, table-list, page, or date fields can display stale
  cached values before a Word refresh.** → Set `w:updateFields=true`, retain the
  documented Word refresh step, and test field instructions structurally.
- **[Risk] A figure or table list is empty when Markdown does not produce
  captioned Pandoc nodes.** → Document the prerequisite and treat an empty list
  as correct for a document without matching captions.
- **[Risk] Moving the template and changing title syntax breaks old callers.**
  → Update every maintained caller and source template atomically and fail early
  on missing YAML title metadata.
- **[Trade-off] Pandoc repeats table header rows by default.** → Adopt that
  accessible native behavior instead of preserving a formatter-only rule that
  would require post-processing.

## Migration Plan

1. Inventory and normalize the supplied skill-local reference DOCX, then write
   `references/style.md` from the final package evidence.
2. Migrate PRD/HLD Markdown templates and maintained public Markdown to YAML
   titles with level-one body chapters.
3. Switch `SKILL.md`, tests, and documentation to the direct Pandoc command and
   skill-local reference path.
4. Run direct conversions, structural checks, skill validation, repository
   quality checks, and available render inspection.
5. Delete `scripts/format_docx.py` and `openspec/publics/template.docx`, then
   confirm no maintained reference remains.

Rollback restores the prior public template, formatter, Markdown heading
levels, command sequence, tests, and documentation together. The source
Markdown remains the canonical content throughout the migration.
