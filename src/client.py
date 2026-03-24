"""Test client for Spotify MCP server.

Start the server first:
    python -m src.main

Then run this script to verify tools work:
    python -m src.client
"""

import asyncio
import os

from dedalus_mcp.client import MCPClient


async def main() -> None:
    url = os.getenv("MCP_URL", "http://127.0.0.1:8080/mcp")
    print(f"Connecting to {url}...")

    client = await MCPClient.connect(url)

    tools = await client.list_tools()
    print(f"Available tools ({len(tools.tools)}):")
    for t in tools.tools:
        print(f"  - {t.name}: {getattr(t, 'description', '')}")

    await client.close()
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
