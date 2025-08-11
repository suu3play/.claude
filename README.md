# Claude Code 設定ファイル

Claude Code の動作を制御する設定ファイル（CLAUDE.md）の共有リポジトリです。

## 概要

このリポジトリには、プロフェッショナルなソフトウェア開発をサポートするための Claude Code 設定が含まれています。一貫した開発品質とコーディング規約を維持するための包括的なガイドラインを提供します。

## 設定内容

### アシスタント設定

-   対象ユーザー: ソフトウェアエンジニア
-   対応言語: Python, JavaScript, TypeScript, C#, SQL 等
-   品質重視: 保守性の高いコード・技術解説

### 開発方針

-   初回実装時のテスト必須
-   .gitignore 自動生成
-   言語別標準除外パターン適用

### コード品質基準

-   型ヒント完全対応
-   単一責任原則
-   88 文字行長制限
-   既存コードスタイル遵守

### テスト要件

-   境界値・異常系テスト
-   新機能対応テスト
-   回帰テスト

### Git 操作ルール

-   プルリクエスト重視
-   生成ツール名記載禁止
-   最小差分コミット

## 使用方法

### 1. カスタムスラッシュコマンド（推奨）

標準テンプレートとラベル体系を簡単に適用できるコマンドが利用可能です。

#### 個別プロジェクト適用

```bash
# ラベル体系の適用
/copy-labels [プロジェクト名]

# issueテンプレートの適用
/copy-templates [プロジェクト名] [プロジェクトタイプ]
```

#### 全プロジェクト一括適用

```bash
# 全プロジェクトに標準ラベル体系を適用
/copy-labels all

# 全プロジェクトに適切なテンプレートを適用（自動判定）
/copy-templates all
```

**対象プロジェクト** (all 指定時)：
作業ディレクトリ（`D:\自己開発`）配下のディレクトリを自動スキャンし、
プロジェクトタイプを判定して適用します。

### 2. 個人プロジェクトでの利用

```bash
# Claude Codeプロジェクトのルートディレクトリで
curl -o CLAUDE.md https://raw.githubusercontent.com/[ユーザー名]/claude-config/main/CLAUDE.md
```

### 3. チーム共有での利用

```bash
# プロジェクトにサブモジュールとして追加
git submodule add https://github.com/[ユーザー名]/claude-config.git .claude
ln -s .claude/CLAUDE.md CLAUDE.md
```

### 4. 環境設定の調整

CLAUDE.md 内の開発環境設定を、各プロジェクトの環境に合わせて編集してください：

```markdown
## 開発環境設定

-   作業ディレクトリ: `/path/to/your/project`
-   シンボリックリンク設定: 各環境に応じて調整
```

## ファイル構成

```
.claude/
├── CLAUDE.md                           # メイン設定ファイル
├── README.md                           # このファイル
├── settings.local.json                 # ローカル設定ファイル
├── .github/
│   └── ISSUE_TEMPLATE/                 # 標準issueテンプレート
│       ├── 🐛バグ報告.md
│       ├── 🚀新規機能・改善提案.md
│       └── ❓質問・相談.md
├── commands/                           # カスタムスラッシュコマンド
│   ├── copy-labels.md
│   ├── copy-templates.md
│   ├── create-pr.md
│   └── issue.md
├── rules/                              # 開発ルール
│   ├── code-quality-standards.md
│   ├── development-workflow.md
│   ├── issue-management.md
│   └── testing-requirements.md
└── templates/                          # テンプレート管理
    ├── code-quality-check-template.md
    ├── issue-template.md
    ├── project-detection.md           # プロジェクト自動判定システム
    ├── pull-request-template.md
    └── github/                         # GitHubテンプレート関連
        ├── bug-report-template.md
        ├── feature-request-template.md
        ├── question-template.md
        └── standard-labels.md
```

## 設定項目詳細

### 行動指針

-   **簡潔性**: 必要十分な技術背景を含む簡潔な回答
-   **実用性**: そのまま使える可読性の高いコード
-   **予防性**: 事前の注意点・警告提示
-   **具体性**: 曖昧な表現を避けた具体的実装
-   **品質重視**: パフォーマンス・可読性・スケーラビリティ重視

### コミュニケーションスタイル

-   冷静・丁寧・専門的なトーン
-   絵文字は原則使用しない
-   日本語優先、英語対応

### 対応言語・フレームワーク別 .gitignore

#### Node.js/React

```
node_modules/
.env
.env.local
dist/
build/
*.log
```

#### Python

```
__pycache__/
*.pyc
.venv/
.env
*.egg-info/
```

#### C#/.NET

```
bin/
obj/
.vs/
*.user
*.suo
```

#### 一般

```
.DS_Store
Thumbs.db
*.log
.env
```

## 主要機能

### 🏷️ 標準ラベル体系

統一された日本語ラベルで issue 管理を効率化：

**Type 系ラベル**

-   Type：ドキュメント更新、バグ、リファクタリング、新機能・既存改修、good first issue、作業、質問・相談

**Priority 系ラベル**

-   Priority：最優先、中、低

**緊急度系ラベル（質問・相談用）**

-   緊急度：高、中、低

### 📋 充実した issue テンプレート

プロジェクトタイプ別に最適化されたテンプレート：

-   **🐛 バグ報告**: 環境情報付きバグレポート
-   **🚀 新規機能・改善提案**: 受け入れ条件付き機能要求
-   **❓ 質問・相談**: 緊急度付き技術相談

### 🔄 動的一括管理機能

all 引数で全プロジェクトに一括適用：

-   **自動検出**: 作業ディレクトリ配下のプロジェクトを自動スキャン
-   **メンテナンスフリー**: 新規プロジェクト追加時の手動更新不要
-   **タイプ自動判定**: ファイル構造からプロジェクトタイプを自動識別
-   **効率性**: 複数プロジェクトを同時管理
-   **一貫性**: 統一された issue 管理体系

## カスタマイズ

### プロジェクト固有の設定追加

CLAUDE.md を各プロジェクトの要件に合わせてカスタマイズできます：

1. 使用する言語・フレームワークに特化した設定
2. チーム固有のコーディング規約
3. プロジェクト固有のツール・ライブラリ

### 設定の拡張例

```markdown
## プロジェクト固有設定

### 使用技術スタック

-   フロントエンド: React + TypeScript
-   バックエンド: Node.js + Express
-   データベース: PostgreSQL
-   インフラ: Docker + AWS

### 追加ツール

-   Linter: ESLint + Prettier
-   テスト: Jest + Testing Library
-   CI/CD: GitHub Actions
```

## コントリビューション

設定の改善提案やバグ報告は Issue または Pull Request でお知らせください。

### 改善提案の例

-   新しい言語・フレームワーク対応
-   コード品質基準の追加
-   テスト戦略の改善
-   ドキュメントの充実

## ライセンス

MIT License

## 更新履歴

-   v1.0.0: 初期リリース
    -   基本的な Claude Code 設定
    -   開発方針・コード品質基準
    -   Git 操作ルール
    -   .gitignore 自動生成対応

---

**高品質なソフトウェア開発を Claude Code でサポート**
