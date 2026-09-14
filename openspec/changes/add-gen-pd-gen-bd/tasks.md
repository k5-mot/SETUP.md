## 1. 共通変換

- [x] 1.1 Pandocと`reference.docx`を使う共通DOCX変換処理を追加し、サンプルMarkdownからDOCXを生成できることを確認する
- [x] 1.2 `openspec/changes/**/docs/*.docx`をGit管理外にし、Markdownと`reference.docx`だけが追跡されることを確認する

## 2. gen-pd

- [x] 2.1 `.agents/skills/gen-pd/SKILL.md`を`proposal`と`specs`から`docs/rd.md`を生成する規則へ更新し、Skill定義を読み込めることを確認する
- [x] 2.2 `spec-driven`形式のサンプルから`rd.md`と`rd.docx`を生成し、RequirementとScenarioの参照が保持されることを確認する
- [x] 2.3 必須Artifact欠落とDOCX変換失敗を試し、誤って生成完了を報告しないことを確認する

## 3. gen-bd

- [x] 3.1 `.agents/skills/gen-bd/SKILL.md`を`proposal`、`specs`、任意の`design`から`docs/bd.md`を生成する規則へ更新し、Skill定義を読み込めることを確認する
- [x] 3.2 `spec-driven`形式のサンプルから`bd.md`と`bd.docx`を生成し、Requirement、Scenario、設計判断の参照が保持されることを確認する
- [x] 3.3 Design省略とDOCX変換失敗を試し、`TBD`と部分成功が報告されることを確認する

## 4. sdd-custom

- [x] 4.1 `spec-driven`を維持した`sdd-custom`へ`rd`と`bd`を追加し、Schema検証が成功することを確認する
- [x] 4.2 `rd.md`と`bd.md`のTemplateを追加し、Artifact指示が各Skillと`docs/`配下の出力先を示すことを確認する
- [x] 4.3 既定Schemaを`sdd-custom`へ変更し、`tasks`、`rd`、`bd`が揃うまでApplyがBlockedになることを確認する

## 5. 検証

- [x] 5.1 両Skillを同じテストChangeへ実行し、`docs/rd.md`と`docs/bd.md`だけが生成されることを確認する
- [x] 5.2 `openspec schema validate sdd-custom`と`openspec validate add-gen-pd-gen-bd --strict`を実行し、エラーがないことを確認する
