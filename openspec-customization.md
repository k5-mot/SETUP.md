# 🧩 OpenSpecカスタマイズ: Config・Schema・Template

> OpenSpecのカスタマイズは、まず`openspec/config.yaml`、次にプロジェクトローカルのCustom Schema、最後にユーザー共通Schemaの順で検討する。
> 仕様確認日: 2026-09-14

## 1️⃣ どこを変更するか

| レベル | 変更できること | 適した用途 |
| --- | --- | --- |
| Project Config | 既定Schema、プロジェクト文脈、Artifact別ルール、Apply／Archiveのガイダンス | ほとんどのチーム |
| Custom Schema | Artifactの種類、生成ファイル、依存関係、指示、Template | 独自の承認・調査・レビュー工程があるチーム |
| User-level Schema | 複数プロジェクトで共通利用するSchema | 個人共通のワークフロー。配布・再現性には注意 |

判断の目安は次のとおり。

- 出力の観点やチーム規約を足すだけなら`config.yaml`の`context`／`rules`を使う。
- 見出しや記入形式を変えるならTemplateを変える。
- Artifactを追加・削除する、順序や依存関係を変えるならSchemaを変える。
- チームで共有するSchemaは`openspec/schemas/`へ置き、コードと一緒にバージョン管理する。

## 2️⃣ Project Config

`openspec/config.yaml`は最も軽量なカスタマイズ手段である。

```yaml
# openspec/config.yaml
schema: spec-driven

context: |
  Tech stack: TypeScript, React, Node.js, PostgreSQL
  API style: REST。公開APIの後方互換性を維持する
  Testing: Vitest + Playwright
  ADRはdocs/adr/へ保存する

rules:
  proposal:
    - ロールバック方針を含める
    - 影響するチームと運用を明記する
  specs:
    - WHEN／THENで検証可能なScenarioを書く
    - 新しいパターンを作る前に既存Specを参照する
  design:
    - 採用しなかった代替案と理由を残す
  tasks:
    - 実装と対応するテストを同じ作業単位へ含める

operations:
  apply:
    guidance:
      - 変更箇所に近いテストを先に実行する
      - 全テスト前にLintと型検査を実行する
  archive:
    guidance:
      - 完了サマリーを簡潔にする
```

Artifact生成時の指示は、主に次の要素から構成される。

```text
context（全Artifact共通）
rules（対象Artifactだけ）
SchemaのinstructionとTemplate
依存Artifactの内容
```

`context`は各Artifactの指示へ追加され、`rules`は一致するArtifactだけへ追加される。

`context`は全Artifactへ入るため、長い設計書を貼る場所ではない。公式仕様では50KBの上限がある。安定した短い規約だけを記載し、詳細文書はパスやリンクで参照する。

標準SchemaのArtifact IDは`proposal`、`specs`、`design`、`tasks`である。`rules`のキーを誤ると警告になるため、次で確認する。

```powershell
# SchemaとArtifact IDをJSONで確認する。
openspec schemas --json
```

## 3️⃣ Custom Schemaを作る

### 既定SchemaからForkする

既定の規約を保ちながら一部だけ変える場合に推奨する。

```powershell
# 既定Schemaをプロジェクト用SchemaへForkする。
Set-Location -LiteralPath '<project-root>'
openspec schema fork spec-driven team-spec-driven
```

生成物:

```text
openspec/schemas/team-spec-driven/
├─ schema.yaml
└─ templates/
   ├─ proposal.md
   ├─ spec.md
   ├─ design.md
   └─ tasks.md
```

### ゼロから作る

```powershell
# 対話形式
openspec schema init research-first

# 非対話形式
openspec schema init rapid `
  --description '短い変更向けの軽量ワークフロー' `
  --artifacts 'proposal,tasks' `
  --default
```

既存Schemaを上書きする`--force`は、差分を確認し、上書き対象が明確な場合だけ使う。

## 4️⃣ `schema.yaml`の構造

次は、Proposalの前に調査を置き、実装前にレビューを必須にする例である。

```yaml
# openspec/schemas/research-first/schema.yaml
name: research-first
version: 1
description: 調査と実装前レビューを含む変更ワークフロー

artifacts:
  - id: research
    generates: research.md
    description: 既存実装、制約、選択肢の調査
    template: research.md
    instruction: |
      既存コードと仕様を調べ、事実と推測を分けて記録する。
      変更候補、影響範囲、未解決事項を示す。
    requires: []

  - id: proposal
    generates: proposal.md
    description: 調査に基づく変更提案
    template: proposal.md
    instruction: |
      research.mdを根拠に、変更の目的と範囲を説明する。
      実装詳細より、問題と期待する結果を優先する。
    requires:
      - research

  - id: specs
    generates: "specs/**/*.md"
    description: 振る舞いのDelta Spec
    template: spec.md
    instruction: |
      外部から観測でき、テスト可能な振る舞いを定義する。
    requires:
      - proposal

  - id: design
    generates: design.md
    description: 技術設計
    template: design.md
    instruction: |
      要件を実現する構成、データフロー、移行方法を説明する。
    requires:
      - proposal

  - id: review
    generates: review.md
    description: 実装前レビュー
    template: review.md
    instruction: |
      SpecとDesignを確認し、セキュリティ、性能、テスト、運用上の
      懸念と、実装開始を妨げる未解決事項を列挙する。
    requires:
      - specs
      - design

  - id: tasks
    generates: tasks.md
    description: 実装チェックリスト
    template: tasks.md
    instruction: |
      依存順に並んだ、検証可能な実装タスクを作る。
    requires:
      - review

apply:
  requires:
    - tasks
  tracks: tasks.md
```

主要フィールド:

| フィールド | 役割 |
| --- | --- |
| `name` | Schema名。ディレクトリ名と一致させる |
| `version` | Schema定義のバージョン |
| `description` | 一覧で用途を判断するための説明 |
| `artifacts[].id` | コマンド、依存関係、Configの`rules`で使う一意なID |
| `generates` | 生成先。`specs/**/*.md`のようなglobも使用可能 |
| `template` | 同Schemaの`templates/`配下にあるファイル名 |
| `instruction` | そのArtifactを作るAIへの意味的な指示 |
| `requires` | 先に存在すべきArtifact ID |
| `apply.requires` | 実装開始に必要なArtifact |
| `apply.tracks` | 実装進捗を追跡するファイル |

`artifacts`の列挙順は、同時に複数Artifactを生成可能な場合の優先順になる。`requires`は依存グラフを作るため、循環依存にしてはいけない。

## 5️⃣ Templateを設計する

TemplateはMarkdownで、Artifact生成時にそのままAIへのプロンプトへ渡される。変更後のビルドは不要で、次回生成から反映される。

### `templates/research.md`

```markdown
# 調査結果

## 調査対象

<!-- 対象の機能、コード、Spec、外部依存を列挙する -->

## 確認できた事実

<!-- ファイルパスやコマンド結果など、検証可能な根拠を添える -->

## 選択肢

| 選択肢 | 利点 | 欠点 | 制約 |
| --- | --- | --- | --- |

## 影響範囲

<!-- 変更されるCapability、API、データ、運用、テスト -->

## 未解決事項

<!-- Proposal確定前に回答が必要な問い -->
```

### `templates/review.md`

```markdown
# 実装前レビュー

## 判定

- [ ] 実装開始可能
- [ ] 要修正

## チェック

- [ ] ProposalとDelta Specの対象範囲が一致している
- [ ] 全Requirementに検証可能なScenarioがある
- [ ] Designが移行とロールバックを扱っている
- [ ] セキュリティとプライバシー上の影響を確認した
- [ ] 性能と可用性のリスクを確認した
- [ ] Tasksにテストと文書更新が含まれる

## Blocker

<!-- 実装開始を妨げる事項。なければ「なし」 -->

## Follow-up

<!-- 実装を妨げない後続作業 -->
```

### Template作成の原則

- 見出しで期待する出力構造を固定する。
- HTMLコメントで記入基準を伝え、生成後の本文には不要な説明を残さない。
- 抽象的な「詳しく書く」ではなく、必要な観点を列挙する。
- 例を載せる場合は、内容ではなく形式を模倣できる最小例にする。
- `instruction`には目的と判断基準、Templateには出力の形を置く。
- 標準のSpec形式を変える場合は、OpenSpecのValidationとArchiveが期待する見出しを壊さない。

## 6️⃣ 検証して利用する

```powershell
# Schema定義、Template参照、循環依存、Artifact IDを検証
openspec schema validate research-first --verbose

# 利用可能なSchemaと解決元を確認
openspec schemas
openspec schema which research-first
openspec schema which --all

# Artifactごとに実際に解決されるTemplateを確認
openspec templates --schema research-first
openspec templates --schema research-first --json

# 明示的にSchemaを指定してChangeを作る
openspec new change investigate-cache --schema research-first
```

プロジェクトの既定にする場合は`openspec/config.yaml`へ設定する。

```yaml
schema: research-first
```

作成済みChangeが使用するSchemaはChange内の`.openspec.yaml`へ記録されるため、プロジェクト既定を後から変えても、既存Changeのワークフローを意図せず変えない。

## 7️⃣ Schemaの選択順と解決順

「どのSchema名を使うか」と「そのSchemaをどこから読むか」は別の優先順位を持つ。

### 使用するSchema名の選択

1. CLIの`--schema <name>`
2. Change内の`.openspec.yaml`
3. `openspec/config.yaml`の`schema`
4. 既定の`spec-driven`

### 同名Schemaの解決元

1. プロジェクト: `openspec/schemas/<name>/`
2. ユーザー: `${XDG_DATA_HOME}/openspec/schemas/<name>/`
3. OpenSpecパッケージ内の組み込みSchema

Windowsで実際の解決先を推測せず、次のコマンドの出力を正とする。

```powershell
# Schemaの解決元を確認する。
openspec schema which '<schema-name>'
openspec schema which --all
```

プロジェクトSchemaが推奨される理由は、コードレビュー、バージョン固定、CI検証、他メンバーとの共有が可能だからである。User-level Schemaは個人用の横断設定に限定する。

## 8️⃣ 安全な変更手順

1. 作業前に`git status --short`を確認する。
2. 組み込みSchemaを直接編集せず、`openspec schema fork`する。
3. まずTemplateだけを小さく変更する。
4. 新しいテスト用Changeを作り、Artifact単位で出力を確認する。
5. `openspec schema validate <name> --verbose`を実行する。
6. `openspec templates --schema <name>`で参照先を確認する。
7. Schemaの依存関係を変えた場合は、`continue`と`ff`の両方を試す。
8. `git diff`でSchema、Template、Config以外の予期しない変更がないか確認する。
9. チームレビュー後に既定Schemaを切り替える。

## 9️⃣ よくある問題

### `rules`が反映されない

- ファイル名が`openspec/config.yaml`であることを確認する。`.yml`ではない。
- YAML構文を確認する。
- `rules`のキーがSchemaのArtifact IDと一致するか`openspec schemas --json`で確認する。
- Configの変更は即時反映されるため、通常は再起動不要である。

### Templateが使われない

```powershell
# TemplateとSchemaの解決元を確認する。
openspec templates --schema '<schema-name>'
openspec schema which '<schema-name>'
```

別の同名Schema、Changeに保存されたSchema名、または`--schema`指定が優先されていないか確認する。

### Schema Validationが失敗する

- `schema.yaml`が正しいYAMLか確認する。
- `template`が`templates/`内の実在ファイルを指すか確認する。
- `requires`に存在しないArtifact IDがないか確認する。
- 依存グラフが循環していないか確認する。
- Artifact IDとSchema名をkebab-case中心の単純な名前にする。

### 標準SpecをカスタマイズしたらArchiveで壊れる

SpecはOpenSpecが解析する構造を持つ。少なくともRequirementとScenarioの見出し、Delta操作の見出し、`MODIFIED`の完全な要件ブロックという規約を維持する。見た目だけを変えるために解析対象の構造を変更しない。

## 🔟 CIでの確認例

```powershell
# SchemaとすべてのChangeを検証する。
openspec schema validate
if ($LASTEXITCODE -ne 0) { throw 'OpenSpec schema validation failed.' }

openspec validate --all
if ($LASTEXITCODE -ne 0) { throw 'OpenSpec change/spec validation failed.' }
```

SchemaとTemplateを変更するPull Requestでは、少なくとも次をレビュー対象にする。

- Artifact依存グラフに意図しない待ちや循環がない。
- `apply.requires`が必要なレビューを迂回しない。
- Templateが機密情報の記入を求めていない。
- Agentが判断できる具体的な指示になっている。
- 既存の進行中Changeへの影響が説明されている。
- サンプルChangeで生成結果を確認している。

## References

- [OpenSpec Customization](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md)
- [OpenSpec OPSX](https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md)
- [OpenSpec CLI](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)
- [Built-in spec-driven schema](https://github.com/Fission-AI/OpenSpec/blob/main/schemas/spec-driven/schema.yaml)
