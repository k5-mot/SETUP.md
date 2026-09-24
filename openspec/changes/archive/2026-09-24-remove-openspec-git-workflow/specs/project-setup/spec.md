<!-- markdownlint-disable MD013 MD022 MD032 MD041 -->

## MODIFIED Requirements

### Requirement: Only repository-owned skills are tracked

The repository MUST track exactly `generate-prd`, `generate-hld`, and
`markdown2docx` under `.agents/skills/`, plus the local `.gitignore`. Every
other locally installed Skill MUST be ignored and MUST NOT be removed from a
developer's working directory merely to untrack it.

For quality requirement QR-007 (maintainability), the measure is the number of
tracked repository-owned Skill directories, the target is three, the condition
is every repository status check, and the verification method is the Git index
and `.agents/skills/.gitignore` inspection.

#### Scenario: A third-party skill exists locally

- **WHEN** Git evaluates a Skill outside the three repository-owned names
- **THEN** `.agents/skills/.gitignore` excludes it from repository tracking
- **THEN** the local Skill remains available on the developer's filesystem

#### Scenario: A repository-owned skill changes

- **WHEN** a maintainer edits one of the three repository-owned Skills
- **THEN** Git reports that change as trackable

#### Scenario: The retired Git wrapper remains installed locally

- **WHEN** `openspec-git-workflow` remains in a developer's local Skill directory
- **THEN** Git ignores it as a non-repository-owned Skill
- **THEN** the repository contains no tracked file for that Skill
