from __future__ import annotations

from typing import Literal

from pydantic import BaseSettings, Extra, Field
from sqlalchemy.engine.url import URL


ASYNC_DRIVER_NAME = "postgresql+asyncpg"
SYNC_DRIVER_NAME = "postgresql"


class CustomBaseSettings(BaseSettings):
    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = Extra.ignore


class DatabaseSettings(CustomBaseSettings):
    host: str
    port: int

    user: str
    password: str

    db: str

    timeout: int = 60  # in seconds
    # https://postgresqlco.nf/doc/ru/param/statement_timeout/
    statement_timeout: int = 55

    @property
    def full_url_async(self) -> str:
        url = URL.create(
            drivername=ASYNC_DRIVER_NAME,
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            database=self.db,
        )
        return url.render_as_string(hide_password=False)

    @property
    def full_url_sync(self) -> str:
        url = URL.create(
            drivername=SYNC_DRIVER_NAME,
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            database=self.db,
        )
        return url.render_as_string(hide_password=False)

    class Config(CustomBaseSettings.Config):
        env_prefix = "database_"


class SecuritySettings(CustomBaseSettings):
    pbkdf2hmac_iterations: int = 100_000
    salt_length: int = 16

    class Config(CustomBaseSettings.Config):
        env_prefix = "security_"


class LoggingSettings(CustomBaseSettings):
    level: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = Field(
        default="INFO",
    )
    format: str = (
        "{level} {time:YYYY-MM-DD HH:mm:ss} {name}:{function}-{message} | {extra}"
    )
    pod_name: str | None = Field(
        None, description="Name of POD. k8s should be set it automatically"
    )

    class Config(CustomBaseSettings.Config):
        env_prefix = "logging_"
        allow_population_by_field_name = True


database_settings = DatabaseSettings()
security_settings = SecuritySettings()
logging_settings = LoggingSettings()
