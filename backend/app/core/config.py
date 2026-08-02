from functools import lru_cache
from typing import Annotated, Literal

from pydantic import BeforeValidator, Field, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


def _split_csv(value: object) -> object:
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    return value


CsvList = Annotated[list[str], NoDecode, BeforeValidator(_split_csv)]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    app_name: str = "secure-healthcare-api"
    app_version: str = "1.0.0"
    app_env: Literal["development", "test", "staging", "production"] = "development"
    app_debug: bool = False
    database_url: str = "postgresql+psycopg://healthcare_app:change_me@localhost:5432/healthcare"
    jwt_issuer: str = "https://localhost:9443/oauth2/token"
    jwt_audience: str = "secure-healthcare-api"
    jwks_url: str = "https://localhost:9443/oauth2/jwks"
    jwt_algorithms: CsvList = ["RS256"]
    allowed_origins: CsvList = ["http://localhost:3000"]
    log_level: str = "INFO"
    access_token_leeway_seconds: int = Field(30, ge=0, le=300)
    max_page_size: int = Field(100, ge=1, le=1000)
    default_page_size: int = Field(20, ge=1)
    max_request_body_bytes: int = Field(1_048_576, ge=1024)

    @model_validator(mode="after")
    def secure_production(self) -> "Settings":
        if self.default_page_size > self.max_page_size:
            raise ValueError("DEFAULT_PAGE_SIZE cannot exceed MAX_PAGE_SIZE")
        if self.app_env == "production" and self.app_debug:
            raise ValueError("Debug mode is prohibited in production")
        if self.app_env == "production" and "*" in self.allowed_origins:
            raise ValueError("Wildcard CORS is prohibited in production")
        if not self.jwt_algorithms or any(a.lower() == "none" for a in self.jwt_algorithms):
            raise ValueError("At least one secure JWT algorithm is required")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
