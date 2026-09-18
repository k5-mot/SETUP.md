---
name: markdown2docx
description: openspec/publics配下のMySDD正本MarkdownをPandocで同名のDOCXへ変換する場合に使用する。本文の作成には使用しない。
---

# MarkdownをDOCXへ変換する

`openspec/publics/`配下のMarkdownパスを1つ受け取る。出力先は同じディレクトリと
ベース名を使用し、拡張子を`.docx`とする。参照文書には
`openspec/publics/template.docx`を使用する。

## 入力を検証する

すべてのパスをRepository RootからLiteral Pathとして解決する。入力または参照文書が
存在しない場合、入力が`openspec/publics/`の外部にある場合、または出力条件を
満たせない場合は変換前に停止する。変換前に入力のSHA-256 Hashを記録する。

## DOCXへ変換する

<!-- markdownlint-disable MD013 -->

```powershell
# miseで固定したPandocを実行し、共通の参照文書を適用する。
mise exec pandoc@3.11 -- pandoc '<input.md>' --from=gfm --to=docx --reference-doc='openspec/publics/template.docx' --output='<same-basename.docx>'

# 本文10pt、表紙、目次、章改ページ、中央配置の表および注意ブロック配色を適用する。
mise exec python@3.12 -- python '.agents/skills/markdown2docx/scripts/format_docx.py' generated '<same-basename.docx>'
```

<!-- markdownlint-enable MD013 -->

## 検証して報告する

Pandocと整形Scriptが正常終了したこと、DOCXが存在して空でないこと、入力の
SHA-256 Hashが変化していないことを確認する。Wordを利用できる場合は全Fieldを
更新して保存し、目次へ最新の見出しとPage番号を反映する。成功時はDOCXの絶対Pathを
返す。いずれかに失敗した場合は入力Markdownを保持し、呼び出し元へ部分成功として
報告する。すべての確認に合格していないDOCXを利用可能として報告しない。
