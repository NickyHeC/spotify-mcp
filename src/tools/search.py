"""Search tools for Spotify."""

from __future__ import annotations

from typing import Any

from dedalus_mcp import tool

from spotify.request import spotify_get


@tool(description="Search Spotify for tracks, artists, albums, playlists, shows, or episodes")
async def spotify_search(
    query: str,
    search_type: str = "track",
    limit: int = 10,
    offset: int = 0,
    market: str = "",
) -> dict[str, Any]:
    """Search the Spotify catalog.

    Args:
        query: Search query (e.g. "Bohemian Rhapsody", "artist:Queen").
               Supports field filters: album, artist, track, year, genre, tag.
        search_type: Comma-separated types to search: track, artist, album,
                     playlist, show, episode. Default: "track".
        limit: Max results per type (1-50, default 10).
        offset: Index of first result (default 0).
        market: ISO 3166-1 alpha-2 country code for market filtering (optional).
    """
    params: dict[str, Any] = {
        "q": query,
        "type": search_type,
        "limit": limit,
        "offset": offset,
    }
    if market:
        params["market"] = market

    return await spotify_get("/v1/search", params=params)


search_tools = [
    spotify_search,
]
