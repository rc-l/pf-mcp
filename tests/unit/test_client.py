"""Unit tests for PingFederate client."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from pf_mcp.client import PingFederateClient
from pf_mcp.config import Settings


@pytest.fixture
def settings() -> Settings:
    """Create test settings."""
    return Settings(
        pingfederate_base_url="https://test.example.com:9999",
        pingfederate_username="admin",
        pingfederate_password="password",
        pingfederate_verify_ssl=False,
    )


@pytest.fixture
def client(settings: Settings) -> PingFederateClient:
    """Create test client."""
    return PingFederateClient(settings)


@pytest.mark.asyncio
async def test_get_version(client: PingFederateClient) -> None:
    """Test getting PingFederate version."""
    expected_response = {"version": "11.3.0"}

    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = expected_response
        result = await client.get_version()

        mock_request.assert_called_once_with("GET", "/version")
        assert result == expected_response


@pytest.mark.asyncio
async def test_list_oauth_clients(client: PingFederateClient) -> None:
    """Test listing OAuth clients."""
    expected_response = {
        "items": [
            {"clientId": "client1", "name": "Client 1"},
            {"clientId": "client2", "name": "Client 2"},
        ]
    }

    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = expected_response
        result = await client.list_oauth_clients(page=1, number_per_page=10)

        mock_request.assert_called_once_with(
            "GET", "/oauth/clients", params={"page": 1, "numberPerPage": 10}
        )
        assert result == expected_response
        assert len(result["items"]) == 2


@pytest.mark.asyncio
async def test_get_oauth_client(client: PingFederateClient) -> None:
    """Test getting a specific OAuth client."""
    expected_response = {"clientId": "test-client", "name": "Test Client"}

    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = expected_response
        result = await client.get_oauth_client("test-client")

        mock_request.assert_called_once_with("GET", "/oauth/clients/test-client")
        assert result == expected_response


@pytest.mark.asyncio
async def test_create_oauth_client(client: PingFederateClient) -> None:
    """Test creating an OAuth client."""
    client_data = {"clientId": "new-client", "name": "New Client"}
    expected_response = {**client_data, "enabled": True}

    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = expected_response
        result = await client.create_oauth_client(client_data)

        mock_request.assert_called_once_with("POST", "/oauth/clients", json=client_data)
        assert result == expected_response


@pytest.mark.asyncio
async def test_update_oauth_client(client: PingFederateClient) -> None:
    """Test updating an OAuth client."""
    client_data = {"name": "Updated Client", "enabled": False}
    expected_response = {"clientId": "test-client", **client_data}

    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = expected_response
        result = await client.update_oauth_client("test-client", client_data)

        mock_request.assert_called_once_with(
            "PUT", "/oauth/clients/test-client", json=client_data
        )
        assert result == expected_response


@pytest.mark.asyncio
async def test_delete_oauth_client(client: PingFederateClient) -> None:
    """Test deleting an OAuth client."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {}
        result = await client.delete_oauth_client("test-client")

        mock_request.assert_called_once_with("DELETE", "/oauth/clients/test-client")
        assert result == {}


@pytest.mark.asyncio
async def test_list_idp_adapters(client: PingFederateClient) -> None:
    """Test listing IDP adapters."""
    expected_response = {
        "items": [{"id": "adapter1", "name": "Adapter 1"}]
    }

    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = expected_response
        result = await client.list_idp_adapters()

        mock_request.assert_called_once_with("GET", "/idp/adapters")
        assert result == expected_response
