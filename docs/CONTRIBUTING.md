# 🤝 Contributing Guideline

本書は、人間のContributorが従う開発フローの基本ルールを一箇所に定めるSingle Source of Truth（SSoT）である。

## 📏 ルール記述ルール

ルールにはRFC 2119およびRFC 8174に対応する日本語を使い、対応する英語キーワードを大文字で併記することを必須（MUST）とする。

| 日本語 | キーワード | 意味 |
| --- | --- | --- |
| 必須 | `MUST` | 例外なく実施する |
| 禁止 | `MUST NOT` | 実施しない |
| 推奨 | `SHOULD` | 原則として実施する |
| 非推奨 | `SHOULD NOT` | 原則として実施しない |
| 任意 | `MAY` | 状況に応じて選択できる |

## 📝 Gitコミットルール

Commit MessageはConventional Commitsとgitmojiを組み合わせ、日本語で記述することを必須（MUST）とする。

```text
<gitmoji> <type>[optional scope][!]: <変更内容>

<変更理由>
```

- Subjectには変更内容、Bodyには変更理由を書くことを必須（MUST）とする。
- 一つのCommitには一つの論理変更だけを含めることを必須（MUST）とする。
- `feat`、`fix`、`docs`など、変更目的に合うTypeを使うことを必須（MUST）とする。
- Breaking Changeは`!`または`BREAKING CHANGE:`で示すことを必須（MUST）とする。
- Commit Messageの作成には`git-cz`を使うことを推奨（SHOULD）する。

```text
📝 docs(git): Commit規則を簡潔化

人間向けの基本ルールへ責務を限定するため。
```

## 🌿 Gitブランチ戦略

GitHub Flowを採用することを必須（MUST）とする。

```text
main ← Pull Request ← short-lived branch
```

- 最新の`main`から目的単位の短命Branchを作ることを必須（MUST）とする。
- Pull RequestでReviewとCIを完了してから`main`へMergeすることを必須（MUST）とする。
- Merge後は作業Branchを削除することを推奨（SHOULD）する。

次の戦略は採用しない。

- Trunk-Based Development: GitHub Flowと共通点はあるが、Pull Requestの作成、Review、Mergeを明示するGitHub Flowを運用名称として統一するため。
- GitLab Flow: 環境BranchやRelease Branchを常設する要件がなく、運用を増やさないため。
- Git Flow: `develop`、Release、Hotfixの長寿命BranchとMerge-backが不要なため。

## 🏷️ Gitリリースルール

ReleaseはSemantic Versioning 2.0.0に従い、`v<MAJOR>.<MINOR>.<PATCH>`形式のGit Tagを付けることを必須（MUST）とする。

| 変更 | Version |
| --- | --- |
| 後方互換性を壊す変更 | `MAJOR` |
| 後方互換な機能追加 | `MINOR` |
| 後方互換な不具合修正 | `PATCH` |

- Release対象を`main`へMergeし、必要なCIを完了してからTagを作ることを必須（MUST）とする。
- 公開済みTagの移動、削除、同名での再利用を禁止（MUST NOT）する。
- Release後の修正は、新しいVersionとして公開することを必須（MUST）とする。

## 📚 参考資料

- [RFC 2119](https://www.rfc-editor.org/info/rfc2119)
- [RFC 8174](https://www.rfc-editor.org/info/rfc8174)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [gitmoji Specification](https://gitmoji.dev/specification)
- [git-cz](https://github.com/streamich/git-cz)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [GitLab Flow](https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Semantic Versioning 2.0.0](https://semver.org/)
