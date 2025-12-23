---
name: issue-creator
description: ユーザーとの対話を通じて適切なGitHub Issueを作成する統合スキル。コード分析結果からのIssue作成、初級者向けタスクのIssue化、通常のIssue作成など、文脈に応じて最適な方法でIssueを生成する。「issueを作成して」「分析結果からissueにして」「good first issueを作って」などの依頼に対応
---

# Issue Creator - GitHub Issue作成統合スキル

ユーザーとの対話を通じて、文脈に応じた適切なGitHub Issueを作成します。

## 使用タイミング

### 通常のIssue作成
- 「Issueを作成して」
- 「バグを報告したい」
- 「機能追加のIssueを作りたい」

### コード分析結果からのIssue作成
- 「分析結果からissueを作成して」
- 「この問題をissue化して」
- 「エラーをissueにまとめて」

### 初級者向けIssue作成
- 「初級者向けissueを作成して」
- 「good first issueを登録して」
- 「ビギナー向けタスクをissue化して」

## 実行フロー

### 1. プロジェクト環境の確認
- Gitリポジトリの確認
- 標準ラベルの読み込み（`.claude/labels.md`）
  - 未設定の場合は`/copy-labels`実行を提案

### 2. Issue作成モードの判定

| キーワード | モード | 確認 |
|-----------|--------|------|
| 「分析結果から」「エラーから」 | コード分析モード | 不要 |
| 「初級者向け」「good first issue」 | Good First Issueモード | 不要 |
| その他 | 通常モード | 必要な場合のみ |

**詳細**: `references/issue-modes.md` 参照

### 3. モード別処理

#### モード1: コード分析Issue作成
1. 分析結果サマリー表示
2. 作成範囲確認（全て/Critical/High/カテゴリ指定）
3. Issue粒度確認（詳細/中/粗）
4. グループ化基準確認
5. Issue内容生成
6. ユーザー確認
7. GitHub Issue作成

#### モード2: Good First Issue作成
1. 初級者向けタスク特定
2. タスク評価と選定
3. 詳細な実装手順生成
4. ユーザー確認
5. Good First Issue作成

#### モード3: 通常Issue作成
1. Issue情報の対話的聞き取り
2. Issue本文構成
3. ユーザー確認
4. GitHub Issue作成

### 4. Issue内容のプレビューと確認

```
作成予定のIssue一覧:

1. [Bug] 欠落モデルファイルの作成
   - 優先度: Critical
   - 影響: badge.dart, goal.dart
   - 見積: 4-6時間

2. [Bug] パス記述エラーの修正
   - 優先度: High
   - 影響: goal_management_usecase.dart
   - 見積: 30分

このままIssueを作成しますか？
- はい（すべて作成）
- 一部のみ作成（番号を指定）
- 内容を修正
- キャンセル
```

### 5. GitHub Issue作成

標準ラベルを使用:
```bash
gh issue create \
  --title "[Bug] 欠落モデルファイルの作成 (Badge, Goal関連)" \
  --body-file issue_content.md \
  --label "Type：バグ" \
  --label "Priority：最優先"
```

**注意**:
- ラベルが存在しない場合はラベルなしで作成
- `/copy-labels`実行を提案
- レート制限への配慮（大量作成時は5件ごとに1秒待機）

### 6. 作成結果の報告

```
✅ Issue作成完了

作成したIssue: 10件

Critical:
- #45: [Bug] 欠落モデルファイルの作成
- #46: [Bug] 欠落リポジトリインターフェースの作成

High:
- #47: [Bug] パス記述エラーの修正
- #48: [Refactoring] 未定義メソッドの実装
[...]

次のステップ:
1. Critical Issueから優先的に対応
2. 各Issueにブランチを作成して修正
3. PRを作成してレビュー
```

## Issueテンプレート

詳細は `references/issue-templates.md` 参照

- コード分析Issue用テンプレート
- Good First Issue用テンプレート
- 通常Issue用テンプレート
- 標準ラベルのマッピング

## 使用例

### 例1: 通常のバグ報告
**ユーザー**: バグを報告したい

**動作**: モード確認 → 通常モード → 対話的にIssue情報を聞き取り → Issue作成

### 例2: コード分析結果からIssue作成（自動判定）
**ユーザー**: growth-diaryの分析結果から、Criticalのissueだけ作成して

**動作**: コード分析モード自動起動 → Criticalに絞り込み → Issue作成

### 例3: Good First Issue作成（自動判定）
**ユーザー**: 初級者向けissueを5件作成して

**動作**: Good First Issueモード自動起動 → タスク特定 → Issue作成

## エラーハンドリング

### GitHub認証エラー
```
エラー: GitHub認証が必要です。
以下のコマンドで認証してください:
  gh auth login
```

### ラベルが存在しない
```
警告: 標準ラベルが存在しません
/copy-labelsを実行してラベルを設定することを推奨します
ラベルなしでIssueを作成しますか？ (y/n)
```

### レート制限
```
警告: GitHubのレート制限に達しました
作成済み: 50件 / 予定: 100件
残り50件は1時間後に自動再開しますか？
```

## 注意事項

1. **大量Issue作成の警告** - 20件以上作成する場合は警告表示
2. **既存Issue重複チェック** - タイトル類似度70%以上で警告
3. **プライベートリポジトリ権限** - Issue作成権限を事前確認
4. **標準ラベルの管理** - `.claude/labels.md`を必ず参照

## 関連スキル

- `issue-fixer` - Issue対応スキル（後工程）
- `pr-creator` - PR作成スキル（後工程）
- `/copy-labels` - 標準ラベル設定コマンド
