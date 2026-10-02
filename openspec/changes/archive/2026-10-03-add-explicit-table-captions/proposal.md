<!-- markdownlint-disable MD013 MD033 MD041 -->

## Why

現在の DOCX 生成は表キャプションを直前のセクション名から自動生成するため、表の内容を表す固有名を設定できない。正本 Markdown で表ごとの名称を管理し、DOCX と表一覧へ同じ名称を反映できるようにする。

## What Changes

- Pandoc Markdown の `table_captions` 記法で指定した表題を DOCX の表キャプションとして使用する。
- Pandoc の `gfm` Readerを基礎として、GFM構文と既存の `implicit_figures` を維持する。
- Pandoc固有構文は明示的に追加・検証したものだけを許可し、対応範囲を書式仕様へ記録する。
- 日本語Navigation、表Caption、余白および表Styleは、Pandocまたはreference.docxで表現できる範囲をそちらへ移し、重複するOOXML編集を削除する。
- PythonのOOXML編集は、Office Engine保存後の互換補正など、Pandocとreference.docxで表現できない処理へ限定する。
- PRD と HLD の全表へ、表の内容に合う固有の表題を設定する。
- 明示的な表題がない既存文書では、現在のセクション名由来のキャプションを維持する。
- DOCX の全表と表一覧に、明示した表題が反映されることを検証する。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `markdown2docx`: 正本 Markdown で指定した表ごとの表題を、DOCX の表キャプションと表一覧へ反映する。

## Impact

- `.agents/skills/markdown2docx/` の表キャプション変換、Pandoc Filterおよび書式仕様。
- `.agents/skills/markdown2docx/references/template.docx` のStyle名、余白および表Style。
- Pandocの日本語翻訳Dataと変換Option。
- `.agents/skills/markdown2docx/` の利用手順と書式仕様。
- `openspec/publics/prd.md` と `openspec/publics/hld.md` の全表。
- `tests/test_markdown2docx.py` のキャプション検証。
- 新しい依存 Package は追加しない。

## Stakeholders and Lifecycle Impact

- 取得・供給: 文書利用者は表一覧から表の内容を直接判別できる。
- 移行: 既存の表題未指定 Markdown は従来の自動キャプションで変換できる。
- 運用・保守: 文書作成者が正本 Markdown で表題を編集し、DOCX 再生成時に反映する。
- 廃止: 表題を廃止する場合は正本 Markdown の Pandoc表キャプションと変換処理を同時に除去する。

## Quality Considerations

| 品質特性 | ID | 目標と検証 |
| --- | --- | --- |
| 機能適合性 | QR-DOCX-002 | PRD/HLD の全表で Markdown の表題と DOCX のキャプションが一致する。OOXML Test で確認する。 |
| 使用性 | QR-DOCX-007 | 表一覧の各項目が対応する表の内容を識別できる固有名を持つ。全ページ描画で確認する。 |
| 互換性 | QR-DOCX-003 | 表題未指定の既存 Markdown も従来どおり変換できる。回帰 Test で確認する。 |
| 互換性 | QR-DOCX-008 | Pandoc `gfm` Readerが扱うGFM構文を維持し、互換Fixtureで確認する。 |
| 保守性 | QR-DOCX-005 | Pandoc／reference.docxと重複するOOXML編集を0件にし、PRD/HLD に同じ規則を適用する。責務表と差分 Review で確認する。 |
| 信頼性 | — | Release の既存生成・検証 Gateを使用するため、独立した目標は追加しない。 |
| 性能効率性 | — | 表直前の1段落を判定するだけであり、独立した性能目標は不要。 |
| セキュリティ | — | 新しい外部入力、Credential、通信または実行経路を追加しない。 |
| 移植性 | — | 標準 OOXML と既存 Pandoc 出力だけを使用し、対応環境を変更しない。 |
