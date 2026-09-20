<!-- markdownlint-disable MD013 MD041 -->

## Context

See `proposal.md` for motivation. The repository currently has one Python
formatter script, no TypeScript or Java source, no markdownlint configuration,
and several Markdown constructs that are intentional but rejected by the
default linter. The requested Python dependency list is guidance for future
projects, not authorization to install every package in this repository.

## Goals / Non-Goals

**Goals:**

- Establish one concise coding-policy document with four required sections.
- Preserve the supplied simplicity rules and Python quality configuration in a
  form that does not force unused dependencies onto every project.
- Define comments by maintenance value: configuration meaning and complex
  intent or constraints, without line-by-line narration of obvious code.
- Reach zero tracked Markdown findings with narrow, explainable suppressions.
- Remove only the verified merged local branch.
- Add one Ubuntu CI job covering the agreed repository quality checks.
- Resolve CI, log, and release policy without adding an operations stack.

**Non-Goals:**

- Execute the Windows setup procedure in CI.
- Create a release tag or production observability stack.
- Rewrite published commits to add missing historical trailers.
- Add Python, TypeScript, or Java dependencies to this repository.
- Reformat unrelated source files or redesign existing architecture.

## Decisions

### Use one root-level policy document

`CODING_RULES.md` will be the only coding-policy source. `AGENTS.md` will link
to it with a MUST requirement. A single document is preferred over separate
language files because the policy is short and has one audience.

### Treat the Python package list as a recommendation catalog

The document will list `playwright`, `polars`, `uv`, `ruff`, `ty`, `httpx`,
`typer`, and `pydantic` as recommended choices when the current task needs the
corresponding capability. The supplied `pyproject.toml` content will be shown
as an adaptable reference, and its large dependency list will not become a
mandatory baseline. This resolves the conflict between YAGNI and unconditional
installation of unused packages.

### Translate simplicity guidance into normative Japanese

The common section will preserve the supplied meaning while using the RFC 8174
keywords required by `DOCUMENTATION_RULES.md`. The heading will retain the
English term in parentheses for discoverability.

### Keep language gates toolchain-aware

Python will use `uv`, Ruff, ty, and pytest when applicable. TypeScript and Java
will require the repository's existing package manager or build tool rather
than mandating new dependencies. TypeScript will require strict type checking;
Java will require the configured compiler, formatter or static analysis, and
tests.

### Use one Ubuntu quality job

`.github/workflows/quality.yml` will run on pull requests and pushes to `main`.
It will use one `quality` job on `ubuntu-latest`; a platform matrix is deferred
because only the repository artifacts and cross-platform document tooling need
automated validation. The Windows setup manual remains reviewed documentation,
not an executable CI contract.

### Keep regression checks dependency-light

One directly executable standard-library Python script will verify local
Markdown links. A second directly executable script will use the real Pandoc
and formatter commands against temporary copies of PRD and HLD inputs. It will
assert non-empty output, representative identifiers, and unchanged source
hashes. No mock, pytest dependency, or checked-in generated DOCX is required.

### Use GitHub Actions logs and manual releases

Each command will be a named workflow step so the standard job log identifies
failures. Retention follows the repository setting; no dashboard, alert, or
on-call integration is added. Maintainers create SemVer tags manually only
after `quality` succeeds for the target `main` commit.

### Fix lint structure and suppress only intentional syntax

`docs/manual/SETUP.md` list indentation and excess blank lines will be fixed.
MD013 and MD033 will be disabled only where long commands or `<details>` blocks
are intentional. OpenSpec public documents and templates may disable the rules
that conflict with generated tables or required template headings. No global
markdownlint configuration will be added.

### Keep Git cleanup non-rewriting

Before deletion, `git merge-base --is-ancestor docs/mysdd-workflow main` must
succeed and `main...docs/mysdd-workflow` must show zero branch-only commits.
The local branch can then be deleted with `git branch -d`. No tag is created
until CI exists and passes, and published commits are not amended or rebased.

## Quality Attribute Design

| Quality ID | Design approach | Trade-off | Verification evidence |
| --- | --- | --- | --- |
| QR-001 | Four explicit policy sections and an `AGENTS.md` link | One longer file | Heading and link inspection |
| QR-002 | Preserve OpenSpec syntax and validate strictly | Narrow lint suppressions remain | Schema, spec, and change validation |
| QR-003 | Zero Markdown findings and one Ubuntu quality job | Generated tables keep long lines; Windows setup is review-only | Workflow inspection and local equivalent run |
| QR-004 | Delete only an ancestor branch; preserve history | Historical trailers remain missing | Branch ancestry and Git log |
| QR-005 | Add no credentials or mandatory packages | Recommendations require judgment | Diff and dependency-file inspection |

## Lifecycle, Migration and Operations

Contributors transition by following the new `AGENTS.md` link on their next
coding task. Existing code does not require a bulk migration. Maintainers update
the one policy document when supported-language expectations change. The local
branch deletion is recoverable from `main` because it has no unique commits.
CI operation uses GitHub Actions standard logs. Runtime operations and support
are not affected.

## Risks / Trade-offs

- [A reference dependency list is mistaken for mandatory installation] → Label
  it as adaptable and retain the rule that dependencies require a current need.
- [Lint suppressions hide structural defects] → Limit suppressions to intentional
  long lines, HTML, and OpenSpec template syntax; fix list and blank-line errors.
- [Rules for absent TypeScript or Java projects become speculative] → State only
  minimum gates and defer exact commands to each project's existing toolchain.
- [Branch cleanup loses work] → Require ancestry and unique-commit checks before
  `git branch -d`.
- [Ubuntu CI is mistaken for Windows setup validation] → State explicitly in
  the workflow contract and documentation that setup remains review-only.
- [Unpinned tool drift breaks CI] → Pin the major action versions and exact CLI
  versions used by validation steps.

## Migration Plan

1. Add `CODING_RULES.md` and link it from `AGENTS.md`.
2. Apply the smallest Markdown lint fixes and local rule suppressions.
3. Add the regression scripts and `ubuntu-latest` quality workflow.
4. Run markdownlint, OpenSpec validation, Python checks, and DOCX regression.
5. Verify branch ancestry and delete `docs/mysdd-workflow` locally.

Rollback consists of reverting tracked documentation changes. The deleted local
branch can be recreated at its recorded commit, which remains an ancestor of
`main`.
