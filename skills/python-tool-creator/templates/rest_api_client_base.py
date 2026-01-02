"""
REST APIクライアントベーステンプレート

外部REST API連携を容易にするテンプレート。
認証、リトライ、エラーハンドリング、ページネーション対応。
"""

import time
import requests
from typing import Optional, Dict, Any, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from common.logger import setup_logger
from common.config_manager import ConfigManager


class RestAPIClient:
    """REST APIクライアントクラス

    外部APIへのHTTPリクエスト、認証、リトライ、エラーハンドリングを提供
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        config_path: str = "config.yaml",
        auth_token: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        初期化

        Args:
            base_url: APIベースURL
            config_path: 設定ファイルパス
            auth_token: Bearer認証トークン
            api_key: APIキー
        """
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config

        # ロガー初期化
        self.logger = setup_logger(
            name="rest_api_client",
            log_level=self.config.get("logging", {}).get("level", "INFO"),
            config=self.config
        )

        # REST API設定取得
        self.api_config = self.config.get("rest_api", {})
        self.base_url = (base_url or self.api_config.get("base_url", "")).rstrip("/")
        self.timeout = self.api_config.get("timeout", 30)

        # リトライ設定
        retry_config = self.api_config.get("retry", {})
        self.max_retries = retry_config.get("max_attempts", 3)
        self.backoff_factor = retry_config.get("backoff_factor", 2)

        # 認証設定
        auth_config = self.api_config.get("auth", {})
        self.auth_type = auth_config.get("type", "bearer")
        self.auth_token = auth_token or auth_config.get("token")
        self.api_key = api_key or auth_config.get("api_key")
        self.auth_header_name = auth_config.get("header_name", "Authorization")

        # デフォルトヘッダー
        self.default_headers = self.api_config.get("headers", {
            "User-Agent": "PythonTool/1.0",
            "Content-Type": "application/json"
        })

        # セッション作成（リトライ設定付き）
        self.session = self._create_session()

        self.logger.info(
            "RestAPIClient初期化完了",
            context={"base_url": self.base_url, "auth_type": self.auth_type}
        )

    def _create_session(self) -> requests.Session:
        """
        リトライ設定付きセッションを作成

        Returns:
            requests.Session
        """
        session = requests.Session()

        # リトライ設定
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _build_headers(self, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        リクエストヘッダーを構築

        Args:
            custom_headers: カスタムヘッダー

        Returns:
            完全なヘッダー辞書
        """
        headers = self.default_headers.copy()

        # 認証ヘッダー追加
        if self.auth_type == "bearer" and self.auth_token:
            headers[self.auth_header_name] = f"Bearer {self.auth_token}"
        elif self.auth_type == "api_key" and self.api_key:
            headers[self.auth_header_name] = self.api_key
        elif self.auth_type == "custom" and self.auth_token:
            headers[self.auth_header_name] = self.auth_token

        # カスタムヘッダーをマージ
        if custom_headers:
            headers.update(custom_headers)

        return headers

    def _build_url(self, endpoint: str) -> str:
        """
        完全なURLを構築

        Args:
            endpoint: エンドポイント

        Returns:
            完全なURL
        """
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}"

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        レスポンスを処理

        Args:
            response: HTTPレスポンス

        Returns:
            レスポンスデータ

        Raises:
            requests.HTTPError: HTTPエラー発生時
        """
        try:
            # ステータスコードチェック
            response.raise_for_status()

            # JSON解析
            if response.content:
                return response.json()
            else:
                return {"status": "success", "message": "No content"}

        except requests.exceptions.HTTPError as e:
            self.logger.error(
                f"HTTPエラー",
                context={
                    "status_code": response.status_code,
                    "url": response.url,
                    "error": str(e)
                },
                exc_info=True
            )
            raise

        except ValueError as e:
            self.logger.error(
                f"JSON解析エラー",
                context={"response": response.text[:200], "error": str(e)},
                exc_info=True
            )
            raise

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        GETリクエスト

        Args:
            endpoint: エンドポイント
            params: クエリパラメータ
            headers: カスタムヘッダー

        Returns:
            レスポンスデータ
        """
        try:
            url = self._build_url(endpoint)
            request_headers = self._build_headers(headers)

            self.logger.debug(
                f"GETリクエスト",
                context={"url": url, "params": params}
            )

            response = self.session.get(
                url,
                params=params,
                headers=request_headers,
                timeout=self.timeout
            )

            result = self._handle_response(response)

            self.logger.info(
                f"GETリクエスト成功",
                context={"url": url, "status_code": response.status_code}
            )

            return result

        except Exception as e:
            self.logger.error(
                f"GETリクエストエラー",
                context={"endpoint": endpoint, "error": str(e)},
                exc_info=True
            )
            raise

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        POSTリクエスト

        Args:
            endpoint: エンドポイント
            data: フォームデータ
            json: JSONデータ
            headers: カスタムヘッダー

        Returns:
            レスポンスデータ
        """
        try:
            url = self._build_url(endpoint)
            request_headers = self._build_headers(headers)

            self.logger.debug(
                f"POSTリクエスト",
                context={"url": url, "has_data": data is not None, "has_json": json is not None}
            )

            response = self.session.post(
                url,
                data=data,
                json=json,
                headers=request_headers,
                timeout=self.timeout
            )

            result = self._handle_response(response)

            self.logger.info(
                f"POSTリクエスト成功",
                context={"url": url, "status_code": response.status_code}
            )

            return result

        except Exception as e:
            self.logger.error(
                f"POSTリクエストエラー",
                context={"endpoint": endpoint, "error": str(e)},
                exc_info=True
            )
            raise

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        PUTリクエスト

        Args:
            endpoint: エンドポイント
            data: フォームデータ
            json: JSONデータ
            headers: カスタムヘッダー

        Returns:
            レスポンスデータ
        """
        try:
            url = self._build_url(endpoint)
            request_headers = self._build_headers(headers)

            self.logger.debug(
                f"PUTリクエスト",
                context={"url": url}
            )

            response = self.session.put(
                url,
                data=data,
                json=json,
                headers=request_headers,
                timeout=self.timeout
            )

            result = self._handle_response(response)

            self.logger.info(
                f"PUTリクエスト成功",
                context={"url": url, "status_code": response.status_code}
            )

            return result

        except Exception as e:
            self.logger.error(
                f"PUTリクエストエラー",
                context={"endpoint": endpoint, "error": str(e)},
                exc_info=True
            )
            raise

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        DELETEリクエスト

        Args:
            endpoint: エンドポイント
            headers: カスタムヘッダー

        Returns:
            レスポンスデータ
        """
        try:
            url = self._build_url(endpoint)
            request_headers = self._build_headers(headers)

            self.logger.debug(
                f"DELETEリクエスト",
                context={"url": url}
            )

            response = self.session.delete(
                url,
                headers=request_headers,
                timeout=self.timeout
            )

            result = self._handle_response(response)

            self.logger.info(
                f"DELETEリクエスト成功",
                context={"url": url, "status_code": response.status_code}
            )

            return result

        except Exception as e:
            self.logger.error(
                f"DELETEリクエストエラー",
                context={"endpoint": endpoint, "error": str(e)},
                exc_info=True
            )
            raise

    def get_paginated(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        page_param: str = "page",
        limit_param: str = "limit",
        max_pages: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        ページネーション対応GETリクエスト

        Args:
            endpoint: エンドポイント
            params: クエリパラメータ
            page_param: ページ番号パラメータ名
            limit_param: 件数制限パラメータ名
            max_pages: 最大ページ数（Noneの場合は全ページ取得）

        Returns:
            全ページのデータリスト
        """
        all_data = []
        page = 1
        params = params or {}

        try:
            while True:
                # ページパラメータ設定
                params[page_param] = page

                self.logger.debug(
                    f"ページネーションリクエスト",
                    context={"page": page, "endpoint": endpoint}
                )

                # リクエスト実行
                response = self.get(endpoint, params=params)

                # データ抽出（レスポンス構造に応じて調整が必要）
                if isinstance(response, list):
                    data = response
                elif isinstance(response, dict):
                    # 一般的なパターン: {"data": [...], "total": 100}
                    data = response.get("data", response.get("results", []))
                else:
                    data = []

                if not data:
                    break

                all_data.extend(data)

                # 最大ページ数チェック
                if max_pages and page >= max_pages:
                    break

                page += 1

            self.logger.info(
                f"ページネーション完了",
                context={"total_items": len(all_data), "pages": page}
            )

            return all_data

        except Exception as e:
            self.logger.error(
                f"ページネーションエラー",
                context={"endpoint": endpoint, "page": page, "error": str(e)},
                exc_info=True
            )
            raise

    def close(self) -> None:
        """
        セッションをクローズ
        """
        self.session.close()
        self.logger.info("セッションクローズ")


# 使用例
if __name__ == "__main__":
    # REST API呼び出しの基本フロー
    client = RestAPIClient(
        base_url="https://api.example.com",
        auth_token="YOUR_TOKEN_HERE"
    )

    try:
        # GETリクエスト
        users = client.get("/users", params={"page": 1, "limit": 10})
        print(f"取得ユーザー数: {len(users)}")

        # POSTリクエスト
        new_user = client.post("/users", json={
            "name": "John Doe",
            "email": "john@example.com"
        })
        print(f"作成ユーザーID: {new_user.get('id')}")

        # PUTリクエスト
        updated_user = client.put(f"/users/{new_user['id']}", json={
            "name": "John Updated"
        })
        print(f"更新完了: {updated_user.get('name')}")

        # ページネーション取得
        all_users = client.get_paginated("/users", params={"limit": 100})
        print(f"全ユーザー数: {len(all_users)}")

    finally:
        client.close()
