<!-- markdownlint-disable MD041 -->

## Why

The authoritative directory layout in `docs/references/MySDD-Spec.md` now
defines different skill names, document names, and output locations than the
rest of that document and the implemented OpenSpec assets. The accepted
decisions in `docs/adr/ADR.md` must also become testable OpenSpec requirements
before the standalone ADR file is removed.

## What Changes

- Treat section 5 of `MySDD-Spec.md` as authoritative, with the approved
  correction from `_markdown2docx` to `markdown2docx`, and align every other
  section without otherwise rewriting section 5.
- Rename the live document skills to `generate-prd`, `generate-hld`, and
  `markdown2docx`; rename their template assets and generated documents to
  `prd` and `hld`.
- Move the shared reference DOCX and generated documents to
  `openspec/publics/`, tracking Markdown and excluding generated DOCX files.
- Align the MySDD schema instructions, templates, configuration guidance,
  canonical specifications, tests, and live change material with the new
  names and paths. Historical archived changes remain immutable.
- Convert every accepted decision in `docs/adr/ADR.md` into an observable
  OpenSpec requirement, verify a complete ADR-to-requirement mapping, and only
  then delete the standalone ADR file.
- Remove the obsolete completed `add-gen-pd-gen-bd` live change after its
  still-applicable contracts are represented by this change.

## Capabilities

### New Capabilities

- `project-setup`: Defines the user-scoped PowerShell setup, two-level setup
  documentation, Agent Skill location, and explicit MCP exclusion.
- `mysdd-workflow`: Defines the four-command workflow, Markdown source of
  truth, generated DOCX policy, and verification gate before archive.
- `mysdd-schema`: Defines the spec-driven-compatible four-artifact MySDD
  schema with ISO lifecycle and product-quality viewpoints.
- `generate-prd`: Generates `openspec/publics/prd.md` and its distributable
  DOCX from MySDD change artifacts without inventing facts.
- `generate-hld`: Generates `openspec/publics/hld.md` and its distributable
  DOCX from MySDD change artifacts without inventing facts.

### Modified Capabilities

- `md2docx`: Renames the shared skill to `markdown2docx` and changes its
  reference document and allowed outputs to `openspec/publics/`.

## Impact

- `docs/references/MySDD-Spec.md` outside its authoritative directory-layout
  section
- `docs/adr/ADR.md`
- `openspec/config.yaml`, `openspec/schemas/mysdd/`, `openspec/specs/`,
  `openspec/publics/`, and non-archived `openspec/changes/`
- `.agents/skills/gen-pd/`, `.agents/skills/gen-bd/`, and
  `.agents/skills/md2docx/`, which migrate to the approved skill names
- Links, tests, ignore rules, and commands that use the old names or paths

## Stakeholders and Lifecycle Impact

- **Stakeholders:** Maintainers and AI agents receive one consistent contract;
  document consumers continue to receive PRD and HLD DOCX files.
- **Transition:** Live files and references are migrated atomically. Historical
  archived changes remain unchanged, while the obsolete live change is removed
  only after its contracts are captured here.
- **Operation:** Propose, apply, verify, and archive remain the standard daily
  workflow. Document generation stays outside the schema artifact graph.
- **Maintenance:** Fork-update and validation instructions are rewritten for
  the new skill names and public output location.
- **Disposal:** Old live skill directories, paths, and the standalone ADR are
  deleted only after replacement checks succeed; rollback restores the prior
  paths and ADR from Git.
- **Acquisition and supply:** Not applicable because the change introduces no
  procurement, supplier, or external delivery agreement.

## Quality Considerations

- **QR-001 Functional suitability:** Map 10 of 10 ADR decisions to at least one
  validated OpenSpec requirement and leave zero live references to the deleted
  ADR.
- **QR-002 Compatibility:** `openspec schema validate mysdd --verbose`, strict
  change validation, and Agent Skills naming validation must all pass.
- **QR-003 Maintainability:** Leave zero old live names or paths outside
  `openspec/changes/archive/`, with section 5 remaining the directory-layout
  source of truth.
- **QR-004 Reliability:** PRD and HLD conversion tests must preserve source
  Markdown and report every conversion failure.
- **Performance efficiency:** Not applicable; no runtime performance path is
  introduced.
- **Interaction capability:** Not applicable; no user interface changes.
- **Security:** Not applicable beyond preserving existing safe literal-path
  handling; no identity, authorization, or secret handling changes.
- **Flexibility:** Not separately applicable; reuse is covered by the shared
  conversion contract and does not require a new measurable target.
- **Safety:** Not applicable because the change controls documentation tooling
  and has no safety-related system behavior.
