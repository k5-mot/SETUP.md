<!-- markdownlint-disable MD041 -->

## Context

See `proposal.md` for motivation. The current repository has four overlapping
surfaces: a Git wrapper Skill, Git rules in `CONTRIBUTING.md` and `AGENTS.md`,
and operation timing in `openspec/config.yaml`. OpenSpec 1.13.0 accepts
operation-specific guidance only for `apply` and `archive`, while the `context`
field is supplied to every artifact and supported operation workflow.

The active Main Specs require both the wrapper Skill and four separate Phase
commits. Retiring the Capability therefore requires removing every Requirement
and setting `retire_capabilities: true`; archived Change history remains
immutable.

## Goals / Non-Goals

**Goals:**

- Establish `CONTRIBUTING.md` as the only normative source for Git mechanics.
- Establish `openspec/config.yaml` as the only runtime instruction source for
  OpenSpec operation commit and post-archive merge timing.
- Preserve isolated Phase commits, including successful and failed Verify
  checkpoints, without a wrapper Skill.
- Merge an archived `feature/*` branch into `main` only after the repository's
  Pull Request and CI gates are satisfied.
- Remove current documentation and tracking references to the retired Skill.

**Non-Goals:**

- Rewrite archived Changes or published Git history.
- Change the four-command MySDD sequence or OpenSpec schema graph.
- Introduce a custom executable, hook, dependency, or CI workflow for Git
  automation.
- Bypass the existing Pull Request, CI, review, or merge-commit rules.

## Decisions

### Split policy content from operation timing

`CONTRIBUTING.md` will own commit format, AI-assistance metadata, human author
identity, worktree isolation, staging, conflict handling, history protection,
push, Pull Request, and merge rules. `AGENTS.md` will retain only its existing
requirement to follow `CONTRIBUTING.md`; its duplicate Git-specific bullets will
be removed.

`openspec/config.yaml` will retain one reference to `CONTRIBUTING.md` and will
define exactly when Propose, Apply, Verify, and Archive results are committed.
The same `context` will define that Archive first creates its dedicated commit
and then starts the gated `feature/*` to `main` integration. The existing
`operations.apply` and `operations.archive` entries will be removed so timing
is not duplicated within the configuration.

This uses `context` rather than adding `operations.propose` or
`operations.verify`, because OpenSpec 1.13.0 supports only `apply` and `archive`
operation IDs. Adding unknown IDs would be ignored with a warning.

Alternative considered: keep the wrapper as an enforcement layer. Rejected
because it preserves the duplicate source and direct Skill dependency the
change is intended to remove.

### Keep Phase results isolated without a wrapper

Each operation reads the shared timing context and applies the Git mechanics
from `CONTRIBUTING.md`. The contributor or Coding Agent records a baseline,
stages only operation-owned paths, reviews the staged diff, runs applicable
checks, and commits only after the operation reaches its configured boundary.
Propose, Apply, and Archive failures do not create success commits. Verify
always records its completed result; a no-change result uses an empty commit and
the message identifies success or failure.

Alternative considered: combine all OpenSpec work into one Archive commit.
Rejected because it removes Phase traceability and conflicts with the retained
`mysdd-workflow` Requirement.

### Treat post-archive integration as a gated continuation

The Archive timing entry will require the Archive commit before integration.
Normal push, Pull Request creation or update, CI completion, and merge are then
performed under `CONTRIBUTING.md`. The target is always `main`, the source must
match `feature/*`, and the existing merge-commit rule remains authoritative.
Failure to satisfy the gate leaves the feature branch unmerged rather than
bypassing the rule.

Alternative considered: merge locally immediately after moving the Change.
Rejected because it would bypass the mandatory Pull Request and CI gate.

### Retire the Skill Capability and update living documents only

The tracked Skill file and its `.gitignore` exceptions will be removed. The
Main Spec Capability is retired during archive after all four Requirements are
removed. `project-setup` will list exactly three repository-owned Skills, and
`mysdd-workflow` will retain Phase boundaries while naming the two canonical
sources.

Living PRD, HLD, and MySDD reference content will describe configuration-driven
timing instead of the wrapper. Archived Change artifacts remain unchanged as
historical evidence.

## Quality Attribute Design

- **QR-001 Functional suitability:** Four operation timings and the Archive
  integration timing are present in one Config context. Evidence is Config and
  instruction-output inspection.
- **QR-002 Maintainability:** Current Skill, Spec, setup allowlist, and living
  document references are removed. Evidence is targeted repository search that
  excludes archived Change history and the retirement Delta itself.
- **QR-003 Compatibility:** The Config uses only supported fields, all Delta
  Specs remain valid, and the three retained Skills stay tracked. Evidence is
  strict OpenSpec validation, Markdown lint, and Git ignore checks.
- **QR-004 Reliability:** Failed gates cannot trigger an Archive merge, while
  completed Verify results remain traceable. Evidence is Scenario review and
  Git history inspection during Verify.
- **QR-005 Security:** Staged-path isolation, conflict refusal, non-AI author
  identity, and history protection move to one common policy. Evidence is
  staged diff and commit metadata review.

## Lifecycle, Migration and Operations

- **Transition:** Add the common Git rules before deleting the wrapper; update
  Config timing and living documents in the same Apply commit.
- **Operation:** Direct OpenSpec workflows consume Config context and apply the
  shared Git policy. Archive continues through the gated merge only after its
  own commit succeeds.
- **Support:** If a locally installed retired Skill remains, `.gitignore`
  treats it as third-party and leaves it on disk without tracking it.
- **Maintenance:** Future Git mechanics change only in `CONTRIBUTING.md`; future
  OpenSpec timing changes only in `openspec/config.yaml`.
- **Disposal:** Archive sync deletes the retired Main Spec Capability. Historical
  archived artifacts and published commits are preserved.

## Risks / Trade-offs

- **[Risk] Config context is prompt guidance rather than executable Git
  automation.** → Keep every timing statement explicit and verify the rendered
  instruction inputs for Propose, Apply, Verify, and Archive-compatible paths.
- **[Risk] Archive-triggered integration waits on remote CI.** → Treat the gate
  as part of post-archive completion and leave the branch unmerged on failure.
- **[Risk] Broad text replacement could alter historical evidence.** → Limit
  edits to living documents, Main Specs, configuration, and tracked Skill
  metadata; exclude `openspec/changes/archive/`.
- **[Trade-off] Removing the wrapper eliminates one procedural enforcement
  layer.** → Replace it with one shared policy and one shared timing context,
  reducing drift at the cost of relying on workflow agents to honor context.

## Migration Plan

1. Expand `CONTRIBUTING.md` with the Git rules formerly owned by the wrapper and
   move the AI trailer and author identity rules from `AGENTS.md`.
2. Replace duplicated Git directives in `openspec/config.yaml` with one policy
   reference and explicit timings for all four operations plus post-Archive
   integration.
3. Remove the wrapper Skill and its repository-owned `.gitignore` exceptions.
4. Update the living Specs, PRD, HLD, and MySDD reference documentation.
5. Validate Config instruction rendering, strict OpenSpec content, Markdown,
   links, Git ignore behavior, and repository tests.
6. During Archive, sync the Delta Specs, retire the wrapper Capability, commit
   the Archive, then complete the gated `feature/*` to `main` integration.

Rollback before merge restores the deleted Skill and reverts the policy,
Config, Specs, and living documents in one operation-scoped commit. After merge,
use a normal revert commit; do not rewrite published history.
