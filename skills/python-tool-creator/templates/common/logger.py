"""
ロギング共通モジュール（拡張版）

標準的なロギング設定、ファイル・コンソール出力、レベル別フォーマット
JSON形式ログ、日付ベースローテーション、コンテキスト情報対応
"""

import logging
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """JSON形式のログフォーマッター"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # コンテキスト情報があれば追加
        if hasattr(record, "context"):
            log_data["context"] = record.context

        # 例外情報があれば追加
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


class Logger:
    """ロガークラス（拡張版）"""

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
        enable_json_file: bool = False,
        rotation_type: str = "size",  # "size" or "time"
        time_rotation: str = "midnight",  # "midnight", "H", "D", "W0-W6"
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        初期化

        Args:
            name: ロガー名
            log_level: ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
            log_file: ログファイル名（未指定の場合は自動生成）
            log_dir: ログディレクトリ
            max_bytes: ログファイルの最大サイズ（サイズベースローテーション時）
            backup_count: バックアップファイル数
            enable_console: コンソール出力を有効にするか
            enable_file: ファイル出力を有効にするか
            enable_json_file: JSON形式ファイル出力を有効にするか
            rotation_type: ローテーションタイプ（"size" or "time"）
            time_rotation: 時間ベースローテーション設定
            config: YAML設定から読み込んだ設定（オプション）
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # 既存のハンドラーをクリア
        self.logger.handlers.clear()

        # 設定を適用
        if config and "logging" in config:
            self._apply_config(config["logging"])
        else:
            # デフォルト設定
            self._apply_default_config(
                log_level,
                log_file,
                log_dir,
                max_bytes,
                backup_count,
                enable_console,
                enable_file,
                enable_json_file,
                rotation_type,
                time_rotation,
            )

    def _apply_config(self, logging_config: Dict[str, Any]):
        """YAML設定を適用"""
        # ログレベル設定
        level = logging_config.get("level", "INFO")
        self.logger.setLevel(getattr(logging, level.upper()))

        # フォーマット設定
        format_str = logging_config.get(
            "format", "[%(levelname)s] %(asctime)s - %(message)s"
        )
        datefmt = logging_config.get("datefmt", "%Y-%m-%d %H:%M:%S")

        self.console_formatter = logging.Formatter(fmt=format_str, datefmt=datefmt)
        self.file_formatter = logging.Formatter(
            fmt="[%(levelname)s] %(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s",
            datefmt=datefmt,
        )

        # ハンドラー設定
        handlers = logging_config.get("handlers", {})

        # コンソールハンドラー
        if handlers.get("console", {}).get("enabled", True):
            self._add_console_handler()

        # ファイルハンドラー
        if handlers.get("file", {}).get("enabled", True):
            file_config = handlers.get("file", {})
            self._add_file_handler(
                log_file=file_config.get("filename"),
                log_dir=file_config.get("log_dir", "logs"),
                max_bytes=file_config.get("max_bytes", 10 * 1024 * 1024),
                backup_count=file_config.get("backup_count", 5),
                rotation_type=file_config.get("rotation", "size"),
            )

        # JSON形式ファイルハンドラー
        if handlers.get("json_file", {}).get("enabled", False):
            json_config = handlers.get("json_file", {})
            self._add_json_file_handler(
                log_file=json_config.get("filename", "app.json"),
                log_dir=json_config.get("log_dir", "logs"),
                rotation_type=json_config.get("rotation", "daily"),
            )

    def _apply_default_config(
        self,
        log_level: str,
        log_file: Optional[str],
        log_dir: str,
        max_bytes: int,
        backup_count: int,
        enable_console: bool,
        enable_file: bool,
        enable_json_file: bool,
        rotation_type: str,
        time_rotation: str,
    ):
        """デフォルト設定を適用"""
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
            self._add_file_handler(
                log_file, log_dir, max_bytes, backup_count, rotation_type, time_rotation
            )

        # JSON形式ファイルハンドラー
        if enable_json_file:
            self._add_json_file_handler(log_dir=log_dir, rotation_type=rotation_type)

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
        rotation_type: str = "size",
        time_rotation: str = "midnight",
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

        # ローテーションタイプに応じてハンドラーを作成
        if rotation_type == "time":
            # 時間ベースローテーション
            file_handler = TimedRotatingFileHandler(
                file_path,
                when=time_rotation,
                backupCount=backup_count,
                encoding="utf-8",
            )
        else:
            # サイズベースローテーション
            file_handler = RotatingFileHandler(
                file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )

        file_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(file_handler)

    def _add_json_file_handler(
        self,
        log_file: str = "app.json",
        log_dir: str = "logs",
        rotation_type: str = "daily",
    ):
        """JSON形式ファイルハンドラーを追加"""
        # ログディレクトリ作成
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)

        file_path = log_path / log_file

        # 日付ベースローテーション
        if rotation_type == "daily":
            when = "midnight"
        elif rotation_type == "weekly":
            when = "W0"  # 月曜日
        elif rotation_type == "monthly":
            when = "midnight"
        else:
            when = "midnight"

        file_handler = TimedRotatingFileHandler(
            file_path,
            when=when,
            backupCount=30,  # 30日分保持
            encoding="utf-8",
        )

        json_formatter = JSONFormatter(datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(json_formatter)
        self.logger.addHandler(file_handler)

    def _log_with_context(self, level: int, message: str, context: Optional[Dict] = None, exc_info: bool = False):
        """コンテキスト情報付きログ出力"""
        if context:
            # コンテキスト情報を追加
            extra = {"context": context}
            self.logger.log(level, message, extra=extra, exc_info=exc_info)
        else:
            self.logger.log(level, message, exc_info=exc_info)

    def debug(self, message: str, context: Optional[Dict] = None):
        """DEBUGログ出力"""
        self._log_with_context(logging.DEBUG, message, context)

    def info(self, message: str, context: Optional[Dict] = None):
        """INFOログ出力"""
        self._log_with_context(logging.INFO, message, context)

    def warning(self, message: str, context: Optional[Dict] = None):
        """WARNINGログ出力"""
        self._log_with_context(logging.WARNING, message, context)

    def error(self, message: str, context: Optional[Dict] = None, exc_info: bool = False):
        """ERRORログ出力"""
        self._log_with_context(logging.ERROR, message, context, exc_info)

    def critical(self, message: str, context: Optional[Dict] = None, exc_info: bool = False):
        """CRITICALログ出力"""
        self._log_with_context(logging.CRITICAL, message, context, exc_info)

    def exception(self, message: str, context: Optional[Dict] = None):
        """例外情報付きERRORログ出力"""
        self._log_with_context(logging.ERROR, message, context, exc_info=True)

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
    enable_json_file: bool = False,
    config: Optional[Dict[str, Any]] = None,
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
        enable_json_file: JSON形式ファイル出力を有効にするか
        config: YAML設定から読み込んだ設定

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
        enable_json_file=enable_json_file,
        config=config,
    )


# 使用例
if __name__ == "__main__":
    # 基本的な使用例
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

    # コンテキスト付きログ
    logger.info("ユーザーログイン", context={"user_id": 123, "ip": "192.168.1.1"})
    logger.error("処理エラー", context={"error_code": "E001", "details": "Database connection failed"})

    # 例外ログ
    try:
        result = 10 / 0
    except Exception:
        logger.exception("例外が発生しました", context={"operation": "division"})

    # ログレベル変更
    logger.set_level("WARNING")
    logger.info("このメッセージは表示されません（WARNINGレベル以下のため）")
    logger.warning("このメッセージは表示されます")

    print("\nログファイルは ./logs/sample.log に出力されています")

    # JSON形式ログの使用例
    json_logger = setup_logger(
        name="json_app",
        log_level="INFO",
        log_file="app.json",
        enable_console=False,
        enable_file=False,
        enable_json_file=True,
    )

    json_logger.info("JSON形式ログ", context={"action": "test", "status": "success"})

    # クリーンアップ（テスト用）
    import shutil
    log_path = Path("logs")
    if log_path.exists():
        shutil.rmtree(log_path)
