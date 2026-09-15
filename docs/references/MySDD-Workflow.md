# 🚀 MySDD ワークフロー

MySDDは、OpenSpecの`spec-driven`をForkし、ISO/IEC/IEEE 12207とISO/IEC 25010の観点を計画Artifactへ組み込んだカスタムSchemaである。

## 🛝 使い方の流れ

```mermaid
flowchart LR
    P["`/opsx:propose`<br/>ISO観点を含む4 Artifact"]
    P --> RD["`$gen-pd`<br/>要件定義書"]
    P --> BD["`$gen-bd`<br/>基本設計書"]
    RD --> A["`/opsx:apply`<br/>実装とテスト"]
    BD --> A
    A --> V["`/opsx:verify`<br/>実装と成果物を検証"]
    V -->|合格| R["`/opsx:archive`<br/>Spec反映と履歴化"]
    V -->|不合格| A
```

OpenSpec Artifactは`proposal`、`specs`、`design`、`tasks`の4つである。
`rd`と`bd`はSchema Artifactではなく、Propose完了後に専用Agent Skillで作る正式文書とする。

## 1️⃣ `/opsx:propose`; 変更分の差分仕様を作成

```text
# MySDD Changeの4つの計画Artifactを生成する。
/opsx:propose <変更名または変更内容>
```

Proposeは次を行う。

- `spec-driven`互換の4 Artifactを生成する。
- ISO/IEC/IEEE 12207のステークホルダ、移行、運用、保守、廃止の観点を計画へ反映する。
- ISO/IEC 25010の適用品質特性、測定目標、検証方法を計画へ反映する。

```text
openspec/changes/<change-name>/
├─ .openspec.yaml
├─ proposal.md                    # 変更理由、範囲、ISO観点
├─ specs/
│  └─ <capability>/spec.md     # 振る舞いと測定可能な要求
├─ design.md                      # 品質とライフサイクルの実現方式
└─ tasks.md                       # 実装と検証Evidence
```

4 Artifactの内容とISO観点が揃えばPropose完了である。未確定の重要事項が残る場合は次へ進まない。

## 2️⃣ `$gen-pd` / `$gen-bd`; 正式文書を別途生成

```text
# ProposalとDelta Specから要件定義書を生成する。
$gen-pd <change-name>

# Proposal、Delta Spec、存在するDesignから基本設計書を生成する。
$gen-bd <change-name>
```

```text
openspec/changes/<change-name>/docs/
├─ rd.md                         # 要件定義書の正本
├─ rd.docx                       # 要件定義書の配布物
├─ bd.md                         # 基本設計書の正本
└─ bd.docx                       # 基本設計書の配布物
```

両Skillは入力Artifactにない事実を補完せず、未確定事項を`TBD`とする。Markdownが正本、DOCXはGit管理外の配布物である。必須Markdownが欠ける場合はApplyへ進まない。DOCXだけが失敗した場合はMarkdownを保持し、再生成する。

## 3️⃣ `/opsx:apply`; ドキュメントに従って実装

```text
# tasks.mdに従って実装し、完了項目を更新する。
/opsx:apply <change-name>
```

Schema上のApply開始条件は`tasks`である。MySDD運用では、`gen-pd`と`gen-bd`の完了を確認してからApplyを開始する。要求または設計が変わった場合は、Artifactと正式文書を先に更新する。

## 4️⃣ `/opsx:verify`; 実装を検証

```text
# 実装、4つのArtifact、正式文書、テスト証跡を照合する。
/opsx:verify <change-name>
```

次を確認する。

- RequirementとScenarioが実装・テストへ追跡できる。
- `rd.md`と`bd.md`が入力Artifactと整合する。
- ISOの適用観点に未達のTargetまたは証跡欠落がない。
- Schema Validation、Change Validation、Projectのテストが成功する。

CRITICALな不整合、参照切れ、失敗テストがある場合はArchiveへ進まず、ApplyとVerifyを再実行する。

## 5️⃣ `/opsx:archive`; Spec反映と変更の履歴化

```text
# 検証済みChangeをArchiveする。
/opsx:archive <change-name>
```

Delta SpecがMain Specへ反映され、正式文書を含むChange全体が`openspec/changes/archive/`へ移動する。Archiveが失敗した場合は手作業で移動せず、ValidationまたはSyncの原因を解消する。

## #️⃣ そのほかのコマンド

### *️⃣ `/opsx:explore`; 変更前の論点整理

```text
# Changeの論点と適用範囲を整理する。
/opsx:explore <検討内容>
```

### *️⃣ `/opsx:update`; 計画Artifactの改訂

```text
# Active Changeの計画Artifactを整合させる。
/opsx:update <change-name> <変更内容>

# 更新した計画から正式文書を再生成する。
$gen-pd <change-name>
$gen-bd <change-name>
```

### *️⃣ `/opsx:sync`; Delta Specの先行反映

```text
# Delta SpecをMain Specへ反映し、ChangeはActiveのまま残す。
/opsx:sync <change-name>
```

`rd`と`bd`はMain SpecへSyncされず、Change側に残る。

## 🔖 参考文献

- [OpenSpec Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
- [OpenSpec Customization](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md)
- [ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html)
- [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html)
