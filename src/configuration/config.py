from configparser import ConfigParser
from os import getenv
from pathlib import Path


class AppConfig:
    def __init__(self) -> None:
        env_path = Path(__file__).resolve().parents[2] / "environments"
        config_path = env_path / "config.ini"
        app_config = ConfigParser()
        app_config.read(config_path)

        self.environment: str = getenv("sightseeings_environment", "development")
        env_config_path = env_path / f"config_{self.environment}.ini"
        app_config.read(env_config_path)  # environment-specific config values

        self.connection_string: str = app_config.get("database", "url", fallback="sqlite:///./sightseeings.db")