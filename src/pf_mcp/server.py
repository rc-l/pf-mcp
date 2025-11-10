"""MCP Server implementation for PingFederate."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .client import PingFederateClient
from .config import get_settings

logger = logging.getLogger(__name__)


class PingFederateMCPServer:
    """MCP Server for PingFederate administrative operations."""

    def __init__(self) -> None:
        """Initialize the MCP server."""
        self.settings = get_settings()
        self.client = PingFederateClient(self.settings)
        self.server = Server(self.settings.mcp_server_name)
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up MCP server handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="get_version",
                    description="Get PingFederate server version",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
                Tool(
                    name="list_oauth_clients",
                    description="List all OAuth 2.0 clients",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "integer",
                                "description": "Page number (default: 1)",
                                "minimum": 1,
                            },
                            "numberPerPage": {
                                "type": "integer",
                                "description": "Items per page (default: 10, max: 100)",
                                "minimum": 1,
                                "maximum": 100,
                            },
                        },
                    },
                ),
                Tool(
                    name="get_oauth_client",
                    description="Get details of a specific OAuth 2.0 client",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "clientId": {
                                "type": "string",
                                "description": "OAuth client ID",
                            }
                        },
                        "required": ["clientId"],
                    },
                ),
                Tool(
                    name="create_oauth_client",
                    description="Create a new OAuth 2.0 client",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "clientId": {"type": "string", "description": "Unique client ID"},
                            "name": {"type": "string", "description": "Client name"},
                            "description": {"type": "string", "description": "Client description"},
                            "enabled": {
                                "type": "boolean",
                                "description": "Enable the client",
                                "default": True,
                            },
                            "grantTypes": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Allowed OAuth grant types",
                            },
                            "redirectUris": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Allowed redirect URIs",
                            },
                        },
                        "required": ["clientId", "name"],
                    },
                ),
                Tool(
                    name="update_oauth_client",
                    description="Update an existing OAuth 2.0 client",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "clientId": {"type": "string", "description": "Client ID to update"},
                            "name": {"type": "string", "description": "Updated client name"},
                            "description": {"type": "string", "description": "Updated description"},
                            "enabled": {"type": "boolean", "description": "Enable/disable client"},
                            "grantTypes": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Updated grant types",
                            },
                            "redirectUris": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Updated redirect URIs",
                            },
                        },
                        "required": ["clientId"],
                    },
                ),
                Tool(
                    name="delete_oauth_client",
                    description="Delete an OAuth 2.0 client",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "clientId": {"type": "string", "description": "Client ID to delete"}
                        },
                        "required": ["clientId"],
                    },
                ),
                Tool(
                    name="list_idp_adapters",
                    description="List all identity provider adapters",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Call a tool with the given arguments."""
            try:
                if name == "get_version":
                    result = await self.client.get_version()
                elif name == "list_oauth_clients":
                    page = arguments.get("page", 1)
                    number_per_page = arguments.get("numberPerPage", 10)
                    result = await self.client.list_oauth_clients(page, number_per_page)
                elif name == "get_oauth_client":
                    result = await self.client.get_oauth_client(arguments["clientId"])
                elif name == "create_oauth_client":
                    result = await self.client.create_oauth_client(arguments)
                elif name == "update_oauth_client":
                    client_id = arguments.pop("clientId")
                    result = await self.client.update_oauth_client(client_id, arguments)
                elif name == "delete_oauth_client":
                    result = await self.client.delete_oauth_client(arguments["clientId"])
                elif name == "list_idp_adapters":
                    result = await self.client.list_idp_adapters()
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]

                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    async def run(self) -> None:
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, self.server.create_initialization_options())


def main() -> None:
    """Main entry point for the MCP server."""
    logging.basicConfig(level=logging.INFO)
    server = PingFederateMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
