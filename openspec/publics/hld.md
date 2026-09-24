<!-- markdownlint-disable MD013 -->

# 🏛️ 基本設計書

## 1. 文書概要と適用範囲

| 項目 | 内容 |
| --- | --- |
| 対象Change | `archive/2026-09-18-align-mysdd-structure-and-adr` |
| Schema | `mysdd` |
| Change状態 | Archive済み |
| 設計対象 | MySDD Schema、文書生成Skill、Git Workflow Skill、Setup構成 |
| 正本 | 本Markdown |
| 配布形式 | `openspec/publics/hld.docx` |

本書は、対象ChangeのProposal、7件のDelta SpecおよびDesignから、MySDDの
High-Level Designを整理する。入力にない実装Class、Function、外部Serviceまたは
運用組織は推測せず`TBD`とする。

適用範囲は次のとおりである。

- `spec-driven`互換のMySDD Artifact Graph
- `generate-prd`、`generate-hld`、`markdown2docx`
- `openspec-git-workflow`
- `.agents/skills/`の追跡境界
- `openspec/publics/`の文書境界
- Windows向けProject Setup
- ADR-001～ADR-010から移管した設計判断

## 2. 関連文書

- [Proposal](../changes/archive/2026-09-18-align-mysdd-structure-and-adr/proposal.md)
- [Design](../changes/archive/2026-09-18-align-mysdd-structure-and-adr/design.md)
- [Task List](../changes/archive/2026-09-18-align-mysdd-structure-and-adr/tasks.md)
- [MySDD仕様](../../docs/references/MySDD-Spec.md)
- [MySDD Workflow](../../docs/references/MySDD-Workflow.md)
- `openspec/changes/archive/2026-09-18-align-mysdd-structure-and-adr/specs/**/spec.md`
- `openspec/specs/**/spec.md`

## 3. システム全体構成

### 3.1 論理構成

| Layer | Component | 責務 |
| --- | --- | --- |
| Workflow | OpenSpec Phase Skills | propose、apply、verify、archiveを実行する |
| Commit境界 | `openspec-git-workflow` | 1 Phaseの結果だけを安全にCommitする |
| Planning | `mysdd` Schema | 4 ArtifactとISO観点を提供する |
| Specification | Delta Specs／Main Specs | 観測可能なBehaviorとScenarioを保持する |
| 文書生成 | `generate-prd`／`generate-hld` | Change Artifactから正本Markdownを生成する |
| 文書変換 | `markdown2docx` | 正本Markdownを同名DOCXへ変換する |
| 公開境界 | `openspec/publics/` | 正本Markdown、Reference DOCX、配布DOCXを配置する |
| Setup | `docs/manual/SETUP.md` | 必須手順と任意Toolを分離して案内する |

### 3.2 処理Flow

1. MaintainerまたはAI AgentがMySDD Changeをproposeする。
2. `proposal`、`specs`、`design`、`tasks`を完成させる。
3. applyでTaskを実装し、verifyでOpenSpecと必須CIを確認する。
4. 必要に応じて`generate-prd`または`generate-hld`を明示的に実行する。
5. 文書生成SkillがMarkdownを`openspec/publics/`へ書き出す。
6. `markdown2docx`がReference DOCXを適用して同名DOCXを生成する。
7. verify成功後にChangeをarchiveし、Delta SpecをMain Specへ同期する。
8. `openspec-git-workflow`を使用する場合、各Phaseを独立Commitとして記録する。

PRD／HLD／DOCXはMySDD Artifact Graphに含めない。Planning完了と文書生成の成否を
分離し、OpenSpecの標準4 Artifactとの互換性を保つ。

## 4. アプリケーション・ソフトウェア構成

### 4.1 MySDD Schema

| Artifact | Output | Dependency | 主な設計責務 |
| --- | --- | --- | --- |
| `proposal` | `proposal.md` | なし | 変更理由、Capability、Lifecycle影響、品質観点 |
| `specs` | `specs/**/*.md` | `proposal` | Requirement、Scenario、品質目標と検証方法 |
| `design` | `design.md` | `proposal` | 設計判断、Trade-off、Lifecycle、Risk |
| `tasks` | `tasks.md` | `specs`、`design` | 実装、統合、検証およびEvidence Task |

`apply.requires`は`[tasks]`、進捗追跡対象は`tasks.md`とする。

### 4.2 文書生成Skill

#### `generate-prd`

- Input：Change名、`proposal.md`、1件以上のDelta Spec
- Template：`.agents/skills/generate-prd/assets/prd.md`
- Output：`openspec/publics/prd.md`
- 後続処理：`markdown2docx`へ`prd.docx`生成を委譲
- 停止条件：Proposal欠落またはDelta Specが0件
- 不足情報：`TBD`として明示

#### `generate-hld`

- Input：Change名、`proposal.md`、1件以上のDelta Spec、存在する`design.md`
- Template：`.agents/skills/generate-hld/assets/hld.md`
- Output：`openspec/publics/hld.md`
- 後続処理：`markdown2docx`へ`hld.docx`生成を委譲
- Design欠落時：ProposalとDelta Specから生成し、設計固有の不足情報を`TBD`とする

#### `markdown2docx`

- Input：`openspec/publics/`直下のMarkdown
- Template：`openspec/publics/template.docx`
- Output：Inputと同一Directory、同一Base NameのDOCX
- Path処理：Repository RootからLiteral Pathとして解決
- 成功条件：Process成功、DOCX存在、非Zero Size、Source Hash不変
- 失敗条件：Input／Reference欠落、不許可Path、Process非Zero、空DOCX、Source変更

### 4.3 Git Workflow Skill

`openspec-git-workflow`はPhaseとChange名を各1件受け取り、対応するインストール済み
OpenSpec Workflowへ委譲する。独自にOpenSpec Behaviorを再実装しない。

Phase実行前にBranch、HEAD、未追跡Fileを含むStatusとConflict状態をBaselineとして
記録する。成功後はBaselineとの差分からPhase所有PathだけをStageする。既存変更と
重複するPath、帰属不明の差分またはConflictがある場合はCommitを中止する。

### 4.4 Skill追跡境界

`.agents/skills/.gitignore`はIgnore-Allと明示的な例外を使用し、次だけを追跡する。

- `generate-prd`
- `generate-hld`
- `markdown2docx`
- `openspec-git-workflow`
- `.agents/skills/.gitignore`

Third-party SkillはLocal環境へ残し、Git Indexへ追加しない。

## 5. インフラ・ネットワーク方式

### 5.1 実行環境

- Setup手順の対象PlatformはWindows 11である。
- Setupは非昇格PowerShellで実行する。
- 対応PackageはWinGetの`--scope user`で導入する。
- Git Repository内のOpenSpec Rootを処理単位とする。
- CI検証PlatformはGitHub Actionsの`ubuntu-latest`である。
- Windows SetupはReview済み手順書とし、CIでは実行しない。

CIのCPU、MemoryおよびDisk容量はGitHub-hosted Runnerの提供条件に従い、固定値を
Project要件として定義しない。

### 5.2 Network

MySDD Schema、文書生成およびDOCX変換にRuntime Network Interfaceは定義されていない。
標準SetupはMCP Server／Client、CredentialまたはEndpointを導入しない。

Package取得時のNetwork要件、Proxy、MirrorおよびOffline Setup方式は`TBD`とする。

## 6. データ・外部インタフェース方式

### 6.1 File Interface

| Path | 種別 | Read／Write | 制約 |
| --- | --- | --- | --- |
| `openspec/config.yaml` | Config | Read | `schema: mysdd`を選択する |
| `openspec/schemas/mysdd/schema.yaml` | Schema | Read | 4 Artifact Graphを維持する |
| `openspec/changes/<change>/proposal.md` | Artifact | Read | PRD／HLD必須Input |
| `openspec/changes/<change>/specs/**/spec.md` | Artifact | Read | 1件以上を必須とする |
| `openspec/changes/<change>/design.md` | Artifact | Read | HLDでは存在時に使用する |
| `openspec/publics/prd.md` | 正本 | Write | PRD Output |
| `openspec/publics/hld.md` | 正本 | Write | HLD Output |
| `openspec/publics/template.docx` | Template | Read | DOCX共通書式 |
| `openspec/publics/prd.docx` | 配布物 | Write | Git管理対象外 |
| `openspec/publics/hld.docx` | 配布物 | Write | Git管理対象外 |

Archive済みChangeを入力とする場合は、Change名に`archive/<archive-name>`を指定し、
同じ`openspec/changes/<change-name>/`契約でArtifactを解決する。

### 6.2 Data Integrity

- Source Markdownの変換前SHA-256 Hashを記録する。
- 変換後もHashが同一であることを確認する。
- DOCXは非Zero Sizeと代表Requirement／Design IDの包含を確認する。
- Requirement見出し、Scenario名、Capability Pathおよび既存IDを改名しない。
- Inputにない事実を確定情報として出力しない。

Database Schema、Message FormatおよびNetwork APIは対象外である。

## 7. 認証・認可・セキュリティ方式

Identity、AuthenticationおよびAuthorizationの新規機能は設計対象外である。
本変更のSecurity／IntegrityはFile PathとGit変更境界で扱う。

| Control | Design |
| --- | --- |
| Path制限 | Input、Reference、OutputをLiteral Pathとして解決する |
| Output制限 | `openspec/publics/`の同一Base Name DOCXだけを許可する |
| 不許可書込 | 別Directoryまたは別Base Name要求を変換前に拒否する |
| Source保護 | DOCX失敗時もMarkdownを変更・削除しない |
| Commit分離 | Phase実行前Baselineと実行後Statusを比較する |
| Conflict保護 | 未解決ConflictがあればStage／Commitしない |
| Remote保護 | Wrapper SkillはPushしない |
| 履歴保護 | Amend、Reset、履歴書換えを行わない |
| Secret | MCP CredentialやEndpointを標準Setupへ追加しない |

Secret Scanner、Credential Storeおよび署名方式は入力Artifactに定義されていないため
`TBD`とする。

## 8. 性能・容量・可用性・復旧方式

### 8.1 性能・容量

ProposalではRuntime Performance Pathを追加しないため、Performance efficiencyは
非適用とされている。変換時間、最大Markdown Size、最大画像数および同時変換数は
入力Artifactに定義されていないため`TBD`とする。

性能・容量は、どの大きさの文書を、何秒以内に、何件同時に処理できれば利用者が
困らないかを定める品質目標である。代表文書のSize分布、許容待ち時間および同時実行の
必要性が未定のため、現時点で数値を置くと根拠のない制限になる。CIでは変換時間を記録
するだけとし、合否Thresholdは設けない。実運用の代表文書と許容時間が決まった時点で、
基準値、上限値および測定条件を同じChangeで定義する。

### 8.2 可用性・復旧

- Markdownを正本とし、DOCXを再生成可能にする。
- DOCX変換に失敗しても完成済みMarkdownを保持する。
- Archive済みChangeとMain SpecをGitで保持する。
- Migration失敗時はOperation CommitのRevertで旧構成を復元する。
- `template.docx`は再生成不能な共通資産としてGit管理する。

Recovery Time Objective、Recovery Point Objective、Backup媒体およびRetention期間は
入力Artifactに定義されていないため`TBD`とする。

## 9. ログ・監視・運用・保守方式

### 9.1 観測対象

| 対象 | Evidence |
| --- | --- |
| Schema | Verbose Schema Validation結果 |
| Change | Strict Validation結果、Artifact／Task完了状態 |
| Main Specs | `openspec validate --specs`結果 |
| DOCX変換 | Process Exit、Output存在、Size、代表ID、Source Hash |
| Git Phase | Baseline、Porcelain Status、Staged Diff、Commit ID |
| Migration | 旧Live Name／Path検索、ADR対応表 |

### 9.2 Error Handling

- Artifact不足時は不足Pathを報告して文書生成成功としない。
- Reference DOCX不足時は変換を開始しない。
- Renderer失敗または空DOCXでは利用可能なDOCXとして報告しない。
- Phase失敗時はCommitを作成せず、失敗理由を報告する。
- Existing WorktreeとPhase Outputが重複する場合はStageせず停止する。

CI LogはGitHub Actionsの標準Job Logへ出力し、保持期間はRepository設定に従う。
専用Dashboard、外部Alert通知先およびOn-call手順は導入しない。

### 9.3 保守

- `spec-driven`更新時に4 Artifact GraphとTemplate見出しを比較する。
- Skill名、Asset名、Output PathおよびMain Specの整合を確認する。
- Generated DOCXをGitへ追加しない。
- Third-party SkillをRepository更新のために削除しない。

## 10. 移行・デプロイ・リリース・構成管理方式

### 10.1 移行順序

1. `MySDD-Spec.md`のAuthorityを確認する。
2. `openspec/publics/`を文書境界として作成する。
3. 旧文書Skillを`generate-prd`、`generate-hld`、`markdown2docx`へ移行する。
4. `openspec-git-workflow`とSkill用`.gitignore`を追加する。
5. Schema、Template、Config、LinkおよびTestを新Contractへ合わせる。
6. 7件のDelta Spec、Schema、Skill、変換および旧Path残存を検証する。
7. ADR-001～ADR-010の移管後に独立ADR文書と旧Live Changeを廃止する。
8. 不要Directoryを削除し、ChangeをArchiveする。

### 10.2 構成管理

- Configは`openspec/config.yaml`の`schema: mysdd`でSchemaを選択する。
- Schema、Template、Main Spec、Skill、Markdown正本をGit管理する。
- DOCX配布物は`.gitignore`で除外する。
- Phaseごとにgitmoji付き日本語Conventional Commitを作成する。
- Verifyで追跡対象変更がない場合はEmpty CommitをCheckpointとする。

### 10.3 Rollback

移行を所有するOperation CommitをRevertし、旧Path、旧Skill名、独立ADRおよび旧Changeを
復元する。Wrapper Skillは自動でReset、AmendまたはHistory Rewriteを行わない。

Release TagはSemantic Versioningの`v<MAJOR>.<MINOR>.<PATCH>`形式とする。対象の
`main` Commitで`quality` Jobが成功した後、Maintainerが手動でTagを作成する。
自動Deployment Pipelineは導入せず、`quality`成功とMaintainer判断を承認Gateとする。

## 11. ISO/IEC 25010品質特性への対応

| 品質ID | 特性 | Design対応 | Evidence |
| --- | --- | --- | --- |
| QR-001 | Functional suitability | ID／Requirement／Scenarioを生成文書へ保持し、VerifyをArchive Gateにする | 10/10 ADR対応、生成文書比較、Verification結果 |
| QR-002 | Compatibility | 4 Artifact Graph維持、非昇格User Scope Setup | Schema Validation、Template確認、Setup Dry Run |
| QR-003 | Maintainability | Markdown正本、DOCX非追跡、4 Skillだけを追跡 | `git status`、Source／Output比較、旧Path検索 |
| QR-004 | Reliability | 変換失敗時もSource Markdownを保持 | 変換前後SHA-256 Hash比較 |
| QR-005 | Reliability | 失敗理由をCallerへ返す | Negative Test結果 |
| QR-006 | Security and integrity | Literal Path、Output制限、Phase差分分離 | Path Negative Test、Staged Diff Review |
| QR-008 | Functional completeness | 非空DOCXと代表ID包含を要求 | PRD／HLD Conversion Test |

Quality IDはTraceability用の識別子であり、連番の欠番自体は機能欠落を意味しない。
QR-007に対応する品質要求はSource Artifactに存在しないため、既存要求から内容を推測して
追加しない。将来、独立した品質要求が必要になったChangeで、QR-007を使用するか予約欠番
として維持するかを決定する。

非適用または独立目標を設けない観点：

- Performance efficiency：Runtime性能経路を追加しない。
- Interaction capability：UI変更がない。
- Flexibility：共有変換Contractの再利用で扱う。
- Safety：安全関連Behaviorがない。
- SecurityのIdentity領域：認証・認可・Secret処理を追加しない。

## 12. ADR

| ADR | Design判断 | 実装先 |
| --- | --- | --- |
| ADR-001 | Setupを非昇格PowerShellとUser Scopeで実行する | `project-setup` |
| ADR-002 | 単一`SETUP.md`内で必須手順と任意Toolを分離する | `project-setup` |
| ADR-003 | Project Skillの正本を`.agents/skills/`へ集約する | `project-setup` |
| ADR-004 | 標準SetupからMCPを除外する | `project-setup` |
| ADR-005 | propose→apply→verify→archiveを標準Workflowとする | `mysdd-workflow` |
| ADR-006 | Markdownを正本、DOCXを再生成可能な配布物とする | `mysdd-workflow`、`markdown2docx` |
| ADR-007 | 4 Artifactを維持し、ISO観点をInstructionへ追加する | `mysdd-schema` |
| ADR-008 | PRD／HLD生成でSource事実を保持し、推測しない | `generate-prd`、`generate-hld` |
| ADR-009 | Verification成功をArchive条件にする | `mysdd-workflow` |
| ADR-010 | 文書生成と同名DOCX変換のInterface／失敗時動作を固定する | 文書生成3 Skill |

### 12.1 主要Trade-off

- Compatibility Aliasを残さないため旧Callerは更新が必要だが、Skill名の正本を一意にできる。
- DOCXを追跡しないため配布時に再生成が必要だが、DOCXだけの変更を防止できる。
- Wrapper Skillは既存変更との重複時にCommitを拒否するため自動化が停止し得るが、
  User変更の混入を防止できる。
- Archive内容を歴史的Evidenceとして保持するため旧名称がArchive内に残り得るが、
  Live Contractとの混同を避けるため検索時にArchiveを区別する。

## 13. 要求・設計・検証トレーサビリティ

| Capability／Requirement | Design判断 | 検証Evidence |
| --- | --- | --- |
| `project-setup`／`Setup uses ordinary user permissions` | 非昇格PowerShell、`--scope user` | Command Review、Setup Dry Run |
| `project-setup`／`Setup documentation separates required and optional tools` | 単一正本内のSection分離 | 文書Review |
| `project-setup`／`Project Agent Skills use one canonical location` | `.agents/skills/`へ集約 | Repository検索 |
| `project-setup`／`Only repository-owned skills are tracked` | Ignore-All＋4 Skill例外 | `git status`、Ignore確認 |
| `project-setup`／`Standard setup excludes MCP` | MCP設定を標準手順に含めない | Setup文書検索 |
| `mysdd-workflow`／`Daily changes use the four-command workflow` | 4 Phase直列Flow | Workflow文書Review |
| `mysdd-workflow`／`Markdown is the document source of truth` | DOCXを派生物として除外 | Git Status、Source比較 |
| `mysdd-workflow`／`Verification gates archive` | Verify成功をGate化 | Verification Report、CI結果 |
| `mysdd-workflow`／`Workflow operations have separate commit boundaries` | Phase単位Commit | Git Log、Empty Verify Commit |
| `mysdd-schema`／`MySDD preserves the four standard artifacts` | Fork元Graphを維持 | Verbose Schema Validation |
| `mysdd-schema`／`MySDD adds ISO viewpoints to planning artifacts` | Instruction／TemplateへISO観点追加 | Resolved Template確認 |
| `mysdd-schema`／`Formal document generation remains outside the artifact graph` | 文書生成を独立Skill化 | Planning完了状態確認 |
| `generate-prd`／`Generate the PRD from a named change` | Proposal＋Delta Spec＋PRD Template | `prd.md`／`prd.docx`生成確認 |
| `generate-prd`／`Preserve source facts and traceability` | Source ID保持、欠落は`TBD` | 生成文書比較 |
| `generate-prd`／`Preserve Markdown on conversion failure` | Markdown完成後に変換委譲 | Failure Test、Hash比較 |
| `generate-hld`／`Generate the HLD from a named change` | Proposal＋Delta Spec＋任意Design | `hld.md`／`hld.docx`生成確認 |
| `generate-hld`／`Preserve source facts and traceability` | Requirement／Design／ADR／Riskを保持 | 生成文書比較 |
| `generate-hld`／`Preserve Markdown on conversion failure` | Markdown完成後に変換委譲 | Failure Test、Hash比較 |
| `markdown2docx`／`正本Markdownを同名DOCXへ変換する` | 共通Reference DOCXを使用 | 非空DOCX、代表ID確認 |
| `markdown2docx`／`変換先を安全に制限する` | Literal Pathと同名Output | Path Negative Test |
| `markdown2docx`／`変換失敗時に正本を保持する` | SourceをRead-only Contractとして扱う | Hash比較、Failure報告 |
| `openspec-git-workflow`／`Delegate each phase to the existing workflow` | Thin Wrapper | Delegation結果 |
| `openspec-git-workflow`／`Commit only successful isolated phase changes` | Baseline差分からStage | Isolated Repository Test |
| `openspec-git-workflow`／`Use project commit policy and verify checkpoints` | 日本語Conventional Commit、Empty Verify | Commit Message／Git Log |
| `openspec-git-workflow`／`Preserve repository history and remotes` | Push／Amend／Rewrite禁止 | Failure／Conflict Test |

### 13.1 Scenario Traceability

| Capability | Source Scenario |
| --- | --- |
| `project-setup` | `Install a user-scoped package` |
| `project-setup` | `Choose the minimum setup` |
| `project-setup` | `Choose optional tools` |
| `project-setup` | `Add or migrate a project skill` |
| `project-setup` | `A third-party skill exists locally` |
| `project-setup` | `A repository-owned skill changes` |
| `project-setup` | `Complete the canonical setup` |
| `mysdd-workflow` | `Complete a normal change` |
| `mysdd-workflow` | `Publish a distributable document` |
| `mysdd-workflow` | `Verification succeeds` |
| `mysdd-workflow` | `Verification fails` |
| `mysdd-workflow` | `Verification changes no tracked files` |
| `mysdd-schema` | `Inspect a MySDD change` |
| `mysdd-schema` | `Propose a MySDD change` |
| `mysdd-schema` | `Complete the proposal workflow` |
| `generate-prd` | `Required artifacts exist` |
| `generate-prd` | `Required artifacts are missing` |
| `generate-prd` | `A required section lacks source information` |
| `generate-prd` | `DOCX conversion fails` |
| `generate-hld` | `Required artifacts exist` |
| `generate-hld` | `Design is absent` |
| `generate-hld` | `A required section lacks source information` |
| `generate-hld` | `DOCX conversion fails` |
| `markdown2docx` | `要件定義書を変換する` |
| `markdown2docx` | `基本設計書を変換する` |
| `markdown2docx` | `出力先が入力と対応しない` |
| `markdown2docx` | `必須入力が存在しない` |
| `markdown2docx` | `Rendererが失敗する` |
| `markdown2docx` | `変換が成功する` |
| `openspec-git-workflow` | `Run an accepted phase` |
| `openspec-git-workflow` | `Reject an unsupported phase` |
| `openspec-git-workflow` | `Unrelated changes predate the phase` |
| `openspec-git-workflow` | `Phase output overlaps a pre-existing path` |
| `openspec-git-workflow` | `Apply changes tracked files` |
| `openspec-git-workflow` | `Verify changes no tracked files` |
| `openspec-git-workflow` | `OpenSpec phase fails` |
| `openspec-git-workflow` | `Repository is conflicted` |

全RequirementのScenario名は対応するArchive済みDelta Specを正本とし、Test Case作成時に
省略せず使用する。

## 14. 未決事項・リスク

### 14.1 未決事項

- 文書変換の性能・容量上限：代表文書と許容時間の合意後に定義するため`TBD`
- QR-007の定義：対応する品質要求が生じるまで`TBD`

### 14.2 確定した運用方針

- CI：GitHub Actionsの`.github/workflows/quality.yml`にある`quality` Job
- CI Platform：`ubuntu-latest`。Windows SetupはReview済み手順書としてCI対象外
- Log：GitHub Actions標準Job Log。保持期間はRepository設定に従う
- 監視：専用Dashboard、外部AlertおよびOn-callは導入しない
- Release：`quality`成功後にMaintainerがSemVer Tagを手動作成する

### 14.3 リスクと軽減策

- **旧Skill名を使用するCallerが残る** → Repository全体を検索し、Live Callerを同一変更で更新する。
- **Reference DOCX移動で変換が失敗する** → 成功TestとReference欠落Testを実行する。
- **ADR内容が削除時に失われる** → ADR-001～ADR-010の対応表とStrict ValidationをDeletion Gateにする。
- **Archive内の旧名称をLive不整合と誤認する** → Live Path検索ではArchiveを歴史的Evidenceとして区別する。
- **文書Testが正本Markdownを変更する** → 変換前後Hashを比較し、Source不変を必須にする。
- **Phase CommitへUser変更が混入する** → Baselineと重複するPathがあればCommitを拒否する。
