"""
ロギング共通モジュール

標準的なロギング設定、ファイル・コンソール出力、レベル別フォーマット
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler
from datetime import datetime


class Logger:
    """ロガークラス"""

    def __init__(
        self,
        name: str = __name__,
        log_level: str = "INFO",
        log_file: Optional[str] = None,
        log_dir: str = "logs",
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        enable_console: bool = True,
        enable_file: bool = True,
    ):
        """
        初期化

        Args:
            name: ロガー名
            log_level: ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
            log_file: ログファイル名（未指定の場合は自動生成）
            log_dir: ログディレクトリ
            max_bytes: ログファイルの最大サイズ
            backup_count: バックアップファイル数
            enable_console: コンソール出力を有効にするか
            enable_file: ファイル出力を有効にするか
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # 既存のハンドラーをクリア
        self.logger.handlers.clear()

        # フォーマッター設定
        self.console_formatter = logging.Formatter(
            fmt="[%(levelname)s] %(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        self.file_formatter = logging.Formatter(
            fmt="[%(levelname)s] %(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # コンソールハンドラー
        if enable_console:
            self._add_console_handler()

        # ファイルハンドラー
        if enable_file:
            self._add_file_handler(log_file, log_dir, max_bytes, backup_count)

    def _add_console_handler(self):
        """コンソールハンドラーを追加"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(console_handler)

    def _add_file_handler(
        self,
        log_file: Optional[str],
        log_dir: str,
        max_bytes: int,
        backup_count: int,
    ):
        """ファイルハンドラーを追加（ローテーション対応）"""
        # ログディレクトリ作成
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)

        # ログファイル名設定
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d")
            log_file = f"app_{timestamp}.log"

        file_path = log_path / log_file

        # ローテーションファイルハンドラー
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str):
        """DEBUGログ出力"""
        self.logger.debug(message)

    def info(self, message: str):
        """INFOログ出力"""
        self.logger.info(message)

    def warning(self, message: str):
        """WARNINGログ出力"""
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """ERRORログ出力"""
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: bool = False):
        """CRITICALログ出力"""
        self.logger.critical(message, exc_info=exc_info)

    def exception(self, message: str):
        """例外情報付きERRORログ出力"""
        self.logger.exception(message)

    def set_level(self, level: str):
        """
        ログレベルを変更

        Args:
            level: ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        """
        self.logger.setLevel(getattr(logging, level.upper()))


def setup_logger(
    name: str = __name__,
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_dir: str = "logs",
    enable_console: bool = True,
    enable_file: bool = True,
) -> Logger:
    """
    ロガーをセットアップ

    Args:
        name: ロガー名
        log_level: ログレベル
        log_file: ログファイル名
        log_dir: ログディレクトリ
        enable_console: コンソール出力を有効にするか
        enable_file: ファイル出力を有効にするか

    Returns:
        Loggerインスタンス
    """
    return Logger(
        name=name,
        log_level=log_level,
        log_file=log_file,
        log_dir=log_dir,
        enable_console=enable_console,
        enable_file=enable_file,
    )


# 使用例
if __name__ == "__main__":
    # ロガーセットアップ
    logger = setup_logger(
        name="sample_app",
        log_level="DEBUG",
        log_file="sample.log",
    )

    # 各レベルのログ出力
    logger.debug("これはデバッグメッセージです")
    logger.info("これは情報メッセージです")
    logger.warning("これは警告メッセージです")
    logger.error("これはエラーメッセージです")
    logger.critical("これは重大エラーメッセージです")

    # 例外ログ
    try:
        result = 10 / 0
    except Exception:
        logger.exception("例外が発生しました")

    # ログレベル変更
    logger.set_level("WARNING")
    logger.info("このメッセージは表示されません（WARNINGレベル以下のため）")
    logger.warning("このメッセージは表示されます")

    print("\nログファイルは ./logs/sample.log に出力されています")

    # クリーンアップ（テスト用）
    import shutil
    log_path = Path("logs")
    if log_path.exists():
        shutil.rmtree(log_path)
