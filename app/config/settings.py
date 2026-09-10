from urllib.parse import quote_plus
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./business.db"
    db_host: str | None = None
    db_user: str | None = None
    db_pass: str | None = None
    db_port: int = 3306
    db_name: str = "business"
    jwt_secret_key: str = Field(min_length=32)
    jwt_algorithm: str
    jwt_access_token_minutes: int
    bot_api_url: str = "http://127.0.0.1:4159"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def resolved_database_url(self) -> str:
        """Build a MySQL URL from DB_* settings, or use DATABASE_URL otherwise."""
        if not self.db_host:
            return self.database_url
        if not self.db_user or self.db_pass is None:
            raise ValueError("DB_USER y DB_PASS son obligatorios cuando se define DB_HOST")
        user = quote_plus(self.db_user)
        password = quote_plus(self.db_pass)
        return f"mysql+pymysql://{user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"


settings = Settings()
