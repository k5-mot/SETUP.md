# mysdd-workflow Specification

## Purpose

Define the operational MySDD workflow, document source-of-truth policy, and
verification gate that every project change follows.

## Requirements

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
dedicated Git commit containing only that operation's changes. The timing for
creating each operation commit MUST be declared in `openspec/config.yaml`, and
the Git execution rules MUST be defined only in `CONTRIBUTING.md`. A successful
verify with no tracked file change MUST produce an empty verification checkpoint
commit. After archive succeeds and its commit is created, the current
`feature/*` branch MUST be merged into `main` after satisfying the Pull Request
and CI conditions defined in `CONTRIBUTING.md`.

For quality requirement QR-004 (reliability), the measure is the percentage of
successful operations recorded at the configured boundary and archived feature
branches integrated after the required gate, the target is 100%, the conditions
are normal completion, failure, no-change verification, and archive completion,
and the verification method is configuration inspection, Git history, and Pull
Request status review.

#### Scenario: A workflow operation succeeds

- **WHEN** propose, apply, verify, or archive completes successfully
- **THEN** the operation is committed at the timing declared for that operation
  in `openspec/config.yaml`
- **THEN** the commit follows `CONTRIBUTING.md`

#### Scenario: Verification changes no tracked files

- **WHEN** verification succeeds without modifying a tracked file
- **THEN** an empty commit records the successful verification boundary

#### Scenario: Verification fails

- **WHEN** verification completes with Critical or Warning findings
- **THEN** a verification checkpoint commit records the failure result
- **THEN** archive remains blocked until correction and successful verification

#### Scenario: Archive completes on a feature branch

- **WHEN** archive succeeds and its dedicated commit is created on a `feature/*`
  branch
- **THEN** the branch satisfies the Pull Request and CI conditions in
  `CONTRIBUTING.md`
- **THEN** the feature branch is merged into `main`

#### Scenario: A workflow operation fails

- **WHEN** propose, apply, or archive fails, or Git reports unresolved conflicts
- **THEN** no operation commit or archive-triggered merge is created
