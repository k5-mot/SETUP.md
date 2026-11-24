<!-- markdownlint-disable MD013 MD033 -->

# 🔒 Windows閉域環境セットアップ 2026年度版

本書は、[SETUP.md](SETUP.md)の手順をインターネットに接続できない閉域環境で再現するための手順書である。
開域側のWindows PCで資材をダウンロードしてzipにまとめ、外部媒体などで閉域側のWindows PCへ搬入してからインストールする。

- 開域側PC: インターネットに接続できるWindows PC（PowerShell）
- 閉域側PC: インターネットに接続できないWindows PC（PowerShell）
- 両PCとも管理者権限は不要である
- 閉域側ではwingetを使用できないため、各ツールの公式配布物（zipまたはインストーラ）を直接展開する
- 閉域側ではリポジトリを取得する手段がないため、SETUP.mdに加えてGitをインストールする
- GitHub APIはRate Limitの対象となるため使用しない。最新版はWebの`releases/latest`のリダイレクト先から判定する
- 資材の検証はダウンロード時のみ行う。配布元がチェックサムを公開している資材はSHA256で照合する

資材は以下の構成のzip（`offline-dist-<日付>.zip`）にまとめる。

```text
offline-dist/
├─ tools/                  # crane、Git、PowerShell、VSCode、mise、uv、jq、Pandoc、ripgrep
├─ mise/                   # miseでインストール済みのPython / Node.js
├─ vsix/                   # VSIXとインストール順序
├─ npm/                    # npmキャッシュとnpmパッケージ一覧
├─ pip/                    # wheelとpipパッケージ一覧
└─ skills/                 # 任意のAgent Skills資材
```

## 📑 目次

1. [🔕 テレメトリを無効化する](#-テレメトリを無効化する)
2. [0️⃣ 開域側PCで資材をダウンロードする](#0️⃣-開域側pcで資材をダウンロードする)
   - [0-1 共通設定をする](#-0-1-共通設定をする)
   - [0-2 craneをダウンロードする](#-0-2-craneをダウンロードする)
   - [0-3 開発ツールをダウンロードする](#-0-3-開発ツールをダウンロードする)
   - [0-4 Python/Node.jsをダウンロードする](#-0-4-pythonnodejsをダウンロードする)
   - [0-5 VSCode拡張機能をダウンロードする](#-0-5-vscode拡張機能をダウンロードする)
   - [0-6 npmパッケージをダウンロードする](#-0-6-npmパッケージをダウンロードする)
   - [0-7 pipパッケージをダウンロードする](#-0-7-pipパッケージをダウンロードする)
   - [0-8 その他のAgent Skillsをダウンロードする (任意)](#-0-8-その他のagent-skillsをダウンロードする-任意)
   - [0-9 資材をzipにまとめて搬出する](#-0-9-資材をzipにまとめて搬出する)
3. [1️⃣ 資材を展開し、共通設定をする](#1️⃣-資材を展開し共通設定をする)
4. [2️⃣ craneをインストールする](#2️⃣-craneをインストールする)
5. [3️⃣ 開発ツールをインストールする](#3️⃣-開発ツールをインストールする)
6. [4️⃣ miseでPython/Node.jsを設定する](#4️⃣-miseでpythonnodejsを設定する)
7. [5️⃣ VSCode 拡張機能をインストールする](#5️⃣-vscode-拡張機能をインストールする)
8. [6️⃣ VSCode の設定を追加する](#6️⃣-vscode-の設定を追加する)
9. [7️⃣ コーディングエージェントにローカルLLMを設定する](#7️⃣-コーディングエージェントにローカルllmを設定する)
10. [8️⃣ npm/pipパッケージをインストールし、OpenSpecを導入する](#8️⃣-npmpipパッケージをインストールしopenspecを導入する)
11. [9️⃣ 動作確認](#9️⃣-動作確認)
12. [🔟 その他のAgent Skillsを導入する (任意)](#-その他のagent-skillsを導入する-任意)
13. [🔖 参考文献](#-参考文献)

## 🔕 テレメトリを無効化する

各ツールが利用状況を外部へ送信しないよう、最初にテレメトリ無効化用の環境変数を設定する。
開域側PCと閉域側PCの**両方**で実行する。

```powershell
### 1. テレメトリ無効化用の環境変数を列挙
$TelemetryEnv = [ordered]@{
    # 共通の DO_NOT_TRACK 規約（OpenSpec、skills CLI、Claude Code など）
    DO_NOT_TRACK                             = '1'
    # OpenSpec
    OPENSPEC_TELEMETRY                       = '0'
    # skills CLI / Claude Code
    DISABLE_TELEMETRY                        = '1'
    # Claude Code（エラー報告と、自動更新などの必須でない通信を無効化）
    DISABLE_ERROR_REPORTING                  = '1'
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = '1'
    # PowerShell 7（pwsh 起動前に設定されている必要がある）
    POWERSHELL_TELEMETRY_OPTOUT              = '1'
}

### 2. ユーザ環境変数と現在のセッションに設定
foreach ($Name in $TelemetryEnv.Keys) {
    [Environment]::SetEnvironmentVariable($Name, $TelemetryEnv[$Name], "User")
    Set-Item -Path "Env:$Name" -Value $TelemetryEnv[$Name]
}
```

## 0️⃣ 開域側PCで資材をダウンロードする

0-1から0-9までは、**同一のPowerShellセッション**で順に実行する。
途中でセッションを閉じた場合は、0-1から再実行する。

### 🧰 0-1 共通設定をする

```powershell
$ErrorActionPreference = "Stop"

# Windows PowerShell 5.1でのダウンロード速度低下とTLSエラーを防ぐ。
$ProgressPreference = "SilentlyContinue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

### 1. 資材の出力先と作業ディレクトリを設定
$Dist = Join-Path $env:TEMP "offline-dist"
$Work = Join-Path $env:TEMP "offline-dist-work"
$ToolsDir = Join-Path $Dist "tools"
$MiseDir = Join-Path $Dist "mise"
$VsixDir = Join-Path $Dist "vsix"
$NpmDir = Join-Path $Dist "npm"
$PipDir = Join-Path $Dist "pip"
$SkillsDir = Join-Path $Dist "skills"

### 2. ディレクトリを作成
foreach ($Dir in @($Dist, $Work, $ToolsDir, $MiseDir, $VsixDir, $NpmDir, $PipDir, $SkillsDir)) {
    New-Item -ItemType Directory -Path $Dir -Force | Out-Null
}

### 3. GitHub APIを使わず、releases/latest のリダイレクト先から最新タグを取得する関数
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

### 4. ダウンロードしたファイルを配布元のチェックサムファイルで検証する関数
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

### 5. GitHub Releasesから資材をダウンロードし、チェックサムがあれば検証する関数
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
```

### 📦 0-2 craneをダウンロードする

```powershell
### SETUP.mdと同じバージョンのcraneをダウンロードし、checksums.txt で検証.
Save-GitHubReleaseAsset `
    -Repo "google/go-containerregistry" `
    -Tag "v0.22.1" `
    -FileName "go-containerregistry_Windows_x86_64.tar.gz" `
    -ChecksumFile "checksums.txt"
```

### 🔧 0-3 開発ツールをダウンロードする

SETUP.mdでwingetからインストールしているツールとGitの、ユーザ権限でインストールできる配布物をダウンロードする。
GitとPandocは配布元がチェックサムファイルを公開していないため、HTTPSでのダウンロードのみとする。

```powershell
### 1. GitHub Releasesで配布されているツールを列挙（タグからファイル名とチェックサムファイル名を決める）
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
        Repo     = 'jdx/mise'
        File     = { param($Tag) "mise-$Tag-windows-x64.zip" }
        Checksum = { param($Tag, $File) 'SHASUMS256.txt' }
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
        File     = { param($Tag) "pandoc-$Tag-windows-x86_64.zip" }
        Checksum = { param($Tag, $File) $null }
    }
    @{
        Repo     = 'BurntSushi/ripgrep'
        File     = { param($Tag) "ripgrep-$Tag-x86_64-pc-windows-msvc.zip" }
        Checksum = { param($Tag, $File) "$File.sha256" }
    }
)

### 2. 最新リリースをダウンロードして検証
foreach ($Asset in $Assets) {
    $Tag = Get-GitHubLatestTag -Repo $Asset.Repo
    $File = & $Asset.File $Tag
    Save-GitHubReleaseAsset `
        -Repo $Asset.Repo `
        -Tag $Tag `
        -FileName $File `
        -ChecksumFile (& $Asset.Checksum $Tag $File)
}

### 3. VSCode（ユーザインストーラ版）をダウンロードし、更新APIが返すSHA256で検証
$VSCodeRelease = Invoke-RestMethod -Uri "https://update.code.visualstudio.com/api/update/win32-x64-user/stable/latest"
$VSCodeSetup = Join-Path $ToolsDir "VSCodeUserSetup-x64-$($VSCodeRelease.productVersion).exe"
Invoke-WebRequest -Uri $VSCodeRelease.url -OutFile $VSCodeSetup -UseBasicParsing
if ((Get-FileHash -LiteralPath $VSCodeSetup -Algorithm SHA256).Hash -ne $VSCodeRelease.sha256hash.ToUpperInvariant()) {
    throw "SHA256 mismatch: VSCode"
}
Write-Host "Verified: $(Split-Path $VSCodeSetup -Leaf)"
```

### 🐍 0-4 Python/Node.jsをダウンロードする

開域側で一時的にmiseを使ってPython/Node.jsをインストールし、そのインストール済みディレクトリを資材にする。
ダウンロード時の検証はmiseが行う。開域側の既存のmise環境には影響しない。

```powershell
### 1. バージョンを設定
$PythonVersion = "3.14"
$NodeVersion = "24"

### 2. 0-3でダウンロードしたmiseを作業ディレクトリへ展開
$MiseZip = Get-ChildItem -LiteralPath $ToolsDir -Filter "mise-v*-windows-x64.zip" | Select-Object -First 1
$MiseWork = Join-Path $Work "mise"
New-Item -ItemType Directory -Path $MiseWork -Force | Out-Null
tar -xf $MiseZip.FullName -C $MiseWork
if ($LASTEXITCODE -ne 0) {
    throw "Failed to extract mise."
}
$Mise = (Get-ChildItem -LiteralPath $MiseWork -Recurse -Filter "mise.exe" | Select-Object -First 1).FullName

### 3. 既存のmise環境と分離するため、データ・キャッシュ・設定の保存先を作業ディレクトリへ変更
$env:MISE_DATA_DIR = Join-Path $Work "mise-data"
$env:MISE_CACHE_DIR = Join-Path $Work "mise-cache"
$env:MISE_CONFIG_DIR = Join-Path $Work "mise-config"

### 4. Python / Node.js をインストール
& $Mise install "python@$PythonVersion" "node@$NodeVersion"
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install Python / Node.js."
}

### 5. インストール先を取得し、資材ディレクトリへコピー
$PythonDir = (& $Mise where "python@$PythonVersion").Trim()
$NodeDir = (& $Mise where "node@$NodeVersion").Trim()
foreach ($Tool in @(@{ Name = "python"; Dir = $PythonDir }, @{ Name = "node"; Dir = $NodeDir })) {
    $Dest = Join-Path $MiseDir $Tool.Name
    # 再実行時に入れ子でコピーされないよう、古い資材を削除してからコピーする。
    Remove-Item -LiteralPath $Dest -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Path $Dest -Force | Out-Null
    Copy-Item -LiteralPath $Tool.Dir -Destination (Join-Path $Dest (Split-Path $Tool.Dir -Leaf)) -Recurse -Force
}

### 6. 0-6以降で使うため、Python / Node.js のパスを取得
$PythonExe = (Get-ChildItem -LiteralPath $PythonDir -Recurse -Filter "python.exe" | Select-Object -First 1).FullName
$Npm = Join-Path $NodeDir "npm.cmd"
$env:Path = "$NodeDir;$env:Path"

### 7. コピーしたバージョンを確認
Get-ChildItem -LiteralPath $MiseDir -Directory | Get-ChildItem -Directory | Select-Object FullName
```

### 🧩 0-5 VSCode拡張機能をダウンロードする

Visual Studio Marketplaceから、各拡張機能の最新の安定版VSIXをダウンロードする。

```powershell
### 1. VSCode 拡張機能を列挙（閉域側でこの順にインストールする）
$ExtensionIds = @(
    'GitHub.copilot'
    'GitHub.copilot-chat'
    'ZooCodeOrganization.zoo-code'
    'anthropic.claude-code'
    'openai.chatgpt'
    'sst-dev.opencode-v2'
)

### 2. 安定版かつWindows x64対応のVSIXをダウンロード
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

### 3. インストール順序を保存
$VsixFiles | Set-Content -LiteralPath (Join-Path $VsixDir "extensions.txt") -Encoding UTF8
```

### 📜 0-6 npmパッケージをダウンロードする

依存パッケージを含めてnpmキャッシュへ保存し、閉域側で`npm install --offline`できるようにする。
ダウンロード時の検証（integrity）はnpmが行う。
プラットフォーム別のバイナリを含むパッケージがあるため、閉域側と同じWindows x64のPCで実行する。

```powershell
### 1. npmキャッシュの保存先、パッケージ一覧、ダウンロード用の一時インストール先を設定
$NpmCache = Join-Path $NpmDir "npm-cache"
$NpmList = Join-Path $NpmDir "npm-packages.txt"
$NpmPrefix = Join-Path $Work "npm-prefix"

### 2. 最新バージョンを固定して依存パッケージごとnpmキャッシュへ保存し、一覧へ追記する関数
function Save-NpmPackage {
    param([Parameter(Mandatory)][string]$Name)
    $Version = (& $Npm view $Name version).Trim()
    & $Npm install --global --prefix $NpmPrefix --cache $NpmCache "$Name@$Version"
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to download $Name@$Version"
    }
    Add-Content -LiteralPath $NpmList -Value "$Name@$Version" -Encoding UTF8
}

### 3. npm パッケージを列挙
$NpmPackages = @(
    '@fission-ai/openspec'
    '@opencode/cli'
    '@openai/codex'
    '@anthropic-ai/claude-code'
    '@github/copilot'
    'git-cz'
)

### 4. パッケージ一覧を初期化し、各パッケージを保存
Set-Content -LiteralPath $NpmList -Value @() -Encoding UTF8
foreach ($Package in $NpmPackages) {
    Save-NpmPackage $Package
}
```

### 🐍 0-7 pipパッケージをダウンロードする

0-4のPythonで依存パッケージを含めたwheelをダウンロードし、閉域側で`pip install --no-index`できるようにする。
閉域側でビルドが発生しないよう、`--only-binary=:all:`でwheelのみを対象とする（wheelが配布されていないパッケージはここでエラーになる）。
ダウンロード時の検証はpipが行う。

```powershell
### 1. wheelの保存先とパッケージ一覧を設定
$WheelDir = Join-Path $PipDir "wheels"
$PipList = Join-Path $PipDir "pip-packages.txt"

### 2. pip パッケージを列挙
$PipPackages = @(
    'cowsay'
)

### 3. 依存パッケージを含めたwheelをダウンロードし、一覧を保存
& $PythonExe -m pip download @PipPackages --only-binary=:all: --dest $WheelDir
if ($LASTEXITCODE -ne 0) {
    throw "Failed to download wheels."
}
$PipPackages | Set-Content -LiteralPath $PipList -Encoding UTF8
```

<details>
<summary>0-8 その他のAgent Skillsをダウンロードする (任意)</summary>

### ➕ 0-8 その他のAgent Skillsをダウンロードする (任意)

閉域側で[🔟 その他のAgent Skillsを導入する (任意)](#-その他のagent-skillsを導入する-任意)を実施する場合だけ実行する。
`agent-browser`はブラウザ本体を追加でダウンロードするため、閉域環境では対象外とする。

```powershell
### 1. skills CLIをnpmキャッシュへ保存（パッケージ一覧へ追記される）
Save-NpmPackage "skills"

### 2. 導入するSkillのリポジトリとSkill名を列挙し、閉域側で使うため保存
$SkillSources = @(
    @{ Repo = 'mattpocock/skills'; Skills = @('ask-matt', 'code-review', 'codebase-design', 'diagnosing-bugs', 'domain-modeling', 'grill-me', 'grill-with-docs', 'grilling', 'handoff', 'implement', 'improve-codebase-architecture', 'prototype', 'research', 'resolving-merge-conflicts', 'setup-matt-pocock-skills', 'tdd', 'teach', 'to-questionnaire', 'to-spec', 'to-tickets', 'triage', 'wait-what', 'wayfinder', 'wizard', 'writing-great-skills') }
    @{ Repo = 'vercel-labs/agent-skills'; Skills = @('react-best-practices') }
    @{ Repo = 'trailofbits/skills'; Skills = @('modern-python', 'codeql', 'insecure-defaults') }
    @{ Repo = 'github/awesome-copilot'; Skills = @('java-springboot', 'spring-boot-testing') }
    @{ Repo = 'DietrichGebert/ponytail'; Skills = @('ponytail', 'ponytail-review', 'ponytail-audit') }
)
$SkillSources | ConvertTo-Json -Depth 3 |
    Set-Content -LiteralPath (Join-Path $SkillsDir "skills.json") -Encoding UTF8

### 3. 各リポジトリのデフォルトブランチをzipでダウンロード
foreach ($Source in $SkillSources) {
    $FileName = ($Source.Repo -replace '/', '__') + ".zip"
    Invoke-WebRequest `
        -Uri "https://github.com/$($Source.Repo)/archive/HEAD.zip" `
        -OutFile (Join-Path $SkillsDir $FileName) `
        -UseBasicParsing
}

### 4. Graphifyと依存パッケージのwheelを、0-4のPythonでダウンロード（0-7と同じ保存先）
& $PythonExe -m pip download graphifyy --only-binary=:all: --dest $WheelDir
if ($LASTEXITCODE -ne 0) {
    throw "Failed to download wheels for graphifyy."
}
```

</details>

### 🗜️ 0-9 資材をzipにまとめて搬出する

```powershell
### 1. 資材をzipにまとめる（Compress-Archiveの2GB制限を避けるため tar を使う）
$ZipFile = Join-Path $HOME ("offline-dist-{0:yyyyMMdd}.zip" -f (Get-Date))
tar -a -c -f $ZipFile -C $Dist .
if ($LASTEXITCODE -ne 0) {
    throw "Failed to create $ZipFile"
}

### 2. 資材ディレクトリと作業ディレクトリを削除
Remove-Item -LiteralPath $Dist, $Work -Recurse -Force -ErrorAction SilentlyContinue

### 3. zipのパスとサイズを確認
Get-Item -LiteralPath $ZipFile | Select-Object FullName, @{ Name = "SizeMB"; Expression = { [math]::Round($_.Length / 1MB) } }
```

`$HOME\offline-dist-<日付>.zip`を、組織の持ち込み規程（ウイルススキャンなど）に従って外部媒体へコピーし、閉域側PCへ搬入する。

## 1️⃣ 資材を展開し、共通設定をする

ここからは閉域側PCで実行する。
搬入した`offline-dist-<日付>.zip`を`$HOME`へコピーしてから、以下を実行する。
1️⃣から🔟までは**同一のPowerShellセッション**で順に実行する。途中でセッションを閉じた場合は、1️⃣の「2. 共通設定」から再実行する。

```powershell
$ErrorActionPreference = "Stop"

### 1. 最新の資材zipを $HOME\offline-dist へ展開
$Dist = Join-Path $HOME "offline-dist"
$ZipFile = Get-ChildItem -LiteralPath $HOME -Filter "offline-dist-*.zip" |
    Sort-Object Name -Descending |
    Select-Object -First 1
if (-not $ZipFile) {
    throw "Not found offline-dist-*.zip in $HOME"
}
Remove-Item -LiteralPath $Dist -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $Dist -Force | Out-Null
tar -xf $ZipFile.FullName -C $Dist
if ($LASTEXITCODE -ne 0) {
    throw "Failed to extract $($ZipFile.Name)"
}

### 2. 共通設定
$Dist = Join-Path $HOME "offline-dist"
$BinDir = Join-Path $HOME ".local\bin"
$OptDir = Join-Path $HOME ".local\opt"
$Work = Join-Path $env:TEMP "offline-setup"
foreach ($Dir in @($BinDir, $OptDir, $Work)) {
    New-Item -ItemType Directory -Path $Dir -Force | Out-Null
}

### 3. ユーザ環境変数 PATH と現在のセッションの PATH にディレクトリを追加する関数（重複防止）
function Add-PathEntry {
    param(
        [Parameter(Mandatory)][string]$Dir,
        [switch]$Prepend
    )
    $UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $PathEntries = @($UserPath -split ';' | Where-Object { $_ })
    if ($PathEntries -notcontains $Dir) {
        $NewEntries = if ($Prepend) { @($Dir) + $PathEntries } else { $PathEntries + @($Dir) }
        [Environment]::SetEnvironmentVariable("Path", ($NewEntries -join ';'), "User")
    }
    if (($env:Path -split ';') -notcontains $Dir) {
        $env:Path = if ($Prepend) { "$Dir;$env:Path" } else { "$env:Path;$Dir" }
    }
}
```

## 2️⃣ craneをインストールする

```powershell
### 1. crane.exe を展開
$Archive = Join-Path $Dist "tools\go-containerregistry_Windows_x86_64.tar.gz"
tar -xzf $Archive -C $BinDir crane.exe
if ($LASTEXITCODE -ne 0) {
    throw "Failed to extract crane.exe"
}

### 2. PATH に追加
Add-PathEntry -Dir $BinDir

### 3. 動作確認
crane version
```

## 3️⃣ 開発ツールをインストールする

SETUP.mdの2️⃣でwingetを使ってインストールしているツールとGitを、配布物からインストールする。

```powershell
$ToolsDir = Join-Path $Dist "tools"

### 1. zipを作業ディレクトリへ展開する関数
function Expand-ToolArchive {
    param([Parameter(Mandatory)][string]$Filter)
    $Archive = Get-ChildItem -LiteralPath $ToolsDir -Filter $Filter | Select-Object -First 1
    if (-not $Archive) {
        throw "Archive not found: $Filter"
    }
    $Dest = Join-Path $Work $Archive.BaseName
    New-Item -ItemType Directory -Path $Dest -Force | Out-Null
    tar -xf $Archive.FullName -C $Dest
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to extract $($Archive.Name)"
    }
    $Dest
}

### 2. 展開先から実行ファイルを探して $BinDir へコピーする関数
function Copy-ToolExe {
    param(
        [Parameter(Mandatory)][string]$Root,
        [Parameter(Mandatory)][string[]]$Names
    )
    foreach ($Name in $Names) {
        $Exe = Get-ChildItem -LiteralPath $Root -Recurse -Filter $Name | Select-Object -First 1
        if (-not $Exe) {
            throw "Not found $Name in $Root"
        }
        Copy-Item -LiteralPath $Exe.FullName -Destination $BinDir -Force
    }
}

### 3. インストーラを無人実行する関数
function Invoke-Installer {
    param(
        [Parameter(Mandatory)][string]$Filter,
        [Parameter(Mandatory)][string[]]$Arguments
    )
    $Installer = Get-ChildItem -LiteralPath $ToolsDir -Filter $Filter | Select-Object -First 1
    if (-not $Installer) {
        throw "Installer not found: $Filter"
    }
    $Process = Start-Process -FilePath $Installer.FullName -ArgumentList $Arguments -Wait -PassThru
    if ($Process.ExitCode -ne 0) {
        throw "Failed to install $($Installer.Name). ExitCode: $($Process.ExitCode)"
    }
}

### 4. 単体の実行ファイルで動くツールを $BinDir へ配置
Copy-ToolExe -Root (Expand-ToolArchive "mise-v*-windows-x64.zip") -Names "mise.exe"
Copy-ToolExe -Root (Expand-ToolArchive "uv-x86_64-pc-windows-msvc.zip") -Names "uv.exe", "uvx.exe", "uvw.exe"
Copy-ToolExe -Root (Expand-ToolArchive "pandoc-*-windows-x86_64.zip") -Names "pandoc.exe"
Copy-ToolExe -Root (Expand-ToolArchive "ripgrep-*-x86_64-pc-windows-msvc.zip") -Names "rg.exe"
Copy-Item -LiteralPath (Join-Path $ToolsDir "jq-windows-amd64.exe") -Destination (Join-Path $BinDir "jq.exe") -Force
Add-PathEntry -Dir $BinDir

### 5. PowerShell 7 をディレクトリごと配置
$PwshDir = Join-Path $OptDir "pwsh"
$PwshZip = Get-ChildItem -LiteralPath $ToolsDir -Filter "PowerShell-*-win-x64.zip" | Select-Object -First 1
New-Item -ItemType Directory -Path $PwshDir -Force | Out-Null
tar -xf $PwshZip.FullName -C $PwshDir
if ($LASTEXITCODE -ne 0) {
    throw "Failed to extract PowerShell."
}
Add-PathEntry -Dir $PwshDir

### 6. Git をユーザ権限でサイレントインストール
Invoke-Installer -Filter "Git-*-64-bit.exe" -Arguments "/VERYSILENT", "/NORESTART", "/NOCANCEL", "/SP-", "/CURRENTUSER"
Add-PathEntry -Dir (Join-Path $env:LOCALAPPDATA "Programs\Git\cmd")

### 7. VSCode（ユーザインストーラ版）をサイレントインストール
Invoke-Installer -Filter "VSCodeUserSetup-x64-*.exe" -Arguments "/VERYSILENT", "/NORESTART", "/MERGETASKS=!runcode,addtopath"
Add-PathEntry -Dir (Join-Path $env:LOCALAPPDATA "Programs\Microsoft VS Code\bin")

### 8. 動作確認
git --version
mise --version
uv --version
jq --version
pandoc --version
rg --version
pwsh --version
code --version
```

## 4️⃣ miseでPython/Node.jsを設定する

0-4でコピーしたインストール済みディレクトリを、miseのインストール先へ配置する。

```powershell
### 1. mise がインターネットへ問い合わせないよう、オフラインモードを設定
[Environment]::SetEnvironmentVariable("MISE_OFFLINE", "1", "User")
$env:MISE_OFFLINE = "1"

### 2. Python / Node.js を mise のインストール先へコピー
$MiseDir = Join-Path $Dist "mise"
$MiseInstalls = Join-Path $env:LOCALAPPDATA "mise\installs"
$Versions = @{}
foreach ($Tool in @("python", "node")) {
    $Source = Get-ChildItem -LiteralPath (Join-Path $MiseDir $Tool) -Directory | Select-Object -First 1
    $Dest = Join-Path $MiseInstalls $Tool
    New-Item -ItemType Directory -Path $Dest -Force | Out-Null
    Copy-Item -LiteralPath $Source.FullName -Destination $Dest -Recurse -Force
    $Versions[$Tool] = $Source.Name
}

### 3. コピーしたバージョンをグローバルに設定
mise use --global "python@$($Versions.python)" "node@$($Versions.node)"
if ($LASTEXITCODE -ne 0) {
    throw "Failed to set Python / Node.js."
}

### 4. mise の shims を生成し、PATH の先頭に追加
mise reshim
if ($LASTEXITCODE -ne 0) {
    throw "Failed to generate mise shims."
}
Add-PathEntry -Dir (Join-Path $env:LOCALAPPDATA "mise\shims") -Prepend

### 5. 動作確認
mise ls
python --version
node --version
npm --version
Get-Command python
Get-Command node
```

## 5️⃣ VSCode 拡張機能をインストールする

```powershell
### 0-5で保存した順序で VSIX をインストール.
$VsixDir = Join-Path $Dist "vsix"
foreach ($FileName in Get-Content -LiteralPath (Join-Path $VsixDir "extensions.txt")) {
    code --install-extension (Join-Path $VsixDir $FileName) --force
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install $FileName"
    }
}
code --list-extensions --show-versions
```

## 6️⃣ VSCode の設定を追加する

[SETUP.mdの5️⃣ VSCode の設定を追加する](SETUP.md#5️⃣-vscode-の設定を追加する)の設定を追加したうえで、閉域環境では以下も追加する。

```json
{
    // 閉域環境では更新確認が失敗するため、自動更新を無効化.
    "update.mode": "none",
    "extensions.autoUpdate": false,
    "extensions.autoCheckUpdates": false
}
```

## 7️⃣ コーディングエージェントにローカルLLMを設定する

[SETUP.mdの6️⃣ コーディングエージェントにローカルLLMを設定する](SETUP.md#6️⃣-コーディングエージェントにローカルllmを設定する)と同じ手順で設定する。
`localhost`の代わりに閉域内のLLMサーバを使う場合は、URLのホスト名を置き換える。

## 8️⃣ npm/pipパッケージをインストールし、OpenSpecを導入する

0-8を実行した場合は、skills CLIもここでインストールされる。

```powershell
### 1. npmキャッシュから、一覧のパッケージをオフラインインストール
$NpmDir = Join-Path $Dist "npm"
foreach ($Package in Get-Content -LiteralPath (Join-Path $NpmDir "npm-packages.txt")) {
    npm install --global --offline --cache (Join-Path $NpmDir "npm-cache") $Package
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install $Package"
    }
}
mise reshim

### 2. wheelから、一覧のpipパッケージをオフラインインストール
$PipDir = Join-Path $Dist "pip"
$PipPackages = @(Get-Content -LiteralPath (Join-Path $PipDir "pip-packages.txt") | Where-Object { $_ })
python -m pip install --no-index --find-links (Join-Path $PipDir "wheels") @PipPackages
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install pip packages."
}
mise reshim

### 3. OpenSpecをプロジェクトへ導入
Set-Location -LiteralPath '<project-root>'
openspec init --tools agents --force --profile custom --no-animation
openspec config set telemetry.enabled false
```

## 9️⃣ 動作確認

```powershell
# インストールしたコマンドのバージョンを確認する。
crane version
git --version
mise --version
node --version
npm --version
python --version
pwsh --version
code --version
uv --version
jq --version
pandoc --version
rg --version
openspec --version
opencode --version
codex --version
claude --version
copilot --version
git-cz --version
python -m pip show cowsay
```

<details>
<summary>その他のAgent Skillsを導入する</summary>

## 🔟 その他のAgent Skillsを導入する (任意)

[0-8](#-0-8-その他のagent-skillsをダウンロードする-任意)で資材をダウンロードした場合だけ、プロジェクトのルートで実行する。

```powershell
$SkillsDir = Join-Path $Dist "skills"
Set-Location -LiteralPath '<project-root>'

### 1. 各リポジトリを展開し、ローカルパスからSkillを導入（skills CLI は8️⃣でインストール済み）
$SkillSources = Get-Content -LiteralPath (Join-Path $SkillsDir "skills.json") -Raw | ConvertFrom-Json
foreach ($Source in $SkillSources) {
    $Name = $Source.Repo -replace '/', '__'
    $Dest = Join-Path $Work "skills\$Name"
    New-Item -ItemType Directory -Path $Dest -Force | Out-Null
    tar -xf (Join-Path $SkillsDir "$Name.zip") -C $Dest --strip-components=1
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to extract $Name"
    }
    skills add $Dest --agent universal --yes @($Source.Skills)
}

### 2. Graphify を wheel からオフラインインストールし、プロジェクトへ導入
$PythonExe = (Get-Command python).Source
uv tool install graphifyy --offline --no-index --find-links (Join-Path $Dist "pip\wheels") --python $PythonExe
graphify agents install --project
```

</details>

## 🔖 参考文献

- [SETUP.md](SETUP.md)
- [Documentation for Visual Studio Code](https://code.visualstudio.com/docs)
- [Install Visual Studio Code extensions - Install from a VSIX](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace#_install-from-a-vsix)
- [Installing PowerShell on Windows - Microsoft Learn](https://learn.microsoft.com/ja-jp/powershell/scripting/install/installing-powershell-on-windows)
- [Linking to releases - GitHub Docs](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases)
- [Git for Windows](https://gitforwindows.org/)
- [Git for Windows - Silent or Unattended Installation](https://github.com/git-for-windows/git/wiki/Silent-or-Unattended-Installation)
- [mise - Configuration / Settings](https://mise.jdx.dev/configuration/settings.html)
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
- [cowsay - PyPI](https://pypi.org/project/cowsay/)
- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)
- [about_Telemetry - PowerShell | Microsoft Learn](https://learn.microsoft.com/ja-jp/powershell/module/microsoft.powershell.core/about/about_telemetry)
- [Data usage - Claude Code](https://docs.claude.com/en/docs/claude-code/data-usage)
