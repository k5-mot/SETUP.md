# 🛠️ Windows開発環境とOpenSpec

Windows 11の開発環境を構築し、OpenSpecのMySDD（`mysdd`）Schemaで仕様駆動開発を行うためのRepository。

## 🚀 セットアップ

- 最小構成: [SETUP.md](docs/manual/SETUP.md)
- 拡張構成: [SETUP.full.md](docs/manual/SETUP.full.md)

セットアップ後、PowerShellでmiseを有効化する。

```powershell
# このPowerShellセッションでmise管理のToolを有効化する。
(&mise activate pwsh) | Out-String | Invoke-Expression

# OpenSpecのカスタムSchemaを検証する。
openspec schema validate mysdd --verbose
```

Schema検証が成功すれば利用準備は完了。失敗した場合は、Repositoryのルートで実行していることを確認する。

## 🔄 開発ワークフロー

Coding Agentへ次のSkillを順に指定する。

```text
# ISO観点を含む4つの計画Artifactを作成する。
$openspec-propose <変更内容>

# 要件定義書を別途生成する。
$gen-pd <change-name>

# 基本設計書を別途生成する。
$gen-bd <change-name>

# Tasksに従って実装する。
$openspec-apply-change <change-name>

# 実装とArtifactの整合性を検証する。
$openspec-verify-change <change-name>

# 検証済みChangeをArchiveする。
$openspec-archive-change <change-name>
```

MySDDはOpenSpec標準の4 ArtifactにISO/IEC/IEEE 12207とISO/IEC 25010の観点を追加する。
`rd`と`bd`はSchema Artifactではなく、Propose後に専用Agent Skillで生成する。

| Step | 完了結果 | 中断条件 |
| --- | --- | --- |
| Propose | ISO観点を含む4つの計画Artifactがある | ArtifactまたはISO観点が不足している |
| 文書生成 | `gen-pd`と`gen-bd`がMarkdownとDOCXを生成している | 必須入力または正本Markdownが不足している |
| Apply | Tasksと必要なテストが完了している | ApplyがBlocked、またはテストが失敗する |
| Verify | CRITICALな不整合がない | CRITICALな不整合がある |
| Archive | ChangeがArchiveされ、Delta Specが反映される | Verify未完了、またはArchiveが失敗する |

## 📄 ワークフロー全体で生成される成果物

```text
openspec/changes/<change-name>/
├─ proposal.md
├─ specs/<capability>/spec.md
├─ design.md
├─ tasks.md
└─ docs/
   ├─ rd.md
   ├─ rd.docx
   ├─ bd.md
   └─ bd.docx
```

Markdownが正本。DOCXはPandocで再生成され、Git管理外となる。

## ♻️ 文書の再生成

Proposal、Delta Spec、Designを更新した場合は、Coding Agentへ対象Changeを指定する。

```text
# 要件定義書を再生成する。
$gen-pd <change-name>

# 基本設計書を再生成する。
$gen-bd <change-name>
```

`gen-pd`はProposalとDelta Specを使用する。`gen-bd`はそれらに加え、存在する場合はDesignも使用する。入力にない情報は補完せず、必要な箇所を`TBD`とする。

## 📚 ドキュメント

- [OpenSpec標準ワークフロー](docs/references/OpenSpec-Workflow.md)
- [MySDDワークフロー](docs/references/MySDD-Workflow.md)
- [MySDDカスタムSchema仕様](docs/references/MySDD-Spec.md)
- [Architecture Decision Records](docs/adr/ADR.md)
