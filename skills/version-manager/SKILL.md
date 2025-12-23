---
name: version-manager
description: セマンティックバージョニングに基づいたバージョン番号管理を自動化するスキル。コミット履歴から適切なバージョンを推論し、package.json/.csproj等を更新、CHANGELOGを生成する。「バージョンを上げて」「バージョン更新して」と依頼された時に使用
---

# Version Manager - バージョン番号管理スキル

セマンティックバージョニング（SemVer）に基づいてプロジェクトのバージョン番号を自動管理します。

## 目的

- コミット履歴からバージョン種別（major/minor/patch）を自動推論
- プロジェクトタイプに応じたバージョンファイルの更新
- CHANGELOGの自動生成
- バージョンタグの作成

## 使用タイミング

- 「バージョンを上げて」
- 「バージョン更新して」
- 「次のリリースバージョンを設定して」
- PR作成前にバージョンチェックが必要な時

## セマンティックバージョニング（SemVer）

```
MAJOR.MINOR.PATCH (例: 2.1.3)
```

### バージョン種別
1. **MAJOR (X.0.0)** - 破壊的変更
2. **MINOR (0.X.0)** - 新機能追加（後方互換性あり）
3. **PATCH (0.0.X)** - バグ修正

## サポートするプロジェクトタイプ

| タイプ | ファイル | 詳細 |
|--------|---------|------|
| Node.js/npm | package.json | `references/version-languages.md` |
| C#/.NET | *.csproj | `references/version-languages.md` |
| Python | pyproject.toml, setup.py | `references/version-languages.md` |
| Rust | Cargo.toml | `references/version-languages.md` |
| Flutter/Dart | pubspec.yaml | `references/version-languages.md` |

## コミットメッセージからの推論

### Conventional Commits 形式
```
<type>(<scope>): <subject>
```

### バージョン種別の判定

| 条件 | バージョン種別 |
|------|---------------|
| `BREAKING CHANGE:` を含む | MAJOR |
| type に `!` が付いている | MAJOR |
| type が `feat` | MINOR |
| type が `fix`, `perf`, `security` | PATCH |
| type が `docs`, `style`, `refactor`, `test`, `chore` | バージョンアップ不要 |

## 実行フロー

### 1. プロジェクトタイプの検出
```bash
if [ -f package.json ]; then
  PROJECT_TYPE="npm"
  VERSION_FILE="package.json"
elif [ -n "$(find . -maxdepth 2 -name "*.csproj" | head -n 1)" ]; then
  PROJECT_TYPE="csharp"
  VERSION_FILE=$(find . -maxdepth 2 -name "*.csproj" | head -n 1)
# ...
fi
```

### 2. 現在のバージョン取得
プロジェクトタイプに応じた取得方法で実行

### 3. mainブランチとの比較
```bash
git fetch origin main

# mainブランチの最新バージョンを取得
# プロジェクトタイプに応じた方法で取得

if [ "$CURRENT_VERSION" = "$MAIN_VERSION" ]; then
  echo "⚠️ バージョンが更新されていません"
  NEEDS_UPDATE=true
fi
```

### 4. コミット履歴の分析
```bash
COMMITS=$(git log origin/main..HEAD --pretty=format:"%s")

# バージョン種別を判定
if echo "$COMMITS" | grep -qE "(BREAKING CHANGE|!)"; then
  VERSION_TYPE="major"
elif echo "$COMMITS" | grep -qE "^feat"; then
  VERSION_TYPE="minor"
elif echo "$COMMITS" | grep -qE "^(fix|perf|security)"; then
  VERSION_TYPE="patch"
else
  VERSION_TYPE="none"
fi
```

### 5. ユーザーへの確認
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
バージョン更新の確認
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

現在のバージョン: 2.1.0
mainブランチ: 2.1.0

コミット履歴の分析結果:
推奨: minor (新機能が追加されています)

どのバージョンを上げますか？

1. major (破壊的変更) → 3.0.0
2. minor (新機能) → 2.2.0 ★推奨
3. patch (バグ修正) → 2.1.1
4. スキップ (バージョンを上げない)

選択してください (1-4):
```

### 6. バージョン更新の実行
プロジェクトタイプに応じた更新方法で実行

**詳細**: `references/version-languages.md` 参照

### 7. CHANGELOG生成
```bash
# CHANGELOG.mdが存在しない場合は作成
if [ ! -f CHANGELOG.md ]; then
  # テンプレート作成
fi

# 新しいバージョンのエントリを追加
# コミットメッセージを分類して追加

echo "✅ CHANGELOG.mdを更新しました"
```

### 8. Gitタグの作成（オプション）
```bash
read -p "Gitタグ (v$NEW_VERSION) を作成しますか？ (y/n): " CREATE_TAG

if [ "$CREATE_TAG" = "y" ]; then
  git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"
  echo "✅ Gitタグを作成しました: v$NEW_VERSION"
fi
```

### 9. 結果報告
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
バージョン更新完了
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 プロジェクト: npm
📄 更新ファイル: package.json
🔢 旧バージョン: 2.1.0
🔢 新バージョン: 2.2.0
📝 CHANGELOG: 更新済み
🏷️  Gitタグ: v2.2.0 (作成済み)

次のステップ:
1. バージョンファイルとCHANGELOGをコミット
2. プッシュしてPR作成
```

## 使用例

### 例1: 自動推論でバージョン更新
**ユーザー**: value-meのバージョンを上げて

**動作**:
1. プロジェクトタイプ検出: npm (package.json)
2. 現在のバージョン: 1.2.0
3. コミット履歴分析 → 推奨: MINOR
4. ユーザー選択: 2 (minor)
5. バージョン更新: 1.2.0 → 1.3.0
6. CHANGELOG更新
7. Gitタグ作成: v1.3.0

### 例2: C#プロジェクトのバージョン更新
**ユーザー**: MyWebAPIのバージョンを更新

**動作**:
1. プロジェクトタイプ検出: csharp (MyWebAPI.csproj)
2. 現在のバージョン: 2.1.0
3. コミット履歴分析 → 推奨: PATCH
4. .csproj更新: 2.1.0 → 2.1.1 (Version, AssemblyVersion, FileVersion)
5. CHANGELOG更新

## 高度な機能

プレリリースバージョン、モノレポ対応など詳細は `references/version-advanced.md` 参照

## エラーハンドリング

### バージョンファイルが見つからない
```
❌ エラー: サポートされているバージョンファイルが見つかりません

対応方法:
1. package.json, *.csproj, pyproject.toml等を確認
2. プロジェクトルートで実行しているか確認
```

### Gitリポジトリではない
```
❌ エラー: Gitリポジトリが初期化されていません

対応方法:
git init
```

## 注意事項

1. **mainブランチとの同期** - バージョン更新前に必ずmainブランチを確認
2. **CHANGELOGの保守** - 自動生成は補助として使用、必要に応じて手動編集
3. **タグの管理** - タグは削除・変更しない
4. **セマンティックバージョニングの遵守** - 規約に従ったコミットメッセージを使用

## 関連ツール

- `pr-creator` - PR作成時にバージョンチェック
- `conventional-changelog` - CHANGELOG自動生成
- `standard-version` - バージョン管理自動化
