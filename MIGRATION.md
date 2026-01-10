# Claude Code設定の移行手順

このドキュメントは、`claude-code-config/`ディレクトリから標準的な`.claude/`ディレクトリ構成に移行する手順を説明します。

## 移行の目的

- Claude Codeの標準ディレクトリ構成（`.claude/`）に準拠
- パス参照の簡潔化（`claude-code-config/` → `.claude/`）
- 他のプロジェクトとの一貫性確保

## 前提条件

- Gitリポジトリが初期化されていること
- `claude-code-config/`ディレクトリが存在すること
- 作業ブランチを作成していること

## 移行手順

### ステップ1: 現在の状態確認

```bash
cd [プロジェクトルート]
ls -la | grep claude
git status
```

### ステップ2: `.claude/`ディレクトリ作成

```bash
# claude-code-configの内容を.claudeにコピー
cp -r claude-code-config .claude

# 確認
ls -la .claude/
```

**注意**: `mv`コマンドで移動しようとすると権限エラーが発生する場合があるため、`cp`でコピーしてください。

### ステップ3: CLAUDE.mdのパス更新

以下のパスをすべて置換：

| 置換前 | 置換後 |
|-------|--------|
| `claude-code-config/` | `.claude/` |

**対象ファイル**: `CLAUDE.md`

**置換箇所**:
- ディレクトリ構造図内のパス
- 開発ワークフロー参照パス
- ルールファイル参照パス
- テンプレートファイル参照パス

**例**:
```markdown
# 置換前
**重要**: 開発作業を開始する前に、必ず`claude-code-config/rules/development-workflow.md`を読み込んでから作業を開始すること。

# 置換後
**重要**: 開発作業を開始する前に、必ず`.claude/rules/development-workflow.md`を読み込んでから作業を開始すること。
```

### ステップ4: .gitignore更新

`.gitignore`ファイルに`claude-code-config/`を追加して除外対象にします。

```gitignore
# 個別プロジェクト（別リポジトリとして管理）
desk-app-kit/
clilog-viewer/
finder-scope/
hobby-weather/
portfolio/
source-flow/
value-me/
workplace-toolkit/
claude-code-config/    # ← この行を追加
```

これにより、旧ディレクトリはGit管理対象外になります。

### ステップ5: 変更をステージング

```bash
# .claude、CLAUDE.md、.gitignoreをステージング
git add .claude CLAUDE.md .gitignore

# 状態確認
git status
```

### ステップ6: コミット

```bash
git commit -m "refactor: .claudeディレクトリ構成に変更

- claude-code-configディレクトリを.claudeにコピー
- CLAUDE.mdのパス参照をすべて更新（claude-code-config/ → .claude/）
- .gitignoreにclaude-code-config/を追加して除外
- 標準的なClaude Code設定構成に準拠"
```

### ステップ7: プッシュ（必要に応じて）

```bash
git push -u origin [ブランチ名]
```

### ステップ8: 旧ディレクトリの削除（オプション）

移行が完了し、動作確認が済んだら、旧ディレクトリを削除できます。

```bash
# .gitignoreで除外されているため、Gitには影響しない
rm -rf claude-code-config
```

## 移行後の確認事項

### 1. ディレクトリ構造確認

```bash
ls -la .claude/
```

以下のディレクトリが存在することを確認：
- `rules/`
- `skills/`
- `templates/`
- `commands/`

### 2. CLAUDE.mdのパス確認

CLAUDE.md内のすべてのパス参照が`.claude/`に更新されていることを確認。

### 3. Git状態確認

```bash
git status
```

- `.claude/`がGit管理対象になっていること
- `claude-code-config/`が表示されないこと（.gitignoreで除外済み）

### 4. スキルとコマンドの動作確認

- スキルが正しく読み込まれること
- カスタムスラッシュコマンドが動作すること

## トラブルシューティング

### 問題1: `mv`コマンドで権限エラー

**症状**: `mv: cannot move 'claude-code-config' to '.claude': Permission denied`

**解決方法**: `cp -r`でコピーしてください。
```bash
cp -r claude-code-config .claude
```

### 問題2: .claudeディレクトリが既に存在

**症状**: `.claude`ディレクトリが既に存在している

**解決方法**:
```bash
# 既存の.claudeを削除してから再度コピー
rm -rf .claude
cp -r claude-code-config .claude
```

### 問題3: パス参照が動作しない

**症状**: CLAUDE.md内のパス参照が見つからない

**解決方法**: すべてのパス参照が`.claude/`に更新されているか確認：
```bash
# CLAUDE.md内でclaude-code-configが残っていないか確認
grep -n "claude-code-config" CLAUDE.md
```

## 移行チェックリスト

- [ ] `.claude/`ディレクトリが作成された
- [ ] CLAUDE.mdのすべてのパス参照が`.claude/`に更新された
- [ ] `.gitignore`に`claude-code-config/`が追加された
- [ ] 変更がコミットされた
- [ ] （オプション）リモートにプッシュされた
- [ ] （オプション）旧ディレクトリ`claude-code-config/`が削除された
- [ ] ディレクトリ構造が正しいことを確認した
- [ ] スキルとコマンドが動作することを確認した

## 参考情報

### 移行前の構造
```
プロジェクトルート/
├── claude-code-config/
│   ├── rules/
│   ├── skills/
│   └── ...
└── CLAUDE.md (参照: claude-code-config/...)
```

### 移行後の構造
```
プロジェクトルート/
├── .claude/              # Git管理対象
│   ├── rules/
│   ├── skills/
│   └── ...
├── claude-code-config/   # .gitignoreで除外（削除可能）
└── CLAUDE.md (参照: .claude/...)
```

## 関連ドキュメント

- `CLAUDE.md` - Claude Code設定の全体像
- `.claude/rules/development-workflow.md` - 開発ワークフロー
- `README.md` - リポジトリ概要
