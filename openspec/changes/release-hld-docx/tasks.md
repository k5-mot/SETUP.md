<!-- markdownlint-disable MD041 MD013 -->

## 1. Release Workflow

- [x] 1.1 `.github/workflows/` にタグ形式、main 包含、対象 Commit の `quality` 成功を確認する Job を追加し、不正なタグで Release 処理に進まないことを Workflow Review で確認する（QR-REL-003、供給）。
- [x] 1.2 `mysdd` Schema 検証と既存 Pandoc 契約による `hld.docx` 生成を追加し、ローカル変換 Test と非空出力で確認する（QR-REL-001、QR-REL-004、保守）。
- [x] 1.3 検証後の `gh release create --verify-tag` に DOCX Asset を渡し、失敗時に公開 Step が実行されないことを Workflow Review で確認する（QR-REL-002、運用）。

## 2. Integration and Operation

- [x] 2.1 Workflow 構文、OpenSpec、Markdown、既存 DOCX Test を確認し、生成 DOCX が Git 管理外で、次の手動タグから適用できることを確認する（QR-REL-001～004、移行・廃止）。
