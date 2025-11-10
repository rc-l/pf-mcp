"""Example: Create OAuth Client

This example demonstrates how to create a new OAuth client in PingFederate.
"""

import asyncio
from pf_mcp.client import PingFederateClient
from pf_mcp.config import get_settings


async def main() -> None:
    """Main function to create an OAuth client."""
    # Get settings from environment
    settings = get_settings()

    # Create client
    client = PingFederateClient(settings)

    # Define the OAuth client
    oauth_client = {
        "clientId": "example-client",
        "name": "Example OAuth Client",
        "description": "An example OAuth 2.0 client created via MCP",
        "enabled": True,
        "grantTypes": ["authorization_code", "refresh_token"],
        "redirectUris": ["https://example.com/callback"],
    }

    try:
        # Create the client
        print("Creating OAuth client...")
        result = await client.create_oauth_client(oauth_client)
        print(f"Successfully created OAuth client: {result['clientId']}")
        print(f"Client name: {result['name']}")
        print(f"Grant types: {result.get('grantTypes', [])}")

        # Verify by fetching it
        print("\nVerifying creation...")
        fetched = await client.get_oauth_client("example-client")
        print(f"Client verified: {fetched['name']}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
