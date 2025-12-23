---
name: code-analyzer
description: プロジェクトのソースコードを分析してバグ、リファクタリング案、改修提案を特定するスキル。「コードを分析して」「バグやエラーをチェック」「静的解析を実行」と依頼された時に使用。分析結果を整理して報告し、必要に応じてissue-creatorスキルと連携
---

# Code Analyzer - コード分析スキル

このスキルは、プロジェクトのソースコードを分析し、バグ、リファクタリング案、その他の改修提案を特定して報告します。

## 使用タイミング

- 「コードを分析して」と依頼された時
- 「バグやエラーをチェックして」と依頼された時
- 「静的解析を実行して」と依頼された時
- 「コードレビューして」と依頼された時
- 「技術的負債を確認して」と依頼された時

## 実行フロー

### ステップ1: プロジェクト情報の取得

1. **プロジェクト名の特定**
   - ユーザーの指示から抽出
   - 指定がない場合はカレントディレクトリから判定
   - 不明な場合はユーザーに確認

2. **プロジェクトディレクトリへ移動**
   ```bash
   cd "[プロジェクトルート]/[プロジェクト名]"
   ```

3. **プロジェクトタイプの判定**
   - TypeScript/JavaScript (package.json)
   - Python (requirements.txt, pyproject.toml)
   - Flutter/Dart (pubspec.yaml)
   - Rust (Cargo.toml)
   - Go (go.mod)
   - C# (.csproj, .sln)

### ステップ2: 静的解析・エラーチェック

プロジェクトタイプに応じて適切なチェックツールを実行:

#### TypeScript/JavaScript
```bash
# 型チェック
npx tsc --noEmit

# リント
npm run lint

# ビルド
npm run build
```

#### Python
```bash
# 型チェック
mypy .

# リント
pylint **/*.py
ruff check .
```

#### Flutter/Dart
```bash
# 解析
flutter analyze

# フォーマットチェック
dart format --set-exit-if-changed .
```

#### Rust
```bash
# チェック
cargo check

# Clippy（リント）
cargo clippy -- -W clippy::all
```

#### C#
```bash
# ビルド
dotnet build

# コード分析
dotnet format --verify-no-changes
```

### ステップ3: コード分析

1. **エラー・警告の収集**
   - 各ツールの出力を収集
   - エラーレベルで分類（error, warning, info）

2. **パターン分析**
   - Grepツールで以下のパターンを検索:
     - `TODO:`, `FIXME:`, `HACK:`, `XXX:` コメント
     - `any`, `unknown` 型の使用（TypeScript）
     - `console.log`, `print` デバッグコード
     - 非推奨API（deprecated）の使用
     - 複雑度の高いコード（長い関数、深いネスト）

3. **コードメトリクス収集**
   - ファイル数とコード行数
   - 重複コードの検出
   - テストカバレッジ（可能な場合）

### ステップ4: 改修案の分類

発見された問題を以下のカテゴリに分類:

#### 🐛 バグ (Bug)
- ビルドエラー
- 型エラー
- null/undefined参照エラー
- 配列範囲外アクセス
- 無限ループの可能性

**優先度**: Critical または High

#### 🔧 リファクタリング (Refactoring)
- コードの重複
- 長い関数（100行以上）
- 深いネスト（4階層以上）
- 命名の問題
- 複雑度の高いコード

**優先度**: Medium または Low

#### 📝 ドキュメント (Documentation)
- TODOコメント
- 未ドキュメント化のAPI
- README更新

**優先度**: Low

#### ⚡ パフォーマンス (Performance)
- 非効率なアルゴリズム
- 不要な再レンダリング
- メモリリークの可能性

**優先度**: Medium

#### 🧪 テスト (Testing)
- テストカバレッジ不足
- テストの欠如
- テストの改善提案

**優先度**: Medium

#### 🔒 セキュリティ (Security)
- ハードコードされた認証情報
- SQLインジェクションの可能性
- XSSの脆弱性

**優先度**: Critical

#### ♿ アクセシビリティ (Accessibility)
- aria属性の欠如
- キーボードナビゲーション
- コントラスト比の問題

**優先度**: Medium

### ステップ5: 分析結果の整理と報告

1. **優先度の決定**
   - Critical: セキュリティ、ビルドエラー
   - High: 型エラー、バグ
   - Medium: リファクタリング、パフォーマンス
   - Low: ドキュメント、軽微な改善

2. **サマリーの表示**
   ```
   📊 コード分析結果サマリー

   総問題数: 362件
   - 🔴 Critical: 31件（ビルドエラー、欠落ファイル）
   - 🟠 High: 148件（型エラー、未定義メソッド）
   - 🟡 Medium: 150件（Null安全性、リファクタリング）
   - ⚪ Low: 33件（デバッグコード、TODOコメント）

   カテゴリ別:
   - 🐛 バグ: 180件
   - 🔧 リファクタリング: 120件
   - 📝 ドキュメント: 36件
   - ⚡ パフォーマンス: 15件
   - 🧪 テスト: 11件
   ```

3. **詳細レポートの生成（オプション）**
   `./reports/code_analysis_yyyyMMddHHmm.md`に保存:

   ```markdown
   # コード分析レポート

   実行日時: 2025-11-26 14:30
   プロジェクト: [project-name]
   プロジェクトタイプ: Flutter/Dart

   ## サマリー
   総問題数: 362件
   - Critical: 31件
   - High: 148件
   - Medium: 150件
   - Low: 33件

   ## 詳細

   ### Critical (31件)

   #### 1. 欠落ファイル参照
   - badge.dart が存在しない
     - 影響: lib/usecases/badge_management_usecase.dart:5
   - goal.dart が存在しない
     - 影響: lib/usecases/goal_management_usecase.dart:3

   #### 2. ビルドエラー
   - Unicodeエスケープエラー
     - 影響: lib/usecases/goal_management_usecase.dart:11

   ### High (148件)

   #### 1. 型定義エラー
   - BadgeManagementUsecase で84件の型エラー
   - GoalManagementUsecase で53件の型エラー

   #### 2. 未定義識別子
   - AnswerRepository が未定義（20箇所）

   [...]
   ```

### ステップ6: 次のステップの提案

分析結果に応じて、ユーザーに次のアクションを提案:

```
次のステップ:

1. Critical問題を優先的に修正
2. issue-creatorスキルでGitHub Issueを作成
   - 「分析結果からissueを作成して」と依頼してください
3. issue-fixerスキルで各Issueに対応
4. 修正後に再度コード分析を実行して確認
```

## 使用例

### 例1: プロジェクト全体を分析

**ユーザー**: growth-diary のコードを分析して

**スキルの動作**:
1. growth-diaryディレクトリに移動
2. flutter analyzeで静的解析実行
3. TODOコメントやパターンを検索
4. 362件の改修案を特定
5. カテゴリごとに分類
6. サマリーを表示
7. 詳細レポートを生成（オプション）
8. 次のステップを提案

### 例2: カレントディレクトリで実行

**ユーザー**: このプロジェクトのコードをチェックして

**スキルの動作**:
1. カレントディレクトリから自動判定
2. 以降は例1と同じフロー

### 例3: 特定カテゴリのみ報告

**ユーザー**: セキュリティ問題だけチェックして

**スキルの動作**:
1. 静的解析実行
2. セキュリティ関連のみフィルタリング
3. 結果を報告

## 分析レポートの保存形式

### Markdownレポート（詳細）

`./reports/code_analysis_yyyyMMddHHmm.md`に保存:

```markdown
# コード分析レポート

実行日時: 2025-11-26 14:30
プロジェクト: project-name

## サマリー
- 総問題数: 362件
- Critical: 31件
- High: 148件
- Medium: 150件
- Low: 33件

## カテゴリ別内訳
- バグ: 180件
- リファクタリング: 120件
- ドキュメント: 36件
- パフォーマンス: 15件
- テスト: 11件

## 詳細

### Critical問題

#### [1] 欠落ファイル: badge.dart
- **カテゴリ**: バグ
- **優先度**: Critical
- **影響範囲**:
  - lib/usecases/badge_management_usecase.dart:5
  - lib/models/badge.dart (存在しない)
- **説明**: badge.dartファイルが存在しないため、84件の型エラーが発生
- **推奨対応**: badge.dartモデルファイルを作成

[...]
```

### JSONレポート（機械可読）

`./reports/code_analysis_yyyyMMddHHmm.json`に保存（オプション）:

```json
{
  "timestamp": "2025-11-26T14:30:00Z",
  "project": "project-name",
  "projectType": "flutter",
  "summary": {
    "total": 362,
    "critical": 31,
    "high": 148,
    "medium": 150,
    "low": 33
  },
  "categories": {
    "bug": 180,
    "refactoring": 120,
    "documentation": 36,
    "performance": 15,
    "testing": 11
  },
  "issues": [
    {
      "id": 1,
      "title": "欠落ファイル: badge.dart",
      "category": "bug",
      "priority": "critical",
      "affectedFiles": [
        "lib/usecases/badge_management_usecase.dart:5"
      ],
      "description": "badge.dartファイルが存在しないため、84件の型エラーが発生",
      "recommendation": "badge.dartモデルファイルを作成"
    }
  ]
}
```

## 設定オプション

環境変数でカスタマイズ可能:

```bash
# レポート出力先
export ANALYSIS_REPORT_DIR=./reports

# レポート形式（markdown/json/both）
export ANALYSIS_REPORT_FORMAT=markdown

# 最小優先度（この値以上のみ報告）
export ANALYSIS_MIN_PRIORITY=medium

# 除外ディレクトリ
export ANALYSIS_EXCLUDE_DIRS=node_modules,dist,build,.git
```

## エラーハンドリング

### 静的解析ツールが見つからない

```
警告: TypeScriptが見つかりません。
型チェックをスキップして他の分析を続行しますか？
```

### プロジェクトタイプが不明

```
エラー: プロジェクトタイプを判定できません。
手動でプロジェクトタイプを指定してください:
- TypeScript/JavaScript
- Python
- Flutter/Dart
- Rust
- Go
- C#
```

### 分析結果が空

```
分析結果: 問題は見つかりませんでした。
コードは良好な状態です。
```

## 注意事項

1. **分析範囲の制限**
   - node_modules, dist, buildなど除外ディレクトリを設定
   - .gitignoreのパターンを尊重

2. **実行時間**
   - 大規模プロジェクトでは分析に時間がかかる可能性
   - バックグラウンド実行も検討

3. **Issue作成との連携**
   - 分析後にissue-creatorスキルを使用してIssue作成
   - 「分析結果からissueを作成して」と依頼

4. **偽陽性の可能性**
   - 静的解析ツールは偽陽性を報告する場合がある
   - 結果を確認してから対応を判断

## 関連スキル・コマンド

- `issue-creator` - Issue作成スキル（後工程）
- `issue-fixer` - Issue対応スキル（後工程）
- `/analyze-errors` - エラー分析コマンド（既存）

## 連携例

### コード分析 → Issue作成

```
ユーザー: コードを分析して
スキル (code-analyzer): [分析実行]
スキル (code-analyzer): [結果報告]
ユーザー: 分析結果からissueを作成して
スキル (issue-creator): [Issue作成実行]
```

## トラブルシューティング

### スキルが発動しない

- 「コード分析」「静的解析」などのキーワードを含めて依頼
- 例: 「このプロジェクトのコードを分析して」

### 分析結果が不十分

- 静的解析ツールが正しくインストールされているか確認
- プロジェクトルートで実行しているか確認

### 分析が遅い

- 大規模プロジェクトの場合は時間がかかる
- 除外ディレクトリの設定を確認
- 特定ディレクトリのみ分析することも検討
