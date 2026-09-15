# 🚀 OpenSpec ワークフロー

OpenSpecのデフォルトである [OPSX Workflow](https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md)を紹介する。

## 🛝 使い方の流れ

```mermaid
flowchart LR
    P["`/opsx:propose`<br/>変更分のドキュメントを作成"] --> A["`/opsx:apply`<br/>ドキュメントに従って実装"]
    A --> V["`/opsx:verify`<br/>実装を検証"]
    V -->|合格| R["`/opsx:archive`<br/>差分仕様を正本仕様へ反映し、変更をアーカイブ"]
    V -->|不合格| A
    R --> C["正本仕様<br/>openspec/specs/"]
    R --> H["変更履歴<br/>changes/archive/"]
```

## 📌 用語定義

- Spec: システムの動作を記述したドキュメント
- Artifact: 変更を示す4つのドキュメント成果物(proposal, specs, design, tasks)
- Change: `openspec/changes/<name>/`ディレクトリとしてパッケージングされたドキュメント群
- Delta Spec: Changeに含まれるSpecの一種であり、変更分の差分仕様を示す
- Main Spec: 既存のシステム仕様を示す正本仕様書
  - = Canonical Spec
  - = Source of truth: 唯一の情報源

## 1️⃣`/opsx:propose`; 変更分の差分仕様を作成

Delta Specを含む4つのArtifact(proposal, specs, design, tasks)を作成する。

```text
/opsx:propose <変更名または変更内容>
```

実行後、次のディレクトリ構造が作成される。

```bash
openspec/
├─ config.yaml
├─ specs/
│  └─ <capability>/spec.md              # 既存のCanonical Spec
└─ changes/
   └─ <change-name>/
      ├─ .openspec.yaml
      ├─ proposal.md                    # 変更理由(Why)と範囲(What)
      ├─ design.md                      # 技術的なアプローチ(How)
      ├─ tasks.md                       # 実装チェックリスト
      └─ specs/                         # Delta Spec
         └─ <capability>/spec.md
```

## 2️⃣ `/opsx:apply`; ドキュメントに従って実装

`tasks.md`に記載されたタスクを依存順に実装する。

```text
/opsx:apply <change-name>
```

## 3️⃣ `/opsx:verify`; 実装を検証

実装と4つのArtifact(proposal, specs, design, tasks)とが整合するか検証する。

```text
/opsx:verify <change-name>
```

## 4️⃣ `/opsx:archive`; 差分仕様を正本仕様へ反映し、変更をアーカイブ

Delta SpecをMain Specへ反映し、完了したChangeを変更履歴としてアーカイブする。

```text
/opsx:archive <change-name>
```

実行後、次のディレクトリ構造が作成される。

```bash
openspec/
├─ specs/
│  └─ <capability>/spec.md
└─ changes/
   └─ archive/
      └─ YYYY-MM-DD-<change-name>/
         ├─ .openspec.yaml
         ├─ proposal.md
         ├─ specs/
         │  └─ <capability>/spec.md
         ├─ design.md
         └─ tasks.md
```

> [!NOTE]
> Delta SpecをMain Specへ反映するコマンドは`/opsx:sync`である。
> `/opsx:archive`実行前に、`/opsx:sync`が実行されていない場合、同期が提案される。
>
> - [OpenSpec/docs/commands.md at main · Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md#opsxarchive)

## #️⃣ そのほかのコマンド

### *️⃣ `/opsx:explore`; アイデア検討

変更に着手する前に、アイデアをじっくり検討し、問題点を調査し、要件を明確にする。

```text
/opsx:explore <検討内容>
```

### *️⃣ `/opsx:update`;　変更計画の成果物を改訂

`/opsx:propose` → `/opsx:apply`まで完了し、変更内容自体を改定する場合に使用する。

```text
/opsx:update <change-name> <変更内容>

# update 後は最初から、ワークフローを開始する.
/opsx:propose <変更名または変更内容>
/opsx:apply <change-name>
```

### *️⃣ `/opsx:sync`;　差分仕様を正本仕様へ反映

Delta SpecをMain Specへ反映する。

```text
/opsx:sync <change-name>
```

## 🔖 参考文献

- [OpenSpec Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
- [OpenSpec Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)
- [OpenSpec OPSX](https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md)
- [Built-in spec-driven schema](https://github.com/Fission-AI/OpenSpec/blob/main/schemas/spec-driven/schema.yaml)
