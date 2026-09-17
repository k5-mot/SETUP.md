# 🚀 Windows開発環境セットアップ 2026年度版

<!-- markdownlint-disable MD013 -->

## 1️⃣ wingetで開発ツールをインストールする

```powershell
### インストールするパッケージを列挙.
$PackageIds = @(
  'Git.Git'
  'OpenJS.NodeJS.LTS'
  'Python.Python.3.12'
  'Microsoft.PowerShell'
  'Microsoft.VisualStudioCode'
  'astral-sh.uv'
  'jqlang.jq'
  'JohnMacFarlane.Pandoc'
  'BurntSushi.ripgrep.MSVC'
)

### wingetでパッケージをインストール.
foreach ($PackageId in $PackageIds) {
  winget install --exact --id $PackageId --source winget --scope user --accept-source-agreements --accept-package-agreements --disable-interactivity
}
```

## 2️⃣ VSCode 拡張機能をインストールする

```powershell
### VSCode 拡張機能を列挙.
$ExtensionIds = @(
  'GitHub.copilot'
  'GitHub.copilot-chat'
  'ZooCodeOrganization.zoo-code'
)

### VSCode 拡張機能をインストール.
foreach ($ExtensionId in $ExtensionIds) {
    code --install-extension $ExtensionId --force
}
```

## 3️⃣ VSCode の設定を追加する

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
    "chat.tools.global.autoApprove": false,
    // 読み取り系だけ自動承認。
    "chat.tools.terminal.autoApprove": {
        // PowerShell
        "Get-ChildItem": true,
        "Get-Item": true,
        "Get-Content": true,
        "Get-Location": true,
        "Resolve-Path": true,
        "Test-Path": true,
        "Select-String": true,
        "Get-FileHash": true,
        "Get-Command": true,
        "Out-String": true,
        "where": true,
        "/^pwsh\\s+(?:--version|-v)\\s*$/i": true,
        // Linux
        "dir": true,
        "ls": true,
        "cat": true,
        "pwd": true,
        "type": true,
        "head": true,
        "tail": true,
        "wc": true,
        "grep": true,
        "stat": true,
        "file": true,
        "which": true,
        "realpath": true,
        "readlink": true,
        "basename": true,
        "dirname": true,
        "cut": true,
        "uniq": true,
        "tr": true,
        // Git
        "/^git\\s+--version\\s*$/i": true,
        "/^git\\s+(?:(?:-C\\s+(?:\"[^\"]+\"|'[^']+'|\\S+)\\s+)|(?:--no-pager\\s+))*(?:status|log|show|diff|ls-files|rev-parse|rev-list|describe)\\b/i": true,
        "/^git\\s+branch\\s+(?:--list|-l)(?:\\s|$)/i": true,
        "/^git\\s+tag\\s+(?:--list|-l)(?:\\s|$)/i": true,
        "/^git\\s+remote\\s*$/i": true,
        "/^git\\s+remote\\s+(?:-v|--verbose)\\s*$/i": true,
        // ripgrep
        "rg": true,
        "/^rg\\b.*(?:--pre(?:=|\\s)|--hostname-bin(?:=|\\s))/i": false,
        // jq
        "jq": true,
        // Node.js / npm / pnpm / Corepack
        "/^node\\s+(?:--version|-v|--help|-h)\\s*$/i": true,
        "/^npm\\s+(?:--version|-v|--help|-h)\\s*$/i": true,
        "/^npm\\s+(?:ls|list|root|prefix|explain|query)\\b/i": true,
        "/^npm\\s+config\\s+get\\b/i": true,
        "/^corepack\\s+--version\\s*$/i": true,
        "/^npm\\s+run\\s+(?:lint|test|typecheck|type-check|check)\\s*$/i": true,
        "/^npm\\s+test\\s*$/i": true,
        "/^pnpm\\s+(?:ls|list|why|root)\\b/i": true,
        "/^pnpm\\s+config\\s+get\\b/i": true,
        "/^pnpm\\s+run\\s+(?:lint|test|typecheck|type-check|check)\\s*$/i": true,
        "/^pnpm\\s+test\\s*$/i": true,
        // Python / pip
        "/^python(?:3(?:\\.\\d+)?)?\\s+(?:--version|-V|--help|-h)\\s*$/i": true,
        "/^py\\s+(?:-3(?:\\.\\d+)?\\s+)?(?:--version|-V|--help|-h)\\s*$/i": true,
        "/^pip(?:3(?:\\.\\d+)?)?\\s+--version\\s*$/i": true,
        "/^pip(?:3(?:\\.\\d+)?)?\\s+(?:list|check)\\s*$/i": true,
        "/^pip(?:3(?:\\.\\d+)?)?\\s+(?:show|freeze|inspect)\\b/i": true,
        "/^python(?:3(?:\\.\\d+)?)?\\s+-m\\s+pip\\s+--version\\s*$/i": true,
        "/^python(?:3(?:\\.\\d+)?)?\\s+-m\\s+pip\\s+(?:list|check)\\s*$/i": true,
        "/^python(?:3(?:\\.\\d+)?)?\\s+-m\\s+pip\\s+(?:show|freeze|inspect)\\b/i": true,
        "/^py\\s+(?:-3(?:\\.\\d+)?\\s+)?-m\\s+pip\\s+--version\\s*$/i": true,
        "/^py\\s+(?:-3(?:\\.\\d+)?\\s+)?-m\\s+pip\\s+(?:list|check)\\s*$/i": true,
        "/^py\\s+(?:-3(?:\\.\\d+)?\\s+)?-m\\s+pip\\s+(?:show|freeze|inspect)\\b/i": true,
        // uv
        "/^uv\\s+(?:--version|--help|-h)\\s*$/i": true,
        "/^uv\\s+version\\s*$/i": true,
        "/^uv\\s+pip\\s+(?:list|check)\\s*$/i": true,
        "/^uv\\s+pip\\s+(?:show|freeze|tree)\\b/i": true,
        "/^uv\\s+tool\\s+list\\s*$/i": true,
        "/^uv\\s+tool\\s+dir(?:\\s+--bin)?\\s*$/i": true,
        "/^uv\\s+python\\s+list\\b(?=.*--only-installed\\b)/i": true,
        "/^uv\\s+python\\s+dir\\s*$/i": true,
        "/^uv\\s+cache\\s+dir\\s*$/i": true,
        "/^uv\\s+tree\\b(?=.*(?:--locked|--frozen)\\b)/i": true,
        "/^uv\\s+lock\\s+--check-exists\\s*$/i": true,
        "/^uv\\s+run\\s+--no-sync\\s+pytest(?:\\s|$)/i": true,
        "/^uv\\s+run\\s+--no-sync\\s+ruff\\s+check(?:\\s|$)/i": true,
        "/^uv\\s+run\\b.*\\bruff\\s+check\\b.*(?:--fix|--unsafe-fixes)\\b/i": false,
        "/^uv\\s+run\\s+--no-sync\\s+ty\\s+check(?:\\s|$)/i": true,
        "/^uv\\s+run\\b.*\\bty\\s+check\\b.*--add-ignore\\b/i": false,
        // VSCode
        "/^(?:code|code-insiders)\\s+--version\\s*$/i": true,
        "/^(?:code|code-insiders)\\s+--status\\s*$/i": true,
        "/^(?:code|code-insiders)\\s+(?:--help|-h)\\s*$/i": true,
        "/^(?:code|code-insiders)\\s+--list-extensions(?:\\s+--show-versions)?\\s*$/i": true,
        // Pandoc
        "/^pandoc\\s+(?:--version|-v|--help|-h)\\s*$/i": true,
        "/^pandoc\\s+(?:--list-input-formats|--list-output-formats|--list-highlight-languages|--list-highlight-styles)\\s*$/i": true,
        "/^pandoc\\s+--list-extensions(?:=[^\\s]+|\\s+[^\\s]+)?\\s*$/i": true,
        "/^pandoc\\s+--print-default-template(?:=[^\\s]+|\\s+[^\\s]+)\\s*$/i": true,
        // Docker
        "/^docker\\s+(?:--version|version|info)\\b/i": true,
        "/^docker\\s+(?:ps|inspect|images|logs|top|port)\\b/i": true,
        "/^docker\\s+container\\s+(?:ls|list|ps|inspect|logs|top|port)\\b/i": true,
        "/^docker\\s+image\\s+(?:ls|list|inspect|history)\\b/i": true,
        "/^docker\\s+network\\s+(?:ls|list|inspect)\\b/i": true,
        "/^docker\\s+volume\\s+(?:ls|list|inspect)\\b/i": true,
        "/^docker\\s+context\\s+(?:ls|list|show|inspect)\\b/i": true,
        "/^docker\\s+system\\s+df\\b/i": true,
        "/^docker\\s+compose\\s+(?:ps|images|logs|ls|version)\\b/i": true,
        "/^docker\\s+compose\\s+config\\b(?!.*(?:\\s-o(?:\\s|=)|--output(?:=|\\s)))/i": true,
        // Podman
        "/^podman\\s+(?:ps|container\\s+(?:ps|ls|list))\\b.*--sync\\b/i": false,
        "/^podman\\s+(?:--version|version|info)\\b/i": true,
        "/^podman\\s+(?:ps|inspect|images|logs|top|port)\\b/i": true,
        "/^podman\\s+container\\s+(?:ls|list|ps|inspect|logs|top|port)\\b/i": true,
        "/^podman\\s+image\\s+(?:ls|list|inspect|history|tree)\\b/i": true,
        "/^podman\\s+network\\s+(?:ls|list|inspect)\\b/i": true,
        "/^podman\\s+volume\\s+(?:ls|list|inspect)\\b/i": true,
        "/^podman\\s+pod\\s+(?:ps|inspect)\\b/i": true,
        "/^podman\\s+system\\s+df\\b/i": true,
        "/^podman\\s+machine\\s+(?:list|ls|inspect)\\b/i": true
    },
    "zoo-code.allowedCommands": [
        "git log",
        "git diff",
        "git show",
        "mkdir",
        "python",
        "ls",
        "cp",
        "cd",
        "uv",
        "uv run",
        "uv run python"
    ],
    "zoo-code.deniedCommands": [],
}
```

## 4️⃣ コーディングエージェントにローカルLLMを設定する

### 🐙 GitHub Copilot Chatで使う場合

`Ctrl+Shift+P`から`Chat: Manage Language Models`を開く

1. `Add Models`から`Custom Endpoint`を選ぶ
2. API Typeに`Chat Completions`を選ぶ
3. URLに`http://localhost:8000/v1/chat/completions`を設定する
4. API Keyに`local`、Model IDに`<model-id>`を設定する
5. Tool Calling対応モデルの場合は`toolCalling`を有効にする
6. Model Pickerから追加したモデルを選ぶ

### 🦓 Zoo Codeで使う場合

1. `Settings`(⚙️)を開く
2. `Providers` タブを開く
3. 以下を入力する

#### Ollamaの場合

- `API Provider`: `Ollama`
- `Base URL`: `http://localhost:11434`
- `API Key`: `EMPTY`
- `Model Name`: `<model-name>`

#### vLLMの場合

- `API Provider`: `OpenAI Compatible`
- `Base URL`: `http://localhost:8000/v1`
- `API Key`: `local`
- `Model ID`: `<model-id>`

## 5️⃣ OpenSpecをプロジェクトに導入する

```powershell
### OpenSpecをインストール.
npm install --global @fission-ai/openspec@latest

### OpenSpecをプロジェクトへ導入.
Set-Location -LiteralPath '<project-root>'
openspec init --tools agents --force --profile custom --no-animation
openspec config set telemetry.enabled false
```

## 6️⃣ 動作確認

```powershell
# インストールしたコマンドのバージョンを確認する。
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
```

<!-- markdownlint-enable MD013 -->

## 🔖 参考文献

- [Documentation for Visual Studio Code](https://code.visualstudio.com/docs)
- [PowerShell とは - PowerShell | Microsoft Learn](https://learn.microsoft.com/ja-jp/powershell/scripting/overview?view=powershell-7.6)
- [uv](https://docs.astral.sh/uv/)
- [jqlang/jq: Command-line JSON processor](https://github.com/jqlang/jq)
- [Pandoc - index](https://pandoc.org/)
- [BurntSushi/ripgrep: ripgrep recursively searches directories for a regex pattern while respecting your gitignore](https://github.com/burntsushi/ripgrep)
- [GitHub Copilot ドキュメント - GitHubドキュメント](https://docs.github.com/ja/copilot)
- [Zoo Code Docs | Zoo Code Documentation](https://docs.zoocode.dev/)
- [Fission-AI/OpenSpec: Spec-driven development (SDD) for AI coding assistants.](https://github.com/Fission-AI/OpenSpec)
- [mattpocock/skills: Skills for Real Engineers. Straight from my .agents directory.](https://github.com/mattpocock/skills)
- [Graphify-Labs/graphify: Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. A /graphify skill for Claude Code, Cursor, Codex, and Gemini CLI: local deterministic AST parsing, every edge explained, no vector store.](https://github.com/Graphify-Labs/graphify)
- [Introduction - Ollama](https://docs.ollama.com/api/introduction)
- [vLLM](https://docs.vllm.ai/en/latest/)
