<!-- markdownlint-disable MD041 -->

## Purpose

Keep MySDD compatible with the spec-driven artifact graph while adding
explicit ISO lifecycle and product-quality planning viewpoints.

## ADDED Requirements

### Requirement: MySDD preserves the four standard artifacts

The `mysdd` schema MUST preserve the `proposal`, `specs`, `design`, and `tasks`
artifact identifiers, outputs, and dependency graph from `spec-driven`.
`apply.requires` MUST remain `[tasks]`. This requirement incorporates the
compatibility portion of ADR-007.

#### Scenario: Inspect a MySDD change

- **WHEN** OpenSpec resolves a change using the `mysdd` schema
- **THEN** exactly the four standard planning artifacts are available
- **THEN** Apply becomes ready when `tasks` is complete

### Requirement: MySDD adds ISO viewpoints to planning artifacts

The `mysdd` schema instructions and templates MUST add applicable
ISO/IEC/IEEE 12207 lifecycle viewpoints and ISO/IEC 25010 product-quality
viewpoints to the four standard artifacts. Non-applicable viewpoints MUST be
recorded with reasons. This requirement incorporates ADR-007.

For quality requirement QR-002 (compatibility), the measure is successful
schema validation with the unchanged artifact graph, the target is 100%, the
condition is every schema update, and the verification method is verbose
OpenSpec schema validation and resolved-template inspection.

#### Scenario: Propose a MySDD change

- **WHEN** a maintainer proposes a change using `mysdd`
- **THEN** lifecycle impacts and applicable product-quality targets are
  captured in the standard planning artifacts
- **THEN** no PRD or HLD is generated as a schema artifact

### Requirement: Formal document generation remains outside the artifact graph

The `mysdd` schema MUST NOT define PRD, HLD, or DOCX conversion as artifacts.
It MUST describe `generate-prd` and `generate-hld` as separately invoked Agent
Skills that consume completed planning artifacts.

#### Scenario: Complete the proposal workflow

- **WHEN** all four MySDD planning artifacts are complete
- **THEN** OpenSpec reports planning complete without requiring PRD or HLD
- **THEN** a maintainer can invoke either document-generation skill separately
