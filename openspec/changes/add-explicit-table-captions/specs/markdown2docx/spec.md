<!-- markdownlint-disable MD013 MD022 MD032 MD041 -->

## ADDED Requirements

### Requirement: 表ごとの表題を正本Markdownで指定する

The `markdown2docx` skill MUST treat a non-empty `表題: <caption>` paragraph immediately before a table as that table's explicit caption. The generated DOCX MUST display the caption as `表 <number>: <caption>` using the canonical table-caption style and MUST use the same display text in `表一覧`. The caption text MUST be independent of the enclosing section heading. When the paragraph is absent, the skill MUST preserve the existing section-derived caption behavior for compatibility.

For quality requirements QR-DOCX-002, QR-DOCX-003, QR-DOCX-005, and QR-DOCX-007, the measures are explicit-caption matches, table-caption coverage, and successful conversion of an unmarked table; the targets are 100% matches for marked tables, 100% caption coverage for all tables, and one successful compatibility case; the conditions are PRD and HLD conversion; and the verification methods are source-to-OOXML comparison, regression tests, and all-page rendering.

#### Scenario: 明示した表題をDOCXへ反映する

- **WHEN** a canonical Markdown table is immediately preceded by `表題: 文書概要`
- **THEN** the corresponding DOCX caption is `表 <number>: 文書概要`
- **THEN** the table-list entry uses the same caption text and does not use the enclosing section name as its title

#### Scenario: 表題を表ごとに変更する

- **WHEN** two tables in the same section have different explicit table titles
- **THEN** each DOCX table receives its corresponding explicit title
- **THEN** the table list contains both distinct titles

#### Scenario: 明示的な表題がない既存文書を変換する

- **WHEN** a Markdown table has no `表題: <caption>` paragraph immediately before it
- **THEN** the skill generates the existing section-derived caption
- **THEN** conversion does not fail because the explicit title is absent
