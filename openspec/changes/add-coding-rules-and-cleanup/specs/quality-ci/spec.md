<!-- markdownlint-disable MD041 -->

## Purpose

Provide a reproducible Ubuntu-based quality gate for repository changes while
keeping the reviewed Windows setup procedure outside automated execution.

## ADDED Requirements

### Requirement: Pull requests and main updates run one quality workflow

The repository MUST run `.github/workflows/quality.yml` for pull requests and
pushes to `main`. The workflow MUST contain a `quality` job on `ubuntu-latest`
that validates OpenSpec, tracked Markdown, local Markdown links, Python quality,
and DOCX conversion behavior. It MUST NOT execute the Windows setup procedure.

For quality requirement QR-003 (maintainability), the measure is defined CI checks
completed in one run, the target is all checks passing, the condition is a pull
request or push to `main`, and the verification method is workflow inspection
and a local equivalent run.

#### Scenario: A pull request changes repository content

- **WHEN** GitHub Actions receives a pull request event
- **THEN** the `quality` job runs on `ubuntu-latest`
- **THEN** every defined quality check must pass for the job to succeed
- **THEN** the Windows setup procedure is not executed

#### Scenario: Main receives an update

- **WHEN** a commit is pushed to `main`
- **THEN** the same `quality` job runs without a separate platform matrix

### Requirement: DOCX regression checks preserve source Markdown

The quality workflow MUST convert representative PRD and HLD Markdown through
Pandoc and the public formatter command, MUST verify non-empty DOCX output and
representative document identifiers, and MUST verify that each source Markdown
SHA-256 hash remains unchanged.

#### Scenario: Representative documents are converted

- **WHEN** the DOCX regression command runs with Pandoc available
- **THEN** both representative outputs are non-empty DOCX files
- **THEN** each output contains its representative identifier
- **THEN** each source Markdown hash is unchanged

### Requirement: CI uses standard logs without a separate operations stack

The workflow MUST write command output and failure details to standard GitHub
Actions job logs. The repository MUST NOT add a separate dashboard, alert
destination, log store, credential, or on-call process for this documentation
and tooling project. Log retention MUST follow the repository's GitHub Actions
setting rather than being duplicated in workflow code.

#### Scenario: A quality command fails

- **WHEN** a command in the `quality` job exits unsuccessfully
- **THEN** the job fails and its standard log identifies the failed step
- **THEN** no external monitoring credential or notification is required

### Requirement: Releases use manual SemVer tags after quality succeeds

A maintainer MUST create release tags manually in `v<MAJOR>.<MINOR>.<PATCH>`
format only after the `quality` job succeeds for the target `main` commit. The
repository MUST NOT create a release tag automatically in this change.

#### Scenario: A maintainer prepares a release

- **WHEN** the target `main` commit has a successful `quality` job
- **THEN** a maintainer may create the corresponding Semantic Versioning tag
- **THEN** the release process does not rewrite published history
