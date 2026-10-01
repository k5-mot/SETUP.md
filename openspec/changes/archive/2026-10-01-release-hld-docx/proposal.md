<!-- markdownlint-disable MD013 MD033 MD041 -->

## Why

基本設計書の正本は Git 管理された Markdown だが、公開済み Release から DOCX を取得できない。手動でタグを作成する既存運用に、再現可能な配布手順を追加する。

## What Changes

- `v<MAJOR>.<MINOR>.<PATCH>` タグの push 時に `mysdd` Schema を検証し、`hld.md` から DOCX を生成する。
- 生成した `hld.docx` をそのタグの GitHub Release に登録する。
- 正本 Markdown と Schema は変更せず、生成 DOCX は Git に追加しない。

## Capabilities

### New Capabilities

- `release-hld-docx`: 手動タグを起点に、検証済み基本設計書を Release Asset として配布する。

### Modified Capabilities

なし。既存の `mysdd-workflow`、`mysdd-schema`、`markdown2docx` の要件は維持する。

## Impact

- `.github/workflows/` に Release 用 Workflow を追加する。
- 既存の `openspec/publics/hld.md`、`openspec/schemas/mysdd/`、参照 DOCX を入力に使う。
- GitHub Actions の `contents: write` 権限、Pandoc 3.11、OpenSpec CLI を使用する。

## Stakeholders and Lifecycle Impact

- 取得・供給: 利用者は Release から DOCX を取得できる。Maintainer は既存規則どおり品質検査後にタグを手動作成する。
- 移行: 既存タグや履歴の移動は不要。
- 運用・保守: Release Job の標準ログと正本 Markdown で失敗原因と再生成元を確認する。
- 廃止: 追加サービスや保存先はないため、Workflow の削除で運用を終了できる。

## Quality Considerations

| 品質特性 | ID | 目標と検証 |
| --- | --- | --- |
| 機能適合性 | QR-REL-001 | 有効なタグで非空の `hld.docx` を Release に1件登録する。Workflow と DOCX 内容を確認する。 |
| 信頼性 | QR-REL-002 | 検証または変換失敗時は Release を作成しない。失敗経路を確認する。 |
| セキュリティ | QR-REL-003 | 対象タグと main 上の Commit を確認し、Release Job にだけ書込権限を与える。Workflow を検査する。 |
| 保守性 | QR-REL-004 | DOCX の Git 追跡件数を0に保ち、既存の Pandoc 契約を再利用する。差分と Git 状態を確認する。 |
| 性能効率性 | — | 対象文書は1件であり、時間目標を別途設ける必要がない。 |
| 互換性 | — | 外部 API や既存 Artifact Graph を変更しない。 |
| 使用性 | — | 利用者向け UI を変更しない。 |
| 移植性 | — | Ubuntu Runner 上の公開ツールのみを使用し、別環境への移植要求はない。 |
