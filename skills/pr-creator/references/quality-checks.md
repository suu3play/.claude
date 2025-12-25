# コード品質チェック詳細

プロジェクトタイプごとの詳細なチェックコマンドと設定方法。

## TypeScript/Node.js

### 型チェック
```bash
npx tsc --noEmit
echo "✅ 型チェック: 成功"
```

### Lint
```bash
npm run lint
echo "✅ Lint: 成功"
```

### ビルド
```bash
npm run build
echo "✅ ビルド: 成功"
```

### テスト（存在する場合）
```bash
npm test
echo "✅ テスト: 成功"
```

## Python

### 型チェック
```bash
mypy .
echo "✅ 型チェック: 成功"
```

### Lint
```bash
ruff check .
pylint **/*.py
echo "✅ Lint: 成功"
```

### フォーマットチェック
```bash
black --check .
echo "✅ フォーマット: 成功"
```

### テスト
```bash
pytest
echo "✅ テスト: 成功"
```

## Flutter/Dart

### 解析
```bash
flutter analyze
echo "✅ 解析: 成功"
```

### フォーマットチェック
```bash
dart format --set-exit-if-changed .
echo "✅ フォーマット: 成功"
```

### テスト
```bash
flutter test
echo "✅ テスト: 成功"
```

### ビルド
```bash
flutter build apk --debug
echo "✅ ビルド: 成功"
```

## Rust

### チェック
```bash
cargo check
echo "✅ チェック: 成功"
```

### Clippy
```bash
cargo clippy -- -D warnings
echo "✅ Clippy: 成功"
```

### フォーマットチェック
```bash
cargo fmt --check
echo "✅ フォーマット: 成功"
```

### テスト
```bash
cargo test
echo "✅ テスト: 成功"
```

### ビルド
```bash
cargo build
echo "✅ ビルド: 成功"
```

## C#/.NET

### ビルド
```bash
dotnet build
echo "✅ ビルド: 成功"
```

### フォーマットチェック
```bash
dotnet format --verify-no-changes
echo "✅ フォーマット: 成功"
```

### テスト
```bash
dotnet test
echo "✅ テスト: 成功"
```

## Go

### Vet
```bash
go vet ./...
echo "✅ Vet: 成功"
```

### Lint
```bash
golangci-lint run
echo "✅ Lint: 成功"
```

### テスト
```bash
go test ./...
echo "✅ テスト: 成功"
```

### ビルド
```bash
go build ./...
echo "✅ ビルド: 成功"
```

## 品質チェックのカスタマイズ

プロジェクトルートに `.claude/pr-check-config.json` を配置してカスタマイズ可能:

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
