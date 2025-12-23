# バージョン管理 - 高度な機能

## プレリリースバージョン

### Node.js/npm

#### アルファ版
```bash
npm version prerelease --preid=alpha --no-git-tag-version
# 1.2.0 → 1.2.1-alpha.0
```

#### ベータ版
```bash
npm version prerelease --preid=beta --no-git-tag-version
# 1.2.0 → 1.2.1-beta.0
```

#### リリース候補
```bash
npm version prerelease --preid=rc --no-git-tag-version
# 1.2.0 → 1.2.1-rc.0
```

### プレリリースバージョンの形式
```
MAJOR.MINOR.PATCH-PRERELEASE.BUILD

例:
- 2.0.0-alpha.1
- 2.0.0-beta.2
- 2.0.0-rc.1
```

## モノレポ対応

### 複数のpackage.jsonの更新

```bash
# 複数のpackage.jsonが存在する場合
find . -name "package.json" -not -path "*/node_modules/*" | while read -r pkg; do
  echo "Updating: $pkg"
  cd "$(dirname "$pkg")"
  npm version minor --no-git-tag-version
  cd - > /dev/null
done
```

### Lernaを使用した一括更新
```bash
# すべてのパッケージのバージョンを統一
lerna version minor --no-git-tag-version --yes

# 独立バージョン管理
lerna version --independent
```

### Workspaceパターン
```bash
# package.jsonのworkspacesフィールドを確認
if grep -q "workspaces" package.json; then
  echo "Workspace detected"
  # 各ワークスペースを更新
  for pkg in packages/*; do
    if [ -f "$pkg/package.json" ]; then
      cd "$pkg"
      npm version $VERSION_TYPE --no-git-tag-version
      cd -
    fi
  done
fi
```

## CHANGELOG自動生成

### CHANGELOGの構造
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-01-15

### Added
- ユーザープロフィール編集機能
- エクスポート機能

### Fixed
- ログインエラーの修正
- パフォーマンス改善

### Changed
- APIレスポンス形式の変更

### Deprecated
- 旧認証方式（v3.0で削除予定）

## [2.0.0] - 2025-01-01
...
```

### CHANGELOGエントリの生成
```bash
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
```

## Gitタグの管理

### タグ作成
```bash
# アノテート付きタグ
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"

# タグをリモートにプッシュ
git push origin "v$NEW_VERSION"
```

### タグ一覧
```bash
# すべてのタグを表示
git tag -l

# バージョン順に並べ替え
git tag -l | sort -V
```

### タグの削除
```bash
# ローカルタグを削除
git tag -d v1.0.0

# リモートタグを削除
git push origin --delete v1.0.0
```

## カスタム設定

### .versionrc (standard-version設定)
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

### 環境変数
```bash
# デフォルトのバージョン種別
export VERSION_DEFAULT_TYPE=minor

# CHANGELOGの生成を無効化
export VERSION_SKIP_CHANGELOG=true

# タグの自動作成を無効化
export VERSION_SKIP_TAG=true
```

## CI/CD連携

### GitHub Actions例
```yaml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Bump version
        run: npm version patch --no-git-tag-version
      - name: Commit changes
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add package.json
          git commit -m "chore: bump version"
          git push
```
