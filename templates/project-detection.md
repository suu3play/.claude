# プロジェクト自動判定システム

## 概要

作業ディレクトリ配下のディレクトリを自動スキャンしてプロジェクトタイプを判定するシステム。
`/copy-labels all` や `/copy-templates all` コマンドで動的にプロジェクト一覧を取得します。

## プロジェクト判定ルール

### 1. ディレクトリスキャン

```bash
# 作業ディレクトリ配下の第1階層ディレクトリを取得
find "${WORKING_DIR}" -maxdepth 1 -type d -not -path "${WORKING_DIR}"
```

### 2. プロジェクトタイプ自動判定

#### React プロジェクト (`react`)

-   `package.json` が存在
-   かつ以下のいずれかの条件：
    -   `package.json` に "react" 依存関係が存在
    -   `vite.config.ts` または `vite.config.js` が存在
    -   `src/` ディレクトリ内に `.tsx` ファイルが存在

#### Web プロジェクト (`web`)

-   `package.json` が存在
-   かつ React プロジェクトの条件に該当しない
-   かつ以下のいずれかの条件：
    -   `index.html` が存在
    -   `public/` ディレクトリが存在
    -   `package.json` に "typescript", "javascript" 関連の依存関係

#### Desktop プロジェクト (`desktop`)

-   `*.csproj` ファイルが存在
-   または `*.sln` ファイルが存在
-   または `src/` 配下に `.csproj` ファイルが存在

#### API プロジェクト (`api`)

-   `package.json` が存在
-   かつ以下のいずれかの条件：
    -   `package.json` に "express", "fastify", "koa" 等のサーバー依存関係
    -   `server.js`, `server.ts`, `app.js`, `app.ts` が存在
    -   `routes/` または `controllers/` ディレクトリが存在

#### CLI プロジェクト (`cli`)

-   `package.json` の `bin` フィールドが存在
-   または `#!/usr/bin/env node` で始まるファイルが存在
-   または `cli/` ディレクトリが存在

#### Question プロジェクト (`question`)

-   プロジェクト名が ".claude" に一致
-   または `.github/ISSUE_TEMPLATE/` ディレクトリのみ存在
-   または主に Markdown ファイルで構成される設定プロジェクト

### 3. 除外条件

以下のディレクトリは自動判定から除外：

-   `.git`, `.github`, `.vscode`, `.idea`
-   `node_modules`, `dist`, `build`, `out`
-   `bin`, `obj`, `target`
-   隠しディレクトリ（`.` で始まる）

## 実装例

### Bash 実装

```bash
#!/bin/bash

detect_project_type() {
    local project_dir="$1"

    # React判定
    if [[ -f "$project_dir/package.json" ]]; then
        if grep -q '"react"' "$project_dir/package.json" 2>/dev/null || \
           [[ -f "$project_dir/vite.config.ts" ]] || \
           [[ -f "$project_dir/vite.config.js" ]]; then
            echo "react"
            return
        fi

        # API判定
        if grep -qE '"(express|fastify|koa)"' "$project_dir/package.json" 2>/dev/null || \
           [[ -f "$project_dir/server.js" ]] || \
           [[ -f "$project_dir/server.ts" ]]; then
            echo "api"
            return
        fi

        # CLI判定
        if grep -q '"bin"' "$project_dir/package.json" 2>/dev/null; then
            echo "cli"
            return
        fi

        # Web判定（デフォルト）
        echo "web"
        return
    fi

    # Desktop判定
    if find "$project_dir" -name "*.csproj" -o -name "*.sln" | grep -q .; then
        echo "desktop"
        return
    fi

    # Question判定
    if [[ "$(basename "$project_dir")" == ".claude" ]]; then
        echo "question"
        return
    fi

    # デフォルト
    echo "unknown"
}

get_all_projects() {
    local working_dir="$1"
    local projects=()

    for dir in "$working_dir"/*; do
        if [[ -d "$dir" ]]; then
            local basename=$(basename "$dir")

            # 除外ディレクトリチェック
            if [[ "$basename" == .* ]] || \
               [[ "$basename" == "node_modules" ]] || \
               [[ "$basename" == "dist" ]] || \
               [[ "$basename" == "build" ]]; then
                continue
            fi

            local project_type=$(detect_project_type "$dir")
            if [[ "$project_type" != "unknown" ]]; then
                projects+=("$basename:$project_type")
            fi
        fi
    done

    printf '%s\n' "${projects[@]}"
}
```

## 使用方法

### コマンド内での使用

````markdown
## 実行手順

1. **プロジェクト自動検出**
    ```bash
    WORKING_DIR="D:/自己開発"
    PROJECTS=$(get_all_projects "$WORKING_DIR")
    ```
````

2. **各プロジェクトへの適用**
    ```bash
    while IFS=':' read -r project_name project_type; do
        echo "Processing $project_name ($project_type)"
        # ラベルやテンプレートの適用処理
    done <<< "$PROJECTS"
    ```

```

## メリット

1. **メンテナンスフリー**: 新規プロジェクト追加時の手動更新が不要
2. **柔軟性**: プロジェクトの追加・削除・移動に自動対応
3. **正確性**: ファイル構造による客観的判定
4. **拡張性**: 新しいプロジェクトタイプの判定ルール追加が容易

## 注意事項

- プロジェクトディレクトリには識別可能な構造ファイル（package.json, *.csproj等）が必要
- 判定ルールは上から順に評価され、最初にマッチした条件で決定
- 判定不能なディレクトリは自動的に除外される
```
