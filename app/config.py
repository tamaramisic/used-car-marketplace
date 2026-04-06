from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore"
)

class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER:str
    POSTGRES_PORT:int
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_NAME:str

    model_config = _base_config

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"

db_settings = DatabaseSettings()