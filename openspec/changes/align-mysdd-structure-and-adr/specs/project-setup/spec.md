<!-- markdownlint-disable MD041 -->

## Purpose

Define a reproducible Windows setup contract that works without elevation and
keeps optional tools separate from the minimum project setup.

## ADDED Requirements

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

### Requirement: Setup documentation has minimum and extended levels

The project MUST provide `docs/manual/SETUP.md` as the minimum setup and
`docs/manual/SETUP.full.md` as the setup with additional tools. Shared
instructions MUST treat the minimum setup as authoritative. This requirement
incorporates ADR-002.

#### Scenario: Choose the minimum setup

- **WHEN** a contributor needs only the required project tools
- **THEN** `docs/manual/SETUP.md` provides a complete minimum procedure
- **THEN** optional tools do not become minimum prerequisites

#### Scenario: Choose the extended setup

- **WHEN** a contributor needs the additional supported tools
- **THEN** `docs/manual/SETUP.full.md` identifies the additional procedure
- **THEN** shared steps refer to the minimum setup instead of duplicating it

### Requirement: Project Agent Skills use one canonical location

Project-specific Agent Skills MUST reside under `.agents/skills/` and MUST NOT
be duplicated under `.github/` or `.roo/`. This requirement incorporates
ADR-003.

#### Scenario: Add or migrate a project skill

- **WHEN** a maintainer adds or migrates a project-specific Agent Skill
- **THEN** the skill exists under `.agents/skills/<skill-name>/`
- **THEN** no duplicate copy is added under `.github/` or `.roo/`

### Requirement: Standard setup excludes MCP

The standard setup procedures MUST NOT install or configure a Model Context
Protocol (MCP) integration. A consuming project MUST make its own explicit
decision before introducing MCP. This requirement incorporates ADR-004.

#### Scenario: Complete either setup level

- **WHEN** a contributor completes the minimum or extended setup
- **THEN** no MCP server or MCP client configuration is installed
- **THEN** the setup succeeds without MCP credentials or endpoints
