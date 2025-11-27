---
name: refactor-assistant
description: コードのリファクタリングを支援するスキル。重複検出、複雑度分析、改善案提示を行う。「リファクタリング」「コード改善」「リファクタして」と依頼された時に使用
---

# Refactor Assistant - リファクタリング支援スキル

このスキルは、コードを分析し、リファクタリングの必要性を検出して改善案を提示します。

## 使用タイミング

以下のいずれかの表現でリファクタリング依頼された時に自動的に起動します：

- 「リファクタリング」「リファクタして」
- 「コード改善」「コードを改善」
- 「重複コード検出」「コード最適化」

## 実行フロー

### ステップ1: リファクタリング対象の確認

1. **対象の特定**
   - ファイル/ディレクトリ指定がある場合: そのまま使用
   - 指定がない場合: 最近変更されたファイルを提案

2. **対象コードの読み込み**
   - 対象ファイル群を読み込み
   - コード構造を解析

### ステップ2: コード分析

#### 1. 重複コード検出

**検出対象**:
- 完全一致する関数・ブロック
- 類似度の高いコード（80%以上）
- コピー&ペーストされたコード

**分析方法**:
```typescript
// 重複例
function calculateUserTotal(user: User): number {
  const base = user.amount * 1.1;
  const discount = base * 0.05;
  return base - discount;
}

function calculateAdminTotal(admin: Admin): number {
  const base = admin.amount * 1.1;
  const discount = base * 0.05;
  return base - discount;
}

// 改善案
function calculateTotal(amount: number): number {
  const base = amount * 1.1;
  const discount = base * 0.05;
  return base - discount;
}
```

#### 2. 複雑度分析

**Cyclomatic Complexity（循環的複雑度）の計算**:
- 分岐（if, switch, ?: 等）の数
- ループ（for, while 等）の数
- 論理演算子（&&, || 等）の数

**複雑度の目安**:
- 1-10: シンプル（問題なし）
- 11-20: やや複雑（要注意）
- 21-50: 複雑（リファクタリング推奨）
- 51+: 非常に複雑（即座にリファクタリング必要）

#### 3. 長すぎる関数/クラスの検出

**基準**:
- 関数: 30行以上（推奨: 20行以内）
- クラス: 300行以上（推奨: 200行以内）
- ネストの深さ: 4レベル以上（推奨: 3レベル以内）

#### 4. その他のコード臭

- **Large Class**: 責務が多すぎるクラス
- **Long Parameter List**: パラメータが多すぎる（5個以上）
- **Feature Envy**: 他クラスのメソッドを多用
- **Data Clumps**: 同じデータの組み合わせが複数箇所に
- **Primitive Obsession**: プリミティブ型の過度な使用

### ステップ3: リファクタリング案の作成

#### パターン1: Extract Function（関数の抽出）

**Before**:
```typescript
function processOrder(order: Order): void {
  // 合計計算
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  const tax = total * 0.1;
  total += tax;

  // 割引適用
  if (order.couponCode) {
    const discount = total * 0.1;
    total -= discount;
  }

  order.total = total;
}
```

**After**:
```typescript
function processOrder(order: Order): void {
  const subtotal = calculateSubtotal(order.items);
  const total = applyDiscount(subtotal, order.couponCode);
  order.total = total;
}

function calculateSubtotal(items: OrderItem[]): number {
  const subtotal = items.reduce((sum, item) =>
    sum + item.price * item.quantity, 0
  );
  return subtotal * 1.1; // 税込み
}

function applyDiscount(amount: number, couponCode?: string): number {
  if (!couponCode) return amount;
  return amount * 0.9; // 10%割引
}
```

#### パターン2: Replace Conditional with Polymorphism

**Before**:
```typescript
function calculateShippingCost(order: Order): number {
  if (order.shippingType === 'standard') {
    return order.weight * 100;
  } else if (order.shippingType === 'express') {
    return order.weight * 200;
  } else if (order.shippingType === 'overnight') {
    return order.weight * 500;
  }
  return 0;
}
```

**After**:
```typescript
interface ShippingStrategy {
  calculate(weight: number): number;
}

class StandardShipping implements ShippingStrategy {
  calculate(weight: number): number {
    return weight * 100;
  }
}

class ExpressShipping implements ShippingStrategy {
  calculate(weight: number): number {
    return weight * 200;
  }
}

class OvernightShipping implements ShippingStrategy {
  calculate(weight: number): number {
    return weight * 500;
  }
}

function calculateShippingCost(order: Order, strategy: ShippingStrategy): number {
  return strategy.calculate(order.weight);
}
```

#### パターン3: Introduce Parameter Object

**Before**:
```typescript
function createUser(
  name: string,
  email: string,
  age: number,
  address: string,
  phone: string
): User {
  // 実装
}
```

**After**:
```typescript
interface UserInfo {
  name: string;
  email: string;
  age: number;
  address: string;
  phone: string;
}

function createUser(userInfo: UserInfo): User {
  // 実装
}
```

### ステップ4: 優先順位付け

**優先度の判定基準**:

1. **致命的（即座に対応）**
   - 循環的複雑度 50以上
   - セキュリティリスクを含む
   - パフォーマンス問題を引き起こしている

2. **重要（近日中に対応）**
   - 循環的複雑度 20-49
   - 重複コードが3箇所以上
   - 長すぎる関数（100行以上）

3. **推奨（余裕があれば対応）**
   - 循環的複雑度 11-19
   - 軽微な重複コード
   - 命名の改善

### ステップ5: リファクタリング計画の作成

1. **計画ドキュメントの生成**
   - 出力先: `./docs/refactoring/refactor_plan_yyyyMMddHHmm.md`

2. **計画の内容**
   ```markdown
   # リファクタリング計画

   作成日: YYYY-MM-DD
   対象: [ファイル/ディレクトリ名]

   ## 分析結果サマリー

   ### 重複コード
   - 検出件数: X件
   - 重複行数: XXX行

   ### 複雑度
   - 高複雑度関数: X件
   - 平均複雑度: XX

   ### コード臭
   - Long Function: X件
   - Large Class: X件
   - Long Parameter List: X件

   ## リファクタリング案

   ### 優先度: 致命的
   1. [ファイル名:関数名] - 循環的複雑度52
      - 問題: 分岐が多すぎる
      - 提案: Strategy パターンで分岐を削減
      - 影響: [関連ファイル一覧]

   ### 優先度: 重要
   2. [ファイル名] - 重複コード
      - 問題: 同じロジックが3箇所に存在
      - 提案: 共通関数を抽出
      - 影響: 軽微

   ### 優先度: 推奨
   3. [ファイル名:関数名] - 長すぎる関数
      - 問題: 80行の関数
      - 提案: 処理を3つの関数に分割
      - 影響: なし

   ## 実施手順

   1. テストの追加（リファクタリング前）
   2. 致命的な問題から順に対応
   3. 各修正後にテスト実行
   4. コードレビュー
   5. マージ

   ## 期待される効果

   - 保守性の向上
   - バグ混入リスクの低減
   - パフォーマンス改善（見込み: X%）
   - テストカバレッジ向上
   ```

### ステップ6: ユーザーへの確認

1. **分析結果の表示**
   ```
   📊 リファクタリング分析完了

   検出された問題:
   - 🔴 致命的: 2件
   - 🟡 重要: 5件
   - 🟢 推奨: 8件

   詳細は ./docs/refactoring/refactor_plan_202501281600.md を確認してください

   次のステップ:
   1. 計画を確認
   2. 「リファクタリング実行」と指示すると実施開始
   ```

### ステップ7: リファクタリング実行

ユーザーの承認後、計画に従って段階的にリファクタリングを実施：

1. **テスト追加**（リファクタリング前）
2. **1件ずつリファクタリング**
3. **テスト実行**（各修正後）
4. **コミット**（各修正後）
5. **次の項目へ**

## 使用例

### 例1: ファイル全体のリファクタリング

**ユーザー**: src/services/orderService.ts をリファクタリングして

**スキルの動作**:
1. orderService.ts を分析
2. 検出結果:
   - 循環的複雑度35の関数: 1件
   - 重複コード: 3箇所
   - 長すぎる関数: 2件
3. リファクタリング計画を作成
4. ユーザーに提示

**計画の例**:
```
優先度: 致命的
- processComplexOrder関数（複雑度35）
  → Extract Function で3つに分割

優先度: 重要
- 配送料計算の重複
  → calculateShippingCost関数を抽出

優先度: 推奨
- validateOrder関数（65行）
  → バリデーションロジックを分離
```

### 例2: プロジェクト全体の分析

**ユーザー**: src/ 配下のコードを分析してリファクタリング候補を教えて

**スキルの動作**:
1. src/ 配下の全ファイルを分析
2. 最も問題のあるファイルTop10をリストアップ
3. 統計情報を表示:
   - 平均複雑度: 12.5
   - 重複コード総数: 250行
   - 長すぎる関数: 15件
4. 優先的に対応すべきファイルを提案

## リファクタリングのベストプラクティス

### 1. テストファースト

- リファクタリング前に必ずテストを追加
- 既存のテストがすべてパスすることを確認
- リファクタリング後もテストがパスすることを確認

### 2. 小さなステップで

- 一度に大きな変更をしない
- 各ステップでテストを実行
- 各ステップでコミット

### 3. 1つずつ対応

- 複数の問題を同時に修正しない
- 1つのリファクタリングパターンを適用したらコミット

### 4. 既存の動作を変えない

- リファクタリングは動作を変えない
- 新機能追加とリファクタリングを混ぜない

### 5. コードレビュー

- リファクタリング後は必ずレビューを受ける
- チーム全体で改善パターンを共有

## 注意事項

1. **既存のテストがない場合**
   - まずテストを追加してからリファクタリング
   - テストがないままのリファクタリングは危険

2. **大規模なリファクタリング**
   - 一度に全部やらない
   - 段階的に実施
   - フィーチャーフラグの活用を検討

3. **パフォーマンスへの影響**
   - リファクタリングでパフォーマンスが低下しないか確認
   - ベンチマークテストの実施

4. **チームとの調整**
   - 大規模なリファクタリングはチームに相談
   - コンフリクトを避けるため、作業タイミングを調整

## 関連ファイル

- `.claude/rules/code-quality-standards.md` - コード品質基準
- `.claude/rules/testing-requirements.md` - テスト要件

## 拡張可能性

1. **自動リファクタリング**: 安全なパターンの自動適用
2. **技術的負債の追跡**: 時系列での負債の増減を可視化
3. **リファクタリングメトリクス**: 改善効果の定量的評価
4. **AIによる提案**: より高度なリファクタリングパターンの提案
