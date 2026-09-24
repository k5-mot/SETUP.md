# markdown2docx Specification

## Purpose

Convert canonical MySDD Markdown under `openspec/publics/` to distributable
same-name DOCX files with one shared Pandoc contract while preserving the
source document on both success and failure.

## Requirements

### Requirement: 正本Markdownを同名DOCXへ変換する

The `markdown2docx` skill MUST generate a DOCX beside a specified source
Markdown file under `openspec/publics/`, using the same base name and
`.agents/skills/markdown2docx/references/template.docx` as the reference
document. The source Markdown MUST provide its document title as YAML metadata,
and the skill MUST invoke Pandoc directly rather than through a tool-version
wrapper or a post-processing formatter.

For quality requirements QR-001, QR-003, and QR-008, the generated DOCX MUST
be non-empty and MUST contain the source title, headings, body, tables, and
identifiers together with fields for the table of contents, list of figures,
and list of tables. The measure is output existence, non-zero size,
representative identifier matches, and required field presence; the target is
100% for both PRD and HLD; the condition is that every required input exists;
and the verification method is the conversion test and OOXML inspection. This
requirement incorporates the shared Pandoc decisions in ADR-006 and ADR-010.

#### Scenario: 要件定義書を変換する

- **WHEN** `generate-prd` supplies `openspec/publics/prd.md` with YAML title metadata
- **THEN** the skill generates `openspec/publics/prd.docx`
- **THEN** the DOCX is non-empty and contains the title, navigation fields, and a representative requirement ID

#### Scenario: 基本設計書を変換する

- **WHEN** `generate-hld` supplies `openspec/publics/hld.md` with YAML title metadata
- **THEN** the skill generates `openspec/publics/hld.docx`
- **THEN** the DOCX is non-empty and contains the title, navigation fields, and a representative design ID

#### Scenario: 文書名Metadataがない

- **WHEN** the source Markdown does not provide a non-empty YAML `title`
- **THEN** the skill stops before conversion and reports the missing title metadata
- **THEN** it does not report successful DOCX generation

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

- **WHEN** the source Markdown or `.agents/skills/markdown2docx/references/template.docx` is absent
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

### Requirement: 技術文書のページ構成と版面を統一する

The `markdown2docx` skill MUST obtain fonts, styles, page geometry, headers,
footers, and list presentation from the canonical reference DOCX. Generated
DOCX body text MUST use 10-point type and MUST arrange the document as a
one-page cover followed by a table of contents, a list of figures, a list of
tables, and the body. Each level-one body heading MUST begin on a new page.
Every table MUST be centered on the page, and its header row MUST repeat after
a page break. The document MUST otherwise use a monochrome palette, while note
blocks MAY use restrained colors to distinguish their roles.

#### Scenario: 表紙と目次を生成する

- **WHEN** the source supplies title metadata and body sections
- **THEN** the document title occupies the cover page using the `Title` style
- **THEN** the table of contents, list of figures, and list of tables follow the cover before the body

#### Scenario: 本文の章を改ページする

- **WHEN** a level-one body section follows preceding content
- **THEN** the level-one heading starts on a new page

#### Scenario: 本文と表を印刷向けに整形する

- **WHEN** the DOCX is generated with the canonical reference document
- **THEN** body text uses 10-point type
- **THEN** every table is centered on the page
- **THEN** table header rows repeat after a page break

#### Scenario: 注意ブロックを識別する

- **WHEN** the DOCX contains a note, tip, important, warning, or caution block
- **THEN** the block may use a restrained role-specific color
- **THEN** content outside note blocks remains monochrome

#### Scenario: Fieldを更新する

- **WHEN** the generated DOCX is opened in a field-aware Word processor
- **THEN** the table of contents, figure list, table list, page numbers, and saved-date fields are marked for refresh
- **THEN** refreshed entries correspond to the generated headings and captions

### Requirement: Reference DOCXの書式契約を文書化する

The `markdown2docx` skill MUST provide
`.agents/skills/markdown2docx/references/style.md` as the maintained inventory
of the canonical reference DOCX. It MUST describe fonts, paragraph and table
styles, headers, footers, table of contents, cover, list of figures, and list
of tables, including which elements Pandoc copies, generates, or leaves for a
field-aware Word processor to refresh.

For quality requirement QR-006, the measure is documented requested style
categories, the target is eight of eight, the condition is a canonical
template or conversion-contract change, and the verification method is a
documentation checklist plus comparison with the DOCX package.

#### Scenario: 書式契約を確認する

- **WHEN** a maintainer needs to change or troubleshoot generated DOCX formatting
- **THEN** `references/style.md` identifies the responsible template style or field behavior for all eight categories
- **THEN** the document distinguishes automatic Pandoc output from deferred field refresh
