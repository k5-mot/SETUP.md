# 🧭 Architecture Decision Records

## ADR-001: 通常権限とUser Scopeを使う

- Status: Accepted
- Decision: セットアップは通常権限PowerShellで実行し、WinGetは`--scope user`を使う。
- Consequence: Machine Scopeが必要なツールは個別対応とする。

## ADR-002: セットアップ手順を2段階に分ける

- Status: Accepted
- Decision: `SETUP.md`を最小構成、`SETUP.full.md`を追加ツール込みの構成とする。
- Consequence: 共通手順は`SETUP.md`を優先する。

## ADR-003: Agent Skillsを`.agents/skills/`へ配置する

- Status: Accepted
- Decision: OpenSpecと追加Skillはプロジェクトの`.agents/skills/`へ配置する。
- Consequence: `.github/`や`.roo/`にはSkillを複製しない。

## ADR-004: MCPを導入しない

- Status: Accepted
- Decision: セットアップ手順にMCPを含めない。
- Consequence: 必要になったプロジェクトで個別に判断する。

## ADR-005: OpenSpecの日常操作を4コマンドに限定する

- Status: Accepted
- Decision: `propose → apply → verify → archive`を標準フローとする。
- Consequence: その他のWorkflowコマンドはマニュアルで扱わない。

## ADR-006: OpenSpecのMarkdownを正本とする

- Status: Accepted
- Decision: 要求、設計、検証、正式文書のMarkdownをGit管理する。DOCXはMarkdownから生成する。
- Consequence: DOCXを直接編集せず、生成DOCXはGit管理外とする。

## ADR-007: ISO観点をProject-local Schemaへ組み込む

- Status: Accepted
- Decision: `iso-sdlc` SchemaとTemplateを`openspec/schemas/`で管理する。
- Consequence: 規格本文は転載せず、ライフサイクルと品質要求の観点だけを実装する。

## ADR-008: 文書生成を`gen-pd`と`gen-bd`へ分離する

- Status: Accepted
- Decision: 要件定義書は`gen-pd`、基本設計書は`gen-bd`で生成する。
- Consequence: 両Skillは入力Artifactにない事実を追加しない。

## ADR-009: Verify結果をCIでも判定する

- Status: Accepted
- Decision: OpenSpec Verifyに加え、トレーサビリティと証跡をCIで検証する。
- Consequence: 検証失敗時はArchiveせず、修正後に再検証する。

## ADR-010: 文書生成のInterfaceと変換順を固定する

- Status: Accepted
- Decision: `gen-pd`と`gen-bd`は`change-name`だけを受け取り、規定パスの入力からMarkdown、DOCXの順に生成する。DOCX変換は共通のPandoc処理を使う。
- Consequence: DOCX変換に失敗してもMarkdownを保持し、部分成功として報告する。
