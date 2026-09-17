<!-- markdownlint-disable MD041 -->

## Purpose

Define the operational MySDD workflow, document source-of-truth policy, and
verification gate that every project change follows.

## ADDED Requirements

### Requirement: Daily changes use the four-command workflow

The standard MySDD workflow MUST execute `propose`, `apply`, `verify`, and
`archive` in that order. Other OpenSpec commands MAY support exceptional or
optional maintenance but MUST NOT replace the standard sequence. This
requirement incorporates ADR-005.

#### Scenario: Complete a normal change

- **WHEN** a maintainer processes a normal MySDD change
- **THEN** the change is proposed before implementation
- **THEN** implementation is verified before the change is archived

### Requirement: Markdown is the document source of truth

Requirements, designs, verification evidence, PRD, and HLD content MUST use
Git-managed Markdown as their source of truth. DOCX files MUST be generated
from Markdown, MUST NOT be edited as a source, and MUST remain outside Git
tracking. This requirement incorporates ADR-006.

For quality requirement QR-003 (maintainability), the measure is the number of
tracked generated DOCX files and DOCX-only content changes, the target is zero,
the condition is document generation and review, and the verification method
is `git status` plus source/output comparison.

#### Scenario: Publish a distributable document

- **WHEN** a PRD or HLD is ready for distribution
- **THEN** its Markdown source is tracked by Git
- **THEN** its DOCX is regenerated from that Markdown and remains untracked

### Requirement: Verification gates archive

A change MUST pass OpenSpec verification and the configured CI checks for
traceability and evidence before archive. A failed check MUST prevent archive
until the failure is corrected and verification is repeated. This requirement
incorporates ADR-009.

For quality requirement QR-001 (functional suitability), the measure is the
percentage of archived changes with successful OpenSpec and CI verification,
the target is 100%, the condition is every archive attempt, and the
verification method is the verification report and CI result.

#### Scenario: Verification succeeds

- **WHEN** OpenSpec verification and every required CI check pass
- **THEN** the change is eligible for archive

#### Scenario: Verification fails

- **WHEN** OpenSpec verification or a required CI check fails
- **THEN** the change is not archived
- **THEN** verification is repeated after corrective changes

### Requirement: Workflow operations have separate commit boundaries

Successful propose, apply, verify, and archive operations MUST each produce a
dedicated Git commit containing only that operation's changes. A successful
verify with no tracked file change MUST produce an empty verification
checkpoint commit.

#### Scenario: Verification changes no tracked files

- **WHEN** verification succeeds without modifying a tracked file
- **THEN** an empty commit records the successful verification boundary
