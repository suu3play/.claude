# SQLite Storage Base Template

ローカルデータベース（SQLite）保存用のPythonテンプレート。データの永続化、履歴管理、クエリ・集計機能を提供します。

## 目次

- [概要](#概要)
- [主な機能](#主な機能)
- [インストール](#インストール)
- [基本的な使い方](#基本的な使い方)
- [詳細な機能](#詳細な機能)
- [設定ファイル](#設定ファイル)
- [他テンプレートとの連携](#他テンプレートとの連携)
- [ユースケース](#ユースケース)

## 概要

`sqlite_storage_base.py`は、SQLiteデータベースを使用したデータ永続化を簡単に実現するためのテンプレートです。

### 用途

- 取得データのローカルDB保存
- データの永続化
- 履歴管理
- クエリ・集計

### 特徴

- シンプルなAPI設計
- DataFrame統合（pandas）
- 自動タイムスタンプ管理
- トランザクション対応
- 論理削除対応
- 既存の共通モジュール（logger、config_manager）と統合

## 主な機能

### 1. データベース管理

- SQLiteデータベース作成
- テーブル自動生成（スキーマ定義から）
- インデックス管理
- テーブル存在確認

### 2. CRUD操作

- **Create**: データ挿入（単一・一括）
- **Read**: データ取得（条件指定、ソート、ページング）
- **Update**: データ更新
- **Delete**: データ削除（論理削除・物理削除）

### 3. データ変換

- DataFrame → SQLite保存
- SQLite → DataFrame取得
- JSON → SQLite保存（データフィールドとして）

### 4. クエリ実行

- SQLクエリ実行
- パラメータ化クエリ
- トランザクション管理
- 集計クエリ（COUNT、SUM、AVG等）

### 5. データ管理

- 自動タイムスタンプ（created_at、updated_at）
- 論理削除対応（deleted_at）
- テーブル情報取得

## インストール

### 必要なライブラリ

```bash
pip install pandas pyyaml python-dotenv
```

### ファイル構成

```
project/
├── sqlite_storage_base.py      # メインテンプレート
├── common/
│   ├── logger.py               # ロガー（既存）
│   └── config_manager.py       # 設定管理（既存）
├── config.yaml                 # 設定ファイル
└── examples/
    ├── sqlite_config_example.yaml      # 設定ファイル例
    └── sqlite_usage_example.py         # 使用例
```

## 基本的な使い方

### 1. 初期化

```python
from sqlite_storage_base import SQLiteStorage

# デフォルト設定で初期化
storage = SQLiteStorage("data/app.db")

# 設定ファイルを指定
storage = SQLiteStorage(
    db_path="data/app.db",
    config_path="config.yaml"
)
```

### 2. テーブル作成

```python
# スキーマ定義
schema = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "name": "TEXT NOT NULL",
    "email": "TEXT UNIQUE",
    "age": "INTEGER",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "deleted_at": "TIMESTAMP"
}

# テーブル作成（インデックス付き）
storage.create_table("users", schema, indexes=["email"])
```

### 3. データ挿入

```python
# 単一データ挿入
storage.insert("users", {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
})

# 一括挿入
users = [
    {"name": "Alice", "email": "alice@example.com", "age": 25},
    {"name": "Bob", "email": "bob@example.com", "age": 35}
]
storage.insert("users", users)
```

### 4. データ取得

```python
# 全件取得
all_users = storage.select("users")

# 条件付き取得
john = storage.select("users", condition={"name": "John Doe"})

# ソート・制限付き取得
recent_users = storage.select(
    "users",
    order_by="created_at DESC",
    limit=10
)
```

### 5. データ更新

```python
storage.update(
    "users",
    {"age": 31},
    {"name": "John Doe"}
)
```

### 6. データ削除

```python
# 論理削除（deleted_atを設定）
storage.delete("users", {"name": "Bob"}, soft_delete=True)

# 物理削除
storage.delete("users", {"name": "Bob"}, soft_delete=False)
```

### 7. クローズ

```python
storage.close()
```

## 詳細な機能

### DataFrame統合

#### DataFrameから一括挿入

```python
import pandas as pd

df = pd.DataFrame([
    {"name": "Charlie", "email": "charlie@example.com", "age": 28},
    {"name": "Diana", "email": "diana@example.com", "age": 32}
])

storage.bulk_insert_from_df("users", df, if_exists="append")
```

#### SQLiteからDataFrame取得

```python
# テーブル全体を取得
df = storage.to_dataframe("users")

# 条件付き取得
df = storage.to_dataframe("users", condition={"age": 30})

# カスタムSQLで取得
df = storage.to_dataframe(
    "users",
    sql="SELECT * FROM users WHERE age >= 30 ORDER BY created_at DESC"
)
```

### 集計クエリ

```python
# COUNT, AVG等の集計
result = storage.query("""
    SELECT
        COUNT(*) as count,
        AVG(age) as avg_age,
        MIN(age) as min_age,
        MAX(age) as max_age
    FROM users
    WHERE deleted_at IS NULL
""")

print(result)
# [{'count': 5, 'avg_age': 29.4, 'min_age': 25, 'max_age': 35}]
```

### トランザクション管理

```python
# auto_commit=Falseで初期化
storage = SQLiteStorage("data/app.db")
storage.auto_commit = False
storage._connect()

try:
    storage.begin_transaction()

    # 複数の操作
    storage.insert("users", {"name": "Alice", "email": "alice@example.com"})
    storage.update("users", {"age": 26}, {"name": "Alice"})

    # コミット
    storage.commit()

except Exception as e:
    # ロールバック
    storage.rollback()
    raise
finally:
    storage.close()
```

### テーブル情報取得

```python
# テーブル存在確認
if storage.table_exists("users"):
    print("usersテーブルは存在します")

# テーブル情報取得
table_info = storage.get_table_info("users")
print(table_info)
# [{'cid': 0, 'name': 'id', 'type': 'INTEGER', ...}, ...]
```

## 設定ファイル

### config.yaml例

```yaml
# ロギング設定
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/sqlite_storage.log"

# SQLite設定
sqlite:
  db_path: "data/app.db"
  auto_commit: true
  check_same_thread: false
  timeout: 30

  # テーブル定義（オプション）
  tables:
    users:
      schema:
        id: INTEGER PRIMARY KEY AUTOINCREMENT
        name: TEXT NOT NULL
        email: TEXT UNIQUE NOT NULL
        created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      indexes:
        - email
```

### 設定項目

| 項目 | 説明 | デフォルト値 |
|------|------|-------------|
| `db_path` | データベースファイルパス | `data.db` |
| `auto_commit` | 自動コミット | `true` |
| `check_same_thread` | スレッドチェック | `false` |
| `timeout` | タイムアウト（秒） | `30` |

## 他テンプレートとの連携

### 1. REST API Client との連携

API取得データをSQLiteに保存する例：

```python
from rest_api_client_base import RestAPIClient
from sqlite_storage_base import SQLiteStorage

# API取得
client = RestAPIClient("https://api.example.com")
users = client.get("/users")

# SQLiteに保存
storage = SQLiteStorage("data/api_data.db")
storage.insert("users", users)
```

### 2. CSV Processor との連携

CSV読み込みデータをSQLiteに移行する例：

```python
from csv_processor_base import CSVProcessor
from sqlite_storage_base import SQLiteStorage

# CSV読み込み
processor = CSVProcessor("data.csv")
df = processor.read_csv()

# SQLiteに保存
storage = SQLiteStorage("data/app.db")
storage.bulk_insert_from_df("data_table", df)
```

### 3. KOT Attendance との連携

勤怠データをSQLiteに蓄積する例：

```python
from kot_attendance_base import KOTAttendanceClient
from sqlite_storage_base import SQLiteStorage

# 勤怠データ取得
kot = KOTAttendanceClient()
attendance_data = kot.get_attendance()

# 履歴として保存
storage = SQLiteStorage("data/attendance_history.db")
storage.insert("attendance_history", attendance_data)
```

## ユースケース

### 1. APIデータの永続化

REST APIから取得したデータを定期的にSQLiteに保存し、ローカルで履歴管理。

```python
import schedule
import time

def fetch_and_store():
    client = RestAPIClient("https://api.example.com")
    storage = SQLiteStorage("data/api_history.db")

    try:
        data = client.get("/data")
        storage.insert("api_data", data)
        print(f"{len(data)}件のデータを保存")
    finally:
        client.close()
        storage.close()

# 1時間ごとに実行
schedule.every().hour.do(fetch_and_store)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 2. CSVデータの集約

複数のCSVファイルを1つのSQLiteデータベースに統合。

```python
from pathlib import Path
import pandas as pd

storage = SQLiteStorage("data/consolidated.db")

for csv_file in Path("data/csv/").glob("*.csv"):
    df = pd.read_csv(csv_file)
    storage.bulk_insert_from_df("consolidated_data", df, if_exists="append")
    print(f"{csv_file.name}を統合")

storage.close()
```

### 3. 日次データの履歴管理

日次で取得したデータを履歴として蓄積し、後で分析。

```python
from datetime import datetime

storage = SQLiteStorage("data/daily_history.db")

# 日次データ取得（擬似コード）
daily_data = fetch_daily_data()

# タイムスタンプ付きで保存
daily_data["fetched_date"] = datetime.now().date().isoformat()
storage.insert("daily_records", daily_data)

# 過去30日間のデータを分析
df = storage.to_dataframe(
    "daily_records",
    sql="""
        SELECT * FROM daily_records
        WHERE fetched_date >= date('now', '-30 days')
        ORDER BY fetched_date
    """
)

print(df.describe())
```

### 4. データ分析基盤

SQLiteに蓄積したデータをpandasで分析。

```python
storage = SQLiteStorage("data/analytics.db")

# データ取得
df = storage.to_dataframe("sales")

# pandas分析
monthly_sales = df.groupby(df['date'].str[:7])['amount'].sum()
print(monthly_sales)

# 可視化（例）
import matplotlib.pyplot as plt
monthly_sales.plot(kind='bar')
plt.show()
```

## トラブルシューティング

### データベースロックエラー

```python
# timeout値を増やす
storage.timeout = 60
```

### 同時アクセスエラー

```python
# check_same_threadをFalseに設定
storage.check_same_thread = False
```

## ライセンス

このテンプレートは自由に使用・改変できます。

## 関連ファイル

- [sqlite_storage_base.py](sqlite_storage_base.py) - メインテンプレート
- [sqlite_config_example.yaml](examples/sqlite_config_example.yaml) - 設定ファイル例
- [sqlite_usage_example.py](examples/sqlite_usage_example.py) - 使用例コード
- [common/logger.py](common/logger.py) - ロガーモジュール
- [common/config_manager.py](common/config_manager.py) - 設定管理モジュール
