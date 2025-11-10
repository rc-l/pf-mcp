"""Configuration management for PingFederate MCP Server."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # PingFederate connection settings
    pingfederate_base_url: str = "https://localhost:9999"
    pingfederate_username: str = "administrator"
    pingfederate_password: str = ""
    pingfederate_api_version: str = "11.3"
    pingfederate_verify_ssl: bool = True

    # MCP Server settings
    mcp_server_name: str = "pingfederate"
    mcp_server_version: str = "0.1.0"

    # Logging
    log_level: str = "INFO"


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
