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
$ExpectedOutput = [IO.Path]::ChangeExtension($InputFile.FullName, '.docx')

if (-not $OutputFile.Equals(
    $ExpectedOutput,
    [StringComparison]::OrdinalIgnoreCase
  )) {
  throw "OutputPath must be: $ExpectedOutput"
}

$OutputDirectory = Split-Path -Parent $OutputFile

$MiseCommand = Get-Command mise -CommandType Application -ErrorAction SilentlyContinue |
  Select-Object -First 1
if (-not $MiseCommand) {
  throw 'mise is required.'
}

[void][IO.Directory]::CreateDirectory($OutputDirectory)

& $MiseCommand.Source exec 'pandoc@3.11' -- pandoc `
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
