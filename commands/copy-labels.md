# ラベルコピーコマンド

## 概要

.claude プロジェクトの標準ラベル設定を指定されたプロジェクトまたは全プロジェクトにコピーするスラッシュコマンド

## 実行手順

1. **対象プロジェクトの確認**

    - 個別指定: 指定プロジェクトが Git リポジトリであることを確認
    - all 指定: 作業ディレクトリ配下を自動スキャンしてプロジェクト一覧を取得
    - プロジェクトタイプの自動判定（package.json, \*.csproj 等から判定）
    - gh CLI でアクセス可能であることを確認

2. **標準ラベル作成**

    - Type 系：ドキュメント更新、バグ、リファクタリング、新機能・既存改修、good first issue、作業
    - Priority 系：最優先、中、低
    - 色設定とラベル説明も統一適用

3. **既存 issue の更新**

    - 既存の英語ラベルから日本語ラベルへの変換マッピング
    - 全 issue のラベル一括更新
    - 古いラベルの削除とクリーンアップ

4. **適用確認**
    - ラベル一覧の確認
    - issue 更新結果の確認

## 使用方法

### 個別プロジェクトへの適用

```
/copy-labels [対象プロジェクト名]
```

### 全プロジェクトへの一括適用

```
/copy-labels all
```

## 実行例

### 個別適用

```
/copy-labels source-flow
/copy-labels portfolio
/copy-labels hobby-weather
/copy-labels finder-scope
```

### 一括適用

```
/copy-labels all
```

上記コマンドは作業ディレクトリ（`D:\自己開発`）配下の全プロジェクトに標準ラベル体系を適用します。
対象プロジェクトは実行時に自動検出されます。

## 標準ラベル体系

### Type 系ラベル

-   Type：ドキュメント更新 (#0075ca)
-   Type：バグ (#d73a4a)
-   Type：リファクタリング (#cfd3d7)
-   Type：新機能・既存改修 (#0e8a16)
-   Type：good first issue (#7057ff)
-   Type：作業 (#27cdee)

### Priority 系ラベル

-   Priority：最優先 (#b60205)
-   Priority：中 (#f66a0a)
-   Priority：低 (#fbca04)

## 注意事項

-   .claude が標準ラベル管理プロジェクト
-   既存ラベルは統一体系に変換される
-   GitHub の書き込み権限が必要
-   プロジェクト自動判定の詳細は `templates/project-detection.md` を参照

### all 引数使用時の特別な注意

-   **実行時間**: 複数プロジェクトへの適用のため時間がかかります
-   **エラー処理**: 一部プロジェクトで失敗しても他のプロジェクトは継続処理
-   **自動検出**: 作業ディレクトリ配下のディレクトリを動的にスキャン
-   **プロジェクト判定**: ファイル構造からプロジェクトタイプを自動判定
-   **除外ディレクトリ**: node_modules, dist, .git 等は自動で除外

### プロジェクト自動検出の流れ

```bash
# 1. 作業ディレクトリ配下をスキャン
WORKING_DIR="D:/自己開発"
for dir in "$WORKING_DIR"/*; do
    if [[ -d "$dir" ]]; then
        # プロジェクトタイプを判定
        PROJECT_TYPE=$(detect_project_type "$dir")
        if [[ "$PROJECT_TYPE" != "unknown" ]]; then
            # ラベル適用処理
        fi
    fi
done
```
