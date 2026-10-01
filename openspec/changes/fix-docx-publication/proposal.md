<!-- markdownlint-disable MD013 MD033 MD041 -->

## Why

公開した DOCX では目次・図一覧・表一覧の表示内容が未更新で、一覧見出しが指定した日本語にならず、表キャプションと指定余白も欠けている。また、Release に HLD しか登録されず、PRD を取得できない。

## What Changes

- PRD と HLD の DOCX に、表示内容を更新した「目次」「図一覧」「表一覧」を含める。
- 全表に表キャプションを付与し、表一覧へ反映する。
- 全 Section の余白を上25.4mm、下25.4mm、左19.05mm、右19.05mmにする。
- Release に `prd.docx` と `hld.docx` の両方を登録する。
- 欠損を検出する DOCX 構造 Test と描画確認を追加する。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `markdown2docx`: 配布 DOCX のナビゲーション、表キャプション、余白およびフィールド更新要件を修正する。
- `release-hld-docx`: Release Asset を HLD と PRD の2文書へ拡張する。

## Impact

- `.agents/skills/markdown2docx/` の変換契約、参照 DOCX および補助処理。
- `.github/workflows/` の Release Workflow。
- `tests/test_markdown2docx.py` と配布 DOCX の検証方法。
- `openspec/publics/prd.md` と `hld.md` は正本として維持する。

## Stakeholders and Lifecycle Impact

- 取得・供給: 利用者は同じ Release から PRD と HLD を取得できる。
- 移行: 公開済み `v0.0.0` とタグは変更せず、修正版を次の Patch Release として供給する。
- 運用・保守: 生成時に構造検査とフィールド更新を行い、Release 前に描画結果を確認する。
- 廃止: 旧変換引数だけに依存する経路を削除し、正本 Markdown は保持する。

## Quality Considerations

| 品質特性 | ID | 目標と検証 |
| --- | --- | --- |
| 機能適合性 | QR-DOCX-001 | PRD/HLD の目次に1件以上、表一覧に全表と同数の項目を表示し、見出し3件を指定日本語にする。OOXML と描画で確認する。 |
| 使用性 | QR-DOCX-002 | 全表に内容を識別できる日本語キャプションを表示する。OOXML と全ページ描画で確認する。 |
| 互換性 | QR-DOCX-003 | Word と自動 Release の双方で表示可能な DOCX とし、正本 Markdownを変更しない。Hash と変換 Test で確認する。 |
| 信頼性 | QR-DOCX-004 | 2文書のいずれかの生成・検査に失敗した場合、Release を公開しない。Workflow Review で確認する。 |
| 保守性 | QR-DOCX-005 | PRD/HLD に同じ変換処理を適用し、生成 DOCX の Git 追跡件数を0件に保つ。差分と Git 状態で確認する。 |
| 移植性 | QR-DOCX-006 | 全 Section の余白を 1440/1440/1080/1080 twip とし、構造 Test で確認する。 |
| 性能効率性 | — | Release 時に2文書を処理するだけであり、独立した性能目標は不要。 |
| セキュリティ | — | 新しい入力境界、Credential または外部公開範囲を追加しない。 |
