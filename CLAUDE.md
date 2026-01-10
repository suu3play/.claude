# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## リポジトリ概要

このリポジトリは**Claude Code設定管理リポジトリ**です。プロフェッショナルな開発をサポートするための：
- 開発ワークフロールール
- コード品質基準
- Issue/PR管理テンプレート
- カスタムスキル
- スラッシュコマンド

を一元管理しています。

## アーキテクチャ

### ディレクトリ構造

```
.claude/                   # Claude Code設定ファイル群
├── rules/                 # 開発ルール定義
│   ├── development-workflow.md      # ブランチ作成→コミット→PR作成フロー
│   ├── code-quality-standards.md    # 品質基準とチェック項目
│   ├── testing-requirements.md      # テスト要件
│   └── documentation-standards.md   # ドキュメント標準
├── skills/                # Claude Codeカスタムスキル（13個）
│   ├── pr-creator/        # PR作成（品質チェック→コミット→プッシュ→PR）
│   ├── issue-creator/     # Issue作成（分析→グルーピング→一括作成）
│   ├── code-analyzer/     # コード分析→Issue登録
│   ├── branch-cleaner/    # ブランチ整理→main更新
│   ├── version-manager/   # バージョン管理（SemVer対応）
│   └── ...                # その他8個のスキル
├── templates/             # 各種テンプレート
│   ├── pull-request-template.md
│   ├── issue-template.md
│   └── code-quality-check-template.md
├── commands/              # カスタムスラッシュコマンド
│   └── copy-labels.md     # ラベル体系コピーコマンド
├── labels.md              # 標準ラベル定義（Type系/Priority系）
└── settings.json          # Claude Code設定

個別プロジェクト/           # 各プロジェクトは別リポジトリとして管理
├── desk-app-kit/          # .gitignoreで除外
├── hobby-weather/
└── ...
```

### 設定の階層構造

1. **CLAUDE.md（このファイル）** - エントリーポイント
2. **rules/** - 作業開始前に読み込む詳細ルール
3. **skills/** - 自動発動するタスク専用エージェント
4. **templates/** - 成果物の標準フォーマット

## 重要な動作原則

### 言語とトーン
- デフォルトは**日本語**（ユーザーが英語で話した場合のみ英語で応答）
- 冷静・丁寧・専門的なトーン
- 絵文字は原則使用しない

### 生成ツール名の記載禁止
**いかなる記述にもClaude等の生成ツール名を一切記載しないこと**
- コード内コメント
- コミットメッセージ
- ドキュメント
- PR/Issue本文

### 作業フロー
複雑なタスクの場合、TodoWriteツールを使用して計画的に対応すること。

## 開発作業時の必須手順

**重要**: 開発作業を開始する前に、必ず`.claude/rules/development-workflow.md`を読み込んでから作業を開始すること。

### 基本フロー

1. **作業用ブランチ作成**
   - Issue対応: `feature/issue-[番号]`
   - 機能追加: `feature/[機能名]`
   - バグ修正: `fix/[修正内容]`

2. **コード品質チェック実行**（必須）
   - `testing-requirements.md`記載の全チェック項目を実行
   - 結果を`./code_check/code_check_yyyyMMddHHmm.md`に出力
   - すべてのチェックが成功することを確認

3. **コミット** - Conventional Commits形式（feat:, fix:, docs:, refactor:, test:）

4. **ユーザー報告と確認待ち**
   - 変更ファイル一覧と変更内容サマリーを表示
   - 品質チェック結果を報告
   - ユーザーの承認を待つ

5. **プッシュ** - ユーザー承認後に実行

6. **PR作成** - ユーザーから明示的に指示された場合のみ

## スキルシステム

このリポジトリには13個のカスタムスキルが定義されています。スキルは特定のキーワードで自動発動します。

### 主要スキル

| スキル名 | 発動キーワード | 機能 |
|---------|-------------|------|
| pr-creator | "PR作成", "プルリク" | 品質チェック→コミット→PR作成 |
| issue-creator | "Issue作成", "issue登録" | 分析結果をIssueとして一括登録 |
| code-analyzer | "コード分析", "バグ検出" | 静的解析→Issue自動登録 |
| branch-cleaner | "ブランチ整理" | マージ済みブランチ削除→main更新 |
| version-manager | "バージョン更新" | SemVerに従ったバージョン管理 |

詳細: `skills/*/SKILL.md`を参照

## ルールファイルの使用方法

作業内容に応じて該当ルールを読み込んでから作業を開始：

- **開発ワークフロー**: `.claude/rules/development-workflow.md`
- **コード品質基準**: `.claude/rules/code-quality-standards.md`
- **テスト要件**: `.claude/rules/testing-requirements.md`
- **ドキュメント標準**: `.claude/rules/documentation-standards.md`

## テンプレートの使用

成果物作成時は該当テンプレートの構成に従うこと：

- **プルリクエスト**: `.claude/templates/pull-request-template.md`
- **Issue作成**: `.claude/templates/issue-template.md`
- **コード品質チェック**: `.claude/templates/code-quality-check-template.md`

## 個別プロジェクトの扱い

`desk-app-kit/`, `hobby-weather/`等の個別プロジェクトディレクトリは：
- 別リポジトリとして独立管理
- `.gitignore`で除外済み
- このリポジトリでは追跡しない

## カスタムスラッシュコマンド

現在利用可能なコマンド:
- `/copy-labels` - 標準ラベル体系を個別プロジェクトにコピー

スキルで担保されているため、以下のコマンドは削除済み:
- `/create-pr` → pr-creatorスキル
- `/issue` → issue-fixerスキル
- `/branch-cleanup` → branch-cleanerスキル
