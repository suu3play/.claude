# Analysis Issue Creator

コード分析結果を基にユーザーと対話しながら適切なGitHub Issueを作成するスキルです。

## 概要

このスキルは、静的解析ツールやコードレビューで発見された問題を、適切な粒度と優先度でGitHub Issueとして登録します。大量の問題を効率的に管理可能なIssueに変換し、開発チームの生産性を向上させます。

## 主な機能

### 1. インテリジェントなグループ化
- **ファイル単位**: 同じファイルの問題をまとめる
- **機能単位**: 関連機能の問題をまとめる
- **エラー種類単位**: 同種のエラーをまとめる
- **自動判定**: AI判断で最適にグループ化

### 2. 柔軟なフィルタリング
- 優先度で絞り込み（Critical, High, Medium, Low）
- カテゴリで絞り込み（Bug, Refactoring, Documentation等）
- カスタム条件指定

### 3. ユーザー対話型
- 作成前に必ず確認
- 重複チェック機能
- プレビュー表示

### 4. 充実したIssue内容
- 問題の詳細説明
- 修正方法の提案
- 見積もり時間
- チェックリスト

## ファイル構成

```
analysis-issue-creator/
├── SKILL.md                    # スキル本体（実行手順・ロジック）
├── README.md                   # このファイル
├── EXAMPLES.md                 # 使用例集
└── templates/
    └── issue-template.md       # Issueテンプレート
```

## 使い方

### 基本的な使用方法

```
# Criticalのみ作成（推奨）
「growth-diaryの分析結果から、Criticalのissueだけ作成して」

# 特定カテゴリ
「バグだけをissue化して」

# カスタム条件
「HighとCriticalのバグとリファクタリングだけ、ファイル単位でまとめて」
```

### トリガーキーワード

以下のフレーズでスキルが起動します:
- 「分析結果からissueを作成して」
- 「この問題をissue化して」
- 「バグレポートをGitHubに登録して」
- 「エラーをissueにまとめて」

## 典型的なワークフロー

### 1. コード分析実行
```
code-analyzerスキル、またはflutter analyze等を実行
```

### 2. Issue作成スキル起動
```
「分析結果からCriticalのissueを作成して」
```

### 3. 対話的に設定
- 作成範囲の選択
- Issue粒度の選択
- グループ化基準の選択

### 4. プレビュー確認
- 作成予定Issueの内容確認
- 必要に応じて修正

### 5. Issue作成実行
- GitHub Issueを自動作成
- 結果レポート生成

### 6. 後続作業
- `issue-fixer`スキルでIssue対応
- `pr-creator`スキルでPR作成

## Issue粒度の選び方

### 詳細粒度（Fine）
- **適用**: 問題数が少ない（< 10件）
- **メリット**: 各問題を個別に追跡できる
- **デメリット**: Issue数が多くなる

### 中粒度（Medium）- 推奨
- **適用**: 問題数が中程度（10-50件）
- **メリット**: 管理しやすく詳細度も保てる
- **デメリット**: グループ化基準の判断が必要

### 粗粒度（Coarse）
- **適用**: 問題数が多い（50件以上）
- **メリット**: Issue数を大幅に削減
- **デメリット**: 個別問題の追跡が難しい

## フィルタリング戦略

### 初回分析時
```
1. Criticalのみ作成 → 対応
2. 完了後、Highを作成 → 対応
3. 必要に応じてMedium以降を検討
```

### 継続的改善
```
1. 毎週Highまでを作成
2. 月次でMediumを作成
3. Lowは四半期ごと
```

### 緊急対応
```
1. Criticalを即座に作成・対応
2. ビルドエラーを最優先
3. セキュリティ問題は即日対応
```

## ラベル体系

### カテゴリラベル
- `bug`: バグ修正
- `refactoring`: コードリファクタリング
- `documentation`: ドキュメント更新
- `performance`: パフォーマンス改善
- `testing`: テスト追加・修正
- `security`: セキュリティ修正
- `accessibility`: アクセシビリティ改善

### 優先度ラベル
- `priority: critical`: 即座対応必要
- `priority: high`: 優先度高
- `priority: medium`: 通常優先度
- `priority: low`: 余裕があれば対応

### 状態ラベル
- `needs-implementation`: 実装待ち
- `needs-review`: レビュー待ち
- `in-progress`: 対応中

## 環境変数設定

`.env`ファイルで設定可能:

```bash
# デフォルト粒度
ISSUE_DEFAULT_GRANULARITY=medium

# デフォルト優先度フィルター
ISSUE_DEFAULT_PRIORITY=critical,high

# 自動アサイン
ISSUE_AUTO_ASSIGN=true

# マイルストーン
ISSUE_DEFAULT_MILESTONE=v1.0

# レポート出力先
ISSUE_REPORT_DIR=./reports

# レート制限待機時間（秒）
ISSUE_RATE_LIMIT_WAIT=1
```

## トラブルシューティング

### GitHub認証エラー
```bash
gh auth login
```

### レート制限
- 5件ごとに1秒待機（自動）
- 制限到達時は1時間後に再開

### ラベルが存在しない
- 自動作成オプションを選択
- または手動で事前作成

## 関連スキル

- **code-analyzer**: コード分析実行（前工程）
- **issue-fixer**: Issue対応（後工程）
- **pr-creator**: PR作成（後工程）
- **good-first-issue-creator**: 初心者向けIssue作成

## ライセンス

MIT

## 変更履歴

### v1.0.0 (2025-01-26)
- 初回リリース
- 基本機能実装
- グループ化ロジック実装
- テンプレート実装
