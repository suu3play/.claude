"""
勤怠情報取得ベーステンプレート（KOT連携）

社内システム(KOT)から勤怠データを取得するベース実装
- 勤怠データ取得（期間指定）
- 集計・分析機能
- 残業時間計算
- CSV出力対応

注意: KOT APIの仕様に応じて、エンドポイント・認証方式・パラメータを調整してください
"""

import os
import json
import csv
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta, date
import requests
from pathlib import Path


class KOTAttendanceClient:
    """KOT勤怠情報クライアント"""

    def __init__(
        self,
        api_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        初期化

        Args:
            api_endpoint: KOT APIエンドポイント（未指定の場合は環境変数KOT_API_ENDPOINTを使用）
            api_key: KOT API Key（未指定の場合は環境変数KOT_API_KEYを使用）
        """
        self.api_endpoint = api_endpoint or os.getenv("KOT_API_ENDPOINT")
        self.api_key = api_key or os.getenv("KOT_API_KEY")

        if not self.api_endpoint or not self.api_key:
            raise ValueError("KOT APIエンドポイントとAPI Keyを設定してください")

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

    def get_attendance_by_employee(
        self,
        employee_id: str,
        start_date: date,
        end_date: date,
    ) -> List[Dict[str, Any]]:
        """
        従業員の勤怠データを取得

        Args:
            employee_id: 従業員ID
            start_date: 開始日
            end_date: 終了日

        Returns:
            勤怠データのリスト

        TODO: エンドポイントとレスポンス形式をKOT APIの仕様に合わせて調整してください
        """
        try:
            # TODO: 実際のエンドポイントに変更
            url = f"{self.api_endpoint}/attendance/{employee_id}"

            params = {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            }

            response = requests.get(
                url, params=params, headers=self._get_headers(), timeout=30
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            print(f"勤怠データ取得エラー: {str(e)}")
            return []

    def get_attendance_by_department(
        self,
        department: str,
        start_date: date,
        end_date: date,
    ) -> List[Dict[str, Any]]:
        """
        部署の勤怠データを取得

        Args:
            department: 部署名
            start_date: 開始日
            end_date: 終了日

        Returns:
            勤怠データのリスト

        TODO: エンドポイントとレスポンス形式をKOT APIの仕様に合わせて調整してください
        """
        try:
            # TODO: 実際のエンドポイントに変更
            url = f"{self.api_endpoint}/attendance/department/{department}"

            params = {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            }

            response = requests.get(
                url, params=params, headers=self._get_headers(), timeout=30
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            print(f"勤怠データ取得エラー: {str(e)}")
            return []

    def calculate_overtime(
        self, attendance_records: List[Dict[str, Any]], standard_hours: float = 8.0
    ) -> Dict[str, Any]:
        """
        残業時間を計算

        Args:
            attendance_records: 勤怠データのリスト
            standard_hours: 標準労働時間（デフォルト: 8時間）

        Returns:
            集計結果

        TODO: フィールド名と計算ロジックをKOT APIのレスポンス形式に合わせて調整してください
        """
        total_work_hours = 0.0
        total_overtime_hours = 0.0
        work_days = 0

        for record in attendance_records:
            # TODO: 実際のフィールド名に変更
            work_hours = record.get("work_hours", 0.0)
            total_work_hours += work_hours

            if work_hours > standard_hours:
                total_overtime_hours += work_hours - standard_hours
                work_days += 1
            elif work_hours > 0:
                work_days += 1

        return {
            "total_work_hours": round(total_work_hours, 2),
            "total_overtime_hours": round(total_overtime_hours, 2),
            "work_days": work_days,
            "average_work_hours": (
                round(total_work_hours / work_days, 2) if work_days > 0 else 0.0
            ),
            "average_overtime_hours": (
                round(total_overtime_hours / work_days, 2) if work_days > 0 else 0.0
            ),
        }

    def aggregate_by_employee(
        self, attendance_records: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        従業員ごとに勤怠データを集計

        Args:
            attendance_records: 勤怠データのリスト

        Returns:
            従業員IDをキーとした集計結果

        TODO: フィールド名をKOT APIのレスポンス形式に合わせて調整してください
        """
        employee_data: Dict[str, List[Dict[str, Any]]] = {}

        for record in attendance_records:
            # TODO: 実際のフィールド名に変更
            employee_id = record.get("employee_id")
            if employee_id:
                if employee_id not in employee_data:
                    employee_data[employee_id] = []
                employee_data[employee_id].append(record)

        # 各従業員の集計
        result = {}
        for employee_id, records in employee_data.items():
            result[employee_id] = self.calculate_overtime(records)

        return result

    def get_monthly_attendance(
        self, employee_id: str, year: int, month: int
    ) -> List[Dict[str, Any]]:
        """
        月次勤怠データを取得

        Args:
            employee_id: 従業員ID
            year: 年
            month: 月

        Returns:
            月次勤怠データ
        """
        # 月初と月末を計算
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)

        return self.get_attendance_by_employee(employee_id, start_date, end_date)

    def export_to_csv(
        self, attendance_records: List[Dict[str, Any]], output_path: str
    ):
        """
        勤怠データをCSVに出力

        Args:
            attendance_records: 勤怠データのリスト
            output_path: 出力ファイルパス

        TODO: フィールド名をKOT APIのレスポンス形式に合わせて調整してください
        """
        if not attendance_records:
            print("出力するデータがありません")
            return

        # TODO: 実際のフィールド名に変更
        fieldnames = [
            "date",
            "employee_id",
            "employee_name",
            "check_in",
            "check_out",
            "work_hours",
            "break_hours",
            "overtime_hours",
            "notes",
        ]

        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(attendance_records)

        print(f"CSVファイルを出力しました: {output_path}")

    def export_summary_to_csv(
        self, summary_data: Dict[str, Dict[str, Any]], output_path: str
    ):
        """
        集計データをCSVに出力

        Args:
            summary_data: 集計データ（従業員IDをキーとした辞書）
            output_path: 出力ファイルパス
        """
        if not summary_data:
            print("出力するデータがありません")
            return

        fieldnames = [
            "employee_id",
            "total_work_hours",
            "total_overtime_hours",
            "work_days",
            "average_work_hours",
            "average_overtime_hours",
        ]

        rows = []
        for employee_id, data in summary_data.items():
            row = {"employee_id": employee_id, **data}
            rows.append(row)

        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"集計CSVファイルを出力しました: {output_path}")


# 使用例
if __name__ == "__main__":
    # 初期化
    client = KOTAttendanceClient()

    # 今月のデータを取得
    today = date.today()
    print(f"=== {today.year}年{today.month}月の勤怠データ取得 ===")
    attendance = client.get_monthly_attendance("E12345", today.year, today.month)
    print(f"取得件数: {len(attendance)}件")

    # 期間指定で取得
    print("\n=== 期間指定で取得 ===")
    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 31)
    attendance = client.get_attendance_by_employee("E12345", start_date, end_date)
    print(f"取得件数: {len(attendance)}件")

    # 残業時間計算
    if attendance:
        print("\n=== 残業時間計算 ===")
        summary = client.calculate_overtime(attendance)
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    # 部署ごとの勤怠データ取得
    print("\n=== 部署ごとの勤怠データ取得 ===")
    dept_attendance = client.get_attendance_by_department(
        "営業部", start_date, end_date
    )
    print(f"取得件数: {len(dept_attendance)}件")

    # 従業員ごとに集計
    if dept_attendance:
        print("\n=== 従業員ごとに集計 ===")
        aggregated = client.aggregate_by_employee(dept_attendance)
        for emp_id, data in aggregated.items():
            print(f"\n従業員ID: {emp_id}")
            print(json.dumps(data, ensure_ascii=False, indent=2))

        # 集計結果をCSV出力
        client.export_summary_to_csv(aggregated, "attendance_summary.csv")

    # 詳細データをCSV出力
    if attendance:
        client.export_to_csv(attendance, "attendance_detail.csv")
