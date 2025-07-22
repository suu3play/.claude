# GitHub Templates & Configuration

GitHubリポジトリの運用を効率化するためのテンプレート集とワークフロー設定です。

## 📋 含まれるテンプレート

### Issue Templates (YML形式)
- **🐛 Bug Report** - バグレポート用のフォームテンプレート
- **✨ Feature/Enhancement** - 新機能・既存機能改善用の統合フォームテンプレート  
- **📝 Task** - タスク管理用のフォームテンプレート
- **❓ Question** - 質問・相談用のフォームテンプレート

### Pull Request Template
- 包括的なPRテンプレート（Markdown形式）
- チェックリスト、テスト項目、レビューポイント等を含む

### GitHub Actions Workflows
- **Issue Labeler** - Issueの自動ラベル付け
- **PR Labeler** - Pull Requestの自動ラベル付け
- **Auto Reviewer Assignment** - 自動レビューア割り当て

### Labels Configuration
- 統一されたラベルセット（YAML形式）
- 優先度、コンポーネント、状態別の分類

## 🚀 使用方法

### 1. 基本設定

リポジトリのルートに `.github` ディレクトリを作成し、以下のファイルをコピーしてください：

```
your-repo/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── config.yml
│   │   ├── bug-report.yml
│   │   ├── feature-enhancement.yml
│   │   ├── task.yml
│   │   └── question.yml
│   ├── workflows/
│   │   ├── issue-labeler.yml
│   │   └── pr-labeler.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── labels.yml
```

### 2. カスタマイズ

#### Issue Template Config
`.github/ISSUE_TEMPLATE/config.yml` を編集して、プロジェクト固有の情報を設定：

```yaml
contact_links:
  - name: 🌐 公式ドキュメント
    url: https://your-project-docs.com
    about: プロジェクトの詳細情報
  
  - name: 💬 ディスカッション  
    url: https://github.com/YOUR-ORG/YOUR-REPO/discussions
    about: 一般的な質問や議論
```

#### ワークフローの設定
`workflows/` ディレクトリのYMLファイルで以下を調整：

- **レビューア設定**: 特定の変更に対する自動レビューア指定
- **ラベル名**: プロジェクトで使用するラベル名に合わせる
- **権限設定**: リポジトリの権限設定に応じて調整

### 3. ラベルの同期

Labels設定を適用するために、[Label Sync](https://github.com/EndBug/label-sync) などのツールを使用：

```yaml
# .github/workflows/label-sync.yml
name: Sync Labels
on:
  push:
    branches: [main]
    paths: ['.github/labels.yml']

jobs:
  label-sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: EndBug/label-sync@v2
        with:
          config-file: .github/labels.yml
          token: ${{ secrets.GITHUB_TOKEN }}
```

## 🔧 高度な設定

### 自動化機能

#### Issue自動処理
- タイトルプレフィックスによる自動ラベル付け
- 優先度の自動判定
- コンポーネント別ラベリング

#### PR自動処理  
- 変更ファイルに基づく自動ラベル付け
- PRサイズの自動判定
- 自動レビューア割り当て

### カスタムラベル

プロジェクト固有のラベルを追加する場合は、`labels.yml` を編集：

```yaml
- name: "your-custom-label"
  color: "ff0000"
  description: "Your custom label description"
```

### レビューア自動割り当て

特定の変更に対して自動でレビューアを割り当て：

```javascript
// pr-labeler.yml内
if (changedFiles.some(file => file.includes('security'))) {
  reviewers.push('security-team');
}
```

## 📊 プロジェクト管理の改善

### メトリクス計測
- Issue解決時間の追跡
- PR処理時間の測定
- ラベル別の統計分析

### ワークフロー最適化
- 自動化によるマニュアル作業削減
- 一貫性のある分類・管理
- レビュープロセスの効率化

## 🎯 ベストプラクティス

### Issue管理
1. **明確なタイトル**: 内容が分かりやすいタイトルを使用
2. **適切なテンプレート**: 内容に最適なテンプレートを選択
3. **詳細な記述**: 必要な情報を漏れなく記載

### PR管理
1. **小さなPR**: レビューしやすいサイズに分割
2. **明確な変更内容**: 何を変更したかを明記
3. **適切なテスト**: 十分なテストの実施

### ラベル活用
1. **一貫性**: チーム全体で統一されたラベル使用
2. **適切な粒度**: 過度に細かすぎない分類
3. **定期的な見直し**: ラベルセットの定期的な最適化

## 🔄 メンテナンス

### 定期的な見直し
- 月次でのテンプレート効果確認
- ラベル使用状況の分析
- ワークフロー最適化の検討

### フィードバック収集
- チームメンバーからの改善提案
- 使いづらい点の特定と改善
- 新しい要件への対応

## 📞 サポート

このテンプレート集に関する質問や改善提案は、Issue またはディスカッションでお気軽にお聞かせください。

---

**更新履歴**
- 2024-07-22: 初版リリース（Issue Templates, PR Template, Workflows, Labels）