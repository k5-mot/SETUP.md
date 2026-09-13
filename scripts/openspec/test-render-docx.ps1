[CmdletBinding()]
param(
  [string]$ReferenceDoc = (
    Join-Path $PSScriptRoot '..\..\openspec\document-templates\reference.docx'
  )
)

$ErrorActionPreference = 'Stop'
$TempBase = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
$TestRoot = [IO.Path]::GetFullPath(
  (Join-Path $TempBase ('gen-doc-' + [guid]::NewGuid().ToString('N')))
)

if (-not $TestRoot.StartsWith($TempBase, [StringComparison]::OrdinalIgnoreCase)) {
  throw "Unsafe test directory: $TestRoot"
}

[void][IO.Directory]::CreateDirectory($TestRoot)

try {
  $InputPath = Join-Path $TestRoot 'sample.md'
  $OutputPath = Join-Path $TestRoot 'sample.docx'
  [IO.File]::WriteAllText(
    $InputPath,
    "# 📋 要件定義書`n`n| ID | 要求 |`n| --- | --- |`n| REQ-001 | ログインできること |`n",
    [Text.UTF8Encoding]::new($false)
  )

  & (Join-Path $PSScriptRoot 'render-docx.ps1') `
    -InputPath $InputPath `
    -OutputPath $OutputPath `
    -ReferenceDoc $ReferenceDoc | Out-Null

  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $Archive = [IO.Compression.ZipFile]::OpenRead($OutputPath)
  try {
    $DocumentEntry = $Archive.GetEntry('word/document.xml')
    if (-not $DocumentEntry) { throw 'word/document.xml is missing.' }
    $Reader = [IO.StreamReader]::new($DocumentEntry.Open())
    try {
      $Xml = $Reader.ReadToEnd()
    } finally {
      $Reader.Dispose()
    }
    if (-not $Xml.Contains('REQ-001')) { throw 'Expected requirement ID is missing.' }
  } finally {
    $Archive.Dispose()
  }

  'render-docx: PASS'
} finally {
  if (Test-Path -LiteralPath $TestRoot) {
    Remove-Item -LiteralPath $TestRoot -Recurse -Force
  }
}
