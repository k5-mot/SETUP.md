## Why

OpenSpecの`spec-driven`フローから、内容を推測で補わずに要件定義書と基本設計書を再生成できるようにする。📄 Markdownを正本とし、配布用DOCXを同じ入力から生成する。

## What Changes

- `spec-driven`をForkした`mysdd` Schemaへ`rd`と`bd` Artifactを追加する。
- `gen-pd` Skillを使い、ProposalとDelta Specから`docs/rd.md`と配布用DOCXを生成する。
- `gen-bd` Skillを使い、Proposal、Delta Spec、任意のDesignから`docs/bd.md`と配布用DOCXを生成する。
- 元Artifactの識別子とトレーサビリティを維持し、不足情報は`TBD`として出力する。
- 生成MarkdownをGit管理し、再生成可能なDOCXをGit管理外とする。

## Capabilities

### New Capabilities

- `gen-pd`: 要求関連Artifactを要件定義書へ変換する。
- `gen-bd`: 要求・方式・設計Artifactを基本設計書へ変換する。
- `mysdd-schema`: `spec-driven`へ要件定義書と基本設計書のArtifactを追加する。

### Modified Capabilities

なし。

## Impact

- `.agents/skills/gen-pd/`
- `.agents/skills/gen-bd/`
- `openspec/schemas/mysdd/`
- `openspec/changes/<change-name>/docs/`
- DOCX変換用のPandoc設定と`.gitignore`
