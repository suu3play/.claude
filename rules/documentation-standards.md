# ドキュメント作成基準

## 基本方針

-   **作成タイミング**: 新規プロジェクト作成時のみREADME.mdを自動作成
-   **更新方針**: 既存のドキュメントは、ユーザーの明示的な指示がない限り更新しない
-   **生成ツール名の禁止**: いかなるドキュメントにもClaudeなど生成ツール名を記載しないこと

## README.md 作成基準

### 新規プロジェクト作成時

プロジェクト作成時には、以下の情報を含むREADME.mdを自動生成すること：

1. **プロジェクト名と概要**
   - プロジェクトの目的と機能を簡潔に説明
   - 主要な技術スタックを明記

2. **セットアップ手順**
   - 必要な環境・ツールのバージョン
   - インストール手順（依存関係のインストール）
   - 環境変数の設定（機密情報は含めない）

3. **使用方法**
   - 開発サーバーの起動方法
   - ビルド方法
   - テスト実行方法

4. **プロジェクト構成**（必要に応じて）
   - 主要なディレクトリ構成
   - 重要なファイルの説明

5. **ライセンス**（必要に応じて）

### 既存プロジェクトのREADME更新

-   ユーザーが明示的に「READMEを更新して」「ドキュメントを更新して」と指示した場合のみ更新
-   自動的な更新は行わない

## コード内コメント基準

### コメントを記述すべき場合

-   **複雑なロジック**: アルゴリズムやビジネスロジックが複雑な場合
-   **回避策（Workaround）**: 特定の問題を回避するための処理
-   **パフォーマンス最適化**: 最適化のために可読性を犠牲にしている箇所
-   **外部依存**: APIの仕様やライブラリの動作に依存している箇所
-   **型定義**: 複雑な型定義やジェネリクスの説明

### コメントを記述すべきでない場合

-   **自明な処理**: コードを読めば明らかな内容
-   **変数名・関数名で説明できる内容**: 適切な命名で十分説明できる場合
-   **コードの繰り返し**: コードと同じ内容をコメントで繰り返す

### コメントの記述形式

#### Python
```python
def calculate_total_cost(items: list[Item]) -> Decimal:
    """商品リストから合計金額を計算する。

    Args:
        items: 商品リスト

    Returns:
        税込み合計金額
    """
    # 消費税率を10%として計算（軽減税率は考慮しない）
    subtotal = sum(item.price for item in items)
    return subtotal * Decimal('1.10')
```

#### TypeScript/React
```typescript
/**
 * ユーザー情報を取得する
 * @param userId - ユーザーID
 * @returns ユーザー情報
 * @throws {NotFoundError} ユーザーが存在しない場合
 */
async function fetchUser(userId: string): Promise<User> {
  // キャッシュから取得を試みる（APIコール削減のため）
  const cached = cache.get(userId);
  if (cached) return cached;

  const user = await api.getUser(userId);
  cache.set(userId, user);
  return user;
}
```

#### C#
```csharp
/// <summary>
/// 商品の在庫を更新する
/// </summary>
/// <param name="productId">商品ID</param>
/// <param name="quantity">変更数量（負の値で減少）</param>
/// <returns>更新後の在庫数</returns>
/// <exception cref="InvalidOperationException">在庫がマイナスになる場合</exception>
public async Task<int> UpdateStockAsync(int productId, int quantity)
{
    // トランザクション内で在庫を更新（競合状態を防ぐため）
    using var transaction = await _context.Database.BeginTransactionAsync();
    // ... 実装
}
```

## API ドキュメント

### REST API

-   OpenAPI (Swagger) 形式でのドキュメント作成を推奨
-   各エンドポイントには以下を記載：
    -   URL、HTTPメソッド
    -   リクエストパラメータ（型、必須/任意、説明）
    -   レスポンス形式（成功時、エラー時）
    -   認証要件
    -   使用例

### GraphQL API

-   スキーマ定義にコメントを記述
-   複雑なクエリには使用例を提供

## 変更履歴（CHANGELOG）

### 記述タイミング

-   バージョン更新時に必ず更新
-   Keep a Changelog 形式に従う

### 記述内容

```markdown
## [1.2.0] - 2025-01-28

### Added
- 新機能の説明

### Changed
- 既存機能の変更内容

### Fixed
- 修正したバグの説明

### Deprecated
- 非推奨となった機能

### Removed
- 削除された機能

### Security
- セキュリティ関連の修正
```

## プロジェクト固有ドキュメント

### アーキテクチャドキュメント

大規模プロジェクトでは以下のドキュメントを作成することを推奨：

-   **アーキテクチャ概要**: システム全体の構成
-   **データモデル**: ER図、スキーマ定義
-   **API設計**: エンドポイント一覧、認証フロー
-   **デプロイメント**: インフラ構成、CI/CD

### 意思決定記録（ADR: Architecture Decision Records）

重要な設計判断は記録として残すことを推奨：

```markdown
# ADR-001: 状態管理にContext APIを採用

## 状況
複数コンポーネント間で状態を共有する必要がある

## 決定
Redux ではなく React Context API を採用

## 理由
- プロジェクト規模が小さく、Reduxは過剰
- ボイラープレートコードを削減
- React標準機能で学習コストが低い

## 結果
- コード量が削減された
- 新規メンバーの学習が容易になった
```

## ドキュメントの配置場所

-   **README.md**: プロジェクトルート
-   **CHANGELOG.md**: プロジェクトルート
-   **API ドキュメント**: `docs/api/` または OpenAPI YAMLファイル
-   **アーキテクチャドキュメント**: `docs/architecture/`
-   **ADR**: `docs/adr/` または `docs/decisions/`
-   **開発ガイド**: `docs/development/`

## 禁止事項

1. **生成ツール名の記載禁止**
   - README、コメント、コミットメッセージ等すべてのドキュメントに適用
   - 「Claudeで生成」「AI生成」などの記載は一切禁止

2. **過度な自動更新**
   - ユーザーの明示的な指示なしにドキュメントを更新しない
   - 機能追加時に自動でREADMEを更新しない

3. **不正確な情報**
   - コードと矛盾する情報を記載しない
   - 未実装の機能を記載しない
   - 古い情報を放置しない（更新時に注意）
