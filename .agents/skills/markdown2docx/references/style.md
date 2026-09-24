# 🎨 Markdown2DOCX 書式仕様

## 📌 位置付け

`.agents/skills/markdown2docx/references/template.docx`を、生成するDOCXの書式に
関する唯一の正本とする。本書は、保守と障害調査のために正本の有効値と責任分界を
列挙する。

Pandocは参照DOCXから名前付きStyle、Section設定、HeaderおよびFooterを取り込む。
参照DOCX内のSample本文はCopyしない。表紙とNavigation Fieldは、入力Markdownの
MetadataおよびPandoc Optionから生成する。

PageはA4縦の11906×16838 twipで、余白は上1134、右720、下1134、左720 twipとする。

## 🔤 Font

| 用途 | 欧文Font | 日本語Font | Size |
| --- | --- | --- | --- |
| 本文、表、脚注、Code | Times New Roman | MS PMincho | 10pt |
| Title | Arial | MS PGothic | 28pt |
| Heading 1、TOC Heading | Arial | MS PGothic | 14pt |
| Heading 2 | Arial | MS PGothic | 12pt |
| Heading 3 | Arial | MS PGothic | 11pt |
| Heading 4から6 | Arial | MS PGothic | 10pt |
| Header、Footer | Arial | MS PGothic | 9pt |

FontとSizeは参照DOCXの各Styleが所有する。入力Markdownや変換後処理で上書きしない。

## 🧱 Style

| Word Style | 主な用途 | 段落設定 |
| --- | --- | --- |
| `Normal`、`Body Text` | 本文 | 10pt、段落後6pt、行間13.8pt |
| `Title` | 表紙Title | 28pt、中央、段落前210pt、段落後0pt |
| `TOC Heading` | 目次、図一覧、表一覧のHeading | 14pt、前12pt、後8pt、直前で改Page |
| `Heading 1` | 本文の章 | 14pt、前24pt、後12pt、直前で改Page |
| `Heading 2` | 節 | 12pt、前18pt、後8pt |
| `Heading 3` | 項 | 11pt、前14pt、後6pt |
| `Heading 4`から`Heading 6` | 下位Heading | 10pt、改Pageなし |
| `Table` | 表全体 | 10pt、Page中央 |
| `Table Caption` | 表Caption | Arial／MS PGothic、中央、連番Field |
| `Image Caption` | 図Caption | Arial／MS PGothic、中央、連番Field |
| `Source Code` | Code Block | 10pt、単一行間 |
| `Block Text` | 引用などのBlock | 10pt |

PandocはTableの先頭行へ`w:tblHeader`を出力し、改Page後にも見出し行を繰り返す。
この指定は参照DOCXのStyleではなく、Pandocが生成するTable構造が所有する。

注意Blockは本文外の識別用途に限って、次の抑制した背景色を使用できる。文字色は
いずれも黒とし、それ以外の本文はMonochromeとする。

| Style | 背景色 |
| --- | --- |
| `Note` | `#DDF4FF` |
| `Tip` | `#DAFBE1` |
| `Important` | `#F3E8FF` |
| `Warning` | `#FFF8C5` |
| `Caution` | `#FFEBE9` |

## 🧭 Header

表紙のFirst Headerは空欄とする。本文と付録のDefault Headerは、左に
`○○システム 基本設計書`、右に`SYS-DS-001`を表示する。Literal Textは参照DOCXで
管理し、文書固有値へ変更する場合も参照DOCXと本書を同じ変更で更新する。

PandocはSection PropertyとHeader Relationshipを参照DOCXから取り込む。入力
MarkdownからHeaderは生成しない。

## 🦶 Footer

表紙のFirst Footerは空欄とする。本文のDefault Footerは、左に
`社外秘 / ○○株式会社`、中央に章番号とPage番号、右に保存日と`最終更新`を表示する。
章番号は`STYLEREF`、Page番号は`PAGE`、保存日は`SAVEDATE` Fieldを使用する。

付録のDefault Footerは中央のPage番号と右の保存日を表示する。Fieldの値はWordなど
Fieldを扱えるWord Processorで更新するまでCacheされた値である。

## 📑 目次

SkillはPandocを`--toc --toc-depth=6 --metadata='toc-title:目次'`付きで実行する。
Pandocが`TOC Heading`と次のFieldを生成し、参照DOCXが書式を与える。

```text
TOC \o "1-6" \h \z \u
```

Heading 1からHeading 6が目次項目の入力となる。参照DOCXの
`w:updateFields=true`により、Wordで開いたときの更新対象として扱う。

## 🪧 表紙

入力MarkdownはFile先頭のYAML Metadataに空でない`title`を持たなければならない。

```yaml
---
title: "📋 要件定義書"
---
```

Pandocは`title`を`Title` Styleの段落へ変換する。`Title`の大きな段落前余白で表紙を
構成し、次の`TOC Heading`の改PageによってNavigation Pageと分離する。参照DOCXの
Sample表紙本文は生成物へCopyされない。

## 🖼️ 図一覧

SkillはPandocを`--lof --metadata='lof-title:図一覧'`付きで実行する。Pandocは
`TOC Heading`と次のFieldを生成する。

```text
TOC \h \z \t "Image Caption" \c
```

Pandocが図として認識し、`Image Caption`を付与した要素だけが一覧の入力となる。
該当する図Captionがない文書では、空の図一覧が正しい結果である。

## 📊 表一覧

SkillはPandocを`--lot --metadata='lot-title:表一覧'`付きで実行する。Pandocは
`TOC Heading`と次のFieldを生成する。

```text
TOC \h \z \t "Table Caption" \c
```

PandocがCaption付きTableとして認識し、`Table Caption`を付与した要素だけが一覧の
入力となる。該当する表Captionがない文書では、空の表一覧が正しい結果である。

## 🔄 Fieldの更新

PandocはField Codeを生成するが、最終的な項目とPage番号は計算しない。生成後に
Microsoft Wordを使用できる場合は、文書を開いて`Ctrl+A`、`F9`の順に実行してから
保存する。目次、図一覧、表一覧、Page番号および保存日が更新対象となる。

Wordを利用できない場合はField Codeと`w:updateFields=true`の存在を検証し、表示中の
Cache値を最新として報告しない。

## 🛠️ 保守

参照DOCXを変更するときは、本書の8分類であるFont、Style、Header、Footer、目次、
表紙、図一覧、表一覧を実Packageと比較し、同じ変更で本書も更新する。Macro Partと
外部Relationshipは追加しない。
