from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr

BASE_DIRECTORY = Path(__file__).absolute().parent.parent.parent

class AdvancedBaseSettings(BaseSettings):
    # Родительский объект с общими настройками.
    # Нужен для того, чтобы не описывать несколько раз одно и то же.

    class Config:
        # Эта настройка делает объект неизменяемым.
        allow_mutation = False

class ServiceDatabaseSettings(AdvancedBaseSettings):
    DB_HOST: str
    DB_PORT: int = Field(default="5432")
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_NAME: str

    class Config:
        env_file = '.env'

    @property
    def postgresql_url(self) -> str:
        """
        property (свойство)
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

#    JWT_PUBLIC_KEY: str
#    JWT_PRIVATE_KEY: str
#    REFRESH_TOKEN_EXPIRES_IN: int
#    ACCESS_TOKEN_EXPIRES_IN: int
#    JWT_ALGORITHM: str
#
#    CLIENT_ORIGIN: str


settings = ServiceDatabaseSettings()
