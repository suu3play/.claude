---
description: プロジェクトのエラーを分析し、修正計画をmdファイルとして出力後、GitHub Issueに登録
---

# エラー分析とIssue登録

指定したプロジェクトのビルドエラーを分析し、修正計画を作成してGitHub Issueに登録します。

## コマンド形式

```
/analyze-errors [プロジェクト名]
```

- **引数なし**: カレントディレクトリのプロジェクトを解析
- **引数あり**: `d:\自己開発\[プロジェクト名]` ディレクトリを解析

## 使用例

```bash
# カレントプロジェクトを解析
/analyze-errors

# growth-diaryプロジェクトを解析
/analyze-errors growth-diary

# value-meプロジェクトを解析
/analyze-errors value-me

# portfolio-siteプロジェクトを解析
/analyze-errors portfolio-site
```

## 実行手順

### フェーズ1: エラー分析とmdファイル出力

1. **プロジェクトディレクトリの決定**
   - 引数が指定された場合: `d:\自己開発\[プロジェクト名]` に移動
   - 引数がない場合: カレントディレクトリを使用
   - ディレクトリが存在しない場合はエラーメッセージを表示

2. プロジェクトタイプを自動判定し、適切な解析コマンドを実行
   - **Flutter/Dart**: `flutter analyze` または `dart analyze`
   - **TypeScript/JavaScript**: `npm run lint` または `tsc --noEmit` または `eslint .`
   - **Python**: `pylint` または `flake8` または `mypy`
   - **Rust**: `cargo check` または `cargo clippy`
   - **Go**: `go vet` または `golangci-lint run`
   - **Java/Kotlin**: `./gradlew check` または `mvn verify`
   - **Ruby**: `rubocop`
   - **その他**: package.json、Makefile、プロジェクト構造から判定

3. エラーをカテゴリ別に分類・集計

4. 各エラーカテゴリごとに修正計画をmdファイルとして出力
   - **出力先**: 解析対象のプロジェクトディレクトリ（引数で指定したディレクトリまたはカレントディレクトリ）
   - ファイル名形式: `FIX_PLAN_XX_<カテゴリ名>.md`
   - 各ファイルには以下を含める:
     - 問題の概要
     - 優先度（🔴最高、🟡中、🟢低）
     - 影響範囲（エラー件数）
     - エラー詳細
     - 修正手順（具体的なコマンドとコード例）
     - 期待される結果
     - 注意事項
     - 次のステップ

5. 全体のサマリーファイル `FIX_PLAN_SUMMARY.md` を作成
   - **出力先**: 解析対象のプロジェクトディレクトリ
   - エラー統計
   - 修正計画一覧
   - 推奨修正順序（フェーズ分け）
   - 進捗トラッキング用チェックリスト

### フェーズ2: ユーザー確認待ち

生成されたmdファイルをユーザーに確認してもらい、Issue登録の承認を待つ。

**ユーザーへのメッセージ**:
```
修正計画を以下のファイルとして出力しました：
- FIX_PLAN_SUMMARY.md（全体サマリー）
- FIX_PLAN_01_*.md
- FIX_PLAN_02_*.md
...

内容を確認後、「issueに登録して」と指示してください。
登録後、mdファイルは自動的に削除されます。
```

### フェーズ3: GitHub Issue登録

ユーザーの承認後:

1. 各修正計画ファイルの内容を読み込み
2. GitHub Issueとして登録（`mcp__github__create_issue`を使用）
   - タイトル: mdファイルの見出しから抽出
   - 本文: mdファイルの内容をそのまま使用
   - ラベル: 優先度とカテゴリに応じて設定
     - 優先度: `high priority`, `medium priority`, `low priority`
     - タイプ: `bug`, `enhancement`, `refactoring`
     - カテゴリ: `dependencies`, `models`, `notifications`, `navigation`, `code quality`等
3. 登録完了後、Issue URLを表示
4. すべてのIssue登録が完了したら、生成したmdファイルをすべて削除

### フェーズ4: クリーンアップ

解析対象のプロジェクトディレクトリ内の以下のファイルを削除:
- `FIX_PLAN_*.md`（すべて）
- `analyze_output.txt`（解析結果の一時ファイル）
- `error_stats.txt`（統計情報の一時ファイル）

**注意**: プロジェクトの既存ファイル（README.md等）は削除しないこと

**重要**: mdファイルの削除は、Issue登録が完了した後のみ実行されます

## プロジェクトタイプの判定方法

以下のファイルやディレクトリの存在から自動判定:

| プロジェクトタイプ | 判定条件 |
|------------------|---------|
| Flutter | `pubspec.yaml` + `lib/`ディレクトリ + Flutter依存関係 |
| Dart | `pubspec.yaml` + `lib/`ディレクトリ（Flutter以外） |
| TypeScript | `tsconfig.json` または `package.json` + `.ts`ファイル |
| JavaScript | `package.json` + `.js`ファイル |
| Python | `requirements.txt`, `setup.py`, `pyproject.toml`, または`.py`ファイル |
| Rust | `Cargo.toml` |
| Go | `go.mod` |
| Java | `pom.xml` または `build.gradle` |
| Kotlin | `build.gradle.kts` |
| Ruby | `Gemfile` |
| C# | `.csproj` または `.sln` |

## エラーカテゴリの分類基準（言語共通）

エラーを以下のカテゴリに分類:

1. **依存関係の問題**
   - パッケージ/モジュール/ライブラリが見つからない
   - バージョン競合
   - 循環依存
2. **欠落ファイル**
   - インポート/requireされているが存在しないファイル
   - リソースファイルの欠落
3. **型/インターフェース定義不足**
   - 未定義のプロパティ/メソッド
   - 型不一致
   - インターフェース未実装
4. **API更新必要**
   - パッケージの破壊的変更
   - 非互換なAPI使用
5. **非推奨API**
   - Deprecatedな機能の使用
6. **コード品質**
   - Lintルール違反
   - 未使用のインポート/変数
   - フォーマット問題
7. **構文エラー**
   - 文法エラー
   - コンパイルエラー
8. **その他の実装エラー**

## 優先度の判定基準

- 🔴 **最高**: ビルド不可、アプリ起動不可
- 🟡 **中**: 一部機能が動作しない
- 🟢 **低**: 警告のみ、コード品質の問題

## Issue登録時のラベル設定

```
高優先度 + ビルドエラー → ["bug", "high priority", カテゴリ]
中優先度 + 機能エラー → ["bug", "medium priority", カテゴリ]
低優先度 + 警告 → ["enhancement", "low priority", カテゴリ]
```

## 実行例

### 例1: カレントディレクトリを解析（引数なし）

```
ユーザー: /analyze-errors

アシスタント:
カレントディレクトリを解析: d:\自己開発\growth-diary
プロジェクトタイプを検出: Flutter
1. flutter analyzeを実行してエラーを取得...
2. エラーを分類・集計...
3. 修正計画をmdファイルとして出力...

修正計画を7つのファイルとして出力しました（d:\自己開発\growth-diary）：
- FIX_PLAN_SUMMARY.md（全体サマリー）
- FIX_PLAN_01_MISSING_DEPENDENCIES.md（118件のエラー）
...

内容を確認後、「issueに登録して」と指示してください。
```

### 例2: プロジェクト名を指定して解析

```
ユーザー: /analyze-errors value-me

アシスタント:
解析対象: d:\自己開発\value-me
プロジェクトタイプを検出: TypeScript
1. tsc --noEmitを実行してエラーを取得...
2. eslintを実行してコード品質をチェック...
3. エラーを分類・集計...
4. 修正計画をmdファイルとして出力...

修正計画を5つのファイルとして出力しました（d:\自己開発\value-me）：
- FIX_PLAN_SUMMARY.md（全体サマリー）
- FIX_PLAN_01_TYPE_ERRORS.md（45件のエラー）
- FIX_PLAN_02_LINT_ERRORS.md（23件の警告）
...

内容を確認後、「issueに登録して」と指示してください。
```

### 例3: 別のプロジェクトを解析

```
ユーザー: /analyze-errors portfolio

アシスタント:
解析対象: d:\自己開発\portfolio
プロジェクトタイプを検出: Python
1. mypyを実行して型チェック...
2. flake8を実行してスタイルチェック...
3. エラーを分類・集計...
4. 修正計画をmdファイルとして出力...

修正計画を4つのファイルとして出力しました（d:\自己開発\portfolio）：
- FIX_PLAN_SUMMARY.md（全体サマリー）
- FIX_PLAN_01_TYPE_ANNOTATIONS.md（67件のエラー）
...

内容を確認後、「issueに登録して」と指示してください。
```

### 例4: 存在しないプロジェクトを指定

```
ユーザー: /analyze-errors nonexistent-project

アシスタント:
エラー: プロジェクトディレクトリが存在しません
パス: d:\自己開発\nonexistent-project

利用可能なプロジェクト:
- growth-diary
- value-me
- portfolio
- hobby-weather
...
```

### Issue登録（共通）

```
ユーザー: issueに登録して

アシスタント:
1. Issue #1を作成: 不足している依存関係の追加
2. Issue #2を作成: 型定義の修正
3. Issue #3を作成: コード品質の改善
...

すべてのIssueを登録しました。mdファイルを削除しています...

完了しました。以下のURLで確認できます：
https://github.com/<owner>/<repo>/issues
```

## 注意事項

- 様々なプロジェクトタイプに対応（Flutter, TypeScript, Python, Rust, Go等）
- プロジェクトタイプは自動判定されます
- GitHub認証情報が設定されている必要があります
- 大量のエラーがある場合、処理に時間がかかる可能性があります
- mdファイルの内容を確認してから、Issue登録を承認してください
- 解析ツールがインストールされていない場合、適切なエラーメッセージが表示されます
