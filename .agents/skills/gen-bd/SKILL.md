---
name: gen-bd
description: MySDD Changeから基本設計書のMarkdownとDOCXを生成する。基本設計書の作成または再生成を依頼されたときに使用する。
---

# 🏛️ gen-bd

## 入力

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/specs/**/*.md`（1ファイル以上）
- `openspec/changes/<change-name>/design.md`（存在する場合）

必ず[Template Asset](assets/bd.md)を読み、その章立てに従う。

## 出力

- `openspec/changes/<change-name>/docs/bd.md`
- `openspec/changes/<change-name>/docs/bd.docx`

Designがない場合は設計固有の項目を`TBD`とする。既存IDがない場合は
Requirement見出し、Scenario名、Design見出しを参照名として使う。

入力にない事実を追加せず、Requirement見出し、Scenario名、既存IDと
参照関係は変更しない。

`bd.md`の生成後、[md2docx](../md2docx/SKILL.md)を読み、`bd.md`を
`bd.docx`へ変換する。DOCX変換に失敗した場合はMarkdownを保持し、
部分成功と失敗理由を報告する。

## 完了条件

Templateの全章を持つ`bd.md`と同名DOCXが生成され、要求・設計・検証の
参照関係が保たれている。
