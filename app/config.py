from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "A.S.A.S. Cloud"
    environment: str = "development"

    database_url: str = "postgresql+psycopg://asas:asas@db:5432/asas"
    redis_url: str = "redis://redis:6379/0"

    secret_key: str = "change-this-development-secret"
    access_token_expire_minutes: int = 60

    cors_origins: str = "http://localhost:8080,http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
