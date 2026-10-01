<!-- markdownlint-disable MD041 MD013 -->

## Context

動機は [proposal.md](proposal.md) を参照。正本 `openspec/publics/hld.md` と `mysdd` Schema は Git 管理され、DOCX は既存の Pandoc 3.11 契約で生成する。Release Tag は Maintainer が `quality` 成功後に手動作成する。

## Goals / Non-Goals

**Goals:** 同じタグの入力、検証結果、Release Asset を対応付ける。

**Non-Goals:** Schema 内容を DOCX に収録すること、タグの自動作成、正本の再生成。

## Decisions

- タグ push を起点とする独立 Workflow を追加する。`quality.yml` に Release 書込権限を与える必要がなく、公開処理の起点を手動タグに限定できる。
- 完全な SemVer 形式、`main` への包含、および対象 Commit の成功した `quality` の push Run を検査する。単に `v*` で起動するだけでは、既存の手動タグ規則を保証できない。
- `openspec schema validate mysdd --verbose` の後、既存 `markdown2docx` Skill と同じ Pandoc 引数、参照 DOCX、出力名を使う。Schema は入力文書として結合しない。
- `gh release create --verify-tag` で既存タグを使い、生成 DOCX を作成と同時に添付する。成功前に Asset のない Release を公開する経路を避ける。

## Quality Attribute Design

| ID | 方法・Trade-off | Evidence |
| --- | --- | --- |
| QR-REL-001 | 生成後に非空ファイルを確認し、Release 作成に Asset を渡す | DOCX 生成 Test、Workflow Review |
| QR-REL-002 | 全検証を Release 作成前に実施する | 失敗経路の Workflow Review |
| QR-REL-003 | タグと成功 Run を確認し、Token 権限を当該 Job に限定する | 条件・権限の Review |
| QR-REL-004 | 既存の参照 DOCX と変換引数を再利用する | 差分、Git Status |

## Lifecycle, Migration and Operations

既存の手動タグ手順は維持する。公開失敗は Actions の Job Log で調査し、入力または Workflow を修正後に再実行する。既存 Release やタグの移動は行わない。Workflow の廃止時は追加ファイルを除去し、公開済み Asset は履歴として保持する。

## Risks / Trade-offs

- [リリース時点で `quality` Run の記録を取得できない] → 公開を停止し、Maintainer が Run の状態を確認する。
- [Word の目次などの Field 値が Runner 上で更新されない] → 参照 DOCX の自動更新設定を維持し、Field Cache を最新値とは扱わない。

## Migration Plan

Workflow を `main` に取り込んだ後、次の手動 SemVer Tag から利用する。問題があれば Workflow を修正し、対象の未公開タグで再実行する。公開済みタグは移動しない。
