"""MCP server entrypoint.

Expose Spotify tools via Dedalus MCP framework.
OAuth credentials provided by DAuth at runtime.
"""

import os

from dedalus_mcp import MCPServer
from dedalus_mcp.server import TransportSecuritySettings

from spotify.config import spotify
from tools import spotify_tools


def create_server() -> MCPServer:
    """Create MCP server with current env config."""
    as_url = os.getenv("DEDALUS_AS_URL", "https://as.dedaluslabs.ai")
    server = MCPServer(
        name="spotify-mcp",
        connections=[spotify],
        http_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
        streamable_http_stateless=True,
        authorization_server=as_url,
    )
    return server


async def main() -> None:
    """Start MCP server."""
    server = create_server()
    server.collect(*spotify_tools)
    await server.serve(port=8080)
