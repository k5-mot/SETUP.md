<!-- markdownlint-disable MD041 -->

## Purpose

Provide one canonical, verifiable coding policy for contributors and coding
agents across common concerns and the repository's supported languages.

## ADDED Requirements

### Requirement: The repository publishes one canonical coding policy

The repository MUST provide `CODING_RULES.md` as the canonical coding policy,
MUST organize it into common, Python, TypeScript, and Java sections, and MUST
require coding agents to follow it through `AGENTS.md`.

For quality requirement QR-001 (functional suitability), the measure is the
number of required policy sections present, the target is four of four, the
condition is the tracked repository state, and the verification method is
heading and content inspection.

#### Scenario: A contributor looks up coding guidance

- **WHEN** a contributor or coding agent starts an implementation task
- **THEN** `AGENTS.md` directs them to `CODING_RULES.md`
- **THEN** the policy contains common, Python, TypeScript, and Java guidance

### Requirement: The policy requires the simplest current implementation

The coding policy MUST require the smallest reasonable change that satisfies
the current request, MUST prohibit speculative abstraction and unnecessary
dependencies, and MUST preserve the repository's existing architectural level.
Recommended tools MUST remain optional until a concrete current need justifies
their use.

#### Scenario: A task can be completed without a new abstraction

- **WHEN** existing code or the current platform satisfies the requirement
- **THEN** the implementation reuses that capability
- **THEN** no hypothetical layer, service, factory, wrapper, interface, helper,
  or dependency is introduced

### Requirement: Comments explain configuration and complex intent

The coding policy MUST require explanatory comments for configuration values
whose purpose, unit, valid range, or selection rationale is not self-evident.
It MUST require comments at an appropriate level for complex algorithms,
branches, state transitions, or constraints, and MUST discourage comments that
only repeat obvious code behavior.

#### Scenario: A change introduces configuration or complex processing

- **WHEN** a contributor adds a configuration value or complex processing
- **THEN** comments explain the value's meaning or the processing intent and
  constraints at the point needed for maintenance
- **THEN** comments do not narrate self-evident statements line by line

### Requirement: Language guidance defines executable quality gates

The Python, TypeScript, and Java sections MUST define the minimum formatting,
linting or static-analysis, type-checking where applicable, and test commands
that a change must pass using the consuming project's existing toolchain.
Python guidance MUST additionally require direct script execution and
`time.perf_counter()` task timing for each Python file.

#### Scenario: A language-specific change is completed

- **WHEN** a contributor finishes a Python, TypeScript, or Java change
- **THEN** the applicable documented quality gates pass
- **THEN** the contributor records any unavailable gate instead of silently
  treating it as successful

### Requirement: Repository documentation remains lint-clean

All tracked Markdown MUST pass the documented repository-wide markdownlint
command. Intentional OpenSpec syntax, long generated tables, and HTML disclosure
blocks MAY use narrow rule suppressions, but structural list and whitespace
errors MUST be corrected rather than suppressed.

For quality requirement QR-003 (maintainability), the measure is tracked
Markdown lint findings, the target is zero, the condition is the complete set
returned by `git ls-files '*.md'`, and the verification method is
`markdownlint-cli2` over that set.

#### Scenario: Markdown quality is verified

- **WHEN** the repository-wide Markdown lint command runs on tracked files
- **THEN** it exits successfully with zero findings
- **THEN** OpenSpec validation still succeeds after any lint-only adjustments
