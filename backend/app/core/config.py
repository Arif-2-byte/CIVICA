from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings
    Loaded automatically from environment variables or .env file.
    """

    # ==========================================================
    # Application
    # ==========================================================

    APP_NAME: str = "CIVICA API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False

    # ==========================================================
    # Database
    # ==========================================================

    DATABASE_URL: str

    # ==========================================================
    # JWT
    # ==========================================================

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # New (Refresh Token)
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ==========================================================
    # Configuration
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached application settings.
    """
    return Settings()


settings = get_settings()