<!-- markdownlint-disable MD013 MD041 -->

## Why

The `markdown2docx` skill currently applies a reference DOCX and then rewrites
the generated OOXML with a repository-specific Python script. This duplicates
style ownership, requires an additional runtime, and leaves the actual
reference-document contract undocumented even though Pandoc 3.11 can generate
the table of contents, list of figures, and list of tables directly.

## What Changes

- **BREAKING:** Move the canonical reference document from
  `openspec/publics/template.docx` to
  `.agents/skills/markdown2docx/references/template.docx` and remove the old
  duplicate asset.
- **BREAKING:** Require source Markdown to provide its document title through
  YAML metadata so Pandoc can map it to the Word `Title` style without OOXML
  post-processing.
- Invoke `pandoc` directly with `--reference-doc`, `--toc`, `--lof`, and
  `--lot`; do not invoke it through `mise`.
- Delete `scripts/format_docx.py` and make the reference DOCX the sole owner of
  fonts, styles, page layout, headers, footers, cover treatment, and list
  presentation.
- Add `references/style.md` that inventories the template's font and style
  mappings and explains the handling and field-refresh requirements for the
  cover, headers, footers, table of contents, list of figures, and list of
  tables.
- Update document-generation templates, tests, and maintained documentation to
  use the new title and reference-document contract.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `markdown2docx`: Changes the canonical reference path, source-title
  contract, direct Pandoc invocation, generated front matter, and style
  ownership while preserving same-name DOCX output and source retention.

## Impact

- Affects `.agents/skills/markdown2docx/`, the PRD and HLD Markdown templates,
  DOCX conversion tests, and documentation that names the old template or
  formatter.
- Removes the custom Python formatting runtime from this conversion path and
  retains Pandoc 3.11 as the only renderer dependency.
- Existing Markdown without YAML title metadata must be migrated before it can
  produce the documented cover-page layout.
- No external API or network service is added.

## Stakeholders and Lifecycle Impact

- **Acquisition:** No new dependency is acquired; the existing Pandoc 3.11
  installation becomes the complete conversion toolchain.
- **Supply:** Maintainers receive the reference DOCX and its written style
  contract together inside the skill that consumes them.
- **Transition:** Existing PRD and HLD templates and maintained Markdown are
  migrated to YAML title metadata, and callers must use the new reference path.
- **Operation:** Document generation becomes one direct Pandoc command followed
  by output, source-hash, field, and visual checks.
- **Maintenance:** Style changes are made in one reference DOCX and recorded in
  `references/style.md`; regression tests verify the resulting OOXML roles.
- **Disposal:** The formatter script and old public template are deleted after
  reference and caller searches confirm that no maintained path depends on
  them.

## Quality Considerations

- **QR-001 Functional suitability:** The measure is representative PRD and HLD
  conversions containing their title, identifiers, TOC, figure-list, and
  table-list fields; the target is 100% for both documents, verified by the
  conversion test and OOXML inspection.
- **QR-002 Compatibility:** The measure is retained required styles, page
  geometry, headers, and footers after direct Pandoc conversion; the target is
  100% of the documented template roles, verified structurally and by rendered
  page inspection.
- **QR-003 Maintainability:** The measures are conversion-specific executable
  scripts and canonical reference DOCX files; the targets are zero scripts and
  one reference file, verified by tracked-file and reference searches.
- **QR-004 Reliability:** The measure is source Markdown modified on successful
  or failed conversion; the target is zero bytes, verified by SHA-256 comparison
  and failure-path tests.
- **QR-005 Performance efficiency:** The measure is renderer invocations per
  document; the target is one Pandoc process with no formatting subprocess,
  verified by command and test inspection.
- **QR-006 Usability:** The measure is requested template concerns documented
  in `references/style.md`; the target is all eight categories, verified by a
  documentation checklist.
- **Security:** No credentials, macros, or external content are introduced;
  verification inspects the DOCX package and dependency diff.
- **Interaction capability:** Not applicable because the change adds no user
  interface.
- **Flexibility:** The template remains replaceable through Pandoc's standard
  `--reference-doc` interface; no additional target is needed.
- **Safety:** Not applicable because document conversion has no safety-related
  control function.
