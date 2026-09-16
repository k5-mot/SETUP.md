---
name: gen-pd
description: MySDD Changeから要件定義書のMarkdownとDOCXを生成する。要件定義書の作成または再生成を依頼されたときに使用する。
---

# 📋 gen-pd

## 入力

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/specs/**/*.md`（1ファイル以上）

必ず[Template Asset](assets/rd.md)を読み、その章立てに従う。

## 出力

- `openspec/changes/<change-name>/docs/rd.md`
- `openspec/changes/<change-name>/docs/rd.docx`

品質要件にはQuality Characteristic、Requirement、Measure、Target、
Conditions、Verification Methodを記載する。要求IDがない場合は
Capability path、Requirement見出し、Scenario名をトレーサビリティの
参照名として使う。

入力にない事実を追加せず、不足情報は`TBD`とする。Requirement見出し、
Scenario名、既存IDと参照関係は変更しない。

`rd.md`の生成後、[md2docx](../md2docx/SKILL.md)を読み、`rd.md`を
`rd.docx`へ変換する。DOCX変換に失敗した場合はMarkdownを保持し、
部分成功と失敗理由を報告する。

## 完了条件

Templateの全章を持つ`rd.md`と同名DOCXが生成され、要求と検証方法の
参照関係が保たれている。
