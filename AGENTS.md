# AGENTS.md

## Scope

- MUST respond to users in Japanese.
- MUST follow the [CONTRIBUTING_GUIDELINE](CONTRIBUTING.md), when developing.
- MUST follow the [CODING_RULES](CODING_RULES.md), when implementing code.
- MUST follow the [DOCUMENTATION_RULES](DOCUMENTATION_RULES.md), when writing documentation.
- MUST; Planning, proposals, new capabilities, breaking changes, or
  architectural changes must follow the OpenSpec workflow defined in
  `openspec/config.yaml`.

## Boundaries

- MUST NOT generate database migration files automatically. Request human
  confirmation before creating a migration file.
- MUST NOT execute a production deployment without the user's explicit approval
  of the concrete deployment target and release artifact.
- MUST NOT execute paid operations, even with the user's approval. Explain the
  expected cost and risks so the user can perform those operations manually.
