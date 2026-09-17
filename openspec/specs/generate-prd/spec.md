# generate-prd Specification

## Purpose

Generate a traceable product requirements document from MySDD artifacts while
keeping generated content faithful to the supplied source material.

## Requirements

### Requirement: Generate the PRD from a named change

The `generate-prd` Agent Skill MUST accept a `change-name`, read that change's
`proposal.md` and one or more `specs/**/*.md` files, apply
`.agents/skills/generate-prd/assets/prd.md`, and write
`openspec/publics/prd.md`. It MUST then delegate DOCX conversion to
`markdown2docx`. This requirement incorporates the PRD portions of ADR-008 and
ADR-010.

#### Scenario: Required artifacts exist

- **WHEN** a maintainer invokes `generate-prd` with a valid change name
- **THEN** the skill writes `openspec/publics/prd.md` from the change artifacts
- **THEN** it requests generation of `openspec/publics/prd.docx`

#### Scenario: Required artifacts are missing

- **WHEN** the proposal or every delta spec is missing
- **THEN** the skill reports the missing input
- **THEN** it does not report successful PRD generation

### Requirement: Preserve source facts and traceability

The `generate-prd` skill MUST preserve available capability paths,
requirement headings, scenario names, identifiers, quality targets, and
verification methods. It MUST NOT introduce a fact absent from its inputs and
MUST mark required but unresolved content as `TBD`. This requirement
incorporates the no-invention consequence of ADR-008.

For quality requirement QR-001 (functional suitability), the measure is the
percentage of sampled source identifiers retained in the PRD, the target is
100%, the condition is a fixture containing identifiers and missing content,
and the verification method is generated-document comparison.

#### Scenario: A required section lacks source information

- **WHEN** the PRD template requires information absent from the artifacts
- **THEN** the generated section contains `TBD`
- **THEN** no inferred fact is presented as confirmed

### Requirement: Preserve Markdown on conversion failure

The `generate-prd` skill MUST retain a successfully generated `prd.md` when
DOCX conversion fails and MUST report partial success with the conversion
failure reason. This requirement incorporates the failure behavior in ADR-010.

#### Scenario: DOCX conversion fails

- **WHEN** `markdown2docx` fails after `prd.md` is complete
- **THEN** `openspec/publics/prd.md` remains unchanged
- **THEN** the skill reports partial success and the failure reason
