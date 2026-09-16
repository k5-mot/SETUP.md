---
name: md2docx
description: MySDD文書の正本MarkdownをPandocで同名DOCXへ変換する。gen-pdまたはgen-bdがDOCX生成を委譲するときに使用する。文書内容の作成には使用しない。
---

# md2docx

正本Markdownの内容を変更せず、Project共通書式のDOCXへ変換する。

## 入力

- `InputPath`: 変換元Markdown
- `OutputPath`: 変換先DOCX

参照書式には`openspec/document-templates/reference.docx`を使う。

## 変換

1. Repository rootをCurrent Directoryにする。
1. `InputPath`と参照書式をLiteral pathとして解決する。存在しないPathを
   報告し、変換を開始しない。
1. `OutputPath`を絶対Pathへ解決する。入力と同じDirectory、同じBase name、
   `.docx`拡張子でない場合は、期待するPathを報告して変換を開始しない。
1. 入力MarkdownのHashを記録する。
1. 次のRendererを実行する。このRendererがmise管理のPandocを使用する。

```powershell
# 正本MarkdownをProject共通書式のDOCXへ変換する。
./.agents/skills/md2docx/scripts/render-docx.ps1 `
  -InputPath '<resolved-input-path>' `
  -OutputPath '<resolved-output-path>' `
  -ReferenceDoc './openspec/document-templates/reference.docx'
```

1. Rendererが返したDOCXが存在し、非ゼロSizeであることを確認する。
1. 入力MarkdownのHashが変換前と一致することを確認する。

## 完了条件

成功時は生成したDOCXの絶対Pathを返す。入力Markdown、参照書式、生成DOCX
以外のファイルを変更しない。

Renderer、出力確認、またはHash確認が失敗した場合は成功を報告しない。
呼び出し元が生成済みのMarkdownを保持したまま、部分成功と失敗理由を返す。
