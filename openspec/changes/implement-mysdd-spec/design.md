<!-- markdownlint-disable MD041 -->

## Context

変更理由は[Proposal](proposal.md)を参照する。現在の`gen-pd`と`gen-bd`は
`.agents/skills/_shared/document-generation.md`を読み、文書生成とDOCX変換の
共通手順をそこから取得している。DOCX変換自体は
`scripts/openspec/render-docx.ps1`に実装済みで、参照書式と変換テストも存在する。

一方、MySDD仕様は共通変換をAgent Skill `_md2docx`として分離すること、
MySDDのDesign TemplateへMigration PlanとOpen Questionsを含めること、各Taskに
検証Evidenceを含めることを求めている。既存の`add-gen-pd-gen-bd` Changeは
`gen-pd`、`gen-bd`、`mysdd-schema`の外部要件を定義済みであるため、本Changeは
その契約を変更せず、未実装の共通変換Capabilityと構造上の差分だけを扱う。

## Goals / Non-Goals

**Goals:**

- `_md2docx`をDOCX変換契約の唯一のAgent Skillにする。
- 文書内容の生成と形式変換の責務を分離する。
- 既存Renderer、参照DOCX、出力先、部分成功の扱いを維持する。
- MySDD Templateと文書を`MySDD-Spec.md`の定義へ一致させる。
- 正常系と失敗系を自動検証できる状態にする。

**Non-Goals:**

- `gen-pd`または`gen-bd`が生成する章立てや外部Interfaceの変更
- MySDD Artifact Graph、Delta Spec構文、Apply依存の変更
- 新しいDOCX Rendererまたは外部Dependencyの導入
- DOCXからMarkdownへの逆変換
- 既存の`add-gen-pd-gen-bd` Changeの履歴改変

## Decisions

### `_md2docx`を薄いAgent Skillとして追加する

`.agents/skills/_md2docx/SKILL.md`は、変換前の入力検証、許可する出力先、
既存Rendererの呼び出し、成功判定、失敗報告だけを定義する。文書内容の生成、
章立て、`TBD`補完、トレーサビリティ作成は担当しない。

Interfaceは変換元Markdownと出力先DOCXを受け取り、出力先が入力と同じ
Directoryかつ同じBase nameであることを検証する。参照書式は
`openspec/document-templates/reference.docx`へ固定し、RendererにはLiteral
pathとして渡す。

代替案として、旧`_shared`文書を残す方法は変更量が少ないが、呼び出し可能な
Skillとして責務が明確にならず、MySDD仕様とも一致しないため採用しない。
各生成Skillへ変換手順を複製する方法も、修正箇所が増えるため採用しない。

### 文書生成Skillから変換Skillへ明示的に委譲する

`gen-pd`と`gen-bd`は固有Assetを使ったMarkdown生成までを担当し、その後に
`_md2docx`の手順へ委譲する。必須Artifact不足は各生成Skill、変換入力不足と
Renderer失敗は`_md2docx`が報告する。DOCX変換失敗時も生成済みMarkdownを
保持し、生成全体を部分成功として扱う。

移行は`_md2docx`追加、2 Skillの参照更新、参照切れ検査、旧`_shared`削除の
順に行い、中間状態で参照先が存在しない時間を作らない。

### 既存Schemaの構造を変えずTemplateの不足だけを補う

`design.md` Templateへ`Migration Plan`と`Open Questions`を追加し、Schemaの
instructionとMySDD仕様の章立てを一致させる。`tasks.md` TemplateのTask例は、
各項目にテスト、Command、観測結果または成果物による完了確認を含む形式へ
変更する。Artifact ID、依存関係、出力先には触れない。

### 仕様書は検証完了後の実体を記録する

`MySDD-Spec.md`のStatusはすべての受け入れ条件を満たした時点で
`Implemented`へ変更する。想定Directory構成は`_md2docx`を実在する構成として
示し、廃止した`_shared`を残さない。`MySDD-Workflow.md`はDOCX変換の委譲関係を
簡潔に補足する。外部資料を使う両文書の最終節はProject規約どおり
`## References`とする。

## Quality Attribute Design

<!-- markdownlint-disable MD013 -->
| Quality ID | 設計上の対応 | Trade-off | Verification Evidence |
| --- | --- | --- | --- |
| `QR-001` | 既存Rendererと参照DOCXを薄いSkillから再利用する | Renderer固有の制約を引き継ぐ | `rd.md`と`bd.md`の変換テスト |
| `QR-003` | Skill名、入出力先、Schemaの4 Artifactを維持する | 既存Interfaceの整理は行わない | Schema Validationと差分Review |
| `QR-004` | 入力不足とRenderer失敗を別の失敗理由として報告する | Error分類をSkill指示で管理する | 失敗Scenarioの検証記録 |
| `QR-005` | Renderer実行前後でMarkdownを更新しない | DOCX失敗時に全体成功にはならない | 入力Hash比較と非ゼロ終了テスト |
| `QR-006` | Literal pathと同一Directory・Base name制約を使う | 任意出力先への変換は許可しない | 許可外Pathの失敗系テスト |
| `QR-007` | 変換規則を`_md2docx/SKILL.md`へ一元化する | Skill間の委譲が1段増える | 旧`_shared`参照0件の検索結果 |
| `QR-008` | 文書種別に依存しない入力・出力Interfaceにする | DOCX固有の個別調整は参照書式側で行う | 2文書種別の同一手順による変換結果 |
<!-- markdownlint-enable MD013 -->

`QR-002`と`QR-009`はProposalの理由どおり対象外とする。

## Lifecycle, Migration and Operations

- 移行: 新Skillを追加してから呼び出し元を切り替え、旧手順を最後に削除する。
- Rollback: 旧手順と2 Skillの参照を同一Commit単位で復元する。生成済みの
  MarkdownとChange Artifactは削除しない。
- 運用: 成功時は生成DOCXのPath、失敗時は不足PathまたはRendererの失敗理由を
  報告する。
- Support: 問題の切り分けはSkill入力検証、Renderer、参照DOCXの順に行う。
- 保守: Rendererの変更時は`_md2docx`の契約と変換テストを同時に更新する。
- 廃止: `_shared/document-generation.md`とその参照は移行完了時に廃止する。

## Risks / Trade-offs

- `[Skillから別Skillへの委譲方法がAgentごとに異なる]` → 相対Linkで
  `_md2docx/SKILL.md`を必読手順として指定し、入力と期待結果を明記する。
- `[既存Changeと要件が重複する]` → 新Delta Specは`md2docx`だけに限定し、
  `gen-pd`、`gen-bd`、`mysdd-schema`は実装互換性の検証対象に留める。
- `[出力先制約が既存Scriptより厳しい]` → 制約はSkill境界で検証し、汎用の
  Renderer Script自体は変更しない。
- `[文書だけがImplementedになり実装が未完了になる]` → Status変更を全検証の
  最終Taskにし、失敗時は`Proposed`を維持する。

## Migration Plan

1. `_md2docx/SKILL.md`を追加し、既存Rendererによる正常系と失敗系を検証する。
2. `gen-pd`と`gen-bd`を新Skillへ委譲する記述へ更新する。
3. Repository内の旧共通手順への参照が0件であることを確認して削除する。
4. MySDD Templateの不足見出しとTaskのEvidence記述を補う。
5. MySDD文書を実装状態へ更新し、Schema、Change、DOCX、Markdownを検証する。
6. 失敗した場合は文書Statusを変更せず、該当段階の変更を戻して再検証する。
