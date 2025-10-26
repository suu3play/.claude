---
name: good-first-issue-creator
description: プロジェクトから初級者でも取り組みやすいタスクを特定し、詳細な手順付きで「good first issue」としてGitHub Issueに登録するスキル。「初級者向けissueを作成」「good first issueを登録」「ビギナー向けタスクをissue化」と依頼された時に使用
---

# Good First Issue Creator - 初級者向けIssue自動作成スキル

このスキルは、プロジェクトから初級者でも取り組みやすいタスクを特定し、詳細な手順と学習リソース付きで「good first issue」としてGitHub Issueに登録します。

## 使用タイミング

- 「初級者向けissueを作成して」と依頼された時
- 「good first issueを登録して」と依頼された時
- 「ビギナー向けタスクをissue化して」と依頼された時
- 「新人がやれるタスクをissueにして」と依頼された時
- 「簡単なissueを作成して」と依頼された時

## Good First Issueの定義

初級者向けIssueは以下の条件を満たすもの:

### ✅ 適切なタスク

1. **範囲が限定的**
   - 1つのファイルまたは少数のファイルのみ修正
   - 変更行数が50行以内
   - 他の機能への影響が少ない

2. **明確な仕様**
   - やるべきことが明確
   - 期待される結果が具体的
   - 曖昧さがない

3. **技術的難易度が低い**
   - 基本的な言語構文のみ使用
   - 複雑なアルゴリズム不要
   - 既存パターンの踏襲

4. **詳細な手順付き**
   - ステップバイステップの説明
   - 参考コードやドキュメントへのリンク
   - 予想される所要時間

### ❌ 不適切なタスク

- アーキテクチャ変更
- パフォーマンスチューニング
- セキュリティ関連
- 複雑なバグ修正
- 広範囲なリファクタリング

## 実行フロー

### ステップ1: プロジェクト情報の取得

1. **プロジェクト名の特定**
   - ユーザーの指示から抽出
   - 指定がない場合はカレントディレクトリから判定

2. **プロジェクトディレクトリへ移動**
   ```bash
   cd "[プロジェクトルート]/[プロジェクト名]"
   ```

3. **プロジェクト構造の把握**
   - ディレクトリ構造を分析
   - 技術スタック確認（package.json, requirements.txt, pubspec.yamlなど）
   - コーディング規約の確認（.eslintrc, .prettierrcなど）

### ステップ2: 初級者向けタスクの特定

以下のカテゴリから適切なタスクを探索:

#### 📝 ドキュメント改善

```bash
# READMEの不足を確認
grep -r "TODO" README.md
grep -r "WIP" docs/

# コメント不足の関数を検索
grep -r "export function" --include="*.ts" | wc -l
grep -r "\/\*\*" --include="*.ts" | wc -l
```

**タスク例**:
- READMEにインストール手順を追加
- API関数にJSDocコメントを追加
- コントリビューションガイドの作成
- サンプルコードの追加

#### 🎨 UI/スタイル改善

```bash
# TODOコメントを検索
grep -r "TODO.*style" --include="*.css" --include="*.scss"
grep -r "FIXME.*color" --include="*.tsx" --include="*.vue"
```

**タスク例**:
- ボタンのホバー効果追加
- カラースキームの統一
- レスポンシブデザインの微調整
- アイコンの追加・変更

#### 🐛 簡単なバグ修正

```bash
# タイポや簡単なエラーを検索
grep -r "TODO.*typo"
grep -r "FIXME.*spelling"
```

**タスク例**:
- テキストのタイポ修正
- リンク切れの修正
- エラーメッセージの改善
- 定数の誤りを修正

#### 🧪 テスト追加

```bash
# テスト不足の関数を特定
# 関数定義数 vs テストケース数を比較
```

**タスク例**:
- 既存関数の単体テストを追加
- テストケースのカバレッジ向上
- エッジケースのテスト追加
- テストデータの作成

#### ♿ アクセシビリティ改善

```bash
# aria属性の欠如をチェック
grep -r "<button" --include="*.tsx" | grep -v "aria-label"
grep -r "<img" --include="*.html" | grep -v "alt="
```

**タスク例**:
- ボタンにaria-labelを追加
- 画像にalt属性を追加
- キーボードナビゲーション対応
- コントラスト比の改善

#### 🌐 国際化対応

```bash
# ハードコードされたテキストを検索
grep -r "\".*\"" --include="*.tsx" | grep -v "import"
```

**タスク例**:
- ハードコードされたテキストを翻訳ファイルに移動
- 新しい言語の翻訳追加
- 日付フォーマットのローカライズ

#### 🔧 コードクリーンアップ

```bash
# 未使用の変数やインポートを検索
grep -r "import.*from" --include="*.ts" | grep -v "use"
```

**タスク例**:
- 未使用のインポート削除
- console.logの削除
- コメントアウトされたコードの削除
- フォーマットの統一

### ステップ3: タスクの評価と選定

各候補タスクを以下の基準で評価:

1. **難易度スコア（1-5点）**
   - 1点: 非常に簡単（テキスト修正など）
   - 3点: 簡単なコーディング（既存パターンの踏襲）
   - 5点: やや複雑（ロジック考慮が必要）

2. **影響範囲スコア（1-5点）**
   - 1点: 1ファイルのみ
   - 3点: 2-3ファイル
   - 5点: 4ファイル以上

3. **学習価値スコア（1-5点）**
   - 1点: 繰り返し作業
   - 3点: 基本パターンを学べる
   - 5点: 新しいスキルを習得できる

**選定基準**:
- 難易度スコア ≤ 3
- 影響範囲スコア ≤ 3
- 学習価値スコア ≥ 2

### ステップ4: Issue内容の構成

各Good First Issueに以下の情報を含める:

#### 1. タイトル
- 簡潔で具体的
- `[Good First Issue]` プレフィックス
- 例: `[Good First Issue] READMEにインストール手順を追加`

#### 2. 説明セクション

**問題の説明**:
```markdown
## 📋 タスクの概要
現在のREADMEにはインストール手順が不足しています。
初めてプロジェクトをセットアップするユーザーが困らないよう、
詳細な手順を追加してください。
```

**対象者**:
```markdown
## 👥 対象者
- プロジェクトに初めて貢献する方
- Markdownの基本を知っている方
- 所要時間: 約30分
```

**実装手順**:
```markdown
## 📝 実装手順

### 1. リポジトリをフォーク・クローン
\`\`\`bash
git clone https://github.com/YOUR_USERNAME/[project-name].git
cd [project-name]
\`\`\`

### 2. README.mdを編集
以下の内容を「インストール」セクションに追加してください:

\`\`\`markdown
## インストール

### 前提条件
- Node.js 18以上
- npm 9以上

### 手順
1. 依存関係のインストール
   \`\`\`bash
   npm install
   \`\`\`

2. 環境変数の設定
   \`\`\`bash
   cp .env.example .env
   # .envファイルを編集
   \`\`\`

3. 開発サーバーの起動
   \`\`\`bash
   npm run dev
   \`\`\`
\`\`\`

### 3. 変更を確認
- README.mdをブラウザでプレビュー
- 誤字脱字がないか確認

### 4. コミットしてプッシュ
\`\`\`bash
git add README.md
git commit -m "docs: READMEにインストール手順を追加"
git push origin main
\`\`\`

### 5. プルリクエストを作成
- GitHubでプルリクエストを作成
- タイトル: "docs: READMEにインストール手順を追加"
```

**学習リソース**:
```markdown
## 📚 学習リソース

- [Markdown記法](https://docs.github.com/ja/get-started/writing-on-github)
- [良いREADMEの書き方](https://github.com/othneildrew/Best-README-Template)
- [プルリクエストの作成方法](https://docs.github.com/ja/pull-requests)
```

**チェックリスト**:
```markdown
## ✅ 完了基準

- [ ] インストール手順が追加されている
- [ ] コードブロックが正しくフォーマットされている
- [ ] 誤字脱字がない
- [ ] スクリーンショットで確認済み（任意）
```

#### 3. ラベル設定

標準ラベル（`.claude/labels.md`から読み込み）:
- **必須**: `Type：good first issue`
- **カテゴリ**:
  - ドキュメント → `Type：ドキュメント更新`
  - UI/スタイル → `Type：新機能・既存改修`
  - テスト → `Type：作業`
  - バグ修正 → `Type：バグ`
- **優先度**: `Priority：低` または `Priority：中`

#### 4. 推定時間
- 30分未満
- 30分-1時間
- 1-2時間

### ステップ5: ユーザー確認とIssue作成

1. **候補タスクのリスト表示**
   ```
   初級者向けタスク候補:

   1. [ドキュメント] READMEにインストール手順を追加 (30分)
   2. [UI] ボタンにホバー効果を追加 (1時間)
   3. [テスト] formatDate関数の単体テスト追加 (1時間)
   4. [アクセシビリティ] 画像にalt属性を追加 (30分)
   5. [バグ] エラーメッセージのタイポ修正 (15分)

   全部で5件のGood First Issueを作成します。
   よろしいですか？
   ```

2. **標準ラベルの読み込み**
   ```bash
   # labels.mdの存在確認
   if [ -f ".claude/labels.md" ]; then
     cat .claude/labels.md
   else
     echo "警告: .claude/labels.mdが見つかりません"
     echo "/copy-labelsを実行してラベルを設定することを推奨します"
   fi
   ```

3. **承認後、順次Issue作成**
   ```bash
   # 標準ラベルを使用したIssue作成
   gh issue create \
     --title "[Good First Issue] READMEにインストール手順を追加" \
     --body "$(cat issue_content.md)" \
     --label "Type：good first issue" \
     --label "Type：ドキュメント更新" \
     --label "Priority：低"
   ```

4. **作成結果の報告**
   ```
   Good First Issue作成完了:
   - #50: [Good First Issue] READMEにインストール手順を追加
   - #51: [Good First Issue] ボタンにホバー効果を追加
   - #52: [Good First Issue] formatDate関数の単体テスト追加
   - #53: [Good First Issue] 画像にalt属性を追加
   - #54: [Good First Issue] エラーメッセージのタイポ修正

   合計: 5件のGood First Issueを作成しました
   ```

## 使用例

### 例1: プロジェクト全体から特定

**ユーザー**: growth-diary の初級者向けissueを作成して

**スキルの動作**:
1. growth-diaryディレクトリに移動
2. プロジェクト構造を分析
3. 7つの初級者向けタスクを特定
4. 各タスクに詳細な手順を作成
5. ユーザーに確認
6. Good First Issueを7件作成

### 例2: 件数指定

**ユーザー**: good first issueを3件作成して

**スキルの動作**:
1. カレントディレクトリから判定
2. 最も適切な3件を選定
3. Issue作成

### 例3: カテゴリ指定

**ユーザー**: ドキュメント関連の初級者向けissueを作成して

**スキルの動作**:
1. ドキュメントカテゴリに絞って検索
2. 適切なタスクを特定
3. Issue作成

## Good First Issueテンプレート例

### ドキュメント系

```markdown
## 📋 タスクの概要
`UserService.ts`の関数にJSDocコメントを追加して、
コードの可読性を向上させてください。

## 👥 対象者
- JavaScriptまたはTypeScriptの基本を理解している方
- JSDocの書き方を学びたい方
- 所要時間: 約1時間

## 📝 実装手順

### 1. 対象ファイルを開く
`src/services/UserService.ts` を開いてください。

### 2. 以下の関数にJSDocを追加

\`\`\`typescript
/**
 * ユーザー情報を取得します
 * @param userId - 取得するユーザーのID
 * @returns ユーザー情報を含むPromise
 * @throws {Error} ユーザーが見つからない場合
 */
async function getUser(userId: string): Promise<User> {
  // 既存の実装
}
\`\`\`

### 3. すべての公開関数に適用
- `getUser`
- `updateUser`
- `deleteUser`
- `listUsers`

## 📚 学習リソース
- [JSDocの書き方](https://jsdoc.app/)
- [TypeScript JSDoc](https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html)

## ✅ 完了基準
- [ ] 4つの関数すべてにJSDocが追加されている
- [ ] パラメータと戻り値が正しく記述されている
- [ ] エラー条件が記載されている
```

### UI系

```markdown
## 📋 タスクの概要
ログインボタンにホバー効果を追加して、
ユーザーエクスペリエンスを向上させてください。

## 👥 対象者
- CSS/Tailwindの基本を理解している方
- UI/UXに興味がある方
- 所要時間: 約30分

## 📝 実装手順

### 1. 対象ファイルを開く
`src/components/LoginButton.tsx` を開いてください。

### 2. ホバー効果を追加

\`\`\`tsx
<button
  className="
    bg-blue-500 text-white px-4 py-2 rounded
    hover:bg-blue-600 hover:shadow-lg
    transition-all duration-200
  "
>
  ログイン
</button>
\`\`\`

### 3. 動作確認
- 開発サーバーを起動: `npm run dev`
- ブラウザでボタンにマウスを重ねる
- 色が濃くなり、影が表示されることを確認

## 📚 学習リソース
- [Tailwind CSS Hover](https://tailwindcss.com/docs/hover-focus-and-other-states)
- [CSS Transitions](https://developer.mozilla.org/ja/docs/Web/CSS/CSS_Transitions)

## ✅ 完了基準
- [ ] ホバー時に背景色が変わる
- [ ] ホバー時に影が表示される
- [ ] アニメーションが滑らか
```

## 注意事項

1. **適切な難易度設定**
   - 初級者が挫折しない範囲
   - しかし学習価値がある内容

2. **詳細な手順提供**
   - ステップバイステップで説明
   - コピペできるコード例を提供
   - 想定される問題と解決策も記載

3. **学習リソースの充実**
   - 公式ドキュメントへのリンク
   - チュートリアル記事
   - 参考コード

4. **明確な完了基準**
   - チェックリスト形式
   - テスト方法の説明
   - レビューポイント

5. **適切なラベル付け**
   - `Type：good first issue`は必須（`.claude/labels.md`から）
   - カテゴリラベル（Type系）も追加
   - Priority系ラベルで優先度を設定

## 関連スキル・コマンド

- `code-analyzer` - コード分析スキル
- `issue-fixer` - Issue対応スキル
- `/create-bug-issue` - バグIssue作成コマンド

## トラブルシューティング

### 適切なタスクが見つからない

- プロジェクトが成熟していて改善余地が少ない可能性
- TODOコメントを追加してタスクを明示化
- ドキュメント不足がないか確認

### Issue内容が不十分

- テンプレートを見直して充実化
- 既存のGood First Issueを参考にする
- コミュニティのフィードバックを反映
