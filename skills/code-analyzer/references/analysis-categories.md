# コード分析カテゴリ詳細

## カテゴリ分類と優先度判定基準

### 🐛 バグ (Bug)

**定義**: 実行時エラーやビルドエラーを引き起こす問題

**検出項目**:
- ビルドエラー
- 型エラー
- null/undefined参照エラー
- 配列範囲外アクセス
- 無限ループの可能性
- 無効な再帰

**優先度**: Critical または High

**判定基準**:
- Critical: ビルド不可、実行不可、セキュリティ上の重大な欠陥
- High: 特定条件下で実行時エラー、データ損失の可能性

**例**:
```typescript
// Critical: 型エラー
const user: User = undefined; // Type 'undefined' is not assignable to type 'User'

// High: null参照の可能性
user.name.toUpperCase(); // Cannot read property 'toUpperCase' of null
```

### 🔧 リファクタリング (Refactoring)

**定義**: コードの構造や可読性を改善する変更

**検出項目**:
- コードの重複
- 長い関数（100行以上）
- 深いネスト（4階層以上）
- 命名の問題（不明瞭な変数名）
- 複雑度の高いコード（McCabe複雑度 > 10）
- マジックナンバー

**優先度**: Medium または Low

**判定基準**:
- Medium: 可読性・保守性に大きく影響
- Low: 軽微な改善提案

**例**:
```typescript
// Medium: コードの重複
function calculatePriceA() { /* 同じロジック */ }
function calculatePriceB() { /* 同じロジック */ }

// Low: マジックナンバー
if (status === 3) { /* 3の意味が不明 */ }
```

### 📝 ドキュメント (Documentation)

**定義**: ドキュメントの不足や不備

**検出項目**:
- TODOコメント
- 未ドキュメント化のAPI
- README更新
- コメント不足

**優先度**: Low

**判定基準**:
- Low: ドキュメント追加・更新が必要

**例**:
```typescript
// TODO: エラーハンドリングを追加
function processData(data: any) { }

// 未ドキュメント化
export function complexFunction() { /* コメントなし */ }
```

### ⚡ パフォーマンス (Performance)

**定義**: 実行速度やリソース使用に関する問題

**検出項目**:
- 非効率なアルゴリズム（O(n²)など）
- 不要な再レンダリング（React）
- メモリリークの可能性
- 不要なループ

**優先度**: Medium

**判定基準**:
- Medium: ユーザー体験に影響する可能性

**例**:
```typescript
// Medium: 不要な再レンダリング
function Component() {
  const data = getExpensiveData(); // 毎レンダリング実行
  return <div>{data}</div>;
}
```

### 🧪 テスト (Testing)

**定義**: テストカバレッジやテストの品質に関する問題

**検出項目**:
- テストカバレッジ不足
- テストの欠如
- テストの改善提案
- 不安定なテスト

**優先度**: Medium

**判定基準**:
- Medium: 重要な機能のテスト不足

**例**:
```typescript
// Medium: テストなし
export function criticalBusinessLogic() {
  // テストが存在しない重要な処理
}
```

### 🔒 セキュリティ (Security)

**定義**: セキュリティ上の脆弱性

**検出項目**:
- ハードコードされた認証情報
- SQLインジェクションの可能性
- XSSの脆弱性
- 不適切な権限チェック
- 暗号化されていない機密情報

**優先度**: Critical

**判定基準**:
- Critical: 即座の対応が必要

**例**:
```typescript
// Critical: ハードコードされた認証情報
const API_KEY = "sk-1234567890abcdef";

// Critical: SQLインジェクション
const query = `SELECT * FROM users WHERE name = '${userName}'`;
```

### ♿ アクセシビリティ (Accessibility)

**定義**: アクセシビリティに関する問題

**検出項目**:
- aria属性の欠如
- キーボードナビゲーション
- コントラスト比の問題
- alt属性の欠如

**優先度**: Medium

**判定基準**:
- Medium: アクセシビリティ基準への準拠

**例**:
```html
<!-- Medium: aria-label欠如 -->
<button></button>

<!-- Medium: alt属性欠如 -->
<img src="logo.png">
```

## 優先度の総合判定

### Critical
- セキュリティ上の重大な欠陥
- ビルドエラー
- 実行不可能な状態
- データ損失の可能性

### High
- 型エラー
- 実行時エラーの可能性（高）
- 主要機能の不具合

### Medium
- リファクタリング（影響範囲大）
- パフォーマンス問題
- テスト不足
- アクセシビリティ問題

### Low
- ドキュメント更新
- 軽微なリファクタリング
- コードスタイル
