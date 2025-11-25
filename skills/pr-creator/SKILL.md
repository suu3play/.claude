---
name: pr-creator
description: ユーザーの明示的な指示がある場合のみ、コード品質チェック（型チェック、Lint、ビルド）を実行し、すべて成功した後にコミット・プッシュ・プルリクエストを作成するスキル。「PRを作成して」「プルリクエスト作って」「PR出して」などの明示的な指示でのみ起動。開発ワークフローに従って品質保証済みのPRを作成
---

# PR Creator - プルリクエスト作成スキル

このスキルは、ユーザーの明示的な指示がある場合のみ、厳格なコード品質チェックを実行し、すべて成功した後にコミット・プッシュ・プルリクエストを作成します。

## 重要な原則

**プルリクエストは勝手に作成しない**

- このスキルは、ユーザーが「PR作成」などと明示的に指示した場合のみ実行されます
- Issue対応やコード修正などの作業完了時に、自動的にPR作成することはありません
- 他のスキル（issue-fixerなど）からの自動呼び出しも禁止します

## 使用タイミング

### 明示的な指示（スキル起動）

以下のキーワードが含まれる場合のみ、このスキルを起動:

**日本語**:
- 「PRを作成して」
- 「プルリクエスト作って」
- 「PR出して」
- 「プルリク作成して」
- 「変更をプッシュしてPR作成して」
- 「MR作成して」
- 「マージリクエスト作成して」

**英語**:
- "create PR"
- "create pull request"
- "make PR"
- "create MR"
- "create merge request"

### スキルを起動しないケース

以下の場合は、このスキルを起動しません:
- 「Issue対応して」→ issue-fixerスキルが起動するが、PR作成はしない
- 「バグ修正して」→ コード修正のみ、PR作成はしない
- 「機能追加して」→ コード修正のみ、PR作成はしない
- 「テスト実行して」→ テストのみ、PR作成はしない

## 主な機能

- **厳格なコード品質チェック**: 型チェック、Lint、ビルド、テストを実行
- **バージョン番号管理**: プロジェクトのバージョンが未更新の場合、セマンティックバージョニングに基づいて更新を提案
  - Node.js/npm: package.json
  - C#/.NET: .csprojファイル (Version, AssemblyVersion, FileVersion)
  - プロジェクトタイプの自動検出
- **自動コミット・プッシュ**: Conventional Commits形式でコミットし、リモートにプッシュ
- **プルリクエスト自動作成**: テンプレートに従ったPRを自動生成
- **包括的なエラーハンドリング**: 各ステップで適切なエラー処理と対処方法を提示

## 実行フロー

### ステップ0: ユーザー指示の確認（最重要）

**このステップは必ず最初に実行する必須チェックです**

1. **明示的な指示の確認**

   ユーザーの入力に以下のキーワードが含まれているかチェック:

   **日本語キーワード**:
   - "PR作成"
   - "プルリクエスト"
   - "プルリク作成"
   - "PR出して"
   - "MR作成"
   - "マージリクエスト"

   **英語キーワード**:
   - "create PR"
   - "create pull request"
   - "make PR"
   - "create MR"
   - "create merge request"

2. **判定結果による処理**

   **✅ 明示的な指示がある場合**:
   ```
   ✓ ユーザーの明示的な指示を確認しました
   → PR作成処理を開始します
   ```
   → ステップ1へ進む

   **❌ 明示的な指示がない場合**:
   ```
   ⚠️ このスキルは明示的な指示でのみ実行されます

   プルリクエストを作成するには、以下のように指示してください:
   - 「PR作成して」
   - 「プルリクエスト作成して」
   - 「PR出して」

   現在の作業内容:
   - コード修正
   - テスト実行
   - ビルド実行
   - コミット作成
   - リモートにプッシュ

   は他のスキル（issue-fixerなど）で実行できます。
   作業完了後に「PR作成して」と指示すれば、このスキルでPRを作成できます。
   ```
   → スキル実行を終了

3. **緊急対応の場合**

   ユーザーの入力に以下のキーワードが含まれる場合、簡易確認:
   - "緊急"
   - "クリティカル"
   - "本番"
   - "hotfix"
   - "urgent"
   - "critical"

   ```
   ⚠️ 緊急対応を検出しました

   すぐにPR作成を実行しますか？
   1. はい - すぐに実行
   2. いいえ - キャンセル
   ```

   → ユーザーが「はい」を選択した場合のみステップ1へ進む

### ステップ1: 開発ワークフローとテンプレートの読み込み

1. **開発ワークフロー読み込み**
   - `.claude/rules/development-workflow.md`

2. **関連ルール・テンプレート読み込み**
   - `.claude/rules/code-quality-standards.md` - コード品質基準
   - `.claude/templates/pull-request-template.md` - PRテンプレート
   - `.claude/templates/code-quality-check-template.md` - 品質チェックテンプレート

### ステップ2: プロジェクト情報の確認

1. **プロジェクト名の特定**
   - ユーザーの指示から抽出
   - 指定がない場合はカレントディレクトリから判定

2. **プロジェクトディレクトリへ移動**
   ```bash
   cd "[プロジェクトルート]/[プロジェクト名]"
   ```

3. **Git状況の確認**
   ```bash
   git status
   ```

   - 変更されたファイルの一覧
   - 現在のブランチ
   - コミットされていない変更の有無

4. **ブランチ情報の取得**
   ```bash
   # 現在のブランチ名
   git branch --show-current

   # mainブランチとの差分確認
   git log main..HEAD --oneline
   ```

### ステップ3: 厳格なコード品質チェック

プロジェクトタイプに応じて以下のチェックを順次実行:

#### TypeScript/Node.jsプロジェクト

```bash
# 1. 型チェック
npx tsc --noEmit
echo "✅ 型チェック: 成功"

# 2. Lint
npm run lint
echo "✅ Lint: 成功"

# 3. ビルド
npm run build
echo "✅ ビルド: 成功"

# 4. テスト（存在する場合）
npm test
echo "✅ テスト: 成功"
```

#### Python プロジェクト

```bash
# 1. 型チェック
mypy .
echo "✅ 型チェック: 成功"

# 2. Lint
ruff check .
pylint **/*.py
echo "✅ Lint: 成功"

# 3. フォーマットチェック
black --check .
echo "✅ フォーマット: 成功"

# 4. テスト
pytest
echo "✅ テスト: 成功"
```

#### Flutter/Dart プロジェクト

```bash
# 1. 解析
flutter analyze
echo "✅ 解析: 成功"

# 2. フォーマットチェック
dart format --set-exit-if-changed .
echo "✅ フォーマット: 成功"

# 3. テスト
flutter test
echo "✅ テスト: 成功"

# 4. ビルド
flutter build apk --debug
echo "✅ ビルド: 成功"
```

#### Rust プロジェクト

```bash
# 1. チェック
cargo check
echo "✅ チェック: 成功"

# 2. Clippy
cargo clippy -- -D warnings
echo "✅ Clippy: 成功"

# 3. フォーマットチェック
cargo fmt --check
echo "✅ フォーマット: 成功"

# 4. テスト
cargo test
echo "✅ テスト: 成功"

# 5. ビルド
cargo build
echo "✅ ビルド: 成功"
```

**重要**: いずれかのチェックが失敗した場合は即座に停止し、エラー内容をユーザーに報告します。

### ステップ4: 品質チェック結果のログ出力

すべてのチェックが成功した場合、結果を記録:

```bash
# ログディレクトリ作成
mkdir -p ./logs

# 結果をMarkdownファイルに出力
cat > ./logs/code_check_$(date +%Y%m%d%H%M).md << 'EOF'
# コード品質チェック結果

実行日時: $(date '+%Y-%m-%d %H:%M:%S')
プロジェクト: [プロジェクト名]
ブランチ: $(git branch --show-current)

## チェック結果

### ✅ 型チェック
- ツール: tsc --noEmit
- 結果: 成功
- エラー数: 0

### ✅ Lint
- ツール: eslint
- 結果: 成功
- 警告数: 0

### ✅ ビルド
- ツール: npm run build
- 結果: 成功
- ビルド時間: 2.3秒

### ✅ テスト
- ツール: npm test
- 結果: 成功
- テストケース: 45件 (全て合格)

## 結論
すべてのチェックが成功しました。
PR作成の準備が完了しています。
EOF
```

### ステップ5: バージョン番号のチェックと更新

**プロジェクトタイプの自動検出**:
```bash
# バージョン管理ファイルを検出
if [ -f package.json ]; then
  PROJECT_TYPE="npm"
  VERSION_FILE="package.json"
elif [ -n "$(find . -maxdepth 2 -name "*.csproj" | head -n 1)" ]; then
  PROJECT_TYPE="csharp"
  VERSION_FILE=$(find . -maxdepth 2 -name "*.csproj" | head -n 1)
else
  echo "⚠️ バージョン管理ファイルが見つかりません。バージョンチェックをスキップします。"
  PROJECT_TYPE="none"
fi
```

#### Node.js/npm プロジェクト (package.json)

1. **package.jsonの存在確認**
   ```bash
   # package.jsonが存在するか確認
   if [ -f package.json ]; then
     echo "✓ package.jsonが見つかりました"
   fi
   ```

2. **現在のバージョン番号を取得**
   ```bash
   # 現在のバージョン
   CURRENT_VERSION=$(node -p "require('./package.json').version")
   echo "現在のバージョン: $CURRENT_VERSION"
   ```

3. **最新コミットのバージョンと比較**
   ```bash
   # mainブランチ（またはベースブランチ）の最新バージョン
   git show main:package.json > /tmp/package.json.main
   MAIN_VERSION=$(node -p "require('/tmp/package.json.main').version")
   echo "mainブランチのバージョン: $MAIN_VERSION"
   ```

#### C#/.NET プロジェクト (.csproj)

1. **.csprojファイルの検出**
   ```bash
   # .csprojファイルを検索
   CSPROJ_FILE=$(find . -maxdepth 2 -name "*.csproj" | head -n 1)
   if [ -n "$CSPROJ_FILE" ]; then
     echo "✓ .csprojファイルが見つかりました: $CSPROJ_FILE"
   fi
   ```

2. **現在のバージョン番号を取得**
   ```bash
   # XMLから<Version>タグを抽出
   CURRENT_VERSION=$(grep -oP '<Version>\K[^<]+' "$CSPROJ_FILE")
   echo "現在のバージョン: $CURRENT_VERSION"
   ```

3. **mainブランチのバージョンと比較**
   ```bash
   # mainブランチの.csprojファイルからバージョンを取得
   MAIN_VERSION=$(git show "main:$CSPROJ_FILE" | grep -oP '<Version>\K[^<]+')
   echo "mainブランチのバージョン: $MAIN_VERSION"
   ```

4. **バージョン更新が必要か判定**

   バージョンが同じ場合、ユーザーに提案:
   ```
   ⚠️ バージョン番号が更新されていません

   現在のバージョン: 2.0.0
   mainブランチ: 2.0.0

   変更内容に応じてバージョンを更新することを推奨します。

   セマンティックバージョニング:
   - MAJOR (X.0.0): 破壊的変更
   - MINOR (0.X.0): 新機能追加（後方互換性あり）
   - PATCH (0.0.X): バグ修正

   どのバージョンを上げますか？
   1. major (破壊的変更) → 3.0.0
   2. minor (新機能) → 2.1.0
   3. patch (バグ修正) → 2.0.1
   4. スキップ（バージョンを上げない）
   ```

5. **ユーザーの選択に基づいてバージョン更新**

   **Node.js/npm プロジェクト**:
   ```bash
   # ユーザーが選択した場合
   npm version [major|minor|patch] --no-git-tag-version

   # 更新されたバージョンを確認
   NEW_VERSION=$(node -p "require('./package.json').version")
   echo "✅ バージョンを更新しました: $CURRENT_VERSION → $NEW_VERSION"
   ```

   **C#/.NET プロジェクト**:
   ```bash
   # バージョンを計算（例: 2.0.0 → 2.1.0）
   IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"
   case "$VERSION_TYPE" in
     major) NEW_VERSION="$((major + 1)).0.0" ;;
     minor) NEW_VERSION="$major.$((minor + 1)).0" ;;
     patch) NEW_VERSION="$major.$minor.$((patch + 1))" ;;
   esac

   # .csprojファイルのバージョンを更新
   sed -i "s|<Version>$CURRENT_VERSION</Version>|<Version>$NEW_VERSION</Version>|" "$CSPROJ_FILE"

   # AssemblyVersionも更新（存在する場合）
   sed -i "s|<AssemblyVersion>$CURRENT_VERSION</AssemblyVersion>|<AssemblyVersion>$NEW_VERSION</AssemblyVersion>|" "$CSPROJ_FILE"
   sed -i "s|<FileVersion>$CURRENT_VERSION</FileVersion>|<FileVersion>$NEW_VERSION</FileVersion>|" "$CSPROJ_FILE"

   echo "✅ バージョンを更新しました: $CURRENT_VERSION → $NEW_VERSION"
   echo "   更新ファイル: $CSPROJ_FILE"
   ```

6. **バージョン更新の判断基準**

   コミットメッセージのプレフィックスから推測:
   - `feat:` → MINOR バージョンアップを提案
   - `fix:` → PATCH バージョンアップを提案
   - `BREAKING CHANGE` または `!` → MAJOR バージョンアップを提案
   - `docs:`, `chore:`, `refactor:`, `test:` → バージョンアップ不要の可能性

### ステップ6: 変更内容の確認とコミット

1. **変更ファイルの整理**
   ```bash
   # 変更されたファイル一覧
   git status --short

   # 差分確認（主要な変更）
   git diff --stat
   ```

2. **変更内容の分析**
   - 追加されたファイル
   - 修正されたファイル
   - 削除されたファイル
   - 変更行数

3. **コミットメッセージの生成**

   Conventional Commits形式で作成:
   - `feat:` - 新機能追加
   - `fix:` - バグ修正
   - `docs:` - ドキュメント更新
   - `refactor:` - リファクタリング
   - `test:` - テスト追加・修正
   - `chore:` - ビルド・設定変更

   **Issue対応の場合**:
   ```
   feat: ユーザープロフィール編集機能を追加 #42

   - プロフィール編集フォームを実装
   - バリデーション処理を追加
   - ユーザー更新APIを実装
   ```

4. **ステージングとコミット**
   ```bash
   # すべての変更をステージング
   git add .

   # コミット
   git commit -m "$(cat <<'EOF'
   feat: ユーザープロフィール編集機能を追加 #42

   - プロフィール編集フォームを実装
   - バリデーション処理を追加
   - ユーザー更新APIを実装
   EOF
   )"
   ```

### ステップ7: リモートへプッシュ

```bash
# カレントブランチをリモートにプッシュ
git push -u origin $(git branch --show-current)
```

プッシュ時のエラーハンドリング:
- コンフリクト検出 → ユーザーに解決を依頼
- 権限エラー → 認証情報の確認を依頼
- ネットワークエラー → 再試行を提案

### ステップ8: プルリクエストの作成

1. **PR内容の構成**

   Issue番号から情報を取得（Issue対応の場合）:
   ```bash
   # Issue情報取得
   gh issue view [issue番号]
   ```

2. **PRタイトルとボディの生成**

   **タイトル**:
   ```
   feat: ユーザープロフィール編集機能を追加 #42
   ```

   **ボディ** (テンプレートに従う):
   ```markdown
   ## 概要
   ユーザーがプロフィール情報を編集できる機能を実装しました。

   ## 変更内容
   - プロフィール編集フォームの実装
     - 名前、メールアドレス、自己紹介の編集機能
     - リアルタイムバリデーション
   - バックエンドAPI実装
     - PUT /api/users/:id エンドポイント
     - 認証・認可処理
   - テストコードの追加
     - コンポーネントテスト: ProfileEditForm
     - APIテスト: updateUser

   ## テスト
   - [x] 型チェック成功
   - [x] Lint成功
   - [x] ビルド成功
   - [x] 単体テスト成功 (45/45件)
   - [x] 手動テスト完了

   ## スクリーンショット
   （任意: 画像があれば追加）

   ## 影響範囲
   - `/profile/edit` ページの追加
   - `UserService.ts` の更新
   - `ProfileEditForm.tsx` の新規作成

   ## 備考
   - Issue #42 の要件をすべて満たしています
   - 既存機能への影響はありません

   fixes #42
   ```

3. **PR作成コマンド実行**
   ```bash
   gh pr create \
     --title "feat: ユーザープロフィール編集機能を追加 #42" \
     --body "$(cat pr_body.md)" \
     --base main \
     --head $(git branch --show-current)
   ```

4. **PR作成結果の取得**
   ```bash
   # 作成されたPRのURLを取得
   PR_URL=$(gh pr view --json url -q .url)
   echo "✅ プルリクエストを作成しました: $PR_URL"
   ```

### ステップ9: 結果報告とTodo更新

1. **作成結果のサマリー表示**
   ```
   ✅ プルリクエスト作成完了

   📋 詳細:
   - プロジェクト: growth-diary
   - ブランチ: feature/issue-42
   - コミット: feat: ユーザープロフィール編集機能を追加 #42
   - PR番号: #15
   - PR URL: https://github.com/user/growth-diary/pull/15

   📊 品質チェック結果:
   - ✅ 型チェック: 成功
   - ✅ Lint: 成功
   - ✅ ビルド: 成功
   - ✅ テスト: 45/45件合格

   📝 次のステップ:
   1. PRのレビューを待つ
   2. レビューコメントに対応
   3. マージ後にブランチを削除
   ```

2. **TodoWriteで作業完了をマーク**
   - 「PRを作成」タスクを完了
   - 「レビュー待ち」タスクを追加（オプション）

## 使用例

### 例1: シンプルなPR作成

**ユーザー**: growth-diary の PR作成して

**スキルの動作**:
1. growth-diaryディレクトリに移動
2. 開発ワークフローとテンプレート読み込み
3. git statusで変更確認
4. flutter analyzeなど品質チェック実行
5. すべて成功
6. package.jsonのバージョン確認
   - mainブランチと同じバージョンの場合、更新を提案
   - ユーザーが選択（major/minor/patch/スキップ）
7. コミット
8. プッシュ
9. PR作成
10. PR URLを報告

### 例2: カレントディレクトリで実行

**ユーザー**: PRを作成して

**スキルの動作**:
1. カレントディレクトリから自動判定
2. 以降は例1と同じフロー

### 例3: バージョン番号更新を伴うPR作成

**ユーザー**: clilog-viewerのPR作成して

**スキルの動作**:
1. clilog-viewerディレクトリに移動
2. 品質チェック実行 → すべて成功
3. package.jsonのバージョンチェック
   ```
   ⚠️ バージョン番号が更新されていません

   現在のバージョン: 2.0.0
   mainブランチ: 2.0.0

   コミットメッセージ: feat: CI/CDパイプラインの構築 #54
   推奨: MINOR バージョンアップ (新機能追加)

   どのバージョンを上げますか？
   1. major (破壊的変更) → 3.0.0
   2. minor (新機能) → 2.1.0 ★推奨
   3. patch (バグ修正) → 2.0.1
   4. スキップ（バージョンを上げない）
   ```
4. ユーザーが「2」を選択
5. npm version minor実行 → 2.1.0に更新
6. package.jsonをコミットに含める
7. プッシュ・PR作成

### 例4: C#プロジェクトでのバージョン更新

**ユーザー**: MyWebAPIのPR作成して

**スキルの動作**:
1. MyWebAPIディレクトリに移動
2. 品質チェック実行（dotnet build, dotnet test） → すべて成功
3. .csprojファイルのバージョンチェック
   ```
   ⚠️ バージョン番号が更新されていません

   現在のバージョン: 1.2.0
   mainブランチ: 1.2.0
   検出ファイル: MyWebAPI/MyWebAPI.csproj

   コミットメッセージ: fix: ユーザー認証のバグを修正 #89
   推奨: PATCH バージョンアップ (バグ修正)

   どのバージョンを上げますか？
   1. major (破壊的変更) → 2.0.0
   2. minor (新機能) → 1.3.0
   3. patch (バグ修正) → 1.2.1 ★推奨
   4. スキップ（バージョンを上げない）
   ```
4. ユーザーが「3」を選択
5. .csprojファイルの以下のタグを更新:
   ```xml
   <Version>1.2.1</Version>
   <AssemblyVersion>1.2.1</AssemblyVersion>
   <FileVersion>1.2.1</FileVersion>
   ```
6. MyWebAPI.csprojをコミットに含める
7. プッシュ・PR作成

**更新される.csprojの例**:
```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Version>1.2.1</Version>
    <AssemblyVersion>1.2.1</AssemblyVersion>
    <FileVersion>1.2.1</FileVersion>
  </PropertyGroup>
</Project>
```

### 例5: エラー発生時

**ユーザー**: PR作成して

**スキルの動作**:
1. 品質チェック開始
2. Lintでエラー検出
3. **即座に停止**
4. エラー内容を詳細に報告:
   ```
   ❌ コード品質チェックに失敗しました

   Lintエラー:
   - src/components/UserProfile.tsx:42:5
     error: 'userName' is assigned but never used

   - src/services/api.ts:18:10
     error: Missing return type on function

   修正後に再度PR作成を実行してください。
   ```

## エラーハンドリング

### 品質チェック失敗

**型チェックエラー**:
```
❌ 型チェックに失敗しました

エラー数: 3件

src/types/user.ts:15:8
  Type 'string | undefined' is not assignable to type 'string'

修正してから再実行してください。
```

**Lintエラー**:
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

**ビルドエラー**:
```
❌ ビルドに失敗しました

原因: webpack compilation error
  Module not found: '@/components/NewComponent'

ファイルパスを確認してください。
```

### Git操作エラー

**コミットするファイルがない**:
```
⚠️ コミットする変更がありません

git statusの結果:
  On branch feature/issue-42
  nothing to commit, working tree clean

すでにコミット済みの場合は、プッシュのみ実行しますか？
```

**プッシュ失敗（コンフリクト）**:
```
❌ プッシュに失敗しました

原因: リモートブランチが先行しています

対処方法:
  git pull --rebase origin $(git branch --show-current)
  # コンフリクトを解決
  git push
```

### GitHub PR作成エラー

**既にPRが存在**:
```
⚠️ このブランチのPRは既に存在します

既存PR: #12
URL: https://github.com/user/repo/pull/12

既存PRを更新しますか？それとも新しいコミットを追加しますか？
```

**権限不足**:
```
❌ PRの作成に失敗しました

原因: 権限不足
このリポジトリへの書き込み権限がありません。

対処方法:
1. リポジトリをフォーク
2. フォーク先にプッシュ
3. 元リポジトリへPR作成
```

## 品質チェックのカスタマイズ

プロジェクトルートに `.claude/pr-check-config.json` を配置することで、チェック内容をカスタマイズ可能:

```json
{
  "checks": {
    "typeCheck": true,
    "lint": true,
    "build": true,
    "test": false,
    "format": true
  },
  "commands": {
    "typeCheck": "npx tsc --noEmit",
    "lint": "npm run lint",
    "build": "npm run build",
    "test": "npm test",
    "format": "npm run format:check"
  },
  "skipOnPatterns": [
    "docs/**",
    "*.md"
  ]
}
```

## 注意事項

1. **品質チェックは必須**
   - すべてのチェックが成功するまでPR作成しません
   - 妥協せず品質を保証します

2. **バージョン番号管理**
   - プロジェクトタイプを自動検出し、適切なバージョンファイルをチェック
     - Node.js/npm: package.json
     - C#/.NET: *.csproj (Version, AssemblyVersion, FileVersion)
   - mainブランチとバージョンが同じ場合、更新を提案
   - セマンティックバージョニング（SemVer）に準拠
   - コミットメッセージから推奨バージョンを自動判定
   - ユーザーが最終判断（スキップも可能）

3. **開発ワークフロー遵守**
   - プロジェクトのルールに従います
   - コミットメッセージ規約を守ります

4. **自動化の範囲**
   - コミット・プッシュ・PR作成まで自動
   - レビューやマージは手動

5. **ログの保存**
   - 品質チェック結果は `./logs/` に保存
   - トラブルシューティングに活用

6. **Issue連携**
   - Issue番号が含まれる場合は自動リンク
   - `fixes #XX` でクローズ連携

## 関連スキル・コマンド

- `issue-fixer` - Issue対応スキル
- `branch-cleaner` - ブランチクリーンアップスキル
- `/create-pr [プロジェクト名]` - カスタムスラッシュコマンド版

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
