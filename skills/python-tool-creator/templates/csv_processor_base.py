"""
CSV処理ベーステンプレート

CSVファイルの読み書き、データ変換、集計を容易にするテンプレート。
エンコーディング自動検出、大容量ファイル対応、pandas統合。
"""

import csv
import chardet
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from common.logger import setup_logger
from common.config_manager import ConfigManager


class CSVProcessor:
    """CSV処理クラス

    CSVファイルの読み書き、フィルタリング、集計、クレンジング機能を提供
    """

    def __init__(self, config_path: str = "config.yaml"):
        """
        初期化

        Args:
            config_path: 設定ファイルパス
        """
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config

        # ロガー初期化
        self.logger = setup_logger(
            name="csv_processor",
            log_level=self.config.get("logging", {}).get("level", "INFO"),
            config=self.config
        )

        # CSV設定取得
        self.csv_config = self.config.get("csv", {})
        self.default_encoding = self.csv_config.get("default_encoding", "utf-8")
        self.chunk_size = self.csv_config.get("chunk_size", 10000)
        self.delimiter = self.csv_config.get("delimiter", ",")
        self.quotechar = self.csv_config.get("quotechar", '"')

        self.logger.info("CSVProcessor初期化完了")

    def detect_encoding(self, file_path: str) -> str:
        """
        ファイルのエンコーディングを自動検出

        Args:
            file_path: ファイルパス

        Returns:
            検出されたエンコーディング
        """
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(100000)  # 最初の100KB読み込み
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                confidence = result['confidence']

                self.logger.debug(
                    f"エンコーディング検出: {encoding} (信頼度: {confidence:.2f})",
                    context={"file": file_path}
                )

                return encoding if encoding else self.default_encoding

        except Exception as e:
            self.logger.warning(
                f"エンコーディング検出失敗、デフォルト使用: {self.default_encoding}",
                context={"error": str(e)}
            )
            return self.default_encoding

    def read_csv(
        self,
        file_path: str,
        encoding: Optional[str] = None,
        use_chunks: bool = False,
        **kwargs
    ) -> Union[pd.DataFrame, pd.io.parsers.TextFileReader]:
        """
        CSVファイルを読み込み

        Args:
            file_path: CSVファイルパス
            encoding: エンコーディング（Noneの場合は自動検出）
            use_chunks: チャンク読み込みを使用するか
            **kwargs: pandas.read_csvの追加オプション

        Returns:
            DataFrameまたはTextFileReader（チャンク読み込み時）
        """
        try:
            # ファイル存在確認
            if not Path(file_path).exists():
                raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

            # エンコーディング自動検出
            if encoding is None:
                encoding = self.detect_encoding(file_path)

            self.logger.info(
                f"CSV読み込み開始",
                context={"file": file_path, "encoding": encoding}
            )

            # pandas.read_csvオプション設定
            read_options = {
                "encoding": encoding,
                "delimiter": self.delimiter,
                "quotechar": self.quotechar,
            }
            read_options.update(kwargs)

            # チャンク読み込み
            if use_chunks:
                read_options["chunksize"] = self.chunk_size
                df = pd.read_csv(file_path, **read_options)
                self.logger.info(
                    f"CSV読み込み完了（チャンクモード）",
                    context={"file": file_path, "chunk_size": self.chunk_size}
                )
            else:
                df = pd.read_csv(file_path, **read_options)
                self.logger.info(
                    f"CSV読み込み完了",
                    context={"file": file_path, "rows": len(df), "columns": len(df.columns)}
                )

            return df

        except Exception as e:
            self.logger.error(
                f"CSV読み込みエラー",
                context={"file": file_path, "error": str(e)},
                exc_info=True
            )
            raise

    def write_csv(
        self,
        df: pd.DataFrame,
        file_path: str,
        encoding: str = "utf-8",
        mode: str = "w",
        **kwargs
    ) -> None:
        """
        DataFrameをCSVファイルに書き込み

        Args:
            df: DataFrame
            file_path: 出力ファイルパス
            encoding: エンコーディング
            mode: 書き込みモード（'w': 上書き, 'a': 追記）
            **kwargs: pandas.to_csvの追加オプション
        """
        try:
            # 出力ディレクトリ作成
            output_dir = Path(file_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            self.logger.info(
                f"CSV書き込み開始",
                context={"file": file_path, "rows": len(df), "mode": mode}
            )

            # pandas.to_csvオプション設定
            write_options = {
                "encoding": encoding,
                "index": False,
                "mode": mode,
                "sep": self.delimiter,
                "quotechar": self.quotechar,
            }
            write_options.update(kwargs)

            # 追記モードの場合、ヘッダーは1回目のみ
            if mode == 'a' and Path(file_path).exists():
                write_options["header"] = False

            df.to_csv(file_path, **write_options)

            self.logger.info(
                f"CSV書き込み完了",
                context={"file": file_path, "rows": len(df)}
            )

        except Exception as e:
            self.logger.error(
                f"CSV書き込みエラー",
                context={"file": file_path, "error": str(e)},
                exc_info=True
            )
            raise

    def filter_data(
        self,
        df: pd.DataFrame,
        conditions: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        データフィルタリング

        Args:
            df: DataFrame
            conditions: フィルタ条件
                例: {"age": ">= 20", "city": "Tokyo"}

        Returns:
            フィルタリング後のDataFrame
        """
        try:
            self.logger.debug(
                f"データフィルタリング開始",
                context={"conditions": conditions}
            )

            filtered_df = df.copy()

            for column, condition in conditions.items():
                if column not in filtered_df.columns:
                    self.logger.warning(
                        f"カラムが存在しません: {column}",
                        context={"available_columns": list(filtered_df.columns)}
                    )
                    continue

                # 条件式解析
                if isinstance(condition, str) and any(op in condition for op in ['>=', '<=', '>', '<', '==']):
                    # 演算子による条件
                    filtered_df = filtered_df.query(f"{column} {condition}")
                else:
                    # 完全一致
                    filtered_df = filtered_df[filtered_df[column] == condition]

            self.logger.info(
                f"フィルタリング完了",
                context={"before": len(df), "after": len(filtered_df)}
            )

            return filtered_df

        except Exception as e:
            self.logger.error(
                f"フィルタリングエラー",
                context={"error": str(e)},
                exc_info=True
            )
            raise

    def aggregate_data(
        self,
        df: pd.DataFrame,
        group_by: List[str],
        aggregations: Dict[str, Union[str, List[str]]]
    ) -> pd.DataFrame:
        """
        データ集計

        Args:
            df: DataFrame
            group_by: グループ化するカラムのリスト
            aggregations: 集計定義
                例: {"salary": "mean", "count": "size", "sales": ["sum", "mean"]}

        Returns:
            集計後のDataFrame
        """
        try:
            self.logger.debug(
                f"データ集計開始",
                context={"group_by": group_by, "aggregations": aggregations}
            )

            # グループ化
            grouped = df.groupby(group_by)

            # 集計実行
            aggregated = grouped.agg(aggregations)

            # カラム名をフラット化
            if isinstance(aggregated.columns, pd.MultiIndex):
                aggregated.columns = ['_'.join(col).strip() for col in aggregated.columns.values]

            # インデックスをリセット
            aggregated = aggregated.reset_index()

            self.logger.info(
                f"集計完了",
                context={"groups": len(aggregated)}
            )

            return aggregated

        except Exception as e:
            self.logger.error(
                f"集計エラー",
                context={"error": str(e)},
                exc_info=True
            )
            raise

    def clean_data(
        self,
        df: pd.DataFrame,
        rules: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        データクレンジング

        Args:
            df: DataFrame
            rules: クレンジングルール
                例: {
                    "remove_duplicates": True,
                    "drop_na": ["column1", "column2"],
                    "fill_na": {"column3": 0},
                    "strip_whitespace": ["name", "address"],
                    "convert_types": {"age": "int", "price": "float"}
                }

        Returns:
            クレンジング後のDataFrame
        """
        try:
            self.logger.debug(
                f"データクレンジング開始",
                context={"rules": list(rules.keys())}
            )

            cleaned_df = df.copy()

            # 重複削除
            if rules.get("remove_duplicates", False):
                before = len(cleaned_df)
                cleaned_df = cleaned_df.drop_duplicates()
                self.logger.debug(f"重複削除: {before} → {len(cleaned_df)}")

            # 欠損値削除
            if "drop_na" in rules:
                before = len(cleaned_df)
                cleaned_df = cleaned_df.dropna(subset=rules["drop_na"])
                self.logger.debug(f"欠損値削除: {before} → {len(cleaned_df)}")

            # 欠損値埋め
            if "fill_na" in rules:
                cleaned_df = cleaned_df.fillna(rules["fill_na"])

            # 空白削除
            if "strip_whitespace" in rules:
                for column in rules["strip_whitespace"]:
                    if column in cleaned_df.columns:
                        cleaned_df[column] = cleaned_df[column].str.strip()

            # 型変換
            if "convert_types" in rules:
                for column, dtype in rules["convert_types"].items():
                    if column in cleaned_df.columns:
                        cleaned_df[column] = cleaned_df[column].astype(dtype)

            self.logger.info(
                f"クレンジング完了",
                context={"before": len(df), "after": len(cleaned_df)}
            )

            return cleaned_df

        except Exception as e:
            self.logger.error(
                f"クレンジングエラー",
                context={"error": str(e)},
                exc_info=True
            )
            raise


# 使用例
if __name__ == "__main__":
    # CSV処理の基本フロー
    processor = CSVProcessor()

    # CSV読み込み
    df = processor.read_csv("input.csv")

    # データクレンジング
    cleaned = processor.clean_data(df, {
        "remove_duplicates": True,
        "drop_na": ["id", "name"],
        "strip_whitespace": ["name", "address"],
        "convert_types": {"age": "int", "price": "float"}
    })

    # フィルタリング
    filtered = processor.filter_data(cleaned, {
        "age": ">= 20",
        "city": "Tokyo"
    })

    # 集計
    aggregated = processor.aggregate_data(
        filtered,
        group_by=["department"],
        aggregations={"salary": ["mean", "sum"], "count": "size"}
    )

    # CSV出力
    processor.write_csv(aggregated, "output.csv")

    print("CSV処理完了")
