import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.logging import RichHandler


class Path:
    app_dir: str = os.path.dirname(os.path.abspath(__file__))
    root_dir: str = os.path.dirname(app_dir)
    env_file: str = os.path.join(root_dir, ".env")


class PiazzaBotConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path.env_file, env_file_encoding="utf-8", extra="ignore")

    PIAZZA_USER_EMAIL: str = Field()
    PIAZZA_USER_PASSWORD: str = Field()


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
