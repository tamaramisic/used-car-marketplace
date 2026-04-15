from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file="./.env", env_ignore_empty=True, extra="ignore"
)


class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_NAME: str

    model_config = _base_config

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"


class KeycloakSettings(BaseSettings):
    KEYCLOAK_SERVER: str
    KEYCLOAK_PORT: int
    KEYCLOAK_REALM_NAME: str
    KEYCLOAK_CLIENT_ID: str
    ADMIN_CLIENT_ID: str
    ADMIN_CLIENT_SECRET: str
    model_config = _base_config

    @property
    def KEYCLOAK_BASE_URL(self):
        return f"http://{self.KEYCLOAK_SERVER}:{self.KEYCLOAK_PORT}"

    @property
    def OPENID_BASE_URL(self):
        return f"{self.KEYCLOAK_BASE_URL}/realms/{self.KEYCLOAK_REALM_NAME}/protocol/openid-connect"

    @property
    def JWKS_URL(self):
        return f"{self.OPENID_BASE_URL}/certs"

    @property
    def AUTH_URL(self):
        return f"{self.OPENID_BASE_URL}/auth"

    @property
    def TOKEN_URL(self):
        return f"{self.OPENID_BASE_URL}/token"


keycloak_settings = KeycloakSettings()
db_settings = DatabaseSettings()
