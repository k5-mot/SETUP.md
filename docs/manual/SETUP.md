<!-- markdownlint-disable MD013 MD033 -->

# 🚀 Windows開発環境セットアップ 2026年度版

## 📝 概要

Windows 11上に、PowerShell 7、VSCode、Python/Node.js、コーディングエージェント、OpenSpecなどの開発環境を構築する手順書である。

## 📑 目次

- [📝 概要](#-概要)
- [✅ 前提条件](#-前提条件)
- [1. テレメトリーを無効化する](#1-テレメトリーを無効化する)
- [2. wingetで開発ツールをインストールする](#2-wingetで開発ツールをインストールする)
- [3. craneをインストールする](#3-craneをインストールする)
- [4. miseで、Python/Node.jsをインストールする](#4-miseでpythonnodejsをインストールする)
- [5. npmパッケージをインストール](#5-npmパッケージをインストール)
- [6. pipパッケージをインストール](#6-pipパッケージをインストール)
- [7. VSCode 拡張機能をインストールする](#7-vscode-拡張機能をインストールする)
- [8. VSCode の設定を追加する](#8-vscode-の設定を追加する)
- [9. コーディングエージェントにローカルLLMを設定する](#9-コーディングエージェントにローカルllmを設定する)
  - [GitHub Copilotで使う場合](#-github-copilotで使う場合)
  - [Codexで使う場合](#-codexで使う場合)
  - [Claude Codeで使う場合](#-claude-codeで使う場合)
  - [Zoo Codeで使う場合](#-zoo-codeで使う場合)
- [10. 重複したPATHを除去](#10-重複したpathを除去)
- [11. 動作確認](#11-動作確認)
- [12. OpenSpecをプロジェクトに導入](#12-openspecをプロジェクトに導入)
- [13. 有用なAgent Skillsをインストール](#13-有用なagent-skillsをインストール)
- [🔖 参考文献](#-参考文献)

## ✅ 前提条件

- Windows 11（x64）であること
- 一般ユーザ権限のPowerShellで実行できること（管理者権限は不要）
- インターネットに接続できること
- wingetが利用できること
- 9.でローカルLLMを使う場合は、OpenAI互換APIを提供するLLMサーバ（vLLMなど）が起動していること

## 1. テレメトリーを無効化する

各ツールが利用状況を外部へ送信しないよう、最初にテレメトリー無効化用の環境変数をユーザ環境変数に設定する。

```powershell
# 1. 共通
[Environment]::SetEnvironmentVariable("DO_NOT_TRACK", "1", "User")
# 2. OpenSpec
[Environment]::SetEnvironmentVariable("OPENSPEC_TELEMETRY", "0", "User")
# 3. skills CLI / Claude Code
[Environment]::SetEnvironmentVariable("DISABLE_TELEMETRY", "1", "User")
# 4. Claude Code
[Environment]::SetEnvironmentVariable("DISABLE_ERROR_REPORTING", "1", "User")
[Environment]::SetEnvironmentVariable("CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC", "1", "User")
# 5. PowerShell 7
[Environment]::SetEnvironmentVariable("POWERSHELL_TELEMETRY_OPTOUT", "1", "User")
```

## 2. wingetで開発ツールをインストールする

```powershell
# 1. インストールするパッケージを列挙
$PackageIds = @(
  'Microsoft.PowerShell'
  'Microsoft.VisualStudioCode'
  'jdx.mise'
  'astral-sh.uv'
  'jqlang.jq'
  'JohnMacFarlane.Pandoc'
  'BurntSushi.ripgrep.MSVC'
)

# 2. wingetでパッケージをインストール
foreach ($PackageId in $PackageIds) {
  winget install --exact --id $PackageId --source winget --scope user --accept-source-agreements --accept-package-agreements --disable-interactivity
}
```

## 3. craneをインストールする

- [crane](https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane.md)

```powershell
# 1. インストール先ディレクトリを作成
New-Item -ItemType Directory -Path "$HOME\.local\bin" -Force | Out-Null
# 2. crane をダウンロードして展開
curl.exe -fsSL -o "$env:TEMP\crane.tar.gz" https://github.com/google/go-containerregistry/releases/download/v0.22.1/go-containerregistry_Windows_x86_64.tar.gz; tar -xzf "$env:TEMP\crane.tar.gz" -C "$HOME\.local\bin" crane.exe
# 3. ユーザ環境変数 PATH に追加
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$HOME\.local\bin", "User")
```

## 4. miseで、Python/Node.jsをインストールする

```powershell
# 1. mise をユーザ環境変数  PATH に追加
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$env:LOCALAPPDATA\Microsoft\WinGet\Links", "User")

# 2. Python 3.14 と Node.js 24 LTS をインストール
mise use --global python@3.14 node@24

# 3. shims を更新
mise reshim

# 4. ユーザ環境変数 PATH の先頭に mise の shims を追加
[Environment]::SetEnvironmentVariable("Path", "$env:LOCALAPPDATA\mise\shims;" + [Environment]::GetEnvironmentVariable("Path", "User"), "User")
```

ここまでに設定した環境変数を反映するため、**PowerShellを開き直してから**次の手順へ進む。

## 5. npmパッケージをインストール

```powershell
# 1. npm パッケージをまとめてインストール
npm install --global @opencode/cli @openai/codex @anthropic-ai/claude-code @github/copilot git-cz markdownlint-cli2 pnpm typescript tsx vite-plus
# 2. インストールしたコマンドを mise の shims に反映
mise reshim
```

## 6. pipパッケージをインストール

```powershell
# 1. pip パッケージをまとめてインストール
python -m pip install ruff pre-commit pytest codespell yamllint graphifyy
# 2. インストールしたコマンドを mise の shims に反映
mise reshim
```

## 7. VSCode 拡張機能をインストールする

```powershell
# 1. VSCode 拡張機能を列挙
$ExtensionIds = @(
  'GitHub.copilot'
  'GitHub.copilot-chat'
  'ZooCodeOrganization.zoo-code'
  'anthropic.claude-code'
  'openai.chatgpt'
  'sst-dev.opencode-v2'
  'ms-vscode-remote.remote-wsl'
  'ms-vscode-remote.remote-containers'
  'ms-vscode-remote.remote-ssh'
  'ms-vscode.remote-server'
  'ms-vscode-remote.vscode-remote-extensionpack'
  'ms-python.python'
  'ms-python.vscode-pylance'
  'charliermarsh.ruff'
  'DavidAnson.vscode-markdownlint'
  'bierner.markdown-mermaid'
  'redhat.vscode-yaml'
  'tamasfe.even-better-toml'
)

# 2. VSCode 拡張機能をインストール
foreach ($ExtensionId in $ExtensionIds) {
    code --install-extension $ExtensionId --force
}
```

## 8. VSCode の設定を追加する

```json
{
    // Windows デフォルトのターミナルを PowerShell にする.
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    // Workspace Trust は有効のままにする。
    "security.workspace.trust.enabled": true,
    "security.workspace.trust.untrustedFiles": "prompt",
    // テレメトリーを無効化.
    "telemetry.telemetryLevel": "off",
    "telemetry.feedback.enabled": false,
    "workbench.enableExperiments": false,
    "docker-compose.enableTelemetry": false,
    "ox-ide.enableTelemetry": false,
    // 余計な UI を無効化.
    "chat.titleBar.signIn.enabled": false,
    "chat.titleBar.openInAgentsWindow.enabled": false,
    "chat.commandCenter.enabled": false,
    "workbench.settings.showAISearchToggle": false,
    "chat.viewTitle.enabled": false,
    // GitHub Copilot のローカル LLM を有効化.
    "chat.agentHost.byokModels.enabled": true,
    "chat.agentHost.allowSignedOutWhenUsable": true,
    "chat.byokUtilityModelDefault": "mainAgent",
    // ワークスペース外への書き込みには承認を要求。
    "chat.tools.terminal.blockDetectedFileWrites": "outsideWorkspace",
    // Agent のターミナルコマンドを勝手に承認しない.
    "chat.tools.terminal.enableAutoApprove": true,
    "chat.tools.global.autoApprove": false
}
```

## 9. コーディングエージェントにローカルLLMを設定する

OpenAI互換APIを提供するローカルLLMサーバ（vLLMなど）に接続する。

- URL: `http://localhost:8000/v1`
- APIキー: `<api-key>`
- モデルID: `<model-id>`

### 💙 GitHub Copilotで使う場合

`Ctrl+Shift+P`から`Chat: Manage Language Models`を開く

1. `Add Models`から`Custom Endpoint`を選ぶ
2. API Typeに`Chat Completions`を選ぶ
3. URLに`http://localhost:8000/v1/chat/completions`を設定する
4. API Keyに`<api-key>`、Model IDに`<model-id>`を設定する
5. Tool Calling対応モデルの場合は`toolCalling`を有効にする
6. Model Pickerから追加したモデルを選ぶ

### 💚 Codexで使う場合

Codexは、OpenAI互換APIのうちResponses API（`/v1/responses`）で接続する。
まず、CodexがAPIキーを参照するユーザ環境変数を設定する。

```powershell
# Codex が参照するAPIキーをユーザ環境変数に設定
[Environment]::SetEnvironmentVariable("LITELLM_MASTER_API_KEY", "<api-key>", "User")
```

次に、`%USERPROFILE%\.codex\config.toml`に以下を追加する。

```toml
# 1. ローカルLLMをデフォルトのモデルプロバイダーにする
model = "<model-id>"
model_provider = "local"

# 2. APIキーは上で設定した環境変数 LITELLM_MASTER_API_KEY から読み込む
[model_providers.local]
name = "Local LLM"
base_url = "http://localhost:8000/v1"
env_key = "LITELLM_MASTER_API_KEY"
```

### 🧡 Claude Codeで使う場合

Claude CodeはOpenAI互換APIではなく、Anthropic Messages API（`/v1/messages`）で接続する。
vLLMはMessages APIにも対応しているため、同じサーバに接続できる。
接続先には`/v1`を含めない。

```powershell
# Claude Code の接続先、APIキー、モデルをユーザ環境変数に設定
[Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "http://localhost:8000", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "<api-key>", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_MODEL", "<model-id>", "User")
```

### 💜 Zoo Codeで使う場合

1. `Settings`(⚙️)を開く
2. `Providers` タブを開く
3. 以下を入力する
   - `API Provider`: `OpenAI Compatible`
   - `Base URL`: `http://localhost:8000/v1`
   - `API Key`: `<api-key>`
   - `Model ID`: `<model-id>`

## 10. 重複したPATHを除去

ここまでの手順でユーザ環境変数PATHに重複して追加されたディレクトリを、順序を保ったまま除去する。

```powershell
# ユーザ環境変数 PATH の重複を除去
[Environment]::SetEnvironmentVariable("Path", (([Environment]::GetEnvironmentVariable("Path", "User") -split ';' | Where-Object { $_ } | Select-Object -Unique) -join ';'), "User")
```

PATHを反映するため、**PowerShellを開き直してから**次の手順へ進む。

## 11. 動作確認

```powershell
# インストールしたコマンドのバージョンを確認する
crane version
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

## 12. OpenSpecをプロジェクトに導入

```powershell
# 1. OpenSpec 1.17.0 をインストール
npm install --global @fission-ai/openspec@1.17.0
mise reshim
openspec --version

# 2. OpenSpecをプロジェクトへ導入
Set-Location -LiteralPath '<project-root>'
openspec init --tools agents --force --profile custom --no-animation
openspec config set telemetry.enabled false
```

## 13. 有用なAgent Skillsをインストール

### 🧠 Matt Pocock Skills

```powershell
# Matt Pocock Skills を導入
npx skills@latest add mattpocock/skills --agent universal --yes ask-matt code-review codebase-design diagnosing-bugs domain-modeling grill-me grill-with-docs grilling handoff implement improve-codebase-architecture prototype research resolving-merge-conflicts setup-matt-pocock-skills tdd teach to-questionnaire to-spec to-tickets triage wait-what wayfinder wizard writing-great-skills
```

### 📊 Graphify

```powershell
# 6.でインストールした Graphify をプロジェクトへ導入
graphify agents install --project
```

### 🌐 agent-browser

```powershell
# 1. agent-browser をインストール
npm install -g agent-browser
# 2. agent-browser を導入
npx agent-browser install
```

### 💻 プログラミング系スキル

```powershell
# 1. React
npx skills@latest add vercel-labs/agent-skills --agent universal --yes react-best-practices
# 2. Python
npx skills@latest add trailofbits/skills --agent universal --yes modern-python codeql insecure-defaults
# 3. Java / Spring Boot
npx skills@latest add github/awesome-copilot --agent universal --yes java-springboot spring-boot-testing
# 4. Ponytail; Tight coding
npx skills@latest add DietrichGebert/ponytail --agent universal --yes ponytail ponytail-review ponytail-audit
```

## 🔖 参考文献

- [Documentation for Visual Studio Code](https://code.visualstudio.com/docs)
- [PowerShell とは - PowerShell | Microsoft Learn](https://learn.microsoft.com/ja-jp/powershell/scripting/overview?view=powershell-7.6)
- [uv](https://docs.astral.sh/uv/)
- [jqlang/jq: Command-line JSON processor](https://github.com/jqlang/jq)
- [Pandoc - index](https://pandoc.org/)
- [BurntSushi/ripgrep: ripgrep recursively searches directories for a regex pattern while respecting your gitignore](https://github.com/burntsushi/ripgrep)
- [GitHub Copilot ドキュメント - GitHubドキュメント](https://docs.github.com/ja/copilot)
- [Advanced configuration - Codex](https://developers.openai.com/codex/config-advanced)
- [Connect Claude Code to an LLM gateway - Claude Code](https://code.claude.com/docs/en/llm-gateway-connect)
- [Zoo Code Docs | Zoo Code Documentation](https://docs.zoocode.dev/)
- [Fission-AI/OpenSpec: Spec-driven development (SDD) for AI coding assistants.](https://github.com/Fission-AI/OpenSpec)
- [mattpocock/skills: Skills for Real Engineers. Straight from my .agents directory.](https://github.com/mattpocock/skills)
- [Graphify-Labs/graphify: Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. A /graphify skill for Claude Code, Cursor, Codex, and Gemini CLI: local deterministic AST parsing, every edge explained, no vector store.](https://github.com/Graphify-Labs/graphify)
- [vLLM](https://docs.vllm.ai/en/latest/)
- [about_Telemetry - PowerShell | Microsoft Learn](https://learn.microsoft.com/ja-jp/powershell/module/microsoft.powershell.core/about/about_telemetry)
- [Data usage - Claude Code](https://docs.claude.com/en/docs/claude-code/data-usage)
- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [Vite+](https://viteplus.dev/guide)
- [pnpm](https://pnpm.io/)
- [Ruff](https://docs.astral.sh/ruff/)
- [pre-commit](https://pre-commit.com/)
