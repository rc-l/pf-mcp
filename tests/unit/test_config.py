"""Unit tests for configuration."""

import pytest
from pf_mcp.config import Settings, get_settings


def test_settings_defaults() -> None:
    """Test default settings values."""
    settings = Settings(pingfederate_password="test123")

    assert settings.pingfederate_base_url == "https://localhost:9999"
    assert settings.pingfederate_username == "administrator"
    assert settings.pingfederate_api_version == "11.3"
    assert settings.pingfederate_verify_ssl is True
    assert settings.mcp_server_name == "pingfederate"
    assert settings.log_level == "INFO"


def test_settings_custom_values() -> None:
    """Test custom settings values."""
    settings = Settings(
        pingfederate_base_url="https://custom.com:8443",
        pingfederate_username="admin",
        pingfederate_password="secret",
        pingfederate_api_version="12.0",
        pingfederate_verify_ssl=False,
        log_level="DEBUG",
    )

    assert settings.pingfederate_base_url == "https://custom.com:8443"
    assert settings.pingfederate_username == "admin"
    assert settings.pingfederate_password == "secret"
    assert settings.pingfederate_api_version == "12.0"
    assert settings.pingfederate_verify_ssl is False
    assert settings.log_level == "DEBUG"


def test_get_settings() -> None:
    """Test get_settings function."""
    settings = get_settings()
    assert isinstance(settings, Settings)
