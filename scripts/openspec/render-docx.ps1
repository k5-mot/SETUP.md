[CmdletBinding()]
param(
  [Parameter(Mandatory)]
  [string]$InputPath,

  [Parameter(Mandatory)]
  [string]$OutputPath,

  [Parameter(Mandatory)]
  [string]$ReferenceDoc
)

$ErrorActionPreference = 'Stop'

$InputFile = Get-Item -LiteralPath $InputPath -ErrorAction Stop
$ReferenceFile = Get-Item -LiteralPath $ReferenceDoc -ErrorAction Stop
$OutputFile = [IO.Path]::GetFullPath($OutputPath)
$OutputDirectory = Split-Path -Parent $OutputFile

if (-not (Get-Command mise -ErrorAction SilentlyContinue)) {
  throw 'mise is required.'
}

[void][IO.Directory]::CreateDirectory($OutputDirectory)

& mise exec 'pandoc@3.11' -- pandoc `
  $InputFile.FullName `
  '--from=gfm' `
  '--to=docx' `
  "--reference-doc=$($ReferenceFile.FullName)" `
  "--output=$OutputFile"

if ($LASTEXITCODE -ne 0) {
  throw "Pandoc conversion failed: $InputPath"
}

$Result = Get-Item -LiteralPath $OutputFile -ErrorAction Stop
if ($Result.Length -eq 0) {
  throw "DOCX is empty: $OutputFile"
}

$Result.FullName
