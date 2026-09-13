
# Gitコミットメッセージの設計ルール

## 目的

Commit Messageを、変更したFileの列挙ではなく、履歴から**何を、なぜ変更したか**を復元するための記録として運用する。人間によるReview、Revert、Release Note生成、Coding Agentによる履歴理解に共通して使える形式を定める。

## 規範語

本文の`MUST`、`MUST NOT`、`SHOULD`、`SHOULD NOT`、`MAY`は、すべて大文字で書かれた場合に限り、[BCP 14（RFC 2119 / RFC 8174）](https://www.rfc-editor.org/rfc/rfc8174)の意味を持つ。小文字の表現には規範的な意味を持たせない。

| 規範語 | この文書での意味 |
| --- | --- |
| `MUST` | 必須。例外なく満たす必要がある。 |
| `MUST NOT` | 禁止。実施してはならない。 |
| `SHOULD` | 原則として従う。外す場合は影響を理解し、理由を説明できる必要がある。 |
| `SHOULD NOT` | 原則として避ける。採用する場合は影響を理解し、理由を説明できる必要がある。 |
| `MAY` | 任意。Projectの事情に応じて採用できる。 |

## Source of Truth

- RepositoryはCommit規約を`CONTRIBUTING.md`または同等のFileに記録しなければならない（`MUST`）。
- Repository固有規約は本Knowledgeの既定値を上書きしてよい（`MAY`）。
- 上書きする場合、言語、Message形式、許可するType、Subject長、Commit作成Toolを明示しなければならない（`MUST`）。
- 規約とcommitlint、`git-cz`などの自動検証設定を矛盾させてはならない（`MUST NOT`）。

## 基本形式

既定形式は、gitmoji付きConventional Commitsとする。

```text
<gitmoji> <type>[optional scope][!]: <日本語のsubject>

[optional body]

[optional footer(s)]
```

例:

```text
🐛 fix(sync): 一時的な失敗時にアップロードを再試行

単発の503応答で同期全体が停止していた。
冪等なアップロードだけを指数Backoffで再試行する。

Refs: #184
```

### Format Requirements

- Commit MessageはRepositoryで定めた形式に従わなければならない（`MUST`）。
- 本文書の既定Profileを採用するRepositoryでは、日本語で書かなければならない（`MUST`）。
- 本文書の既定Profileでは、gitmoji付きConventional Commits形式を使わなければならない（`MUST`）。
- Subjectは変更対象と結果を一行で表さなければならない（`MUST`）。
- Subjectは50文字以内に収めなければならない（`MUST`）。
- Subjectを句点で終えてはならない（`MUST NOT`）。
- `update`、`fix stuff`、`misc`など、対象と結果を特定できないSubjectを使ってはならない（`MUST NOT`）。
- Scopeは変更対象を短く特定できる場合に付けてよい（`MAY`）。

```text
悪い: update files
悪い: fix bug
良い: 🐛 fix(auth): 期限切れRefresh Tokenを拒否
良い: 📝 docs(api): Rate Limit応答Headerを記載
```

## Type

| Type | 用途 |
| --- | --- |
| `feat` | 利用者に見える機能追加 |
| `fix` | 不具合修正 |
| `docs` | Documentationだけの変更 |
| `refactor` | 外部挙動を変えない構造改善 |
| `test` | Testの追加・修正 |
| `build` | Build SystemやDependencyの変更 |
| `ci` | CI/CD設定の変更 |
| `perf` | 性能改善 |
| `chore` | 他Typeに該当しない保守作業 |
| `revert` | 既存Commitの取消し |

- Repositoryは使用可能なTypeを限定すべきである（`SHOULD`）。
- 同じ意味を持つProject固有Typeを無計画に追加すべきではない（`SHOULD NOT`）。
- Type、gitmoji、Scope候補、Message Formatは`.git-cz.json`などの設定で管理すべきである（`SHOULD`）。
- Commit作成には、Repositoryで設定された`git-cz`などの支援Toolを使うべきである（`SHOULD`）。

## BodyとFooter

- Subjectだけで変更理由を説明できない場合、Bodyを追加すべきである（`SHOULD`）。
- BodyはDiffから自明な処理の繰返しではなく、変更前の問題、判断理由、Trade-off、互換性、Test結果を記録すべきである（`SHOULD`）。
- Breaking Changeは`!`または`BREAKING CHANGE:` Footerで明示しなければならない（`MUST`）。
- 関連Issueは`Refs:`または`Fixes:`で追跡してよい（`MAY`）。
- Secret、Token、個人情報、非公開Credential、機密URLをCommit Messageへ含めてはならない（`MUST NOT`）。

```text
✨ feat(api)!: Legacy Token Endpointを削除

BREAKING CHANGE: Clientは/oauth/tokenを使用する必要がある。
```

## Commitの粒度

- 一つのCommitは一つの論理変更だけを含まなければならない（`MUST`）。
- Commitは単独で理解・Review・Revertできなければならない（`MUST`）。
- 原則として各CommitでBuildとTestが成功する状態を保たなければならない（`MUST`）。
- 無関係な変更を同じCommitへ含めてはならない（`MUST NOT`）。
- Refactorと外部挙動の変更は別Commitにしなければならない（`MUST`）。
- 自動Formatや一括Renameは、意味のある挙動変更と分けるべきである（`SHOULD`）。
- 対応する実装とTestは、同じ論理変更である場合に同じCommitへ含めてよい（`MAY`）。
- 同じ作業で発生した軽微な修正を、意味のない独立Commitへ分割してはならない（`MUST NOT`）。

## Coding Agent Requirements

- Coding AgentはCommit前に`git diff`、Test結果、生成物、Secret混入を確認しなければならない（`MUST`）。
- Coding AgentはTaskまたは独立したSubtaskの完了単位でCommitしなければならない（`MUST`）。
- Coding Agentは明示的な依頼なしにWork in ProgressをCommitしてはならない（`MUST NOT`）。
- Coding Agentは既存のUser変更を自分のCommitへ混入させてはならない（`MUST NOT`）。
- Coding AgentはCommit規約が不明な場合、既存履歴と`CONTRIBUTING.md`を確認すべきである（`SHOULD`）。
- Coding AgentはCommit作成前に、提案するMessageをUserへ提示してよい（`MAY`）。

## Merge時の扱い

- Squash Mergeを使うRepositoryは、Pull Request TitleをCommit規約へ適合させなければならない（`MUST`）。
- Rebase Mergeを使うRepositoryは、各Commitを完成した論理変更として整えるべきである（`SHOULD`）。
- Merge方式はRepository内で統一し、例外条件を文書化すべきである（`SHOULD`）。

## Checklist

- [ ] `MUST`: Repository固有規約とMessage形式が一致している
- [ ] `MUST`: Subjectから対象と変更結果を判断できる
- [ ] `MUST`: Subjectが50文字以内で、句点で終わっていない
- [ ] `MUST`: 一つのCommitが一つの論理変更になっている
- [ ] `SHOULD`: 理由やTrade-offをBodyへ記録した
- [ ] `MUST`: Breaking Changeを明示した
- [ ] `MUST NOT`: Secretや個人情報を含めていない
- [ ] `MUST`: Build、Test、Commit Lintを通過した

## Related

- [[40_Knowledges/開発プロセス/Gitブランチ戦略の選び方]]
- [[40_Knowledges/開発プロセス/Gitタグとリリースバージョンの運用ルール]]
- [[30_Projects/dotfiles/仕様/2026年度版Windows開発環境セットアップ手順|2026年度版Windows開発環境セットアップ手順]]

## References

- [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [dotfiles CONTRIBUTING.md](https://github.com/k5-mot/dotfiles/blob/main/CONTRIBUTING.md)
- [git-commit Documentation](https://git-scm.com/docs/git-commit)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)




# Gitタグとリリースバージョンの運用ルール

## 目的

Git Tagを、Release、Artifact、Container Image、Deployment、障害報告を同じCommitへ結び付ける不変の識別子として運用する。Branchは移動する参照として扱い、公開済みRelease Tagは移動させない。

## 規範語

本文の`MUST`、`MUST NOT`、`SHOULD`、`SHOULD NOT`、`MAY`は、すべて大文字で書かれた場合に限り、[BCP 14（RFC 2119 / RFC 8174）](https://www.rfc-editor.org/rfc/rfc8174)の意味を持つ。小文字の表現には規範的な意味を持たせない。

| 規範語 | この文書での意味 |
| --- | --- |
| `MUST` | 必須。例外なく満たす必要がある。 |
| `MUST NOT` | 禁止。実施してはならない。 |
| `SHOULD` | 原則として従う。外す場合は影響と理由を説明できる必要がある。 |
| `SHOULD NOT` | 原則として避ける。採用する場合は影響と理由を説明できる必要がある。 |
| `MAY` | 任意。Projectの事情に応じて採用できる。 |

## Source of Truth

- RepositoryはVersioning方式、Tag形式、Release手順を`CONTRIBUTING.md`または同等のFileに記録しなければならない（`MUST`）。
- 公開APIまたは互換性契約を持つProjectはSemantic Versioning 2.0.0に従わなければならない（`MUST`）。
- Semantic Versioningを使わないProjectは、採用するRelease番号体系と比較規則を文書化しなければならない（`MUST`）。
- CI設定、Release手順、Documentationで異なるTag形式を使ってはならない（`MUST NOT`）。

## Tag形式

既定のRelease Tagは次の形式でなければならない（`MUST`）。

```text
v<MAJOR>.<MINOR>.<PATCH>
```

```text
正しい: v1.4.2
誤り:   1.4.2
誤り:   release-1.4.2
誤り:   v1.4.2-alpha.1
誤り:   v1.4.2+build.184
```

- Tag名は先頭に`v`を付けなければならない（`MUST`）。
- `<MAJOR>.<MINOR>.<PATCH>`はSemantic Versioningに従わなければならない（`MUST`）。
- 本文書の既定ProfileではPre-release Tagを作成してはならない（`MUST NOT`）。
- 本文書の既定ProfileではBuild Metadata付きTagを作成してはならない（`MUST NOT`）。
- Pre-releaseやBuild Metadataが必要なProjectは、既定Profileからの逸脱として形式、用途、昇格方法を明示してよい（`MAY`）。
- 同じRepositoryで複数のTag形式を無計画に混在させてはならない（`MUST NOT`）。

## Semantic Versioningの判断

| 変更 | Version Requirement |
| --- | --- |
| 後方互換性を壊す変更 | `MAJOR`を増やさなければならない（`MUST`） |
| 後方互換な機能追加 | `MINOR`を増やさなければならない（`MUST`） |
| 後方互換なBug Fix | `PATCH`を増やさなければならない（`MUST`） |
| Documentation・運用改善だけのRelease | 既定Profileでは`PATCH`を増やさなければならない（`MUST`） |

- Versionを決める前に、前回Release以降のBreaking Change、Feature、Fixを分類しなければならない（`MUST`）。
- 最も大きい互換性影響に合わせてVersionを決めなければならない（`MUST`）。
- 互換性を壊す変更を`PATCH`または`MINOR`として公開してはならない（`MUST NOT`）。
- `0.y.z`を使う場合、Public APIが不安定であることを利用者へ明示しなければならない（`MUST`）。
- Public APIを定義しない内部Applicationは、Calendar Versioningや連番を採用してよい（`MAY`）。

## Annotated Tagと署名

- 正式ReleaseにはAnnotated Tagを使わなければならない（`MUST`）。
- Lightweight Tagを正式Releaseへ使ってはならない（`MUST NOT`）。
- Supply Chain上の検証が必要なReleaseは署名付きTagを使うべきである（`SHOULD`）。
- Tag MessageはRelease Versionを識別できなければならない（`MUST`）。

```bash
git tag -a v1.4.2 -m "v1.4.2"
git push origin v1.4.2
```

署名する場合:

```bash
git tag -s v1.4.2 -m "v1.4.2"
git tag -v v1.4.2
git push origin v1.4.2
```

## Release手順

1. 対象Commitは保護されたDefault Branchへ統合済みでなければならない（`MUST`）。
2. Required CI、Test、Security Scanを完了しなければならない（`MUST`）。
3. 前回Releaseとの差分からVersionを決めなければならない（`MUST`）。
4. Changelog、Migration情報、Release Noteを確定しなければならない（`MUST`）。
5. 対象CommitへAnnotated TagまたはSigned Tagを作らなければならない（`MUST`）。
6. TagをRemoteへPushする前に、対象CommitとTag Messageを確認しなければならない（`MUST`）。
7. Release ArtifactはTagが指すCommitからBuildしなければならない（`MUST`）。
8. Artifact、Container Image、SBOM、DeploymentへGit SHAとTagを記録すべきである（`SHOULD`）。
9. 公開後にArtifactとTagの対応を検証しなければならない（`MUST`）。

## Tagの不変性

- 公開済みTagを別Commitへ移動してはならない（`MUST NOT`）。
- 公開済みTagを削除して同じ名前で再利用してはならない（`MUST NOT`）。
- Releaseに誤りがあった場合、新しいVersionを発行しなければならない（`MUST`）。
- 公開前の誤Tagを削除する場合も、Remote Push済みか確認しなければならない（`MUST`）。
- 公開済みTagの削除が避けられない場合、影響範囲、理由、代替Versionを告知しなければならない（`MUST`）。

```text
禁止: v1.4.2を別Commitへ付け替える
必須: 修正版をv1.4.3として公開する
```

## Monorepo

- Repository全体を同時Releaseする場合、通常の`v<MAJOR>.<MINOR>.<PATCH>`を使わなければならない（`MUST`）。
- Componentごとに独立Versionを持つ場合、Component名をTagへ含めてよい（`MAY`）。
- Component Prefixの形式はRepository内で統一しなければならない（`MUST`）。
- Repository全体VersionとComponent別Versionを無計画に混在させてはならない（`MUST NOT`）。

```text
api/v2.3.0
worker/v1.8.1
```

## Coding Agent Requirements

- Coding AgentはUserから明示的に依頼されない限り、Tagを作成またはPushしてはならない（`MUST NOT`）。
- Coding AgentはTag作成前にVersion根拠、対象Commit SHA、CI結果を提示しなければならない（`MUST`）。
- Coding Agentは既存Tagの移動、削除、Force Pushを実行してはならない（`MUST NOT`）。
- Coding AgentはRelease Noteを前回Tagとの差分から生成すべきである（`SHOULD`）。
- Coding AgentはVersion判断に不確実性がある場合、Tagを作らずUserへ確認しなければならない（`MUST`）。
- Coding AgentはDry RunまたはLocal Tag作成までを提案してよい（`MAY`）。

## Checklist

- [ ] `MUST`: Versioning方式とTag形式がRepositoryに記録されている
- [ ] `MUST`: Version変更が互換性影響と一致している
- [ ] `MUST`: Tagが`v<MAJOR>.<MINOR>.<PATCH>`形式である
- [ ] `MUST NOT`: Pre-releaseまたはBuild Metadataを使っていない
- [ ] `MUST`: 正式ReleaseにAnnotatedまたはSigned Tagを使った
- [ ] `MUST`: Tag対象CommitとRequired CIを確認した
- [ ] `MUST`: ChangelogとMigration情報を公開した
- [ ] `MUST NOT`: 同じTagを移動・再利用していない
- [ ] `SHOULD`: ArtifactへGit SHAとTagを記録した

## Related

- [[40_Knowledges/開発プロセス/Gitコミットメッセージの設計ルール]]
- [[40_Knowledges/開発プロセス/Gitブランチ戦略の選び方]]
- [[30_Projects/dotfiles/仕様/2026年度版Windows開発環境セットアップ手順|2026年度版Windows開発環境セットアップ手順]]

## References

- [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [dotfiles CONTRIBUTING.md](https://github.com/k5-mot/dotfiles/blob/main/CONTRIBUTING.md)
- [git-tag Documentation](https://git-scm.com/docs/git-tag)
- [Semantic Versioning 2.0.0](https://semver.org/)

# Gitブランチ戦略の選び方

## 結論

継続的に統合・配布する通常のSoftware Projectは、保護された`main`と短命な作業BranchからなるGitHub Flowを既定とする。Release Branchなどの長寿命Branchは、複数Versionの並行保守や独立したRelease工程が必要な場合だけ導入する。

## 規範語

本文の`MUST`、`MUST NOT`、`SHOULD`、`SHOULD NOT`、`MAY`は、すべて大文字で書かれた場合に限り、[BCP 14（RFC 2119 / RFC 8174）](https://www.rfc-editor.org/rfc/rfc8174)の意味を持つ。小文字の表現には規範的な意味を持たせない。

| 規範語 | この文書での意味 |
| --- | --- |
| `MUST` | 必須。例外なく満たす必要がある。 |
| `MUST NOT` | 禁止。実施してはならない。 |
| `SHOULD` | 原則として従う。外す場合は影響と理由を説明できる必要がある。 |
| `SHOULD NOT` | 原則として避ける。採用する場合は影響と理由を説明できる必要がある。 |
| `MAY` | 任意。Projectの事情に応じて採用できる。 |

## Source of Truth

- Repositoryは採用するBranch戦略を`CONTRIBUTING.md`または同等のFileに記録しなければならない（`MUST`）。
- 特段の理由がないRepositoryはGitHub Flowを採用しなければならない（`MUST`）。
- 異なる戦略を採用するRepositoryは、その理由、Branchの役割、Merge条件、廃止条件を記録しなければならない（`MUST`）。
- 慣習だけを理由に長寿命Branchを追加してはならない（`MUST NOT`）。

## 既定Flow

```text
main
  └─ short-lived branch
       ├─ commits
       ├─ pull request
       ├─ review / CI
       └─ merge → main → deploy / release
```

1. 作業者は最新の`main`から一つの変更目的に対応するBranchを作らなければならない（`MUST`）。
2. 作業Branchは短命に保つべきである（`SHOULD`）。
3. Pull Requestは一つの目的だけを扱うべきである（`SHOULD`）。
4. 作業者は早い段階でDraft Pull Requestを作ってContextを共有してよい（`MAY`）。
5. Merge前にRequired CIを通過させなければならない（`MUST`）。
6. Required Reviewが設定されている場合、それを省略してはならない（`MUST NOT`）。
7. Merge後の作業Branchは削除すべきである（`SHOULD`）。

## `main`の要件

- `main`は常にRelease可能な状態に保たなければならない（`MUST`）。
- `main`を破壊する既知の変更を直接Pushしてはならない（`MUST NOT`）。
- 通常の変更はPull Request経由で統合しなければならない（`MUST`）。
- Required Status Checksを設定しなければならない（`MUST`）。
- Force PushとBranch削除を禁止しなければならない（`MUST`）。
- 必要なReview数、CODEOWNERS、署名検証を設定してよい（`MAY`）。
- 緊急Bypass権限は最小化すべきである（`SHOULD`）。
- Bypassを使用した場合、理由と事後Reviewを記録しなければならない（`MUST`）。

## Branch命名

```text
feat/setup-uri-import
fix/184-sync-timeout
docs/recovery-runbook
refactor/chunk-store
release/2.4
hotfix/token-validation
```

- Branch名は変更の種類、対象、目的を識別できなければならない（`MUST`）。
- lowercaseとhyphenを使うべきである（`SHOULD`）。
- Issue IDを含めてよいが、説明語を省略すべきではない（`MAY`、`SHOULD NOT`）。
- 個人名だけ、`work`、`misc`、`test`などの目的不明な名前を使ってはならない（`MUST NOT`）。
- Secret、顧客名、機密Issue名をBranch名へ含めてはならない（`MUST NOT`）。

## Branchを短命に保つ

- 大きな機能は、Review可能な縦に薄い変更へ分割すべきである（`SHOULD`）。
- 未完成機能を安全に統合するため、Feature FlagやBackward-compatible Migrationを利用してよい（`MAY`）。
- 長期Branchや環境別Branchを作るべきではない（`SHOULD NOT`）。
- Branchの寿命を日数だけで判定してはならない（`MUST NOT`）。
- `main`との差分量、Review待ち時間、Conflict頻度、変更Domain数、Rollback可能性を監視すべきである（`SHOULD`）。

## Merge方式

| 方式 | 採用条件 |
| --- | --- |
| Squash Merge | Branch全体を一つの論理変更として残す場合 |
| Rebase Merge | 各Commitが完成した意味単位として整っている場合 |
| Merge Commit | 統合点とBranch構造を履歴へ残す必要がある場合 |

- Repositoryは既定のMerge方式を一つ定めるべきである（`SHOULD`）。
- Squash MergeではPull Request TitleをCommit Message規約へ適合させなければならない（`MUST`）。
- Rebase Mergeでは各Commitを独立してBuild・Test・Revert可能にすべきである（`SHOULD`）。
- 履歴を複雑にする必要がない場合、Merge Commitを無計画に増やすべきではない（`SHOULD NOT`）。

## Release Branch

Release Branchは次のいずれかを満たす場合に作成してよい（`MAY`）。

- 複数のRelease系列を同時保守する。
- Release Candidateの安定化中も次期開発を続ける。
- 審査や認証のためRelease対象Commitを固定する。

導入後は次を守る。

- Release Branchの対象Versionと保守期限を記録しなければならない（`MUST`）。
- Release Branchへ新機能を追加すべきではない（`SHOULD NOT`）。
- Bug Fixは`main`と必要な保守Branchへ反映しなければならない（`MUST`）。
- Cherry-pickの反映状況をIssueまたはPull Requestで追跡しなければならない（`MUST`）。
- 保守終了後のRelease Branchは削除またはRead-only化すべきである（`SHOULD`）。

## Hotfix

1. Productionに対応するTagまたは保守Branchから作らなければならない（`MUST`）。
2. 修正を最小化し、Regression Testを追加しなければならない（`MUST`）。
3. 緊急時でもReviewと必須CIを省略してはならない（`MUST NOT`）。
4. 修正版には新しいTagを発行しなければならない（`MUST`）。
5. 修正を`main`と必要なRelease Branchへ反映しなければならない（`MUST`）。

## Coding Agent Requirements

- Coding Agentは一つのTaskに一つのBranchを使わなければならない（`MUST`）。
- Coding Agentは作業開始前に`main`との差分、`CONTRIBUTING.md`、Projectの`_index.md`を確認しなければならない（`MUST`）。
- Coding Agentは無関係なFormat、Rename、Dependency更新を混在させてはならない（`MUST NOT`）。
- Coding Agentは既存のUser変更を上書き、Reset、別Branchへ移動してはならない（`MUST NOT`）。
- Branch名はAgent名ではなく変更目的を表さなければならない（`MUST`）。
- 大きなTaskでは、独立してMerge可能なSubtaskへ分割すべきである（`SHOULD`）。

## Checklist

- [ ] `MUST`: 採用戦略と例外条件がRepositoryに記録されている
- [ ] `MUST`: Branchが一つの変更目的に限定されている
- [ ] `SHOULD`: Branchが短命でReview可能な大きさである
- [ ] `MUST`: Required ChecksとRequired Reviewを通過した
- [ ] `MUST`: `main`がRelease可能な状態である
- [ ] `SHOULD`: Merge後に作業Branchを削除した
- [ ] `MUST`: Release / Hotfixの修正を`main`へ反映した
- [ ] `MUST`: 長寿命Branchの必要性と廃止条件が記録されている

## Related

- [[40_Knowledges/開発プロセス/Gitコミットメッセージの設計ルール]]
- [[40_Knowledges/開発プロセス/Gitタグとリリースバージョンの運用ルール]]
- [[30_Projects/dotfiles/仕様/2026年度版Windows開発環境セットアップ手順|2026年度版Windows開発環境セットアップ手順]]

## References

- [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
- [dotfiles CONTRIBUTING.md](https://github.com/k5-mot/dotfiles/blob/main/CONTRIBUTING.md)
- [git-branch Documentation](https://git-scm.com/docs/git-branch)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
