<!-- markdownlint-disable MD041 -->

## Context

See `proposal.md` for motivation. The repository currently implements
`gen-pd`, `gen-bd`, and `md2docx`, stores the reference DOCX under
`openspec/document-templates/`, and has one completed but unarchived change
that documents those old names. Section 5 of `MySDD-Spec.md` instead defines
the target `generate-prd`, `generate-hld`, and `openspec/publics/` structure.
The user approved `markdown2docx` in place of the invalid
`_markdown2docx` Agent Skill name.

## Goals / Non-Goals

**Goals:**

- Make live documentation, OpenSpec assets, Agent Skills, and tests use the
  target names and paths consistently.
- Retain the existing behavior contracts while moving every accepted ADR
  decision into validated OpenSpec specifications.
- Make removal of the standalone ADR and obsolete live change contingent on
  explicit completeness checks.

**Non-Goals:**

- Rewriting historical content under `openspec/changes/archive/`.
- Adding PRD, HLD, or DOCX conversion to the MySDD artifact graph.
- Changing the spec-driven Delta Spec grammar or artifact dependencies.
- Editing section 5 of `MySDD-Spec.md` beyond the approved skill-name
  correction from `_markdown2docx` to `markdown2docx`.

## Decisions

### Use the target layout as a migration contract

Capture section 5 before editing and verify afterward that its only content
change is the approved skill-name correction. Rewrite all other sections to
describe `generate-prd`, `generate-hld`, `markdown2docx`, `prd`, `hld`, and
`openspec/publics/` consistently.

Alternative: derive the layout from the current implementation. Rejected
because the user explicitly designated the edited layout as authoritative.

### Migrate skills without compatibility aliases

Move the three live skills and their assets to the new directories, update
frontmatter names and references, and remove old directories. Do not retain
alias skills because they would leave two names as competing sources of truth.
`markdown2docx/SKILL.md` owns the Pandoc invocation directly; its former
skill-local scripts are removed because the authoritative layout lists only
the Skill definition.

Alternative: keep forwarding aliases or the existing scripts. Rejected because
both would contradict the target layout and the zero-old-live-name acceptance
criterion.

### Make `openspec/publics/` the document boundary

Move `reference.docx` to `openspec/publics/reference.docx`. Add a local
`.gitignore` that ignores generated DOCX files while explicitly retaining the
reference DOCX. `prd.md` and `hld.md` are Git-managed generated source
documents; their same-name DOCX files are distributable, reproducible, and
untracked.

Alternative: keep documents inside each change. Rejected because the target
layout defines one public output location and the generating skills accept a
change name only as input, not as their output root.

### Replace ADR prose with capability requirements

The following traceability map is the deletion gate for `docs/adr/ADR.md`:

<!-- markdownlint-disable MD013 -->
| ADR | Replacement capability and requirement |
| --- | --- |
| ADR-001 | `project-setup`: Setup uses ordinary user permissions |
| ADR-002 | `project-setup`: Setup documentation has minimum and extended levels |
| ADR-003 | `project-setup`: Project Agent Skills use one canonical location |
| ADR-004 | `project-setup`: Standard setup excludes MCP |
| ADR-005 | `mysdd-workflow`: Daily changes use the four-command workflow |
| ADR-006 | `mysdd-workflow`: Markdown is the document source of truth; `md2docx`: same-name conversion |
| ADR-007 | `mysdd-schema`: four standard artifacts and ISO viewpoints |
| ADR-008 | `generate-prd` and `generate-hld`: faithful document generation |
| ADR-009 | `mysdd-workflow`: Verification gates archive |
| ADR-010 | `generate-prd`, `generate-hld`, and `md2docx`: fixed interface and conversion behavior |
<!-- markdownlint-enable MD013 -->

Delete the ADR only after strict validation confirms these Delta Specs and a
search confirms that no live file links to `docs/adr/ADR.md`. The obsolete
`add-gen-pd-gen-bd` live change is then removed because its applicable contract
has been superseded by this validated change. Archived changes remain intact.

Alternative: copy the ADR file under `openspec/`. Rejected because that would
duplicate decisions rather than convert them into testable behavior contracts.

## Quality Attribute Design

- **QR-001 Functional suitability:** Use the table above as a 10-row
  traceability oracle. Validation evidence must show 10/10 decisions mapped and
  zero remaining live ADR links.
- **QR-002 Compatibility:** Validate the MySDD schema and templates with the
  OpenSpec CLI, validate the change strictly, and validate each renamed skill
  against Agent Skills naming rules.
- **QR-003 Maintainability:** Search live files outside archive for old names
  and paths. The target is zero matches except text that explicitly documents
  the migration or historical exclusions.
- **QR-004 Reliability:** Exercise successful and failing PRD/HLD conversions,
  compare Markdown hashes, and require 100% preservation plus failure reports.

## Lifecycle, Migration and Operations

- **Transition:** Update `MySDD-Spec.md` first, then move files, then update
  schema instructions and tests so each later edit follows the new contract.
- **Operation:** The four-command workflow and separate operation commits stay
  unchanged. Document skills remain explicit post-proposal actions.
- **Support:** Error messages use the new names and report missing change
  artifacts, reference DOCX, Pandoc, or output constraints.
- **Maintenance:** Future spec-driven updates compare the four-artifact graph
  and templates while preserving the renamed document boundary.
- **Disposal:** Remove old live skill directories, the obsolete live change,
  and the ADR only after replacement evidence passes. Keep archives unchanged.

## Risks / Trade-offs

- **[Existing callers use old skill names]** → Remove aliases deliberately and
  use repository-wide search to update every live caller in the same change.
- **[The reference DOCX move breaks conversion]** → Update the Skill contract
  and run successful and missing-reference conversion tests.
- **[ADR content is lost during deletion]** → Require both the explicit map and
  strict Delta Spec validation before deletion.
- **[Archived files retain old names]** → Treat archive content as immutable
  historical evidence and exclude it from live-name checks.
- **[Generated Markdown changes during tests]** → Use fixtures or restore
  generated public Markdown after comparison so tests do not conceal drift.

## Migration Plan

1. Snapshot section 5 and update every other section of `MySDD-Spec.md`; apply
   only the approved `markdown2docx` correction inside section 5.
2. Create `openspec/publics/`, move the reference DOCX, and establish local
   tracking rules for Markdown and generated DOCX.
3. Move and rewrite the three Agent Skills and their PRD/HLD template assets.
4. Update MySDD schema instructions, templates, configuration guidance, links,
   and tests to the new contract.
5. Validate the six Delta Specs, the schema, skills, document conversion, and
   live-name search.
6. Confirm all ten ADR mappings and no remaining live ADR links, then delete
   `docs/adr/ADR.md` and the superseded `add-gen-pd-gen-bd` live change.
7. Roll back by reverting this operation commit, which restores all moved
   paths, the prior Skill names, the ADR, and the old live change together.
