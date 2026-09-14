# 🧰 Windows開発環境セットアップ 完全版

最小構成は[SETUP.md](./SETUP.md)、設計判断は[ADR.md](../adr/ADR.md)を参照する。

## 1️⃣. wingetでツールをインストールする

```powershell
# 開発ツールをUser Scopeへインストールする。
$ErrorActionPreference = 'Stop'

$PackageIds = @(
  'Git.Git'
  'GitHub.cli'
  'OpenJS.NodeJS.LTS'
  'Python.Python.3.12'
  'Microsoft.PowerShell'
  'Microsoft.WindowsTerminal'
  'Microsoft.VisualStudioCode'
  'twpayne.chezmoi'
  'JanDeDobbeleer.OhMyPosh'
  'jdx.mise'
  'astral-sh.uv'
  'jqlang.jq'
  'JohnMacFarlane.Pandoc'
  'sharkdp.bat'
  'Clement.bottom'
  'dandavison.delta'
  'bootandy.dust'
  'sharkdp.fd'
  'sharkdp.hyperfine'
  'BurntSushi.ripgrep.MSVC'
  'ajeetdsouza.zoxide'
  'lsd-rs.lsd'
  'Dystroy.broot'
  'ducaale.xh'
  'chmln.sd'
  'svenstaro.genact'
  'Terrastruct.D2'
)

foreach ($PackageId in $PackageIds) {
  winget install --exact --id $PackageId --source winget --scope user `
    --accept-source-agreements --accept-package-agreements `
    --disable-interactivity
}

$MachinePath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
$UserPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$env:Path = @($MachinePath, $UserPath) -join ';'
```

## 2️⃣. VS Codeを設定する

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

User Settingsへ追加する。

```jsonc
{
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "chat.agentHost.byokModels.enabled": true,
  "telemetry.telemetryLevel": "off",
  "telemetry.feedback.enabled": false
}
```

## 3️⃣. ローカルLLMを設定する

### 🦙 Ollama

```powershell
# Ollamaへモデルを取得する。
ollama pull '<model-name>'
```

Endpointは`http://localhost:11434`を使う。

### 🚀 vLLM

WSL2またはLinuxホストで起動する。

```bash
# vLLMのOpenAI互換サーバーを起動する。
vllm serve <model-id> --host 0.0.0.0 --port 8000 --api-key local
```

Endpointは`http://localhost:8000/v1`を使う。

### 🐙 GitHub Copilot Chat

`Chat: Manage Language Models`から`Custom Endpoint`を追加する。

| 項目 | 値 |
| --- | --- |
| API Type | `Chat Completions` |
| URL | `http://localhost:8000/v1/chat/completions` |
| API Key | `local` |
| Model ID | `<model-id>` |

### 🦓 Zoo Code

| Backend | Provider | Base URL | API Key |
| --- | --- | --- | --- |
| Ollama | `Ollama` | `http://localhost:11434` | 空欄 |
| vLLM | `OpenAI Compatible` | `http://localhost:8000/v1` | `local` |

## 4️⃣. CLIをインストールする

```powershell
# Coding Agent用CLIをインストールする。
npm install --global @openai/codex @fission-ai/openspec@latest
uv tool install graphifyy
```

## 5️⃣. dotfilesを適用する

```powershell
# dotfilesを取得して適用する。
chezmoi init --apply https://github.com/k5-mot/dotfiles.git
chezmoi doctor
```

## 6️⃣. craneをインストールする

```powershell
# craneをUser-localディレクトリへインストールする。
$ErrorActionPreference = 'Stop'
$BinDir = Join-Path $env:USERPROFILE '.local\bin'
$WorkDir = Join-Path $env:TEMP ('crane-' + [guid]::NewGuid().ToString('N'))

New-Item -ItemType Directory -Force -Path $BinDir, $WorkDir | Out-Null

try {
  $Release = Invoke-RestMethod `
    -Headers @{ 'User-Agent' = 'windows-dev-setup' } `
    -Uri 'https://api.github.com/repos/google/go-containerregistry/releases/latest'
  $Asset = $Release.assets |
    Where-Object name -EQ 'go-containerregistry_Windows_x86_64.tar.gz' |
    Select-Object -First 1
  if (-not $Asset) { throw 'crane asset was not found.' }

  $Archive = Join-Path $WorkDir $Asset.name
  Invoke-WebRequest -Uri $Asset.browser_download_url -OutFile $Archive
  tar.exe -xf $Archive -C $WorkDir
  Copy-Item -LiteralPath (Join-Path $WorkDir 'crane.exe') `
    -Destination $BinDir -Force
} finally {
  Remove-Item -LiteralPath $WorkDir -Recurse -Force
}
```

`%USERPROFILE%\.local\bin`をUser PATHへ追加する。

## 7️⃣. OpenSpecを導入する

```powershell
# OpenSpecをプロジェクトへ導入する。
Set-Location -LiteralPath '<project-root>'
openspec config profile # propose、apply、verify、archiveを選択
openspec init --tools agents --force --profile custom --no-animation
openspec config set telemetry.enabled false
```

使い方は[OpenSpec開発ワークフロー](../references/workflow.md)を参照する。

## 8️⃣. Agent Skillsを導入する

```powershell
# Agent Skillsを.agents/skillsへ追加する。
Set-Location -LiteralPath '<project-root>'

npx skills@latest add vercel-labs/agent-skills `
  --skill react-best-practices --agent universal --copy --yes
npx skills@latest add trailofbits/skills `
  --skill modern-python --skill codeql --skill insecure-defaults `
  --agent universal --copy --yes
npx skills@latest add github/awesome-copilot `
  --skill java-springboot --skill spring-boot-testing `
  --agent universal --copy --yes
npx skills@latest add DietrichGebert/ponytail `
  --skill ponytail --skill ponytail-review --skill ponytail-audit `
  --agent universal --copy --yes

graphify agents install --project
```

Skillsは`.agents/skills/`へ配置する。

<details>
<summary>Matt Pocock Skills</summary>

```powershell
# Matt Pocock Skillsを.agents/skillsへ追加する。
npx skills@latest add mattpocock/skills `
  --skill setup-matt-pocock-skills `
  --agent universal --copy --yes
```

</details>

## 9️⃣. agent-browserを導入する

```powershell
# agent-browserをプロジェクト依存として追加する。
Set-Location -LiteralPath '<project-root>'
npm install --save-dev agent-browser
npx agent-browser install
```

## 🔟. 確認する

```powershell
# 必須コマンドとAgent Skillsを確認する。
$Commands = @(
  'git', 'gh', 'node', 'npm', 'python', 'pwsh', 'code',
  'chezmoi', 'oh-my-posh', 'mise', 'uv', 'jq', 'pandoc',
  'rg', 'fd', 'bat', 'd2', 'crane', 'codex', 'openspec', 'graphify'
)

$Missing = @($Commands | Where-Object {
  -not (Get-Command $_ -ErrorAction SilentlyContinue)
})
if ($Missing.Count -gt 0) { throw "Missing: $($Missing -join ', ')" }

Get-ChildItem -Path '.agents\skills' -Recurse -Filter SKILL.md
git status --short
```

## 🛠️. トラブルシューティング

### WinGetが見つからない

Microsoft Storeで「アプリ インストーラー」を更新し、PowerShellを開き直す。

### インストールしたコマンドが見つからない

PowerShellを開き直す。解決しない場合は次をUser PATHへ追加する。

```text
%LOCALAPPDATA%\Microsoft\WinGet\Links
%APPDATA%\npm
%USERPROFILE%\.local\bin
```

## References

- [VS Code: AI language models](https://code.visualstudio.com/docs/agent-customization/language-models)
- [vLLM: OpenAI-Compatible Server](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/)
- [OpenSpec: Supported Tools](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)
- [Skills CLI](https://www.skills.sh/docs/cli)
