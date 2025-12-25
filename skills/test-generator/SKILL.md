---
name: test-generator
description: 関数・コンポーネントのテストコードを自動生成するスキル。「テスト生成」「テストを追加」「テストコード作成」と依頼された時に使用
---

# Test Generator - テスト自動生成スキル

このスキルは、関数やコンポーネントを分析し、適切なテストケースを自動的に生成します。

## 使用タイミング

以下のいずれかの表現でテスト生成を依頼された時に自動的に起動します：

- 「テスト生成」「テストを生成」
- 「テストを追加」「テスト追加」
- 「テストコード作成」「テストコード書いて」

## 実行フロー

### ステップ1: 対象コードの確認

1. **ユーザーに対象を確認**
   - 特定のファイル/関数が指定されている場合: そのまま使用
   - 指定がない場合: 最近変更されたファイルを提案

2. **対象コードの読み込み**
   - ファイル全体を読み込み
   - 関数・コンポーネントを抽出
   - 型定義を確認

### ステップ2: テストケースの分析

1. **関数の分析**
   - 入力パラメータの型と個数
   - 戻り値の型
   - 例外が throw されるか
   - 副作用があるか（API呼び出し、状態変更等）

2. **テストケースの設計**
   - 正常系テスト
   - 異常系テスト（エッジケース）
   - 境界値テスト
   - エラーケーステスト

### ステップ3: テストコードの生成

#### TypeScript/React の場合

**フレームワーク選択**:
- ユニットテスト: Vitest
- コンポーネントテスト: React Testing Library

**テスト構成**:
```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { [対象] } from './[ファイル名]';

describe('[関数/コンポーネント名]', () => {
  // 正常系テスト
  it('正常に動作する', () => {
    // テストロジック
  });

  // 異常系テスト
  it('null/undefinedの場合にエラーを投げる', () => {
    // テストロジック
  });

  // エッジケーステスト
  it('空配列の場合に空の結果を返す', () => {
    // テストロジック
  });
});
```

#### Python の場合

**フレームワーク**: pytest

**テスト構成**:
```python
import pytest
from [モジュール名] import [関数名]

class Test[関数名]:
    """[関数名]のテストクラス"""

    def test_正常系(self):
        """正常に動作することを確認"""
        # テストロジック
        assert result == expected

    def test_異常系_None(self):
        """Noneを渡すとValueErrorが発生することを確認"""
        with pytest.raises(ValueError):
            [関数名](None)

    def test_境界値_空リスト(self):
        """空リストの場合に空の結果を返すことを確認"""
        # テストロジック
```

### ステップ4: モックの生成

**外部依存がある場合**:

1. **API呼び出しのモック**
   ```typescript
   vi.mock('./api', () => ({
     fetchUser: vi.fn().mockResolvedValue({ id: 1, name: 'Test User' })
   }));
   ```

2. **ローカルストレージのモック**
   ```typescript
   const mockLocalStorage = {
     getItem: vi.fn(),
     setItem: vi.fn(),
   };
   global.localStorage = mockLocalStorage as any;
   ```

3. **日時のモック**
   ```typescript
   vi.setSystemTime(new Date('2025-01-01'));
   ```

### ステップ5: テストファイルの配置

1. **ファイル名の決定**
   - TypeScript/React: `[元ファイル名].test.ts` または `[元ファイル名].spec.ts`
   - Python: `test_[元ファイル名].py`

2. **配置場所の決定**
   - プロジェクトの既存パターンに従う
   - 一般的なパターン:
     - `__tests__/` ディレクトリ
     - ソースファイルと同じディレクトリ
     - `tests/` ディレクトリ

### ステップ6: テストの実行と確認

1. **テスト実行**
   ```bash
   # TypeScript
   npm test [テストファイル名]

   # Python
   pytest tests/test_[ファイル名].py -v
   ```

2. **結果の確認**
   - すべてのテストがパスしているか
   - カバレッジは適切か
   - 実行時間は許容範囲か

### ステップ7: ユーザーへの報告

1. **生成したテストの概要を表示**
   ```
   ✅ テスト生成完了

   対象: src/utils/calculator.ts
   生成ファイル: src/utils/calculator.test.ts

   テストケース: 12件
   - 正常系: 5件
   - 異常系: 4件
   - エッジケース: 3件

   テスト実行結果: ✅ 12/12 passed
   カバレッジ: 95%
   ```

## テスト生成パターン

### パターン1: ユーティリティ関数

**対象コード**:
```typescript
export function calculateTotal(prices: number[]): number {
  if (!Array.isArray(prices)) {
    throw new Error('prices must be an array');
  }
  return prices.reduce((sum, price) => sum + price, 0);
}
```

**生成されるテスト**:
```typescript
describe('calculateTotal', () => {
  it('正常に合計を計算する', () => {
    expect(calculateTotal([100, 200, 300])).toBe(600);
  });

  it('空配列の場合は0を返す', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('配列でない場合はエラーを投げる', () => {
    expect(() => calculateTotal(null as any)).toThrow('prices must be an array');
  });

  it('負の数を含む場合も正しく計算する', () => {
    expect(calculateTotal([100, -50, 200])).toBe(250);
  });
});
```

### パターン2: Reactコンポーネント

**対象コード**:
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ label, onClick, disabled }) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
};
```

**生成されるテスト**:
```typescript
describe('Button', () => {
  it('ラベルが正しく表示される', () => {
    render(<Button label="Click me" onClick={() => {}} />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('クリック時にonClickが呼ばれる', () => {
    const handleClick = vi.fn();
    render(<Button label="Click me" onClick={handleClick} />);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('disabledの場合はクリックできない', () => {
    const handleClick = vi.fn();
    render(<Button label="Click me" onClick={handleClick} disabled />);
    const button = screen.getByText('Click me');
    expect(button).toBeDisabled();
    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });
});
```

### パターン3: 非同期関数

**対象コード**:
```typescript
export async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error('User not found');
  }
  return response.json();
}
```

**生成されるテスト**:
```typescript
describe('fetchUser', () => {
  it('正常にユーザーを取得する', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ id: '1', name: 'Test User' })
    });

    const user = await fetchUser('1');
    expect(user).toEqual({ id: '1', name: 'Test User' });
    expect(fetch).toHaveBeenCalledWith('/api/users/1');
  });

  it('ユーザーが見つからない場合はエラーを投げる', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false
    });

    await expect(fetchUser('999')).rejects.toThrow('User not found');
  });
});
```

## テストケース設計のポイント

### 1. 正常系テスト

- 典型的な入力値での動作確認
- 期待される戻り値の検証
- 副作用（状態変更、API呼び出し）の確認

### 2. 異常系テスト

- null/undefined の処理
- 型エラー
- 例外が正しく throw されるか

### 3. 境界値テスト

- 空配列/空文字列
- 最大値/最小値
- 0や負の数

### 4. エッジケーステスト

- 非常に大きな配列
- 特殊文字を含む文字列
- タイムアウト

## 使用例

### 例1: 既存の関数にテストを追加

**ユーザー**: src/utils/validator.ts にテストを追加して

**スキルの動作**:
1. validator.ts を読み込み
2. 5つの関数を発見
3. 各関数を分析してテストケースを設計
4. tests/utils/validator.test.ts を生成
5. テスト実行: 25/25 passed
6. カバレッジ: 92%

### 例2: 新規作成したコンポーネントのテスト

**ユーザー**: UserProfile コンポーネントのテストを生成

**スキルの動作**:
1. UserProfile.tsx を読み込み
2. Props、状態、イベントハンドラーを分析
3. レンダリングテスト、インタラクションテストを設計
4. UserProfile.test.tsx を生成
5. テスト実行: 8/8 passed

## 注意事項

1. **既存のテストとの重複確認**
   - テストファイルが既に存在する場合は確認
   - 既存テストを上書きせず、追加のみ

2. **プロジェクトのテスト規約に従う**
   - 既存のテストファイルのパターンを参考にする
   - 命名規則、ファイル配置を統一

3. **モックの適切な使用**
   - 外部依存は必ずモック化
   - モックが複雑になりすぎないよう注意

4. **テストの保守性**
   - 読みやすいテストコードを生成
   - 適切なテスト名（何をテストしているか明確）

5. **カバレッジの確認**
   - 生成後にカバレッジを確認
   - 重要なパスが網羅されているか検証

## 関連ファイル

- `.claude/rules/testing-requirements.md` - テスト要件
- `.claude/rules/code-quality-standards.md` - コード品質基準

## 拡張可能性

1. **スナップショットテスト**: UIコンポーネントのスナップショット生成
2. **E2Eテスト生成**: Playwright/Cypress のテスト生成
3. **カバレッジ分析**: 不足しているテストケースの検出
4. **ミューテーションテスト**: テストの有効性検証
