---
name: openspec-git-workflow
description: Run one OpenSpec propose, apply, verify, or archive workflow and commit only that successful phase without absorbing pre-existing changes.
---

# OpenSpec Git Workflow

Accept exactly one phase (`propose`, `apply`, `verify`, or `archive`) and one
`change-name`. Reject every other phase without changing the repository.

## Establish the boundary

From the repository root, record the current branch, `HEAD`, porcelain status
including untracked files, and unresolved paths. Treat this snapshot as the
pre-existing worktree. Stop immediately if Git already reports a conflict.

## Delegate the phase

Invoke the installed OpenSpec workflow matching the requested phase. Follow
that workflow completely; do not reproduce or bypass its instructions. The
delegated workflow's success or failure is authoritative.

- `propose`: use `openspec-propose`
- `apply`: use `openspec-apply-change`
- `verify`: use `openspec-verify-change`
- `archive`: use `openspec-archive-change`

If the delegated workflow fails, report its failure and create no commit.

## Isolate and inspect the result

After success, compare the new porcelain status with the baseline. Stop
without staging or committing if a phase-touched path was already changed at
baseline, Git reports a conflict, or phase ownership cannot be established.
Preserve every unrelated pre-existing change.

Stage only paths owned by this phase. Inspect the staged diff, tests, generated
files, and possible secrets as required by `AGENTS.md`. If the inspection
fails, unstage only the phase paths and report the reason.

## Commit the phase

Create exactly one Japanese Conventional Commit with gitmoji and the required
AI-assistance trailer. The subject MUST identify the phase and change. Use an
empty commit only when a successful `verify` phase changed no tracked file.

Never push, amend, reset, clean, rewrite history, or commit unresolved
conflicts. Report the commit ID and leave all pre-existing changes untouched.
