## Purpose

🔄 OpenSpecの標準`spec-driven`フローを維持しながら、要件定義書と基本設計書をChangeの正式Artifactとして生成できるようにする。

## ADDED Requirements

### Requirement: spec-drivenを文書Artifactで拡張する

`mysdd`は、`spec-driven`の`proposal`、`specs`、`design`、`tasks`を維持し、`rd`と`bd`を追加しなければならない（MUST）。

#### Scenario: Schemaから文書を生成する

- **WHEN** 利用者が`mysdd`でChangeのArtifactを生成する
- **THEN** `gen-pd`を使って`docs/rd.md`を生成する
- **THEN** `gen-bd`を使って`docs/bd.md`を生成する

### Requirement: Apply前に文書Artifactを完成させる

`mysdd`は、`tasks`、`rd`、`bd`が存在するまでApplyを開始可能にしてはならない（MUST NOT）。

#### Scenario: 文書Artifactが不足している

- **WHEN** `rd`または`bd`が存在しない
- **THEN** ApplyをBlockedとして扱う

#### Scenario: 必要なArtifactが揃っている

- **WHEN** `tasks`、`rd`、`bd`が存在する
- **THEN** Applyを開始可能にする
