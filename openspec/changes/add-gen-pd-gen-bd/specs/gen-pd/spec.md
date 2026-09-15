## Purpose

📋 OpenSpecの要求関連Artifactを正本として、追跡可能な要件定義書のMarkdownと配布用DOCXを生成する。

## ADDED Requirements

### Requirement: 要件定義書を生成する

`gen-pd`は、対象Changeの`proposal.md`と`specs/**/*.md`から要件定義書を生成しなければならない（MUST）。

#### Scenario: 必要な入力が存在する

- **WHEN** 利用者が対象Changeを指定して`gen-pd`を実行する
- **THEN** `gen-pd/assets/rd.md`をTemplateとして使う
- **THEN** `openspec/changes/<change-name>/docs/rd.md`を生成する
- **THEN** 同じ内容を基に`rd.docx`を生成する

#### Scenario: 必要な入力が不足している

- **WHEN** 必須Artifactが存在しない
- **THEN** 不足ファイルを報告する
- **THEN** 生成完了を報告しない

### Requirement: 入力Artifactの内容を保持する

`gen-pd`は、入力にあるRequirement見出し、Scenario名、要求ID、品質特性、測定条件、受入条件、検証方法を保持しなければならず（MUST）、入力にない要求を追加してはならない（MUST NOT）。

#### Scenario: 情報が不足している

- **WHEN** 文書の必須項目に対応する情報が入力Artifactにない
- **THEN** 該当項目へ`TBD`を記載する
- **THEN** 推測した事実を記載しない

#### Scenario: 要求IDが存在する

- **WHEN** 入力Artifactに要求IDと参照関係がある
- **THEN** 出力文書でIDを変更せず保持する
- **THEN** 要求トレーサビリティ表へ参照関係を記載する

#### Scenario: 要求IDが存在しない

- **WHEN** Delta Specに要求IDがなくRequirement見出しとScenario名がある
- **THEN** Capability path、Requirement見出し、Scenario名をトレーサビリティの参照名として保持する

### Requirement: Markdownを正本として出力する

`gen-pd`はMarkdownを正本として生成し、DOCXをMarkdownから再生成可能な配布物として扱わなければならない（MUST）。

#### Scenario: DOCX生成に失敗する

- **WHEN** Markdown生成後にDOCX変換が失敗する
- **THEN** 生成済みMarkdownを保持する
- **THEN** DOCX生成の失敗を報告する
