"""Application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven application settings."""

    environment: str = "dev"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="SEMICONDUCTOR_RAG_",
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
