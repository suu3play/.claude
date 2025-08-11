# テンプレートコピーコマンド

## 概要

.claude プロジェクトの標準 issue テンプレートを指定されたプロジェクトまたは全プロジェクトにコピーするスラッシュコマンド

## 実行手順

1. **対象プロジェクト確認**

    - 個別指定: 指定プロジェクトのディレクトリ存在確認
    - all 指定: 作業ディレクトリ配下を自動スキャンしてプロジェクト一覧を取得
    - プロジェクトタイプの自動判定（package.json, \*.csproj 等から判定）
    - Git リポジトリ状態の確認

2. **テンプレート配置**

    - `.github/ISSUE_TEMPLATE/` ディレクトリを作成
    - .claude の標準テンプレートをコピー

3. **Git 管理追加**
    - 作成したテンプレートを git add で管理下に追加
    - コミット準備完了状態にする

## 使用方法

### 個別プロジェクトへの適用

```
/copy-templates [プロジェクト名] [プロジェクトタイプ]
```

### 全プロジェクトへの一括適用

```
/copy-templates all
```

※all 指定時は各プロジェクトのタイプを自動判定して適切なテンプレートを適用

### プロジェクトタイプ

-   `web`: 汎用 Web アプリケーション
-   `react`: React/TypeScript/Vite ベースのプロジェクト
-   `desktop`: WPF/.NET 等のデスクトップアプリケーション
-   `mobile`: モバイルアプリケーション
-   `api`: Web API/マイクロサービス
-   `cli`: コマンドラインツール
-   `question`: 質問・相談テンプレートを含む汎用設定

## 実行例

### 個別適用

```
/copy-templates source-flow desktop
/copy-templates portfolio web
/copy-templates hobby-weather react
/copy-templates finder-scope desktop
/copy-templates .claude question
```

### 一括適用

```
/copy-templates all
```

上記コマンドは作業ディレクトリ（`D:\自己開発`）配下の全プロジェクトに自動判定されたタイプでテンプレートを適用します。
対象プロジェクトとタイプは実行時に自動検出されます。

## 自動カスタマイズ内容

### Web (`web`)

-   環境情報：Chrome, Firefox, Safari, Edge, iPhone, Android
-   技術考慮事項：ブラウザ互換性、レスポンシブ対応

### React (`react`)

-   環境情報：Chrome, Firefox, Safari, Edge, Node.js, TypeScript
-   技術考慮事項：React パフォーマンス、TSX 型安全性、Vite ビルド最適化

### Desktop (`desktop`)

-   環境情報：Windows 10/11, .NET 版本, Visual Studio
-   技術考慮事項：OS 互換性、フレームワーク依存

### Mobile (`mobile`)

-   環境情報：iOS 版本, Android 版本, デバイス情報
-   技術考慮事項：デバイス固有機能、パフォーマンス

### API (`api`)

-   環境情報：サーバー環境、データベース、負荷状況
-   技術考慮事項：スケーラビリティ、セキュリティ

### CLI (`cli`)

-   環境情報：OS、シェル、ランタイム版本
-   技術考慮事項：クロスプラットフォーム対応

### Question (`question`)

-   環境情報：技術スタック、開発環境、プロジェクト規模
-   技術考慮事項：実装方法、アーキテクチャ設計、学習リソース

## 標準テンプレート構成

-   日本語ラベル体系との完全連携
-   受け入れ条件・技術考慮事項セクション標準装備
-   プロジェクトタイプ別の適切なカスタマイズ

## 注意事項

-   .claude が標準テンプレート管理プロジェクト
-   既存テンプレートは上書きされる
-   作成後は必要に応じて git commit を実行
-   プロジェクト自動判定の詳細は `templates/project-detection.md` を参照

### all 引数使用時の特別な注意

-   **自動検出**: 作業ディレクトリ配下のディレクトリを動的にスキャン
-   **プロジェクトタイプ自動判定**: package.json、\*.csproj、技術スタックから自動判定
-   **除外ディレクトリ**: node_modules, dist, .git 等は自動で除外
-   **実行時間**: 複数プロジェクトへの適用のため時間がかかります
-   **エラー処理**: 一部プロジェクトで失敗しても他のプロジェクトは継続処理
-   **上書き確認**: 全プロジェクトのテンプレートが上書きされることを確認

### プロジェクト自動検出の流れ

```bash
# 1. 作業ディレクトリ配下をスキャン
WORKING_DIR="D:/自己開発"
for dir in "$WORKING_DIR"/*; do
    if [[ -d "$dir" ]]; then
        # プロジェクトタイプを判定
        PROJECT_TYPE=$(detect_project_type "$dir")
        if [[ "$PROJECT_TYPE" != "unknown" ]]; then
            # タイプ別テンプレート適用処理
        fi
    fi
done
```

### プロジェクトタイプ自動判定ルール

-   **react**: package.json に react 依存関係または vite.config.ts 存在
-   **web**: package.json 存在かつ react 以外の Web 技術
-   **desktop**: \*.csproj ファイル存在
-   **question**: .claude 等の設定・ドキュメントプロジェクト
-   **api**: サーバーサイド関連の依存関係検出
-   **cli**: package.json の bin フィールドや CLI 関連ファイル検出

詳細な判定ロジックは `templates/project-detection.md` を参照してください。
