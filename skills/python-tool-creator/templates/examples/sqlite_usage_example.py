"""
SQLiteストレージ使用例

基本的な使い方から応用パターンまでの実践例
"""

import sys
from pathlib import Path

# パス設定（テンプレートディレクトリをインポートパスに追加）
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlite_storage_base import SQLiteStorage
import pandas as pd
from datetime import datetime, timedelta


def example1_basic_crud():
    """
    例1: 基本的なCRUD操作
    """
    print("=== 例1: 基本的なCRUD操作 ===")

    storage = SQLiteStorage("data/example1.db")

    try:
        # テーブル作成
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE",
            "created_at": "TIMESTAMP",
            "updated_at": "TIMESTAMP"
        }
        storage.create_table("users", schema, indexes=["email"])

        # データ挿入
        user_id = storage.insert("users", {
            "name": "John Doe",
            "email": "john@example.com"
        })
        print(f"挿入成功: {user_id}行")

        # データ取得
        users = storage.select("users")
        print(f"全ユーザー: {users}")

        # データ更新
        storage.update(
            "users",
            {"name": "John Updated"},
            {"email": "john@example.com"}
        )
        print("更新成功")

        # 論理削除
        storage.delete("users", {"email": "john@example.com"}, soft_delete=True)
        print("論理削除成功")

    finally:
        storage.close()


def example2_bulk_insert():
    """
    例2: 一括挿入とDataFrame統合
    """
    print("\n=== 例2: 一括挿入とDataFrame統合 ===")

    storage = SQLiteStorage("data/example2.db")

    try:
        # テーブル作成
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "product_name": "TEXT NOT NULL",
            "price": "REAL",
            "quantity": "INTEGER",
            "created_at": "TIMESTAMP"
        }
        storage.create_table("products", schema)

        # 一括挿入（辞書のリスト）
        products = [
            {"product_name": "Apple", "price": 100, "quantity": 50},
            {"product_name": "Banana", "price": 80, "quantity": 30},
            {"product_name": "Orange", "price": 120, "quantity": 40}
        ]
        storage.insert("products", products)
        print(f"{len(products)}件の商品を挿入")

        # DataFrameから一括挿入
        df_new = pd.DataFrame([
            {"product_name": "Grape", "price": 200, "quantity": 20},
            {"product_name": "Melon", "price": 300, "quantity": 10}
        ])
        storage.bulk_insert_from_df("products", df_new)
        print(f"DataFrameから{len(df_new)}件を挿入")

        # DataFrame形式で取得
        df_all = storage.to_dataframe("products")
        print(f"\n全商品データ:\n{df_all}")

        # 条件付き取得（価格100以上）
        df_filtered = storage.to_dataframe(
            "products",
            sql="SELECT * FROM products WHERE price >= 100"
        )
        print(f"\n価格100以上の商品:\n{df_filtered}")

    finally:
        storage.close()


def example3_aggregation():
    """
    例3: 集計クエリとグルーピング
    """
    print("\n=== 例3: 集計クエリとグルーピング ===")

    storage = SQLiteStorage("data/example3.db")

    try:
        # テーブル作成
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "category": "TEXT NOT NULL",
            "product_name": "TEXT NOT NULL",
            "price": "REAL",
            "sales_count": "INTEGER"
        }
        storage.create_table("sales", schema)

        # サンプルデータ挿入
        sales_data = [
            {"category": "Fruit", "product_name": "Apple", "price": 100, "sales_count": 50},
            {"category": "Fruit", "product_name": "Banana", "price": 80, "sales_count": 30},
            {"category": "Vegetable", "product_name": "Carrot", "price": 60, "sales_count": 40},
            {"category": "Vegetable", "product_name": "Tomato", "price": 90, "sales_count": 35},
            {"category": "Fruit", "product_name": "Orange", "price": 120, "sales_count": 25}
        ]
        storage.insert("sales", sales_data)

        # カテゴリ別集計
        result = storage.query("""
            SELECT
                category,
                COUNT(*) as product_count,
                SUM(sales_count) as total_sales,
                AVG(price) as avg_price
            FROM sales
            GROUP BY category
        """)
        print(f"\nカテゴリ別集計:\n{pd.DataFrame(result)}")

        # 売上TOP3
        top3 = storage.query("""
            SELECT
                product_name,
                price * sales_count as revenue
            FROM sales
            ORDER BY revenue DESC
            LIMIT 3
        """)
        print(f"\n売上TOP3:\n{pd.DataFrame(top3)}")

    finally:
        storage.close()


def example4_api_data_storage():
    """
    例4: API取得データの保存（rest_api_client_base.pyとの連携想定）
    """
    print("\n=== 例4: API取得データの保存 ===")

    storage = SQLiteStorage("data/example4.db")

    try:
        # APIデータ保存テーブル
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "api_name": "TEXT NOT NULL",
            "data_json": "TEXT",
            "status_code": "INTEGER",
            "fetched_at": "TIMESTAMP"
        }
        storage.create_table("api_history", schema, indexes=["api_name", "fetched_at"])

        # 擬似的なAPI取得データ
        api_data = {
            "api_name": "users_api",
            "data_json": '{"users": [{"id": 1, "name": "Alice"}]}',
            "status_code": 200,
            "fetched_at": datetime.now().isoformat()
        }
        storage.insert("api_history", api_data, auto_timestamp=False)
        print("APIデータを保存")

        # 過去7日間のAPI取得履歴
        seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
        history = storage.query(
            "SELECT * FROM api_history WHERE fetched_at >= ? ORDER BY fetched_at DESC",
            params=(seven_days_ago,)
        )
        print(f"\n過去7日間の履歴: {len(history)}件")

    finally:
        storage.close()


def example5_transaction():
    """
    例5: トランザクション管理
    """
    print("\n=== 例5: トランザクション管理 ===")

    # auto_commit=Falseで初期化（明示的にコミットが必要）
    storage = SQLiteStorage("data/example5.db")
    storage.auto_commit = False
    storage._connect()  # 再接続して設定を反映

    try:
        # テーブル作成
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "account_name": "TEXT NOT NULL",
            "balance": "REAL"
        }
        storage.create_table("accounts", schema)
        storage.commit()

        # トランザクション開始
        storage.begin_transaction()

        try:
            # 口座A: 1000円減少
            storage.update(
                "accounts",
                {"balance": 9000},
                {"account_name": "Account A"}
            )

            # 口座B: 1000円増加
            storage.update(
                "accounts",
                {"balance": 6000},
                {"account_name": "Account B"}
            )

            # コミット
            storage.commit()
            print("トランザクションコミット成功")

        except Exception as e:
            # ロールバック
            storage.rollback()
            print(f"トランザクションロールバック: {e}")

    finally:
        storage.close()


def example6_data_migration():
    """
    例6: CSVからSQLiteへの移行
    """
    print("\n=== 例6: CSVからSQLiteへの移行 ===")

    storage = SQLiteStorage("data/example6.db")

    try:
        # CSVファイル読み込み（擬似的に作成）
        csv_data = pd.DataFrame([
            {"id": 1, "name": "Alice", "department": "Sales"},
            {"id": 2, "name": "Bob", "department": "Engineering"},
            {"id": 3, "name": "Charlie", "department": "Marketing"}
        ])

        # CSVデータをSQLiteに保存
        storage.bulk_insert_from_df("employees", csv_data, if_exists="replace")
        print(f"{len(csv_data)}件のCSVデータを移行")

        # 確認
        df = storage.to_dataframe("employees")
        print(f"\n移行後のデータ:\n{df}")

    finally:
        storage.close()


if __name__ == "__main__":
    # 全例を実行
    example1_basic_crud()
    example2_bulk_insert()
    example3_aggregation()
    example4_api_data_storage()
    example5_transaction()
    example6_data_migration()

    print("\n=== 全ての例の実行が完了しました ===")
