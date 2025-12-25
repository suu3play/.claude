"""
Slack通知ベーステンプレート

Slackへの通知送信のベース実装
- Webhook/Bot Token両対応
- リッチメッセージフォーマット（Blocks API）
- チャンネル・DMサポート
- ファイルアップロード対応
"""

import os
from typing import Optional, List, Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests


class SlackNotifier:
    """Slack通知クライアント"""

    def __init__(
        self,
        bot_token: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ):
        """
        初期化

        Args:
            bot_token: Slack Bot Token（未指定の場合は環境変数SLACK_BOT_TOKENを使用）
            webhook_url: Slack Webhook URL（未指定の場合は環境変数SLACK_WEBHOOK_URLを使用）
        """
        self.bot_token = bot_token or os.getenv("SLACK_BOT_TOKEN")
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")

        if self.bot_token:
            self.client = WebClient(token=self.bot_token)
        elif not self.webhook_url:
            raise ValueError("Slack Bot TokenまたはWebhook URLのいずれかを設定してください")

    def send_simple_message(
        self,
        text: str,
        channel: Optional[str] = None,
    ) -> bool:
        """
        シンプルなテキストメッセージを送信

        Args:
            text: メッセージ本文
            channel: チャンネル名またはユーザーID（Bot Token使用時のみ）

        Returns:
            送信成功したかどうか
        """
        try:
            if self.bot_token and channel:
                # Bot Token使用
                self.client.chat_postMessage(
                    channel=channel,
                    text=text,
                )
            elif self.webhook_url:
                # Webhook使用
                payload = {"text": text}
                response = requests.post(self.webhook_url, json=payload)
                response.raise_for_status()
            else:
                raise ValueError("チャンネル指定が必要です（Bot Token使用時）")

            return True

        except (SlackApiError, requests.RequestException) as e:
            print(f"Slack送信エラー: {str(e)}")
            return False

    def send_rich_message(
        self,
        blocks: List[Dict[str, Any]],
        text: str = "メッセージ",
        channel: Optional[str] = None,
    ) -> bool:
        """
        リッチメッセージを送信（Blocks API使用）

        Args:
            blocks: Slack Blocks配列
            text: フォールバック用テキスト
            channel: チャンネル名またはユーザーID（Bot Token使用時のみ）

        Returns:
            送信成功したかどうか
        """
        try:
            if self.bot_token and channel:
                # Bot Token使用
                self.client.chat_postMessage(
                    channel=channel,
                    text=text,
                    blocks=blocks,
                )
            elif self.webhook_url:
                # Webhook使用
                payload = {
                    "text": text,
                    "blocks": blocks,
                }
                response = requests.post(self.webhook_url, json=payload)
                response.raise_for_status()
            else:
                raise ValueError("チャンネル指定が必要です（Bot Token使用時）")

            return True

        except (SlackApiError, requests.RequestException) as e:
            print(f"Slack送信エラー: {str(e)}")
            return False

    def send_notification_with_sections(
        self,
        title: str,
        message: str,
        fields: Optional[List[Dict[str, str]]] = None,
        channel: Optional[str] = None,
        color: str = "#36a64f",
    ) -> bool:
        """
        セクション付き通知を送信

        Args:
            title: タイトル
            message: メッセージ本文
            fields: フィールド情報のリスト [{"title": "項目名", "value": "値", "short": True}, ...]
            channel: チャンネル名またはユーザーID
            color: サイドバーの色

        Returns:
            送信成功したかどうか
        """
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": title,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message,
                },
            },
        ]

        # フィールド追加
        if fields:
            fields_block = {
                "type": "section",
                "fields": [],
            }
            for field in fields:
                fields_block["fields"].append(
                    {
                        "type": "mrkdwn",
                        "text": f"*{field['title']}*\n{field['value']}",
                    }
                )
            blocks.append(fields_block)

        return self.send_rich_message(blocks=blocks, text=title, channel=channel)

    def upload_file(
        self,
        file_path: str,
        channel: str,
        title: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> bool:
        """
        ファイルをアップロード

        Args:
            file_path: アップロードするファイルのパス
            channel: チャンネル名またはユーザーID
            title: ファイルタイトル
            comment: コメント

        Returns:
            アップロード成功したかどうか
        """
        if not self.bot_token:
            raise ValueError("ファイルアップロードにはBot Tokenが必要です")

        try:
            self.client.files_upload_v2(
                channel=channel,
                file=file_path,
                title=title,
                initial_comment=comment,
            )
            return True

        except SlackApiError as e:
            print(f"ファイルアップロードエラー: {str(e)}")
            return False


# 使用例
if __name__ == "__main__":
    # Webhook URLを使用する場合
    notifier = SlackNotifier()

    # シンプルメッセージ
    print("=== シンプルメッセージ送信 ===")
    success = notifier.send_simple_message(
        text="テストメッセージです",
    )
    print(f"送信結果: {success}")

    # セクション付き通知
    print("\n=== セクション付き通知送信 ===")
    success = notifier.send_notification_with_sections(
        title="処理完了通知",
        message="データ処理が正常に完了しました。",
        fields=[
            {"title": "処理件数", "value": "1,234件"},
            {"title": "処理時間", "value": "5分30秒"},
            {"title": "ステータス", "value": "成功"},
        ],
    )
    print(f"送信結果: {success}")

    # Bot Tokenを使用する場合（チャンネル指定可能）
    # notifier_with_token = SlackNotifier(bot_token="xoxb-your-token")
    # notifier_with_token.send_simple_message(
    #     text="メッセージ",
    #     channel="#general"
    # )
    #
    # # ファイルアップロード
    # notifier_with_token.upload_file(
    #     file_path="report.csv",
    #     channel="#general",
    #     title="月次レポート",
    #     comment="今月の集計結果です。"
    # )
