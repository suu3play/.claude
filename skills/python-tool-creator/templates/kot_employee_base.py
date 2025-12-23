"""
従業員情報取得ベーステンプレート（KOT連携）

社内システム(KOT)から従業員マスタデータを取得するベース実装
- 従業員検索（ID、名前、部署等）
- 部署・役職情報取得
- キャッシュ機構（API呼び出し削減）
- CSV/JSON出力

注意: KOT APIの仕様に応じて、エンドポイント・認証方式・パラメータを調整してください
"""

import os
import json
import csv
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import requests
from pathlib import Path


class KOTEmployeeClient:
    """KOT従業員情報クライアント"""

    def __init__(
        self,
        api_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        cache_enabled: bool = True,
        cache_duration_hours: int = 24,
    ):
        """
        初期化

        Args:
            api_endpoint: KOT APIエンドポイント（未指定の場合は環境変数KOT_API_ENDPOINTを使用）
            api_key: KOT API Key（未指定の場合は環境変数KOT_API_KEYを使用）
            cache_enabled: キャッシュを有効にするか
            cache_duration_hours: キャッシュの有効期限（時間）
        """
        self.api_endpoint = api_endpoint or os.getenv("KOT_API_ENDPOINT")
        self.api_key = api_key or os.getenv("KOT_API_KEY")

        if not self.api_endpoint or not self.api_key:
            raise ValueError("KOT APIエンドポイントとAPI Keyを設定してください")

        self.cache_enabled = cache_enabled
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.cache_dir = Path(".cache")
        self.cache_dir.mkdir(exist_ok=True)

    def _get_headers(self) -> Dict[str, str]:
        """
        APIリクエストヘッダーを取得

        TODO: 認証方式をKOT APIの仕様に合わせて調整してください
        - Bearer Token: {"Authorization": f"Bearer {self.api_key}"}
        - API Key Header: {"X-API-Key": self.api_key}
        - Basic認証等
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _get_cache_path(self, cache_key: str) -> Path:
        """キャッシュファイルパスを取得"""
        return self.cache_dir / f"employee_{cache_key}.json"

    def _load_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """キャッシュを読み込み"""
        if not self.cache_enabled:
            return None

        cache_path = self._get_cache_path(cache_key)
        if not cache_path.exists():
            return None

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # キャッシュ有効期限チェック
            cached_at = datetime.fromisoformat(cache_data["cached_at"])
            if datetime.now() - cached_at > self.cache_duration:
                return None

            return cache_data["data"]

        except Exception:
            return None

    def _save_cache(self, cache_key: str, data: Dict[str, Any]):
        """キャッシュを保存"""
        if not self.cache_enabled:
            return

        cache_path = self._get_cache_path(cache_key)
        cache_data = {"cached_at": datetime.now().isoformat(), "data": data}

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

    def get_employee_by_id(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """
        従業員IDで従業員情報を取得

        Args:
            employee_id: 従業員ID

        Returns:
            従業員情報、見つからない場合はNone

        TODO: エンドポイントとレスポンス形式をKOT APIの仕様に合わせて調整してください
        """
        cache_key = f"id_{employee_id}"
        cached = self._load_cache(cache_key)
        if cached:
            return cached

        try:
            # TODO: 実際のエンドポイントに変更
            url = f"{self.api_endpoint}/employees/{employee_id}"
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()

            data = response.json()
            self._save_cache(cache_key, data)
            return data

        except requests.RequestException as e:
            print(f"従業員情報取得エラー: {str(e)}")
            return None

    def search_employees(
        self,
        name: Optional[str] = None,
        department: Optional[str] = None,
        position: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        従業員を検索

        Args:
            name: 名前（部分一致）
            department: 部署名
            position: 役職名

        Returns:
            従業員情報のリスト

        TODO: エンドポイントとパラメータをKOT APIの仕様に合わせて調整してください
        """
        try:
            # TODO: 実際のエンドポイントに変更
            url = f"{self.api_endpoint}/employees/search"

            # 検索パラメータ
            params = {}
            if name:
                params["name"] = name
            if department:
                params["department"] = department
            if position:
                params["position"] = position

            response = requests.get(
                url, params=params, headers=self._get_headers(), timeout=10
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            print(f"従業員検索エラー: {str(e)}")
            return []

    def get_all_employees(self) -> List[Dict[str, Any]]:
        """
        全従業員情報を取得

        Returns:
            全従業員情報のリスト

        TODO: エンドポイントをKOT APIの仕様に合わせて調整してください
        """
        cache_key = "all_employees"
        cached = self._load_cache(cache_key)
        if cached:
            return cached

        try:
            # TODO: 実際のエンドポイントに変更
            url = f"{self.api_endpoint}/employees"
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()

            data = response.json()
            self._save_cache(cache_key, data)
            return data

        except requests.RequestException as e:
            print(f"全従業員情報取得エラー: {str(e)}")
            return []

    def export_to_csv(self, employees: List[Dict[str, Any]], output_path: str):
        """
        従業員情報をCSVに出力

        Args:
            employees: 従業員情報のリスト
            output_path: 出力ファイルパス

        TODO: フィールド名をKOT APIのレスポンス形式に合わせて調整してください
        """
        if not employees:
            print("出力するデータがありません")
            return

        # TODO: 実際のフィールド名に変更
        fieldnames = [
            "employee_id",
            "name",
            "department",
            "position",
            "email",
            "phone",
        ]

        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(employees)

        print(f"CSVファイルを出力しました: {output_path}")

    def export_to_json(self, employees: List[Dict[str, Any]], output_path: str):
        """
        従業員情報をJSONに出力

        Args:
            employees: 従業員情報のリスト
            output_path: 出力ファイルパス
        """
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(employees, f, ensure_ascii=False, indent=2)

        print(f"JSONファイルを出力しました: {output_path}")


# 使用例
if __name__ == "__main__":
    # 初期化
    client = KOTEmployeeClient()

    # 従業員IDで取得
    print("=== 従業員IDで取得 ===")
    employee = client.get_employee_by_id("E12345")
    if employee:
        print(json.dumps(employee, ensure_ascii=False, indent=2))

    # 名前で検索
    print("\n=== 名前で検索 ===")
    employees = client.search_employees(name="田中")
    print(f"検索結果: {len(employees)}件")
    for emp in employees[:3]:  # 最初の3件を表示
        print(f"  - {emp.get('name')} ({emp.get('department')})")

    # 全従業員取得
    print("\n=== 全従業員取得 ===")
    all_employees = client.get_all_employees()
    print(f"全従業員数: {len(all_employees)}人")

    # CSV出力
    if all_employees:
        client.export_to_csv(all_employees, "employees.csv")

    # JSON出力
    if all_employees:
        client.export_to_json(all_employees, "employees.json")
