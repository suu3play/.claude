# コード分析ツール詳細

各言語のコード分析ツールと実行コマンド。

## TypeScript/JavaScript

### 型チェック
```bash
npx tsc --noEmit
```

### Lint
```bash
npm run lint
# または
npx eslint .
```

### ビルド
```bash
npm run build
```

### パターン検索
```bash
# TODO, FIXME コメント
grep -r "TODO:\|FIXME:\|HACK:\|XXX:" --include="*.ts" --include="*.tsx"

# any型の使用
grep -r ": any\|<any>" --include="*.ts" --include="*.tsx"

# console.log
grep -r "console\.log" --include="*.ts" --include="*.tsx"
```

## Python

### 型チェック
```bash
mypy .
```

### Lint
```bash
# Ruff (高速)
ruff check .

# Pylint (詳細)
pylint **/*.py
```

### フォーマットチェック
```bash
black --check .
```

### パターン検索
```bash
# TODO コメント
grep -r "TODO:\|FIXME:" --include="*.py"

# print デバッグ
grep -r "print(" --include="*.py"
```

## Flutter/Dart

### 解析
```bash
flutter analyze
```

### フォーマットチェック
```bash
dart format --set-exit-if-changed .
```

### パターン検索
```bash
# TODO コメント
grep -r "TODO:\|FIXME:" --include="*.dart"

# print デバッグ
grep -r "print(" --include="*.dart"
```

## Rust

### チェック
```bash
cargo check
```

### Clippy（Lint）
```bash
cargo clippy -- -W clippy::all
```

### フォーマットチェック
```bash
cargo fmt --check
```

### パターン検索
```bash
# TODO コメント
grep -r "TODO:\|FIXME:" --include="*.rs"

# unwrap() (潜在的panic)
grep -r "\.unwrap()" --include="*.rs"
```

## C#

### ビルド
```bash
dotnet build
```

### コード分析
```bash
dotnet format --verify-no-changes
```

### パターン検索
```bash
# TODO コメント
grep -r "TODO:\|FIXME:" --include="*.cs"

# Debug.WriteLine
grep -r "Debug\.WriteLine" --include="*.cs"
```

## Go

### Vet
```bash
go vet ./...
```

### Lint
```bash
golangci-lint run
```

### パターン検索
```bash
# TODO コメント
grep -r "TODO:\|FIXME:" --include="*.go"

# panic
grep -r "panic(" --include="*.go"
```

## 共通パターン検索

### デバッグコード検出
```bash
# 言語別デバッグ関数
grep -rE "(console\.log|print\(|Debug\.WriteLine|println!|fmt\.Println)" \
  --include="*.ts" --include="*.tsx" --include="*.py" \
  --include="*.dart" --include="*.rs" --include="*.cs" --include="*.go"
```

### TODOコメント検出
```bash
grep -rE "(TODO|FIXME|HACK|XXX):" \
  --include="*.ts" --include="*.tsx" --include="*.py" \
  --include="*.dart" --include="*.rs" --include="*.cs" --include="*.go"
```

### 非推奨API検出
```bash
grep -rE "@deprecated|@Deprecated|deprecated!" \
  --include="*.ts" --include="*.tsx" --include="*.py" \
  --include="*.dart" --include="*.rs" --include="*.cs" --include="*.go"
```

## コードメトリクス

### ファイル数とコード行数
```bash
# ファイル数
find . -name "*.ts" -o -name "*.tsx" | wc -l

# コード行数（コメント・空行除く）
find . -name "*.ts" -o -name "*.tsx" | xargs cat | grep -v "^\s*$" | grep -v "^\s*//" | wc -l
```

### 重複コード検出
```bash
# jscpdを使用（Node.js）
npx jscpd .

# 手動検索（同じ行が複数回出現）
find . -name "*.ts" | xargs -I {} sh -c 'sort {} | uniq -d'
```
