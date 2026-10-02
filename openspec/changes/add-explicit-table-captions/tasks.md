<!-- markdownlint-disable MD041 MD013 -->

## 1. Regression Contract

- [ ] 1.1 明示表題、同一Section内の異なる表題、未指定時の互換動作を検査する最小回帰Testを追加し、現行処理で明示表題の検査が失敗することを確認する（QR-DOCX-002、003、007）。

## 2. Caption Generation

- [ ] 2.1 表直前の `表題: <caption>` 段落を既存の表走査処理で `TableCaption` へ変換し、回帰TestでDOCXと表一覧の表示値が一致することを確認する（QR-DOCX-002、005、007）。
- [ ] 2.2 明示表題がない表では既存のSection名由来キャプションを維持し、互換Testが成功することを確認する（QR-DOCX-003、移行）。

## 3. Canonical Documents and Documentation

- [ ] 3.1 `prd.md` と `hld.md` の全表へ内容に合う固有の表題を追加し、表題数と表数が一致することを検査する（QR-DOCX-007、運用・保守）。
- [ ] 3.2 `markdown2docx` Skillと書式仕様へ表題記法を追記し、Markdown lintとLink検査が成功することを確認する（QR-DOCX-005、Support）。

## 4. Verification and Publication

- [ ] 4.1 OpenSpec、Ruff、DOCX回帰Testを実行し、PRD/HLDの全ページ描画で表キャプションと表一覧に欠け・重なりがないことを確認する（QR-DOCX-002、003、005、007）。
- [ ] 4.2 Changeを検証・Archiveし、PRとCI成功後にPatch ReleaseへPRD/HLDを登録して再ダウンロード検証を行う（移行・供給）。
