# スキル構造例と成功事例

このドキュメントは、効果的なスキル構造の具体例と、成功事例・失敗事例の比較を提供します。

## 基本的なスキル構造例

### 例1: pdf-editorスキル（scripts活用）

```
pdf-editor/
├── SKILL.md
└── scripts/
    ├── rotate_pdf.py
    ├── merge_pdf.py
    └── split_pdf.py
```

**SKILL.md (簡潔版)**:
```markdown
---
name: pdf-editor
description: PDFファイルの回転、結合、分割を行うスキル。ユーザーが「PDFを回転させて」「PDFを結合して」と依頼した時に使用
---

# PDF Editor

## 使用方法

PDFファイルの編集タスクには、以下のスクリプトを使用する：

- **回転**: `scripts/rotate_pdf.py <input.pdf> <degrees> <output.pdf>`
- **結合**: `scripts/merge_pdf.py <input1.pdf> <input2.pdf> <output.pdf>`
- **分割**: `scripts/split_pdf.py <input.pdf> <start_page> <end_page> <output.pdf>`
```

### 例2: big-queryスキル（references活用）

```
big-query/
├── SKILL.md
└── references/
    ├── schema.md
    └── query-patterns.md
```

**SKILL.md (簡潔版)**:
```markdown
---
name: big-query
description: BigQueryデータベースへのクエリ実行とデータ分析を行うスキル。ユーザーがデータ分析や集計を依頼した時に使用
---

# BigQuery Analyst

## 使用方法

1. ユーザーのクエリ要求を理解する
2. `references/schema.md`からテーブルスキーマを確認する
3. `references/query-patterns.md`から類似パターンを参照する
4. SQLクエリを構築して実行する

## スキーマの参照

大きなスキーマファイルの場合、以下のgrepパターンで検索：
- テーブル名: `grep -n "^## Table:" references/schema.md`
- カラム定義: `grep -n "^###" references/schema.md`
```

### 例3: frontend-webapp-builderスキル（assets活用）

```
frontend-webapp-builder/
├── SKILL.md
└── assets/
    ├── react-template/
    │   ├── package.json
    │   ├── src/
    │   └── public/
    └── html-template/
        ├── index.html
        └── styles.css
```

**SKILL.md (簡潔版)**:
```markdown
---
name: frontend-webapp-builder
description: フロントエンドWebアプリケーションを構築するスキル。ユーザーが「Webアプリを作って」「ダッシュボードを作って」と依頼した時に使用
---

# Frontend Webapp Builder

## 使用方法

1. ユーザーの要件を理解する
2. React or HTMLテンプレートを選択：
   - React: `assets/react-template/`をコピー
   - HTML: `assets/html-template/`をコピー
3. テンプレートをカスタマイズして要件を実装
```

## 成功事例と失敗事例の比較

### ケース1: データベース連携スキル

#### ❌ 失敗例（冗長なSKILL.md）

```markdown
---
name: company-db
description: 社内データベースに接続してクエリを実行する
---

# Company Database

## データベーススキーマ

### users テーブル
- id (INTEGER): ユーザーID
- name (VARCHAR): 名前
- email (VARCHAR): メールアドレス
- created_at (TIMESTAMP): 作成日時
... (500行以上のスキーマ定義が続く)

## クエリパターン

### ユーザー検索
SELECT * FROM users WHERE name LIKE '%keyword%';
... (100行以上のクエリ例が続く)
```

**問題点**:
- SKILL.mdが3000語を超える
- スキーマ情報で大量のトークンを消費
- 常に全情報がコンテキストに読み込まれる

#### ✅ 成功例（Progressive Disclosure活用）

```markdown
---
name: company-db
description: 社内データベースに接続してクエリを実行するスキル。データベースクエリや集計が必要な時に使用
---

# Company Database

## 使用方法

1. ユーザーのクエリ要求を理解する
2. `references/schema.md`から必要なテーブル情報を参照する
3. `references/query-patterns.md`から類似クエリパターンを確認する
4. SQLを構築して実行する

## スキーマの検索

大きなスキーマファイルから情報を探す際は：
- テーブル一覧: `grep "^## Table:" references/schema.md`
- 特定テーブル: `grep -A 20 "^## Table: users" references/schema.md`
```

```
company-db/
├── SKILL.md (200語)
└── references/
    ├── schema.md (2000語、必要時のみ読み込み)
    └── query-patterns.md (800語、必要時のみ読み込み)
```

**改善点**:
- SKILL.mdは200語に圧縮
- 詳細情報はreferencesに分離
- 必要な情報のみ読み込まれる
- トークン効率が大幅に向上

### ケース2: コード生成スキル

#### ❌ 失敗例（scriptsの過度な使用）

```
code-generator/
├── SKILL.md
└── scripts/
    ├── generate_react_component.py
    ├── generate_vue_component.py
    ├── generate_angular_component.py
    ├── generate_function.py
    ├── generate_class.py
    └── ... (20以上のスクリプト)
```

**問題点**:
- あらゆるコード生成をスクリプト化
- Claudeの柔軟性を損なう
- メンテナンスコストが高い
- ユーザー要件の変化に対応しづらい

#### ✅ 成功例（テンプレートとガイダンスの併用）

```
code-generator/
├── SKILL.md
├── assets/
│   ├── react-component-template/
│   └── vue-component-template/
└── references/
    └── coding-patterns.md
```

**SKILL.md**:
```markdown
---
name: code-generator
description: 再利用可能なコンポーネントやクラスを生成するスキル。コード生成が必要な時に使用
---

# Code Generator

## 使用方法

1. ユーザーの要件を理解する
2. 該当するテンプレートがあれば`assets/`から使用
3. `references/coding-patterns.md`でベストプラクティスを確認
4. 要件に応じて柔軟にコードを生成
```

**改善点**:
- スクリプトではなくテンプレートとガイダンスを提供
- Claudeの柔軟性を維持
- ユーザー要件の変化に対応しやすい

### ケース3: API統合スキル

#### ❌ 失敗例（メタデータが曖昧）

```markdown
---
name: api-helper
description: APIを使う
---
```

**問題点**:
- どのAPIか不明
- いつ使用すべきか不明
- トリガーワードが不明確

#### ✅ 成功例（具体的なメタデータ）

```markdown
---
name: slack-api-integration
description: Slack APIを使用してメッセージ送信、チャンネル管理、ユーザー情報取得を行うスキル。Slackへの通知や情報取得が必要な時に使用
---
```

**改善点**:
- 具体的なAPI名を明記
- サポートする機能を列挙
- 使用タイミングを明確化

## 段階的開示（Progressive Disclosure）の実例

### 悪い例: すべてをSKILL.mdに詰め込む

```markdown
---
name: brand-guidelines
description: ブランドガイドライン適用
---

# Brand Guidelines

## ロゴ使用規定
... (500語)

## カラーパレット
... (300語)

## タイポグラフィ
... (400語)

## トーン＆マナー
... (600語)

## ソーシャルメディアガイドライン
... (400語)

## 使用例集
... (800語)

合計: 3000語（常にコンテキスト消費）
```

### 良い例: 段階的開示を活用

```markdown
---
name: brand-guidelines
description: 企業ブランドガイドラインを適用するスキル。ロゴ、カラー、フォント、トーンの選択が必要な時に使用
---

# Brand Guidelines

## 使用方法

ブランドガイドラインに従うため、以下のリソースを参照：

- **ロゴ**: `assets/logos/`から適切なロゴを使用
- **カラー**: `references/colors.md`でパレットを確認
- **フォント**: `assets/fonts/`から選択
- **トーン**: `references/tone-of-voice.md`を参照
- **使用例**: `references/examples.md`で実例を確認

合計: 150語（必要な部分のみ読み込み）
```

```
brand-guidelines/
├── SKILL.md (150語)
├── assets/
│   ├── logos/
│   └── fonts/
└── references/
    ├── colors.md (300語)
    ├── tone-of-voice.md (600語)
    └── examples.md (800語)
```

**利点**:
- SKILL.mdは常に読み込まれても150語のみ
- 詳細情報は必要時のみ読み込み
- トークン効率が20倍向上（3000語 → 150語+必要な部分）

## 記述スタイルの比較

### ❌ 二人称（避けるべき）

```markdown
あなたがユーザーからPDF編集を依頼されたら、以下の手順を実行してください：

1. あなたはまずユーザーの要件を理解すべきです
2. 次にあなたは適切なスクリプトを選択してください
```

### ✅ 命令形/不定詞形（推奨）

```markdown
PDF編集を依頼された場合の手順：

1. ユーザーの要件を理解する
2. 適切なスクリプトを選択する
```

## まとめ: 効果的なスキル設計のチェックリスト

### メタデータ
- [ ] `name`は具体的で明確か
- [ ] `description`は使用タイミングとトリガーワードを含むか
- [ ] 三人称で記述されているか

### SKILL.md
- [ ] 5000語以下に収まっているか
- [ ] 命令形/不定詞形で記述されているか
- [ ] 本質的な手続き的指示のみを含むか
- [ ] 詳細情報はreferencesに移動されているか

### リソース構成
- [ ] scriptsは繰り返し書き直されるコードのみか
- [ ] referencesは必要時に読み込まれるドキュメントか
- [ ] assetsは出力に使用されるファイルか
- [ ] 不要な例示ファイルは削除されているか

### Progressive Disclosure
- [ ] メタデータ（常時）: ~100語
- [ ] SKILL.md（起動時）: <5000語
- [ ] リソース（必要時）: 無制限

これらのチェックリストに従うことで、効率的でメンテナンス性の高いスキルを作成できます。
