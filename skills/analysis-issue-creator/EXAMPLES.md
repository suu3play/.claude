# Analysis Issue Creator - 使用例

このドキュメントでは、analysis-issue-creatorスキルの具体的な使用例を示します。

## 例1: Criticalのみ作成（推奨パターン）

### ユーザーの依頼
```
growth-diaryの分析結果から、Criticalのissueだけ作成して
```

### スキルの応答

#### 1. 分析結果サマリー表示
```
📊 コード分析結果サマリー

総問題数: 362件
- 🔴 Critical: 31件（ビルドエラー、欠落ファイル）
- 🟠 High: 148件（型エラー、未定義メソッド）
- 🟡 Medium: 150件（Null安全性、リファクタリング）
- ⚪ Low: 33件（デバッグコード、TODOコメント）

Criticalの内訳:
- 欠落ファイル参照: 29件
- パス記述エラー: 2件
```

#### 2. Issue粒度の確認
```
Criticalは31件あります。

Issue作成の粒度を選択してください:
1. 詳細（31件のIssue作成）
2. 中粒度（関連問題をグループ化、推奨）→ 約5-8件
3. 粗粒度（カテゴリごと）→ 約2-3件
```

**ユーザーの選択**: 2

#### 3. グループ化基準の確認
```
グループ化基準を選択してください:
1. ファイル単位
2. 機能単位
3. エラー種類単位（推奨）
4. 自動判定
```

**ユーザーの選択**: 3

#### 4. Issue作成計画の提示
```
作成予定のIssue（5件）:

📋 Issue #1
タイトル: [Bug] 欠落モデルファイルの作成（Badge, Goal関連）
優先度: Critical
影響範囲:
  - lib/shared/models/badge.dart (欠落)
  - lib/shared/models/goal.dart (欠落)
  - lib/shared/models/goal_milestone.dart (欠落)
エラー件数: 29件
見積: 4-6時間

修正概要:
1. Badge モデルクラスの作成
   - id, name, description, rarity, iconUrl, unlockedAt
2. Goal モデルクラスの作成
   - id, title, category, status, targetDate, progress
3. GoalMilestone モデルクラスの作成
   - id, goalId, title, completedAt

---

📋 Issue #2
タイトル: [Bug] パス記述エラーの修正（Unicodeエスケープ）
優先度: Critical
影響範囲:
  - lib/features/goals/domain/usecases/goal_management_usecase.dart:4
エラー件数: 2件
見積: 30分

修正概要:
Windowsパス区切り文字（\）がエスケープシーケンスと解釈されている
修正前: 'package:growth_diary/features/userdomain\repositories\user_repository.dart'
修正後: 'package:growth_diary/features/user/domain/repositories/user_repository.dart'

[...]

このままIssueを作成しますか？
- はい（5件すべて作成）
- 番号を指定して作成（例: 1,2,3）
- 内容を修正
- キャンセル
```

**ユーザーの選択**: はい

#### 5. Issue作成実行
```
⏳ GitHub Issueを作成中...

✅ Issue #45 を作成しました
   [Bug] 欠落モデルファイルの作成（Badge, Goal関連）
   https://github.com/user/growth-diary/issues/45

✅ Issue #46 を作成しました
   [Bug] パス記述エラーの修正（Unicodeエスケープ）
   https://github.com/user/growth-diary/issues/46

[...]

✅ Issue作成完了（5件）
```

#### 6. 結果レポート
```
📊 Issue作成完了レポート

作成日時: 2025-01-26 15:30
プロジェクト: growth-diary

作成したIssue: 5件
- Critical: 5件

次のステップ:
1. Issue #45 から優先的に対応開始
2. 各Issueにブランチを作成（例: feature/issue-45）
3. 修正後にPRを作成

レポートファイル: ./reports/issues_created_20250126_1530.md
```

---

## 例2: バグとリファクタリング、High以上のみ

### ユーザーの依頼
```
バグとリファクタリングのHigh以上だけをissue化して。ファイル単位でまとめて
```

### スキルの応答

#### 1. フィルタリング結果表示
```
📊 フィルタリング結果

条件: バグ + リファクタリング、High + Critical
該当件数: 120件

優先度別:
- Critical: 30件
- High: 90件

カテゴリ別:
- バグ: 85件
- リファクタリング: 35件

ファイル別トップ5:
1. badge_management_usecase.dart: 65件
2. goal_management_usecase.dart: 25件
3. answer_repository_impl.dart: 10件
4. main_navigation.dart: 8件
5. その他: 12件
```

#### 2. Issue作成計画
```
ファイル単位でグループ化すると、約15件のIssueになります。

作成予定のIssue（抜粋）:

📋 Issue #1
タイトル: [Bug/Refactoring] badge_management_usecase.dart の型エラー修正
優先度: Critical
問題数: 65件
  - 未定義クラス: 20件
  - 未定義識別子: 18件
  - 型引数エラー: 15件
  - Null安全性: 12件
見積: 8-10時間

📋 Issue #2
タイトル: [Bug] goal_management_usecase.dart の未定義参照修正
優先度: Critical
問題数: 25件
  - 未定義クラス: 15件
  - URIエラー: 8件
  - その他: 2件
見積: 4-6時間

[...]

このままIssueを作成しますか？
```

**ユーザーの選択**: はい

---

## 例3: すべて作成（非推奨パターン）

### ユーザーの依頼
```
分析結果をすべてissue化して
```

### スキルの応答

#### 警告表示
```
⚠️ 警告: 大量のIssue作成

総問題数: 362件

すべてをIssue化すると以下の問題があります:
1. Issue管理が困難になる
2. 重複や関連性の把握が難しい
3. GitHub APIレート制限に達する可能性

推奨案:
- Criticalのみ（31件）
- Critical + High（179件）
- カテゴリを絞る（例: バグのみ 180件）

本当にすべて作成しますか？（y/n）
```

**ユーザーの選択**: y

#### 粒度の確認（強制）
```
大量Issue作成のため、中粒度以上を推奨します:

1. 中粒度（推奨）→ 約40-50件
2. 粗粒度 → 約15-20件
3. キャンセル

※詳細粒度（362件）は選択できません
```

**ユーザーの選択**: 1

---

## 例4: カスタム詳細指定

### ユーザーの依頼
```
growth-diaryの分析結果から：
- Criticalのバグは個別にIssue化
- Highのバグはファイル単位でグループ化
- リファクタリングは全体で1つのIssueにまとめて
```

### スキルの応答

```
📊 カスタム設定の確認

条件1: Critical バグ → 個別Issue
  該当: 20件 → 20 Issues

条件2: High バグ → ファイル単位グループ化
  該当: 65件 → 約8 Issues

条件3: リファクタリング（全優先度）→ 1Issue
  該当: 120件 → 1 Issue

合計: 約29 Issues

この設定で作成しますか？
```

**ユーザーの選択**: はい

---

## 例5: 既存Issue重複チェック

### ユーザーの依頼
```
Criticalのissueを作成して
```

### スキルの応答

```
⚠️ 重複の可能性

作成予定のIssue #1:
タイトル: [Bug] 欠落モデルファイルの作成（Badge, Goal関連）

既存のIssue #12 と類似しています（類似度: 85%）:
タイトル: [Bug] Badgeモデルが見つからない
URL: https://github.com/user/growth-diary/issues/12
状態: Open

どうしますか？
1. 既存Issue #12 にコメントを追加
2. 新しいIssueを作成
3. Issue #12 を更新
4. スキップ
```

**ユーザーの選択**: 1

---

## 例6: マイルストーンとアサインの設定

### ユーザーの依頼
```
Criticalのissueを作成して。v1.0マイルストーンで、自分にアサインして
```

### スキルの応答

```
✅ 設定確認

- 対象: Critical（31件）
- 粒度: 中粒度（約5件のIssue）
- マイルストーン: v1.0
- アサイン: @user（あなた）

Issue作成を開始しますか？
```

**ユーザーの選択**: はい

```
⏳ Issueを作成中...

✅ Issue #45 を作成しました
   マイルストーン: v1.0
   担当者: @user

[...]
```

---

## トラブルシューティング例

### ケース1: GitHub認証エラー

```
❌ エラー: GitHub認証が必要です

以下のコマンドで認証してください:
  gh auth login

認証後、再度スキルを実行してください。
```

### ケース2: レート制限

```
⚠️ GitHubレート制限に達しました

作成済み: 50件 / 予定: 100件
残り: 50件

オプション:
1. 1時間後に自動再開
2. 今すぐ手動で残りを作成（別アカウント使用）
3. 中断

選択してください:
```

### ケース3: ラベルが存在しない

```
⚠️ 警告: ラベルが存在しません

以下のラベルが見つかりません:
- priority: critical
- priority: high

作成しますか？
1. はい（推奨設定で作成）
2. いいえ（ラベルなしで作成）
3. カスタム設定

選択してください:
```

---

## ベストプラクティス

### 1. 初回は少量から
```
# 良い例
「Criticalのissueだけ作成して」→ 5-10件

# 悪い例
「全部作成して」→ 362件
```

### 2. 適切な粒度選択
```
# 問題数による推奨粒度

< 10件: 詳細粒度（1問題 = 1Issue）
10-50件: 中粒度（関連問題をグループ化）
50件以上: 粗粒度（カテゴリごと）
```

### 3. 優先度を意識
```
# 推奨順序

1. Critical のみ作成 → 対応 → 完了
2. High のみ作成 → 対応 → 完了
3. Medium 以降検討
```

### 4. レビュープロセス
```
# 作成前
1. Issue計画を必ず確認
2. グループ化が適切か検討
3. 見積もりが妥当か確認

# 作成後
1. Critical Issueの優先順位を決定
2. チームで分担を決める
3. 進捗を追跡
```
