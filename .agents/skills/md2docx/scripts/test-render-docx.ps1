[CmdletBinding()]
param(
  [string]$ReferenceDoc = (
    Join-Path $PSScriptRoot '..\..\..\..\openspec\document-templates\reference.docx'
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
  Add-Type -AssemblyName System.IO.Compression.FileSystem

  $Cases = @(
    @{ Name = 'rd'; Title = '要件定義書'; Id = 'REQ-001' }
    @{ Name = 'bd'; Title = '基本設計書'; Id = 'DES-001' }
  )

  foreach ($Case in $Cases) {
    $InputPath = Join-Path $TestRoot "$($Case.Name).md"
    $OutputPath = Join-Path $TestRoot "$($Case.Name).docx"
    [IO.File]::WriteAllText(
      $InputPath,
      "# $($Case.Title)`n`n| ID | 内容 |`n| --- | --- |`n| $($Case.Id) | テスト |`n",
      [Text.UTF8Encoding]::new($false)
    )
    $InputHash = (Get-FileHash -LiteralPath $InputPath -Algorithm SHA256).Hash

    & (Join-Path $PSScriptRoot 'render-docx.ps1') `
      -InputPath $InputPath `
      -OutputPath $OutputPath `
      -ReferenceDoc $ReferenceDoc | Out-Null

    $OutputFile = Get-Item -LiteralPath $OutputPath -ErrorAction Stop
    if ($OutputFile.Length -eq 0) { throw "DOCX is empty: $OutputPath" }
    $ResultHash = (Get-FileHash -LiteralPath $InputPath -Algorithm SHA256).Hash
    if ($ResultHash -ne $InputHash) { throw "Markdown changed: $InputPath" }

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
      if (-not $Xml.Contains($Case.Id)) {
        throw "Expected ID is missing: $($Case.Id)"
      }
    } finally {
      $Archive.Dispose()
    }
  }

  $MissingOutput = Join-Path $TestRoot 'missing.docx'
  try {
    & (Join-Path $PSScriptRoot 'render-docx.ps1') `
      -InputPath (Join-Path $TestRoot 'missing.md') `
      -OutputPath $MissingOutput `
      -ReferenceDoc $ReferenceDoc | Out-Null
    throw 'Missing input did not fail.'
  } catch {
    if ($_.Exception.Message -eq 'Missing input did not fail.') { throw }
  }
  if (Test-Path -LiteralPath $MissingOutput) {
    throw "Unexpected DOCX exists: $MissingOutput"
  }

  $MissingReferenceInput = Join-Path $TestRoot 'missing-reference.md'
  $MissingReferenceOutput = Join-Path $TestRoot 'missing-reference.docx'
  [IO.File]::WriteAllText(
    $MissingReferenceInput,
    "# 参照書式検証`n",
    [Text.UTF8Encoding]::new($false)
  )
  try {
    & (Join-Path $PSScriptRoot 'render-docx.ps1') `
      -InputPath $MissingReferenceInput `
      -OutputPath $MissingReferenceOutput `
      -ReferenceDoc (Join-Path $TestRoot 'missing-reference.docx') | Out-Null
    throw 'Missing reference did not fail.'
  } catch {
    if ($_.Exception.Message -eq 'Missing reference did not fail.') { throw }
  }
  if (Test-Path -LiteralPath $MissingReferenceOutput) {
    throw "Unexpected DOCX exists: $MissingReferenceOutput"
  }

  $InvalidInput = Join-Path $TestRoot 'invalid.md'
  $InvalidOutput = Join-Path $TestRoot 'different.docx'
  [IO.File]::WriteAllText(
    $InvalidInput,
    "# 出力先検証`n",
    [Text.UTF8Encoding]::new($false)
  )
  try {
    & (Join-Path $PSScriptRoot 'render-docx.ps1') `
      -InputPath $InvalidInput `
      -OutputPath $InvalidOutput `
      -ReferenceDoc $ReferenceDoc | Out-Null
    throw 'Invalid output path did not fail.'
  } catch {
    if ($_.Exception.Message -eq 'Invalid output path did not fail.') { throw }
  }
  if (Test-Path -LiteralPath $InvalidOutput) {
    throw "Unexpected DOCX exists: $InvalidOutput"
  }

  'render-docx: PASS'
} finally {
  if (Test-Path -LiteralPath $TestRoot) {
    Remove-Item -LiteralPath $TestRoot -Recurse -Force
  }
}
