<!-- markdownlint-disable MD041 -->

## Purpose

Run one existing OpenSpec phase and record its successful result in a focused
Git commit without absorbing unrelated worktree changes.

## ADDED Requirements

### Requirement: Delegate each phase to the existing workflow

The `openspec-git-workflow` Agent Skill MUST accept one phase from `propose`,
`apply`, `verify`, or `archive` plus a change name and MUST invoke the installed
workflow for that phase instead of reimplementing OpenSpec behavior.

#### Scenario: Run an accepted phase

- **WHEN** a maintainer supplies a supported phase and change name
- **THEN** the wrapper records the worktree baseline and invokes that phase
- **THEN** the phase's own success or failure remains authoritative

#### Scenario: Reject an unsupported phase

- **WHEN** a caller supplies a phase outside the four accepted values
- **THEN** the wrapper reports the accepted values without changing the repo

### Requirement: Commit only successful isolated phase changes

After a phase succeeds, the wrapper MUST stage and commit only paths introduced
or changed by that phase. It MUST preserve pre-existing worktree changes and
MUST stop without committing when phase output overlaps a pre-existing changed
path or when Git reports a conflict.

For quality requirement QR-006 (security and integrity), the measure is the
number of unrelated paths included in a phase commit, the target is zero, the
conditions include clean, dirty, overlapping, and conflicted worktrees, and
the verification method is isolated-repository tests and staged-diff review.

#### Scenario: Unrelated changes predate the phase

- **WHEN** a successful phase changes paths disjoint from the recorded baseline
- **THEN** only the phase paths are staged and committed
- **THEN** every pre-existing change remains uncommitted

#### Scenario: Phase output overlaps a pre-existing path

- **WHEN** the phase changes a path already modified at baseline
- **THEN** the wrapper creates no commit and reports the overlapping path

### Requirement: Use project commit policy and verify checkpoints

The wrapper MUST create a Japanese Conventional Commit with gitmoji and the
required AI-assistance trailer after a successful phase. A successful `verify`
phase with no tracked changes MUST create an empty checkpoint commit.

#### Scenario: Apply changes tracked files

- **WHEN** Apply succeeds and produces isolated tracked changes
- **THEN** the wrapper creates one policy-compliant Apply commit

#### Scenario: Verify changes no tracked files

- **WHEN** Verify succeeds without a tracked file change
- **THEN** the wrapper creates one empty verification checkpoint commit

### Requirement: Preserve repository history and remotes

The wrapper MUST NOT push, amend an existing commit, rewrite history, or commit
while Git is conflicted. A failed OpenSpec phase MUST leave its files and every
pre-existing change uncommitted and MUST report the failure.

#### Scenario: OpenSpec phase fails

- **WHEN** the delegated phase reports failure
- **THEN** the wrapper creates no commit and reports the phase failure

#### Scenario: Repository is conflicted

- **WHEN** Git reports unresolved conflicts before commit
- **THEN** the wrapper creates no commit, push, amend, or history rewrite
