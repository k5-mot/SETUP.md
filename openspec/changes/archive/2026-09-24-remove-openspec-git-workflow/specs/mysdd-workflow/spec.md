<!-- markdownlint-disable MD013 MD022 MD032 MD041 -->

## MODIFIED Requirements

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
