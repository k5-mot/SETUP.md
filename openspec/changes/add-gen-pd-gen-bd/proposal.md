## Why

OpenSpecの要求・設計Artifactから、内容を推測で補わずに要件定義書と基本設計書を再生成できるようにする。📄 Markdownを正本とし、配布用DOCXを同じ入力から生成する。

## What Changes

- `gen-pd` Skillを追加し、OpenSpec Artifactから要件定義書のMarkdownとDOCXを生成する。
- `gen-bd` Skillを追加し、OpenSpec Artifactから基本設計書のMarkdownとDOCXを生成する。
- 元Artifactの識別子とトレーサビリティを維持し、不足情報は`TBD`として出力する。
- 生成MarkdownをGit管理し、再生成可能なDOCXをGit管理外とする。

## Capabilities

### New Capabilities

- `gen-pd`: 要求関連Artifactを要件定義書へ変換する。
- `gen-bd`: 要求・方式・設計Artifactを基本設計書へ変換する。

### Modified Capabilities

なし。

## Impact

- `.agents/skills/gen-pd/`
- `.agents/skills/gen-bd/`
- `openspec/artifacts/<change-name>/`
- DOCX変換用のPandoc設定と`.gitignore`
