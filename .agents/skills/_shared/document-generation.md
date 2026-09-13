# 📄 文書生成の共通手順

1. `change-name`を受け取る。未指定または複数候補がある場合は利用者へ確認する。
2. miseを有効化し、`openspec context --json`でOpenSpecルートを解決する。
3. Skill固有の必須入力を確認する。不足時は不足パスを報告し、生成完了を報告しない。
4. 入力Artifactをすべて読み、Skill固有の章立てでMarkdownを生成する。
5. 入力にない事実を追加せず、不足情報は`TBD`とする。既存IDと参照関係は変更しない。
6. 出力は対象Changeの`openspec/artifacts/<change-name>/`配下だけへ書く。
7. 次のRendererでDOCXを生成する。

```powershell
# 正本Markdownから配布用DOCXを生成する。
.\scripts\openspec\render-docx.ps1 `
  -InputPath '<output.md>' `
  -OutputPath '<output.docx>' `
  -ReferenceDoc '.\openspec\document-templates\reference.docx'
```

DOCX生成に失敗した場合はMarkdownを保持し、部分成功と失敗理由を報告する。
