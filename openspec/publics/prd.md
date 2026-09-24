---
title: "📋 要件定義書"
---

<!-- markdownlint-disable MD013 MD025 -->

# 1. 文書概要

| 項目 | 内容 |
| --- | --- |
| 対象Change | `archive/2026-09-18-align-mysdd-structure-and-adr` |
| Schema | `mysdd` |
| Change状態 | Archive済み |
| 文書目的 | MySDDの構成、文書生成、Git運用およびSetupに関する要求を定義する |
| 正本 | 本Markdown |
| 配布形式 | `openspec/publics/prd.docx` |

入力Artifactは次のとおりである。

- [proposal.md](../changes/archive/2026-09-18-align-mysdd-structure-and-adr/proposal.md)
- [design.md](../changes/archive/2026-09-18-align-mysdd-structure-and-adr/design.md)
- `openspec/changes/archive/2026-09-18-align-mysdd-structure-and-adr/specs/**/spec.md`

本書は入力Artifactに記載された事実を整理したものであり、入力にない製品機能、
組織、担当者または外部Serviceを要求として追加しない。

# 2. 背景・目的

`docs/references/MySDD-Spec.md`の想定Directory構成と、従来のSkill名、文書名、
出力先およびOpenSpec資産に不一致があった。また、独立したADR文書に記録されていた
10件の判断を、検証可能なOpenSpec Requirementとして保持する必要があった。

本変更の目的は次のとおりである。

- MySDDを`spec-driven`互換の4 Artifact構成として維持する。
- ISO/IEC/IEEE 12207とISO/IEC 25010の観点をPlanningへ組み込む。
- 要件定義書と基本設計書を独立したAgent Skillから生成する。
- Markdownを正本、DOCXを再生成可能な配布物として扱う。
- OpenSpecの各Phaseを独立した安全なGit Commitとして記録する。
- Windows Setup、Skill配置、追跡対象およびMCP非導入方針を一意にする。

# 3. 対象システムとスコープ

## 3.1 対象システム

対象は、このRepositoryで運用するMySDDおよび関連するOpenSpec／Agent Skill群である。

| 区分 | 対象 |
| --- | --- |
| OpenSpec | `mysdd` Schema、Template、Main Spec、Change Artifact |
| 文書生成 | `generate-prd`、`generate-hld`、`markdown2docx` |
| Git運用 | `CONTRIBUTING.md`、`openspec/config.yaml` |
| Setup | `docs/manual/SETUP.md`と`.agents/skills/.gitignore` |
| 成果物 | `openspec/publics/prd.md`、`hld.md`および同名DOCX |

## 3.2 対象範囲

- Skill名と出力Pathの統一
- `openspec/publics/`への文書境界の集約
- MySDD SchemaのArtifact GraphとISO観点
- PRD／HLD生成時の事実保持とTraceability
- Pandocによる同名DOCX変換
- propose、apply、verify、archiveのCommit分離
- 非昇格PowerShellとUser ScopeによるWindows Setup
- Repository固有SkillだけをGit管理するIgnore規則
- ADR-001～ADR-010のRequirementへの取り込み

## 3.3 対象外

- PRD、HLDまたはDOCX変換をMySDD Artifact Graphへ追加すること
- `spec-driven`のDelta Spec文法やArtifact依存関係の変更
- UIまたはRuntime Applicationの追加
- MCP Server／Clientの標準Setupへの導入
- 調達、供給者契約または外部納品契約
- Archive済みの歴史的Changeを一般的に書き換えること
- Runtime性能経路、安全関連機能または認証機能の追加

# 4. ステークホルダ

| ステークホルダ | 関心事項 |
| --- | --- |
| Maintainer | 一貫した構成、検証可能なRequirement、安全なCommit |
| AI Agent | 一意なSkill名、入力契約、出力先、停止条件 |
| Contributor | 管理者権限を要求しない再現可能なSetup |
| 文書利用者 | Traceabilityを保持したPRD／HLDのMarkdownとDOCX |
| Reviewer | ISO品質目標、ADR対応、検証Evidenceの確認 |

具体的な個人名、承認者および運用責任者は入力Artifactに定義されていないため`TBD`とする。

# 5. 前提条件・制約

- MySDDは`proposal`、`specs`、`design`、`tasks`の4 Artifactを維持する。
- `apply.requires`は`[tasks]`とする。
- PRD／HLD生成はOpenSpec Planning完了後に明示的に実行する。
- MarkdownをGit管理される正本とし、生成DOCXはGit管理対象外とする。
- 文書生成時はChange Artifactにない事実を補完しない。
- 不足情報は`TBD`として可視化する。
- Project固有Skillは`.agents/skills/`だけに配置する。
- Repositoryが追跡するSkillは3件と`.gitignore`に限定する。
- 標準SetupはMCP CredentialまたはEndpointを要求しない。
- Propose、ApplyまたはArchiveが失敗した場合、そのPhaseのCommitを作成しない。
- Verify完了時は成功または失敗をCheckpoint Commitへ記録する。
- 具体的なCI Provider、Workflow Fileおよび実行環境は入力Artifactにないため`TBD`とする。

# 6. 業務・システム・機能要求

## 6.1 `project-setup`

| Requirement | 要求概要 |
| --- | --- |
| `Setup uses ordinary user permissions` | 非昇格PowerShellを使用し、対応Packageを`--scope user`で導入する |
| `Setup documentation separates required and optional tools` | `docs/manual/SETUP.md`を正本とし、必須手順と任意手順を分離する |
| `Project Agent Skills use one canonical location` | Project固有Skillを`.agents/skills/`だけに配置する |
| `Only repository-owned skills are tracked` | 自作3 Skillと`.gitignore`だけを追跡する |
| `Standard setup excludes MCP` | 標準SetupでMCPを導入・設定しない |

保持対象Scenario：

- `Install a user-scoped package`
- `Choose the minimum setup`
- `Choose optional tools`
- `Add or migrate a project skill`
- `A third-party skill exists locally`
- `A repository-owned skill changes`
- `Complete the canonical setup`

## 6.2 `mysdd-workflow`

| Requirement | 要求概要 |
| --- | --- |
| `Daily changes use the four-command workflow` | propose→apply→verify→archiveの順序を標準とする |
| `Markdown is the document source of truth` | Requirement、Design、Evidence、PRD、HLDの正本をMarkdownとする |
| `Verification gates archive` | OpenSpecと必須CIの検証成功をArchive条件とする |
| `Workflow operations have separate commit boundaries` | ConfigのTimingで各Phaseを独立Commitとし、Archive後はGateを満たして`main`へ統合する |

保持対象Scenario：

- `Complete a normal change`
- `Publish a distributable document`
- `Verification succeeds`
- `Verification fails`
- `A workflow operation succeeds`
- `Verification changes no tracked files`
- `Archive completes on a feature branch`
- `A workflow operation fails`

## 6.3 `mysdd-schema`

| Requirement | 要求概要 |
| --- | --- |
| `MySDD preserves the four standard artifacts` | `spec-driven`互換の4 Artifactと依存関係を維持する |
| `MySDD adds ISO viewpoints to planning artifacts` | ライフサイクル観点と製品品質観点をPlanningへ追加する |
| `Formal document generation remains outside the artifact graph` | PRD、HLD、DOCXをSchema Artifactにしない |

保持対象Scenario：

- `Inspect a MySDD change`
- `Propose a MySDD change`
- `Complete the proposal workflow`

## 6.4 `generate-prd`

| Requirement | 要求概要 |
| --- | --- |
| `Generate the PRD from a named change` | Proposalと1件以上のDelta Specから`prd.md`を生成し、DOCX変換を委譲する |
| `Preserve source facts and traceability` | Capability、Requirement、Scenario、ID、品質目標および検証方法を保持する |
| `Preserve Markdown on conversion failure` | DOCX変換失敗時も完成済み`prd.md`を保持する |

保持対象Scenario：

- `Required artifacts exist`
- `Required artifacts are missing`
- `A required section lacks source information`
- `DOCX conversion fails`

## 6.5 `generate-hld`

| Requirement | 要求概要 |
| --- | --- |
| `Generate the HLD from a named change` | Proposal、Delta Spec、存在するDesignから`hld.md`を生成する |
| `Preserve source facts and traceability` | Requirement／Design ID、ADR、品質目標およびRisk関係を保持する |
| `Preserve Markdown on conversion failure` | DOCX変換失敗時も完成済み`hld.md`を保持する |

保持対象Scenario：

- `Required artifacts exist`
- `Design is absent`
- `A required section lacks source information`
- `DOCX conversion fails`

## 6.6 `markdown2docx`

| Requirement | 要求概要 |
| --- | --- |
| `正本Markdownを同名DOCXへ変換する` | `openspec/publics/`のMarkdownをReference DOCX付きで同名DOCXへ変換する |
| `変換先を安全に制限する` | Literal Pathを使用し、同一Directory・同一Base Name以外への出力を拒否する |
| `変換失敗時に正本を保持する` | 失敗時にSource MarkdownをByte単位で保持し、失敗理由を報告する |

保持対象Scenario：

- `要件定義書を変換する`
- `基本設計書を変換する`
- `出力先が入力と対応しない`
- `必須入力が存在しない`
- `Rendererが失敗する`
- `変換が成功する`

# 7. ISO/IEC 25010品質要求

| 品質ID | 品質特性 | 測定量 | 目標値 | 条件 | 検証方法 |
| --- | --- | --- | --- | --- | --- |
| QR-001 | Functional suitability | ADR対応率、Source ID保持率、検証済みArchive率 | 対象ごとに100% | ADR移管、PRD／HLD生成、Archive | 対応表、生成文書比較、Verification結果 |
| QR-002 | Compatibility | Schema検証成功率、昇格が必要な必須Command数 | 100%、0件 | Schema更新、Clean Windows User環境 | Verbose Schema Validation、Template確認、Setup Review |
| QR-003 | Maintainability | 追跡DOCX数、DOCXのみの変更数、旧Live Path残存数 | すべて0件 | 文書生成、Review、Migration | `git status`、Source／Output比較、Repository検索 |
| QR-004 | Reliability | 変換失敗後のMarkdown保持率 | 100% | Rendererが非Zero終了 | Hash比較とNegative Test |
| QR-005 | Reliability | 変換失敗理由の報告率 | 100% | Rendererが非Zero終了 | Negative Test |
| QR-006 | Security and integrity | Phase Commitへの無関係Path混入数、不許可Pathへの書込数 | 0件 | Clean／Dirty／Conflict状態、無効出力要求 | Staged Diff Review、Path Review、Negative Test |
| QR-008 | Functional completeness | DOCXの存在、非Zero Size、代表ID一致率 | PRD／HLDとも100% | 必須入力がすべて存在 | Conversion Test |

QR-007の定義は入力Artifactに存在しないため`TBD`とする。新しいIDは本書で補完しない。

次のISO/IEC 25010観点はProposalで非適用とされている。

- Performance efficiency：Runtime性能経路を追加しないため非適用
- Interaction capability：UI変更がないため非適用
- Flexibility：共有変換Contractで扱われ、独立した測定目標を要求しない
- Safety：安全関連System Behaviorを扱わないため非適用
- Security：Identity／Authorization／Secret処理は追加しない。ただしPathとCommitの
  IntegrityはQR-006で扱う

# 8. 外部インタフェース・データ要求

| Interface／Data | Input | Output／制約 |
| --- | --- | --- |
| OpenSpec Change | `proposal.md`、`specs/**/spec.md`、任意の`design.md` | PRD／HLD生成の唯一の事実Source |
| PRD Template | `.agents/skills/generate-prd/assets/prd.md` | `openspec/publics/prd.md` |
| HLD Template | `.agents/skills/generate-hld/assets/hld.md` | `openspec/publics/hld.md` |
| DOCX Template | `.agents/skills/markdown2docx/references/template.docx` | PRD／HLD共通の書式Source |
| Pandoc変換 | `openspec/publics/*.md` | 同一Directoryの同名`.docx`のみ許可 |
| Git | `CONTRIBUTING.md`、Config Timing、Staged Diff | Phase固有CommitとGate済みArchive後Merge |
| WinGet | Package ID | 対応Packageでは`--scope user`を使用 |

Database、Network API、認証ProviderおよびMCP Endpointは入力Artifactに定義されていない。

# 9. 移行・運用・保守・廃止要求

## 9.1 移行

- 旧`gen-pd`、`gen-bd`、`md2docx`を、それぞれ`generate-prd`、`generate-hld`、
  `markdown2docx`へ移行する。
- 参照DOCXと生成物を`openspec/publics/`へ集約する。
- ADR-001～ADR-010を検証可能なCapability Requirementへ移管する。
- 旧Live Changeと不要Directoryは、代替Contractの確認後に廃止する。

## 9.2 運用

- 日常Workflowはpropose→apply→verify→archiveとする。
- 各Phaseは`openspec/config.yaml`のTimingで独立Commitとして記録する。
- PRD／HLDはPlanning完了後に必要に応じて個別生成する。
- Archive前にOpenSpec Verificationと設定済みCIを成功させる。
- Archive Commit後はPull RequestとCI条件を満たして`feature/*`を`main`へMergeする。
- DOCXは配布の都度、正本Markdownから再生成する。

## 9.3 保守

- `spec-driven`更新時も4 Artifact Graphを維持する。
- Skill名、Path、Template、Specおよび文書参照の整合を検査する。
- Third-party SkillはRepositoryで追跡せず、Local環境から削除もしない。

## 9.4 廃止・Rollback

- 旧Skill Aliasは競合する正本を作るため保持しない。
- Archiveは歴史的Evidenceとして保持する。
- MigrationのRollbackは該当Operation CommitのRevertで行う。
- Source Markdownは変換失敗時にも削除または変更しない。

# 10. 受入条件と検証方法

| 受入条件 | 合格基準 | 検証方法 |
| --- | --- | --- |
| Schema互換性 | 4 Artifact、依存関係、Apply条件が維持される | MySDD Schema Verbose Validation |
| Delta Spec妥当性 | 対象CapabilityがStrict Validationを通過する | OpenSpec Strict Validation |
| ADR移管 | ADR-001～ADR-010の10/10がRequirementへ対応する | Traceability表Review |
| PRD生成 | Source見出し、Scenario、IDを保持した非空Markdownが生成される | 生成文書比較 |
| HLD生成 | SourceとDesignのID、ADR、Risk関係を保持する | 生成文書比較 |
| DOCX生成 | PRD／HLDの同名DOCXが存在し、非Zero Sizeで代表IDを含む | Conversion Test |
| 変換失敗 | Markdown Hashが不変で、失敗理由が報告される | Negative TestとHash比較 |
| Safe Path | 不許可Directory／Base Nameへ書き込まない | Negative Test |
| Skill追跡 | 自作3 Skill以外をGit追跡しない | `git status`とIgnore規則確認 |
| Phase分離 | 無関係な既存変更をCommitへ含めない | Baseline比較とStaged Diff Review |
| Verify Gate | 検証失敗時にArchiveしない | Verify失敗Scenario確認 |
| Setup | 必須手順が非昇格PowerShellで完了する | Command ReviewとSetup Dry Run |

CIの具体的なJob名、Test Fixtureおよび自動化Script Pathは入力Artifactにないため`TBD`とする。

# 11. 要求トレーサビリティ

| ADR | Capability／Requirement | 主な品質ID |
| --- | --- | --- |
| ADR-001 | `project-setup`／`Setup uses ordinary user permissions` | QR-002 |
| ADR-002 | `project-setup`／`Setup documentation separates required and optional tools` | QR-003 |
| ADR-003 | `project-setup`／`Project Agent Skills use one canonical location` | QR-003 |
| ADR-004 | `project-setup`／`Standard setup excludes MCP` | QR-006 |
| ADR-005 | `mysdd-workflow`／`Daily changes use the four-command workflow` | QR-001 |
| ADR-006 | `mysdd-workflow`／`Markdown is the document source of truth`、`markdown2docx`／`正本Markdownを同名DOCXへ変換する` | QR-003、QR-008 |
| ADR-007 | `mysdd-schema`／`MySDD preserves the four standard artifacts`、`MySDD adds ISO viewpoints to planning artifacts` | QR-002 |
| ADR-008 | `generate-prd`・`generate-hld`／`Preserve source facts and traceability` | QR-001 |
| ADR-009 | `mysdd-workflow`／`Verification gates archive` | QR-001 |
| ADR-010 | `generate-prd`、`generate-hld`、`markdown2docx`の生成・失敗時保持Requirement | QR-004、QR-005、QR-008 |

すべての機能要求は、対応するCapability Path、Requirement見出しおよびScenario名を
第6章に保持している。検証時はArchive済みDelta SpecをSourceとして比較する。

# 12. 用語集

| 用語 | 定義 |
| --- | --- |
| MySDD | `spec-driven`をForkし、ISOライフサイクル・製品品質観点を追加したSchema |
| Artifact Graph | Proposal、Specs、Design、Tasksの依存関係 |
| Delta Spec | Changeに含まれる追加・変更・削除・改名Requirement |
| Main Spec | `openspec/specs/`に同期された正式なCapability仕様 |
| PRD | Product Requirements Document。本書に相当する要件定義書 |
| HLD | High-Level Design。基本設計書 |
| 正本Markdown | Git管理され、文書内容のSource of TruthとなるMarkdown |
| Template DOCX | Pandocが書式参照に使用する`.agents/skills/markdown2docx/references/template.docx` |
| Phase | propose、apply、verify、archiveのいずれか1工程 |
| Evidence | Requirementまたは品質目標を満たしたことを示す検証結果 |
| TBD | 入力Artifactに必要情報がなく、確定できない項目 |
