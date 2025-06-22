# Claude Code 設定ファイル

Claude Codeの動作を制御する設定ファイル（CLAUDE.md）の共有リポジトリです。

## 概要

このリポジトリには、プロフェッショナルなソフトウェア開発をサポートするためのClaude Code設定が含まれています。一貫した開発品質とコーディング規約を維持するための包括的なガイドラインを提供します。

## 設定内容

### アシスタント設定
- 対象ユーザー: ソフトウェアエンジニア
- 対応言語: Python, JavaScript, TypeScript, C#, SQL 等
- 品質重視: 保守性の高いコード・技術解説

### 開発方針
- 初回実装時のテスト必須
- .gitignore自動生成
- 言語別標準除外パターン適用

### コード品質基準
- 型ヒント完全対応
- 単一責任原則
- 88文字行長制限
- 既存コードスタイル遵守

### テスト要件
- 境界値・異常系テスト
- 新機能対応テスト
- 回帰テスト

### Git操作ルール
- プルリクエスト重視
- 生成ツール名記載禁止
- 最小差分コミット

## 使用方法

### 1. 個人プロジェクトでの利用

```bash
# Claude Codeプロジェクトのルートディレクトリで
curl -o CLAUDE.md https://raw.githubusercontent.com/[ユーザー名]/claude-config/main/CLAUDE.md
```

### 2. チーム共有での利用

```bash
# プロジェクトにサブモジュールとして追加
git submodule add https://github.com/[ユーザー名]/claude-config.git .claude
ln -s .claude/CLAUDE.md CLAUDE.md
```

### 3. 環境設定の調整

CLAUDE.md内の開発環境設定を、各プロジェクトの環境に合わせて編集してください：

```markdown
## 開発環境設定

- 作業ディレクトリ: `/path/to/your/project`
- シンボリックリンク設定: 各環境に応じて調整
```

## ファイル構成

```
claude-config/
├── CLAUDE.md          # メイン設定ファイル
├── README.md          # このファイル
└── examples/          # 使用例（今後追加予定）
```

## 設定項目詳細

### 行動指針
- **簡潔性**: 必要十分な技術背景を含む簡潔な回答
- **実用性**: そのまま使える可読性の高いコード
- **予防性**: 事前の注意点・警告提示
- **具体性**: 曖昧な表現を避けた具体的実装
- **品質重視**: パフォーマンス・可読性・スケーラビリティ重視

### コミュニケーションスタイル
- 冷静・丁寧・専門的なトーン
- 絵文字は原則使用しない
- 日本語優先、英語対応

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

## カスタマイズ

### プロジェクト固有の設定追加

CLAUDE.mdを各プロジェクトの要件に合わせてカスタマイズできます：

1. 使用する言語・フレームワークに特化した設定
2. チーム固有のコーディング規約
3. プロジェクト固有のツール・ライブラリ

### 設定の拡張例

```markdown
## プロジェクト固有設定

### 使用技術スタック
- フロントエンド: React + TypeScript
- バックエンド: Node.js + Express
- データベース: PostgreSQL
- インフラ: Docker + AWS

### 追加ツール
- Linter: ESLint + Prettier
- テスト: Jest + Testing Library
- CI/CD: GitHub Actions
```

## コントリビューション

設定の改善提案やバグ報告は Issue または Pull Request でお知らせください。

### 改善提案の例
- 新しい言語・フレームワーク対応
- コード品質基準の追加
- テスト戦略の改善
- ドキュメントの充実

## ライセンス

MIT License

## 更新履歴

- v1.0.0: 初期リリース
  - 基本的なClaude Code設定
  - 開発方針・コード品質基準
  - Git操作ルール
  - .gitignore自動生成対応

---

**高品質なソフトウェア開発をClaude Codeでサポート**