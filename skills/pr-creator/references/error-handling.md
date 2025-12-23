# エラーハンドリング詳細

## 品質チェック失敗

### 型チェックエラー
```
❌ 型チェックに失敗しました

エラー数: 3件

src/types/user.ts:15:8
  Type 'string | undefined' is not assignable to type 'string'

修正してから再実行してください。
```

### Lintエラー
```
❌ Lintチェックに失敗しました

警告数: 5件
エラー数: 2件

詳細:
- console.logが残っています (src/utils/debug.ts:10)
- 未使用のインポート (src/components/App.tsx:3)

自動修正を試しますか？
  npm run lint:fix
```

### ビルドエラー
```
❌ ビルドに失敗しました

原因: webpack compilation error
  Module not found: '@/components/NewComponent'

ファイルパスを確認してください。
```

## Git操作エラー

### コミットするファイルがない
```
⚠️ コミットする変更がありません

git statusの結果:
  On branch feature/issue-42
  nothing to commit, working tree clean

すでにコミット済みの場合は、プッシュのみ実行しますか？
```

### プッシュ失敗（コンフリクト）
```
❌ プッシュに失敗しました

原因: リモートブランチが先行しています

対処方法:
  git pull --rebase origin $(git branch --show-current)
  # コンフリクトを解決
  git push
```

## GitHub PR作成エラー

### 既にPRが存在
```
⚠️ このブランチのPRは既に存在します

既存PR: #12
URL: https://github.com/user/repo/pull/12

既存PRを更新しますか？それとも新しいコミットを追加しますか？
```

### 権限不足
```
❌ PRの作成に失敗しました

原因: 権限不足
このリポジトリへの書き込み権限がありません。

対処方法:
1. リポジトリをフォーク
2. フォーク先にプッシュ
3. 元リポジトリへPR作成
```

### GitHub認証エラー
```
❌ GitHub認証エラー

GitHub CLIが認証されていません。

対処方法:
  gh auth login
```

## トラブルシューティング

### スキルが発動しない
- 「PR作成」「プルリクエスト」などのキーワードを使用
- 例: 「growth-diaryのPR作って」

### 品質チェックが通らない
- エラー内容を確認して修正
- 自動修正可能な場合は提案を受け入れる
- 必要に応じて `npm run lint:fix` など実行

### PR作成が失敗する
- GitHub認証状態を確認: `gh auth status`
- リポジトリ権限を確認
- ブランチ名が適切か確認
