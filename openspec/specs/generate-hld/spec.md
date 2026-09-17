# generate-hld Specification

## Purpose

Generate a traceable high-level design document from MySDD artifacts while
keeping generated content faithful to the supplied source material.

## Requirements

### Requirement: Generate the HLD from a named change

The `generate-hld` Agent Skill MUST accept a `change-name`, read that change's
`proposal.md`, one or more `specs/**/*.md` files, and `design.md` when present,
apply `.agents/skills/generate-hld/assets/hld.md`, and write
`openspec/publics/hld.md`. It MUST then delegate DOCX conversion to
`markdown2docx`. This requirement incorporates the HLD portions of ADR-008 and
ADR-010.

#### Scenario: Required artifacts exist

- **WHEN** a maintainer invokes `generate-hld` with a valid change name
- **THEN** the skill writes `openspec/publics/hld.md` from the change artifacts
- **THEN** it requests generation of `openspec/publics/hld.docx`

#### Scenario: Design is absent

- **WHEN** the named change validly omits `design.md`
- **THEN** the skill generates the HLD from proposal and delta specs
- **THEN** design-specific unresolved content is marked `TBD`

### Requirement: Preserve source facts and traceability

The `generate-hld` skill MUST preserve available capability paths,
requirement headings, scenario names, requirement and design identifiers,
quality targets, ADR content, and risk relationships. It MUST NOT introduce a
design fact absent from its inputs and MUST mark required but unresolved
content as `TBD`. This requirement incorporates the no-invention consequence
of ADR-008.

For quality requirement QR-001 (functional suitability), the measure is the
percentage of sampled requirement and design identifiers retained in the HLD,
the target is 100%, the condition is a fixture containing identifiers and
missing design content, and the verification method is generated-document
comparison.

#### Scenario: A required section lacks source information

- **WHEN** the HLD template requires information absent from the artifacts
- **THEN** the generated section contains `TBD`
- **THEN** no inferred design fact is presented as confirmed

### Requirement: Preserve Markdown on conversion failure

The `generate-hld` skill MUST retain a successfully generated `hld.md` when
DOCX conversion fails and MUST report partial success with the conversion
failure reason. This requirement incorporates the failure behavior in ADR-010.

#### Scenario: DOCX conversion fails

- **WHEN** `markdown2docx` fails after `hld.md` is complete
- **THEN** `openspec/publics/hld.md` remains unchanged
- **THEN** the skill reports partial success and the failure reason
