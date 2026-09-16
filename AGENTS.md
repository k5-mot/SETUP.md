# AGENTS.md

## Scope

- AI agents MUST respond to users in Japanese.
- Human contributors MUST follow the
  [contribution rules](docs/CONTRIBUTING.md). AI agents MUST follow the Git and
  release rules in this file when working with branches, commits, or tags.
- AI agents MUST follow the
  [OpenSpec workflow](docs/references/OpenSpec-Workflow.md) when using
  `spec-driven` and the [MySDD workflow](docs/references/MySDD-Workflow.md)
  when using `mysdd`.
- If a directory contains another `AGENTS.md`, its more specific rules MUST
  take precedence within that directory.

## Documentation Rules

### Format and Language

- All project documentation MUST use Markdown and MUST have the `.md`
  extension.
- Documents under `docs/` MUST be written in Japanese.
- Project-governance `AGENTS.md` files MUST be written in English. Runtime
  persona or workspace `AGENTS.md` files for Hermes, OpenClaw, and QwenPaw MAY
  use the agent's configured language.
- Language required by an external file format, source code, command,
  identifier, product name, or quoted specification MAY remain unchanged.

### Structure and Content

- Each rule MUST have one authoritative location. The same rule MUST NOT be
  duplicated across documents.
- References to rules in another document MUST use relative links.
- Headings MUST identify their contents clearly and MUST distinguish
  procedures, expected results, exceptions, and rollback steps.
- Every executable command in documentation MUST have a comment that explains
  its purpose.
- Commands requiring elevated privileges MUST show `sudo` explicitly.
- Procedures that change state MUST document their expected results and
  failure criteria.
- Acronyms, standards, and project-specific terms SHOULD be explained or
  linked when first introduced.
- Moving or renaming a document MUST update all project-local links in the
  same change.

### Reference Requirements

- A document that relies on an external specification, official documentation,
  issue, or article MUST include a final `## References` section.
- A `References` section MUST list only sources actually used by that document.
- Primary sources and official documentation SHOULD be preferred when
  available.
- A document without external references MAY omit the `References` section.
- No content section MAY appear after `References`.

## Git Operations

- AI agents MUST inspect diffs, tests, generated files, and possible secrets
  before committing.
- AI agents MUST NOT include unrelated user changes in a commit.
- AI agents MUST NOT force-push or rewrite shared history.

### Normative Language

Rules MUST use the uppercase keywords from RFC 2119 and RFC 8174 with their
ordinary meanings.

| Keyword | Meaning |
| --- | --- |
| `MUST` | Required without exception |
| `MUST NOT` | Prohibited without exception |
| `SHOULD` | Recommended unless a justified exception exists |
| `SHOULD NOT` | Discouraged unless a justified exception exists |
| `MAY` | Optional according to the situation |

### Commit Rules

Commit messages MUST combine Conventional Commits and gitmoji and MUST be
written in Japanese.

```text
<gitmoji> <type>[optional scope][!]: <変更内容>

<変更理由>
```

- The subject MUST describe the change, and the body MUST explain its reason.
- Each commit MUST contain exactly one logical change.
- The type, such as `feat`, `fix`, or `docs`, MUST match the purpose.
- A breaking change MUST be marked with `!` or `BREAKING CHANGE:`.
- AI agents SHOULD use `git-cz` to compose commit messages when practical.

```text
📝 docs(git): Commit規則を簡潔化

人間向けの基本ルールへ責務を限定するため。
```

### Branch Strategy

AI agents MUST use GitHub Flow.

```text
main ← Pull Request ← short-lived branch
```

- A short-lived branch scoped to one purpose MUST start from the latest
  `main`.
- Review and required CI MUST finish in a Pull Request before merging to
  `main`.
- The working branch SHOULD be deleted after the merge.

The project does not use the following strategies:

- Trunk-Based Development, because GitHub Flow explicitly standardizes Pull
  Requests, review, and merge.
- GitLab Flow, because permanent environment and release branches are not
  required.
- Git Flow, because long-lived `develop`, release, and hotfix branches and
  merge-back are unnecessary.

### Release Rules

Releases MUST follow Semantic Versioning 2.0.0 and MUST use Git tags in the
form `v<MAJOR>.<MINOR>.<PATCH>`.

| Change | Version |
| --- | --- |
| Backward-incompatible change | `MAJOR` |
| Backward-compatible feature | `MINOR` |
| Backward-compatible bug fix | `PATCH` |

- Release changes MUST be merged into `main`, and required CI MUST complete
  before creating the tag.
- A published tag MUST NOT be moved, deleted, or reused.
- A post-release correction MUST be published as a new version.

## Tooling

- AI agents MUST use mise for Node.js, npm, Pandoc, and Python.
- AI agents MUST activate mise in PowerShell with
  `(&mise activate pwsh) | Out-String | Invoke-Expression`.

## References

- [Contributing Guideline](docs/CONTRIBUTING.md)
- [RFC 2119](https://www.rfc-editor.org/info/rfc2119)
- [RFC 8174](https://www.rfc-editor.org/info/rfc8174)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [gitmoji Specification](https://gitmoji.dev/specification)
- [git-cz](https://github.com/streamich/git-cz)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [GitLab Flow](https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Semantic Versioning 2.0.0](https://semver.org/)
