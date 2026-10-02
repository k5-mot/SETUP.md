<!-- markdownlint-disable MD041 MD013 -->

## Context

動機は [proposal.md](proposal.md) を参照。現行処理は DOCX 内の各表を走査し、直前の見出しから `TableCaption` を挿入する。Pandoc 3.11 の `gfm` Reader は `table_captions` Extensionをサポートしないため、GFM Pipe Tableだけでは表題を渡せない。

## Goals / Non-Goals

**Goals:** 正本 Markdown で表ごとの表題を読める形で記述し、既存の共通変換処理で DOCX と表一覧へ反映する。

**Non-Goals:** 新しい Markdown Parser、Pandoc Filter、Dependencyまたは汎用Metadata構文を追加すること。

## Decisions

- 表の直前に置く `表題: <caption>` 段落を明示表題とする。通常の GFM 段落として Pandoc の DOCX 出力へ残るため、変換処理は入力 Markdown を別途解析せずに表との対応を確定できる。
- 既存の表走査処理で、直前段落が明示表題ならその段落を `TableCaption` へ置換する。その他の表は現在のセクション名由来の生成を維持する。
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

移行時に PRD/HLD の全表へ表題行を追加する。以後は文書作成者が正本 Markdown で表題を保守し、既存 Release Workflow が DOCX 生成と検証を行う。未移行文書は従来の自動キャプションを使用できる。廃止時は表題行を削除すれば既存動作へ戻る。

## Risks / Trade-offs

- [表題行と表の間へ別段落を挿入すると対応しない] → 「直前」という単純な契約を Skill と書式仕様へ明記し、回帰 Testで固定する。
- [通常本文が偶然 `表題:` で始まる] → 直後が表の場合だけ表題として扱う。
- [Markdown では表題行に自動番号がない] → 番号は並べ替えに追随させるため DOCX 生成時だけ付与する。

## Migration Plan

変換処理と回帰 Testを先に更新し、PRD/HLD の表題行を追加して DOCX を再生成する。全ページ描画と Release Asset検証後に Patch Releaseを作成する。Rollback は表題行と判定分岐を同時に戻し、従来のセクション名由来キャプションへ復帰する。
