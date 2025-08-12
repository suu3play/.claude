# テンプレートコピーコマンド

## 概要

.claude プロジェクトの標準 issue テンプレートを指定されたプロジェクトまたは全プロジェクトにコピーするスラッシュコマンド

## 実行手順

1. **対象プロジェクト確認**

    - 個別指定: 指定プロジェクトのディレクトリ存在確認
    - all 指定: 作業ディレクトリ配下を自動スキャンしてプロジェクト一覧を取得
    - Git リポジトリ状態の確認

2. **テンプレート配置**

    - 対象プロジェクトに`.github/ISSUE_TEMPLATE/` ディレクトリを作成
    - .claude の`.github/ISSUE_TEMPLATE/`ディレクトリ配下の標準テンプレートをコピー

3. **Git 管理追加**
    - 作成したテンプレートを git add で管理下に追加
    - コミット準備完了状態にする

## 使用方法

### 個別プロジェクトへの適用

```
/copy-templates [プロジェクト名]
```

### 個別適用

```
/copy-templates source-flow
/copy-templates portfolio
/copy-templates hobby-weather
/copy-templates finder-scope
/copy-templates .claude
```

### 一括適用

```
/copy-templates all
```

上記コマンドは作業ディレクトリ（`D:\自己開発`）配下の全プロジェクトにテンプレートを適用します。
対象プロジェクトは実行時に自動検出されます。

## 注意事項

-   .claude が標準テンプレート管理プロジェクト
-   既存テンプレートは上書きされる
-   作成後は必要に応じて git commit を実行

### all 引数使用時の特別な注意

-   **自動検出**: 作業ディレクトリ配下のディレクトリを動的にスキャン
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
        # テンプレート適用処理
        copy_templates_to_project "$dir"
    fi
done
```
