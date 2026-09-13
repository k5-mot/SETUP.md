# 📜 Windows開発環境セットアップ 2026年度版

## 1️⃣. wingetで開発ツールをインストールする

```powershell
# 開発ツールをUser Scopeへインストールする。
$ErrorActionPreference = 'Stop'

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

foreach ($PackageId in $PackageIds) {
  winget install --exact --id $PackageId --source winget --scope user `
    --accept-source-agreements --accept-package-agreements `
    --disable-interactivity
}
```

## 2️⃣. VSCode拡張機能をインストールする

```powershell
# 必要なVS Code拡張機能をインストールする。
$InstalledExtensions = @(code --list-extensions)
$ExtensionIds = @(
  'GitHub.copilot'
  'GitHub.copilot-chat'
  'ZooCodeOrganization.zoo-code'
)

foreach ($ExtensionId in $ExtensionIds) {
  if ($InstalledExtensions -notcontains $ExtensionId) {
    code --install-extension $ExtensionId
  }
}
```

## 3️⃣. VSCodeに設定を追加する

```json
{
    // WindowsデフォルトのターミナルをPowerShellにする.
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    // 余計なUIを無効化.
    "chat.titleBar.signIn.enabled": false,
    "chat.titleBar.openInAgentsWindow.enabled": false,
    // GitHub CopilotのローカルLLMを有効化.
    "chat.agentHost.byokModels.enabled": true,
    // テレメトリーを無効化.
    "telemetry.telemetryLevel": "off",
    "telemetry.feedback.enabled": false,
    "docker-compose.enableTelemetry": false,
    "ox-ide.enableTelemetry": false
}
```

## 4️⃣. コーディングエージェントにローカルLLMを設定する

### 🐙 GitHub Copilot Chatで使う場合

`Ctrl+Shift+P`から`Chat: Manage Language Models`を開く。

1. `Add Models`から`Custom Endpoint`を選ぶ。
2. API Typeに`Chat Completions`を選ぶ。
3. URLに`http://localhost:8000/v1/chat/completions`を設定する。
4. API Keyに`local`、Model IDに`<model-id>`を設定する。
5. Tool Calling対応モデルの場合は`toolCalling`を有効にする。
6. Model Pickerから追加したモデルを選ぶ。

### 🦓 Zoo Codeで使う場合

Zoo CodeのSettingsを開く。

| Backend | API Provider | Base URL | API Key | Model |
| --- | --- | --- | --- | --- |
| Ollama | `Ollama` | `http://localhost:11434` | 空欄 | `<model-name>` |
| vLLM | `OpenAI Compatible` | `http://localhost:8000/v1` | `local` | `<model-id>` |

設定を保存して接続を確認する。

## 5️⃣. OpenSpecをプロジェクトに導入する

```powershell
# OpenSpecをインストールしてプロジェクトへ導入する。
npm install --global @fission-ai/openspec@latest

Set-Location -LiteralPath '<project-root>'
openspec config profile # propose、apply、verify、archiveを選択
openspec init --tools agents --force --profile custom --no-animation
openspec config set telemetry.enabled false
```

## 6️⃣. 動作確認

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

## #️⃣. その他のAgent Skillsを導入する (任意)

<details>
<summary>Matt Pocock Skills</summary>

```powershell
# Matt Pocock Skillsを.agents/skillsへ追加する。
npx skills@latest add mattpocock/skills `
  --skill setup-matt-pocock-skills `
  --agent github-copilot --copy --yes
```

</details>

<details>
<summary>Graphify</summary>

```powershell
# GraphifyをインストールしてSkillを.agents/skillsへ追加する。
uv tool install graphifyy
graphify agents install --project
```

</details>

## References

- [VS Code: AI language models](https://code.visualstudio.com/docs/agent-customization/language-models)
- [vLLM: OpenAI-Compatible Server](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/)
- [vLLM: GPU Installation](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/)
- [Zoo Code: Ollama](https://github.com/Zoo-Code-Org/Zoo-Code-Docs/blob/main/docs/providers/ollama.md)
- [OpenSpec: Supported Tools](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)
