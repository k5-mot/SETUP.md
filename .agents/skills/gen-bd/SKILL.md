---
name: gen-bd
description: OpenSpecの要求・方式・設計Artifactから基本設計書のMarkdownとDOCXを生成する。基本設計書の作成または再生成を依頼されたときに使用する。
---

# 🏛️ gen-bd

最初に[文書生成の共通手順](../_shared/document-generation.md)を読む。

## 入力

- `openspec/changes/<change-name>/requirements.md`
- `openspec/changes/<change-name>/architecture.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/specs/**/*.md`（1ファイル以上）

## 出力

- `openspec/artifacts/<change-name>/basic-design/基本設計書.md`
- `openspec/artifacts/<change-name>/basic-design/基本設計書.docx`

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

各設計判断にはArchitecture IDまたはDesign IDと、対応する要求IDを記載する。
