---
name: gen-pd
description: OpenSpecの要求関連Artifactから要件定義書のMarkdownとDOCXを生成する。要件定義書の作成または再生成を依頼されたときに使用する。
---

# 📋 gen-pd

最初に[文書生成の共通手順](../_shared/document-generation.md)を読む。

## 入力

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/requirements.md`
- `openspec/changes/<change-name>/specs/**/*.md`（1ファイル以上）
- `openspec/changes/<change-name>/architecture.md`

## 出力

- `openspec/artifacts/<change-name>/requirements-definition/要件定義書.md`
- `openspec/artifacts/<change-name>/requirements-definition/要件定義書.docx`

## 章立て

1. 文書概要
2. 背景・目的
3. 対象システムとスコープ
4. ステークホルダー
5. 前提条件・制約
6. 業務・システム・機能要件
7. ISO 25010品質要件
8. 外部インタフェース・データ要件
9. 運用・保守要件
10. 受入条件と検証方法
11. 要求トレーサビリティ
12. 用語集

品質要件にはQuality Characteristic、Requirement、Measure、Target、Conditions、Verification Methodを記載する。
