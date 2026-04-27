"""Spotify connection configuration.

Evaluated at import time, after ``load_dotenv()`` in ``main.py``
has already injected the .env file.

Spotify uses OAuth2 for authentication. The Dedalus platform handles
token exchange; the server only declares the secret name it expects.
"""

from __future__ import annotations

from dedalus_mcp.auth import Connection, SecretKeys


spotify = Connection(
    name="spotify-mcp",
    secrets=SecretKeys(token="SPOTIFY_ACCESS_TOKEN"),
    base_url="https://api.spotify.com",
    auth_header_format="Bearer {api_key}",
)
