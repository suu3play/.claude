# 社内用Pythonツール作成スキル - README

## 概要

このスキルは、社内用Pythonツールを効率的に作成するためのテンプレート集です。5種類のベース機能を提供し、必要に応じて組み合わせて使用できます。

## ベース機能一覧

### 1. ChatGPT応答ベース (`templates/chatgpt_base.py`)
OpenAI GPT-4o APIを使用した対話型処理
- プロンプトテンプレート管理
- ストリーミング応答対応
- 会話履歴管理
- エラーハンドリング（レート制限、タイムアウト）

### 2. Slack通知ベース (`templates/slack_notification_base.py`)
Slackへの通知送信
- Webhook/Bot Token両対応
- リッチメッセージフォーマット（Blocks API）
- チャンネル・DMサポート
- ファイルアップロード対応

### 3. Teams通知ベース (`templates/teams_notification_base.py`)
Microsoft Teamsへの通知送信
- Webhook経由での通知
- アダプティブカード対応
- メンション機能
- アクションボタン設定

### 4. 従業員情報取得ベース (`templates/kot_employee_base.py`)
社内システム(KOT)から従業員マスタデータを取得
- 従業員検索（ID、名前、部署等）
- 部署・役職情報取得
- キャッシュ機構（API呼び出し削減）
- CSV/JSON出力

### 5. 勤怠情報取得ベース (`templates/kot_attendance_base.py`)
社内システム(KOT)から勤怠データを取得
- 勤怠データ取得（期間指定）
- 集計・分析機能
- 残業時間計算
- CSV出力対応

## ディレクトリ構造

```
python-tool-creator/
├── SKILL.md                           # スキル定義
├── README.md                          # 本ファイル
└── templates/                         # テンプレートファイル
    ├── chatgpt_base.py               # ChatGPT応答ベース
    ├── slack_notification_base.py    # Slack通知ベース
    ├── teams_notification_base.py    # Teams通知ベース
    ├── kot_employee_base.py          # 従業員情報取得ベース
    ├── kot_attendance_base.py        # 勤怠情報取得ベース
    ├── common/
    │   ├── config_manager.py         # 設定管理共通モジュール
    │   ├── logger.py                 # ロギング共通モジュール
    │   └── requirements.txt          # 依存パッケージ
    └── examples/
        └── combined_tool_example.py  # 複数ベース組み合わせ例
```

## 使用方法

### スキルの起動

Claude Codeで以下のように依頼します：

```
社内用Pythonツールを作成して
```

または具体的に：

```
ChatGPTで分析してSlackに通知するツールを作成して
勤怠データを取得してTeamsに送るツール
```

### 生成されるファイル

スキルを実行すると、以下のファイルが生成されます：

- `main.py`: メイン処理ロジック
- `config.yaml`: 設定ファイル
- `.env.example`: 環境変数のサンプル
- `requirements.txt`: 必要なパッケージ一覧
- `README.md`: ツールの使用方法
- `.gitignore`: Git除外設定

## 使用例

### 例1: ChatGPTで分析してSlackに通知

```
ユーザー: "ChatGPTで分析してSlackに通知するツールを作成して"

→ スキルが以下を生成:
  - chatgpt_base.py + slack_notification_base.py を統合
  - main.py にビジネスロジック
  - config.yaml に設定項目
  - .env.example に必要な環境変数
  - README.md に使用方法
```

### 例2: 勤怠データをTeamsに送信

```
ユーザー: "勤怠データを取得してTeamsに送るツール"

→ スキルが以下を生成:
  - kot_attendance_base.py + teams_notification_base.py を統合
  - データ変換ロジック
  - スケジュール実行設定例
```

## セキュリティ注意事項

### API Key管理
- API Key等の機密情報は必ず環境変数で管理
- `.env`ファイルは`.gitignore`に追加
- `.env.example`には実際の値を含めない
- 本番環境では適切なアクセス制御を実施

### .env ファイル例

```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Slack
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Teams
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/YOUR/WEBHOOK/URL

# KOT (社内システム)
KOT_API_ENDPOINT=https://your-internal-api.example.com
KOT_API_KEY=your_kot_api_key
```

## 共通モジュール

### config_manager.py
YAML/JSON設定ファイル管理、環境変数読み込み、デフォルト値設定

### logger.py
標準的なロギング設定、ファイル・コンソール出力、レベル別フォーマット

### requirements.txt
```
openai>=1.0.0
requests>=2.31.0
slack-sdk>=3.23.0
pymsteams>=0.2.2
pyyaml>=6.0
python-dotenv>=1.0.0
```

## カスタマイズ

生成されたテンプレートは以下の点でカスタマイズ可能です：

- エラーハンドリングの追加・変更
- ログレベルの調整
- データ加工ロジックの追加
- リトライ処理の追加
- バリデーション強化

## KOT APIについて

KOT（社内システム）のAPI仕様が確定していない部分については、テンプレートにTODOコメントを含めています。以下の点をカスタマイズしてください：

- エンドポイントURL
- 認証方式（Bearer Token、API Key等）
- リクエスト/レスポンス形式
- エラーコード処理

## トラブルシューティング

### API接続エラー
- API Keyが正しく設定されているか確認
- ネットワーク接続を確認
- エンドポイントURLが正しいか確認

### 認証エラー
- 環境変数が正しく読み込まれているか確認
- API Keyの有効期限を確認
- 権限設定を確認

### レート制限エラー
- リトライ処理の実装
- リクエスト間隔の調整
- バッチ処理の検討

## 期待される効果

- 社内ツール開発の時間短縮
- 一貫したコード品質
- ベストプラクティスの共有
- 新規開発者のオンボーディング効率化

## 関連情報

- OpenAI API: https://platform.openai.com/docs/api-reference
- Slack API: https://api.slack.com/
- Microsoft Teams Webhooks: https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/
