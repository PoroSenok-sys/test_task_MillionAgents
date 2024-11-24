"""Конфигурационный файл"""
import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    load_dotenv()
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: int = os.environ.get("DB_PORT")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    DB_NAME: str = os.environ.get("DB_NAME")

    LOCAL_STORAGE: str = os.environ.get("LOCAL_STORAGE")
    CLOUD_STORAGE_URL: str = os.environ.get("CLOUD_STORAGE_URL")

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="../../.env")


settings = Settings()
