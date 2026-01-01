"""
ファイル監視ベーステンプレート

ディレクトリ/ファイルの変更を監視し、自動処理を実行するテンプレート。
watchdog統合、パターンマッチング、カスタムハンドラー登録対応。
"""

import time
import fnmatch
from pathlib import Path
from typing import Optional, List, Dict, Callable, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from common.logger import setup_logger
from common.config_manager import ConfigManager


class FileWatcher:
    """ファイル監視クラス

    ディレクトリ/ファイルの作成・変更・削除を監視し、カスタムハンドラーを実行
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
            name="file_watcher",
            log_level=self.config.get("logging", {}).get("level", "INFO"),
            config=self.config
        )

        # ファイル監視設定取得
        self.watcher_config = self.config.get("file_watcher", {})
        self.watch_directory = self.watcher_config.get("watch_directory", "./data")
        self.recursive = self.watcher_config.get("recursive", True)
        self.patterns = self.watcher_config.get("patterns", [])
        self.exclude_patterns = self.watcher_config.get("exclude_patterns", [])
        self.ignore_directories = self.watcher_config.get("ignore_directories", [])

        # カスタムハンドラー格納
        self.custom_handlers: Dict[str, List[Callable]] = {
            "created": [],
            "modified": [],
            "deleted": [],
            "moved": []
        }

        # watchdog Observer
        self.observer: Optional[Observer] = None
        self.event_handler: Optional[CustomEventHandler] = None

        self.logger.info("FileWatcher初期化完了")

    def register_handler(
        self,
        event_type: str,
        handler: Callable[[str], Any],
        patterns: Optional[List[str]] = None
    ) -> None:
        """
        カスタムイベントハンドラーを登録

        Args:
            event_type: イベントタイプ（created, modified, deleted, moved）
            handler: ハンドラー関数（引数: file_path）
            patterns: 適用するファイルパターン（Noneの場合は全ファイル）
        """
        if event_type not in self.custom_handlers:
            raise ValueError(f"無効なイベントタイプ: {event_type}")

        # ハンドラーとパターンをセットで保存
        handler_info = {
            "handler": handler,
            "patterns": patterns or []
        }
        self.custom_handlers[event_type].append(handler_info)

        self.logger.info(
            f"カスタムハンドラー登録",
            context={"event_type": event_type, "patterns": patterns}
        )

    def _match_patterns(self, file_path: str, patterns: List[str]) -> bool:
        """
        ファイルパスがパターンに一致するか確認

        Args:
            file_path: ファイルパス
            patterns: パターンリスト

        Returns:
            一致する場合True
        """
        if not patterns:
            return True

        file_name = Path(file_path).name
        return any(fnmatch.fnmatch(file_name, pattern) for pattern in patterns)

    def _should_ignore(self, file_path: str) -> bool:
        """
        ファイルを無視すべきか判定

        Args:
            file_path: ファイルパス

        Returns:
            無視する場合True
        """
        path = Path(file_path)

        # 除外パターンチェック
        if self.exclude_patterns and self._match_patterns(file_path, self.exclude_patterns):
            return True

        # 無視ディレクトリチェック
        for ignore_dir in self.ignore_directories:
            if ignore_dir in path.parts:
                return True

        return False

    def _execute_handlers(self, event_type: str, file_path: str) -> None:
        """
        登録されたハンドラーを実行

        Args:
            event_type: イベントタイプ
            file_path: ファイルパス
        """
        if event_type not in self.custom_handlers:
            return

        # 無視すべきファイルか確認
        if self._should_ignore(file_path):
            self.logger.debug(
                f"ファイルを無視",
                context={"file": file_path, "event_type": event_type}
            )
            return

        # 各ハンドラーを実行
        for handler_info in self.custom_handlers[event_type]:
            handler = handler_info["handler"]
            patterns = handler_info["patterns"]

            # パターンマッチング
            if patterns and not self._match_patterns(file_path, patterns):
                continue

            try:
                self.logger.debug(
                    f"ハンドラー実行",
                    context={"file": file_path, "event_type": event_type}
                )
                handler(file_path)

            except Exception as e:
                self.logger.error(
                    f"ハンドラー実行エラー",
                    context={
                        "file": file_path,
                        "event_type": event_type,
                        "error": str(e)
                    },
                    exc_info=True
                )

    def watch(
        self,
        directory: Optional[str] = None,
        patterns: Optional[List[str]] = None,
        recursive: Optional[bool] = None
    ) -> None:
        """
        ディレクトリ監視を開始

        Args:
            directory: 監視ディレクトリ（Noneの場合は設定ファイルから取得）
            patterns: 監視パターン（Noneの場合は設定ファイルから取得）
            recursive: 再帰的監視（Noneの場合は設定ファイルから取得）
        """
        try:
            # パラメータ設定
            watch_dir = directory or self.watch_directory
            watch_patterns = patterns or self.patterns
            watch_recursive = recursive if recursive is not None else self.recursive

            # ディレクトリ存在確認
            watch_path = Path(watch_dir)
            if not watch_path.exists():
                raise FileNotFoundError(f"監視ディレクトリが見つかりません: {watch_dir}")

            self.logger.info(
                f"ファイル監視開始",
                context={
                    "directory": watch_dir,
                    "patterns": watch_patterns,
                    "recursive": watch_recursive
                }
            )

            # イベントハンドラー作成
            self.event_handler = CustomEventHandler(self, watch_patterns)

            # Observer作成と監視開始
            self.observer = Observer()
            self.observer.schedule(
                self.event_handler,
                watch_dir,
                recursive=watch_recursive
            )
            self.observer.start()

            # 監視継続
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("ファイル監視を停止します（Ctrl+C）")
                self.stop()

        except Exception as e:
            self.logger.error(
                f"ファイル監視エラー",
                context={"error": str(e)},
                exc_info=True
            )
            raise

    def stop(self) -> None:
        """
        ファイル監視を停止
        """
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.logger.info("ファイル監視停止完了")


class CustomEventHandler(FileSystemEventHandler):
    """カスタムファイルシステムイベントハンドラー"""

    def __init__(self, watcher: FileWatcher, patterns: List[str]):
        """
        初期化

        Args:
            watcher: FileWatcherインスタンス
            patterns: 監視パターン
        """
        super().__init__()
        self.watcher = watcher
        self.patterns = patterns

    def _should_process(self, event: FileSystemEvent) -> bool:
        """
        イベントを処理すべきか判定

        Args:
            event: ファイルシステムイベント

        Returns:
            処理する場合True
        """
        # ディレクトリイベントは無視
        if event.is_directory:
            return False

        # パターンマッチング
        if self.patterns and not self.watcher._match_patterns(event.src_path, self.patterns):
            return False

        return True

    def on_created(self, event: FileSystemEvent) -> None:
        """
        ファイル作成イベント

        Args:
            event: ファイルシステムイベント
        """
        if not self._should_process(event):
            return

        self.watcher.logger.info(
            f"ファイル作成検知",
            context={"file": event.src_path}
        )
        self.watcher._execute_handlers("created", event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        """
        ファイル変更イベント

        Args:
            event: ファイルシステムイベント
        """
        if not self._should_process(event):
            return

        self.watcher.logger.info(
            f"ファイル変更検知",
            context={"file": event.src_path}
        )
        self.watcher._execute_handlers("modified", event.src_path)

    def on_deleted(self, event: FileSystemEvent) -> None:
        """
        ファイル削除イベント

        Args:
            event: ファイルシステムイベント
        """
        if not self._should_process(event):
            return

        self.watcher.logger.info(
            f"ファイル削除検知",
            context={"file": event.src_path}
        )
        self.watcher._execute_handlers("deleted", event.src_path)

    def on_moved(self, event: FileSystemEvent) -> None:
        """
        ファイル移動イベント

        Args:
            event: ファイルシステムイベント
        """
        if not self._should_process(event):
            return

        self.watcher.logger.info(
            f"ファイル移動検知",
            context={"src": event.src_path, "dest": event.dest_path}
        )
        self.watcher._execute_handlers("moved", event.dest_path)


# 使用例
if __name__ == "__main__":
    # ファイル監視の基本フロー
    watcher = FileWatcher()

    # CSV処理ハンドラー
    def process_csv(file_path: str):
        print(f"CSV処理: {file_path}")
        # CSV処理ロジック

    # Excel処理ハンドラー
    def process_excel(file_path: str):
        print(f"Excel処理: {file_path}")
        # Excel処理ロジック

    # ハンドラー登録
    watcher.register_handler("created", process_csv, patterns=["*.csv"])
    watcher.register_handler("modified", process_csv, patterns=["*.csv"])
    watcher.register_handler("created", process_excel, patterns=["*.xlsx", "*.xls"])

    # 監視開始
    watcher.watch(directory="./data", recursive=True)
