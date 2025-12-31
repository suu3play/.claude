# Issue Fixer - エラーハンドリングとトラブルシューティング

このドキュメントは、issue-fixerスキル実行時に発生する可能性のあるエラーとその対処法を説明します。

## プロジェクト関連エラー

### エラー: プロジェクトディレクトリが存在しない

**エラーメッセージ**:
```
エラー: プロジェクト '[プロジェクト名]' が見つかりません。
プロジェクトルート配下に存在するプロジェクトを確認してください。
```

**原因**:
- 指定したプロジェクト名が間違っている
- プロジェクトルートの設定が正しくない
- プロジェクトがまだ作成されていない

**対処方法**:

#### 1. プロジェクト名のスペルを確認
```bash
# プロジェクトルート配下のディレクトリ一覧を表示
ls [プロジェクトルート]
```

#### 2. 利用可能なプロジェクトを確認
```bash
# Gitリポジトリを持つディレクトリのみ表示
find [プロジェクトルート] -maxdepth 1 -type d -name ".git" -exec dirname {} \;
```

#### 3. プロジェクトルートの設定を確認
- `.claude/CLAUDE.md` でプロジェクトルートが正しく設定されているか確認
- 環境変数が正しく設定されているか確認

### エラー: Gitリポジトリではない

**エラーメッセージ**:
```
エラー: 指定されたディレクトリはGitリポジトリではありません。
git init を実行するか、正しいプロジェクトディレクトリを指定してください。
```

**原因**:
- `.git`ディレクトリが存在しない
- Gitが初期化されていない

**対処方法**:

#### 1. Gitリポジトリであることを確認
```bash
cd [プロジェクトディレクトリ]
git rev-parse --git-dir
```

**成功時の出力**:
```
.git
```

#### 2. Gitリポジトリでない場合
**新規プロジェクトの場合**:
```bash
cd [プロジェクトディレクトリ]
git init
git remote add origin [リモートURL]
```

**既存プロジェクトの場合**:
```bash
# 既存のリモートリポジトリをクローン
git clone [リモートURL] [プロジェクト名]
```

## GitHub Issue関連エラー

### エラー: GitHub Issueが存在しない

**エラーメッセージ**:
```
エラー: Issue #[issue番号] が見つかりません。
正しいIssue番号か確認してください。
```

**原因**:
- Issue番号が間違っている
- Issueが削除されている
- リポジトリへのアクセス権限がない

**対処方法**:

#### 1. Issue番号を確認
```bash
# 開いているIssueの一覧を表示
gh issue list --state open

# すべてのIssueを表示（閉じたIssueも含む）
gh issue list --state all
```

#### 2. Issueが存在するか確認
```bash
# 特定のIssueを表示
gh issue view [issue番号]
```

#### 3. リポジトリのアクセス権限を確認
```bash
# 現在認証されているユーザーを確認
gh auth status

# リモートURLを確認
git remote -v
```

### エラー: GitHub CLI認証エラー

**エラーメッセージ**:
```
エラー: GitHub CLIで認証されていません。
gh auth login を実行してください。
```

**原因**:
- GitHub CLIで認証されていない
- 認証トークンが期限切れ

**対処方法**:

#### 1. 認証状態を確認
```bash
gh auth status
```

#### 2. 認証を実行
```bash
gh auth login
```

**対話式プロンプト**:
```
? What account do you want to log into? GitHub.com
? What is your preferred protocol for Git operations? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser
```

#### 3. 認証後の確認
```bash
gh auth status
```

**成功時の出力**:
```
✓ Logged in to github.com as [username]
✓ Git operations for https://github.com configured to use https protocol.
✓ Token: *******************
```

## Git操作関連エラー

### エラー: ブランチが既に存在する

**エラーメッセージ**:
```
警告: ブランチ 'feature/issue-[issue番号]' は既に存在します。
既存のブランチを使用しますか？それとも新しいブランチ名を指定しますか？
```

**原因**:
- 同じIssue番号でブランチが既に作成されている
- 以前の作業が残っている

**対処方法**:

#### 1. 既存ブランチの状態を確認
```bash
# ブランチ一覧を表示
git branch -v

# 特定のブランチに切り替え
git checkout feature/issue-[issue番号]

# ブランチの状態を確認
git status
git log --oneline -5
```

#### 2. 選択肢の提示

**選択肢A: 既存のブランチを使用**
```bash
git checkout feature/issue-[issue番号]
```

**選択肢B: 新しいブランチ名を使用**
```bash
# 新しいブランチ名を提案
git checkout -b feature/issue-[issue番号]-v2
# または
git checkout -b feature/issue-[issue番号]-[日付]
```

**選択肢C: 既存ブランチを削除して作り直す**
```bash
# ローカルブランチを削除
git branch -D feature/issue-[issue番号]

# リモートブランチも削除する場合
git push origin --delete feature/issue-[issue番号]

# 新しくブランチを作成
git checkout -b feature/issue-[issue番号]
```

### エラー: 未コミットの変更がある

**エラーメッセージ**:
```
エラー: ワーキングツリーに未コミットの変更があります。
先にコミットまたはスタッシュしてください。
```

**原因**:
- 現在のブランチに未保存の変更がある
- ブランチ切り替え前に変更をコミットする必要がある

**対処方法**:

#### 1. 未コミットの変更を確認
```bash
git status
git diff
```

#### 2. 選択肢の提示

**選択肢A: 変更をコミット**
```bash
git add .
git commit -m "作業中の変更を保存"
```

**選択肢B: 変更をスタッシュ**
```bash
# 一時保存
git stash save "Issue対応前の作業"

# ブランチ作業後に復元
git stash pop
```

**選択肢C: 変更を破棄（注意）**
```bash
# すべての変更を破棄
git reset --hard HEAD

# 未追跡ファイルも削除
git clean -fd
```

### エラー: リモートとの通信エラー

**エラーメッセージ**:
```
エラー: リモートリポジトリに接続できません。
ネットワーク接続を確認してください。
```

**原因**:
- ネットワーク接続の問題
- Git認証情報の期限切れ
- リモートURLが間違っている

**対処方法**:

#### 1. ネットワーク接続を確認
```bash
# リモートURLへの接続テスト
git ls-remote origin
```

#### 2. リモートURL を確認
```bash
git remote -v
```

**出力例**:
```
origin  https://github.com/user/repo.git (fetch)
origin  https://github.com/user/repo.git (push)
```

#### 3. HTTPS認証の再設定
```bash
# 認証情報をクリア
git config --unset credential.helper

# 再度プル（認証情報を入力）
git pull origin main
```

#### 4. SSH認証の確認
```bash
# SSH接続テスト
ssh -T git@github.com

# SSH鍵の確認
ls -la ~/.ssh/
```

## コミット関連エラー

### エラー: コミットメッセージが空

**エラーメッセージ**:
```
エラー: コミットメッセージが空です。
有効なコミットメッセージを指定してください。
```

**原因**:
- コミットメッセージが生成されなかった
- メッセージが空文字列

**対処方法**:

#### 1. Issueタイトルからメッセージを生成
```bash
# Issueタイトルを取得
gh issue view [issue番号] --json title --jq .title

# コミットメッセージを生成
feat: [Issueタイトル] #[issue番号]
```

#### 2. デフォルトメッセージを使用
```bash
git commit -m "feat: Issue #[issue番号]の対応"
```

### エラー: プッシュ時のコンフリクト

**エラーメッセージ**:
```
エラー: リモートブランチとコンフリクトしています。
先にプルしてマージしてください。
```

**原因**:
- リモートブランチが更新されている
- ローカルとリモートの履歴が分岐している

**対処方法**:

#### 1. リモートの変更を取得
```bash
git fetch origin
```

#### 2. リモートの変更をマージ
```bash
# リモートの変更をマージ
git pull origin feature/issue-[issue番号]

# コンフリクトがある場合は解決
# エディタでコンフリクトマーカーを削除

# 解決後にコミット
git add .
git commit -m "Merge remote changes"
```

#### 3. 再度プッシュ
```bash
git push origin feature/issue-[issue番号]
```

## PR作成関連エラー

### エラー: PR作成に失敗

**エラーメッセージ**:
```
エラー: プルリクエストの作成に失敗しました。
リポジトリへの書き込み権限を確認してください。
```

**原因**:
- リポジトリへの書き込み権限がない
- 同じブランチでPRが既に存在する
- GitHub APIのレート制限

**対処方法**:

#### 1. 権限を確認
```bash
# リポジトリの権限を確認
gh api repos/[owner]/[repo] --jq .permissions
```

#### 2. 既存のPRを確認
```bash
# ブランチのPRを検索
gh pr list --head feature/issue-[issue番号]
```

#### 3. 既存のPRがある場合
```bash
# 既存のPRを表示
gh pr view [PR番号]

# 必要に応じて既存のPRを更新
git push origin feature/issue-[issue番号]
```

## 一般的なトラブルシューティング

### スキルが起動しない

**原因**:
- キーワードが認識されていない
- 他のスキルが優先されている

**対処方法**:

#### 1. 明示的なキーワードを使用
```
✓ 「issue 8 を改修して」
✓ 「growth-diary の issue 8 を対応して」
✓ 「issueから改修して」

✗ 「これを修正して」（曖昧）
✗ 「タスクを処理して」（キーワードなし）
```

#### 2. スキル名を明示
```
issue-fixerスキルを使って issue 8 を改修して
```

### 実装が自動で進んでしまう

**原因**:
- ユーザー確認フェーズが適切に実装されていない
- 自動実行が有効になっている

**対処方法**:

#### 1. 各確認フェーズで停止することを確認
- 改修計画提示後
- 実装完了後
- コミット完了後

#### 2. ユーザーに明示的に承認を求める
```
問題なければ「続行」と指示してください。
```

### Todoリストが更新されない

**原因**:
- TodoWriteツールが正しく使用されていない
- 状態の更新タイミングが間違っている

**対処方法**:

#### 1. Todoリストの作成を確認
ステップ5（改修計画の立案）でTodoWriteを使用

#### 2. 状態の更新タイミング
- タスク開始時: `pending` → `in_progress`
- タスク完了時: `in_progress` → `completed`

#### 3. 1つのタスクのみ`in_progress`に
同時に複数のタスクが`in_progress`にならないよう注意

### コード品質チェックが実行されない

**原因**:
- 品質チェックタスクがTodoリストに含まれていない
- 実装フローに組み込まれていない

**対処方法**:

#### 1. Todoリストに品質チェックを含める
```
- [ ] コード品質チェック実行
```

#### 2. ステップ8（修正内容の確認）で実行
実装完了後、コミット前に品質チェックを実行

#### 3. 品質チェック結果を報告
```
📊 品質チェック結果:
- flutter analyze: 10 issues（修正前: 15）
- エラー削減: 5件
- テスト: 全25件パス
```

## デバッグのヒント

### ログの確認

#### 1. Git操作のログ
```bash
# コミット履歴
git log --oneline -10

# ブランチ操作履歴
git reflog
```

#### 2. GitHub CLI のログ
```bash
# デバッグモードで実行
GH_DEBUG=1 gh issue view [issue番号]
```

### 手動での確認方法

#### 1. ブランチ状態の確認
```bash
git status
git branch -v
git log --oneline -5
```

#### 2. Issue情報の確認
```bash
gh issue view [issue番号]
gh issue view [issue番号] --json title,body,labels
```

#### 3. プロジェクト情報の確認
```bash
pwd
ls -la
git remote -v
```

## よくある質問

### Q: Issue番号を間違えた場合はどうすれば良いですか？

**A**: スキルを中止して、正しいIssue番号で再実行してください。

```
1. 「中止」と指示
2. 正しいIssue番号で再度実行
   「issue [正しい番号] を改修して」
```

### Q: 実装途中で中断したい場合は？

**A**: 各確認フェーズで中止を指示できます。

```
- 改修計画確認時: 「中止」
- 修正内容確認時: 「中止」
- コミット後: 「中止」（コミットは残ります）
```

中断後、作業を再開するには:
```bash
# ブランチに切り替え
git checkout feature/issue-[issue番号]

# 作業を続行
```

### Q: 複数のIssueを同時に処理できますか？

**A**: スキルは1つのIssueに対して1つのブランチを作成します。

複数Issueを処理する場合:
```
1. Issue A を完了（PR作成まで）
2. mainブランチに戻る
3. Issue B を開始
```

### Q: 自動テスト生成はサポートされていますか？

**A**: 現在のバージョンでは手動でテストを追加する必要があります。

将来的な拡張機能として検討されています。
