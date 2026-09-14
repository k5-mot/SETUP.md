# 📄 文書生成の共通手順

1. `change-name`を受け取る。未指定または複数候補がある場合は利用者へ確認する。
2. miseを有効化し、対象ChangeのStatusとSkill固有のArtifact指示を取得する。
3. 指示の`dependencies`とSkill固有の任意入力を読む。必須入力の不足時は不足パスを報告し、生成完了を報告しない。
4. 指示のTemplateに従い、`resolvedOutputPath`へMarkdownを生成する。
5. 入力にない事実を追加せず、不足情報は`TBD`とする。Requirement見出し、Scenario名、既存IDと参照関係は変更しない。
6. Markdownと同じディレクトリへ同名のDOCXを生成する。それ以外のパスへ書かない。
7. 次のRendererでDOCXを生成する。

```powershell
# 正本Markdownから配布用DOCXを生成する。
.\scripts\openspec\render-docx.ps1 `
  -InputPath '<resolved-output-path>' `
  -OutputPath '<same-name.docx>' `
  -ReferenceDoc '.\openspec\document-templates\reference.docx'
```

DOCX生成に失敗した場合はMarkdownを保持し、部分成功と失敗理由を報告する。
