---
name: markdown2docx
description: openspec/publics配下のMySDD正本MarkdownをPandocで同名のDOCXへ変換する場合に使用する。本文の作成には使用しない。
---

# MarkdownをDOCXへ変換する

`openspec/publics/`配下のMarkdown Pathを1つ受け取る。出力先は同じDirectoryと
Base Nameを使用し、拡張子を`.docx`とする。参照文書には
`references/template.docx`を使用する。書式の変更または障害調査では、先に
[書式仕様](references/style.md)を読む。

## 入力を検証する

Repository Rootから入力と参照文書をLiteral Pathとして解決し、次を確認する。

- 入力が存在し、`openspec/publics/`の直下にあるMarkdownである
- 出力が入力と同じDirectoryおよびBase NameのDOCXである
- `.agents/skills/markdown2docx/references/template.docx`が存在する
- 入力の先頭YAML Metadataに空でない`title`がある

いずれかを満たさない場合はPandocを実行せず、許可されたPathまたは不足した条件を
報告する。変換前に入力のSHA-256 Hashを記録する。

## DOCXへ変換する

Pandoc 3.11を入力ごとに1回実行した後、同梱の`main.py`でNavigation見出し、
表Captionおよび余白を確定し、Field対応Office Engineで表示内容を更新する。
WindowsではMicrosoft Wordを使用する。LinuxではLibreOffice WriterとPython UNOで
配置を2回計算し、図表CaptionとPage番号を一覧の表示結果へ確定する。

<!-- markdownlint-disable MD013 -->

```powershell
pandoc '<input.md>' --from='gfm+implicit_figures' --to=docx --standalone --reference-doc='.agents/skills/markdown2docx/references/template.docx' --toc --toc-depth=6 --lof --lot --metadata='toc-title:目次' --metadata='lof-title:図一覧' --metadata='lot-title:表一覧' --output='<same-basename.docx>'
python '.agents/skills/markdown2docx/main.py' finalize '<same-basename.docx>'
python '.agents/skills/markdown2docx/main.py' refresh '<same-basename.docx>'
```

<!-- markdownlint-enable MD013 -->

## 検証して報告する

Pandoc、`finalize`および`refresh`が正常終了し、DOCXが存在して空でなく、入力の
SHA-256 Hashが変化していないことを確認する。目次、図一覧、表一覧の日本語見出しと
表示項目、全表のCaption、Page番号および保存日が更新され、全Sectionの余白が上・下
25.4mm、左・右19.05mmであることを確認する。

すべての確認に合格した場合だけ、DOCXの絶対Pathを返す。失敗した場合は入力
Markdownを保持し、完了した処理と失敗した確認を部分成功として報告する。Field対応
Office Engineを利用できない環境では変換を成功扱いにしない。
