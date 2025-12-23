---
name: documentation-generator
description: ドキュメントを自動生成・更新するスキル。設計書、API仕様書、コンポーネントカタログ等を作成。「ドキュメント生成」「設計書更新」「API仕様書作成」と依頼された時に使用
---

# Documentation Generator - ドキュメント自動生成スキル

このスキルは、コードベースを分析し、各種ドキュメントを自動的に生成・更新します。

## 使用タイミング

以下のいずれかの表現でドキュメント生成を依頼された時に自動的に起動します：

- 「ドキュメント生成」「ドキュメント作成」
- 「設計書更新」「設計書を更新」
- 「API仕様書作成」「API ドキュメント生成」
- 「README更新」（明示的な指示の場合のみ）

## 実行フロー

### ステップ1: ドキュメント種類の確認

1. **ユーザーに種類を確認**
   - 設計書（DESIGN.md）
   - API仕様書
   - README.md
   - コンポーネントカタログ
   - その他

2. **既存ドキュメントの確認**
   - 既存ファイルがある場合: 更新モード
   - ない場合: 新規作成モード

### ステップ2: コードベースの分析

#### 設計書（DESIGN.md）の場合

1. **プロジェクト構造の分析**
   ```bash
   # ディレクトリ構成
   tree src/ -L 3

   # ファイル数・行数
   find src/ -name "*.ts" -o -name "*.tsx" | wc -l
   ```

2. **依存関係の分析**
   ```bash
   # package.json の読み込み
   cat package.json
   ```

3. **主要機能の特定**
   - src/components/ 配下のコンポーネント
   - src/services/ 配下のサービス
   - src/hooks/ 配下のカスタムフック
   - src/utils/ 配下のユーティリティ

4. **型定義の抽出**
   - インターフェース定義
   - エンティティ定義
   - データモデル

#### API仕様書の場合

1. **エンドポイントの検出**
   - Express/Fastify ルート定義
   - ASP.NET Core コントローラー
   - API ルートファイル

2. **リクエスト/レスポンスの型抽出**
   - 型定義ファイル
   - バリデーションスキーマ

3. **認証・認可の確認**
   - 認証ミドルウェア
   - 認可ロジック

### ステップ3: ドキュメント生成

#### パターン1: 設計書（DESIGN.md）の生成

`.claude/templates/design-template.md` と `.claude/rules/documentation-standards.md` に従って生成：

**生成される構成**:
```markdown
# [プロジェクト名] 設計書

最終更新: 2025-01-28

## 概要

プロジェクトの目的、主要機能、対象ユーザー

## アーキテクチャ

### システム構成
- フロントエンド: React 18 + TypeScript
- ビルドツール: Vite
- 状態管理: Context API
- ルーティング: React Router v6

### ディレクトリ構成
[自動生成されたディレクトリツリー]

## データモデル

[型定義ファイルから抽出]

## 機能一覧

### 実装済み機能
[コンポーネント・サービスファイルから抽出]

## 状態管理

[Context/Store ファイルから抽出]

## パフォーマンス考慮事項

[React.memo、useMemo等の使用状況]

## セキュリティ考慮事項

[認証・バリデーション機能の確認]

## テスト戦略

[テストファイルの存在とカバレッジ]

## デプロイメント

[package.json の scripts と環境変数]
```

#### パターン2: API仕様書（OpenAPI形式）の生成

```yaml
openapi: 3.0.0
info:
  title: [プロジェクト名] API
  version: 1.0.0
  description: [プロジェクト概要]

servers:
  - url: https://api.example.com
    description: 本番環境
  - url: http://localhost:3000
    description: ローカル開発

paths:
  /users:
    get:
      summary: ユーザー一覧取得
      tags:
        - Users
      security:
        - bearerAuth: []
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
        '401':
          description: 未認証

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
          format: email

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

#### パターン3: README.md の更新

`.claude/rules/documentation-standards.md` に従い、ユーザーの明示的な指示がある場合のみ更新：

**更新される項目**:
- セットアップ手順
- 使用方法（開発サーバー、ビルド、テスト）
- プロジェクト構成
- 依存関係の最新化

### ステップ4: 設計書の自動更新（機能追加時）

`.claude/rules/documentation-standards.md`の自動更新ルールに従う：

#### 更新条件1: 新規機能追加時

**検出方法**:
- 新規コンポーネント/サービスファイル
- 新規APIエンドポイント
- 新規データモデル

**更新内容**:
```markdown
## 機能一覧

### 実装済み機能

#### [新規] ユーザープロフィール編集機能
- **概要**: ユーザーが自分のプロフィール情報を編集できる機能
- **実装場所**: `src/components/features/profile/`
- **主要なファイル**:
  - `ProfileEditor.tsx` - プロフィール編集UI
  - `useProfile.ts` - プロフィール管理フック
- **依存関係**: User認証機能、APIサービス
- **状態管理**: Context API
```

#### 更新条件2: アーキテクチャ変更時

**検出方法**:
- package.jsonの主要な依存関係変更
- ディレクトリ構造の変更
- 状態管理方法の変更

**更新内容**:
```markdown
## アーキテクチャ

### システム構成
- 状態管理: Context API → Zustand に変更（2025-01-28）
  - 理由: グローバル状態の管理が複雑化したため
  - 影響: 既存のContext実装を段階的に移行中
```

#### 更新条件3: セキュリティ対策実装時

**検出方法**:
- 認証・認可ロジックの追加
- バリデーション機能の追加
- セキュリティライブラリの導入

**更新内容**:
```markdown
## セキュリティ考慮事項

### XSS対策（追加: 2025-01-28）
- DOMPurify を導入
- ユーザー入力のHTMLをサニタイズ
- dangerouslySetInnerHTML の使用を制限
```

### ステップ5: ドキュメントの品質チェック

1. **整合性チェック**
   - コードとドキュメントの矛盾がないか
   - リンク切れがないか
   - 古い情報が残っていないか

2. **完全性チェック**
   - 必須セクションがすべて含まれているか
   - 主要機能がすべてドキュメント化されているか

3. **最終更新日の更新**
   - ドキュメント冒頭の日付を更新

### ステップ6: ユーザーへの報告

1. **生成/更新結果の表示**
   ```
   📝 ドキュメント生成完了

   生成ファイル: docs/DESIGN.md
   更新内容:
   - 新規機能「ユーザープロフィール編集」を追加
   - アーキテクチャセクションを更新（状態管理変更）
   - 最終更新日を更新

   次のステップ:
   1. docs/DESIGN.md を確認
   2. 必要に応じて手動で調整
   3. コミットして共有
   ```

## 使用例

### 例1: 新規プロジェクトの設計書作成

**ユーザー**: このプロジェクトの設計書を作成して

**スキルの動作**:
1. プロジェクト構造を分析
2. package.json から技術スタックを抽出
3. src/ 配下のファイルを分析
4. docs/DESIGN.md を生成
5. 以下の内容を含む:
   - 概要（package.jsonから）
   - アーキテクチャ（使用技術）
   - ディレクトリ構成
   - 実装済み機能（10件検出）
   - データモデル（5つのインターフェース）

### 例2: 機能追加後の設計書自動更新

**状況**: ユーザーが「通知機能」を実装して機能追加

**スキルの自動動作**（`.claude/rules/documentation-standards.md`に従う）:
1. 新規ファイル検出:
   - `src/components/notifications/`
   - `src/services/notificationService.ts`
   - `src/hooks/useNotifications.ts`
2. docs/DESIGN.md を自動更新:
   - 「機能一覧」セクションに追加
   - 「データモデル」に Notification 型を追加
   - 最終更新日を更新
3. ユーザーに報告

### 例3: API仕様書の生成

**ユーザー**: API仕様書を OpenAPI 形式で作成して

**スキルの動作**:
1. src/routes/ または src/controllers/ を分析
2. エンドポイント検出: 15件
3. リクエスト/レスポンス型を抽出
4. 認証方式を確認（JWT）
5. docs/api/openapi.yaml を生成
6. Swagger UI で表示可能な形式

## ドキュメント種類別の対応

### 1. 設計書（DESIGN.md）

**生成タイミング**:
- 新規プロジェクト作成時（自動）
- 機能追加時（自動更新）
- リファクタリング時（自動更新）

**テンプレート**: `.claude/templates/design-template.md`

### 2. README.md

**生成タイミング**:
- 新規プロジェクト作成時のみ（自動）
- ユーザーの明示的な指示時のみ（手動）

**注意**: 自動更新しない（`.claude/rules/documentation-standards.md`）

### 3. API仕様書

**生成タイミング**:
- ユーザーの指示時（手動）
- APIエンドポイント追加時（提案）

**形式**: OpenAPI 3.0 / Markdown

### 4. コンポーネントカタログ

**生成タイミング**:
- ユーザーの指示時（手動）

**形式**: Storybook / Markdown

### 5. CHANGELOG.md

**生成タイミング**:
- バージョン更新時（手動）

**形式**: Keep a Changelog

## 注意事項

1. **自動更新のルールを遵守**
   - `.claude/rules/documentation-standards.md` に従う
   - READMEは明示的な指示がない限り更新しない
   - 設計書は変更のたびに自動更新

2. **既存情報の保護**
   - 手動で追加された情報を上書きしない
   - 更新時は既存セクションとマージ

3. **最終更新日の記録**
   - ドキュメント冒頭の日付を必ず更新

4. **リンクの整合性**
   - 内部リンクが正しいか確認
   - 存在しないファイルへのリンクを作らない

5. **図表の活用**
   - 複雑な構成はMermaid記法で図示
   - アーキテクチャ図、データフロー図等

## 関連ファイル

- `.claude/rules/documentation-standards.md` - ドキュメント作成基準
- `.claude/templates/design-template.md` - 設計書テンプレート
- `.claude/rules/code-quality-standards.md` - コード品質基準

## 拡張可能性

1. **自動図表生成**: Mermaid図の自動生成
2. **多言語対応**: 英語版ドキュメントの自動生成
3. **バージョン管理**: ドキュメントの変更履歴追跡
4. **差分ハイライト**: 更新箇所を明示
5. **AI要約**: 長文ドキュメントの要約生成
