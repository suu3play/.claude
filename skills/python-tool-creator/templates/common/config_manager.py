"""
設定管理共通モジュール

YAML/JSON設定ファイル管理、環境変数読み込み、デフォルト値設定
"""

import os
import json
import yaml
from typing import Any, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv


class ConfigManager:
    """設定管理クラス"""

    def __init__(
        self,
        config_path: Optional[str] = None,
        env_file: Optional[str] = None,
        auto_load_env: bool = True,
    ):
        """
        初期化

        Args:
            config_path: 設定ファイルパス（YAML/JSON）
            env_file: .envファイルのパス
            auto_load_env: 環境変数を自動読み込みするか
        """
        self.config: Dict[str, Any] = {}

        # 環境変数読み込み
        if auto_load_env:
            if env_file:
                load_dotenv(env_file)
            else:
                load_dotenv()

        # 設定ファイル読み込み
        if config_path:
            self.load_config(config_path)

    def load_config(self, config_path: str):
        """
        設定ファイルを読み込み

        Args:
            config_path: 設定ファイルパス（YAML/JSON）
        """
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"設定ファイルが見つかりません: {config_path}")

        with open(path, "r", encoding="utf-8") as f:
            if path.suffix in [".yaml", ".yml"]:
                self.config = yaml.safe_load(f)
            elif path.suffix == ".json":
                self.config = json.load(f)
            else:
                raise ValueError(
                    f"サポートされていないファイル形式です: {path.suffix}"
                )

    def get(self, key: str, default: Any = None, from_env: bool = True) -> Any:
        """
        設定値を取得

        Args:
            key: 設定キー（ドット記法対応: "database.host"）
            default: デフォルト値
            from_env: 環境変数も検索するか

        Returns:
            設定値
        """
        # 環境変数から取得（優先）
        if from_env:
            env_key = key.upper().replace(".", "_")
            env_value = os.getenv(env_key)
            if env_value is not None:
                return self._convert_type(env_value, default)

        # 設定ファイルから取得
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value if value is not None else default

    def _convert_type(self, value: str, default: Any) -> Any:
        """
        文字列を適切な型に変換

        Args:
            value: 変換する値
            default: デフォルト値（型判定に使用）

        Returns:
            変換後の値
        """
        if default is None:
            return value

        # デフォルト値の型に合わせて変換
        if isinstance(default, bool):
            return value.lower() in ["true", "1", "yes", "on"]
        elif isinstance(default, int):
            try:
                return int(value)
            except ValueError:
                return default
        elif isinstance(default, float):
            try:
                return float(value)
            except ValueError:
                return default
        else:
            return value

    def get_required(self, key: str, from_env: bool = True) -> Any:
        """
        必須設定値を取得

        Args:
            key: 設定キー
            from_env: 環境変数も検索するか

        Returns:
            設定値

        Raises:
            ValueError: 設定値が見つからない場合
        """
        value = self.get(key, from_env=from_env)
        if value is None:
            raise ValueError(f"必須設定が見つかりません: {key}")
        return value

    def set(self, key: str, value: Any):
        """
        設定値をセット

        Args:
            key: 設定キー（ドット記法対応）
            value: 設定値
        """
        keys = key.split(".")
        target = self.config

        for i, k in enumerate(keys[:-1]):
            if k not in target:
                target[k] = {}
            target = target[k]

        target[keys[-1]] = value

    def save_config(self, config_path: str):
        """
        設定ファイルを保存

        Args:
            config_path: 保存先パス
        """
        path = Path(config_path)

        with open(path, "w", encoding="utf-8") as f:
            if path.suffix in [".yaml", ".yml"]:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
            elif path.suffix == ".json":
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            else:
                raise ValueError(
                    f"サポートされていないファイル形式です: {path.suffix}"
                )

    def to_dict(self) -> Dict[str, Any]:
        """
        設定を辞書として取得

        Returns:
            設定の辞書
        """
        return self.config.copy()


# 使用例
if __name__ == "__main__":
    # YAML設定ファイルの例
    example_yaml = """
    app:
      name: "Sample App"
      debug: true
      version: "1.0.0"

    database:
      host: "localhost"
      port: 5432
      name: "mydb"

    api:
      openai:
        model: "gpt-4o"
        temperature: 0.7
      slack:
        channel: "#general"
    """

    # 設定ファイル作成（テスト用）
    with open("config_example.yaml", "w", encoding="utf-8") as f:
        f.write(example_yaml)

    # .envファイルの例
    example_env = """
    DATABASE_HOST=prod-db.example.com
    DATABASE_PORT=5432
    OPENAI_API_KEY=sk-xxxxx
    """

    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(example_env)

    # 使用例
    print("=== ConfigManager使用例 ===\n")

    # 初期化
    config = ConfigManager(config_path="config_example.yaml")

    # 設定値取得
    print(f"App Name: {config.get('app.name')}")
    print(f"Debug Mode: {config.get('app.debug')}")
    print(f"Database Host: {config.get('database.host')}")
    print(f"API Model: {config.get('api.openai.model')}")

    # デフォルト値指定
    print(f"Timeout: {config.get('api.timeout', default=30)}")

    # 必須設定値取得
    try:
        api_key = config.get_required("openai.api.key")
    except ValueError as e:
        print(f"エラー: {e}")

    # 設定値セット
    config.set("app.environment", "production")
    print(f"\nEnvironment: {config.get('app.environment')}")

    # 全設定表示
    print("\n=== 全設定 ===")
    print(json.dumps(config.to_dict(), ensure_ascii=False, indent=2))

    # クリーンアップ
    Path("config_example.yaml").unlink(missing_ok=True)
    Path(".env.example").unlink(missing_ok=True)
