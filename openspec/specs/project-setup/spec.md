# project-setup Specification

## Purpose

Define a reproducible Windows setup contract that works without elevation and
keeps optional tools separate from the minimum project setup.

## Requirements

### Requirement: Setup uses ordinary user permissions

The project setup MUST run in a non-elevated PowerShell session and MUST use
WinGet with `--scope user` when the package supports user scope. This
requirement incorporates ADR-001.

For quality requirement QR-002 (compatibility), the measure is the number of
minimum setup commands requiring elevation, the target is zero, the condition
is a clean supported Windows user environment, and the verification method is
a command review and setup dry run.

#### Scenario: Install a user-scoped package

- **WHEN** a maintainer follows the minimum setup instructions
- **THEN** each supported WinGet install command includes `--scope user`
- **THEN** the procedure does not require an elevated PowerShell session

### Requirement: Setup documentation separates required and optional tools

The project MUST provide `docs/manual/SETUP.md` as the canonical setup
procedure. The document MUST distinguish required setup from optional tools,
and MUST treat the required setup as authoritative. This requirement
incorporates ADR-002.

#### Scenario: Choose the minimum setup

- **WHEN** a contributor needs only the required project tools
- **THEN** `docs/manual/SETUP.md` provides a complete minimum procedure
- **THEN** optional tools do not become minimum prerequisites

#### Scenario: Choose optional tools

- **WHEN** a contributor needs the additional supported tools
- **THEN** `docs/manual/SETUP.md` identifies them in separate optional sections
- **THEN** optional procedures do not duplicate the required setup

### Requirement: Project Agent Skills use one canonical location

Project-specific Agent Skills MUST reside under `.agents/skills/` and MUST NOT
be duplicated under `.github/` or `.roo/`. This requirement incorporates
ADR-003.

#### Scenario: Add or migrate a project skill

- **WHEN** a maintainer adds or migrates a project-specific Agent Skill
- **THEN** the skill exists under `.agents/skills/<skill-name>/`
- **THEN** no duplicate copy is added under `.github/` or `.roo/`

### Requirement: Only repository-owned skills are tracked

The repository MUST track exactly `generate-prd`, `generate-hld`,
`markdown2docx`, and `openspec-git-workflow` under `.agents/skills/`, plus the
local `.gitignore`. Every other locally installed Skill MUST be ignored and
MUST NOT be removed from a developer's working directory merely to untrack it.

#### Scenario: A third-party skill exists locally

- **WHEN** Git evaluates a Skill outside the four repository-owned names
- **THEN** `.agents/skills/.gitignore` excludes it from repository tracking
- **THEN** the local Skill remains available on the developer's filesystem

#### Scenario: A repository-owned skill changes

- **WHEN** a maintainer edits one of the four repository-owned Skills
- **THEN** Git reports that change as trackable

### Requirement: Standard setup excludes MCP

The standard setup procedures MUST NOT install or configure a Model Context
Protocol (MCP) integration. A consuming project MUST make its own explicit
decision before introducing MCP. This requirement incorporates ADR-004.

#### Scenario: Complete the canonical setup

- **WHEN** a contributor completes the required setup or an optional procedure
- **THEN** no MCP server or MCP client configuration is installed
- **THEN** the setup succeeds without MCP credentials or endpoints
