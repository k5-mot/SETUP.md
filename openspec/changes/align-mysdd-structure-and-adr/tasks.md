<!-- markdownlint-disable MD041 -->

## 1. Align the authoritative MySDD document

- [ ] 1.1 Capture section 5 of `docs/references/MySDD-Spec.md`, rewrite every
  other section for `generate-prd`, `generate-hld`, `markdown2docx`, `prd`,
  `hld`, and `openspec/publics/`, and verify a section comparison shows only
  the approved `_markdown2docx` to `markdown2docx` correction inside section 5.
- [ ] 1.2 Update the table of contents, diagrams, examples, validation steps,
  acceptance criteria, and references in `MySDD-Spec.md`, then verify Markdown
  lint passes and every documented live path resolves to the target layout.

## 2. Establish the public document boundary

- [ ] 2.1 Create `openspec/publics/`, move `reference.docx` into it, and add a
  local `.gitignore`; verify the reference DOCX and Markdown files are tracked
  while `prd.docx` and `hld.docx` are ignored.
- [ ] 2.2 Remove superseded global ignore patterns and old reference paths,
  then verify Git reports no live file under `openspec/document-templates/`
  and no generated public DOCX as trackable content.

## 3. Migrate the document Agent Skills

- [ ] 3.1 Replace `gen-pd` with `generate-prd`, rename `assets/rd.md` to
  `assets/prd.md`, target `openspec/publics/prd.md`, and verify the Skill
  metadata and directory name pass Agent Skills naming validation.
- [ ] 3.2 Replace `gen-bd` with `generate-hld`, rename `assets/bd.md` to
  `assets/hld.md`, target `openspec/publics/hld.md`, and verify the Skill
  metadata and directory name pass Agent Skills naming validation.
- [ ] 3.3 Replace `md2docx` with `markdown2docx`, move the Pandoc conversion
  contract into its `SKILL.md`, remove the obsolete skill-local scripts, and
  verify the directory contains only the target-layout files.
- [ ] 3.4 Exercise successful PRD and HLD conversion plus missing-input and
  renderer-failure cases; verify both DOCX files are non-empty on success and
  source Markdown hashes remain unchanged in every case (QR-004).

## 4. Align OpenSpec configuration and live assets

- [ ] 4.1 Update `openspec/schemas/mysdd/schema.yaml` and its four templates to
  use the new skill and document terms while retaining exactly the four
  spec-driven artifacts and `apply.requires: [tasks]`; verify verbose schema
  validation and resolved-template inspection pass (QR-002).
- [ ] 4.2 Review `openspec/config.yaml` against the target contract, preserve
  `schema: mysdd` and separate operation commit guidance, and verify a newly
  scaffolded inspection change resolves the MySDD schema without adding PRD or
  HLD artifacts.
- [ ] 4.3 Update live OpenSpec references outside archive to the new names and
  paths, then verify no runtime or canonical reference to `gen-pd`, `gen-bd`,
  `md2docx`, `rd.md`, `bd.md`, or `document-templates` remains outside explicit
  migration records (QR-003).

## 5. Implement the setup and workflow decisions

- [ ] 5.1 Reconcile `docs/manual/SETUP.md`, create or repair
  `docs/manual/SETUP.full.md`, and verify the minimum procedure uses ordinary
  PowerShell with user-scoped WinGet while the extended procedure reuses the
  minimum steps.
- [ ] 5.2 Verify project-specific skills exist only under `.agents/skills/`,
  standard setup contains no MCP installation, the documented daily workflow
  is propose/apply/verify/archive, and failed verification prevents archive.

## 6. Complete ADR migration and disposal

- [ ] 6.1 Validate all six Delta Specs strictly and check the design
  traceability table against ADR-001 through ADR-010; verify 10 of 10 decisions
  have at least one replacement requirement and scenario (QR-001).
- [ ] 6.2 Replace every live link to `docs/adr/ADR.md`, then verify a repository
  search outside archive returns zero live links before deleting
  `docs/adr/ADR.md`.
- [ ] 6.3 Remove the superseded `openspec/changes/add-gen-pd-gen-bd/` only
  after its applicable behavior is covered by validated replacement Specs;
  verify archived changes remain byte-for-byte untouched.

## 7. Final evidence

- [ ] 7.1 Run strict validation for `align-mysdd-structure-and-adr`, MySDD
  schema validation, Agent Skill validation, Markdown lint, link checks, and
  Git ignore checks; record zero validation errors as completion evidence.
- [ ] 7.2 Inspect the final diff for unrelated changes, generated files, and
  secrets, and verify the Apply commit contains only implementation changes
  for this Change.
