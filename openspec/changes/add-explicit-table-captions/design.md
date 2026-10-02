<!-- markdownlint-disable MD041 MD013 -->

## Context

動機は [proposal.md](proposal.md) を参照。現行処理は `gfm+implicit_figures` Readerを使用し、DOCX 内の各表へ直前の見出しから `TableCaption` を挿入する。strict GFMには表キャプション構文がなく、Pandocの `gfm` Readerも `table_captions` Extensionをサポートしない。Pandocの `markdown` Readerは表キャプションを扱えるが、GFM固有の `tex_math_gfm` を扱えない。

## Goals / Non-Goals

**Goals:** GFM Readerの解釈を維持し、Pandoc標準の表キャプションを正本 Markdown に記述して DOCX と表一覧へ反映する。GFMと追加Pandoc構文の対応範囲を検証可能にする。

**Non-Goals:** Pandoc Markdownの全拡張を一括で有効化すること、任意のRaw HTMLをWord固有要素へ変換すること、新しい外部Dependencyを追加すること。

## Decisions

- Readerは `gfm+implicit_figures` を維持する。`markdown` Readerへの切替は `tex_math_gfm` を失い、GFM全体を基礎とする契約を満たさないため採用しない。
- 正本 Markdown では `: <caption>` を表の前後に置くPandoc標準構文を使用する。Pandoc同梱のLua Filterで隣接段落をTable Captionへ変換し、既存のDOCX仕上げ処理が本文を保持して連番を付与する。
- Pandocが `TableCaption` を生成しない表は、現在のセクション名由来の生成を維持する。
- GFM互換FixtureはPandoc `gfm` Readerで有効な構文を網羅する。Raw HTMLなどDOCX Writerで同等表現を保証できない構文は、解析可能であることと出力上の制限を書式仕様へ分けて記録する。
- 固定書式とPandocが生成できる構造は、次の責務表に従ってPythonのOOXML編集から移す。Office Engine保存後にだけ必要な補正は、再現Testがあるものだけ残す。

| 責務 | 所有先 | Python OOXML |
| --- | --- | --- |
| 本文、GFM要素、表Captionと連番 | Pandoc＋Lua Filter | 削除 |
| 目次・図一覧・表一覧の日本語見出し | Pandoc翻訳Data | 削除 |
| 図表一覧Fieldが参照するStyle名 | reference.docx | 削除 |
| 余白、表中央配置、Header/Footer、改PageStyle | reference.docx | 変換直後の補正を削除 |
| 表Rowの途中改Page禁止 | DOCX Row Property | 維持 |
| Page番号を含む一覧の確定 | Word／LibreOffice | 維持 |
| LibreOffice保存後の偶数Page部品などの補正 | 再現Testに基づく互換処理 | 必要な処理だけ維持 |

- Lua Filterが `表 <number>:` を付けるため、Markdown には番号を書かない。表の追加・並べ替え後も連番を再計算できる。
- PRD/HLD の全表へ固有の表題を設定する。表題は列名の反復ではなく、表が示す対象を簡潔に表す。

## Quality Attribute Design

| ID | 方法・Trade-off | Evidence |
| --- | --- | --- |
| QR-DOCX-002 | 全表に既存 Caption Styleと連番を適用する | 表数と Caption 数の一致、全ページ描画 |
| QR-DOCX-003 | 未指定表では既存処理へ戻す | 表題未指定の回帰 Test |
| QR-DOCX-005 | Pandoc／reference.docxと重複するOOXML編集を削除する | 責務表、差分 Review、Ruff |
| QR-DOCX-007 | Markdown 表題と DOCX／表一覧の表示値を比較する | Source-to-OOXML Test、全ページ描画 |
| QR-DOCX-008 | GFM Readerを維持し、追加構文を明示する | AST互換Fixture、書式仕様Review |

## Lifecycle, Migration and Operations

移行時に PRD/HLD の全表へPandoc表キャプションを追加し、日本語翻訳Dataとreference.docxのStyle名を更新する。以後は文書作成者が正本 Markdown で表題を保守し、既存 Release Workflow が DOCX 生成と検証を行う。未移行文書は従来の自動キャプションを使用できる。廃止時は表キャプションを削除すれば既存動作へ戻る。

## Risks / Trade-offs

- [GitHub表示ではキャプションが通常段落に見える] → 配布変換ではLua Filterを正規経路とし、DOCXのTable Captionを検証する。
- [任意のRaw HTMLはDOCXで同等表示にならない] → GFMとして解析は許容し、保証できないWord表現を書式仕様へ明記する。
- [LibreOfficeがreference.docx由来の書式を保存時に変更する] → 変換直後と保存後を別々に検査し、再現する項目だけ互換補正を残す。
- [Markdown では表題行に自動番号がない] → 番号は並べ替えに追随させるため DOCX 生成時だけ付与する。

## Migration Plan

Lua Filter、変換処理、互換Fixtureを先に更新し、PRD/HLD のPandoc表キャプションを追加して DOCX を再生成する。全ページ描画と Release Asset検証後に Patch Releaseを作成する。Rollback はFilter指定と表キャプションを同時に戻し、従来のセクション名由来キャプションへ復帰する。
