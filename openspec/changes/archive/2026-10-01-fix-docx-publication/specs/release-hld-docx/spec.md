<!-- markdownlint-disable MD013 MD022 MD032 MD041 -->

## MODIFIED Requirements

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
