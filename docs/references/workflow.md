# 🔄 OpenSpec開発ワークフロー

OpenSpecのデフォルトSchemaは`spec-driven`である。このProjectでは、そのProposal、Delta Spec、Design、Tasksを維持し、要件定義書と基本設計書を追加した`sdd-custom`を使う。開発の流れは変えない。

```text
propose → apply → verify → archive
```

## 1️⃣ Propose

```text
# Changeと計画Artifactを作成する。
/opsx:propose <変更内容>
```

Changeを作成し、Proposal、Delta Spec、Design、Tasks、`docs/rd.md`、`docs/bd.md`を生成する。生成物を確認し、内容が正しくなるまで実装へ進まない。

### Propose完了時の構成

```text
openspec/
├─ config.yaml
├─ schemas/sdd-custom/
│  ├─ schema.yaml
│  └─ templates/
└─ changes/
   └─ <change-name>/
      ├─ .openspec.yaml
      ├─ proposal.md
      ├─ specs/
      │  └─ <capability>/spec.md
      ├─ design.md
      ├─ tasks.md
      └─ docs/
         ├─ rd.md
         ├─ rd.docx
         ├─ bd.md
         └─ bd.docx
```

DOCXは生成されるがGit管理外となる。必要なArtifactが欠けている場合はApplyへ進まない。

## 2️⃣ Apply

```text
# Tasksに沿って実装する。
/opsx:apply <change-name>
```

Tasksに沿って実装とテストを行い、完了した項目を更新する。

## 3️⃣ Verify

```text
# 実装とArtifactの整合性を確認する。
/opsx:verify <change-name>
```

実装が要求、Spec、Design、Tasksと一致し、必要なテストが成功していることを確認する。問題があれば修正し、再度実行する。

## 4️⃣ Archive

```text
# 完了したChangeを保管する。
/opsx:archive <change-name>
```

検証済みのChangeをアーカイブし、Delta SpecをCanonical Specへ反映する。

### Archive完了時の構成

```text
openspec/
├─ specs/
│  └─ <capability>/spec.md
└─ changes/
   └─ archive/
      └─ YYYY-MM-DD-<change-name>/
         ├─ .openspec.yaml
         ├─ proposal.md
         ├─ specs/
         │  └─ <capability>/spec.md
         ├─ design.md
         ├─ tasks.md
         └─ docs/
            ├─ rd.md
            ├─ rd.docx
            ├─ bd.md
            └─ bd.docx
```

`openspec/specs/`にはDelta Specを反映したCanonical Specが残り、Change一式は日付付きのArchiveへ移動する。Archiveに失敗した場合は、Changeを手作業で移動せず原因を修正して再実行する。

## 🧭 その他のコマンド

### Explore

```text
# 実装前に課題、選択肢、要求を整理する。
/opsx:explore <検討内容>
```

変更内容が曖昧なときにProposeの前に使う。通常はArtifactや実装を変更しない。

### Sync

```text
# Delta SpecをCanonical Specへ反映し、ChangeはActiveのまま残す。
/opsx:sync <change-name>
```

長期のChangeや並行Changeで、Archive前に`openspec/specs/`を更新したい場合に使う。成功時はCanonical Specが更新され、対象Changeは`openspec/changes/<change-name>/`に残る。失敗時はArchiveへ進まず、Delta SpecとCanonical Specの不整合を修正する。

通常はArchive時にSyncできるため、個別実行は任意となる。

## 💾 コミット

Commit MessageとGit操作の共通ルールは[Contributing Guideline](../CONTRIBUTING.md)に従う。

各工程後に追跡対象の変更がある場合は、検証してから論理単位でCommitする。変更がない場合は空Commitを作らない。

| 境界 | Commit対象 |
| --- | --- |
| Propose完了後 | Proposal、Delta Spec、Design、Tasks、`rd.md`、`bd.md` |
| Apply中または完了後 | 完了した独立TaskまたはTask群の実装、テスト、Task更新 |
| Verify完了後 | Verifyで発生した修正または追跡対象の検証記録 |
| `rd`／`bd`再生成後 | 内容が変わった正本Markdown。Git管理外のDOCXは含めない |
| Archive完了後 | Archiveへ移動したChangeと、更新されたCanonical Spec |

> コマンド名はツールによって`/opsx-propose`や`$openspec-propose`などと表示される。`verify`はOpenSpecのWorkflow設定で有効化しておく。

## References

- [OpenSpec Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
- [OpenSpec Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)
