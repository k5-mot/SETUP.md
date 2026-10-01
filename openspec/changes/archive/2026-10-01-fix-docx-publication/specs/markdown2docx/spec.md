<!-- markdownlint-disable MD013 MD022 MD032 MD041 -->

## MODIFIED Requirements

### Requirement: 正本Markdownを同名DOCXへ変換する

The `markdown2docx` skill MUST generate a DOCX beside a specified source Markdown file under `openspec/publics/`, using the same base name and `.agents/skills/markdown2docx/references/template.docx` as the reference document. The source Markdown MUST provide its document title as YAML metadata. The conversion MUST use one shared process for PRD and HLD, and MUST update navigation fields before reporting success.

For quality requirements QR-001, QR-003, QR-008, QR-DOCX-001, and QR-DOCX-003, the generated DOCX MUST be non-empty and MUST contain the source title, headings, body, tables, identifiers, and populated navigation sections. The measure is output existence, non-zero size, representative identifier matches, and visible navigation entry counts; the target is 100% for both PRD and HLD; the condition is that every required input exists; and the verification method is the conversion test, OOXML inspection, and rendered-page review. This requirement incorporates the shared conversion decisions in ADR-006 and ADR-010.

#### Scenario: 要件定義書を変換する

- **WHEN** `generate-prd` supplies `openspec/publics/prd.md` with YAML title metadata
- **THEN** the skill generates `openspec/publics/prd.docx`
- **THEN** the DOCX is non-empty and contains the title, populated navigation sections, and a representative requirement ID

#### Scenario: 基本設計書を変換する

- **WHEN** `generate-hld` supplies `openspec/publics/hld.md` with YAML title metadata
- **THEN** the skill generates `openspec/publics/hld.docx`
- **THEN** the DOCX is non-empty and contains the title, populated navigation sections, and a representative design ID

#### Scenario: 文書名Metadataがない

- **WHEN** the source Markdown does not provide a non-empty YAML `title`
- **THEN** the skill stops before conversion and reports the missing title metadata
- **THEN** it does not report successful DOCX generation

### Requirement: 技術文書のページ構成と版面を統一する

The `markdown2docx` skill MUST obtain fonts, styles, page geometry, headers, footers, and list presentation from the canonical reference DOCX. Generated DOCX body text MUST use 10-point type and MUST arrange the document as a one-page cover followed by `目次`, `図一覧`, `表一覧`, and the body. Navigation fields MUST contain current visible entries when conversion succeeds. If a document contains no figures, `図一覧` MUST remain present and MAY state that no figures exist. Every table MUST have a Japanese caption, MUST be centered on the page, and MUST repeat its header row after a page break. Every Section MUST use top and bottom margins of 25.4 mm and left and right margins of 19.05 mm. Each level-one body heading MUST begin on a new page. The document MUST otherwise use a monochrome palette, while note blocks MAY use restrained colors to distinguish their roles.

For quality requirements QR-DOCX-001, QR-DOCX-002, and QR-DOCX-006, the measures are populated navigation sections, caption coverage, and Section margin values; the targets are one or more TOC entries, table-list entries equal to the table count, caption coverage of 100%, and margins of 1440/1440/1080/1080 twip; the conditions are successful PRD and HLD conversion; and the verification methods are OOXML inspection and all-page rendering.

#### Scenario: 表紙と目次を生成する

- **WHEN** the source supplies title metadata and body sections
- **THEN** the document title occupies the cover page using the `Title` style
- **THEN** `目次`, `図一覧`, and `表一覧` follow the cover before the body
- **THEN** the table of contents and table list contain current visible entries

#### Scenario: 本文の章を改ページする

- **WHEN** a level-one body section follows preceding content
- **THEN** the level-one heading starts on a new page

#### Scenario: 本文と表を印刷向けに整形する

- **WHEN** the DOCX is generated with the canonical reference document
- **THEN** body text uses 10-point type
- **THEN** every Section uses the specified top, bottom, left, and right margins
- **THEN** every table has a Japanese caption and is centered on the page
- **THEN** table header rows repeat after a page break

#### Scenario: 注意ブロックを識別する

- **WHEN** the DOCX contains a note, tip, important, warning, or caution block
- **THEN** the block may use a restrained role-specific color
- **THEN** content outside note blocks remains monochrome

#### Scenario: Fieldを更新する

- **WHEN** conversion succeeds
- **THEN** the table of contents, figure list, table list, page numbers, and saved-date fields contain current display values
- **THEN** refreshed entries correspond to the generated headings and captions
