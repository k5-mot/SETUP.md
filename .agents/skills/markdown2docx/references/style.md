# 🎨 デフォルトテンプレート 記述スタイル

本書は、markdown2docxスキルのデフォルトテンプレートスタイルの仕様を記述する。

## 📌 pandoc使用例

```bash
pandoc 'openspec/publics/<document>.md' \
  --from='gfm+implicit_figures' \
  --to=docx \
  --standalone \
  --reference-doc='.agents/skills/markdown2docx/references/template.docx' \
  --toc \
  --toc-depth=6 \
  --lof \
  --lot \
  --metadata='toc-title:目次' \
  --metadata='lof-title:図一覧' \
  --metadata='lot-title:表一覧' \
  --output='openspec/publics/<document>.docx'
```

Repository Rootで実行し、`<document>`には変換対象のMarkdownと同じBase Nameを
指定する。参照DOCXには`.agents/skills/markdown2docx/references/template.docx`を
使用する。変換にはPandoc 3.11を使用し、入力形式は`gfm+implicit_figures`とする。Pandocは
参照DOCXから名前付きStyle、Section設定、HeaderおよびFooterを取り込むが、参照
DOCX内のSample本文は生成物へCopyしない。

## 🧩 GitHub Flavored Markdown対応

入力Markdownでは、Pandocの`gfm` Readerが解釈できるSyntaxを使用する。
`implicit_figures`だけは図Captionを生成するため、GFMへ明示的に追加している。

| GFM要素 | Markdown例 | Wordでの表現 |
| --- | --- | --- |
| 段落 | 通常の文章 | `Normal`または`BodyText` |
| 太字 | `**太字**` | 本文Fontを維持した太字 |
| 斜体 | `*斜体*` | 本文Fontを維持した斜体 |
| 取消線 | `~~取消線~~` | 本文Fontを維持した取消線 |
| Inline Code | `` `code` `` | `VerbatimChar` |
| Code Block | Fenced Code Block | `SourceCode` |
| Block Quote | `> 引用` | `BlockText` |
| Link | `表示名`と`URL` | `Hyperlink` |
| 箇条書き | `- 項目` | `ListBullet`系 |
| 番号付きList | `1. 項目` | `ListNumber`系 |
| Task List | `- [x] 完了` | Check記号を含むList |
| Pipe Table | `\| A \| B \|` | `Table` |
| 単独の画像 | 代替TextとLocal Path | `Figure`、`CaptionedFigure`、`ImageCaption` |
| Footnote | `[^1]` | `FootnoteText`、`FootnoteReference` |
| Alert | `> [!NOTE]`など | `Note`、`Tip`などのAlert Style |
| 数式 | `$x$`、`$$x$$` | `Equation`または`EquationBlock` |
| YAML Metadata | File先頭の`---` Block | `Title`、`Subtitle`などの文書Metadata |

GFMでは見出し1から見出し6までを直接記述できる。見出し7から見出し9、
`TableCaption`および`CodeCaption`の標準Syntaxはない。Raw HTMLはDOCX Writerで同じ表示に
なる保証がないため、書式制御には使用しない。

Soft Line Breakは通常の空白として扱う。強制改行が必要な場合はGFMのHard Line
Breakを使用する。入力Markdownに直接Font名、Font Size、文字色またはWord固有Styleを
記述せず、参照DOCXへ責務を集約する。

## 余白

| 項目 | 設定値 |
| --- | --- |
| 用紙Size | A4 |
| 用紙方向 | 縦 |
| Page幅 | 11906 twip |
| Page高さ | 16838 twip |
| 上余白 | 1134 twip |
| 右余白 | 720 twip |
| 下余白 | 1134 twip |
| 左余白 | 720 twip |

色は原則として黒と白を使用し、GFM Alertだけは役割を識別するための抑制した背景色を
使用できる。

## 🔤 フォント

Font SizeはWordの表示単位であるptで示す。括弧内はOOXMLの`w:rFonts`値である。

| 系統 | 日本語Font | 欧文Font | 主な用途 |
| --- | --- | --- | --- |
| 本文系 | MS P明朝 (`MS PMincho`) | Times New Roman | 本文、List、表、Footnote、目次項目 |
| 見出し系 | MS Pゴシック (`MS PGothic`) | Arial | 表題、見出し、Caption、目次、Header、Footer |
| Code系 | MSゴシック (`MS Gothic`) | Consolas | Inline／Block Code、Highlight Token |

| Word Styleまたは用途 | 日本語Font | 欧文Font | Size | 装飾 |
| --- | --- | --- | --- | --- |
| `Normal`、`BodyText` | MS P明朝 | Times New Roman | 10pt | 黒、通常 |
| 太字、斜体、取消線 | 本文のFontを継承 | 本文のFontを継承 | 10pt | GFMに応じた直接書式 |
| `Hyperlink` | MS P明朝 | Times New Roman | 10pt | 黒、下線 |
| `FootnoteText` | MS P明朝 | Times New Roman | 10pt | 黒、通常 |
| `Title` | MS Pゴシック | Arial | 28pt | 黒、中央 |
| `Subtitle` | MS Pゴシック | Arial | 14pt | 黒 |
| `Heading1`、`TOCHeading` | MS Pゴシック | Arial | 14pt | 黒、見出し1は太字 |
| `Heading2` | MS Pゴシック | Arial | 12pt | 黒、太字 |
| `Heading3` | MS Pゴシック | Arial | 11pt | 黒、太字 |
| `Heading4`から`Heading7`、`Heading9` | MS Pゴシック | Arial | 10pt | 黒、通常 |
| `Heading8` | MS Pゴシック | Arial | 10pt | 黒、斜体 |
| `TOC1`から`TOC6` | MS P明朝 | Times New Roman | 10pt | 黒、通常 |
| `Caption`、各Caption Style | MS Pゴシック | Arial | 10pt | 黒、中央 |
| `Table` | MS P明朝 | Times New Roman | 10pt | 黒、通常 |
| `BlockText` | MS P明朝 | Times New Roman | 10pt | 黒、通常 |
| `SourceCode`、`VerbatimChar` | MSゴシック | Consolas | 10pt | 黒、等幅 |
| Header、Footer | MS Pゴシック | Arial | 9pt | 黒 |

FontとSizeは参照DOCXの各Styleが所有する。Pandocが太字、斜体、取消線またはSyntax
HighlightのRun Propertyを付ける場合も、Font Familyと基準Sizeは対応するStyleから
継承する。

## 📄 本文

本文は`Normal`または`BodyText`を使用し、10pt、段落前0pt、段落後6pt、行間
13.8ptとする。文字色は黒とし、本文中の強調は次の規則に従う。

- `**text**`は太字、`*text*`は斜体、`***text***`は太字かつ斜体とする。
- `~~text~~`は取消線とする。
- Inline Codeは`VerbatimChar`へ変換し、MSゴシック／Consolasの10ptとする。
- Linkは`Hyperlink`を使用し、黒色と下線で識別する。
- 箇条書き、番号付きListおよびTask Listは本文Fontと10ptを継承する。
- Horizontal Ruleは文書構造の区切りに限定し、表題や見出しの直下には置かない。

GFM AlertはPandoc 3.11の`alerts` Extensionで処理する。文字色は黒、Sizeは10ptとし、
次の背景色だけを使用できる。

| GFM Alert | Word Style | 背景色 |
| --- | --- | --- |
| `[!NOTE]` | `Note` | `#DDF4FF` |
| `[!TIP]` | `Tip` | `#DAFBE1` |
| `[!IMPORTANT]` | `Important` | `#F3E8FF` |
| `[!WARNING]` | `Warning` | `#FFF8C5` |
| `[!CAUTION]` | `Caution` | `#FFEBE9` |

## 🪧 表題・副題

表題と副題はFile先頭のYAML Metadataから生成する。

```yaml
---
title: "要件定義書"
subtitle: "対象システム名"
---
```

`title`は必須であり、`Title`へ変換する。`Title`は28pt、中央、段落前210pt、
段落後0pt、行間12ptとする。`subtitle`は任意であり、`Subtitle`へ変換する。
Markdown本文の最初の見出しを表題の代用にしない。

## 🧱 見出し1–9

| Level | GFM Syntax | Word Style | Size | 太字／斜体 | 段落前 | 段落後 | 改Page |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `#` | `Heading1` | 14pt | 太字 | 24pt | 12pt | あり |
| 2 | `##` | `Heading2` | 12pt | 太字 | 18pt | 8pt | なし |
| 3 | `###` | `Heading3` | 11pt | 太字 | 14pt | 6pt | なし |
| 4 | `####` | `Heading4` | 10pt | 通常 | 10pt | 4pt | なし |
| 5 | `#####` | `Heading5` | 10pt | 通常 | 8pt | 3pt | なし |
| 6 | `######` | `Heading6` | 10pt | 通常 | 6pt | 2pt | なし |
| 7 | GFM Syntaxなし | `Heading7` | 10pt | 通常 | 2pt | 0pt | なし |
| 8 | GFM Syntaxなし | `Heading8` | 10pt | 斜体 | 継承 | 0pt | なし |
| 9 | GFM Syntaxなし | `Heading9` | 10pt | 通常 | 継承 | 0pt | なし |

見出し1から見出し6はGFMから直接生成し、目次の対象とする。見出し7から見出し9は
Word互換性のためTemplateに保持する予約Styleであり、現在の`gfm+implicit_figures`
変換では生成しない。見出し7から見出し9を入力から生成する変更は、Reader、Filter
および目次深度を同時に設計してから行う。

章番号は入力Markdownが所有する。`Heading1`から`Heading9`にはWordの自動採番を
設定せず、`# 1. 文書概要`のように入力へ記述した番号をそのまま表示する。これにより、
GFM本文の章番号とWordの自動採番が重複することを防ぐ。

## 🖼️ 図

段落内に画像だけを置くと、`implicit_figures`が図として解釈する。

GFMの画像Syntaxへ代替TextとLocal Pathを指定する。代替Textは図の説明およびCaption
の元になる。図は本文幅を超えないSizeとし、縦横比を保持する。文章と同じ段落に置いた
画像はInline Imageであり、図Captionや図一覧の対象にしない。変換の再現性を保つため、
画像はRepository内のLocal Pathを使用する。

## 📊 表

GFM Pipe Tableを`Table`へ変換する。Table全体はPage中央、本文は10ptとし、先頭行は
Header Rowとして太字にする。Pandocが先頭行へ`w:tblHeader`を付与し、改Page後にも
Header Rowを繰り返す。列のAlignment指定はGFMのDelimiter Rowに従う。

```markdown
| 項目 | 値 |
| --- | ---: |
| 件数 | 10 |
```

GFM Pipe TableにはCaption Syntaxがないため、通常の変換では`TableCaption`を生成
しない。Captionのない表は表一覧へ表示されない。

## 🏷️ 図表・コードCaption

| 対象 | Word Style | Font | Size | Alignment | GFMでの生成方法 |
| --- | --- | --- | --- | --- | --- |
| 図 | `ImageCaption` | MS Pゴシック／Arial | 10pt | 中央 | 単独画像の代替Text |
| 表 | `TableCaption` | MS Pゴシック／Arial | 10pt | 中央 | 標準Syntaxなし |
| Code | `CodeCaption` | MS Pゴシック／Arial | 10pt | 中央 | 標準Syntaxなし |

図Captionは図一覧の入力となる。`TableCaption`と`CodeCaption`はTemplateに保持する
が、GFMだけでは生成されない。Code Block本体は`SourceCode`を使用する。Caption対応を
追加するときは、GFM互換性を維持できるPandoc Filterなどを別途設計する。

`ImageCaption`と`TableCaption`は`Caption`を継承し、10pt、斜体、中央、段落前4pt、
段落後6ptとする。`CodeCaption`は10pt、太字、中央、段落前4pt、段落後2ptとする。

## 💬 ブロックQuote

`>`で始まるGFM Block Quoteは`BlockText`へ変換する。FontはMS P明朝／Times New
Roman、Sizeは10pt、段落前後は各5ptとする。入れ子のQuoteはPandocが生成するIndentで
階層を表す。Block QuoteをAlertとして表示する場合は、`> [!NOTE]`などのGFM Alert
Syntaxを使用する。

## 🧭 Header

表紙のFirst Headerは空欄であり、Fieldを含まない。2Page目以降のDefault Headerは、
左に`○○システム 基本設計書`、右に`SYS-DS-001`を表示する。いずれもLiteral Textで
あり、HeaderにはData Fieldを置かない。

PandocはSection PropertyとHeader Relationshipを参照DOCXから取り込む。入力
MarkdownからHeaderは生成しない。文書固有値へ変更するときは、参照DOCXと本書を
同じ変更で更新する。

## 🦶 Footer

表紙のFirst Footerは空欄であり、Fieldを含まない。2Page目以降のDefault Footerは、
左に`社外秘 / ○○株式会社`、中央に章番号とPage番号、右に保存日と`最終更新`を表示
する。

| 表示位置 | 内容 | Field Code | 参照先 |
| --- | --- | --- | --- |
| 左 | `社外秘 / ○○株式会社` | なし | Template内のLiteral Text |
| 中央 | 章番号 | `STYLEREF 1 \n` | 文書内の直近の`Heading1`番号 |
| 中央 | Page番号 | `PAGE` | 現在の文書Page |
| 右 | 保存日 | `SAVEDATE \@ "yyyy/MM/dd"` | 現在の文書Property |
| 右 | `最終更新` | なし | Template内のLiteral Text |

FooterのFieldは文書内部または文書Propertyだけを参照し、外部File、外部URL、Database
または外部Applicationを参照しない。

## 🗂️ 表紙

表紙はYAML Metadataの`title`と任意の`subtitle`から生成する。参照DOCXのSample表紙
本文はCopyしない。`Title`の段落前余白で表紙内の位置を調整し、直後の`TOCHeading`
に設定した改PageでNavigation Pageと分離する。

表紙ではFirst HeaderとFirst Footerを使用し、どちらも空欄とする。表紙に日付、版数、
作成者などを追加する場合は、対応するMetadataから生成できる方法を別途定義し、固定の
Sample本文へ依存しない。

## 📑 目次

SkillはPandocを`--toc --toc-depth=6 --metadata='toc-title:目次'`付きで実行する。
Pandocは`TOCHeading`と次のFieldを生成する。

```text
TOC \o "1-6" \h \z \u
```

`TOCHeading`は14pt、段落前12pt、段落後8ptとし、直前で改Pageする。目次項目は
`TOC1`から`TOC6`を使用し、MS P明朝／Times New Romanの10ptとする。見出し7から
見出し9は現在の目次へ含めない。

## 🖼️ 図一覧

SkillはPandocを`--lof --metadata='lof-title:図一覧'`付きで実行する。Pandocは
`TOCHeading`と次のFieldを生成する。

```text
TOC \h \z \t "Image Caption" \c
```

`implicit_figures`が`ImageCaption`を付与した図だけを一覧の入力とする。Inline Image
やCaptionのない画像は対象外とする。該当する図がない文書では、空の図一覧を正しい
結果とする。

## 📊 表一覧

SkillはPandocを`--lot --metadata='lot-title:表一覧'`付きで実行する。Pandocは
`TOCHeading`と次のFieldを生成する。

```text
TOC \h \z \t "Table Caption" \c
```

`TableCaption`がある表だけを一覧の入力とする。GFM Pipe TableはCaptionを生成しない
ため、GFMだけで作成した文書では通常、表一覧は空になる。空の一覧を変換失敗として
扱わない。

## 🔄 Data Field

生成DOCXで使用するFieldを次に限定する。

| Field | 使用箇所 | 参照範囲 | 更新内容 |
| --- | --- | --- | --- |
| `TOC \o "1-6" \h \z \u` | 目次 | 文書内 | 見出しとPage番号 |
| `TOC \h \z \t "Image Caption" \c` | 図一覧 | 文書内 | 図CaptionとPage番号 |
| `TOC \h \z \t "Table Caption" \c` | 表一覧 | 文書内 | 表CaptionとPage番号 |
| `STYLEREF 1 \n` | Footer | 文書内 | 直近の見出し1番号 |
| `PAGE` | Footer | 文書内 | 現在のPage番号 |
| `SAVEDATE \@ "yyyy/MM/dd"` | Footer | 文書Property | 保存日 |

TemplateおよびSkillは`INCLUDETEXT`、`INCLUDEPICTURE`、`LINK`、`DDE`、`DATABASE`、
`RD`などの外部参照Fieldを使用してはならない。Template Packageにも
`TargetMode="External"`のRelationshipを含めない。入力GFMに記述した通常の外部Linkは
`Hyperlink`でありData Fieldではないが、変換結果に外部Hyperlink Relationshipが生成
されるため、文書の配布方針に従って入力段階で確認する。

PandocはField Codeを生成するが、最終的な項目やPage番号を計算しない。参照DOCXの
`w:updateFields=true`により更新対象として扱う。Microsoft Wordを使用できる場合は、
文書を開いて`Ctrl+A`、`F9`の順に実行して保存する。Wordを利用できない場合はField
Codeと`w:updateFields=true`の存在を検証し、表示中のCache値を最新として報告しない。

## 📚 Word Style一覧

参照DOCXの`word/styles.xml`に明示定義された全110 Styleを記録する。表示名はXMLの
値であり、Wordの言語設定により組み込みStyleの表示名が異なる場合がある。
`paragraph`は段落、`character`は文字、`table`は表のStyleである。継承元の`—`は
明示指定なしを示す。参照だけが存在する`TableNormal`は110 Styleに含めない。

本書でWord Styleを参照するときは、次表の`Style ID`をBacktickで囲んで記載する。
`表示名`は次表の記録と、WordのField Codeが表示名を要求する箇所だけで使用する。
このため、図一覧と表一覧のField Code内にある`"Image Caption"`および
`"Table Caption"`はStyle IDへ置換しない。

| Style ID | 種別 | 表示名 | 継承元 |
| --- | --- | --- | --- |
| Normal | paragraph | Normal | — |
| BodyText | paragraph | Body Text | Normal |
| FirstParagraph | paragraph | First Paragraph | BodyText |
| Compact | paragraph | Compact | BodyText |
| Title | paragraph | Title | Normal |
| TitleChar | character | Title Char | DefaultParagraphFont |
| Subtitle | paragraph | Subtitle | Title |
| SubtitleChar | character | Subtitle Char | DefaultParagraphFont |
| Author | paragraph | Author | Title |
| Date | paragraph | Date | Title |
| AbstractTitle | paragraph | Abstract Title | Normal |
| Abstract | paragraph | Abstract | Normal |
| Bibliography | paragraph | Bibliography | Normal |
| Heading1 | paragraph | heading 1 | Normal |
| Heading2 | paragraph | heading 2 | Normal |
| Heading3 | paragraph | heading 3 | Normal |
| Heading4 | paragraph | heading 4 | Normal |
| Heading5 | paragraph | heading 5 | Normal |
| Heading6 | paragraph | heading 6 | Normal |
| Heading7 | paragraph | heading 7 | Normal |
| Heading8 | paragraph | heading 8 | Normal |
| Heading9 | paragraph | heading 9 | Normal |
| Heading1Char | character | Heading 1 Char | DefaultParagraphFont |
| Heading2Char | character | Heading 2 Char | DefaultParagraphFont |
| Heading3Char | character | Heading 3 Char | DefaultParagraphFont |
| Heading4Char | character | Heading 4 Char | DefaultParagraphFont |
| Heading5Char | character | Heading 5 Char | DefaultParagraphFont |
| Heading6Char | character | Heading 6 Char | DefaultParagraphFont |
| Heading7Char | character | Heading 7 Char | DefaultParagraphFont |
| Heading8Char | character | Heading 8 Char | DefaultParagraphFont |
| Heading9Char | character | Heading 9 Char | DefaultParagraphFont |
| BlockText | paragraph | Block Text | BodyText |
| FootnoteBlockText | paragraph | Footnote Block Text | FootnoteText |
| DefaultParagraphFont | character | Default Paragraph Font | — |
| Table | table | Table | TableNormal |
| DefinitionTerm | paragraph | Definition Term | Normal |
| Definition | paragraph | Definition | Normal |
| TableCaption | paragraph | 表タイトル | Caption |
| ImageCaption | paragraph | 図タイトル | Caption |
| BodyTextChar | character | Body Text Char | DefaultParagraphFont |
| SectionNumber | character | Section Number | BodyTextChar |
| KeywordTok | character | KeywordTok | VerbatimChar |
| DataTypeTok | character | DataTypeTok | VerbatimChar |
| DecValTok | character | DecValTok | VerbatimChar |
| BaseNTok | character | BaseNTok | VerbatimChar |
| FloatTok | character | FloatTok | VerbatimChar |
| ConstantTok | character | ConstantTok | VerbatimChar |
| CharTok | character | CharTok | VerbatimChar |
| SpecialCharTok | character | SpecialCharTok | VerbatimChar |
| StringTok | character | StringTok | VerbatimChar |
| VerbatimStringTok | character | VerbatimStringTok | VerbatimChar |
| SpecialStringTok | character | SpecialStringTok | VerbatimChar |
| ImportTok | character | ImportTok | VerbatimChar |
| CommentTok | character | CommentTok | VerbatimChar |
| DocumentationTok | character | DocumentationTok | VerbatimChar |
| AnnotationTok | character | AnnotationTok | VerbatimChar |
| CommentVarTok | character | CommentVarTok | VerbatimChar |
| OtherTok | character | OtherTok | VerbatimChar |
| FunctionTok | character | FunctionTok | VerbatimChar |
| VariableTok | character | VariableTok | VerbatimChar |
| ControlFlowTok | character | ControlFlowTok | VerbatimChar |
| OperatorTok | character | OperatorTok | VerbatimChar |
| BuiltInTok | character | BuiltInTok | VerbatimChar |
| ExtensionTok | character | ExtensionTok | VerbatimChar |
| PreprocessorTok | character | PreprocessorTok | VerbatimChar |
| AttributeTok | character | AttributeTok | VerbatimChar |
| RegionMarkerTok | character | RegionMarkerTok | VerbatimChar |
| InformationTok | character | InformationTok | VerbatimChar |
| WarningTok | character | WarningTok | VerbatimChar |
| AlertTok | character | AlertTok | VerbatimChar |
| ErrorTok | character | ErrorTok | VerbatimChar |
| NormalTok | character | NormalTok | VerbatimChar |
| SourceCode | paragraph | コードブロック | BodyText |
| VerbatimChar | character | Verbatim Char | DefaultParagraphFont |
| Caption | paragraph | Caption | Normal |
| Figure | paragraph | Figure | Normal |
| CaptionedFigure | paragraph | Captioned Figure | Figure |
| FootnoteText | paragraph | Footnote Text | Normal |
| FootnoteReference | character | Footnote Reference | DefaultParagraphFont |
| Hyperlink | character | Hyperlink | DefaultParagraphFont |
| TOC1 | paragraph | TOC 1 | Normal |
| TOC2 | paragraph | TOC 2 | Normal |
| TOC3 | paragraph | TOC 3 | Normal |
| TOC4 | paragraph | TOC 4 | Normal |
| TOC5 | paragraph | TOC 5 | Normal |
| TOC6 | paragraph | TOC 6 | Normal |
| TOCHeading | paragraph | TOC Heading | Normal |
| ListBullet | paragraph | List Bullet | BodyText |
| ListBullet2 | paragraph | List Bullet 2 | BodyText |
| ListBullet3 | paragraph | List Bullet 3 | BodyText |
| ListNumber | paragraph | List Number | BodyText |
| ListNumber2 | paragraph | List Number 2 | BodyText |
| ListNumber3 | paragraph | List Number 3 | BodyText |
| Equation | paragraph | Equation | Normal |
| Note | paragraph | Note / 注記 | BlockText |
| Warning | paragraph | Warning / 警告 | BlockText |
| Caution | paragraph | Caution / 注意 | BlockText |
| Header | paragraph | Header | Normal |
| Footer | paragraph | Footer | Normal |
| CodeCaption | paragraph | コードタイトル | Normal |
| AppendixLabel | paragraph | Appendix Label / 付録ラベル | Heading1 |
| AppendixHeading1 | paragraph | Appendix Heading 1 / 付録 章 | Heading1 |
| AppendixHeading2 | paragraph | Appendix Heading 2 / 付録 見出し2 | Heading2 |
| AppendixHeading3 | paragraph | Appendix Heading 3 / 付録 見出し3 | Heading3 |
| AppendixHeading4 | paragraph | Appendix Heading 4 / 付録 見出し4 | Heading4 |
| AppendixHeading5 | paragraph | Appendix Heading 5 / 付録 見出し5 | Heading5 |
| AppendixHeading6 | paragraph | Appendix Heading 6 / 付録 見出し6 | Heading6 |
| Tip | paragraph | Tip / ヒント | BlockText |
| Important | paragraph | Important / 重要 | BlockText |
| EquationBlock | paragraph | 数式ブロック | BodyText |

## 🛠️ 保守

参照DOCXを変更するときは、本書の各分類と実Packageを比較し、同じ変更で本書も更新
する。最低限、次を検証する。

- GFM要素とWord Styleの対応がPandoc 3.11の出力と一致すること
- Font Family、Font Size、段落間隔および改Pageが本書と一致すること
- `word/styles.xml`に110 Styleがあり、Style ID、種別、表示名、継承元が一致すること
- HeaderおよびFooterのLiteral Text、Field Code、First／Defaultの参照が一致すること
- 目次、図一覧、表一覧のField Codeと`w:updateFields=true`が存在すること
- Macro Part、外部参照Fieldおよび外部RelationshipがTemplateに存在しないこと
- 代表的なGFM文書を変換し、全Pageに欠け、重なり、Font置換または表崩れがないこと
