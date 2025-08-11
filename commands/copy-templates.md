# テンプレートコピーコマンド

## 概要
claude-configプロジェクトの標準issueテンプレートを指定されたプロジェクトまたは全プロジェクトにコピーするスラッシュコマンド

## 実行手順

1. **対象プロジェクト確認**
   - 個別指定: 指定プロジェクトのディレクトリ存在確認
   - all指定: 作業ディレクトリ配下を自動スキャンしてプロジェクト一覧を取得
   - プロジェクトタイプの自動判定（package.json, *.csproj等から判定）
   - Gitリポジトリ状態の確認

2. **テンプレート配置**
   - `.github/ISSUE_TEMPLATE/` ディレクトリを作成
   - claude-configの標準テンプレートをコピー

3. **プロジェクト別カスタマイズ**
   - 🐛バグ報告テンプレートの環境情報をプロジェクトタイプに適応
   - 🚀新規機能・改善提案テンプレートの受け入れ条件を調整

4. **Git管理追加**
   - 作成したテンプレートをgit addで管理下に追加
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
※all指定時は各プロジェクトのタイプを自動判定して適切なテンプレートを適用

### プロジェクトタイプ
- `web`: 汎用Webアプリケーション
- `react`: React/TypeScript/Viteベースのプロジェクト
- `desktop`: WPF/.NET等のデスクトップアプリケーション  
- `mobile`: モバイルアプリケーション
- `api`: Web API/マイクロサービス
- `cli`: コマンドラインツール
- `question`: 質問・相談テンプレートを含む汎用設定

## 実行例

### 個別適用
```
/copy-templates source-flow desktop
/copy-templates portfolio web
/copy-templates hobby-weather react
/copy-templates finder-scope desktop
/copy-templates claude-config question
```

### 一括適用
```
/copy-templates all
```
上記コマンドは作業ディレクトリ（`D:\自己開発`）配下の全プロジェクトに自動判定されたタイプでテンプレートを適用します。
対象プロジェクトとタイプは実行時に自動検出されます。

## 自動カスタマイズ内容

### Web (`web`)
- 環境情報：Chrome, Firefox, Safari, Edge, iPhone, Android
- 技術考慮事項：ブラウザ互換性、レスポンシブ対応

### React (`react`)
- 環境情報：Chrome, Firefox, Safari, Edge, Node.js, TypeScript
- 技術考慮事項：Reactパフォーマンス、TSX型安全性、Viteビルド最適化

### Desktop (`desktop`) 
- 環境情報：Windows 10/11, .NET版本, Visual Studio
- 技術考慮事項：OS互換性、フレームワーク依存

### Mobile (`mobile`)
- 環境情報：iOS版本, Android版本, デバイス情報
- 技術考慮事項：デバイス固有機能、パフォーマンス

### API (`api`)
- 環境情報：サーバー環境、データベース、負荷状況  
- 技術考慮事項：スケーラビリティ、セキュリティ

### CLI (`cli`)
- 環境情報：OS、シェル、ランタイム版本
- 技術考慮事項：クロスプラットフォーム対応

### Question (`question`)
- 環境情報：技術スタック、開発環境、プロジェクト規模
- 技術考慮事項：実装方法、アーキテクチャ設計、学習リソース

## 標準テンプレート構成

- 日本語ラベル体系との完全連携
- 受け入れ条件・技術考慮事項セクション標準装備
- プロジェクトタイプ別の適切なカスタマイズ

## 注意事項

- claude-configが標準テンプレート管理プロジェクト
- 既存テンプレートは上書きされる
- 作成後は必要に応じてgit commitを実行
- プロジェクト自動判定の詳細は `templates/project-detection.md` を参照

### all引数使用時の特別な注意
- **自動検出**: 作業ディレクトリ配下のディレクトリを動的にスキャン
- **プロジェクトタイプ自動判定**: package.json、*.csproj、技術スタックから自動判定
- **除外ディレクトリ**: node_modules, dist, .git 等は自動で除外
- **実行時間**: 複数プロジェクトへの適用のため時間がかかります  
- **エラー処理**: 一部プロジェクトで失敗しても他のプロジェクトは継続処理
- **上書き確認**: 全プロジェクトのテンプレートが上書きされることを確認

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
- **react**: package.jsonにreact依存関係またはvite.config.ts存在
- **web**: package.json存在かつreact以外のWeb技術
- **desktop**: *.csprojファイル存在  
- **question**: claude-config等の設定・ドキュメントプロジェクト
- **api**: サーバーサイド関連の依存関係検出
- **cli**: package.jsonのbinフィールドやCLI関連ファイル検出

詳細な判定ロジックは `templates/project-detection.md` を参照してください。