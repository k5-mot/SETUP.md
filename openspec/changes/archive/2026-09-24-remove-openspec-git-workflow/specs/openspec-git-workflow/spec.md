<!-- markdownlint-disable MD013 MD022 MD032 MD041 -->

## REMOVED Requirements

### Requirement: Delegate each phase to the existing workflow

**Reason**: Git運用を専用Agent Skillへ委譲せず、Git規則を`CONTRIBUTING.md`、
OpenSpec Phaseの実行Timingを`openspec/config.yaml`へ集約するため。

**Migration**: 各OpenSpec Workflowを直接使用し、Git操作は両正本文書の指示に従う。

### Requirement: Commit only successful isolated phase changes

**Reason**: Phase固有のStageおよびCommit規則をRepository共通のGit規則として管理し、
専用Wrapperへの依存をなくすため。

**Migration**: `CONTRIBUTING.md`の変更境界、StageおよびConflict規則へ移行する。

### Requirement: Use project commit policy and verify checkpoints

**Reason**: Commit内容の規則とCommitするTimingの責務を分離し、重複定義をなくすため。

**Migration**: Commit規則は`CONTRIBUTING.md`、各PhaseのCommit Timingは
`openspec/config.yaml`を参照する。

### Requirement: Preserve repository history and remotes

**Reason**: 履歴とRemoteを保護する規則をOpenSpec専用SkillではなくRepository全体へ
適用するため。

**Migration**: `CONTRIBUTING.md`の履歴保護、Push、MergeおよびConflict規則へ移行する。
