"""
SQLiteストレージベーステンプレート

ローカルデータベース（SQLite）保存用のテンプレート。
データの永続化、履歴管理、クエリ・集計機能を提供。
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, Any, List, Union
from pathlib import Path
import pandas as pd
from common.logger import setup_logger
from common.config_manager import ConfigManager


class SQLiteStorage:
    """SQLiteストレージクラス

    ローカルデータベース保存、CRUD操作、データ変換、クエリ実行機能を提供
    """

    def __init__(
        self,
        db_path: str = "data.db",
        config_path: str = "config.yaml"
    ):
        """
        初期化

        Args:
            db_path: データベースファイルパス
            config_path: 設定ファイルパス
        """
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config

        # ロガー初期化
        self.logger = setup_logger(
            name="sqlite_storage",
            log_level=self.config.get("logging", {}).get("level", "INFO"),
            config=self.config
        )

        # SQLite設定取得
        self.sqlite_config = self.config.get("sqlite", {})
        self.db_path = db_path or self.sqlite_config.get("db_path", "data.db")

        # データベースディレクトリ作成
        db_dir = Path(self.db_path).parent
        if not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"データベースディレクトリ作成: {db_dir}")

        # データベース接続設定
        self.auto_commit = self.sqlite_config.get("auto_commit", True)
        self.check_same_thread = self.sqlite_config.get("check_same_thread", False)
        self.timeout = self.sqlite_config.get("timeout", 30)

        # 接続初期化
        self.conn: Optional[sqlite3.Connection] = None
        self._connect()

        self.logger.info(
            "SQLiteStorage初期化完了",
            context={"db_path": self.db_path}
        )

    def _connect(self) -> None:
        """
        データベースに接続
        """
        try:
            self.conn = sqlite3.connect(
                self.db_path,
                check_same_thread=self.check_same_thread,
                timeout=self.timeout
            )
            self.conn.row_factory = sqlite3.Row  # 辞書形式でアクセス可能

            if self.auto_commit:
                self.conn.isolation_level = None

            self.logger.debug(f"データベース接続成功: {self.db_path}")

        except Exception as e:
            self.logger.error(
                f"データベース接続エラー",
                context={"db_path": self.db_path, "error": str(e)},
                exc_info=True
            )
            raise

    def create_table(
        self,
        table_name: str,
        schema: Dict[str, str],
        indexes: Optional[List[str]] = None
    ) -> None:
        """
        テーブルを作成

        Args:
            table_name: テーブル名
            schema: カラム定義 {"column_name": "TYPE CONSTRAINTS"}
            indexes: インデックスを作成するカラムリスト
        """
        try:
            # スキーマSQL生成
            columns = []
            for col_name, col_def in schema.items():
                columns.append(f"{col_name} {col_def}")

            columns_sql = ", ".join(columns)
            create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"

            self.logger.debug(
                f"テーブル作成SQL",
                context={"sql": create_sql}
            )

            # テーブル作成
            self.conn.execute(create_sql)

            # インデックス作成
            if indexes:
                for index_col in indexes:
                    index_name = f"idx_{table_name}_{index_col}"
                    index_sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({index_col})"
                    self.conn.execute(index_sql)
                    self.logger.debug(f"インデックス作成: {index_name}")

            self.logger.info(
                f"テーブル作成成功",
                context={"table_name": table_name, "columns": len(schema)}
            )

        except Exception as e:
            self.logger.error(
                f"テーブル作成エラー",
                context={"table_name": table_name, "error": str(e)},
                exc_info=True
            )
            raise

    def insert(
        self,
        table_name: str,
        data: Union[Dict[str, Any], List[Dict[str, Any]]],
        auto_timestamp: bool = True
    ) -> int:
        """
        データを挿入

        Args:
            table_name: テーブル名
            data: 挿入データ（辞書または辞書のリスト）
            auto_timestamp: created_at/updated_atを自動設定

        Returns:
            挿入された行数
        """
        try:
            # 単一データを配列化
            if isinstance(data, dict):
                data = [data]

            if not data:
                return 0

            # タイムスタンプ追加
            if auto_timestamp:
                now = datetime.now().isoformat()
                for row in data:
                    if "created_at" not in row:
                        row["created_at"] = now
                    if "updated_at" not in row:
                        row["updated_at"] = now

            # INSERT SQL生成
            columns = list(data[0].keys())
            placeholders = ", ".join(["?" for _ in columns])
            columns_sql = ", ".join(columns)
            insert_sql = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"

            # バルク挿入
            values = [tuple(row.get(col) for col in columns) for row in data]
            cursor = self.conn.executemany(insert_sql, values)

            inserted_count = cursor.rowcount

            self.logger.info(
                f"データ挿入成功",
                context={"table_name": table_name, "count": inserted_count}
            )

            return inserted_count

        except Exception as e:
            self.logger.error(
                f"データ挿入エラー",
                context={"table_name": table_name, "error": str(e)},
                exc_info=True
            )
            raise

    def update(
        self,
        table_name: str,
        data: Dict[str, Any],
        condition: Dict[str, Any],
        auto_timestamp: bool = True
    ) -> int:
        """
        データを更新

        Args:
            table_name: テーブル名
            data: 更新データ
            condition: 更新条件
            auto_timestamp: updated_atを自動更新

        Returns:
            更新された行数
        """
        try:
            # タイムスタンプ更新
            if auto_timestamp and "updated_at" not in data:
                data["updated_at"] = datetime.now().isoformat()

            # UPDATE SQL生成
            set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
            where_clause = " AND ".join([f"{col} = ?" for col in condition.keys()])
            update_sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

            # パラメータ結合
            params = list(data.values()) + list(condition.values())

            cursor = self.conn.execute(update_sql, params)
            updated_count = cursor.rowcount

            self.logger.info(
                f"データ更新成功",
                context={"table_name": table_name, "count": updated_count}
            )

            return updated_count

        except Exception as e:
            self.logger.error(
                f"データ更新エラー",
                context={"table_name": table_name, "error": str(e)},
                exc_info=True
            )
            raise

    def delete(
        self,
        table_name: str,
        condition: Dict[str, Any],
        soft_delete: bool = True
    ) -> int:
        """
        データを削除

        Args:
            table_name: テーブル名
            condition: 削除条件
            soft_delete: 論理削除（deleted_atを設定）

        Returns:
            削除された行数
        """
        try:
            if soft_delete:
                # 論理削除（deleted_at設定）
                data = {"deleted_at": datetime.now().isoformat()}
                return self.update(table_name, data, condition, auto_timestamp=False)
            else:
                # 物理削除
                where_clause = " AND ".join([f"{col} = ?" for col in condition.keys()])
                delete_sql = f"DELETE FROM {table_name} WHERE {where_clause}"

                cursor = self.conn.execute(delete_sql, list(condition.values()))
                deleted_count = cursor.rowcount

                self.logger.info(
                    f"データ削除成功",
                    context={"table_name": table_name, "count": deleted_count}
                )

                return deleted_count

        except Exception as e:
            self.logger.error(
                f"データ削除エラー",
                context={"table_name": table_name, "error": str(e)},
                exc_info=True
            )
            raise

    def select(
        self,
        table_name: str,
        columns: Optional[List[str]] = None,
        condition: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        データを取得

        Args:
            table_name: テーブル名
            columns: 取得カラムリスト（Noneの場合は全カラム）
            condition: 検索条件
            order_by: ソート順（例: "created_at DESC"）
            limit: 取得件数制限
            offset: オフセット

        Returns:
            取得データリスト
        """
        try:
            # SELECT SQL生成
            columns_sql = ", ".join(columns) if columns else "*"
            select_sql = f"SELECT {columns_sql} FROM {table_name}"
            params = []

            # WHERE句
            if condition:
                where_clause = " AND ".join([f"{col} = ?" for col in condition.keys()])
                select_sql += f" WHERE {where_clause}"
                params.extend(condition.values())

            # ORDER BY句
            if order_by:
                select_sql += f" ORDER BY {order_by}"

            # LIMIT/OFFSET句
            if limit:
                select_sql += f" LIMIT {limit}"
            if offset:
                select_sql += f" OFFSET {offset}"

            # クエリ実行
            cursor = self.conn.execute(select_sql, params)
            rows = cursor.fetchall()

            # 辞書形式に変換
            result = [dict(row) for row in rows]

            self.logger.debug(
                f"データ取得成功",
                context={"table_name": table_name, "count": len(result)}
            )

            return result

        except Exception as e:
            self.logger.error(
                f"データ取得エラー",
                context={"table_name": table_name, "error": str(e)},
                exc_info=True
            )
            raise

    def query(
        self,
        sql: str,
        params: Optional[Union[tuple, List[Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        SQLクエリを実行

        Args:
            sql: SQLクエリ
            params: パラメータ（パラメータ化クエリ）

        Returns:
            クエリ結果
        """
        try:
            params = params or []
            cursor = self.conn.execute(sql, params)

            # SELECT文の場合は結果を返す
            if sql.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]

                self.logger.debug(
                    f"クエリ実行成功",
                    context={"sql": sql[:100], "count": len(result)}
                )

                return result
            else:
                # INSERT/UPDATE/DELETE等の場合は影響行数を返す
                self.logger.info(
                    f"クエリ実行成功",
                    context={"sql": sql[:100], "rowcount": cursor.rowcount}
                )

                return [{"rowcount": cursor.rowcount}]

        except Exception as e:
            self.logger.error(
                f"クエリ実行エラー",
                context={"sql": sql[:100], "error": str(e)},
                exc_info=True
            )
            raise

    def bulk_insert_from_df(
        self,
        table_name: str,
        df: pd.DataFrame,
        if_exists: str = "append"
    ) -> int:
        """
        DataFrameから一括挿入

        Args:
            table_name: テーブル名
            df: pandas DataFrame
            if_exists: 既存テーブルへの動作（'fail', 'replace', 'append'）

        Returns:
            挿入された行数
        """
        try:
            # DataFrameをSQLiteに保存
            df.to_sql(
                table_name,
                self.conn,
                if_exists=if_exists,
                index=False
            )

            inserted_count = len(df)

            self.logger.info(
                f"DataFrame一括挿入成功",
                context={"table_name": table_name, "count": inserted_count}
            )

            return inserted_count

        except Exception as e:
            self.logger.error(
                f"DataFrame一括挿入エラー",
                context={"table_name": table_name, "error": str(e)},
                exc_info=True
            )
            raise

    def to_dataframe(
        self,
        table_name: str,
        condition: Optional[Dict[str, Any]] = None,
        sql: Optional[str] = None
    ) -> pd.DataFrame:
        """
        SQLite → DataFrame変換

        Args:
            table_name: テーブル名
            condition: 検索条件
            sql: カスタムSQLクエリ（指定時はtable_name/conditionは無視）

        Returns:
            pandas DataFrame
        """
        try:
            if sql:
                # カスタムSQL
                df = pd.read_sql_query(sql, self.conn)
            else:
                # テーブル全体または条件付き取得
                if condition:
                    where_clause = " AND ".join([f"{col} = ?" for col in condition.keys()])
                    sql = f"SELECT * FROM {table_name} WHERE {where_clause}"
                    df = pd.read_sql_query(sql, self.conn, params=list(condition.values()))
                else:
                    df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)

            self.logger.debug(
                f"DataFrame変換成功",
                context={"table_name": table_name, "rows": len(df)}
            )

            return df

        except Exception as e:
            self.logger.error(
                f"DataFrame変換エラー",
                context={"table_name": table_name, "error": str(e)},
                exc_info=True
            )
            raise

    def table_exists(self, table_name: str) -> bool:
        """
        テーブルの存在確認

        Args:
            table_name: テーブル名

        Returns:
            テーブルが存在する場合True
        """
        try:
            sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
            cursor = self.conn.execute(sql, (table_name,))
            return cursor.fetchone() is not None

        except Exception as e:
            self.logger.error(
                f"テーブル存在確認エラー",
                context={"table_name": table_name, "error": str(e)},
                exc_info=True
            )
            raise

    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        テーブル情報を取得

        Args:
            table_name: テーブル名

        Returns:
            カラム情報リスト
        """
        try:
            cursor = self.conn.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            result = [dict(col) for col in columns]

            self.logger.debug(
                f"テーブル情報取得成功",
                context={"table_name": table_name, "columns": len(result)}
            )

            return result

        except Exception as e:
            self.logger.error(
                f"テーブル情報取得エラー",
                context={"table_name": table_name, "error": str(e)},
                exc_info=True
            )
            raise

    def begin_transaction(self) -> None:
        """
        トランザクション開始
        """
        if self.auto_commit:
            self.logger.warning("auto_commit=Trueのため、トランザクション管理は無効です")
            return

        self.conn.execute("BEGIN")
        self.logger.debug("トランザクション開始")

    def commit(self) -> None:
        """
        トランザクションコミット
        """
        if self.auto_commit:
            return

        self.conn.commit()
        self.logger.debug("トランザクションコミット")

    def rollback(self) -> None:
        """
        トランザクションロールバック
        """
        if self.auto_commit:
            return

        self.conn.rollback()
        self.logger.debug("トランザクションロールバック")

    def close(self) -> None:
        """
        データベース接続をクローズ
        """
        if self.conn:
            self.conn.close()
            self.logger.info("データベース接続クローズ")


# 使用例
if __name__ == "__main__":
    # SQLiteストレージの基本フロー
    storage = SQLiteStorage("data/app.db")

    try:
        # テーブル作成
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "email": "TEXT UNIQUE",
            "age": "INTEGER",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "deleted_at": "TIMESTAMP"
        }
        storage.create_table("users", schema, indexes=["email"])

        # データ挿入（単一）
        storage.insert("users", {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        })

        # データ挿入（一括）
        users = [
            {"name": "Alice", "email": "alice@example.com", "age": 25},
            {"name": "Bob", "email": "bob@example.com", "age": 35}
        ]
        storage.insert("users", users)

        # データ取得
        all_users = storage.select("users")
        print(f"全ユーザー数: {len(all_users)}")

        # 条件付き取得
        john = storage.select("users", condition={"name": "John Doe"})
        print(f"John: {john}")

        # データ更新
        storage.update(
            "users",
            {"age": 31},
            {"name": "John Doe"}
        )

        # 論理削除
        storage.delete("users", {"name": "Bob"}, soft_delete=True)

        # DataFrameから一括挿入
        df = pd.DataFrame([
            {"name": "Charlie", "email": "charlie@example.com", "age": 28},
            {"name": "Diana", "email": "diana@example.com", "age": 32}
        ])
        storage.bulk_insert_from_df("users", df)

        # DataFrame取得
        df_users = storage.to_dataframe("users")
        print(f"DataFrame行数: {len(df_users)}")
        print(df_users)

        # 集計クエリ
        result = storage.query(
            "SELECT COUNT(*) as count, AVG(age) as avg_age FROM users WHERE deleted_at IS NULL"
        )
        print(f"統計: {result}")

    finally:
        storage.close()
