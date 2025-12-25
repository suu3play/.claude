"""
複数ベース機能組み合わせ例

ChatGPTで分析してSlackに通知するツールの実装例
"""

import sys
from pathlib import Path

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from chatgpt_base import ChatGPTClient
from slack_notification_base import SlackNotifier
from common.config_manager import ConfigManager
from common.logger import setup_logger


class DataAnalysisTool:
    """データ分析＆通知ツール"""

    def __init__(self, config_path: str = "config.yaml"):
        """
        初期化

        Args:
            config_path: 設定ファイルパス
        """
        # 設定読み込み
        self.config = ConfigManager(config_path=config_path)

        # ロガーセットアップ
        self.logger = setup_logger(
            name="data_analysis_tool",
            log_level=self.config.get("logging.level", default="INFO"),
            log_file=self.config.get("logging.file"),
        )

        # ChatGPTクライアント初期化
        self.chatgpt = ChatGPTClient(
            model=self.config.get("openai.model", default="gpt-4o"),
            temperature=self.config.get("openai.temperature", default=0.7),
        )

        # Slack通知クライアント初期化
        self.slack = SlackNotifier()

        self.logger.info("データ分析ツールを初期化しました")

    def analyze_data(self, data_summary: str) -> str:
        """
        データを分析

        Args:
            data_summary: データサマリー

        Returns:
            分析結果
        """
        self.logger.info("データ分析を開始します")

        # システムプロンプト
        system_prompt = """
        あなたはデータ分析の専門家です。
        提供されたデータサマリーを分析し、以下の観点でレポートを作成してください：

        1. 主要な傾向
        2. 注目すべきポイント
        3. 改善提案

        簡潔で分かりやすく、箇条書きで記載してください。
        """

        # ChatGPTで分析
        try:
            analysis = self.chatgpt.chat(
                user_message=f"以下のデータサマリーを分析してください：\n\n{data_summary}",
                system_prompt=system_prompt,
                reset_history=True,
            )

            self.logger.info("データ分析が完了しました")
            return analysis

        except Exception as e:
            self.logger.error(f"データ分析中にエラーが発生しました: {str(e)}")
            raise

    def send_notification(
        self, title: str, analysis_result: str, data_summary: str
    ) -> bool:
        """
        Slackに分析結果を通知

        Args:
            title: タイトル
            analysis_result: 分析結果
            data_summary: データサマリー

        Returns:
            送信成功したかどうか
        """
        self.logger.info("Slack通知を送信します")

        # 通知フィールド作成
        fields = [
            {"title": "データサマリー", "value": data_summary[:100] + "..."},
            {"title": "分析結果", "value": analysis_result[:500] + "..."},
        ]

        # Slack通知送信
        try:
            success = self.slack.send_notification_with_sections(
                title=title,
                message="データ分析が完了しました。",
                fields=fields,
                color="#36a64f",
            )

            if success:
                self.logger.info("Slack通知を送信しました")
            else:
                self.logger.warning("Slack通知の送信に失敗しました")

            return success

        except Exception as e:
            self.logger.error(f"Slack通知送信中にエラーが発生しました: {str(e)}")
            return False

    def run(self, data_summary: str) -> bool:
        """
        データ分析＆通知を実行

        Args:
            data_summary: データサマリー

        Returns:
            処理成功したかどうか
        """
        try:
            # データ分析
            analysis_result = self.analyze_data(data_summary)

            # Slack通知
            success = self.send_notification(
                title="データ分析レポート",
                analysis_result=analysis_result,
                data_summary=data_summary,
            )

            return success

        except Exception as e:
            self.logger.exception(f"処理中にエラーが発生しました: {str(e)}")
            return False


# 使用例
if __name__ == "__main__":
    # サンプルデータ
    sample_data = """
    【2024年1月の売上データサマリー】

    - 総売上: 12,500,000円（前月比 +15%）
    - 新規顧客数: 234件（前月比 +8%）
    - リピート率: 68%（前月比 -2%）
    - 平均単価: 53,000円（前月比 +12%）
    - トップ商品カテゴリ:
      1. 製品A: 4,200,000円
      2. 製品B: 3,800,000円
      3. 製品C: 2,100,000円

    【主要トピック】
    - キャンペーン実施により新規顧客数が増加
    - 既存顧客のリピート率がやや低下
    - 平均単価の上昇傾向が継続
    """

    # config.yamlのサンプル
    sample_config = """
    logging:
      level: "INFO"
      file: "analysis_tool.log"

    openai:
      model: "gpt-4o"
      temperature: 0.7

    slack:
      channel: "#analytics"
    """

    # 設定ファイル作成（テスト用）
    with open("config.yaml", "w", encoding="utf-8") as f:
        f.write(sample_config)

    print("=== データ分析＆Slack通知ツール実行例 ===\n")

    # ツール初期化
    tool = DataAnalysisTool(config_path="config.yaml")

    # 実行
    print("データ分析を実行中...\n")
    success = tool.run(sample_data)

    if success:
        print("\n✓ 処理が正常に完了しました")
        print("  - データ分析完了")
        print("  - Slack通知送信完了")
    else:
        print("\n✗ 処理中にエラーが発生しました")

    # クリーンアップ
    Path("config.yaml").unlink(missing_ok=True)
