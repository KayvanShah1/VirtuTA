import logging
import os
from functools import lru_cache
from typing import Any

from google.oauth2.service_account import Credentials
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.logging import RichHandler


class Path:
    app_dir: str = os.path.dirname(os.path.abspath(__file__))
    root_dir: str = os.path.dirname(app_dir)
    secrets_dir: str = os.path.join(root_dir, "secrets")
    env_file: str = os.path.join(root_dir, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path.env_file, env_file_encoding="utf-8", extra="ignore")

    GCLOUD_SERVICE_ACCOUNT_KEY_PATH: str = Field(default="<your-gcp-service-acc-key-filename>")
    PROJECT_ID: str = Field(default="<your-gcp-project-id>")
    PROJECT_LOCATION: str = Field(default="<your-gcp-project-location>")
    CREDENTIALS: Any | Credentials = Field(default=None)

    MONGODB_URI: str = Field(default="<mongodb-connection-string>")

    OPENAI_API_KEY: str = Field(default="<your-openai-api-key>")
    HUGGINGFACEHUB_API_TOKEN: str = Field(default="<your-huggingfacehub-access-token>")


class PiazzaBotConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path.env_file, env_file_encoding="utf-8", extra="ignore")

    PIAZZA_USER_EMAIL: str = Field()
    PIAZZA_USER_PASSWORD: str = Field()


class VectorStoreConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path.env_file, env_file_encoding="utf-8", extra="ignore")

    MONGODB_URI: str = Field(default="<mongodb-connection-string>")


def get_logger(name):
    # Create a logger
    logger = logging.getLogger(name)

    # Set the logging level (adjust as needed)
    logger.setLevel(logging.DEBUG)

    # Create a console handler and set the level
    ch = RichHandler()
    ch.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter("%(message)s")
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)
    return logger


@lru_cache(maxsize=64)
def get_settings() -> Settings:
    settings = Settings()
    settings.CREDENTIALS = Credentials.from_service_account_file(
        os.path.join(Path.secrets_dir, settings.GCLOUD_SERVICE_ACCOUNT_KEY_PATH),
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    return settings


config = get_settings()
piazza_creds = PiazzaBotConfig()
# print(config.model_dump())
