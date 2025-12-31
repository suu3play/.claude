# Issue Fixer - 詳細ワークフローガイド

このドキュメントは、issue-fixerスキルの各ステップの詳細な実行方法を説明します。

## 全体フロー概要

issue-fixerスキルは、GitHub Issueの改修を10のステップで実行します：

1. 開発ワークフローの読み込み
2. プロジェクトとIssue番号の特定
3. GitHub Issueの取得と分析
4. ブランチの作成
5. 改修計画の立案
6. ユーザーへの改修計画確認
7. 実装の実行
8. 修正内容の確認フェーズ
9. 変更内容のコミット
10. プッシュとPR作成

## ステップ1: 開発ワークフローの読み込み

### 目的
プロジェクト固有の開発ルールを確認し、それに従った作業を行うため。

### 実行内容

#### 1. メインワークフローの読み込み
```bash
# .claude/rules/development-workflow.md を読み込み
```

#### 2. 必要に応じて関連ルール・テンプレートも読み込み
- `.claude/rules/code-quality-standards.md` - コード品質基準
- `.claude/templates/pull-request-template.md` - PRテンプレート
- `.claude/templates/code-quality-check-template.md` - 品質チェックテンプレート

### 確認事項
- ブランチ命名規則
- コミットメッセージ形式
- 品質チェック項目
- ユーザー確認フェーズの要件

## ステップ2: プロジェクトとIssue番号の特定

### 目的
どのプロジェクトのどのIssueを対応するか明確にする。

### パターン別の処理

#### パターン1: プロジェクト名とIssue番号が明示されている
**例**: 「growth-diary の issue 8 を改修して」

1. プロジェクト名を抽出: `growth-diary`
2. Issue番号を抽出: `8`
3. プロジェクトディレクトリを確認:
   ```bash
   ls "[プロジェクトルート]/growth-diary"
   ```

#### パターン2: Issue番号のみ指定（カレントディレクトリで実行）
**例**: 「issue 5 を対応して」

1. カレントディレクトリを確認:
   ```bash
   pwd
   ```
2. ディレクトリ名からプロジェクト名を判定
3. Issue番号を抽出: `5`

#### パターン3: 曖昧な指定
**例**: 「このissueを修正して」

1. ユーザーにプロジェクト名を確認:
   ```
   プロジェクト名を教えてください。
   利用可能なプロジェクト: [リスト表示]
   ```
2. ユーザーにIssue番号を確認:
   ```
   対応するIssue番号を教えてください。
   ```

### プロジェクトディレクトリの確認

#### 存在確認
```bash
if [ -d "[プロジェクトルート]/[プロジェクト名]" ]; then
  echo "プロジェクトが見つかりました"
else
  echo "エラー: プロジェクトが見つかりません"
fi
```

#### Gitリポジトリ確認
```bash
cd "[プロジェクトルート]/[プロジェクト名]"
git rev-parse --git-dir
```

## ステップ3: GitHub Issueの取得と分析

### 目的
Issue内容を理解し、実装要件を明確にする。

### Issue取得

#### コマンド実行
```bash
cd "[プロジェクトルート]/[プロジェクト名]"
gh issue view [issue番号]
```

#### 取得情報の例
```
title:	ユーザープロフィール編集機能を追加
state:	OPEN
author:	username
labels:	enhancement, Priority：中
assignees:
number:	42
--
## 概要
ユーザーが自分のプロフィール情報を編集できる機能を実装する。

## 要件
- 名前、メールアドレス、プロフィール画像を編集可能
- バリデーション機能
- 更新後に確認メッセージを表示

## 実装詳細
- UI: lib/features/user/pages/profile_edit_page.dart
- ロジック: lib/features/user/services/user_service.dart
```

### Issue分析

#### 1. 問題の種類を判定
- **機能追加** (enhancement): 新機能の実装
- **バグ修正** (bug): 既存機能の不具合修正
- **リファクタリング** (refactoring): コード構造の改善
- **ドキュメント** (documentation): ドキュメント更新
- **パフォーマンス** (performance): パフォーマンス改善

#### 2. 影響範囲を推定
- 変更が必要なファイル
- 影響を受ける既存機能
- 追加が必要なテスト

#### 3. 必要なファイルやコンポーネントを特定
Issue内容から以下を特定:
- 新規作成が必要なファイル
- 修正が必要な既存ファイル
- 追加が必要なテストファイル
- 更新が必要なドキュメント

## ステップ4: ブランチの作成

### 目的
Issue対応用の作業ブランチを作成する。

### 実行手順

#### 1. 現在のブランチを確認
```bash
git status
```

**確認事項**:
- 未コミットの変更がないか
- 現在のブランチ名

#### 2. mainブランチに移動して最新を取得
```bash
git checkout main
git pull origin main
```

**出力例**:
```
Already on 'main'
From https://github.com/user/repo
 * branch            main       -> FETCH_HEAD
Already up to date.
```

#### 3. Issue対応用のブランチを作成
```bash
git checkout -b feature/issue-[issue番号]
```

**ブランチ命名規則**:
- Issue対応: `feature/issue-[issue番号]`
- 例: `feature/issue-42`

**出力例**:
```
Switched to a new branch 'feature/issue-42'
```

### ブランチが既に存在する場合

**エラー**:
```
fatal: A branch named 'feature/issue-42' already exists.
```

**対処**:
1. 既存ブランチを使用するか確認
2. 新しいブランチ名を提案（例: `feature/issue-42-v2`）
3. ユーザーに選択してもらう

## ステップ5: 改修計画の立案

### 目的
Issue内容に基づいて、具体的な実装計画を作成する。

### 実装要件の整理

#### 1. 実装すべき機能や修正内容
Issue内容から以下を抽出:
- 新規追加する機能
- 修正する既存の問題
- 変更する仕様

#### 2. 影響を受けるファイル
- 新規作成ファイル
- 修正ファイル
- 削除ファイル

#### 3. 追加・修正が必要なテスト
- ユニットテスト
- 統合テスト
- E2Eテスト

#### 4. ドキュメント更新の必要性
- README更新
- API仕様書更新
- コメント追加

### 作業計画の策定

#### 開発ワークフローに基づいた作業計画

**実装手順の明確化**:
1. 必要なファイルの作成・修正
2. ロジックの実装
3. テストコードの追加
4. コード品質チェック
5. コミット・プッシュ・PR作成

**各ステップの詳細説明**:
- 実装する機能の詳細
- 使用する技術・ライブラリ
- 考慮すべき制約

**品質チェック項目の確認**:
- 型チェック
- リント
- テスト実行
- ビルド確認

### TodoWriteツールで作業計画を作成

#### Todoリストの構成例
```markdown
- [ ] Issue内容の詳細確認
- [ ] 影響範囲の特定
- [ ] ProfileEditPageの作成
- [ ] UserServiceの修正
- [ ] バリデーション機能の実装
- [ ] テストコードの追加
- [ ] コード品質チェック実行
- [ ] コミット
- [ ] プッシュとPR作成
```

#### Todoの状態管理
- `pending`: 未着手
- `in_progress`: 作業中
- `completed`: 完了

## ステップ6: ユーザーへの改修計画確認

### 目的
実装前にユーザーの承認を得て、方向性が正しいか確認する。

### 提示する情報

#### 1. 作成したブランチ名
```
📋 作成したブランチ: feature/issue-42
```

#### 2. 実装する内容の概要
```
📝 実装内容:
- ユーザープロフィール編集機能を追加
- 名前、メールアドレス、プロフィール画像の編集機能
- バリデーション機能の実装
- 更新後の確認メッセージ表示
```

#### 3. 予想される作業時間
```
⏱️ 予想作業時間: 1〜2時間
```

#### 4. Todoリストの内容
```
✅ 作業計画（9タスク）:
1. Issue内容の詳細確認
2. 影響範囲の特定
3. ProfileEditPageの作成
4. UserServiceの修正
5. バリデーション機能の実装
6. テストコードの追加
7. コード品質チェック実行
8. コミット
9. プッシュとPR作成
```

### ユーザーの承認待ち

**承認キーワード**:
- 「問題なし」
- 「作業開始」
- 「続行」
- 「OK」

**修正依頼の場合**:
- 具体的な修正内容を確認
- 計画を調整して再提示

**中止の場合**:
- 「中止」「キャンセル」「停止」
- 作業を終了

## ステップ7: 実装の実行

### 目的
改修計画に従って実装を行う。

### 実装プロセス

#### 1. 改修計画に従って実装を開始
- TodoリストのタスクTo順次実行
- 各タスク開始時に状態を`in_progress`に更新

#### 2. 各タスクを進める際にTodoリストを更新
```
Todoの更新例:
- [x] Issue内容の詳細確認（completed）
- [x] 影響範囲の特定（completed）
- [~] ProfileEditPageの作成（in_progress）
- [ ] UserServiceの修正（pending）
```

#### 3. 実装完了後、ユーザーに修正内容の確認を求める
実装が完了したら、ステップ8へ進む

## ステップ8: 修正内容の確認フェーズ

### 目的
実装内容をユーザーに確認してもらい、コミット前に修正の機会を提供する。

### 重要事項
**自動でコミットせずユーザーの確認を待つ**

### 修正内容のサマリー表示

#### 1. 変更ファイルの一覧
```bash
git status --short
git diff --stat
```

**出力例**:
```
✅ 修正完了

📝 変更ファイル:
- lib/features/user/pages/profile_edit_page.dart（新規作成、120行）
- lib/features/user/services/user_service.dart（15行追加、3行削除）
- lib/models/user.dart（新規作成、30行）
- test/user_service_test.dart（20行追加）
```

#### 2. 品質チェック結果
```
📊 品質チェック結果:
- flutter analyze: 10 issues（修正前: 15）
- エラー削減: 5件
- テスト: 全25件パス
```

#### 3. 次のステップの案内
```
次のステップ:
1. 変更内容を確認してください
2. 問題なければ「コミット」または「続行」と指示してください
3. 修正が必要な場合は具体的に指示してください
```

### ユーザーの指示を待つ

**コミット実行のキーワード**:
- 「問題なし」
- 「続行」
- 「コミット」

**修正依頼の場合**:
- 具体的な修正内容を確認
- 該当箇所を修正
- 再度ステップ8へ戻る

**中止の場合**:
- 処理を終了

## ステップ9: 変更内容のコミット

### 目的
ユーザーの承認を得て、変更内容をGitリポジトリにコミットする。

### 重要事項
**ユーザーから承認を得た後のみ実行**

### コミット手順

#### 1. 変更ファイルの最終確認
```bash
git status --short
git diff --stat
```

#### 2. コミットメッセージの生成
**Conventional Commits形式**:
```
feat: ユーザープロフィール編集機能を追加 #42

- ProfileEditPageを実装
- UserServiceに編集機能を追加
- バリデーション機能を実装
- テストコードを追加
```

**形式**:
- `feat:` - 新機能追加
- `fix:` - バグ修正
- `refactor:` - リファクタリング
- `docs:` - ドキュメント更新
- `test:` - テスト追加・修正
- `#[issue番号]` - Issue番号を含める

#### 3. コミットメッセージをユーザーに表示
```
📝 コミットメッセージ:
feat: ユーザープロフィール編集機能を追加 #42

- ProfileEditPageを実装
- UserServiceに編集機能を追加
- バリデーション機能を実装
- テストコードを追加
```

#### 4. コミットを実行
```bash
git add .
git commit -m "feat: ユーザープロフィール編集機能を追加 #42"
```

#### 5. コミット結果を報告
```
✅ コミット完了

コミットID: abc1234
メッセージ: feat: ユーザープロフィール編集機能を追加 #42

変更ファイル数: 4
追加行数: 185
削除行数: 3

次のステップ:
「PR作成」と指示するとプッシュとPR作成を実行します
```

### ユーザーの指示を待つ

**PR作成のキーワード**:
- 「PR作成」
- 「プッシュ」
- 「続行」

**その他の作業の場合**:
- スキルを終了

## ステップ10: プッシュとPR作成

### 目的
リモートリポジトリにプッシュし、プルリクエストを作成する。

### 重要事項
**ユーザーから指示を得た後のみ実行**

### 実行手順

#### 1. リモートへプッシュ
```bash
git push -u origin feature/issue-42
```

**出力例**:
```
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 8 threads
Compressing objects: 100% (10/10), done.
Writing objects: 100% (10/10), 2.5 KiB | 2.5 MiB/s, done.
Total 10 (delta 5), reused 0 (delta 0)
remote:
remote: Create a pull request for 'feature/issue-42' on GitHub by visiting:
remote:      https://github.com/user/repo/pull/new/feature/issue-42
remote:
To https://github.com/user/repo.git
 * [new branch]      feature/issue-42 -> feature/issue-42
```

#### 2. PR作成
```bash
gh pr create --title "feat: ユーザープロフィール編集機能を追加 #42" --body "..."
```

**PRタイトル**: コミットメッセージと同じ

**PR本文**:
```markdown
## 概要
ユーザープロフィール編集機能を実装しました。

## 変更点
- ProfileEditPageを実装
- UserServiceに編集機能を追加
- バリデーション機能を実装
- テストコードを追加

## テスト
- [x] ユニットテスト追加
- [x] 品質チェック実行
- [x] 動作確認完了

fixes #42
```

#### 3. 完了報告
```
✅ プルリクエスト作成完了

PR番号: #15
URL: https://github.com/user/repo/pull/15
タイトル: feat: ユーザープロフィール編集機能を追加 #42

📊 作業サマリー:
- ブランチ: feature/issue-42
- コミット: 1件
- 変更ファイル: 4件
- PR: #15

作業完了しました。
```

## TodoWriteの活用ガイド

### TodoWriteツールの目的
- 作業計画の可視化
- 進捗状況の追跡
- ユーザーへの進捗報告

### Todoリストの作成タイミング
ステップ5（改修計画の立案）で作成

### Todoの状態管理

#### 状態の種類
- `pending`: 未着手
- `in_progress`: 作業中（1つのみ）
- `completed`: 完了

#### 更新のタイミング
- タスク開始時: `pending` → `in_progress`
- タスク完了時: `in_progress` → `completed`
- 次のタスク開始時: 新しいタスクを`in_progress`に

### Todoリストの例

```typescript
[
  { content: "Issue内容の詳細確認", status: "completed", activeForm: "Issue内容の詳細確認中" },
  { content: "影響範囲の特定", status: "completed", activeForm: "影響範囲の特定中" },
  { content: "ProfileEditPageの作成", status: "in_progress", activeForm: "ProfileEditPageの作成中" },
  { content: "UserServiceの修正", status: "pending", activeForm: "UserServiceの修正中" },
  { content: "バリデーション機能の実装", status: "pending", activeForm: "バリデーション機能の実装中" },
  { content: "テストコードの追加", status: "pending", activeForm: "テストコードの追加中" },
  { content: "コード品質チェック実行", status: "pending", activeForm: "コード品質チェック実行中" },
  { content: "コミット", status: "pending", activeForm: "コミット中" },
  { content: "プッシュとPR作成", status: "pending", activeForm: "プッシュとPR作成中" }
]
```

## 開発ワークフローとの連携

### 開発ワークフローの読み込み
ステップ1で `.claude/rules/development-workflow.md` を読み込み、以下を確認:

#### 1. ブランチ命名規則
- Issue対応: `feature/issue-[issue番号]`
- 例: `feature/issue-1`, `feature/issue-123`

#### 2. コミットメッセージ形式
Conventional Commits形式:
- `feat:` - 新機能
- `fix:` - バグ修正
- `refactor:` - リファクタリング
- `docs:` - ドキュメント
- `test:` - テスト

#### 3. 作業フロー（ユーザー確認を含む）
1. ブランチ作成（スキルが実行）
2. Issue分析と改修計画立案（スキルが実行）
3. **ユーザー確認①**: 改修計画の承認
4. 実装の実行（スキルが実行）
5. コード品質チェック（スキルが実行）
6. **ユーザー確認②**: 修正内容の確認
7. コミット（ユーザー承認後に実行）
8. **ユーザー確認③**: PR作成の指示
9. プッシュ（ユーザー指示後に実行）
10. プルリクエスト作成（ユーザー指示後に実行）

### ユーザー確認フェーズの詳細

#### 確認フェーズ①: 改修計画の承認（ステップ6）
**タイミング**: 実装前

**確認内容**:
- ブランチ名
- 実装内容の概要
- 作業計画（Todoリスト）

**承認キーワード**: 「問題なし」「作業開始」「続行」「OK」

#### 確認フェーズ②: 修正内容の確認（ステップ8）
**タイミング**: 実装完了後、コミット前

**確認内容**:
- 変更ファイル一覧
- 品質チェック結果
- 修正内容のサマリー

**承認キーワード**: 「問題なし」「続行」「コミット」

#### 確認フェーズ③: PR作成の指示（ステップ9後）
**タイミング**: コミット完了後、プッシュ・PR作成前

**確認内容**:
- コミット完了報告
- 次のステップの案内

**指示キーワード**: 「PR作成」「プッシュ」「続行」

### 重要な原則
**自動で次のステップに進まない**

- 各確認フェーズで必ず停止
- ユーザーの明示的な指示を待つ
- ユーザーが「問題なし」「続行」等と指示するまで待機
