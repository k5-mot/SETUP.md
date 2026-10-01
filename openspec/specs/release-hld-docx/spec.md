<!-- markdownlint-disable MD013 -->

# release-hld-docx Specification

## Purpose

手動で作成された正式な Release Tag に対応する基本設計書を、Git 管理された正本 Markdown から再生成し、検証済みの DOCX として GitHub Releases から配布できるようにする。

## Requirements

### Requirement: 正式なタグだけで基本設計書を公開する

System は、`v<MAJOR>.<MINOR>.<PATCH>` 形式のタグが `main` 上の Commit を指し、その Commit の `quality` Job が成功している場合に限り、基本設計書の Release 処理を実行しなければならない（MUST）。タグは自動作成してはならない（MUST NOT）。

品質要求 QR-REL-003（セキュリティ）の測定量は条件を満たさないタグからの Release 件数、目標値は0件、条件はタグの push、検証方法は Workflow の条件検査である。

#### Scenario: 正式なタグが push される

- **WHEN** `main` 上の品質検査済み Commit に `v1.2.3` タグが手動で付けられ push される
- **THEN** System はその Commit の基本設計書を Release 処理へ進める

#### Scenario: タグの条件を満たさない

- **WHEN** タグ名、`main` 上の Commit、または `quality` 成功の条件を満たさない
- **THEN** System は Release を作成しない

### Requirement: 正本から DOCX を生成して Release に登録する

System は、対象 Commit の `openspec/schemas/mysdd` を検証し、`openspec/publics/prd.md` と `openspec/publics/hld.md` から非空で検査済みの `prd.docx` と `hld.docx` を生成して、同じタグの GitHub Release に2件の Asset として登録しなければならない（MUST）。正本 Markdown と Schema を変更してはならず（MUST NOT）、DOCX を Git に追跡させてはならない（MUST NOT）。いずれかの生成または検査に失敗した場合は Release を公開してはならない（MUST NOT）。

品質要求 QR-REL-001 および QR-DOCX-004（機能適合性・信頼性）の測定量は有効なタグでの2件の Release Asset 登録率と部分 Release 件数、目標値は100%と0件、条件は入力と検証が正常な場合、検証方法は生成 DOCX の検査と Release Asset の確認である。QR-REL-004 および QR-DOCX-005（保守性）の測定量は Git 追跡された生成 DOCX 件数、目標値は0件、検証方法は Git 状態の確認である。

#### Scenario: 検証と変換が成功する

- **WHEN** 正式なタグの Schema、PRD 正本、HLD 正本が有効である
- **THEN** 非空で検査済みの `prd.docx` と `hld.docx` が対象タグの Release から取得できる
- **THEN** `prd.md`、`hld.md`、Schema の内容は変わらない

#### Scenario: 一方の文書生成が失敗する

- **WHEN** PRD または HLD の生成、フィールド更新、構造検査のいずれかが失敗する
- **THEN** System は部分的な Release を作成しない
- **THEN** 失敗した Step を Job Log に記録する

### Requirement: 失敗時は Release を公開しない

System は、Schema 検証、DOCX 変換、または出力確認に失敗した場合、Release を作成せず、失敗箇所を Job Log に示さなければならない（MUST）。

品質要求 QR-REL-002（信頼性）の測定量は失敗時に作成された Release 件数、目標値は0件、条件は検証または変換失敗、検証方法は失敗経路と Release の確認である。

#### Scenario: Schema または変換が失敗する

- **WHEN** Schema 検証、変換、または生成 DOCX の検査が失敗する
- **THEN** System は Release を作成せず、失敗した Step を記録する
