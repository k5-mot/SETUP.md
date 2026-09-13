## Purpose

🏛️ OpenSpecの要求・方式・設計Artifactを正本として、追跡可能な基本設計書のMarkdownと配布用DOCXを生成する。

## ADDED Requirements

### Requirement: 基本設計書を生成する

`gen-bd`は、対象Changeの`proposal.md`、`specs/**/*.md`、存在する場合の`design.md`から基本設計書を生成しなければならない（MUST）。

#### Scenario: 必要な入力が存在する

- **WHEN** 利用者が対象Changeを指定して`gen-bd`を実行する
- **THEN** `openspec/changes/<change-name>/docs/bd.md`を生成する
- **THEN** 同じ内容を基に`bd.docx`を生成する

#### Scenario: 必要な入力が不足している

- **WHEN** 必須Artifactが存在しない
- **THEN** 不足ファイルを報告する
- **THEN** 生成完了を報告しない

### Requirement: 設計情報とトレーサビリティを保持する

`gen-bd`は、入力にあるRequirement見出し、Scenario名、要求ID、Architecture ID、Design ID、品質要求への対応、ADR、リスクを保持しなければならず（MUST）、入力にない設計事実を追加してはならない（MUST NOT）。

#### Scenario: 情報が不足している

- **WHEN** 文書の必須項目に対応する情報が入力Artifactにない
- **THEN** 該当項目へ`TBD`を記載する
- **THEN** 推測した構成や実装事実を記載しない

#### Scenario: 設計IDが存在する

- **WHEN** 入力Artifactに要求、方式、設計のIDと参照関係がある
- **THEN** 出力文書でIDを変更せず保持する
- **THEN** 要求トレーサビリティ表へ参照関係を記載する

#### Scenario: Designが存在しない

- **WHEN** 対象Changeで`design.md`が省略されている
- **THEN** ProposalとDelta Specから基本設計書を生成する
- **THEN** 設計情報が必要な項目へ`TBD`を記載する

### Requirement: Markdownを正本として出力する

`gen-bd`はMarkdownを正本として生成し、DOCXをMarkdownから再生成可能な配布物として扱わなければならない（MUST）。

#### Scenario: DOCX生成に失敗する

- **WHEN** Markdown生成後にDOCX変換が失敗する
- **THEN** 生成済みMarkdownを保持する
- **THEN** DOCX生成の失敗を報告する
