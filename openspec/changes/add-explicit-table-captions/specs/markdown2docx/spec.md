<!-- markdownlint-disable MD013 MD022 MD032 MD041 -->

## ADDED Requirements

### Requirement: 表ごとの表題を正本Markdownで指定する

The `markdown2docx` skill MUST accept Pandoc table-caption syntax while preserving the Pandoc `gfm` reader as the base input contract. A non-empty paragraph beginning with `Table:`, `table:`, or `:` before or after a table MUST supply that table's explicit caption. The generated DOCX MUST display the caption as `表 <number>: <caption>` using the canonical table-caption style and MUST use the same display text in `表一覧`. The caption text MUST be independent of the enclosing section heading. When a table caption is absent, the skill MUST preserve the existing section-derived caption behavior for compatibility.

For quality requirements QR-DOCX-002, QR-DOCX-003, QR-DOCX-005, and QR-DOCX-007, the measures are explicit-caption matches, table-caption coverage, and successful conversion of an unmarked table; the targets are 100% matches for marked tables, 100% caption coverage for all tables, and one successful compatibility case; the conditions are PRD and HLD conversion; and the verification methods are source-to-OOXML comparison, regression tests, and all-page rendering.

#### Scenario: 明示した表題をDOCXへ反映する

- **WHEN** a canonical Markdown table has the Pandoc caption `: 文書概要` before or after it
- **THEN** the corresponding DOCX caption is `表 <number>: 文書概要`
- **THEN** the table-list entry uses the same caption text and does not use the enclosing section name as its title

#### Scenario: 表題を表ごとに変更する

- **WHEN** two tables in the same section have different explicit table titles
- **THEN** each DOCX table receives its corresponding explicit title
- **THEN** the table list contains both distinct titles

#### Scenario: 明示的な表題がない既存文書を変換する

- **WHEN** a Markdown table has no Pandoc table caption
- **THEN** the skill generates the existing section-derived caption
- **THEN** conversion does not fail because the explicit title is absent

### Requirement: GFMを基礎としてPandoc固有構文を追加する

The `markdown2docx` skill MUST continue to parse every syntax feature enabled by its Pandoc `gfm` reader contract. Pandoc-specific syntax MUST be added explicitly without changing the interpretation of existing GFM content, and the maintained style specification MUST distinguish supported GFM syntax, supported Pandoc additions, and syntax without a reliable DOCX representation.

For quality requirements QR-DOCX-003, QR-DOCX-005, and QR-DOCX-008, the measures are successful parsing of the enabled GFM extensions and documented Pandoc additions; the targets are 100% of the enabled extension fixture and one documented entry for every supported addition; the conditions are conversion with the canonical reader and filters; and the verification methods are a Pandoc AST compatibility test, DOCX regression test, and style-contract review.

#### Scenario: GFM互換Fixtureを変換する

- **WHEN** a Markdown fixture uses every syntax feature enabled by the canonical Pandoc `gfm` reader
- **THEN** the conversion parses every fixture element without error
- **THEN** the generated document retains a corresponding supported document element or records the DOCX limitation in the style specification

#### Scenario: Pandoc固有構文を使用する

- **WHEN** a source uses a Pandoc-specific syntax listed as supported in the style specification
- **THEN** the conversion produces the documented DOCX representation
- **THEN** existing GFM syntax retains its canonical interpretation
