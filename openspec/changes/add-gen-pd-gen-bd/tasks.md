## 1. 共通変換

- [x] 1.1 Pandocと`reference.docx`を使う共通DOCX変換処理を追加し、サンプルMarkdownからDOCXを生成できることを確認する
- [x] 1.2 `openspec/artifacts/**/*.docx`をGit管理外にし、Markdownと`reference.docx`だけが追跡されることを確認する

## 2. gen-pd

- [x] 2.1 `.agents/skills/gen-pd/SKILL.md`へ入力、出力、必須章、`TBD`、ID保持の規則を実装し、Skill定義を読み込めることを確認する
- [x] 2.2 要求Artifactのサンプルから`要件定義書.md`と`要件定義書.docx`を生成し、要求IDとトレーサビリティが保持されることを確認する
- [x] 2.3 必須Artifact欠落とDOCX変換失敗を試し、誤って生成完了を報告しないことを確認する

## 3. gen-bd

- [ ] 3.1 `.agents/skills/gen-bd/SKILL.md`へ入力、出力、必須章、`TBD`、ID保持の規則を実装し、Skill定義を読み込めることを確認する
- [ ] 3.2 設計Artifactのサンプルから`基本設計書.md`と`基本設計書.docx`を生成し、要求・方式・設計IDとADR参照が保持されることを確認する
- [ ] 3.3 必須Artifact欠落とDOCX変換失敗を試し、誤って生成完了を報告しないことを確認する

## 4. 検証

- [ ] 4.1 両Skillを同じChangeへ再実行し、規定の出力先だけが更新されることを確認する
- [ ] 4.2 `openspec validate add-gen-pd-gen-bd --strict`を実行し、エラーがないことを確認する
