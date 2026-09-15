## Purpose

🔄 OpenSpecの標準`spec-driven`フローを維持しながら、ISOライフサイクルと品質の観点を計画に組み込めるようにする。

## ADDED Requirements

### Requirement: 標準4 ArtifactにISO観点を組み込む

`mysdd`は、`spec-driven`の`proposal`、`specs`、`design`、`tasks`とその依存関係を維持し、
ISO/IEC/IEEE 12207とISO/IEC 25010の観点を各Artifactの指示とTemplateに反映しなければならない（MUST）。

#### Scenario: MySDDでChangeをProposeする

- **WHEN** 利用者が`mysdd`でChangeをProposeする
- **THEN** Schema Artifactとして`proposal`、`specs`、`design`、`tasks`の4つを生成する
- **THEN** 適用する12207のライフサイクル観点が計画に記録される
- **THEN** 適用する25010の品質特性、測定目標、検証方法が計画に記録される

### Requirement: 正式文書の生成をProposeから分離する

`mysdd`は`rd`と`bd`をSchema Artifactとして定義せず、要件定義書と基本設計書を専用Agent Skillから生成可能にしなければならない（MUST）。

#### Scenario: Propose後に要件定義書を生成する

- **WHEN** Proposeが4つの計画Artifactを完了する
- **AND** 利用者が`gen-pd`を実行する
- **THEN** `gen-pd`固有のTemplate Assetから`docs/rd.md`と同名DOCXを生成する

#### Scenario: Propose後に基本設計書を生成する

- **WHEN** Proposeが4つの計画Artifactを完了する
- **AND** 利用者が`gen-bd`を実行する
- **THEN** `gen-bd`固有のTemplate Assetから`docs/bd.md`と同名DOCXを生成する

### Requirement: Apply依存をspec-drivenと互換にする

`mysdd`は、Schema上のApply開始条件を`tasks`のみとしなければならない（MUST）。

#### Scenario: Tasksが完了している

- **WHEN** `tasks`が存在する
- **THEN** Schema上はApplyを開始可能にする
