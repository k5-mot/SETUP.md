<!-- markdownlint-disable MD041 -->

## 1. Canonical coding policy

- [x] 1.1 Add `CODING_RULES.md` with Japanese common, Python, TypeScript, and
  Java sections; preserve the simplicity rules, recommended Python catalog,
  executable timing requirement, and adaptable Ruff/ty/pytest reference config,
  then verify all four headings and required terms with `rg` (QR-001).
- [x] 1.2 Add a mandatory relative link from `AGENTS.md` to
  `CODING_RULES.md`, then verify the target resolves and no duplicate coding
  policy is introduced (QR-001, maintenance transition).
- [x] 1.3 Add common rules requiring explanatory comments for configuration
  values and appropriately placed intent or constraint comments for complex
  processing, then verify the wording is present and Markdownlint passes
  (QR-001, QR-003).

## 2. Markdown quality cleanup

- [x] 2.1 Fix list indentation and excess blank lines in
  `docs/manual/SETUP.md`, add only the narrow MD013/MD033 suppressions needed
  for intentional commands and disclosure blocks, and verify the file passes
  markdownlint (QR-003).
- [x] 2.2 Add narrow lint suppressions to the affected OpenSpec public documents
  and templates without changing their semantic content, then verify strict
  schema, main-spec, and active-change validation succeeds (QR-002, QR-003).
- [x] 2.3 Run `markdownlint-cli2` over every tracked `*.md` returned by Git and
  record zero findings as repository-wide maintainability evidence (QR-003).

## 3. Existing Python quality

- [x] 3.1 Add a directly executable standard-library local-link checker with
  `time.perf_counter()` timing, first demonstrate a failing broken-link case,
  then verify all tracked Markdown links pass (QR-003).
- [x] 3.2 Add a directly executable DOCX integration test with task timing,
  first demonstrate the test fails without its generated outputs, then convert
  PRD and HLD fixtures through real Pandoc and formatter commands and verify
  non-empty output, representative IDs, and unchanged Markdown hashes (QR-004).
- [x] 3.3 Run Ruff check and format verification for all tracked Python files,
  and confirm no unnecessary dependency or credential file appears in the Git
  diff (QR-005).

## 4. Ubuntu quality workflow

- [x] 4.1 Add `.github/workflows/quality.yml` with one `quality` job on
  `ubuntu-latest` for pull requests and pushes to `main`; run pinned OpenSpec,
  markdownlint, local-link, Ruff, and DOCX regression checks without executing
  the Windows setup procedure (QR-002, QR-003, QR-004).
- [x] 4.2 Document GitHub Actions standard logs, repository-controlled retention,
  no separate dashboard/alert/on-call stack, and manual SemVer tags only after
  the target `main` commit passes `quality`; verify no tag or credential is
  created (QR-003, QR-005).

## 5. Non-rewriting Git cleanup

- [x] 5.1 Record the `docs/mysdd-workflow` tip, verify it is an ancestor of
  `main` with zero branch-only commits, delete it using `git branch -d`, and
  verify `main` and `origin/main` remain unchanged (QR-004, disposal evidence).
- [x] 5.2 Verify no tag was created before CI exists and no published commit was
  amended or rebased; document that future AI-assisted commits require the
  generic trailer already mandated by `AGENTS.md` (QR-004).

## 6. Final verification

- [x] 6.1 Run strict validation for this Change, all main Specs, archived task
  completion, tracked Markdown, local relative links, and Git status; record
  zero blocking errors and review the diff for unrelated changes.
