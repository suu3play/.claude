# ブランチクリーンアップ - エラーと対処法

このドキュメントは、branch-cleanerスキル実行時に発生する可能性のあるエラーとその対処法を詳しく説明します。

## プロジェクト関連エラー

### エラー: プロジェクトディレクトリが存在しない

**エラーメッセージ**:
```
❌ エラー: プロジェクト '[プロジェクト名]' が見つかりません

確認してください:
  [プロジェクトルート]/[プロジェクト名]
```

**原因**:
- 指定したプロジェクト名が間違っている
- プロジェクトルートの設定が正しくない
- プロジェクトがまだ作成されていない

**対処方法**:
1. プロジェクト名のスペルを確認
2. プロジェクトルートを確認: `ls [プロジェクトルート]`
3. 利用可能なプロジェクト一覧を表示: `ls -d [プロジェクトルート]/*`

### エラー: Gitリポジトリではない

**エラーメッセージ**:
```
❌ エラー: '[プロジェクト名]' はGitリポジトリではありません

Git初期化が必要な場合:
  cd "[プロジェクトルート]/[プロジェクト名]"
  git init
```

**原因**:
- `.git`ディレクトリが存在しない
- Gitが初期化されていない

**対処方法**:
1. Gitリポジトリであることを確認: `ls -la [プロジェクト名]/.git`
2. 必要に応じてGitを初期化:
   ```bash
   cd [プロジェクト名]
   git init
   git remote add origin [リモートURL]
   ```

## Git操作関連エラー

### エラー: リモートとの通信エラー

**エラーメッセージ**:
```
❌ エラー: リモートリポジトリに接続できません

原因: ネットワークエラーまたは認証失敗

対処方法:
1. ネットワーク接続を確認
2. 認証情報を確認: git config --list
3. リモートURLを確認: git remote -v
```

**原因**:
- ネットワーク接続の問題
- Git認証情報の期限切れ
- リモートURLが間違っている
- SSHキーまたはHTTPSトークンの問題

**対処方法**:

#### 1. ネットワーク確認
```bash
# リモートURLへの接続テスト
git ls-remote origin
```

#### 2. 認証情報確認
```bash
# 現在の設定を確認
git config --list | grep -i user
git config --list | grep -i credential

# リモートURL確認
git remote -v
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

### エラー: ブランチ削除失敗

**エラーメッセージ**:
```
❌ エラー: ブランチ 'feature/issue-1' の削除に失敗しました

原因: ブランチがmainにマージされていません

対処方法:
1. マージ状況を確認:
     git log main..feature/issue-1

2. 強制削除する場合（注意）:
     git branch -D feature/issue-1
```

**原因**:
- ブランチがmainにマージされていない
- ブランチに未マージのコミットがある
- 現在チェックアウトしているブランチを削除しようとしている

**対処方法**:

#### 1. マージ状況の確認
```bash
# mainとの差分を確認
git log main..feature/issue-1

# マージ済みブランチのリスト
git branch --merged main

# 未マージブランチのリスト
git branch --no-merged main
```

#### 2. ブランチをマージする
```bash
# mainブランチに切り替え
git checkout main

# ブランチをマージ
git merge feature/issue-1

# プッシュ
git push origin main

# ブランチを削除
git branch -d feature/issue-1
```

#### 3. 強制削除（注意）
```bash
# 未マージでも削除（コミットが失われます）
git branch -D feature/issue-1
```

**注意**: 強制削除 (`-D`) を使用すると、未マージのコミットが永久に失われます。必ず内容を確認してから実行してください。

### エラー: mainブランチの更新失敗

**エラーメッセージ**:
```
❌ エラー: mainブランチの更新に失敗しました

原因: ローカルの変更とコンフリクト

対処方法:
  git stash
  git pull origin main
  git stash pop
```

**原因**:
- mainブランチに未コミットの変更がある
- リモートの変更とコンフリクトしている
- diverged状態（ローカルとリモートの履歴が分岐）

**対処方法**:

#### 1. 未コミット変更がある場合
```bash
# 変更を一時保存
git stash

# mainを更新
git pull origin main

# 変更を復元
git stash pop
```

#### 2. コンフリクトがある場合
```bash
# 現在の状態を確認
git status

# コンフリクトファイルを編集して解決
# エディタでコンフリクトマーカーを削除

# 解決後にコミット
git add .
git commit -m "Merge conflict resolved"
```

#### 3. diverged状態の場合
```bash
# ローカルの履歴を確認
git log origin/main..main

# リモートに強制的に合わせる（ローカルの変更は失われます）
git reset --hard origin/main

# またはリベース
git pull --rebase origin main
```

## 安全性チェック関連

### 警告: 未コミット変更あり

**警告メッセージ**:
```
⚠️ スキップ: growth-diary

理由: 未コミットの変更があります

変更されたファイル:
  M  src/components/UserProfile.tsx
  ?? src/components/NewComponent.tsx

対処方法:
  git add .
  git commit -m "変更をコミット"
```

**原因**:
- ワーキングツリーに未コミットの変更がある
- 新しいファイルが追跡されていない

**対処方法**:

#### 1. 変更をコミット
```bash
# すべての変更をステージング
git add .

# コミット
git commit -m "作業中の変更を保存"

# プッシュ
git push origin [ブランチ名]
```

#### 2. 変更を一時保存
```bash
# スタッシュに保存
git stash save "作業中の変更"

# ブランチクリーンアップ実行後に復元
git stash pop
```

#### 3. 変更を破棄
```bash
# すべての変更を破棄（注意）
git reset --hard HEAD

# 未追跡ファイルを削除（注意）
git clean -fd
```

### 警告: 未プッシュコミットあり

**警告メッセージ**:
```
⚠️ スキップ: portfolio

理由: プッシュされていないコミットがあります

未プッシュコミット (2件):
  abc1234 feat: 新機能追加
  def5678 fix: バグ修正

対処方法:
  git push origin [ブランチ名]
```

**原因**:
- ローカルにコミットがあるがリモートにプッシュされていない
- ブランチがリモートに存在しない

**対処方法**:

#### 1. プッシュする
```bash
# 現在のブランチをプッシュ
git push origin [ブランチ名]

# または-uオプションで追跡ブランチを設定
git push -u origin [ブランチ名]
```

#### 2. プッシュが不要な場合
```bash
# コミットを確認
git log origin/main..HEAD

# コミットをリセット（注意）
git reset --soft origin/main
```

### 警告: 未マージブランチ

**警告メッセージ**:
```
⚠️ 未マージブランチ: feature/wip

このブランチはmainにマージされていません。
削除する場合は強制削除が必要です:
  git branch -D feature/wip

保持しますか？ [Y/n]:
```

**原因**:
- ブランチがmainにマージされていない
- 作業中のブランチ

**対処方法**:

#### 1. ブランチを保持
- プロンプトで「Y」を選択
- ブランチは削除されず保護される

#### 2. ブランチをマージしてから削除
```bash
# mainに切り替え
git checkout main

# ブランチをマージ
git merge feature/wip

# プッシュ
git push origin main

# 再度クリーンアップ実行
```

#### 3. 強制削除
```bash
# 未マージでも削除（コミットが失われます）
git branch -D feature/wip
```

## 全プロジェクトモード固有のエラー

### 警告: 一部プロジェクトでエラー

**警告メッセージ**:
```
⚠️ 一部のプロジェクトで処理をスキップしました

スキップされたプロジェクト (2件):
- source-flow: 未コミット変更あり
- legacy-app: リモート接続エラー

正常処理: 6/8 プロジェクト
```

**原因**:
- 各プロジェクトで個別のエラーが発生

**対処方法**:
1. エラーログを確認
2. 各プロジェクトで個別に対処
3. 再度全プロジェクトモードを実行

### タイムアウト

**エラーメッセージ**:
```
❌ エラー: タイムアウトしました

プロジェクト数が多いため処理に時間がかかっています。
```

**対処方法**:
1. プロジェクトを分けて処理
2. `skipProjects`設定で不要なプロジェクトを除外
3. ネットワーク接続を確認

## デバッグ方法

### 詳細ログの有効化

設定ファイルでログを有効化:

```json
{
  "logResults": true,
  "logPath": "./logs/branch_cleanup.log"
}
```

### 手動でのGit状態確認

```bash
# ブランチ一覧
git branch -v

# マージ状況
git branch --merged main
git branch --no-merged main

# リモート追跡状況
git branch -vv

# 未プッシュコミット
git log --branches --not --remotes --oneline

# ワーキングツリーの状態
git status
```

### よくある問題と解決策

#### 問題: スキルが発動しない
**解決策**: 「ブランチ整理」「クリーンアップ」などのキーワードを使用

#### 問題: ブランチが削除されない
**解決策**: マージ状況を確認し、必要に応じて手動でマージまたは削除

#### 問題: 全プロジェクトモードが遅い
**解決策**:
- プロジェクト数が多い場合は単一モードを使用
- 設定ファイルでスキップ対象を指定
