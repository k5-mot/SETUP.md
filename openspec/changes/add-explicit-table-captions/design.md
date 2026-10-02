<!-- markdownlint-disable MD041 MD013 -->

## Context

動機は [proposal.md](proposal.md) を参照。現行処理は DOCX 内の各表を走査し、直前の見出しから `TableCaption` を挿入する。strict GFMには表キャプション構文がなく、Pandocの `gfm` Readerも `table_captions` Extensionをサポートしない。一方、Pandoc Markdown Readerは同Extensionを標準でサポートする。

## Goals / Non-Goals

**Goals:** Pandoc標準の表キャプションを正本 Markdown に記述し、既存の共通変換処理で DOCX と表一覧へ反映する。

**Non-Goals:** 新しい Markdown Parser、Pandoc Filter、Dependencyまたは汎用Metadata構文を追加すること。

## Decisions

- Pandoc Readerを `gfm` から `markdown` へ変更し、既存文書で使用するGFM系Extensionと `table_captions` を明示的に有効化する。独自ParserやFilterは追加しない。
- 正本 Markdown では `: <caption>` を表の前後に置くPandoc標準構文を使用する。Pandocが対応する表へ `TableCaption` を生成するため、変換処理は既存Captionの本文を保持して連番だけを付与する。
- Pandocが `TableCaption` を生成しない表は、現在のセクション名由来の生成を維持する。
- DOCX 側で `表 <SEQ>:` を付けるため、Markdown には番号を書かない。表の追加・並べ替え後も連番を再計算できる。
- PRD/HLD の全表へ固有の表題を設定する。表題は列名の反復ではなく、表が示す対象を簡潔に表す。

## Quality Attribute Design

| ID | 方法・Trade-off | Evidence |
| --- | --- | --- |
| QR-DOCX-002 | 全表に既存 Caption Styleと連番を適用する | 表数と Caption 数の一致、全ページ描画 |
| QR-DOCX-003 | 未指定表では既存処理へ戻す | 表題未指定の回帰 Test |
| QR-DOCX-005 | 既存の表走査へ1つの分岐だけを追加する | 差分 Review、Ruff |
| QR-DOCX-007 | Markdown 表題と DOCX／表一覧の表示値を比較する | Source-to-OOXML Test、全ページ描画 |

## Lifecycle, Migration and Operations

移行時に PRD/HLD の全表へPandoc表キャプションを追加する。以後は文書作成者が正本 Markdown で表題を保守し、既存 Release Workflow が DOCX 生成と検証を行う。未移行文書は従来の自動キャプションを使用できる。廃止時は表キャプションを削除すれば既存動作へ戻る。

## Risks / Trade-offs

- [Pandoc Markdown Readerはstrict GFMより多くの構文を解釈する] → 正本で使用する構文をSkillに限定し、既存PRD/HLDの変換回帰Testで差分を検出する。
- [strict GFM Rendererではキャプションが通常段落に見える] → 正本の配布変換はPandoc Markdownを正規経路とし、GitHub表示よりDOCXの構造を優先する。
- [Markdown では表題行に自動番号がない] → 番号は並べ替えに追随させるため DOCX 生成時だけ付与する。

## Migration Plan

Reader指定、変換処理、回帰 Testを先に更新し、PRD/HLD のPandoc表キャプションを追加して DOCX を再生成する。全ページ描画と Release Asset検証後に Patch Releaseを作成する。Rollback はReader指定と表キャプションを同時に戻し、従来のセクション名由来キャプションへ復帰する。
