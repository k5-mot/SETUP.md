# 🧰 Windows開発環境の拡張セットアップ

<!-- markdownlint-disable MD013 -->

この文書は任意Toolを追加する手順である。先に
[最小セットアップ](SETUP.md)を完了し、その動作確認が成功してから実行する。
すべて通常権限のPowerShellで実行し、管理者権限は使用しない。

## 1️⃣ miseを有効化する

```powershell
# このPowerShellセッションでmise管理のToolを有効化する。
(&mise activate pwsh) | Out-String | Invoke-Expression
```

## 2️⃣ 任意のAgent Skillsを導入する

```powershell
# Matt Pocock Skillsから必要なSkillを導入する。
npx skills@latest add mattpocock/skills --agent universal --yes ask-matt code-review codebase-design diagnosing-bugs domain-modeling grill-me grill-with-docs grilling handoff implement improve-codebase-architecture prototype research resolving-merge-conflicts setup-matt-pocock-skills tdd teach to-questionnaire to-spec to-tickets triage wait-what wayfinder wizard writing-great-skills

# GraphifyのCLIをUser環境へ導入する。
uv tool install graphifyy

# GraphifyのAgent SkillをProjectへ導入する。
graphify agents install --project

# Browser操作用CLIをUser環境へ導入する。
npm install --global agent-browser

# Browser操作用Runtimeを導入する。
npx agent-browser install
```

`.agents/skills/.gitignore`により、本Repository固有の4 Skill以外はGit管理
対象外になる。追加Skillは各開発者のLocal環境で利用する。

## 3️⃣ 言語・Framework別Skillを導入する

必要なものだけを選択する。

```powershell
# React向けSkillを導入する。
npx skills@latest add vercel-labs/agent-skills --agent universal --yes react-best-practices

# Python向けSkillを導入する。
npx skills@latest add trailofbits/skills --agent universal --yes modern-python codeql insecure-defaults

# JavaとSpring Boot向けSkillを導入する。
npx skills@latest add github/awesome-copilot --agent universal --yes java-springboot spring-boot-testing

# 簡潔な実装とReview向けSkillを導入する。
npx skills@latest add DietrichGebert/ponytail --agent universal --yes ponytail ponytail-review ponytail-audit
```

## 4️⃣ craneを導入する

```powershell
# User専用の実行ファイル配置先を作成する。
$UserBinPath = Join-Path ([Environment]::GetFolderPath('UserProfile')) '.local\bin'
New-Item -ItemType Directory -Force -Path $UserBinPath | Out-Null

# craneのArchiveを一時領域へDownloadする。
$CraneArchivePath = Join-Path ([IO.Path]::GetTempPath()) 'crane.tar.gz'
Invoke-WebRequest `
  'https://github.com/google/go-containerregistry/releases/latest/download/go-containerregistry_Windows_x86_64.tar.gz' `
  -OutFile $CraneArchivePath

# craneだけをUser専用の配置先へ展開する。
tar.exe -xf $CraneArchivePath -C $UserBinPath crane.exe

# 展開後に一時Archiveを削除する。
Remove-Item -LiteralPath $CraneArchivePath
```

期待結果は、選択したCLIのVersion Commandが通常権限で成功することである。
失敗した場合は最小セットアップへ戻り、miseの有効化とPATHを確認する。

<!-- markdownlint-enable MD013 -->

## References

- [Agent Skills](https://agentskills.io/home)
- [Graphify](https://github.com/Graphify-Labs/graphify)
- [agent-browser](https://github.com/vercel-labs/agent-browser)
- [crane](https://github.com/google/go-containerregistry/tree/main/cmd/crane)
