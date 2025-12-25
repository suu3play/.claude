"""
ChatGPT応答ベーステンプレート

OpenAI GPT-4o APIを使用した対話型処理のベース実装
- プロンプトテンプレート管理
- ストリーミング応答対応
- 会話履歴管理
- エラーハンドリング
"""

import os
from typing import List, Dict, Optional, Generator
from openai import OpenAI, OpenAIError
import time


class ChatGPTClient:
    """ChatGPT APIクライアント"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_retries: int = 3,
    ):
        """
        初期化

        Args:
            api_key: OpenAI API Key（未指定の場合は環境変数OPENAI_API_KEYを使用）
            model: 使用するモデル名
            temperature: 生成温度（0.0-2.0）
            max_retries: リトライ回数
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API Keyが設定されていません")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.max_retries = max_retries
        self.conversation_history: List[Dict[str, str]] = []

    def chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        reset_history: bool = False,
    ) -> str:
        """
        チャット実行（非ストリーミング）

        Args:
            user_message: ユーザーメッセージ
            system_prompt: システムプロンプト
            reset_history: 会話履歴をリセットするか

        Returns:
            アシスタントの応答
        """
        if reset_history:
            self.conversation_history = []

        # メッセージ構築
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # 会話履歴追加
        messages.extend(self.conversation_history)

        # ユーザーメッセージ追加
        messages.append({"role": "user", "content": user_message})

        # API呼び出し（リトライ機能付き）
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                )

                assistant_message = response.choices[0].message.content

                # 会話履歴に追加
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": assistant_message})

                return assistant_message

            except OpenAIError as e:
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # 指数バックオフ
                    print(f"エラーが発生しました。{wait_time}秒後にリトライします... ({attempt + 1}/{self.max_retries})")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"ChatGPT API呼び出しに失敗しました: {str(e)}")

    def chat_stream(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        reset_history: bool = False,
    ) -> Generator[str, None, None]:
        """
        チャット実行（ストリーミング）

        Args:
            user_message: ユーザーメッセージ
            system_prompt: システムプロンプト
            reset_history: 会話履歴をリセットするか

        Yields:
            アシスタントの応答（チャンク単位）
        """
        if reset_history:
            self.conversation_history = []

        # メッセージ構築
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # 会話履歴追加
        messages.extend(self.conversation_history)

        # ユーザーメッセージ追加
        messages.append({"role": "user", "content": user_message})

        # API呼び出し（ストリーミング）
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                stream=True,
            )

            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content

            # 会話履歴に追加
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": full_response})

        except OpenAIError as e:
            raise Exception(f"ChatGPT API呼び出しに失敗しました: {str(e)}")

    def reset_history(self):
        """会話履歴をリセット"""
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, str]]:
        """会話履歴を取得"""
        return self.conversation_history.copy()


# 使用例
if __name__ == "__main__":
    # 初期化
    client = ChatGPTClient()

    # システムプロンプト
    system_prompt = "あなたは親切なアシスタントです。"

    # 非ストリーミング
    print("=== 非ストリーミング ===")
    response = client.chat(
        user_message="Pythonの特徴を3つ教えてください。",
        system_prompt=system_prompt,
    )
    print(response)
    print()

    # ストリーミング
    print("=== ストリーミング ===")
    for chunk in client.chat_stream(
        user_message="それぞれ詳しく説明してください。",
    ):
        print(chunk, end="", flush=True)
    print("\n")

    # 会話履歴表示
    print("=== 会話履歴 ===")
    for msg in client.get_history():
        print(f"{msg['role']}: {msg['content'][:50]}...")
