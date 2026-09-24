<!-- markdownlint-disable MD013 MD033 MD041 -->

## Why

OpenSpec PhaseのGit運用が専用Skill、`openspec/config.yaml`、`CONTRIBUTING.md`
および関連文書へ分散しているため、同じ規則の重複と実行契約の不一致が起きやすい。
Git規則とPhase固有の実行タイミングをそれぞれ一つの正本へ集約し、Archive後の
`feature/*`から`main`への統合まで一貫して案内できるようにする。

## What Changes

- **BREAKING**: Repository管理Skill `openspec-git-workflow`を削除し、その
  Capabilityを廃止する。
- GitのBranch、Commit、Stage、履歴保護、Pull RequestおよびMerge規則を
  `CONTRIBUTING.md`へ集約する。
- OpenSpecのPropose、Apply、Verify、ArchiveにおけるCommit時点と、Archive後に
  `feature/*`を`main`へ統合する時点を`openspec/config.yaml`へ集約する。
- Archive後の統合は、`CONTRIBUTING.md`が定めるPull RequestとCIの条件を満たして
  から実行する。
- `.agents/skills/.gitignore`のRepository管理Skill一覧から
  `openspec-git-workflow`を除外する。
- `AGENTS.md`からCommit TrailerとAuthorに関するGit固有ルールを除き、
  `CONTRIBUTING.md`の共通規則へ移す。
- Project Spec、MySDD参照文書、PRDおよびHLDから専用Skill前提を除去し、新しい
  責務分離へ更新する。

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `openspec-git-workflow`: 専用Agent Skillとその4 Requirementを廃止し、Capabilityを
  削除する。
- `project-setup`: Repositoryが追跡するSkillを`generate-prd`、`generate-hld`、
  `markdown2docx`の3件へ変更する。
- `mysdd-workflow`: PhaseごとのCommit境界とArchive後の`main`統合を、
  `openspec/config.yaml`のタイミング指示と`CONTRIBUTING.md`のGit規則で実現する。

## Impact

- `.agents/skills/openspec-git-workflow/`を削除する。
- `.agents/skills/.gitignore`、`AGENTS.md`、`CONTRIBUTING.md`、
  `openspec/config.yaml`を更新する。
- `openspec/specs/openspec-git-workflow/`を廃止し、`project-setup`および
  `mysdd-workflow`のMain Specを更新する。
- `docs/references/MySDD-Spec.md`、`openspec/publics/prd.md`および
  `openspec/publics/hld.md`の旧Skill参照と責務記述を更新する。
- Runtime APIや外部Dependencyは変更しない。

## Stakeholders and Lifecycle Impact

- **Acquisition:** 新しいToolやDependencyは導入しない。
- **Supply:** ContributorとCoding Agentは、Git規則を`CONTRIBUTING.md`、OpenSpecの
  実行タイミングを`openspec/config.yaml`から取得する。
- **Transition:** 既存Skillを削除するため、そのSkill名を直接呼び出す手順は新しい
  OpenSpec操作と設定駆動のGit運用へ移行する。
- **Operation:** 各Phaseの完了時点とArchive後のMerge時点を設定から一貫して案内する。
- **Maintenance:** Git規則とPhase Timingの正本を分離し、同じ規則の重複を許可しない。
- **Disposal:** Skill Directory、追跡例外、Capability Specおよび文書参照を同一変更で
  削除する。Archive済みChangeの履歴は変更しない。

## Quality Considerations

- **QR-001 Functional suitability:** 測定量は4 Phaseに定義されたCommit Timingと
  Archive後Merge Timingの網羅率、目標値は100%、検証方法はConfig Inspectionとする。
- **QR-002 Maintainability:** 測定量は現行文書に残る`openspec-git-workflow`参照数と
  Git規則の重複数、目標値はともに0件、検証方法はRepository検索と文書Reviewとする。
- **QR-003 Compatibility:** 測定量はOpenSpecの厳格検証Failure数、目標値は0件、
  検証方法はMain Spec、Active ChangeおよびArchiveのStrict Validationとする。
- **QR-004 Reliability:** 測定量はPhase失敗時またはConflict時に作成されるCommit数、
  目標値は0件、検証方法はGit規則とConfig TimingのScenario Reviewとする。
- **QR-005 Security:** 測定量は無関係なPathを含むCommit数と履歴書換え回数、目標値は
  0件、検証方法はStaged DiffおよびGit履歴Reviewとする。
- **Performance efficiency:** 文書と設定のみの変更であり、Runtime性能には適用しない。
- **Interaction capability:** User Interfaceを変更しないため適用しない。
- **Flexibility:** Git Providerを変更せずGitHub Flowを維持するため、新たな数値目標は
  設けない。
- **Safety:** Safety関連機能を変更しないため適用しない。
