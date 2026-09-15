---
name: gen-pd
description: MySDD Changeから要件定義書のMarkdownとDOCXを生成する。要件定義書の作成または再生成を依頼されたときに使用する。
---

# 📋 gen-pd

最初に[文書生成の共通手順](../_shared/document-generation.md)を読む。

## 入力

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/specs/**/*.md`（1ファイル以上）

必ず[Template Asset](assets/rd.md)を読み、その章立てに従う。

## 出力

- `openspec/changes/<change-name>/docs/rd.md`
- `openspec/changes/<change-name>/docs/rd.docx`

品質要件にはQuality Characteristic、Requirement、Measure、Target、Conditions、Verification Methodを記載する。
要求IDがない場合はCapability path、Requirement見出し、Scenario名をトレーサビリティの参照名として使う。

## 完了条件

Templateの全章を持つ`rd.md`と同名DOCXが生成され、要求と検証方法の参照関係が保たれている。
