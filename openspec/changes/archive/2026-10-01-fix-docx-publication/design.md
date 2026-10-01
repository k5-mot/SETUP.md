<!-- markdownlint-disable MD041 MD013 -->

## Context

動機は [proposal.md](proposal.md) を参照。現行処理は Pandoc が生成する更新前フィールドをそのまま配布し、GFM 表にはキャプション情報がない。参照 DOCX の余白も指定値と異なり、Release Workflow は HLD のみを扱う。

## Goals / Non-Goals

**Goals:** PRD と HLD を同じ変換経路で生成し、開いた直後からナビゲーションと表キャプションを読める配布物にする。

**Non-Goals:** 正本 Markdown の表を手動で書き換えること、図が存在しない文書へ新しい図を作ること、公開済みタグを移動すること。

## Decisions

- Pandoc の出力後に、標準 Library の OOXML 処理で日本語見出し、一覧が参照する Style、全表キャプションを設定する。GFM 自体にない表 Caption を正本へ大量追加せず、PRD/HLD に同じ規則を適用できる。
- 表キャプションは直前の章・節見出しから文脈を取得し、同一見出し内で重複する場合は連番を付ける。単なる「表」より内容を識別しやすい。
- ナビゲーションはフィールド対応の Office Engine で更新して保存する。CI では Headless LibreOffice、Windows の手動変換では Microsoft Word を使用できる。更新後の表示文字列を OOXML Test で必須にする。
- 余白は参照 DOCX の全 Section を指定 twip 値へ更新する。生成物側でも全 Section を検査する。
- Release Job は2文書を生成・検査した後、1回の Release 作成で両 Asset を添付する。

## Quality Attribute Design

| ID | 方法・Trade-off | Evidence |
| --- | --- | --- |
| QR-DOCX-001 | 更新済みフィールドと指定日本語見出しを必須化 | OOXML Test、描画 |
| QR-DOCX-002 | 全表へ文脈付き Caption を自動付与 | 表数と Caption 数の一致、描画 |
| QR-DOCX-003 | 正本 Hash を前後比較し、標準 DOCX 部品だけを使用 | Hash Test、Word/LibreOffice 表示 |
| QR-DOCX-004 | 2文書を Release 作成前に検査 | Workflow Review、Release Asset 確認 |
| QR-DOCX-005 | 変換処理を1か所に集約 | PRD/HLD 回帰 Test |
| QR-DOCX-006 | Section ごとの twip 値を検査 | OOXML Test |

## Lifecycle, Migration and Operations

修正は次の Patch Release から適用する。`v0.0.0` は履歴として保持する。変換失敗は Release を停止し、Job Log とローカル回帰 Test で調査する。廃止時は補助処理とフィールド更新 Step を同時に除去し、正本 Markdown を残す。

## Risks / Trade-offs

- [Office Engine 間でページ割りが変わる] → 同じ Engine で更新と描画を行い、構造検査も併用する。
- [自動 Caption が表内容を完全には要約できない] → 直前見出しを採用し、同一節内の複数表を連番で区別する。
- [Headless Engine が利用できない] → 変換を失敗させ、更新前 DOCX を公開しない。

## Migration Plan

参照 DOCX、変換補助処理、Test、Workflow を同じ Change で更新する。CI 成功後に `main` へマージし、新しい Patch Tag で PRD/HLD の2 Asset を公開する。Rollback は Workflow を直前版へ戻し、失敗したタグでは Release を公開しない。
