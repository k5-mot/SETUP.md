# 🔄 OpenSpec開発ワークフロー

この流れはOpenSpecのデフォルトSchemaである`spec-driven`を使う。ProposeでProposal、Delta Spec、Design、Tasksを作成し、次の順に進める。

```text
propose → apply → verify → archive
```

## 1️⃣ Propose

```text
# Changeと計画Artifactを作成する。
/opsx:propose <変更内容>
```

Changeを作成し、実装前に必要なArtifactを生成する。生成物を確認し、内容が正しくなるまで実装へ進まない。

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

> コマンド名はツールによって`/opsx-propose`や`$openspec-propose`などと表示される。`verify`はOpenSpecのWorkflow設定で有効化しておく。

## References

- [OpenSpec Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
