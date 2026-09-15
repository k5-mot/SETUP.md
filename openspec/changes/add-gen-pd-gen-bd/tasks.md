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

## 4. MySDD

- [x] 4.1 `spec-driven`の4 Artifactと依存関係を維持し、Schema検証が成功することを確認する
- [x] 4.2 4つのSchema TemplateへISO/IEC/IEEE 12207とISO/IEC 25010の観点を追加し、Proposeの出力に反映されることを確認する
- [x] 4.3 `rd`と`bd`をSchema Artifactから外し、Applyの依存が`tasks`のみであることを確認する

## 5. 検証

- [x] 5.1 `rd.md`と`bd.md`のTemplateを各SkillのAssetへ分離し、Schemaに依存せず正式文書を生成できることを確認する
- [x] 5.2 `openspec schema validate mysdd`と`openspec validate add-gen-pd-gen-bd --strict`を実行し、エラーがないことを確認する
