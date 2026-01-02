from configparser import ConfigParser
from dataclasses import dataclass
from os import getenv
from pathlib import Path


@dataclass
class ConfigData:
    environment: str = "development"
    connection_string: str = "postgresql+psycopg2://name:pass@localhost:5432/db"


class ConfigReader:
    def __init__(self, env_path: Path | None = None) -> None:
        self.env_path = env_path or Path(__file__).resolve().parents[2] / "environments"
        self.parser = ConfigParser()

    def read(self) -> ConfigData:
        # Default values
        self.parser["database"] = {"url": ConfigData.connection_string}

        # Read base config
        config_path = self.env_path / "config.ini"
        if not config_path.exists():
            self.parser.write(open(config_path, 'w'),)
            raise FileNotFoundError(f"Fill in the configuration file at {config_path}")
        self.parser.read(config_path)

        # Read environment-specific config
        environment = getenv("sightseeings_environment", "development")
        env_config_path = self.env_path / f"config_{environment}.ini"
        self.parser.read(env_config_path)  # environment-specific config values

        connection = self.parser.get(
            "database",
            "url",
            fallback=ConfigData.connection_string
        )

        config_data = ConfigData(environment=environment, connection_string=connection)

        self.validate(config_data)

        return config_data

    def validate(self, config_data: ConfigData) -> None:
        error_messages: list[ValueError] = []
        if not config_data.connection_string:
            error_messages.append(ValueError("Database connection string cannot be empty."))
        if config_data.connection_string == ConfigData.connection_string:
            error_messages.append(ValueError("Database connection string cannot be default."))

        if error_messages:
            raise ExceptionGroup("Configuration errors found", error_messages)