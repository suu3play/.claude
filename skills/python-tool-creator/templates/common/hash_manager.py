"""
ファイルハッシュ管理モジュール

生成されたファイルの変更追跡とテンプレート更新検出。
SHA256ハッシュ計算、変更検出、バックアップ機能を提供。
"""

import hashlib
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from common.logger import setup_logger


class HashManager:
    """ファイルハッシュ管理クラス

    生成ファイルのハッシュ記録、変更検出、バックアップ管理
    """

    def __init__(
        self,
        hash_file: str = ".file_hashes.json",
        backup_dir: str = ".backups",
        template_version: str = "1.0.0"
    ):
        """
        初期化

        Args:
            hash_file: ハッシュ管理ファイルパス
            backup_dir: バックアップディレクトリ
            template_version: テンプレートバージョン
        """
        self.hash_file = Path(hash_file)
        self.backup_dir = Path(backup_dir)
        self.template_version = template_version

        # ロガー初期化
        self.logger = setup_logger(
            name="hash_manager",
            log_level="INFO"
        )

        # ハッシュデータ
        self.hash_data: Dict[str, Any] = self._load_hash_file()

        # 除外パターン
        self.exclude_patterns = [
            ".env",
            ".env.*",
            "*.log",
            ".git",
            ".gitignore",
            "__pycache__",
            "*.pyc",
            ".backups",
            ".file_hashes.json",
            "logs"
        ]

        self.logger.info("HashManager初期化完了")

    def _load_hash_file(self) -> Dict[str, Any]:
        """
        ハッシュファイルを読み込み

        Returns:
            ハッシュデータ
        """
        if not self.hash_file.exists():
            return {
                "version": "1.0.0",
                "template_version": self.template_version,
                "generated_at": datetime.now().isoformat(),
                "files": {}
            }

        try:
            with open(self.hash_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(
                f"ハッシュファイル読み込みエラー",
                context={"error": str(e)},
                exc_info=True
            )
            return {
                "version": "1.0.0",
                "template_version": self.template_version,
                "generated_at": datetime.now().isoformat(),
                "files": {}
            }

    def _save_hash_file(self) -> None:
        """
        ハッシュファイルを保存
        """
        try:
            with open(self.hash_file, 'w', encoding='utf-8') as f:
                json.dump(self.hash_data, f, indent=2, ensure_ascii=False)

            self.logger.debug("ハッシュファイル保存完了")

        except Exception as e:
            self.logger.error(
                f"ハッシュファイル保存エラー",
                context={"error": str(e)},
                exc_info=True
            )
            raise

    def _calculate_hash(self, file_path: str) -> str:
        """
        ファイルのSHA256ハッシュを計算

        Args:
            file_path: ファイルパス

        Returns:
            SHA256ハッシュ（sha256:プレフィックス付き）
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

            sha256_hash = hashlib.sha256()
            with open(path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)

            hash_value = sha256_hash.hexdigest()
            return f"sha256:{hash_value}"

        except Exception as e:
            self.logger.error(
                f"ハッシュ計算エラー",
                context={"file": file_path, "error": str(e)},
                exc_info=True
            )
            raise

    def _should_exclude(self, file_path: str) -> bool:
        """
        ファイルを除外すべきか判定

        Args:
            file_path: ファイルパス

        Returns:
            除外する場合True
        """
        path = Path(file_path)

        for pattern in self.exclude_patterns:
            if pattern.startswith("*"):
                # 拡張子パターン
                if path.suffix == pattern[1:]:
                    return True
            elif pattern in str(path):
                return True

        return False

    def generate_hashes(self, files: Optional[List[str]] = None) -> None:
        """
        ファイルハッシュを生成・記録

        Args:
            files: ハッシュ化するファイルリスト（Noneの場合は全ファイル）
        """
        try:
            # ファイルリスト取得
            if files is None:
                # カレントディレクトリの全ファイル
                files = [str(p) for p in Path(".").rglob("*") if p.is_file()]

            # 除外ファイルをフィルタ
            target_files = [f for f in files if not self._should_exclude(f)]

            self.logger.info(
                f"ハッシュ生成開始",
                context={"file_count": len(target_files)}
            )

            # 各ファイルのハッシュ計算
            for file_path in target_files:
                try:
                    hash_value = self._calculate_hash(file_path)
                    self.hash_data["files"][file_path] = {
                        "hash": hash_value,
                        "modified": False,
                        "last_checked": datetime.now().isoformat()
                    }

                    self.logger.debug(
                        f"ハッシュ記録",
                        context={"file": file_path, "hash": hash_value[:16] + "..."}
                    )

                except Exception as e:
                    self.logger.warning(
                        f"ファイルハッシュ計算失敗",
                        context={"file": file_path, "error": str(e)}
                    )
                    continue

            # ハッシュファイル保存
            self._save_hash_file()

            self.logger.info(
                f"ハッシュ生成完了",
                context={"recorded_files": len(self.hash_data["files"])}
            )

        except Exception as e:
            self.logger.error(
                f"ハッシュ生成エラー",
                context={"error": str(e)},
                exc_info=True
            )
            raise

    def detect_changes(self, file_path: Optional[str] = None) -> bool:
        """
        ファイル変更を検出

        Args:
            file_path: チェックするファイルパス（Noneの場合は全ファイル）

        Returns:
            変更がある場合True
        """
        try:
            if file_path:
                # 単一ファイルチェック
                return self._check_single_file(file_path)
            else:
                # 全ファイルチェック
                return self._check_all_files()

        except Exception as e:
            self.logger.error(
                f"変更検出エラー",
                context={"file": file_path, "error": str(e)},
                exc_info=True
            )
            raise

    def _check_single_file(self, file_path: str) -> bool:
        """
        単一ファイルの変更チェック

        Args:
            file_path: ファイルパス

        Returns:
            変更がある場合True
        """
        if file_path not in self.hash_data["files"]:
            self.logger.warning(
                f"ファイルがハッシュ記録に存在しません",
                context={"file": file_path}
            )
            return False

        # 現在のハッシュ計算
        current_hash = self._calculate_hash(file_path)
        recorded_hash = self.hash_data["files"][file_path]["hash"]

        # ハッシュ比較
        if current_hash != recorded_hash:
            self.hash_data["files"][file_path]["modified"] = True
            self.hash_data["files"][file_path]["last_checked"] = datetime.now().isoformat()
            self._save_hash_file()

            self.logger.info(
                f"ファイル変更検出",
                context={"file": file_path}
            )
            return True

        return False

    def _check_all_files(self) -> bool:
        """
        全ファイルの変更チェック

        Returns:
            変更があるファイルが存在する場合True
        """
        changed_files = []

        for file_path in self.hash_data["files"].keys():
            if not Path(file_path).exists():
                self.logger.warning(
                    f"ファイルが存在しません",
                    context={"file": file_path}
                )
                continue

            if self._check_single_file(file_path):
                changed_files.append(file_path)

        if changed_files:
            self.logger.info(
                f"変更ファイル検出",
                context={"count": len(changed_files), "files": changed_files}
            )

        return len(changed_files) > 0

    def get_modified_files(self) -> List[str]:
        """
        カスタマイズされたファイルのリストを取得

        Returns:
            変更されたファイルパスのリスト
        """
        modified = []

        for file_path, info in self.hash_data["files"].items():
            if info.get("modified", False):
                modified.append(file_path)

        return modified

    def backup_file(self, file_path: str) -> str:
        """
        ファイルをバックアップ

        Args:
            file_path: バックアップするファイルパス

        Returns:
            バックアップファイルパス
        """
        try:
            # バックアップディレクトリ作成
            self.backup_dir.mkdir(exist_ok=True)

            # バックアップファイル名（タイムスタンプ付き）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = Path(file_path).name
            backup_path = self.backup_dir / f"{file_name}.{timestamp}.bak"

            # ファイルコピー
            shutil.copy2(file_path, backup_path)

            self.logger.info(
                f"ファイルバックアップ完了",
                context={"source": file_path, "backup": str(backup_path)}
            )

            return str(backup_path)

        except Exception as e:
            self.logger.error(
                f"バックアップエラー",
                context={"file": file_path, "error": str(e)},
                exc_info=True
            )
            raise

    def generate_report(self) -> Dict[str, Any]:
        """
        変更レポートを生成

        Returns:
            レポートデータ
        """
        modified_files = self.get_modified_files()
        total_files = len(self.hash_data["files"])

        report = {
            "total_files": total_files,
            "modified_count": len(modified_files),
            "modified_files": modified_files,
            "template_version": self.hash_data.get("template_version"),
            "generated_at": self.hash_data.get("generated_at"),
            "last_check": datetime.now().isoformat()
        }

        self.logger.info(
            f"変更レポート生成",
            context={
                "total": total_files,
                "modified": len(modified_files)
            }
        )

        return report


# 使用例
if __name__ == "__main__":
    # ハッシュ管理の基本フロー
    hash_manager = HashManager()

    # ツール生成時: ハッシュ記録
    hash_manager.generate_hashes([
        "main.py",
        "config.yaml",
        "requirements.txt"
    ])

    print("ハッシュ生成完了")

    # 実行時: 変更検出
    if hash_manager.detect_changes("main.py"):
        print("main.pyがカスタマイズされています")

        # バックアップ作成
        backup_path = hash_manager.backup_file("main.py")
        print(f"バックアップ作成: {backup_path}")

    # レポート生成
    report = hash_manager.generate_report()
    print(f"\n変更レポート:")
    print(f"  総ファイル数: {report['total_files']}")
    print(f"  変更ファイル数: {report['modified_count']}")
    if report['modified_files']:
        print(f"  変更ファイル: {', '.join(report['modified_files'])}")
