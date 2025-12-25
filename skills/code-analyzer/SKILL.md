---
name: code-analyzer
description: プロジェクトのソースコードを分析してバグ、リファクタリング案、改修提案を特定するスキル。「コードを分析して」「バグやエラーをチェック」「静的解析を実行」と依頼された時に使用。分析結果を整理して報告し、必要に応じてissue-creatorスキルと連携
---

# Code Analyzer - コード分析スキル

プロジェクトのソースコードを分析し、バグ、リファクタリング案、その他の改修提案を特定してGitHub Issueとして自動登録します。

## 使用タイミング

- 「コードを分析してissue登録」
- 「バグやリファクタリング案をissue化」
- 「コードレビューしてissue作成」
- 「技術的負債をissueにして」

## 実行フロー

### 1. プロジェクト情報取得

1. プロジェクト名を特定（ユーザー指示またはカレントディレクトリ）
2. プロジェクトディレクトリに移動
3. プロジェクトタイプ判定（package.json, pyproject.toml, pubspec.yaml等から）

### 2. 静的解析実行

プロジェクトタイプに応じた解析ツールを実行（詳細: `references/analysis-tools.md`）

| プロジェクト | 主要コマンド |
|------------|------------|
| TypeScript | `npx tsc --noEmit`, `npm run lint` |
| Python | `mypy .`, `ruff check .` |
| Flutter | `flutter analyze` |
| Rust | `cargo check`, `cargo clippy` |

### 3. コード分析

- 各ツールの出力を収集
- パターン検索（TODO, FIXME, any型, デバッグコード等）
- コードメトリクス収集（ファイル数、重複コード等）

### 4. 改修案の分類

発見された問題をカテゴリと優先度で分類（詳細: `references/analysis-categories.md`）

| カテゴリ | 優先度 | 例 |
|---------|--------|---|
| 🐛 バグ | Critical/High | 型エラー、null参照 |
| 🔒 セキュリティ | Critical | 認証情報ハードコード |
| 🔧 リファクタリング | Medium/Low | コード重複、長い関数 |
| ⚡ パフォーマンス | Medium | 非効率なアルゴリズム |
| 🧪 テスト | Medium | カバレッジ不足 |
| 📝 ドキュメント | Low | TODOコメント |

**注意**: 標準ラベルは`.claude/labels.md`から読み込みます。未設定の場合は`/copy-labels`実行を提案します。

### 5. Issue作成計画策定

1. 優先度決定
2. Issue内容構成（タイトル、説明、影響範囲、修正方法、見積もり）
3. TodoWriteで作業計画作成

### 6. ユーザー確認

分析結果サマリーを表示し、承認を求める

```
分析結果:
- バグ: 5件
- リファクタリング: 12件
- ドキュメント: 3件
合計: 20件の改修案
```

フィルタリングオプション: 優先度別、カテゴリ別、すべて

### 7. GitHub Issue作成

標準ラベルを使用してIssue作成

```bash
gh issue create \
  --title "[Bug] 型エラー: UserProfile.tsでnullチェック不足" \
  --body "$(cat issue_content.md)" \
  --label "Type：バグ" \
  --label "Priority：中"
```

### 8. 結果レポート

作成したIssue一覧を表示し、オプションでMarkdownレポート生成（`./reports/code_analysis_yyyyMMddHHmm.md`）

## 使用例

**例1**: プロジェクト全体を分析
```
ユーザー: growth-diary のコードを分析してissue登録して
→ 26件の改修案を特定し、GitHub Issueを作成
```

**例2**: 特定カテゴリのみ
```
ユーザー: バグだけをissue化して
→ 5件のバグ関連Issueのみ作成
```

## 設定オプション

環境変数でカスタマイズ可能

```bash
export ISSUE_AUTO_ASSIGN=true           # 自動アサイン
export ISSUE_MIN_PRIORITY=medium        # 優先度閾値
export ANALYSIS_REPORT_DIR=./reports    # レポート出力先
```

## 注意事項

1. **大量Issue作成**: 20件以上は警告表示
2. **重複チェック**: 類似タイトルIssueの確認
3. **分析範囲**: node_modules, dist等を除外
4. **実行時間**: 大規模プロジェクトでは時間がかかる可能性

## 関連スキル

- `issue-fixer` - Issue対応スキル
- `good-first-issue-creator` - 初級者向けIssue作成
- `/analyze-errors` - エラー分析コマンド
