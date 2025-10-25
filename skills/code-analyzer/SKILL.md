---
name: code-analyzer
description: プロジェクトのソースコードを分析してバグ、リファクタリング案、改修提案を特定し、GitHub Issueとして自動登録するスキル。「コードを分析してissue登録」「バグやリファクタリング案をissue化」「改修案をissueにして」と依頼された時に使用
---

# Code Analyzer - コード分析・Issue自動登録スキル

このスキルは、プロジェクトのソースコードを分析し、バグ、リファクタリング案、その他の改修提案を特定してGitHub Issueとして自動登録します。

## 使用タイミング

- 「コードを分析してissue登録して」と依頼された時
- 「バグやリファクタリング案をissue化して」と依頼された時
- 「改修案をissueにして」と依頼された時
- 「コードレビューしてissue作成して」と依頼された時
- 「技術的負債をissueにして」と依頼された時

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

**ラベル**: `bug`, `priority: high`

#### 🔧 リファクタリング (Refactoring)
- コードの重複
- 長い関数（100行以上）
- 深いネスト（4階層以上）
- 命名の問題
- 複雑度の高いコード

**ラベル**: `refactoring`, `tech-debt`

#### 📝 ドキュメント (Documentation)
- TODOコメント
- 未ドキュメント化のAPI
- README更新

**ラベル**: `documentation`

#### ⚡ パフォーマンス (Performance)
- 非効率なアルゴリズム
- 不要な再レンダリング
- メモリリークの可能性

**ラベル**: `performance`

#### 🧪 テスト (Testing)
- テストカバレッジ不足
- テストの欠如
- テストの改善提案

**ラベル**: `testing`

#### 🔒 セキュリティ (Security)
- ハードコードされた認証情報
- SQLインジェクションの可能性
- XSSの脆弱性

**ラベル**: `security`, `priority: high`

#### ♿ アクセシビリティ (Accessibility)
- aria属性の欠如
- キーボードナビゲーション
- コントラスト比の問題

**ラベル**: `accessibility`

### ステップ5: Issue作成計画の策定

1. **優先度の決定**
   - Critical: セキュリティ、ビルドエラー
   - High: 型エラー、バグ
   - Medium: リファクタリング、パフォーマンス
   - Low: ドキュメント、軽微な改善

2. **Issue内容の構成**
   各Issueに以下を含める:
   - タイトル: 簡潔で具体的
   - 説明: 問題の詳細
   - 影響範囲: 影響を受けるファイル
   - 修正方法: 具体的な修正案
   - 優先度: ラベルで表現
   - 見積もり: 修正にかかる時間の目安

3. **TodoWriteで作業計画を作成**
   - 各Issue作成タスクを登録
   - 優先度順に整理

### ステップ6: ユーザー確認

1. **分析結果のサマリーを表示**
   ```
   分析結果:
   - バグ: 5件
   - リファクタリング: 12件
   - ドキュメント: 3件
   - パフォーマンス: 2件
   - テスト: 4件
   合計: 26件の改修案
   ```

2. **作成するIssueのプレビュー**
   - 各カテゴリから代表的なIssue内容を表示
   - ユーザーに承認を求める

3. **フィルタリングオプション**
   - 「優先度Highのみ作成」
   - 「バグのみ作成」
   - 「すべて作成」

### ステップ7: GitHub Issue作成

承認後、順次Issueを作成:

```bash
# Issueテンプレート使用
gh issue create \
  --title "[Bug] 型エラー: UserProfile.tsでnullチェック不足" \
  --body "$(cat issue_content.md)" \
  --label "bug,priority: high" \
  --assignee "@me"
```

各Issue作成後:
- 作成されたIssue番号とURLを記録
- Todoリストのタスクを完了にマーク

### ステップ8: 結果レポート

1. **作成結果のまとめ**
   ```
   Issue作成完了:
   - #45: [Bug] 型エラー修正
   - #46: [Refactoring] UserService.tsのコード重複削除
   - #47: [Testing] ログインフローのテスト追加
   ...
   合計: 26件のIssueを作成しました
   ```

2. **Markdownレポート生成（オプション）**
   - `./reports/code_analysis_yyyyMMddHHmm.md`に保存
   - 分析結果と作成したIssue一覧

## 使用例

### 例1: プロジェクト全体を分析

**ユーザー**: growth-diary のコードを分析してissue登録して

**スキルの動作**:
1. growth-diaryディレクトリに移動
2. flutter analyzeで静的解析実行
3. TODOコメントやパターンを検索
4. 26件の改修案を特定
5. カテゴリごとに分類
6. ユーザーに確認
7. GitHub Issueを26件作成
8. 結果レポートを表示

### 例2: 特定カテゴリのみ

**ユーザー**: バグだけをissue化して

**スキルの動作**:
1. バグのみをフィルタリング
2. 5件のバグを特定
3. ユーザーに確認
4. バグ関連のIssueのみ作成

### 例3: カレントディレクトリで実行

**ユーザー**: このプロジェクトの改修案をissueにして

**スキルの動作**:
1. カレントディレクトリから自動判定
2. 以降は例1と同じフロー

## Issueテンプレート例

### バグIssue

```markdown
## 問題の概要
UserProfile.tsの85行目でnullチェックが不足しており、ランタイムエラーが発生する可能性があります。

## 影響範囲
- lib/models/user_profile.ts:85
- lib/services/user_service.ts:42（呼び出し元）

## 再現手順
1. ログインせずにプロフィール画面にアクセス
2. userオブジェクトがnullの状態で参照される

## 期待される動作
nullチェックを追加し、適切なエラーハンドリングを実装

## 修正方法
```typescript
// 修正前
const userName = user.profile.name;

// 修正後
const userName = user?.profile?.name ?? 'ゲスト';
```

## 優先度
High - ランタイムエラーを引き起こす可能性

## 見積もり
1-2時間
```

### リファクタリングIssue

```markdown
## 改善内容
UserService.tsとAdminService.tsで認証ロジックが重複しています。

## 影響範囲
- lib/services/user_service.ts:120-150
- lib/services/admin_service.ts:95-125

## 提案
共通の認証ロジックをauth_helper.tsに抽出し、両サービスから利用する。

## 修正方法
1. auth_helper.tsを作成
2. 共通認証ロジックを抽出
3. 両サービスから呼び出すように変更

## メリット
- コードの重複削減（約60行）
- 保守性の向上
- テストの簡素化

## 優先度
Medium

## 見積もり
2-3時間
```

## 設定オプション

スキル動作を以下の環境変数でカスタマイズ可能:

```bash
# Issue作成時に自動アサイン
export ISSUE_AUTO_ASSIGN=true

# 優先度の閾値（この値以上のみ作成）
export ISSUE_MIN_PRIORITY=medium

# レポート出力先
export ANALYSIS_REPORT_DIR=./reports
```

## エラーハンドリング

### 静的解析ツールが見つからない

```
警告: TypeScriptが見つかりません。
型チェックをスキップして他の分析を続行しますか？
```

### GitHub認証エラー

```
エラー: GitHub認証が必要です。
以下のコマンドを実行してください:
  gh auth login
```

### Issue作成失敗

```
エラー: Issue #X の作成に失敗しました。
原因: レート制限に達しました
対処: 1時間後に再実行してください
```

## 注意事項

1. **大量Issue作成の警告**
   - 20件以上のIssueを作成する場合は警告を表示
   - ユーザーに再確認を求める

2. **既存Issueの重複チェック**
   - 類似タイトルのIssueが存在する場合は警告
   - 重複を避けるため確認を求める

3. **プライベートリポジトリの権限**
   - Issue作成権限があることを確認
   - 権限不足の場合はエラーを報告

4. **分析範囲の制限**
   - node_modules, dist, buildなど除外ディレクトリを設定
   - .gitignoreのパターンを尊重

5. **実行時間**
   - 大規模プロジェクトでは分析に時間がかかる可能性
   - バックグラウンド実行も検討

## 関連コマンド・スキル

- `/analyze-errors` - エラー分析コマンド（既存）
- `/create-bug-issue` - バグIssue作成コマンド（既存）
- `issue-fixer` - Issue対応スキル
- `good-first-issue-creator` - 初級者向けIssue作成スキル

## 拡張機能案

このスキルは以下の機能拡張が可能:

1. **AI分析**: コード複雑度をAIで評価
2. **優先度の自動学習**: 過去のIssue対応時間から学習
3. **差分分析**: 前回分析からの変更点のみ分析
4. **CI/CD連携**: PRごとに自動分析実行
5. **カスタムルール**: プロジェクト固有の分析ルール追加

## トラブルシューティング

### スキルが発動しない

- 「コード分析」「issue登録」などのキーワードを含めて依頼
- 例: 「growth-diaryを分析してissue作成して」

### 分析結果が空

- 静的解析ツールが正しくインストールされているか確認
- プロジェクトルートで実行しているか確認

### Issue作成が遅い

- 大量のIssueを作成する場合は時間がかかります
- バッチサイズを調整（5件ずつなど）
