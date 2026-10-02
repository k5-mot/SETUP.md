<!-- markdownlint-disable MD041 MD013 -->

## 1. Regression Contract

- [ ] 1.1 Pandoc標準表題、同一Section内の異なる表題、未指定時の互換動作を検査する最小回帰Testを追加し、現行処理で表題の検査が失敗することを確認する（QR-DOCX-002、003、007）。
- [ ] 1.2 Pandoc `gfm` Readerで有効な構文を網羅する互換Fixtureを追加し、既存GFM要素を解析できることをASTで確認する（QR-DOCX-003、008）。

## 2. Caption Generation

- [ ] 2.1 `gfm+implicit_figures` Readerを維持し、Pandoc標準の表題段落をTable Captionへ変換する最小Lua Filterを追加して回帰Testを通す（QR-DOCX-003、005、007、008）。
- [ ] 2.2 Filterが生成した `TableCaption` の個別名を保持して連番を付与し、DOCXと表一覧の表示値が一致することを確認する（QR-DOCX-002、005、007）。
- [ ] 2.3 表題がない表では既存のSection名由来キャプションを維持し、互換Testが成功することを確認する（QR-DOCX-003、移行）。

## 3. Pandoc and Reference DOCX Responsibilities

- [ ] 3.1 Pandocの日本語翻訳Dataで `目次`、`図一覧`、`表一覧` を生成し、Pythonの見出し置換を削除して構造Testを通す（QR-DOCX-001、005）。
- [ ] 3.2 reference.docxの図表Caption Style名をPandocのField参照へ合わせ、PythonのField Code置換を削除して一覧更新Testを通す（QR-DOCX-001、005）。
- [ ] 3.3 reference.docxだけで余白と表中央配置を検証し、変換直後の重複補正を削除する。LibreOffice保存後に崩れる項目だけ再現Test付きで維持する（QR-DOCX-005、006、移植性）。
- [ ] 3.4 全Rowへの `cantSplit` 追加と対応Testを削除し、表Rowの改PageをWord／LibreOfficeの標準配置へ戻す（保守）。
- [ ] 3.5 Office Engine後の互換補正は、各処理に対応する失敗再現Testがあるものだけ残す（信頼性、保守）。

## 4. Canonical Documents and Documentation

- [ ] 4.1 `prd.md` と `hld.md` の全表へ `: <caption>` 形式で内容に合う固有の表題を追加し、表題数と表数が一致することを検査する（QR-DOCX-007、運用・保守）。
- [ ] 4.2 `markdown2docx` Skillと書式仕様へGFM構文、対応するPandoc追加構文、DOCX表現の制限および責務表を追記し、Markdown lintとLink検査が成功することを確認する（QR-DOCX-005、008、Support）。

## 5. Verification and Publication

- [ ] 5.1 OpenSpec、Ruff、DOCX回帰Testを実行し、PRD/HLDの全ページ描画で表キャプションと表一覧に欠け・重なりがないことを確認する（QR-DOCX-002、003、005、007）。
- [ ] 5.2 Changeを検証・Archiveし、PRとCI成功後にPatch ReleaseへPRD/HLDを登録して再ダウンロード検証を行う（移行・供給）。
