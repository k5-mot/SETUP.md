<!-- markdownlint-disable MD041 MD013 -->

## 1. Regression Contract

- [x] 1.1 PRD/HLD の日本語ナビゲーション見出し、表示項目、全表 Caption、指定余白を検査する回帰 Test を追加し、旧変換で失敗することを確認する（QR-DOCX-001～003、006）。

## 2. DOCX Generation

- [x] 2.1 全表に文脈付き日本語 Caption を付与し、ナビゲーション見出しと参照 Style を修正する共通処理を実装し、表数と Caption 数が一致することを確認する（QR-DOCX-001、002、保守）。
- [x] 2.2 参照 DOCX の全 Section を指定余白へ更新し、Style 文書と OOXML Test の値が一致することを確認する（QR-DOCX-006、移行）。
- [x] 2.3 フィールド対応 Engine で目次・図一覧・表一覧を更新して保存し、PRD/HLD の表示項目とページ番号が描画されることを確認する（QR-DOCX-001、003、運用）。

## 3. Release and Documentation

- [x] 3.1 `markdown2docx` Skill と書式仕様を新しい変換・検証契約へ更新し、Markdown lint と Link 検査に成功することを確認する（QR-DOCX-003、005、保守）。
- [x] 3.2 Release Workflow で PRD/HLD を生成・検査後に2 Asset を同時登録し、部分 Release 経路がないことを Workflow 構文検査で確認する（QR-DOCX-004、供給）。

## 4. Verification and Publication

- [x] 4.1 OpenSpec、Python品質、DOCX回帰 Testを実行し、両DOCXの全ページ描画に欠け・重なり・表崩れがないことを確認する（QR-DOCX-001～006）。
- [ ] 4.2 Change を検証・Archiveし、PRで`main`へ統合できる状態にする（移行・運用・供給）。
