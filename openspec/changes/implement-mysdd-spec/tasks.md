<!-- markdownlint-disable MD013 MD041 -->

## 1. 共通DOCX変換Skill

- [ ] 1.1 `.agents/skills/_md2docx/SKILL.md`を追加し、入力、同一Directory・Base name制約、参照DOCX、Renderer、成功条件、部分失敗を定義して、Frontmatterと相対LinkをReviewする
- [ ] 1.2 `scripts/openspec/test-render-docx.ps1`を要件定義書・基本設計書の代表入力、非ゼロDOCX、代表ID、変換前後のMarkdown Hash、入力不足で検証できるように更新し、テストが期待した`PASS`を返すことを確認する
- [ ] 1.3 許可外の出力先と不足入力を拒否し、指定外Pathへ書き込まない手順が`_md2docx`にあることをScenario単位でReviewし、`QR-004`、`QR-005`、`QR-006`のEvidenceを記録する

## 2. 文書生成Skillの移行

- [ ] 2.1 `gen-pd/SKILL.md`をMarkdown生成後に`_md2docx`へ委譲する手順へ更新し、既存の入力、Asset、出力先、`TBD`、部分成功の契約が維持されていることを差分で確認する
- [ ] 2.2 `gen-bd/SKILL.md`をMarkdown生成後に`_md2docx`へ委譲する手順へ更新し、既存の入力、Asset、出力先、Design省略、`TBD`、部分成功の契約が維持されていることを差分で確認する
- [ ] 2.3 `.agents/skills/`内の旧共通手順への参照が0件であることを`rg`で確認してから`_shared/document-generation.md`を削除し、`_md2docx`が変換規則の唯一のSkillであることを確認する

## 3. MySDD Templateの整合

- [ ] 3.1 `templates/design.md`へ`Migration Plan`と`Open Questions`を追加し、Schema instructionが求める設計項目をTemplateがすべて提示することを照合する
- [ ] 3.2 `templates/tasks.md`のTask例へテスト、Command、観測結果または成果物による完了確認を組み込み、各TaskがEvidenceを記録できることをReviewする
- [ ] 3.3 MySDDのSchema ValidationとTemplate解決確認を実行し、Artifactが標準4件、Apply依存が`tasks`のみ、解決Templateが4件だけであることをEvidenceとして保存する

## 4. MySDD文書の実装反映

- [ ] 4.1 `MySDD-Spec.md`のDirectory構成、Agent Skills、運用手順を実装後の実体へ合わせ、旧`_shared`を除去して最終節を`References`へ変更し、相対Linkと目次Anchorを確認する
- [ ] 4.2 `MySDD-Workflow.md`へ`gen-pd`・`gen-bd`から`_md2docx`への委譲と失敗時の責務を簡潔に反映し、最終節を`References`へ変更して重複規則がないことをReviewする

## 5. 受け入れ検証と移行完了

- [ ] 5.1 DOCX変換テストを実行し、`rd.md`と`bd.md`の変換、非ゼロSize、代表ID、Markdown保持が`QR-001`、`QR-005`、`QR-008`のTargetを満たすことを確認する
- [ ] 5.2 `mysdd` Schema、`implement-mysdd-spec` Change、既存`add-gen-pd-gen-bd` Changeを厳格検証し、すべて成功して既存Capabilityとの互換性が保たれることを確認する
- [ ] 5.3 miseでNode.jsとnpmを有効化して変更対象MarkdownへMarkdownlintを実行し、エラー0件と最終`References`節を確認する
- [ ] 5.4 旧共通手順への実行時参照、予期しない生成物、秘密情報、差分の空白Errorがないことを確認した後、`MySDD-Spec.md`のStatusを`Implemented`へ更新してMarkdownlintを再実行する
