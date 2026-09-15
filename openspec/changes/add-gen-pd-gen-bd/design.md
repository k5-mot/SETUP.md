## Context

📄 `mysdd`は標準の4 ArtifactへISO観点を追加し、`gen-pd`と`gen-bd`はProposeと分離して正式文書を生成する。Skill名と正本の扱いは[ADR-006](../../../docs/adr/ADR.md#adr-006-openspecのmarkdownを正本とする)および[ADR-008](../../../docs/adr/ADR.md#adr-008-文書生成をgen-pdとgen-bdへ分離する)に従う。

## Goals / Non-Goals

**Goals:**

- `.agents/skills/gen-pd/`と`.agents/skills/gen-bd/`を独立して実行できるようにする。
- `spec-driven`のProposal、Delta Spec、Design、Tasksの構造と依存関係を維持する。
- ProposeがISO/IEC/IEEE 12207とISO/IEC 25010の観点を4 Artifactへ反映する。
- `rd`と`bd`を各Skill固有のTemplate Assetから別途生成する。
- 入力ArtifactのIDと参照関係を保持する。
- Markdown生成後にPandocでDOCXを生成する。
- 不足情報と変換失敗を利用者へ明示する。

**Non-Goals:**

- OpenSpec Artifactに存在しない要求や設計の補完
- DOCXからMarkdownまたはOpenSpecへの逆同期
- ISO規格への適合認証

## Decisions

SkillのInterface、出力先、変換順、共通DOCX変換は[ADR-010](../../../docs/adr/ADR.md#adr-010-文書生成のinterfaceと変換順を固定する)に従う。`rd`は`proposal`と`specs`、`bd`は同じ入力と存在する場合の`design`を使う。Schema上のApply開始条件はFork元と同じ`tasks`とし、MySDD運用上は正式文書の生成後にApplyを開始する。

## Risks / Trade-offs

- `[入力表記の揺れ]` → OpenSpecのRequirement見出しとScenario名を参照名として使い、既存IDがある場合は保持する。
- `[Pandocまたはreference.docxがない]` → Markdown生成を完了させ、DOCXだけを失敗として報告する。
- `[2つのSkillで変換処理が重複する]` → 共通変換処理を再利用し、文書固有の構成だけを各Skillに持たせる。
