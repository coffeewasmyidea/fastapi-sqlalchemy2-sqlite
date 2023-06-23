import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env_file: str | None = os.environ.get("ENV_FILE")
    app_config_file: Path = Path(__file__).parent / f"config/{env_file}.env"

    model_config = SettingsConfigDict(env_file=app_config_file, case_sensitive=True)

    DEBUG: bool = True
    CURRENT_ENV: str = ""
    APP_NAME: str = ""
    APP_TITLE: str = "URL Shortener - click.local"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080

    UVICORN_APP_NAME: str = "app.main:app"
    UVICORN_GRACEFUL_SHUTDOWN: int = 10
    UVICORN_LOG_LEVEL: str = "info"

    DATABASE_URI: str = "sqlite+aiosqlite:///./click.db"
    ECHO_SQL: bool = False

    SHRINK_LENGTH: int = 5
    PREFIX_PATTERN: str = "^[a-z0-9]+$"
    DOMAIN_NAME: str = "http://localhost"


settings: Settings = Settings.model_validate({})
