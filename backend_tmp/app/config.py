import os
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict

from loguru import logger

logger.remove()

# DEBUG и выше — в консоль
logger.add(sys.stderr, level="DEBUG", format="{time} | {level} | {message}")

# Только INFO и выше — в файл
logger.add(
    "logs/app.log",
    level="INFO",
    rotation="10 MB",
    retention="10 days",
    format="{time} | {level} | {message}",
)


class Settings(BaseSettings):
    # 👉 URL Keycloak сервера
    KEYCLOAK_BASE_URL: str
    BASE_URL: str
    REALM: str
    CLIENT_ID: str
    CLIENT_SECRET: str

    # 👉 URL ZEEBE сервер
    ZEEBE_ADDRESS: str = "localhost:26500"
    ZEEBE_AUTHORIZATION_SERVER_URL: str = os.getenv(
        "ZEEBE_AUTHORIZATION_SERVER_URL", ""
    )
    ZEEBE_CLIENT_ID: str = os.getenv("ZEEBE_CLIENT_ID", "zeebe")
    ZEEBE_CLIENT_SECRET: str = os.getenv("ZEEBE_CLIENT_SECRET", "zecret")

    CAMUNDA_TASKLIST_BASE_URL: str = os.getenv(
        "CAMUNDA_TASKLIST_BASE_URL", "http://localhost:8082"
    )
    CAMUNDA_TASKLIST_BASE_URL_v2: str = os.getenv(
        "CAMUNDA_TASKLIST_BASE_URL_V2", "http://localhost:8088"
    )

    CAMUNDA_OPERATE_BASE_URL: str = os.getenv(
        "CAMUNDA_OPERATE_BASE_URL", "http://localhost:8081"
    )
    
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    OPERATE_TOKEN: str = os.getenv("OPERATE_TOKEN", "")

    DADATA_TOKEN: str = os.getenv("DADATA_TOKEN", "")

    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.BASE_DIR}/data/db.sqlite3"

    # Вычисляемые URL
    @property
    def token_url(self) -> str:
        return f"{self.KEYCLOAK_BASE_URL}/realms/{self.REALM}/protocol/openid-connect/token"

    @property
    def auth_url(self) -> str:
        return (
            f"{self.KEYCLOAK_BASE_URL}/realms/{self.REALM}/protocol/openid-connect/auth"
        )

    @property
    def logout_url(self) -> str:
        return f"{self.KEYCLOAK_BASE_URL}/realms/{self.REALM}/protocol/openid-connect/logout"

    @property
    def userinfo_url(self) -> str:
        return f"{self.KEYCLOAK_BASE_URL}/realms/{self.REALM}/protocol/openid-connect/userinfo"

    @property
    def redirect_uri(self) -> str:
        return f"{self.BASE_URL}/api/login/callback"

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


settings = Settings()  # type: ignore
