"""PingFederate API client."""

import logging
from typing import Any, Optional
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel

from .config import Settings

logger = logging.getLogger(__name__)


class PingFederateClient:
    """Client for interacting with PingFederate Admin API."""

    def __init__(self, settings: Settings):
        """Initialize the PingFederate client.

        Args:
            settings: Application settings containing connection details
        """
        self.settings = settings
        self.base_url = f"{settings.pingfederate_base_url}/pf-admin-api/v1"
        self.auth = (settings.pingfederate_username, settings.pingfederate_password)
        self.verify_ssl = settings.pingfederate_verify_ssl

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to the PingFederate API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Query parameters
            json: Request body for POST/PUT

        Returns:
            Response data as dictionary

        Raises:
            httpx.HTTPStatusError: If the request fails
        """
        url = urljoin(self.base_url, path)

        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            response = await client.request(
                method=method,
                url=url,
                auth=self.auth,
                params=params,
                json=json,
                headers={"Accept": "application/json", "Content-Type": "application/json"},
            )
            response.raise_for_status()

            # Handle 204 No Content
            if response.status_code == 204:
                return {}

            return response.json()

    async def get_version(self) -> dict[str, Any]:
        """Get PingFederate version.

        Returns:
            Version information
        """
        return await self._request("GET", "/version")

    async def list_oauth_clients(
        self, page: int = 1, number_per_page: int = 10
    ) -> dict[str, Any]:
        """List OAuth clients.

        Args:
            page: Page number
            number_per_page: Number of items per page

        Returns:
            List of OAuth clients
        """
        return await self._request(
            "GET", "/oauth/clients", params={"page": page, "numberPerPage": number_per_page}
        )

    async def get_oauth_client(self, client_id: str) -> dict[str, Any]:
        """Get OAuth client details.

        Args:
            client_id: OAuth client ID

        Returns:
            OAuth client details
        """
        return await self._request("GET", f"/oauth/clients/{client_id}")

    async def create_oauth_client(self, client_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new OAuth client.

        Args:
            client_data: OAuth client configuration

        Returns:
            Created OAuth client
        """
        return await self._request("POST", "/oauth/clients", json=client_data)

    async def update_oauth_client(
        self, client_id: str, client_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an existing OAuth client.

        Args:
            client_id: OAuth client ID
            client_data: Updated OAuth client configuration

        Returns:
            Updated OAuth client
        """
        return await self._request("PUT", f"/oauth/clients/{client_id}", json=client_data)

    async def delete_oauth_client(self, client_id: str) -> dict[str, Any]:
        """Delete an OAuth client.

        Args:
            client_id: OAuth client ID

        Returns:
            Empty dict on success
        """
        return await self._request("DELETE", f"/oauth/clients/{client_id}")

    async def list_idp_adapters(self) -> dict[str, Any]:
        """List identity provider adapters.

        Returns:
            List of IDP adapters
        """
        return await self._request("GET", "/idp/adapters")
