import json
from typing import Any, List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "development"
    allowed_origins: str = "*"
    app_name: str = "E-Commerce API"
    app_version: str = "1.0.0"
    database_path: str = "data/ecommerce.db"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    admin_registration_key: str
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

# Export for compatibility
ENV = settings.env
ALLOWED_ORIGINS = [x.strip() for x in settings.allowed_origins.split(",") if x.strip()]
APP_NAME = settings.app_name
APP_VERSION = settings.app_version
DATABASE_PATH = settings.database_path
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
ADMIN_REGISTRATION_KEY = settings.admin_registration_key
PORT = settings.port