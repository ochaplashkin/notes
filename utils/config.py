from dataclasses import dataclass
import configparser
from functools import lru_cache


@dataclass
class AppConfig:
    host: str
    port: int


@dataclass
class Config:
    app: AppConfig


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ('true', 't', '1', 'yes', 'y')


@lru_cache
def load(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    app_config = config["app"]


    return Config(
        app=AppConfig(
            host=app_config["host"],
            port=int(app_config["port"])
        )
    )