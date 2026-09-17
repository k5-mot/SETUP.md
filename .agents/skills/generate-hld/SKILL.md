---
name: generate-hld
description: 1つのOpenSpec ChangeからMySDDの基本設計書をMarkdownおよびDOCXで生成または再生成する場合に使用する。
---

# 基本設計書を生成する

`change-name`を1つだけ受け取る。

## 入力を読み込む

- `openspec/changes/<change-name>/proposal.md`
- 1つ以上の`openspec/changes/<change-name>/specs/**/spec.md`
- 存在する場合は`openspec/changes/<change-name>/design.md`
- [基本設計書テンプレート](assets/hld.md)

`proposal.md`が存在しない場合、またはDelta Specが1件も存在しない場合は停止する。
Capability path、Requirement見出し、Scenario名、Design見出し、IDおよびそれらの
トレーサビリティを維持する。設計上の事実を推測で補わず、設計入力が存在しない、
または不完全な箇所には`TBD`と記載する。

## 文書を生成する

テンプレートを使用して`openspec/publics/hld.md`を生成する。要求および品質目標を、
設計判断と検証Evidenceへ対応付ける。OpenSpec Artifactを新規作成せず、入力元の
Changeを変更しない。

Markdownの完成後に[markdown2docx](../markdown2docx/SKILL.md)を読み、
`openspec/publics/hld.md`から`openspec/publics/hld.docx`への変換を委譲する。

## 完了を報告する

トレーサビリティを維持した完全な基本設計書Markdownと、空でないDOCXの両方が
存在する場合に成功とする。DOCX変換に失敗した場合はMarkdownを保持し、変換失敗を
添えて部分成功として報告する。
