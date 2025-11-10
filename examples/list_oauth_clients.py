"""Example: List OAuth Clients

This example demonstrates how to list all OAuth clients from PingFederate.
"""

import asyncio
from pf_mcp.client import PingFederateClient
from pf_mcp.config import get_settings


async def main() -> None:
    """Main function to list OAuth clients."""
    # Get settings from environment
    settings = get_settings()

    # Create client
    client = PingFederateClient(settings)

    try:
        # Get version info
        print("Getting PingFederate version...")
        version = await client.get_version()
        print(f"PingFederate version: {version['version']}")

        # List OAuth clients
        print("\nListing OAuth clients...")
        clients = await client.list_oauth_clients(page=1, number_per_page=10)

        if "items" in clients and clients["items"]:
            print(f"\nFound {len(clients['items'])} OAuth clients:")
            for client_info in clients["items"]:
                print(f"  - {client_info['clientId']}: {client_info['name']}")
        else:
            print("No OAuth clients found")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
