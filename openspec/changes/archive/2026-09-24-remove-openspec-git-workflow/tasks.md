<!-- markdownlint-disable MD041 -->

## 1. Git Policy Source

- [x] 1.1 `CONTRIBUTING.md`へAI支援Trailer、人間のAuthor、変更境界、Stage、
  Conflict、履歴保護、PushおよびMergeのGit規則を集約し、各規則がRFC 8174
  Keywordで一意に定義されていることをReviewする
- [x] 1.2 `AGENTS.md`から重複するGit固有ルールを削除し、
  `CONTRIBUTING.md`への既存参照だけで規則が到達可能なことを確認する

## 2. OpenSpec Operation Timing

- [x] 2.1 `openspec/config.yaml`の`context`へPropose、Apply、Verify、Archiveの
  Commit Timingを各1件記載し、Verifyの成功・失敗Checkpointと無変更時のEmpty
  Commitを明示する
- [x] 2.2 Archive TimingへArchive Commit後の`feature/*`から`main`への統合を記載し、
  Pull RequestとCI条件は`CONTRIBUTING.md`だけを参照する構成にする
- [x] 2.3 重複する`operations.apply`および`operations.archive`のGit Guidanceを削除し、
  OpenSpec 1.13.0がConfigをWarningなしで読み込むことを確認する

## 3. Wrapper Skill Disposal

- [x] 3.1 `.agents/skills/openspec-git-workflow/SKILL.md`を削除し、Gitが削除として
  追跡することを確認する
- [x] 3.2 `.agents/skills/.gitignore`からWrapper用例外と4 Skill表記を削除し、
  Repository管理Skillが3件だけ追跡され、同名のLocal Skill PathがIgnoreされることを
  `git check-ignore`と`git ls-files`で確認する

## 4. Living Documentation Migration

- [x] 4.1 `docs/references/MySDD-Spec.md`からWrapperの構成、責務およびTest記述を除き、
  Git規則とOperation Timingの正本分離およびArchive後Mergeへ更新する
- [x] 4.2 `openspec/publics/prd.md`と`openspec/publics/hld.md`からWrapper前提を除き、
  Config駆動のPhase境界と`CONTRIBUTING.md`準拠のMerge Flowへ更新する
- [x] 4.3 Archived Changeを変更せず、現行のSkill、Config、Agent指示、Living Documentに
  重複したGit規則または有効なWrapper参照が残っていないことを対象限定検索で確認する

## 5. Quality and Lifecycle Evidence

- [x] 5.1 QR-001とQR-004のEvidenceとして、更新後のConfigが4 Phase Timingと
  Archive後Merge Timingを100%含み、ApplyおよびArchive Instructionへ反映されることを
  JSON出力で確認する
- [x] 5.2 QR-002とQR-005のEvidenceとして、Wrapperの追跡File数、現行文書参照数、
  無関係なStaged Path数および履歴書換え数がすべて0件であることを確認する
- [x] 5.3 QR-003のEvidenceとしてOpenSpec Schema、全Main Spec、Active Change、Archive、
  Markdownlint、Local Link、Ruff、品質TestおよびDOCX Testを実行し、すべて成功することを
  確認する
- [x] 5.4 ISO/IEC/IEEE 12207の移行および廃止Evidenceとして、3 Skillの追跡継続、
  Wrapper CapabilityのRetirement Delta、Archive履歴の無変更およびRollback手順をReviewする
