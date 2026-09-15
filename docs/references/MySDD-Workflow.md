# 🚀 MySDD ワークフロー

MySDDは、OpenSpecの`spec-driven`をForkし、要件定義書`rd`と基本設計書`bd`を追加したSchemaである。機械識別子には`mysdd`を使う。Schemaの定義は[MySDD仕様](MySDD-Spec.md)、OpenSpec標準の用語と操作は[OpenSpecワークフロー](OpenSpec-Workflow.md)を参照する。

## 🛹 使い方の流れ

```mermaid
flowchart LR
    P["`$openspec-propose`<br/>6つのArtifactを作成"] --> A["`$openspec-apply-change`<br/>実装とテスト"]
    A --> V["`$openspec-verify-change`<br/>実装とArtifactを検証"]
    V -->|合格| R["`$openspec-archive-change`<br/>Spec反映と履歴化"]
    V -->|不合格| A
    R --> C["正本仕様<br/>openspec/specs/"]
    R --> H["変更履歴<br/>changes/archive/"]
```

MySDDでは`proposal`、`specs`、`design`、`tasks`に`rd`、`bd`を加えた6つをChangeのArtifactとする。Markdownが正本、DOCXは配布用の再生成物である。

## 1️⃣ `$openspec-propose`; 6つのArtifactを作成

```text
# MySDD Changeと必要なArtifactを一括生成する。
$openspec-propose <変更名または変更内容>
```

`gen-pd`が`rd.md`と`rd.docx`、`gen-bd`が`bd.md`と`bd.docx`を生成する。入力Artifactにない事実は補完せず、未確定事項は`TBD`とする。

```text
openspec/changes/<change-name>/
├─ .openspec.yaml
├─ proposal.md
├─ specs/
│  └─ <capability>/spec.md
├─ design.md
├─ tasks.md
└─ docs/
   ├─ rd.md                         # 要件定義書の正本
   ├─ rd.docx                       # 要件定義書の配布物
   ├─ bd.md                         # 基本設計書の正本
   └─ bd.docx                       # 基本設計書の配布物
```

6つのArtifactが揃えば完了である。必須Markdownが欠ける場合はApplyへ進まない。DOCXだけが失敗した場合はMarkdownを保持し、原因を修正して再生成する。

## 2️⃣ `$openspec-apply-change`; ドキュメントに従って実装

```text
# tasks.mdに従って実装し、完了項目を更新する。
$openspec-apply-change <change-name>
```

Applyは`tasks`、`rd`、`bd`が揃うまでBlockedになる。実装中に要求または設計が変わった場合は、先にArtifactを更新して正本と実装を一致させる。

## 3️⃣ `$openspec-verify-change`; 実装を検証

```text
# 実装、6つのArtifact、テスト証跡を照合する。
$openspec-verify-change <change-name>
```

次を確認する。

- RequirementとScenarioが実装・テストへ追跡できる。
- `rd.md`と`bd.md`が入力Artifactと整合し、未達の品質目標がない。
- Schema Validation、Change Validation、Projectのテストが成功する。

CRITICALな不整合、参照切れ、失敗テストがある場合はArchiveへ進まず、ApplyとVerifyを再実行する。

## 4️⃣ `$openspec-archive-change`; Spec反映と変更の履歴化

```text
# 検証済みChangeをArchiveする。
$openspec-archive-change <change-name>
```

Delta SpecがMain Specへ反映され、Change全体が`openspec/changes/archive/`へ移動する。Archiveが失敗した場合は手作業で移動せず、ValidationまたはSyncの原因を解消する。

```text
openspec/changes/archive/YYYY-MM-DD-<change-name>/
├─ .openspec.yaml
├─ proposal.md
├─ specs/<capability>/spec.md
├─ design.md
├─ tasks.md
└─ docs/
   ├─ rd.md
   ├─ rd.docx
   ├─ bd.md
   └─ bd.docx
```

## #️⃣ そのほかのコマンド

### *️⃣ Explore; 変更前の論点整理

要求、品質特性、運用・保守への影響が曖昧な場合に、Proposeの前で使う。

```text
# Changeの論点と適用範囲を整理する。
$openspec-explore <検討内容>
```

### *️⃣ Update; 計画Artifactの改訂

Active Changeの要求や設計を改訂する。Update後は`rd`と`bd`も再生成する。

```text
# Active Changeの計画Artifactを整合させる。
/opsx:update <change-name> <変更内容>

# 更新した要求から要件定義書を再生成する。
$gen-pd <change-name>

# 更新した要求と設計から基本設計書を再生成する。
$gen-bd <change-name>
```

### *️⃣ Sync; Delta Specの先行反映

Archive前にDelta SpecだけをMain Specへ反映する必要がある場合に使う。`rd`と`bd`はChangeに残り、Main SpecへはSyncされない。

```text
# Delta SpecをMain Specへ反映し、ChangeはActiveのまま残す。
$openspec-sync-specs <change-name>
```

## ♻️ 文書のみを再生成

```text
# ProposalとDelta Specから要件定義書を再生成する。
$gen-pd <change-name>

# Proposal、Delta Spec、存在するDesignから基本設計書を再生成する。
$gen-bd <change-name>
```

再生成後はMarkdownの差分とDOCXの生成結果を確認する。

## References

- [OpenSpec Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
- [OpenSpec Customization](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md)
