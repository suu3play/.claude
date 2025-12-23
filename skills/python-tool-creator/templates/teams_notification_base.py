"""
Teams通知ベーステンプレート

Microsoft Teamsへの通知送信のベース実装
- Webhook経由での通知
- アダプティブカード対応
- メンション機能
- アクションボタン設定
"""

import os
from typing import Optional, List, Dict, Any
import pymsteams
import requests


class TeamsNotifier:
    """Microsoft Teams通知クライアント"""

    def __init__(self, webhook_url: Optional[str] = None):
        """
        初期化

        Args:
            webhook_url: Teams Webhook URL（未指定の場合は環境変数TEAMS_WEBHOOK_URLを使用）
        """
        self.webhook_url = webhook_url or os.getenv("TEAMS_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError("Teams Webhook URLが設定されていません")

    def send_simple_message(self, text: str, title: Optional[str] = None) -> bool:
        """
        シンプルなテキストメッセージを送信

        Args:
            text: メッセージ本文
            title: タイトル

        Returns:
            送信成功したかどうか
        """
        try:
            message = pymsteams.connectorcard(self.webhook_url)
            if title:
                message.title(title)
            message.text(text)
            message.send()
            return True

        except Exception as e:
            print(f"Teams送信エラー: {str(e)}")
            return False

    def send_notification_with_sections(
        self,
        title: str,
        summary: str,
        sections: Optional[List[Dict[str, str]]] = None,
        color: str = "0078D4",
    ) -> bool:
        """
        セクション付き通知を送信

        Args:
            title: タイトル
            summary: サマリー（通知プレビューに表示）
            sections: セクション情報のリスト [{"title": "セクションタイトル", "text": "内容"}, ...]
            color: テーマカラー（16進数、例: "0078D4"）

        Returns:
            送信成功したかどうか
        """
        try:
            message = pymsteams.connectorcard(self.webhook_url)
            message.title(title)
            message.summary(summary)
            message.color(color)

            # セクション追加
            if sections:
                for section_data in sections:
                    section = pymsteams.cardsection()
                    if "title" in section_data:
                        section.activityTitle(section_data["title"])
                    if "text" in section_data:
                        section.text(section_data["text"])
                    if "facts" in section_data:
                        for fact in section_data["facts"]:
                            section.addFact(fact["name"], fact["value"])
                    message.addSection(section)

            message.send()
            return True

        except Exception as e:
            print(f"Teams送信エラー: {str(e)}")
            return False

    def send_notification_with_facts(
        self,
        title: str,
        message_text: str,
        facts: List[Dict[str, str]],
        color: str = "0078D4",
    ) -> bool:
        """
        Facts付き通知を送信

        Args:
            title: タイトル
            message_text: メッセージ本文
            facts: ファクト情報のリスト [{"name": "項目名", "value": "値"}, ...]
            color: テーマカラー

        Returns:
            送信成功したかどうか
        """
        try:
            message = pymsteams.connectorcard(self.webhook_url)
            message.title(title)
            message.text(message_text)
            message.color(color)

            # Facts追加
            section = pymsteams.cardsection()
            for fact in facts:
                section.addFact(fact["name"], fact["value"])
            message.addSection(section)

            message.send()
            return True

        except Exception as e:
            print(f"Teams送信エラー: {str(e)}")
            return False

    def send_adaptive_card(self, card_payload: Dict[str, Any]) -> bool:
        """
        アダプティブカードを送信

        Args:
            card_payload: アダプティブカードのJSON

        Returns:
            送信成功したかどうか
        """
        try:
            response = requests.post(
                self.webhook_url,
                json=card_payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return True

        except requests.RequestException as e:
            print(f"Teams送信エラー: {str(e)}")
            return False

    def send_notification_with_button(
        self,
        title: str,
        message_text: str,
        button_text: str,
        button_url: str,
        color: str = "0078D4",
    ) -> bool:
        """
        ボタン付き通知を送信

        Args:
            title: タイトル
            message_text: メッセージ本文
            button_text: ボタンのテキスト
            button_url: ボタンのリンク先URL
            color: テーマカラー

        Returns:
            送信成功したかどうか
        """
        try:
            message = pymsteams.connectorcard(self.webhook_url)
            message.title(title)
            message.text(message_text)
            message.color(color)
            message.addLinkButton(button_text, button_url)
            message.send()
            return True

        except Exception as e:
            print(f"Teams送信エラー: {str(e)}")
            return False


# アダプティブカードの例
def create_status_card(
    title: str,
    status: str,
    details: List[Dict[str, str]],
    action_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    ステータス通知用アダプティブカードを作成

    Args:
        title: タイトル
        status: ステータス（成功/失敗等）
        details: 詳細情報リスト [{"label": "ラベル", "value": "値"}, ...]
        action_url: アクションボタンのURL

    Returns:
        アダプティブカードのJSON
    """
    # ステータスに応じた色設定
    status_colors = {
        "成功": "good",
        "警告": "warning",
        "失敗": "attention",
        "情報": "default",
    }
    color = status_colors.get(status, "default")

    # 詳細情報のフォーマット
    facts = [{"title": item["label"], "value": item["value"]} for item in details]

    card = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": title,
                            "weight": "bolder",
                            "size": "large",
                        },
                        {
                            "type": "TextBlock",
                            "text": f"ステータス: {status}",
                            "color": color,
                            "weight": "bolder",
                        },
                        {"type": "FactSet", "facts": facts},
                    ],
                },
            }
        ],
    }

    # アクションボタン追加
    if action_url:
        card["attachments"][0]["content"]["actions"] = [
            {
                "type": "Action.OpenUrl",
                "title": "詳細を表示",
                "url": action_url,
            }
        ]

    return card


# 使用例
if __name__ == "__main__":
    notifier = TeamsNotifier()

    # シンプルメッセージ
    print("=== シンプルメッセージ送信 ===")
    success = notifier.send_simple_message(
        title="テスト通知",
        text="これはテストメッセージです。",
    )
    print(f"送信結果: {success}")

    # Facts付き通知
    print("\n=== Facts付き通知送信 ===")
    success = notifier.send_notification_with_facts(
        title="処理完了通知",
        message_text="データ処理が正常に完了しました。",
        facts=[
            {"name": "処理件数", "value": "1,234件"},
            {"name": "処理時間", "value": "5分30秒"},
            {"name": "ステータス", "value": "成功"},
        ],
        color="00FF00",
    )
    print(f"送信結果: {success}")

    # ボタン付き通知
    print("\n=== ボタン付き通知送信 ===")
    success = notifier.send_notification_with_button(
        title="新しいタスク",
        message_text="レビューが必要な項目があります。",
        button_text="レビューを開始",
        button_url="https://example.com/review",
    )
    print(f"送信結果: {success}")

    # アダプティブカード
    print("\n=== アダプティブカード送信 ===")
    card = create_status_card(
        title="ビルド完了",
        status="成功",
        details=[
            {"label": "ビルド番号", "value": "#123"},
            {"label": "ブランチ", "value": "main"},
            {"label": "コミット", "value": "a1b2c3d"},
        ],
        action_url="https://example.com/build/123",
    )
    success = notifier.send_adaptive_card(card)
    print(f"送信結果: {success}")
