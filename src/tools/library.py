"""Library tools for Spotify.

Requires scopes: user-library-read, user-library-modify.
Uses /me/library endpoints (not deprecated type-specific ones).
"""

from __future__ import annotations

from typing import Any

from dedalus_mcp import tool

from spotify.request import spotify_delete, spotify_get, spotify_put


@tool(description="Get the current user's saved tracks")
async def spotify_get_saved_tracks(limit: int = 20, offset: int = 0, market: str = "") -> dict[str, Any]:
    """Get a list of the songs saved in the current user's library.

    Args:
        limit: Max number of tracks to return (1-50, default 20).
        offset: Index of the first item (default 0).
        market: ISO 3166-1 alpha-2 country code for track relinking (optional).
    """
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if market:
        params["market"] = market
    return await spotify_get("/v1/me/tracks", params=params)


@tool(description="Save tracks to the current user's library")
async def spotify_save_tracks(ids: str) -> dict[str, Any]:
    """Save one or more tracks to the user's library.

    Args:
        ids: Comma-separated Spotify track IDs.
             e.g. "4iV5W9uYEdYUVa79Axb7Rh,1301WleyT98MSxVHPZCA6M"
    """
    track_ids = [t.strip() for t in ids.split(",")]
    await spotify_put("/v1/me/tracks", body={"ids": track_ids})
    return {"message": f"Saved {len(track_ids)} track(s) to library"}


@tool(description="Remove tracks from the current user's library")
async def spotify_remove_saved_tracks(ids: str) -> dict[str, Any]:
    """Remove one or more tracks from the user's library.

    Args:
        ids: Comma-separated Spotify track IDs.
    """
    track_ids = [t.strip() for t in ids.split(",")]
    await spotify_delete("/v1/me/tracks", body={"ids": track_ids})
    return {"message": f"Removed {len(track_ids)} track(s) from library"}


@tool(description="Check if tracks are saved in the user's library")
async def spotify_check_saved_tracks(ids: str) -> dict[str, Any]:
    """Check whether one or more tracks are already saved.

    Args:
        ids: Comma-separated Spotify track IDs.

    Returns:
        A dict mapping each track ID to True/False.
    """
    track_ids = [t.strip() for t in ids.split(",")]
    result = await spotify_get("/v1/me/tracks/contains", params={"ids": ",".join(track_ids)})
    if isinstance(result, list):
        return {"results": dict(zip(track_ids, result))}
    return result


@tool(description="Get the current user's saved albums")
async def spotify_get_saved_albums(limit: int = 20, offset: int = 0, market: str = "") -> dict[str, Any]:
    """Get a list of the albums saved in the current user's library.

    Args:
        limit: Max number of albums to return (1-50, default 20).
        offset: Index of the first item (default 0).
        market: ISO 3166-1 alpha-2 country code (optional).
    """
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if market:
        params["market"] = market
    return await spotify_get("/v1/me/albums", params=params)


@tool(description="Save albums to the current user's library")
async def spotify_save_albums(ids: str) -> dict[str, Any]:
    """Save one or more albums to the user's library.

    Args:
        ids: Comma-separated Spotify album IDs.
    """
    album_ids = [a.strip() for a in ids.split(",")]
    await spotify_put("/v1/me/albums", body={"ids": album_ids})
    return {"message": f"Saved {len(album_ids)} album(s) to library"}


@tool(description="Remove albums from the current user's library")
async def spotify_remove_saved_albums(ids: str) -> dict[str, Any]:
    """Remove one or more albums from the user's library.

    Args:
        ids: Comma-separated Spotify album IDs.
    """
    album_ids = [a.strip() for a in ids.split(",")]
    await spotify_delete("/v1/me/albums", body={"ids": album_ids})
    return {"message": f"Removed {len(album_ids)} album(s) from library"}


library_tools = [
    spotify_get_saved_tracks,
    spotify_save_tracks,
    spotify_remove_saved_tracks,
    spotify_check_saved_tracks,
    spotify_get_saved_albums,
    spotify_save_albums,
    spotify_remove_saved_albums,
]
