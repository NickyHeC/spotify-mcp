"""User profile and personalization tools for Spotify.

Requires scopes: user-read-private, user-read-email, user-top-read,
user-read-recently-played.
"""

from __future__ import annotations

from typing import Any

from dedalus_mcp import tool

from spotify.request import spotify_get


@tool(description="Get the current user's Spotify profile")
async def spotify_get_current_user() -> dict[str, Any]:
    """Get detailed profile information about the current user."""
    return await spotify_get("/v1/me")


@tool(description="Get a user's public profile by their Spotify user ID")
async def spotify_get_user_profile(user_id: str) -> dict[str, Any]:
    """Get public profile information about a Spotify user.

    Args:
        user_id: The Spotify user ID.
    """
    return await spotify_get(f"/v1/users/{user_id}")


@tool(description="Get the current user's top artists or tracks")
async def spotify_get_top_items(
    item_type: str = "tracks",
    time_range: str = "medium_term",
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """Get the user's top artists or tracks based on listening history.

    Args:
        item_type: "artists" or "tracks" (default "tracks").
        time_range: Time window — "short_term" (~4 weeks),
                    "medium_term" (~6 months), or "long_term" (all time).
                    Default: "medium_term".
        limit: Max number of items to return (1-50, default 20).
        offset: Index of the first item (default 0).
    """
    return await spotify_get(
        f"/v1/me/top/{item_type}",
        params={"time_range": time_range, "limit": limit, "offset": offset},
    )


@tool(description="Get the user's recently played tracks")
async def spotify_get_recently_played(limit: int = 20) -> dict[str, Any]:
    """Get tracks from the user's recent listening history.

    Args:
        limit: Max number of items to return (1-50, default 20).
    """
    return await spotify_get("/v1/me/player/recently-played", params={"limit": limit})


user_tools = [
    spotify_get_current_user,
    spotify_get_user_profile,
    spotify_get_top_items,
    spotify_get_recently_played,
]
