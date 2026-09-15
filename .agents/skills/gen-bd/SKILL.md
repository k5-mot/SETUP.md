---
name: gen-bd
description: MySDD Changeのbd Artifactとして基本設計書のMarkdownとDOCXを生成する。基本設計書の作成または再生成を依頼されたときに使用する。
---

# 🏛️ gen-bd

最初に[文書生成の共通手順](../_shared/document-generation.md)を読む。

## 入力

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/specs/**/*.md`（1ファイル以上）
- `openspec/changes/<change-name>/design.md`（存在する場合）

Artifact IDは`bd`とする。`openspec instructions bd --change <change-name> --json`のTemplateと`resolvedOutputPath`を使う。

## 出力

- `openspec/changes/<change-name>/docs/bd.md`
- `openspec/changes/<change-name>/docs/bd.docx`

## 章立て

1. 文書概要と適用範囲
2. 関連文書
3. システム全体構成
4. アプリケーション・ソフトウェア構成
5. インフラ・ネットワーク方式
6. データ・外部インタフェース方式
7. 認証・認可・セキュリティ方式
8. 性能・容量・可用性・復旧方式
9. ログ・監視・運用方式
10. デプロイ・リリース・構成管理方式
11. ISO 25010品質特性への対応
12. ADR
13. 要求トレーサビリティ
14. 未決事項・リスク

Designがない場合は設計固有の項目を`TBD`とする。既存IDがない場合はRequirement見出し、Scenario名、Design見出しを参照名として使う。
