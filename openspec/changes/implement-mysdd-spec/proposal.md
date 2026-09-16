<!-- markdownlint-disable MD041 -->

## Why

`docs/references/MySDD-Spec.md`が定める構成のうち、共通DOCX変換Skill
`_md2docx`への責務移管と一部Template項目が未実装であり、仕様書と実体が
一致していない。既存の`gen-pd`、`gen-bd`、`mysdd` Schemaを維持したまま、
残る差分を解消してMySDDを一貫して運用可能な状態にする。

## What Changes

- 正本Markdownを既存RendererでDOCXへ変換する共通Agent Skill
  `_md2docx`を追加する。
- `gen-pd`と`gen-bd`は文書内容の生成に専念し、DOCX変換を
  `_md2docx`へ委譲する。
- 旧`.agents/skills/_shared/document-generation.md`を、参照を残さず
  `_md2docx`へ置き換える。
- MySDDの`design.md`と`tasks.md` Templateを仕様書およびSchema指示と
  照合し、不足する設計項目と検証Evidenceの記入欄を補う。
- `MySDD-Spec.md`と`MySDD-Workflow.md`を実装後の構成、状態、検証手順へ
  合わせ、外部参照を最終`References`節へ統一する。
- Schema、Change、DOCX変換、Skill参照、Markdownを検証し、仕様書の
  受け入れ条件を満たすEvidenceを残す。

## Capabilities

### New Capabilities

- `md2docx`: 正本Markdownを内容変更せず、共通参照書式を使った同名DOCXへ
  安全に変換し、成功または部分失敗を呼び出し元へ報告する。

### Modified Capabilities

なし。既存の`add-gen-pd-gen-bd` Changeが定義する`gen-pd`、`gen-bd`、
`mysdd-schema`の外部要件は変更せず、実装上の責務分離と不足項目だけを補う。

## Impact

- `.agents/skills/_md2docx/`
- `.agents/skills/_shared/document-generation.md`
- `.agents/skills/gen-pd/SKILL.md`
- `.agents/skills/gen-bd/SKILL.md`
- `openspec/schemas/mysdd/templates/design.md`
- `openspec/schemas/mysdd/templates/tasks.md`
- `scripts/openspec/render-docx.ps1`
- `scripts/openspec/test-render-docx.ps1`
- `docs/references/MySDD-Spec.md`
- `docs/references/MySDD-Workflow.md`

既存の`gen-pd`と`gen-bd`の呼び出し方法、生成先、Markdown正本方針、
MySDDの4 ArtifactおよびApply依存は変更しない。

## Stakeholders and Lifecycle Impact

- ステークホルダ: MySDD利用者、Change作成者、Agent Skill保守者が対象。
- 取得・供給: 新規外部ServiceやLibraryの導入はないため対象外。既存の
  mise、Pandoc、PowerShell Script、`reference.docx`を継続利用する。
- 移行: `gen-pd`と`gen-bd`の参照先を同じ変更で切り替え、旧共通手順を
  参照がなくなった後に削除する。利用者向けInterfaceは維持する。
- 運用: 変換成功、入力不足、Pandoc失敗を区別して報告し、DOCX失敗時も
  正本Markdownを保持する。
- 保守: DOCX変換規則を`_md2docx`へ一元化し、文書固有規則は各生成Skillの
  Assetと`SKILL.md`に残す。
- 廃止: `_shared/document-generation.md`は参照切れ検査後に削除する。
- Rollback: `_md2docx`への参照変更と旧共通手順の削除を一組として戻し、
  生成済みMarkdownは保持する。

## Quality Considerations

<!-- markdownlint-disable MD013 -->
| ID | ISO/IEC 25010品質特性 | 適用 | Measure／Target | Conditions | Verification Method |
| --- | --- | --- | --- | --- | --- |
| `QR-001` | 機能適合性 | 適用 | 要件定義書・基本設計書の両方でMarkdownから同名DOCXを生成できる | 必須入力と参照DOCXが存在する | RendererテストとSkill定義Review |
| `QR-002` | 性能効率性 | 対象外 | 対話的な単一文書変換で性能目標を設けない | 通常のMySDD Change | 理由のReview |
| `QR-003` | 互換性 | 適用 | 既存Skill名、入出力先、4 Artifactを変更しない | 現行の`gen-pd`、`gen-bd`、`mysdd` | Schema Validationと差分Review |
| `QR-004` | インタラクション能力 | 適用 | 失敗時に不足入力または変換失敗を明示する | 入力不足、Pandoc失敗 | 失敗ScenarioのReviewとテスト |
| `QR-005` | 信頼性 | 適用 | DOCX失敗時にMarkdownを失わず部分成功を報告する | Rendererが非ゼロ終了する | 失敗系テスト |
| `QR-006` | セキュリティ | 適用 | Literal pathを用い、指定外の文書や秘密情報を生成物へ追加しない | Repository内の正本Markdownを変換する | Skill定義とScriptのReview |
| `QR-007` | 保守性 | 適用 | DOCX変換規則の正本を1 Skillにし、旧共通手順への参照を0件にする | 移行完了後 | `rg`による参照検査 |
| `QR-008` | 柔軟性 | 適用 | `rd.md`と`bd.md`の両方を同一Interfaceで変換できる | 出力先が入力と同じDirectory | 2文書種別の変換テスト |
| `QR-009` | 安全性 | 対象外 | 人身、設備、環境へ危害を与える制御を行わない | 文書変換処理 | 理由のReview |
<!-- markdownlint-enable MD013 -->
