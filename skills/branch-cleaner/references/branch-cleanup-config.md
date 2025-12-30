# ブランチクリーンアップ - 設定オプション

このドキュメントは、branch-cleanerスキルの動作をカスタマイズするための設定オプションを詳しく説明します。

## 設定ファイルの配置

プロジェクトルートに `.claude/branch-cleanup-config.json` を配置:

```
[プロジェクトルート]/
├── .claude/
│   └── branch-cleanup-config.json
├── growth-diary/
├── portfolio/
└── source-flow/
```

## 基本設定例

```json
{
  "protectedBranches": ["main", "develop", "staging"],
  "autoConfirm": false,
  "deleteUnmerged": false,
  "skipProjects": ["legacy-project", "archived-repo"],
  "logResults": true,
  "logPath": "./logs/branch_cleanup.log"
}
```

## 設定項目の詳細

### protectedBranches

**説明**: 削除から保護するブランチ名のリスト

**デフォルト**: `["main"]`

**設定例**:
```json
{
  "protectedBranches": ["main", "develop", "staging", "production"]
}
```

**使用ケース**:
- 本番環境ブランチを保護
- 開発ブランチを保護
- リリースブランチを保護

**注意**: これらのブランチは常に削除対象から除外されます。

### autoConfirm

**説明**: ユーザー確認をスキップして自動実行

**デフォルト**: `false`

**設定例**:
```json
{
  "autoConfirm": true
}
```

**使用ケース**:
- CI/CD環境での自動実行
- 定期的な自動クリーンアップ
- 開発者の操作を減らす

**注意**:
- `true`に設定すると、削除前の確認なしで実行されます
- 本番環境では`false`を推奨
- 安全性チェック（未コミット、未プッシュ）は引き続き実施されます

### deleteUnmerged

**説明**: 未マージブランチも削除対象に含める

**デフォルト**: `false`

**設定例**:
```json
{
  "deleteUnmerged": true,
  "unmergedConfirm": true
}
```

**使用ケース**:
- 古い実験的ブランチを一括削除
- プロトタイプブランチの整理
- 不要になった機能ブランチの削除

**注意**:
- `true`に設定すると、未マージブランチが削除されます（コミットが失われます）
- `unmergedConfirm: true`と併用すると、未マージブランチごとに確認
- 慎重に使用してください

### skipProjects

**説明**: 全プロジェクトモードでスキップするプロジェクト名のリスト

**デフォルト**: `[]`

**設定例**:
```json
{
  "skipProjects": ["legacy-project", "archived-repo", "temp-workspace"]
}
```

**使用ケース**:
- アーカイブプロジェクトを除外
- レガシープロジェクトを除外
- 一時的なワークスペースを除外

**注意**: 単一プロジェクトモードでは無効

### logResults

**説明**: 実行結果をログファイルに記録

**デフォルト**: `false`

**設定例**:
```json
{
  "logResults": true,
  "logPath": "./logs/branch_cleanup.log",
  "logLevel": "info"
}
```

**使用ケース**:
- 実行履歴の記録
- トラブルシューティング
- 監査証跡の作成

**ログレベル**:
- `"debug"`: デバッグ情報を含むすべてのログ
- `"info"`: 通常の実行情報（デフォルト）
- `"warning"`: 警告とエラーのみ
- `"error"`: エラーのみ

### logPath

**説明**: ログファイルの出力パス

**デフォルト**: `"./logs/branch_cleanup.log"`

**設定例**:
```json
{
  "logPath": "/var/log/branch_cleanup.log"
}
```

**注意**:
- 相対パスまたは絶対パスを指定
- ディレクトリが存在しない場合は自動作成

## 高度な設定

### branchPatterns

**説明**: 削除対象にするブランチ名のパターン

**デフォルト**: `["feature/*", "fix/*", "hotfix/*"]`

**設定例**:
```json
{
  "branchPatterns": [
    "feature/*",
    "fix/*",
    "hotfix/*",
    "bugfix/*",
    "release/*"
  ]
}
```

**使用ケース**:
- 特定のプレフィックスを持つブランチのみ削除
- ブランチ命名規則に従った削除

### excludePatterns

**説明**: 削除対象から除外するブランチ名のパターン

**デフォルト**: `[]`

**設定例**:
```json
{
  "excludePatterns": [
    "wip/*",
    "temp/*",
    "*-keep"
  ]
}
```

**使用ケース**:
- 作業中ブランチを保護
- 特定のパターンを持つブランチを保護

### ageDays

**説明**: 指定日数以上古いブランチのみを削除対象

**デフォルト**: `null`（制限なし）

**設定例**:
```json
{
  "ageDays": 30
}
```

**使用ケース**:
- 古いブランチのみ削除
- 最近のブランチは保護

**注意**: ブランチの最終コミット日時を基準に判定

### dryRun

**説明**: 実際には削除せず、削除対象を表示のみ

**デフォルト**: `false`

**設定例**:
```json
{
  "dryRun": true
}
```

**使用ケース**:
- 削除対象の事前確認
- テスト実行

### notifications

**説明**: 実行結果の通知設定

**デフォルト**: `null`

**設定例**:
```json
{
  "notifications": {
    "enabled": true,
    "method": "slack",
    "webhook": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
    "onSuccess": true,
    "onError": true
  }
}
```

**通知方法**:
- `"slack"`: Slack Webhook
- `"email"`: メール（SMTP設定が必要）
- `"teams"`: Microsoft Teams Webhook

## 設定例のテンプレート

### 開発環境用

```json
{
  "protectedBranches": ["main", "develop"],
  "autoConfirm": false,
  "deleteUnmerged": false,
  "logResults": true,
  "logPath": "./logs/branch_cleanup.log",
  "dryRun": false
}
```

### CI/CD環境用

```json
{
  "protectedBranches": ["main", "develop", "staging", "production"],
  "autoConfirm": true,
  "deleteUnmerged": false,
  "skipProjects": ["archived-repo"],
  "logResults": true,
  "logPath": "/var/log/branch_cleanup.log",
  "logLevel": "info",
  "notifications": {
    "enabled": true,
    "method": "slack",
    "webhook": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
    "onSuccess": false,
    "onError": true
  }
}
```

### 厳格なクリーンアップ用

```json
{
  "protectedBranches": ["main"],
  "autoConfirm": false,
  "deleteUnmerged": true,
  "unmergedConfirm": true,
  "branchPatterns": ["feature/*", "fix/*"],
  "ageDays": 90,
  "logResults": true
}
```

### テスト実行用

```json
{
  "dryRun": true,
  "logResults": true,
  "logLevel": "debug"
}
```

## 設定の優先順位

1. コマンドライン引数（最優先）
2. プロジェクト固有の設定ファイル
3. グローバル設定ファイル
4. デフォルト値

## 設定のバリデーション

スキル実行時に設定ファイルが検証されます：

**検証項目**:
- JSON構文エラー
- 不正な設定値
- 必須項目の欠如

**エラー例**:
```
❌ 設定ファイルエラー: .claude/branch-cleanup-config.json

原因: Invalid JSON syntax at line 5

修正してください:
  - JSON構文を確認
  - カンマやブラケットの不足をチェック
```

## トラブルシューティング

### 設定が反映されない

**確認事項**:
1. 設定ファイルのパスが正しいか
2. JSON構文が正しいか
3. プロジェクトルートに配置されているか

**デバッグ**:
```bash
# 設定ファイルの確認
cat .claude/branch-cleanup-config.json

# JSON構文チェック
python -m json.tool .claude/branch-cleanup-config.json
```

### autoConfirmが動作しない

**原因**: 安全性チェックが優先されます

**対処**:
- 未コミット、未プッシュがある場合は自動確認されません
- まずこれらを解決してください

### ログファイルが作成されない

**原因**:
- ログディレクトリが存在しない
- 書き込み権限がない

**対処**:
```bash
# ディレクトリ作成
mkdir -p logs

# 権限確認
ls -la logs/
```
