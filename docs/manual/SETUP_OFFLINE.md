<!-- markdownlint-disable MD013 MD033 -->

# 🔒 Windows閉域環境セットアップ 2026年度版

## 📝 概要

インターネットに接続できない閉域環境において、
Windows 11上に、PowerShell 7、VSCode、Python/Node.js、コーディングエージェント、OpenSpecなどの開発環境を構築する手順書である。
開域側のWindows PCで資材をダウンロードしてzipにまとめ、外部媒体などで閉域側のWindows PCへ搬入してからインストールする。

資材は以下の構成のzip（`offline-dist-<日付>.zip`）にまとめる。

```text
offline-dist/
├─ tools/                  # Git、PowerShell、VSCode、Python、Node.js、uv、jq、Pandoc、ripgrep、crane
├─ npm/                    # npmキャッシュとnpmパッケージ一覧
├─ pip/                    # wheelとpipパッケージ一覧
├─ vsix/                   # VSIXとインストール順序
└─ skills/                 # Agent Skillsのリポジトリと導入するSkill一覧
```

## 📑 目次

- [📝 概要](#-概要)
- [✅ 前提条件](#-前提条件)
- [0. 開域側PCで資材をダウンロードする](#0-開域側pcで資材をダウンロードする)
  - [0-1 開発ツールをダウンロードする](#-0-1-開発ツールをダウンロードする)
  - [0-2 npmパッケージをダウンロードする](#-0-2-npmパッケージをダウンロードする)
  - [0-3 pipパッケージをダウンロードする](#-0-3-pipパッケージをダウンロードする)
  - [0-4 VSCode拡張機能をダウンロードする](#-0-4-vscode拡張機能をダウンロードする)
  - [0-5 資材をzipにまとめて搬出する](#-0-5-資材をzipにまとめて搬出する)
- [1. テレメトリーを無効化する](#1-テレメトリーを無効化する)
- [2. 資材を展開する](#2-資材を展開する)
- [3. 開発ツールをインストールする](#3-開発ツールをインストールする)
- [4. craneをインストールする](#4-craneをインストールする)
- [5. Python/Node.jsをインストールする](#5-pythonnodejsをインストールする)
- [6. npmパッケージをインストール](#6-npmパッケージをインストール)
- [7. pipパッケージをインストール](#7-pipパッケージをインストール)
- [8. VSCode 拡張機能をインストールする](#8-vscode-拡張機能をインストールする)
- [9. VSCode の設定を追加する](#9-vscode-の設定を追加する)
- [10. コーディングエージェントにローカルLLMを設定する](#10-コーディングエージェントにローカルllmを設定する)
- [11. 重複したPATHを除去](#11-重複したpathを除去)
- [12. 動作確認](#12-動作確認)
- [13. OpenSpecをプロジェクトに導入](#13-openspecをプロジェクトに導入)
- [14. 有用なAgent Skillsをインストール](#14-有用なagent-skillsをインストール)
- [🔖 参考文献](#-参考文献)

## ✅ 前提条件

- 開域側PC: インターネットに接続でき、[SETUP.md](SETUP.md)の環境が構築済みのWindows（x64）PCであること
- 閉域側PC: 開域側PCと同じアーキテクチャ（Windows x64）のPCであること
- 両PCとも、一般ユーザ権限のPowerShellで実行できること（管理者権限は不要）
- 両PCとも、`tar`コマンドが利用できること（Windows 10 1803以降は標準で利用できる）
- 資材zipを、組織の持ち込み規程に従って外部媒体などで搬入できること
- ローカルLLMを使う場合は、閉域内でOpenAI互換APIを提供するLLMサーバ（vLLMなど）が起動していること

## 0. 開域側PCで資材をダウンロードする

0-1から0-5までは、**同一のPowerShellセッション**で順に実行する。
途中でセッションを閉じた場合は、0-1から再実行する。

### 0-1 開発ツールをダウンロードする

共通設定を行い、SETUP.mdの2.でwingetからインストールしているツール、Git、crane、Python/Node.jsの配布物をダウンロードする。
閉域側でユーザインストールするため、Pythonはpython.orgのインストーラを、Node.jsはnodejs.orgのzipをダウンロードする（Node.jsのMSIは管理者権限が必要なため）。
Git、Pandoc、Pythonのインストーラは配布元がチェックサムファイルを公開していないため、HTTPSでのダウンロードのみとする。それ以外は配布元のチェックサムで検証する。
0-2、0-3では、SETUP.mdで構築済みの`npm`と`python`を使う。

```powershell
# 1. エラー時に中断し、Windows PowerShell 5.1でのダウンロード速度低下とTLSエラーを防ぐ
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# 2. 資材の出力先と作業ディレクトリを設定
$Dist = Join-Path $env:TEMP "offline-dist"
$Work = Join-Path $env:TEMP "offline-dist-work"
$ToolsDir = Join-Path $Dist "tools"
$NpmDir = Join-Path $Dist "npm"
$PipDir = Join-Path $Dist "pip"
$VsixDir = Join-Path $Dist "vsix"
$SkillsDir = Join-Path $Dist "skills"

# 3. ディレクトリを作成
foreach ($Dir in @($Dist, $Work, $ToolsDir, $NpmDir, $PipDir, $VsixDir, $SkillsDir)) {
    New-Item -ItemType Directory -Path $Dir -Force | Out-Null
}

# 4. GitHub APIを使わず、releases/latest のリダイレクト先から最新タグを取得する関数
function Get-GitHubLatestTag {
    param([Parameter(Mandatory)][string]$Repo)
    $Request = [Net.HttpWebRequest]::Create("https://github.com/$Repo/releases/latest")
    $Request.Method = "HEAD"
    $Request.AllowAutoRedirect = $false
    $Response = $Request.GetResponse()
    try {
        $Location = $Response.Headers["Location"]
    }
    finally {
        $Response.Close()
    }
    if (-not $Location) {
        throw "Failed to resolve latest release: $Repo"
    }
    ($Location -split '/')[-1]
}

# 5. ダウンロードしたファイルを配布元のチェックサムファイルで検証する関数
function Test-FileChecksum {
    param(
        [Parameter(Mandatory)][string]$File,
        [Parameter(Mandatory)][string]$ChecksumUrl
    )
    $SumFile = Join-Path $Work ([IO.Path]::GetRandomFileName())
    Invoke-WebRequest -Uri $ChecksumUrl -OutFile $SumFile -UseBasicParsing
    $FileName = Split-Path $File -Leaf
    $Lines = @(Get-Content -LiteralPath $SumFile | Where-Object { $_ -match '[0-9a-fA-F]{64}' })
    Remove-Item -LiteralPath $SumFile -Force

    # 「<hash>  <file>」形式はファイル名で、ハッシュ単体の形式はその1行で照合する。
    $Line = $Lines | Where-Object { $_ -match "(^|[\s*/])$([regex]::Escape($FileName))\s*$" } | Select-Object -First 1
    if (-not $Line -and $Lines.Count -eq 1) {
        $Line = $Lines[0]
    }
    if (-not $Line) {
        throw "Checksum entry not found: $FileName"
    }
    $Expected = [regex]::Match($Line, '[0-9a-fA-F]{64}').Value.ToUpperInvariant()
    $Actual = (Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash
    if ($Actual -ne $Expected) {
        throw "SHA256 mismatch: $FileName"
    }
    Write-Host "Verified: $FileName"
}

# 6. GitHub Releasesから資材をダウンロードし、チェックサムがあれば検証する関数
function Save-GitHubReleaseAsset {
    param(
        [Parameter(Mandatory)][string]$Repo,
        [Parameter(Mandatory)][string]$Tag,
        [Parameter(Mandatory)][string]$FileName,
        [string]$ChecksumFile
    )
    $BaseUrl = "https://github.com/$Repo/releases/download/$Tag"
    $OutFile = Join-Path $ToolsDir $FileName
    Invoke-WebRequest -Uri "$BaseUrl/$FileName" -OutFile $OutFile -UseBasicParsing
    Write-Host "Downloaded: $Repo $Tag $FileName"
    if ($ChecksumFile) {
        Test-FileChecksum -File $OutFile -ChecksumUrl "$BaseUrl/$ChecksumFile"
    }
}

# 7. GitHub Releasesで配布されているツールを列挙（タグからファイル名とチェックサムファイル名を決める）
$Assets = @(
    @{
        Repo     = 'git-for-windows/git'
        File     = { param($Tag)
            # v2.x.y.windows.1 は Git-2.x.y-64-bit.exe、windows.N（N>1）は Git-2.x.y.N-64-bit.exe になる。
            if ($Tag -notmatch '^v(?<Version>[\d.]+)\.windows\.(?<Rev>\d+)$') { throw "Unexpected tag: $Tag" }
            $Version = if ($Matches.Rev -eq '1') { $Matches.Version } else { "$($Matches.Version).$($Matches.Rev)" }
            "Git-$Version-64-bit.exe"
        }
        Checksum = { param($Tag, $File) $null }
    }
    @{
        Repo     = 'PowerShell/PowerShell'
        File     = { param($Tag) "PowerShell-$($Tag.TrimStart('v'))-win-x64.zip" }
        Checksum = { param($Tag, $File) 'hashes.sha256' }
    }
    @{
        Repo     = 'astral-sh/uv'
        File     = { param($Tag) 'uv-x86_64-pc-windows-msvc.zip' }
        Checksum = { param($Tag, $File) "$File.sha256" }
    }
    @{
        Repo     = 'jqlang/jq'
        File     = { param($Tag) 'jq-windows-amd64.exe' }
        Checksum = { param($Tag, $File) 'sha256sum.txt' }
    }
    @{
        Repo     = 'jgm/pandoc'
        File     = { param($Tag) "pandoc-$Tag-windows-x86_64.msi" }
        Checksum = { param($Tag, $File) $null }
    }
    @{
        Repo     = 'BurntSushi/ripgrep'
        File     = { param($Tag) "ripgrep-$Tag-x86_64-pc-windows-msvc.zip" }
        Checksum = { param($Tag, $File) "$File.sha256" }
    }
)

# 8. 最新リリースをダウンロードして検証
foreach ($Asset in $Assets) {
    $Tag = Get-GitHubLatestTag -Repo $Asset.Repo
    $File = & $Asset.File $Tag
    Save-GitHubReleaseAsset `
        -Repo $Asset.Repo `
        -Tag $Tag `
        -FileName $File `
        -ChecksumFile (& $Asset.Checksum $Tag $File)
}

# 9. VSCode（ユーザインストーラ版）をダウンロードし、更新APIが返すSHA256で検証
$VSCodeRelease = Invoke-RestMethod -Uri "https://update.code.visualstudio.com/api/update/win32-x64-user/stable/latest"
$VSCodeSetup = Join-Path $ToolsDir "VSCodeUserSetup-x64-$($VSCodeRelease.productVersion).exe"
Invoke-WebRequest -Uri $VSCodeRelease.url -OutFile $VSCodeSetup -UseBasicParsing
if ((Get-FileHash -LiteralPath $VSCodeSetup -Algorithm SHA256).Hash -ne $VSCodeRelease.sha256hash.ToUpperInvariant()) {
    throw "SHA256 mismatch: VSCode"
}
Write-Host "Verified: $(Split-Path $VSCodeSetup -Leaf)"

# 10. SETUP.mdと同じバージョンのcraneをダウンロードし、checksums.txt で検証
Save-GitHubReleaseAsset `
    -Repo "google/go-containerregistry" `
    -Tag "v0.22.1" `
    -FileName "go-containerregistry_Windows_x86_64.tar.gz" `
    -ChecksumFile "checksums.txt"

# 11. インストーラが公開されている最新の Python 3.14.x を判定し、インストーラをダウンロード
$PythonVersions = (Invoke-WebRequest -Uri "https://www.python.org/ftp/python/" -UseBasicParsing).Links.href |
    Where-Object { $_ -match '^3\.14\.\d+/$' } |
    ForEach-Object { [version]$_.TrimEnd('/') } |
    Sort-Object -Descending
$PythonVersion = $null
foreach ($Version in $PythonVersions) {
    try {
        Invoke-WebRequest -Uri "https://www.python.org/ftp/python/$Version/python-$Version-amd64.exe" -Method Head -UseBasicParsing | Out-Null
        $PythonVersion = "$Version"
        break
    }
    catch {
        # プレリリースのみのディレクトリにはインストーラがないため、次のバージョンを確認する。
    }
}
if (-not $PythonVersion) {
    throw "Python 3.14 installer not found."
}
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/$PythonVersion/python-$PythonVersion-amd64.exe" -OutFile (Join-Path $ToolsDir "python-$PythonVersion-amd64.exe") -UseBasicParsing

# 12. Node.js 24 の最新版を SHASUMS256.txt から判定し、zip をダウンロードして検証
$NodeBaseUrl = "https://nodejs.org/dist/latest-v24.x"
$NodeZipName = [regex]::Match((Invoke-WebRequest -Uri "$NodeBaseUrl/SHASUMS256.txt" -UseBasicParsing).Content, 'node-v[\d.]+-win-x64\.zip').Value
Invoke-WebRequest -Uri "$NodeBaseUrl/$NodeZipName" -OutFile (Join-Path $ToolsDir $NodeZipName) -UseBasicParsing
Test-FileChecksum -File (Join-Path $ToolsDir $NodeZipName) -ChecksumUrl "$NodeBaseUrl/SHASUMS256.txt"
```

### 0-2 npmパッケージをダウンロードする

依存パッケージを含めてnpmキャッシュへ保存し、閉域側で`npm install --offline`できるようにする。
ダウンロード時の検証（integrity）はnpmが行う。
プラットフォーム別のバイナリを含むパッケージがあるため、閉域側と同じWindows x64のPCで実行する。
14.でskills CLIから導入するAgent Skillsのリポジトリも、あわせてダウンロードする。
`agent-browser`はブラウザ本体を追加でダウンロードするため、閉域環境では対象外とする。

```powershell
# 1. 閉域側の6.でまとめてインストールする npm パッケージを列挙（skills は14.で使う）
$NpmPackages = @(
    '@opencode/cli'
    '@openai/codex'
    '@anthropic-ai/claude-code'
    '@github/copilot'
    'git-cz'
    'markdownlint-cli2'
    'pnpm'
    'typescript'
    'tsx'
    'vite-plus'
    'skills'
)

# 2. 依存パッケージごとnpmキャッシュへ保存（OpenSpecは13.で使うため 1.17.0 に固定して保存）
npm install --global --prefix (Join-Path $Work "npm-prefix") --cache (Join-Path $NpmDir "npm-cache") @NpmPackages "@fission-ai/openspec@1.17.0"
if ($LASTEXITCODE -ne 0) {
    throw "Failed to download npm packages."
}

# 3. パッケージ一覧を保存
$NpmPackages | Set-Content -LiteralPath (Join-Path $NpmDir "npm-packages.txt") -Encoding UTF8

# 4. 導入するSkillのリポジトリとSkill名を列挙し、閉域側で使うため保存
$SkillSources = @(
    @{ Repo = 'mattpocock/skills'; Skills = @('ask-matt', 'code-review', 'codebase-design', 'diagnosing-bugs', 'domain-modeling', 'grill-me', 'grill-with-docs', 'grilling', 'handoff', 'implement', 'improve-codebase-architecture', 'prototype', 'research', 'resolving-merge-conflicts', 'setup-matt-pocock-skills', 'tdd', 'teach', 'to-questionnaire', 'to-spec', 'to-tickets', 'triage', 'wait-what', 'wayfinder', 'wizard', 'writing-great-skills') }
    @{ Repo = 'vercel-labs/agent-skills'; Skills = @('react-best-practices') }
    @{ Repo = 'trailofbits/skills'; Skills = @('modern-python', 'codeql', 'insecure-defaults') }
    @{ Repo = 'github/awesome-copilot'; Skills = @('java-springboot', 'spring-boot-testing') }
    @{ Repo = 'DietrichGebert/ponytail'; Skills = @('ponytail', 'ponytail-review', 'ponytail-audit') }
)
$SkillSources | ConvertTo-Json -Depth 3 |
    Set-Content -LiteralPath (Join-Path $SkillsDir "skills.json") -Encoding UTF8

# 5. 各リポジトリのデフォルトブランチをzipでダウンロード
foreach ($Source in $SkillSources) {
    $FileName = ($Source.Repo -replace '/', '__') + ".zip"
    Invoke-WebRequest `
        -Uri "https://github.com/$($Source.Repo)/archive/HEAD.zip" `
        -OutFile (Join-Path $SkillsDir $FileName) `
        -UseBasicParsing
}
```

### 0-3 pipパッケージをダウンロードする

閉域側と同じPython 3.14・Windows x64向けに、依存パッケージを含めたwheelをダウンロードし、閉域側で`pip install --no-index`できるようにする。
開域側のPythonのバージョンに関係なく閉域側向けのwheelを取得するよう、対象のプラットフォームとバージョンを指定する。
閉域側でビルドが発生しないよう、`--only-binary=:all:`でwheelのみを対象とする（wheelが配布されていないパッケージはここでエラーになる）。
ダウンロード時の検証はpipが行う。

```powershell
# 1. 閉域側の7.でまとめてインストールする pip パッケージを列挙
$PipPackages = @(
    'ruff'
    'pre-commit'
    'pytest'
    'codespell'
    'yamllint'
    'graphifyy'
)

# 2. 依存パッケージを含めたwheelをダウンロード
python -m pip download @PipPackages --only-binary=:all: --platform win_amd64 --python-version 3.14 --implementation cp --dest (Join-Path $PipDir "wheels")
if ($LASTEXITCODE -ne 0) {
    throw "Failed to download wheels."
}

# 3. パッケージ一覧を保存
$PipPackages | Set-Content -LiteralPath (Join-Path $PipDir "pip-packages.txt") -Encoding UTF8
```

### 0-4 VSCode拡張機能をダウンロードする

Visual Studio Marketplaceから、各拡張機能の最新の安定版VSIXをダウンロードする。

```powershell
# 1. VSCode 拡張機能を列挙（閉域側でこの順にインストールする。拡張機能パックや同梱先の拡張機能は、同梱される拡張機能の後に置く）
$ExtensionIds = @(
    'GitHub.copilot'
    'GitHub.copilot-chat'
    'ZooCodeOrganization.zoo-code'
    'anthropic.claude-code'
    'openai.codex-audio'
    'openai.chatgpt'
    'sst-dev.opencode-v2'
    'ms-vscode-remote.remote-wsl'
    'ms-vscode-remote.remote-containers'
    'ms-vscode-remote.remote-ssh'
    'ms-vscode.remote-server'
    'ms-vscode-remote.vscode-remote-extensionpack'
    'ms-python.debugpy'
    'ms-python.vscode-python-envs'
    'ms-python.vscode-pylance'
    'ms-python.python'
    'charliermarsh.ruff'
    'DavidAnson.vscode-markdownlint'
    'bierner.markdown-mermaid'
    'redhat.vscode-yaml'
    'tamasfe.even-better-toml'
)

# 2. 安定版かつWindows x64対応のVSIXをダウンロード
$VsixFiles = foreach ($ExtensionId in $ExtensionIds) {
    $Body = @{
        filters = @(@{
            criteria = @(@{ filterType = 7; value = $ExtensionId })
            pageSize = 1
        })
        # IncludeVersions | IncludeFiles | IncludeVersionProperties | IncludeAssetUri
        flags = 147
    } | ConvertTo-Json -Depth 5

    $Response = Invoke-RestMethod `
        -Method Post `
        -Uri "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery" `
        -ContentType "application/json" `
        -Headers @{ Accept = "application/json;api-version=3.0-preview.1" } `
        -Body $Body
    $Extension = $Response.results[0].extensions | Select-Object -First 1
    if (-not $Extension) {
        throw "Extension not found: $ExtensionId"
    }

    # プレリリース版と他プラットフォーム向けを除外し、最新版を選ぶ。
    $Version = $Extension.versions | Where-Object {
        ($null -eq $_.targetPlatform -or $_.targetPlatform -eq 'win32-x64') -and
        -not ($_.properties | Where-Object { $_.key -eq 'Microsoft.VisualStudio.Code.PreRelease' -and $_.value -eq 'true' })
    } | Select-Object -First 1

    $Source = ($Version.files | Where-Object { $_.assetType -eq 'Microsoft.VisualStudio.Services.VSIXPackage' }).source
    $FileName = "$ExtensionId-$($Version.version).vsix"
    Invoke-WebRequest -Uri $Source -OutFile (Join-Path $VsixDir $FileName) -UseBasicParsing
    Write-Host "Downloaded: $FileName"
    $FileName
}

# 3. インストール順序を保存
$VsixFiles | Set-Content -LiteralPath (Join-Path $VsixDir "extensions.txt") -Encoding UTF8
```

### 0-5 資材をzipにまとめて搬出する

```powershell
# 1. 資材をzipにまとめる（Compress-Archiveの2GB制限を避けるため tar を使い、エクスプローラーでも展開できるよう「.」ではなくフォルダ名を指定する）
$ZipFile = Join-Path $HOME ("offline-dist-{0:yyyyMMdd}.zip" -f (Get-Date))
tar -a -c -f $ZipFile -C $Dist @((Get-ChildItem -LiteralPath $Dist).Name)
if ($LASTEXITCODE -ne 0) {
    throw "Failed to create $ZipFile"
}

# 2. 資材ディレクトリと作業ディレクトリを削除
Remove-Item -LiteralPath $Dist, $Work -Recurse -Force -ErrorAction SilentlyContinue

# 3. zipのパスとサイズを確認
Get-Item -LiteralPath $ZipFile | Select-Object FullName, @{ Name = "SizeMB"; Expression = { [math]::Round($_.Length / 1MB) } }
```

`$HOME\offline-dist-<日付>.zip`を、組織の持ち込み規程（ウイルススキャンなど）に従って外部媒体へコピーし、閉域側PCへ搬入する。

## 1. テレメトリーを無効化する

各ツールが利用状況を外部へ送信しないよう、最初にテレメトリー無効化用の環境変数をユーザ環境変数に設定する。
ここからは閉域側PCで実行する。
設定後、PowerShellを開き直してから次の手順へ進む。

```powershell
# 1. 共通の DO_NOT_TRACK 規約（OpenSpec、skills CLI、Claude Code など）
[Environment]::SetEnvironmentVariable("DO_NOT_TRACK", "1", "User")
# 2. OpenSpec
[Environment]::SetEnvironmentVariable("OPENSPEC_TELEMETRY", "0", "User")
# 3. skills CLI / Claude Code
[Environment]::SetEnvironmentVariable("DISABLE_TELEMETRY", "1", "User")
# 4. Claude Code（エラー報告と、自動更新などの必須でない通信を無効化）
[Environment]::SetEnvironmentVariable("DISABLE_ERROR_REPORTING", "1", "User")
[Environment]::SetEnvironmentVariable("CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC", "1", "User")
# 5. PowerShell 7（pwsh 起動前に設定されている必要がある）
[Environment]::SetEnvironmentVariable("POWERSHELL_TELEMETRY_OPTOUT", "1", "User")
```

## 2. 資材を展開する

搬入した`offline-dist-<日付>.zip`を`$HOME`へコピーしてから、以下を実行する。
以降の各手順は、PowerShellを開き直しても続きから実行できる。

```powershell
# 最新の資材zipを $HOME\offline-dist へ展開
$ZipFile = Get-ChildItem -LiteralPath $HOME -Filter "offline-dist-*.zip" | Sort-Object Name -Descending | Select-Object -First 1
Remove-Item -LiteralPath "$HOME\offline-dist" -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "$HOME\offline-dist" -Force | Out-Null
tar -xf $ZipFile.FullName -C "$HOME\offline-dist"
```

## 3. 開発ツールをインストールする

SETUP.mdの2.でwingetを使ってインストールしているツールとGitを、配布物からインストールする。
Python/Node.jsは5.でインストールするため、miseは使用しない。

```powershell
# 1. 資材の場所と作業ディレクトリを設定し、インストール先ディレクトリを作成
$Tools = "$HOME\offline-dist\tools"
$Work = Join-Path $env:TEMP "offline-setup"
New-Item -ItemType Directory -Path "$HOME\.local\bin", "$HOME\.local\opt\pwsh", $Work -Force | Out-Null

# 2. 単体の実行ファイルで動くツールを展開し、$HOME\.local\bin へ配置
foreach ($Filter in "uv-x86_64-pc-windows-msvc.zip", "ripgrep-*-x86_64-pc-windows-msvc.zip") {
    tar -xf (Get-ChildItem -LiteralPath $Tools -Filter $Filter | Select-Object -First 1).FullName -C $Work
}
Get-ChildItem -LiteralPath $Work -Recurse -Include "uv.exe", "uvx.exe", "uvw.exe", "rg.exe" |
    Copy-Item -Destination "$HOME\.local\bin" -Force
Copy-Item -LiteralPath "$Tools\jq-windows-amd64.exe" -Destination "$HOME\.local\bin\jq.exe" -Force

# 3. PowerShell 7 をディレクトリごと配置
tar -xf (Get-ChildItem -LiteralPath $Tools -Filter "PowerShell-*-win-x64.zip" | Select-Object -First 1).FullName -C "$HOME\.local\opt\pwsh"

# 4. Git、VSCode、Pandoc をユーザ権限でサイレントインストール
Start-Process -Wait -FilePath (Get-ChildItem -LiteralPath $Tools -Filter "Git-*-64-bit.exe" | Select-Object -First 1).FullName -ArgumentList "/VERYSILENT", "/NORESTART", "/NOCANCEL", "/SP-", "/CURRENTUSER"
Start-Process -Wait -FilePath (Get-ChildItem -LiteralPath $Tools -Filter "VSCodeUserSetup-x64-*.exe" | Select-Object -First 1).FullName -ArgumentList "/VERYSILENT", "/NORESTART", "/MERGETASKS=!runcode,addtopath"
Start-Process -Wait -FilePath "msiexec.exe" -ArgumentList "/i", "`"$((Get-ChildItem -LiteralPath $Tools -Filter "pandoc-*-windows-x86_64.msi" | Select-Object -First 1).FullName)`"", "/qn"

# 5. ユーザ環境変数 PATH に追加
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$HOME\.local\bin;$HOME\.local\opt\pwsh;$env:LOCALAPPDATA\Programs\Git\cmd;$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin;$env:LOCALAPPDATA\Pandoc", "User")
```

## 4. craneをインストールする

```powershell
# 1. インストール先ディレクトリを作成
New-Item -ItemType Directory -Path "$HOME\.local\bin" -Force | Out-Null
# 2. crane を展開
tar -xzf "$HOME\offline-dist\tools\go-containerregistry_Windows_x86_64.tar.gz" -C "$HOME\.local\bin" crane.exe
# 3. ユーザ環境変数 PATH に追加
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$HOME\.local\bin", "User")
```

ここまでに設定したPATHを反映するため、**PowerShellを開き直してから**次の手順へ進む。

## 5. Python/Node.jsをインストールする

0-1でダウンロードした配布物から、Python/Node.jsをユーザ権限でインストールする。

```powershell
# 1. Python をユーザ権限でサイレントインストール（ユーザ環境変数 PATH にも追加される）
Start-Process -Wait -FilePath (Get-ChildItem -LiteralPath "$HOME\offline-dist\tools" -Filter "python-3.14.*-amd64.exe" | Select-Object -First 1).FullName -ArgumentList "/quiet", "InstallAllUsers=0", "PrependPath=1", "Include_test=0"
# 2. Node.js をユーザのプログラムフォルダへ展開
New-Item -ItemType Directory -Path "$env:LOCALAPPDATA\Programs\nodejs" -Force | Out-Null
tar -xf (Get-ChildItem -LiteralPath "$HOME\offline-dist\tools" -Filter "node-v*-win-x64.zip" | Select-Object -First 1).FullName -C "$env:LOCALAPPDATA\Programs\nodejs" --strip-components=1
# 3. npm のグローバルインストール先をユーザフォルダに設定
& "$env:LOCALAPPDATA\Programs\nodejs\npm.cmd" config set prefix "$env:APPDATA\npm"
# 4. ユーザ環境変数 PATH に Node.js と npm のグローバルインストール先を追加
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$env:LOCALAPPDATA\Programs\nodejs;$env:APPDATA\npm", "User")
```

PATHを反映するため、**PowerShellを開き直してから**次の手順へ進む。

## 6. npmパッケージをインストール

```powershell
# npmキャッシュから、一覧の npm パッケージをまとめてオフラインインストール
npm install --global --offline --cache "$HOME\offline-dist\npm\npm-cache" (Get-Content "$HOME\offline-dist\npm\npm-packages.txt")
```

## 7. pipパッケージをインストール

```powershell
# wheelから、一覧の pip パッケージをまとめてオフラインインストール
python -m pip install --no-index --find-links "$HOME\offline-dist\pip\wheels" -r "$HOME\offline-dist\pip\pip-packages.txt"
```

## 8. VSCode 拡張機能をインストールする

Remote - SSH、WSL、Dev Containersは、接続先へVS Code Serverを配置する際にインターネットへ接続する。
閉域環境で使う場合は、接続先へVS Code Serverを別途配置する。

```powershell
# 1. 0-4で保存した順序で VSIX をインストール
foreach ($FileName in Get-Content "$HOME\offline-dist\vsix\extensions.txt") {
    code --install-extension "$HOME\offline-dist\vsix\$FileName" --force
}
# 2. インストール結果を確認
code --list-extensions --show-versions
```

## 9. VSCode の設定を追加する

[SETUP.mdの8. VSCode の設定を追加する](SETUP.md#8-vscode-の設定を追加する)の設定を追加したうえで、閉域環境では以下も追加する。

```json
{
    // 閉域環境では更新確認が失敗するため、自動更新を無効化.
    "update.mode": "none",
    "extensions.autoUpdate": false,
    "extensions.autoCheckUpdates": false
}
```

## 10. コーディングエージェントにローカルLLMを設定する

[SETUP.mdの9. コーディングエージェントにローカルLLMを設定する](SETUP.md#9-コーディングエージェントにローカルllmを設定する)と同じ手順で設定する。
`localhost`の代わりに閉域内のLLMサーバを使う場合は、URLのホスト名を置き換える。

## 11. 重複したPATHを除去

ここまでの手順でユーザ環境変数PATHに重複して追加されたディレクトリを、順序を保ったまま除去する。

```powershell
# ユーザ環境変数 PATH の重複を除去
[Environment]::SetEnvironmentVariable("Path", (([Environment]::GetEnvironmentVariable("Path", "User") -split ';' | Where-Object { $_ } | Select-Object -Unique) -join ';'), "User")
```

PATHを反映するため、**PowerShellを開き直してから**次の手順へ進む。

## 12. 動作確認

```powershell
# インストールしたコマンドのバージョンを確認する
crane version
git --version
node --version
npm --version
python --version
pwsh --version
code --version
uv --version
jq --version
pandoc --version
rg --version
opencode --version
codex --version
claude --version
copilot --version
git-cz --version
pnpm --version
tsc --version
tsx --version
vp --version
npm ls --global --depth=0
ruff --version
pre-commit --version
pytest --version
codespell --version
yamllint --version
```

## 13. OpenSpecをプロジェクトに導入

```powershell
# 1. npmキャッシュから OpenSpec 1.17.0 をオフラインインストール
npm install --global --offline --cache "$HOME\offline-dist\npm\npm-cache" "@fission-ai/openspec@1.17.0"
openspec --version

# 2. OpenSpecをプロジェクトへ導入
Set-Location -LiteralPath '<project-root>'
openspec init --tools agents --force --profile custom --no-animation
openspec config set telemetry.enabled false
```

## 14. 有用なAgent Skillsをインストール

プロジェクトのルートで実行する。skills CLIは6.でインストール済みである。

```powershell
# 1. プロジェクトのルートへ移動し、作業ディレクトリを設定
Set-Location -LiteralPath '<project-root>'
$Work = Join-Path $env:TEMP "offline-setup\skills"

# 2. 各リポジトリを展開し、ローカルパスからSkillを導入
foreach ($Source in (Get-Content "$HOME\offline-dist\skills\skills.json" -Raw | ConvertFrom-Json)) {
    $Dest = Join-Path $Work ($Source.Repo -replace '/', '__')
    New-Item -ItemType Directory -Path $Dest -Force | Out-Null
    tar -xf "$HOME\offline-dist\skills\$($Source.Repo -replace '/', '__').zip" -C $Dest --strip-components=1
    skills add $Dest --agent universal --yes @($Source.Skills)
}

# 3. 7.でインストールした Graphify をプロジェクトへ導入
graphify agents install --project
```

## 🔖 参考文献

- [SETUP.md](SETUP.md)
- [Documentation for Visual Studio Code](https://code.visualstudio.com/docs)
- [Install Visual Studio Code extensions - Install from a VSIX](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace#_install-from-a-vsix)
- [Remote Development FAQ - Visual Studio Code](https://code.visualstudio.com/docs/remote/faq)
- [Installing PowerShell on Windows - Microsoft Learn](https://learn.microsoft.com/ja-jp/powershell/scripting/install/installing-powershell-on-windows)
- [Linking to releases - GitHub Docs](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases)
- [Git for Windows](https://gitforwindows.org/)
- [Git for Windows - Silent or Unattended Installation](https://github.com/git-for-windows/git/wiki/Silent-or-Unattended-Installation)
- [Using Python on Windows - Python documentation](https://docs.python.org/3/using/windows.html)
- [Node.js - Download](https://nodejs.org/en/download)
- [npm folders - npm Docs](https://docs.npmjs.com/cli/configuring-npm/folders)
- [Installing pandoc](https://pandoc.org/installing.html)
- [npm install - npm Docs](https://docs.npmjs.com/cli/commands/npm-install)
- [uv tool install - uv](https://docs.astral.sh/uv/reference/cli/#uv-tool-install)
- [pip download - pip documentation](https://pip.pypa.io/en/stable/cli/pip_download/)
- [pip install - pip documentation](https://pip.pypa.io/en/stable/cli/pip_install/)
- [google/go-containerregistry](https://github.com/google/go-containerregistry)
- [jqlang/jq: Command-line JSON processor](https://github.com/jqlang/jq)
- [Pandoc - index](https://pandoc.org/)
- [BurntSushi/ripgrep](https://github.com/burntsushi/ripgrep)
- [Fission-AI/OpenSpec: Spec-driven development (SDD) for AI coding assistants.](https://github.com/Fission-AI/OpenSpec)
- [Claude Code - Anthropic](https://docs.anthropic.com/en/docs/claude-code/overview)
- [openai/codex](https://github.com/openai/codex)
- [GitHub Copilot CLI - GitHub Docs](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)
- [opencode](https://opencode.ai/docs/)
- [git-cz](https://github.com/streamich/git-cz)
- [Vite+](https://viteplus.dev/guide)
- [pnpm](https://pnpm.io/)
- [Ruff](https://docs.astral.sh/ruff/)
- [pre-commit](https://pre-commit.com/)
- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)
- [about_Telemetry - PowerShell | Microsoft Learn](https://learn.microsoft.com/ja-jp/powershell/module/microsoft.powershell.core/about/about_telemetry)
- [Data usage - Claude Code](https://docs.claude.com/en/docs/claude-code/data-usage)
