from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore"
)

class DatabaseSettings(BaseSettings):
    DATABASE_URL: str

    model_config = _base_config

    @property
    def POSTGRES_URL(self):
        return self.DATABASE_URL
