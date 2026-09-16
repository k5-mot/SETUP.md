<!-- markdownlint-disable MD041 -->

## Purpose

MySDDの正本Markdownを変更せず、共通書式を適用した配布用DOCXへ変換し、
要件定義書と基本設計書で同じ変換契約と失敗時の扱いを再利用できるようにする。

## ADDED Requirements

### Requirement: 正本Markdownを同名DOCXへ変換する

`md2docx`は、指定された正本Markdownと参照DOCXから、Markdownと同じ
Directoryに同じBase nameのDOCXを生成しなければならない（MUST）。

品質要求`QR-001`、`QR-003`、`QR-008`として、生成したDOCXは空であっては
ならず（MUST NOT）、入力にある見出し、本文、表および識別子を含まなければ
ならない（MUST）。MeasureはDOCXの存在、非ゼロSizeおよび代表的な識別子の
一致、Targetは要件定義書と基本設計書の両方で100%、Conditionsは必須入力と
参照DOCXが存在すること、Verification Methodは変換テストとする。

#### Scenario: 要件定義書を変換する

- **WHEN** `gen-pd`が生成済みの`docs/rd.md`を変換対象として指定する
- **THEN** 同じDirectoryへ`docs/rd.docx`を生成する
- **THEN** DOCXは非ゼロSizeで、Markdownの代表的な要求IDを含む

#### Scenario: 基本設計書を変換する

- **WHEN** `gen-bd`が生成済みの`docs/bd.md`を変換対象として指定する
- **THEN** 同じDirectoryへ`docs/bd.docx`を生成する
- **THEN** DOCXは非ゼロSizeで、Markdownの代表的な設計IDを含む

### Requirement: 変換先を安全に制限する

`md2docx`は、変換元Markdownと参照DOCXをLiteral pathとして解決し、
出力先を変換元と同じDirectoryの同じBase nameへ制限しなければならない
（MUST）。指定外のファイルを読み書きしてはならない（MUST NOT）。

品質要求`QR-006`として、Measureは許可外Pathへの書き込み件数、Targetは
0件、Conditionsは通常変換と不正な出力先指定、Verification Methodは
Path検証のReviewと失敗系テストとする。

#### Scenario: 出力先が入力と対応しない

- **WHEN** 入力Markdownと異なるDirectoryまたはBase nameの出力先を指定する
- **THEN** 変換を開始せず、許可される出力先を報告する
- **THEN** 指定された出力先へファイルを作成しない

#### Scenario: 必須入力が存在しない

- **WHEN** 変換元Markdownまたは参照DOCXが存在しない
- **THEN** 不足している入力Pathを報告する
- **THEN** DOCX生成の成功を報告しない

### Requirement: 変換失敗時に正本を保持する

`md2docx`は、DOCX変換が失敗しても正本Markdownを変更または削除しては
ならず（MUST NOT）、部分成功と失敗理由を呼び出し元へ報告しなければ
ならない（MUST）。

品質要求`QR-004`、`QR-005`として、Measureは変換失敗後のMarkdown保持率と
失敗理由の報告率、Targetはいずれも100%、ConditionsはRendererの非ゼロ終了、
Verification Methodは入力Hash比較と失敗系テストとする。

#### Scenario: Rendererが失敗する

- **WHEN** Rendererが非ゼロの終了Codeまたは空のDOCXを返す
- **THEN** 変換前と同じ内容のMarkdownを保持する
- **THEN** DOCX生成を完了扱いにせず、失敗理由を報告する

#### Scenario: 変換が成功する

- **WHEN** Rendererが非ゼロSizeのDOCXを生成する
- **THEN** 生成したDOCXのPathを呼び出し元へ返す
- **THEN** 変換元Markdownを変更しない
