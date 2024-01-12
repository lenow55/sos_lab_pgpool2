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

class BrokerSettings(AdvancedBaseSettings):
    broker_protocol: str = Field(default="redis")
    broker_host: str = Field(default="localhost")
    broker_port: int = Field(default=6379)
#    broker_username: SecretStr
#    broker_password: SecretStr

    @property
    def broker_url(self) -> str:
        return f"{self.broker_protocol}://{self.broker_host}:{self.broker_port}/11"

    model_config = SettingsConfigDict(
        env_file=(
            os.path.join(base_dir, 'broker.env.prod'),
            os.path.join(base_dir, 'broker.env.debug')
        )
    )

class BackendSettings(AdvancedBaseSettings):
    backend_protocol: str = Field(default="redis")
    backend_host: str = Field(default="localhost")
    backend_port: int = Field(default=6379)

    @property
    def backend_url(self) -> str:
        return f"{self.backend_protocol}://{self.backend_host}:{self.backend_port}/11"

    model_config = SettingsConfigDict(
        env_file=(
            os.path.join(base_dir, 'backend.env.prod'),
            os.path.join(base_dir, 'backend.env.debug')
        )
    )

broker_settings = BrokerSettings()
backend_settings = BackendSettings()

# tokenSettings = AcessTokenSettings()
