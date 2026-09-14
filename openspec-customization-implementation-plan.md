# 🧩 OpenSpecカスタマイズ実装計画

## 1️⃣ 目的

OpenSpecの`spec-driven`を維持し、要件定義書と基本設計書をChangeのArtifactとして追加する。Markdownを正本、DOCXを配布物とする。

## 2️⃣ 構成

```text
openspec/
├─ config.yaml
├─ schemas/sdd-custom/
│  ├─ schema.yaml
│  └─ templates/
│     ├─ proposal.md
│     ├─ spec.md
│     ├─ design.md
│     ├─ tasks.md
│     ├─ rd.md
│     └─ bd.md
└─ changes/<change-name>/
   ├─ proposal.md
   ├─ specs/<capability>/spec.md
   ├─ design.md
   ├─ tasks.md
   └─ docs/
      ├─ rd.md
      ├─ rd.docx
      ├─ bd.md
      └─ bd.docx

.agents/skills/
├─ gen-pd/SKILL.md
└─ gen-bd/SKILL.md
```

## 3️⃣ Artifact

| ID | 出力 | 依存 |
| --- | --- | --- |
| `proposal` | `proposal.md` | なし |
| `specs` | `specs/**/*.md` | `proposal` |
| `design` | `design.md` | `proposal` |
| `tasks` | `tasks.md` | `specs`、`design` |
| `rd` | `docs/rd.md` | `proposal`、`specs` |
| `bd` | `docs/bd.md` | `proposal`、`specs` |

Applyには`tasks`、`rd`、`bd`を必須とする。`design.md`が省略された場合、`bd.md`の設計固有項目は`TBD`とする。

## 4️⃣ 文書生成Skill

### 📋 gen-pd

- Artifact ID: `rd`
- 入力: `proposal.md`、`specs/**/*.md`
- 出力: `docs/rd.md`、`docs/rd.docx`

### 🏛️ gen-bd

- Artifact ID: `bd`
- 入力: `proposal.md`、`specs/**/*.md`、存在する場合の`design.md`
- 出力: `docs/bd.md`、`docs/bd.docx`

両Skillは入力にない事実を追加せず、不足情報を`TBD`とする。Requirement見出し、Scenario名、既存ID、参照関係を保持する。

## 5️⃣ DOCX

`rd.docx`と`bd.docx`は正本MarkdownからPandocで生成し、Git管理外とする。`reference.docx`だけを追跡する。

## 6️⃣ 検証

```powershell
# sdd-customのSchemaとTemplateを検証する。
openspec schema validate sdd-custom --verbose

# ChangeのArtifact依存関係と出力先を確認する。
openspec status --change '<change-name>' --json

# ChangeとDelta Specを厳格に検証する。
openspec validate '<change-name>' --strict
```

## 7️⃣ 受入条件

- `sdd-custom`が`spec-driven`の4 Artifactと`rd`、`bd`を持つ。
- `rd`と`bd`の指示が対応Skillを使用する。
- `docs/rd.md`と`docs/bd.md`がChange配下へ生成される。
- `tasks`、`rd`、`bd`が揃うまでApplyがBlockedになる。
- MarkdownだけがGit管理され、DOCXは再生成できる。

## References

- [OpenSpec Customization](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md)
- [OpenSpec Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
