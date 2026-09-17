---
name: openspec-git-workflow
description: OpenSpecのpropose、apply、verify、archiveのいずれか1 Phaseを実行し、既存変更を含めず成功したPhaseだけをCommitする場合に使用する。
---

# OpenSpec Gitワークフローを実行する

Phase（`propose`、`apply`、`verify`、`archive`のいずれか）と`change-name`を
それぞれ1つだけ受け取る。それ以外のPhaseはRepositoryを変更せず拒否する。

## 変更境界を記録する

Repository Rootで現在のBranch、`HEAD`、未追跡ファイルを含むPorcelain Status、
未解決Pathを記録する。このSnapshotを既存Worktreeとして扱う。GitがすでにConflictを
報告している場合は直ちに停止する。

## Phaseを委譲する

指定されたPhaseに対応する、インストール済みのOpenSpecワークフローを呼び出す。
そのワークフローの指示を完全に実行し、指示を再実装したり迂回したりしない。
委譲先ワークフローの成功または失敗を最終判定とする。

- `propose`: `openspec-propose`を使用する
- `apply`: `openspec-apply-change`を使用する
- `verify`: `openspec-verify-change`を使用する
- `archive`: `openspec-archive-change`を使用する

委譲先ワークフローが失敗した場合は、その失敗を報告してCommitを作成しない。

## 結果を分離して検査する

成功後、新しいPorcelain StatusをBaselineと比較する。Phaseが変更したPathにBaseline
時点の変更がある場合、GitがConflictを報告する場合、またはPhaseによる変更だと
確定できない場合は、StageもCommitも行わず停止する。無関係な既存変更をすべて
保持する。

このPhaseが所有するPathだけをStageする。`AGENTS.md`に従い、Staged Diff、Test、
生成ファイルおよびSecret混入の可能性を検査する。検査に失敗した場合はPhaseの
PathだけをUnstageし、理由を報告する。

## PhaseをCommitする

gitmojiを含む日本語のConventional Commitを、必須のAI支援Trailer付きで1件だけ
作成する。SubjectでPhaseとChangeを識別できるようにする。成功した`verify` Phaseが
追跡対象ファイルを変更しなかった場合に限り、Empty Commitを使用する。

Push、Amend、Reset、Clean、履歴の書き換え、未解決ConflictのCommitは行わない。
Commit IDを報告し、すべての既存変更を変更せず残す。
