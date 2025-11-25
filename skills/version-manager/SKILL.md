---
name: version-manager
description: セマンティックバージョニングに基づいたバージョン番号管理を自動化するスキル。コミット履歴から適切なバージョンを推論し、package.json/.csproj等を更新、CHANGELOGを生成する。「バージョンを上げて」「バージョン更新して」と依頼された時に使用
---

# Version Manager - バージョン番号管理スキル

このスキルは、セマンティックバージョニング（SemVer）に基づいてプロジェクトのバージョン番号を自動管理します。

## 目的

- コミット履歴からバージョン種別（major/minor/patch）を自動推論
- プロジェクトタイプに応じたバージョンファイルの更新
- CHANGELOGの自動生成
- バージョンタグの作成

## 使用タイミング

- 「バージョンを上げて」と依頼された時
- 「バージョン更新して」と依頼された時
- 「次のリリースバージョンを設定して」と依頼された時
- PR作成前にバージョンチェックが必要な時

## セマンティックバージョニング（SemVer）

```
MAJOR.MINOR.PATCH (例: 2.1.3)
```

### バージョン種別

1. **MAJOR (X.0.0)** - 破壊的変更
   - API仕様の変更
   - 後方互換性のない変更
   - 設定形式の変更

2. **MINOR (0.X.0)** - 新機能追加
   - 後方互換性のある新機能
   - 既存機能の拡張
   - 非推奨機能の追加

3. **PATCH (0.0.X)** - バグ修正
   - 後方互換性のあるバグ修正
   - セキュリティパッチ
   - パフォーマンス改善

## サポートするプロジェクトタイプ

### 1. Node.js/npm (package.json)

**ファイル**: `package.json`

**更新フィールド**:
```json
{
  "version": "2.1.3"
}
```

**更新コマンド**:
```bash
npm version major --no-git-tag-version  # 2.1.3 → 3.0.0
npm version minor --no-git-tag-version  # 2.1.3 → 2.2.0
npm version patch --no-git-tag-version  # 2.1.3 → 2.1.4
```

### 2. C#/.NET (*.csproj)

**ファイル**: `*.csproj`

**更新フィールド**:
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <Version>2.1.3</Version>
    <AssemblyVersion>2.1.3</AssemblyVersion>
    <FileVersion>2.1.3</FileVersion>
  </PropertyGroup>
</Project>
```

**更新方法**:
```bash
# sedを使用した一括更新
sed -i "s|<Version>2.1.3</Version>|<Version>3.0.0</Version>|" MyProject.csproj
sed -i "s|<AssemblyVersion>2.1.3</AssemblyVersion>|<AssemblyVersion>3.0.0</AssemblyVersion>|" MyProject.csproj
sed -i "s|<FileVersion>2.1.3</FileVersion>|<FileVersion>3.0.0</FileVersion>|" MyProject.csproj
```

### 3. Python (pyproject.toml / setup.py)

**ファイル**: `pyproject.toml` または `setup.py`

**pyproject.toml**:
```toml
[project]
version = "2.1.3"
```

**setup.py**:
```python
setup(
    name="my-package",
    version="2.1.3",
)
```

### 4. Rust (Cargo.toml)

**ファイル**: `Cargo.toml`

```toml
[package]
name = "my-crate"
version = "2.1.3"
```

### 5. Flutter/Dart (pubspec.yaml)

**ファイル**: `pubspec.yaml`

```yaml
version: 2.1.3+10
# フォーマット: version+build_number
```

## コミットメッセージからの推論

### Conventional Commits 形式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### バージョン種別の判定ロジック

#### MAJOR バージョンアップ

以下の条件で判定:
- コミットメッセージに `BREAKING CHANGE:` を含む
- type に `!` が付いている（例: `feat!:`, `fix!:`）
- フッターに `BREAKING-CHANGE:` がある

**例**:
```
feat!: APIのレスポンス形式を変更

BREAKING CHANGE: レスポンスがJSONからGraphQLに変更されました
```

#### MINOR バージョンアップ

以下の条件で判定:
- type が `feat` (新機能)
- type が `feature`

**例**:
```
feat: ユーザープロフィール編集機能を追加

- プロフィール編集フォームを実装
- バリデーション処理を追加
```

#### PATCH バージョンアップ

以下の条件で判定:
- type が `fix` (バグ修正)
- type が `perf` (パフォーマンス改善)
- type が `security` (セキュリティ修正)

**例**:
```
fix: ログイン時の認証エラーを修正

refs #42
```

#### バージョンアップ不要

以下の type はバージョンアップ不要:
- `docs` - ドキュメント変更のみ
- `style` - コードスタイル変更
- `refactor` - リファクタリング（機能変更なし）
- `test` - テスト追加・修正
- `chore` - ビルド・設定変更

## 実行フロー

### ステップ1: プロジェクトタイプの検出

```bash
# バージョンファイルを検出
if [ -f package.json ]; then
  PROJECT_TYPE="npm"
  VERSION_FILE="package.json"
elif [ -n "$(find . -maxdepth 2 -name "*.csproj" | head -n 1)" ]; then
  PROJECT_TYPE="csharp"
  VERSION_FILE=$(find . -maxdepth 2 -name "*.csproj" | head -n 1)
elif [ -f pyproject.toml ]; then
  PROJECT_TYPE="python"
  VERSION_FILE="pyproject.toml"
elif [ -f Cargo.toml ]; then
  PROJECT_TYPE="rust"
  VERSION_FILE="Cargo.toml"
elif [ -f pubspec.yaml ]; then
  PROJECT_TYPE="flutter"
  VERSION_FILE="pubspec.yaml"
else
  echo "❌ サポートされているバージョンファイルが見つかりません"
  exit 1
fi

echo "✓ プロジェクトタイプ: $PROJECT_TYPE"
echo "✓ バージョンファイル: $VERSION_FILE"
```

### ステップ2: 現在のバージョン取得

```bash
# プロジェクトタイプに応じた取得方法
case $PROJECT_TYPE in
  npm)
    CURRENT_VERSION=$(node -p "require('./package.json').version")
    ;;
  csharp)
    CURRENT_VERSION=$(grep -oP '<Version>\K[^<]+' "$VERSION_FILE" | head -n 1)
    ;;
  python)
    CURRENT_VERSION=$(grep -oP 'version = "\K[^"]+' pyproject.toml)
    ;;
  rust)
    CURRENT_VERSION=$(grep -oP 'version = "\K[^"]+' Cargo.toml | head -n 1)
    ;;
  flutter)
    CURRENT_VERSION=$(grep -oP 'version: \K[^+]+' pubspec.yaml)
    ;;
esac

echo "現在のバージョン: $CURRENT_VERSION"
```

### ステップ3: mainブランチとの比較

```bash
# mainブランチの最新バージョンを取得
git fetch origin main

case $PROJECT_TYPE in
  npm)
    MAIN_VERSION=$(git show origin/main:package.json | node -p "JSON.parse(require('fs').readFileSync('/dev/stdin', 'utf8')).version")
    ;;
  csharp)
    MAIN_VERSION=$(git show "origin/main:$VERSION_FILE" | grep -oP '<Version>\K[^<]+' | head -n 1)
    ;;
  # 他のタイプも同様
esac

echo "mainブランチのバージョン: $MAIN_VERSION"

if [ "$CURRENT_VERSION" = "$MAIN_VERSION" ]; then
  echo "⚠️ バージョンが更新されていません"
  NEEDS_UPDATE=true
else
  echo "✓ バージョンは既に更新されています"
  NEEDS_UPDATE=false
fi
```

### ステップ4: コミット履歴の分析

```bash
# mainブランチからの差分コミットを取得
COMMITS=$(git log origin/main..HEAD --pretty=format:"%s")

# バージョン種別を判定
VERSION_TYPE="none"

# BREAKING CHANGEチェック
if echo "$COMMITS" | grep -qE "(BREAKING CHANGE|BREAKING-CHANGE|!)"; then
  VERSION_TYPE="major"
  REASON="破壊的変更が含まれています"
# 新機能チェック
elif echo "$COMMITS" | grep -qE "^feat(\(.+\))?:"; then
  VERSION_TYPE="minor"
  REASON="新機能が追加されています"
# バグ修正チェック
elif echo "$COMMITS" | grep -qE "^(fix|perf|security)(\(.+\))?:"; then
  VERSION_TYPE="patch"
  REASON="バグ修正またはパフォーマンス改善が含まれています"
# ドキュメント・リファクタリング等
else
  VERSION_TYPE="none"
  REASON="バージョンアップが不要な変更のみです"
fi

echo "推奨バージョン種別: $VERSION_TYPE"
echo "理由: $REASON"
```

### ステップ5: ユーザーへの確認

```bash
if [ "$NEEDS_UPDATE" = true ]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "バージョン更新の確認"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "現在のバージョン: $CURRENT_VERSION"
  echo "mainブランチ: $MAIN_VERSION"
  echo ""
  echo "コミット履歴の分析結果:"
  echo "推奨: $VERSION_TYPE ($REASON)"
  echo ""
  echo "どのバージョンを上げますか？"
  echo ""

  # バージョン計算
  IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

  echo "1. major (破壊的変更) → $((MAJOR + 1)).0.0"
  if [ "$VERSION_TYPE" = "major" ]; then
    echo "   ★ 推奨"
  fi

  echo "2. minor (新機能) → $MAJOR.$((MINOR + 1)).0"
  if [ "$VERSION_TYPE" = "minor" ]; then
    echo "   ★ 推奨"
  fi

  echo "3. patch (バグ修正) → $MAJOR.$MINOR.$((PATCH + 1))"
  if [ "$VERSION_TYPE" = "patch" ]; then
    echo "   ★ 推奨"
  fi

  echo "4. スキップ (バージョンを上げない)"
  echo ""

  read -p "選択してください (1-4): " CHOICE
fi
```

### ステップ6: バージョン更新の実行

#### Node.js/npm

```bash
case $CHOICE in
  1) npm version major --no-git-tag-version ;;
  2) npm version minor --no-git-tag-version ;;
  3) npm version patch --no-git-tag-version ;;
  4) echo "バージョン更新をスキップしました"; exit 0 ;;
esac

NEW_VERSION=$(node -p "require('./package.json').version")
echo "✅ バージョンを更新しました: $CURRENT_VERSION → $NEW_VERSION"
```

#### C#/.NET

```bash
# バージョン計算
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

case $CHOICE in
  1) NEW_VERSION="$((MAJOR + 1)).0.0" ;;
  2) NEW_VERSION="$MAJOR.$((MINOR + 1)).0" ;;
  3) NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))" ;;
  4) echo "バージョン更新をスキップしました"; exit 0 ;;
esac

# .csprojファイルを更新
sed -i "s|<Version>$CURRENT_VERSION</Version>|<Version>$NEW_VERSION</Version>|" "$VERSION_FILE"
sed -i "s|<AssemblyVersion>$CURRENT_VERSION</AssemblyVersion>|<AssemblyVersion>$NEW_VERSION</AssemblyVersion>|" "$VERSION_FILE"
sed -i "s|<FileVersion>$CURRENT_VERSION</FileVersion>|<FileVersion>$NEW_VERSION</FileVersion>|" "$VERSION_FILE"

echo "✅ バージョンを更新しました: $CURRENT_VERSION → $NEW_VERSION"
echo "   更新ファイル: $VERSION_FILE"
```

### ステップ7: CHANGELOG生成

```bash
# CHANGELOG.mdが存在しない場合は作成
if [ ! -f CHANGELOG.md ]; then
  cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

EOF
fi

# 新しいバージョンのエントリを追加
DATE=$(date +%Y-%m-%d)
TEMP_FILE=$(mktemp)

# ヘッダーを保持
head -n 6 CHANGELOG.md > "$TEMP_FILE"

# 新しいエントリを追加
echo "" >> "$TEMP_FILE"
echo "## [$NEW_VERSION] - $DATE" >> "$TEMP_FILE"
echo "" >> "$TEMP_FILE"

# コミットメッセージを分類
git log origin/main..HEAD --pretty=format:"%s" | while read -r commit; do
  case "$commit" in
    feat*|feature*)
      echo "### Added" >> "$TEMP_FILE"
      echo "- ${commit#*: }" >> "$TEMP_FILE"
      ;;
    fix*)
      echo "### Fixed" >> "$TEMP_FILE"
      echo "- ${commit#*: }" >> "$TEMP_FILE"
      ;;
    perf*)
      echo "### Performance" >> "$TEMP_FILE"
      echo "- ${commit#*: }" >> "$TEMP_FILE"
      ;;
    refactor*)
      echo "### Changed" >> "$TEMP_FILE"
      echo "- ${commit#*: }" >> "$TEMP_FILE"
      ;;
  esac
done

# 既存のエントリを追加
tail -n +7 CHANGELOG.md >> "$TEMP_FILE"

# 置き換え
mv "$TEMP_FILE" CHANGELOG.md

echo "✅ CHANGELOG.mdを更新しました"
```

### ステップ8: Gitタグの作成（オプション）

```bash
# ユーザーに確認
read -p "Gitタグ (v$NEW_VERSION) を作成しますか？ (y/n): " CREATE_TAG

if [ "$CREATE_TAG" = "y" ]; then
  git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"
  echo "✅ Gitタグを作成しました: v$NEW_VERSION"

  read -p "タグをリモートにプッシュしますか？ (y/n): " PUSH_TAG
  if [ "$PUSH_TAG" = "y" ]; then
    git push origin "v$NEW_VERSION"
    echo "✅ タグをプッシュしました"
  fi
fi
```

### ステップ9: 結果報告

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "バージョン更新完了"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 プロジェクト: $PROJECT_TYPE"
echo "📄 更新ファイル: $VERSION_FILE"
echo "🔢 旧バージョン: $CURRENT_VERSION"
echo "🔢 新バージョン: $NEW_VERSION"
echo "📝 CHANGELOG: 更新済み"
if [ "$CREATE_TAG" = "y" ]; then
  echo "🏷️  Gitタグ: v$NEW_VERSION (作成済み)"
fi
echo ""
echo "次のステップ:"
echo "1. バージョンファイルとCHANGELOGをコミット"
echo "2. プッシュしてPR作成"
echo ""
```

## 使用例

### 例1: 自動推論でバージョン更新

**ユーザー**: value-meのバージョンを上げて

**スキルの動作**:
```
1. プロジェクトタイプ検出: npm (package.json)
2. 現在のバージョン: 1.2.0
3. mainブランチ: 1.2.0
4. コミット履歴分析:
   - feat: チームコスト計算機能を追加
   → 推奨: MINOR (新機能)
5. ユーザー選択: 2 (minor)
6. バージョン更新: 1.2.0 → 1.3.0
7. CHANGELOG更新
8. Gitタグ作成: v1.3.0
```

### 例2: C#プロジェクトのバージョン更新

**ユーザー**: MyWebAPIのバージョンを更新

**スキルの動作**:
```
1. プロジェクトタイプ検出: csharp (MyWebAPI.csproj)
2. 現在のバージョン: 2.1.0
3. mainブランチ: 2.1.0
4. コミット履歴分析:
   - fix: 認証エラーを修正
   → 推奨: PATCH (バグ修正)
5. ユーザー選択: 3 (patch)
6. .csproj更新: 2.1.0 → 2.1.1
   - Version
   - AssemblyVersion
   - FileVersion
7. CHANGELOG更新
```

## 高度な機能

### プレリリースバージョン

```bash
# アルファ版
npm version prerelease --preid=alpha --no-git-tag-version
# 1.2.0 → 1.2.1-alpha.0

# ベータ版
npm version prerelease --preid=beta --no-git-tag-version
# 1.2.0 → 1.2.1-beta.0

# リリース候補
npm version prerelease --preid=rc --no-git-tag-version
# 1.2.0 → 1.2.1-rc.0
```

### モノレポ対応

```bash
# 複数のpackage.jsonが存在する場合
find . -name "package.json" -not -path "*/node_modules/*" | while read -r pkg; do
  echo "Updating: $pkg"
  cd "$(dirname "$pkg")"
  npm version minor --no-git-tag-version
  cd - > /dev/null
done
```

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

### mainブランチが存在しない

```
⚠️ 警告: mainブランチが見つかりません

現在のバージョンのみ表示します。
```

## 設定ファイル

### .versionrc (optional-release-it設定)

```json
{
  "types": [
    {"type": "feat", "section": "Features"},
    {"type": "fix", "section": "Bug Fixes"},
    {"type": "perf", "section": "Performance"},
    {"type": "refactor", "section": "Refactoring"},
    {"type": "docs", "section": "Documentation"},
    {"type": "test", "section": "Tests"},
    {"type": "chore", "hidden": true}
  ],
  "commitUrlFormat": "{{host}}/{{owner}}/{{repository}}/commit/{{hash}}",
  "compareUrlFormat": "{{host}}/{{owner}}/{{repository}}/compare/{{previousTag}}...{{currentTag}}"
}
```

## 関連ツール

- `pr-creator` - PR作成時にバージョンチェック
- `conventional-changelog` - CHANGELOG自動生成
- `standard-version` - バージョン管理自動化

## 注意事項

1. **mainブランチとの同期**
   - バージョン更新前に必ずmainブランチを確認

2. **CHANGELOGの保守**
   - 自動生成は補助として使用
   - 必要に応じて手動で編集

3. **タグの管理**
   - タグは削除・変更しない
   - 誤って作成した場合は新しいバージョンで対応

4. **セマンティックバージョニングの遵守**
   - 規約に従ったコミットメッセージを使用
   - 破壊的変更は明確に記載
