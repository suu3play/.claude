# バージョン管理 - 言語別詳細

## Node.js/npm

### バージョンファイル
`package.json`

### 更新フィールド
```json
{
  "version": "2.1.3"
}
```

### 現在のバージョン取得
```bash
CURRENT_VERSION=$(node -p "require('./package.json').version")
echo "現在のバージョン: $CURRENT_VERSION"
```

### mainブランチのバージョン取得
```bash
git show main:package.json > /tmp/package.json.main
MAIN_VERSION=$(node -p "require('/tmp/package.json.main').version")
echo "mainブランチのバージョン: $MAIN_VERSION"
```

### バージョン更新
```bash
npm version major --no-git-tag-version  # 2.1.3 → 3.0.0
npm version minor --no-git-tag-version  # 2.1.3 → 2.2.0
npm version patch --no-git-tag-version  # 2.1.3 → 2.1.4

NEW_VERSION=$(node -p "require('./package.json').version")
echo "✅ バージョンを更新しました: $CURRENT_VERSION → $NEW_VERSION"
```

## C#/.NET

### バージョンファイル
`*.csproj`

### 更新フィールド
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <Version>2.1.3</Version>
    <AssemblyVersion>2.1.3</AssemblyVersion>
    <FileVersion>2.1.3</FileVersion>
  </PropertyGroup>
</Project>
```

### .csprojファイルの検出
```bash
CSPROJ_FILE=$(find . -maxdepth 2 -name "*.csproj" | head -n 1)
if [ -n "$CSPROJ_FILE" ]; then
  echo "✓ .csprojファイルが見つかりました: $CSPROJ_FILE"
fi
```

### 現在のバージョン取得
```bash
CURRENT_VERSION=$(grep -oP '<Version>\K[^<]+' "$CSPROJ_FILE")
echo "現在のバージョン: $CURRENT_VERSION"
```

### mainブランチのバージョン取得
```bash
MAIN_VERSION=$(git show "main:$CSPROJ_FILE" | grep -oP '<Version>\K[^<]+')
echo "mainブランチのバージョン: $MAIN_VERSION"
```

### バージョン更新
```bash
# バージョン計算
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"
case "$VERSION_TYPE" in
  major) NEW_VERSION="$((MAJOR + 1)).0.0" ;;
  minor) NEW_VERSION="$MAJOR.$((MINOR + 1)).0" ;;
  patch) NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))" ;;
esac

# .csprojファイルを更新
sed -i "s|<Version>$CURRENT_VERSION</Version>|<Version>$NEW_VERSION</Version>|" "$CSPROJ_FILE"
sed -i "s|<AssemblyVersion>$CURRENT_VERSION</AssemblyVersion>|<AssemblyVersion>$NEW_VERSION</AssemblyVersion>|" "$CSPROJ_FILE"
sed -i "s|<FileVersion>$CURRENT_VERSION</FileVersion>|<FileVersion>$NEW_VERSION</FileVersion>|" "$CSPROJ_FILE"

echo "✅ バージョンを更新しました: $CURRENT_VERSION → $NEW_VERSION"
echo "   更新ファイル: $CSPROJ_FILE"
```

## Python

### バージョンファイル
`pyproject.toml` または `setup.py`

### pyproject.toml
```toml
[project]
version = "2.1.3"
```

### 現在のバージョン取得
```bash
CURRENT_VERSION=$(grep -oP 'version = "\K[^"]+' pyproject.toml)
```

### バージョン更新
```bash
sed -i "s|version = \"$CURRENT_VERSION\"|version = \"$NEW_VERSION\"|" pyproject.toml
```

## Rust

### バージョンファイル
`Cargo.toml`

### フォーマット
```toml
[package]
name = "my-crate"
version = "2.1.3"
```

### 現在のバージョン取得
```bash
CURRENT_VERSION=$(grep -oP 'version = "\K[^"]+' Cargo.toml | head -n 1)
```

### バージョン更新
```bash
sed -i "0,/version = \"$CURRENT_VERSION\"/s//version = \"$NEW_VERSION\"/" Cargo.toml
```

## Flutter/Dart

### バージョンファイル
`pubspec.yaml`

### フォーマット
```yaml
version: 2.1.3+10
# フォーマット: version+build_number
```

### 現在のバージョン取得
```bash
CURRENT_VERSION=$(grep -oP 'version: \K[^+]+' pubspec.yaml)
```

### バージョン更新
```bash
# build_numberを保持してバージョンのみ更新
BUILD_NUMBER=$(grep -oP 'version: [^+]+\+\K[0-9]+' pubspec.yaml)
sed -i "s|version: .*|version: $NEW_VERSION+$BUILD_NUMBER|" pubspec.yaml
```

## Go

### バージョンファイル
通常はgit tagで管理

### version.goパターン
```go
package main

const Version = "2.1.3"
```

### バージョン更新
```bash
sed -i "s|const Version = \"$CURRENT_VERSION\"|const Version = \"$NEW_VERSION\"|" version.go
```
