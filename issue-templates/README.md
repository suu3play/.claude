# Issue Templates

このディレクトリには、GitHubリポジトリで使用するためのIssueテンプレートが含まれています。

## テンプレート一覧

### 📋 基本テンプレート

| テンプレート | 用途 | ファイル |
|------------|------|----------|
| 🐛 **Bug Report** | バグ・不具合の報告 | `bug-report.md` |
| ✨ **Feature Request** | 新機能の提案 | `feature-request.md` |
| 📝 **Task** | 作業タスクの管理 | `task.md` |
| 🚀 **Improvement** | 既存機能の改善提案 | `improvement.md` |
| ❓ **Question** | 質問・相談 | `question.md` |

## 使用方法

### GitHubリポジトリでの設定

1. リポジトリに `.github/ISSUE_TEMPLATE/` ディレクトリを作成
2. 各テンプレートファイルをコピー
3. 必要に応じてテンプレート内容をカスタマイズ

### ファイル配置例

```
.github/
└── ISSUE_TEMPLATE/
    ├── bug-report.md
    ├── feature-request.md
    ├── task.md
    ├── improvement.md
    └── question.md
```

### フロントマターの追加

GitHubで自動認識させるため、各テンプレートの先頭にフロントマターを追加：

```yaml
---
name: Bug Report
about: バグや不具合を報告する
title: '[BUG] '
labels: 'bug, priority-medium'
assignees: ''
---
```

## カスタマイズのポイント

### プロジェクト固有の調整

1. **ラベル名の統一**: プロジェクトで使用するラベル名に合わせる
2. **セクションの調整**: プロジェクトの特性に応じてセクションを追加・削除
3. **優先度レベル**: チームの運用に合わせて優先度を調整
4. **担当者フィールド**: チーム構成に応じて担当者の役割を調整

### 技術スタック別の追加項目

- **フロントエンド**: ブラウザ環境、画面サイズ
- **バックエンド**: サーバー環境、データベース情報
- **モバイルアプリ**: デバイス情報、OS バージョン
- **API**: エンドポイント情報、リクエスト例

## ベストプラクティス

### Issue作成時

1. **明確なタイトル**: 内容が一目でわかるタイトルをつける
2. **適切なテンプレート選択**: 内容に最も適したテンプレートを使用
3. **必須項目の記入**: ⚡や📋などのマークがついた項目は必ず記入
4. **ラベル付け**: 適切なラベルを設定して分類

### レビュー・対応時

1. **迅速な初期対応**: 24時間以内に何らかの反応を示す
2. **適切な優先度設定**: 影響度と緊急度を考慮して優先度を調整
3. **進捗の可視化**: プロジェクトボードやマイルストーンを活用

## 関連ドキュメント

- [GitHub Issue Templates Documentation](https://docs.github.com/ja/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [Pull Request Templates](../pull-request-templates/)
- [Labels Management](../labels/)

## 更新履歴

- `2024-07-22`: 初版作成（全5テンプレート）