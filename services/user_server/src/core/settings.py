from datetime import timedelta
from enum import Enum
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

base_dir = "environment"


class EnvironmentOption(Enum):
    DEBUG = "debug"
    PRODUCTION = "production"


# Родительский объект с общими настройками.
class AdvancedBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        secrets_dir='/var/run/secrets_dir'
    )


class ServerSettings(AdvancedBaseSettings):
    environment: EnvironmentOption = Field(
        default=EnvironmentOption.DEBUG
    )
    base_url: str
    root_path: str = Field(default="/")
    model_config = SettingsConfigDict(
        # слева на право в порядке приоритетности
        env_file=(
            os.path.join(base_dir, 'server.env.prod'),
            os.path.join(base_dir, 'server.env.debug')
        )
    )


class ServiceDatabaseSettings(AdvancedBaseSettings):
    db_host: str = Field(default="db")
    db_port: int = Field(default="5432")
    db_user: str
    db_password: SecretStr
    db_name: str

    model_config = SettingsConfigDict(
        # слева на право в порядке приоритетности
        env_file=(
            os.path.join(base_dir, 'db.env.prod'),
            os.path.join(base_dir, 'db.env.debug')
        )
    )

    @property
    def postgresql_url(self) -> str:
        """
        property (свойство)
        """
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class TokenSettings(AdvancedBaseSettings):
    jwt_secret: SecretStr
    jwt_algorithm: str = Field(default="HS256")
    access_token_ttl: timedelta = timedelta(minutes=30)
    refresh_token_ttl: timedelta = timedelta(days=7)

    model_config = SettingsConfigDict(
        env_file=(
            os.path.join(base_dir, 'token.env.prod'),
            os.path.join(base_dir, 'token.env.debug')
        )
    )


class RedisCacheSettings(AdvancedBaseSettings):
    redis_cache_host: str = Field(default="localhost")
    redis_cache_port: int = Field(default=6379)

    @property
    def redis_cache_url(self) -> str:
        return f"redis://{self.redis_cache_host}:{self.redis_cache_port}"

    model_config = SettingsConfigDict(
        env_file=(
            os.path.join(base_dir, 'redis_cache.env.prod'),
            os.path.join(base_dir, 'redis_cache.env.debug')
        )
    )


dbSettings = ServiceDatabaseSettings()
serverSettings = ServerSettings()
tokenSettings = TokenSettings()

# tokenSettings = AcessTokenSettings()
