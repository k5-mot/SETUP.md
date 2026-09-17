---
name: generate-prd
description: 1つのOpenSpec ChangeからMySDDの要件定義書をMarkdownおよびDOCXで生成または再生成する場合に使用する。
---

# 要件定義書を生成する

`change-name`を1つだけ受け取る。

## 入力を読み込む

- `openspec/changes/<change-name>/proposal.md`
- 1つ以上の`openspec/changes/<change-name>/specs/**/spec.md`
- [要件定義書テンプレート](assets/prd.md)

`proposal.md`が存在しない場合、またはDelta Specが1件も存在しない場合は停止する。
Capability path、Requirement見出し、Scenario名、IDおよびそれらのトレーサビリティを
維持する。明記されていない事実を要求に変換せず、入力が不足している箇所には`TBD`と
記載する。

## 文書を生成する

テンプレートを使用して`openspec/publics/prd.md`を生成する。適用する各品質特性、
測定量、目標値、条件および検証方法を含める。OpenSpec Artifactを新規作成せず、
入力元のChangeを変更しない。

Markdownの完成後に[markdown2docx](../markdown2docx/SKILL.md)を読み、
`openspec/publics/prd.md`から`openspec/publics/prd.docx`への変換を委譲する。

## 完了を報告する

トレーサビリティを維持した完全な要件定義書Markdownと、空でないDOCXの両方が
存在する場合に成功とする。DOCX変換に失敗した場合はMarkdownを保持し、変換失敗を
添えて部分成功として報告する。
