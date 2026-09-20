<!-- markdownlint-disable MD041 -->

## Why

Repository-wide coding guidance is currently implicit and fragmented, while
tracked Markdown contains avoidable lint findings and a merged local branch
remains after integration. A single canonical coding policy and reproducible
repository hygiene checks are needed together with a reproducible CI and
release gate.

## What Changes

- Add `CODING_RULES.md` as the canonical coding policy with common, Python,
  TypeScript, and Java sections.
- Define implementation-simplicity and YAGNI rules, language-specific quality
  gates, recommended Python packages, and an optional Python project baseline.
- Require explanatory comments for configuration values and appropriately
  document the intent or constraints of complex processing.
- Link the coding policy from `AGENTS.md` so coding agents must follow it.
- Make all tracked Markdown pass the repository lint command without changing
  OpenSpec semantics or removing intentional HTML disclosure blocks.
- Delete the fully merged local `docs/mysdd-workflow` branch.
- Add one GitHub Actions quality workflow on `ubuntu-latest` for OpenSpec,
  Markdown, Python, local-link, and DOCX conversion regression checks.
- Use GitHub Actions job output as the CI log, without a separate dashboard,
  alert destination, or on-call process.
- Preserve published Git history and require the quality job to pass before a
  maintainer manually creates a Semantic Versioning tag.
- Keep the Windows setup procedure outside CI; it remains a reviewed manual.

## Capabilities

### New Capabilities

- `coding-rules`: Defines the canonical repository coding policy, language
  sections, dependency-selection constraints, and executable quality gates.
- `quality-ci`: Defines the Ubuntu-based automated quality gate, CI logging,
  and manual release preconditions.

### Modified Capabilities

None.

## Impact

- Adds `CODING_RULES.md` and one mandatory reference from `AGENTS.md`.
- Adjusts Markdown lint directives and malformed spacing or indentation in the
  five currently failing Markdown files.
- Adds no runtime dependency and changes no public API.
- Adds `.github/workflows/quality.yml` and minimal standard-library regression
  scripts for local links and DOCX conversion.
- Removes one merged local branch only; no remote branch, tag, or published
  commit is rewritten.

## Stakeholders and Lifecycle Impact

- **Acquisition:** Recommended packages remain optional; projects add only
  dependencies required by a current task.
- **Supply:** Contributors and coding agents receive one reviewable source for
  implementation and language-specific quality expectations.
- **Transition:** Existing code is not reformatted or migrated solely because
  the policy is introduced.
- **Operation:** GitHub Actions provides job output and status; no runtime
  service, dashboard, alert integration, or on-call process is introduced.
- **Maintenance:** Markdown lint and language quality commands become explicit
  completion evidence for future changes.
- **Disposal:** The merged local branch is deleted after ancestry verification;
  its commits remain reachable from `main`.

## Quality Considerations

- **QR-001 Functional suitability:** The measure is required policy sections
  present, the target is four of four, and verification is heading and content
  inspection of `CODING_RULES.md`.
- **QR-002 Compatibility:** The measure is existing OpenSpec validation
  failures introduced, the target is zero, and verification is strict schema,
  main-spec, and active-change validation.
- **QR-003 Maintainability:** The measures are tracked Markdown lint findings
  and automated quality checks, the targets are zero findings and all checks in
  one successful `quality` job, and verification is a local equivalent run plus
  workflow inspection.
- **QR-004 Reliability:** The measure is published Git objects rewritten, the
  target is zero, and verification compares `main` and `origin/main` history.
- **QR-005 Security:** The measure is new mandatory dependencies or credentials,
  the target is zero, and verification is diff review.
- **Performance efficiency:** Runtime performance and capacity limits remain
  unresolved because representative document sizes and service levels are not
  yet defined; CI records elapsed test time without setting a product limit.
- **Interaction capability:** Not applicable; no user interface changes.
- **Flexibility:** Applicable through language-specific sections, but no numeric
  target is added because each consuming project retains its existing toolchain.
- **Safety:** Not applicable; no safety-related behavior is introduced.
