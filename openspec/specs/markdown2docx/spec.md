# markdown2docx Specification

## Purpose

Convert canonical MySDD Markdown under `openspec/publics/` to distributable
same-name DOCX files with one shared Pandoc contract while preserving the
source document on both success and failure.

## Requirements

### Requirement: 正本Markdownを同名DOCXへ変換する

The `markdown2docx` skill MUST generate a DOCX beside a specified source
Markdown file under `openspec/publics/`, using the same base name and
`openspec/publics/reference.docx` as the reference document.

For quality requirements QR-001, QR-003, and QR-008, the generated DOCX MUST
be non-empty and MUST contain the source headings, body, tables, and
identifiers. The measure is output existence, non-zero size, and representative
identifier matches; the target is 100% for both PRD and HLD; the condition is
that every required input exists; and the verification method is the
conversion test. This requirement incorporates the shared Pandoc decisions in
ADR-006 and ADR-010.

#### Scenario: 要件定義書を変換する

- **WHEN** `generate-prd` supplies `openspec/publics/prd.md`
- **THEN** the skill generates `openspec/publics/prd.docx`
- **THEN** the DOCX is non-empty and contains a representative requirement ID

#### Scenario: 基本設計書を変換する

- **WHEN** `generate-hld` supplies `openspec/publics/hld.md`
- **THEN** the skill generates `openspec/publics/hld.docx`
- **THEN** the DOCX is non-empty and contains a representative design ID

### Requirement: 変換先を安全に制限する

The `markdown2docx` skill MUST resolve the source Markdown and reference DOCX
as literal paths and MUST restrict the output to the same base name under
`openspec/publics/`. It MUST NOT read or write an unapproved file.

For quality requirement QR-006, the measure is writes to unapproved paths, the
target is zero, the conditions are normal conversion and an invalid output
request, and the verification method is path review plus negative tests.

#### Scenario: 出力先が入力と対応しない

- **WHEN** a caller requests a different directory or base name
- **THEN** the skill does not start conversion and reports the allowed path
- **THEN** it does not create a file at the requested output path

#### Scenario: 必須入力が存在しない

- **WHEN** the source Markdown or `openspec/publics/reference.docx` is absent
- **THEN** the skill reports the missing path
- **THEN** it does not report successful DOCX generation

### Requirement: 変換失敗時に正本を保持する

The `markdown2docx` skill MUST NOT change or delete source Markdown when DOCX
conversion fails. It MUST report partial success and the conversion failure to
the caller.

For quality requirements QR-004 and QR-005, the measures are source retention
and failure-reason reporting after conversion failure, both targets are 100%,
the condition is a non-zero renderer exit, and the verification method is
input hash comparison plus negative tests.

#### Scenario: Rendererが失敗する

- **WHEN** the renderer exits non-zero or returns an empty DOCX
- **THEN** the source Markdown remains byte-for-byte unchanged
- **THEN** the skill reports the failure instead of reporting completion

#### Scenario: 変換が成功する

- **WHEN** the renderer generates a non-empty DOCX
- **THEN** the skill returns the generated DOCX path
- **THEN** the source Markdown remains unchanged
