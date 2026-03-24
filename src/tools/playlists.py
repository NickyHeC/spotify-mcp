"""Playlist tools for Spotify.

Requires scopes: playlist-read-private, playlist-read-collaborative,
playlist-modify-public, playlist-modify-private.
"""

from __future__ import annotations

from typing import Any

from dedalus_mcp import tool

from spotify.request import spotify_delete, spotify_get, spotify_post, spotify_put


@tool(description="Get detailed information about a Spotify playlist")
async def spotify_get_playlist(playlist_id: str) -> dict[str, Any]:
    """Get a playlist by its Spotify ID.

    Args:
        playlist_id: The Spotify ID of the playlist.
    """
    return await spotify_get(f"/v1/playlists/{playlist_id}")


@tool(description="Get items (tracks/episodes) in a playlist")
async def spotify_get_playlist_items(
    playlist_id: str, limit: int = 20, offset: int = 0
) -> dict[str, Any]:
    """Get items in a playlist. Uses /playlists/{id}/items (not deprecated /tracks).

    Args:
        playlist_id: The Spotify ID of the playlist.
        limit: Max number of items to return (1-50, default 20).
        offset: Index of the first item to return (default 0).
    """
    return await spotify_get(
        f"/v1/playlists/{playlist_id}/items",
        params={"limit": limit, "offset": offset},
    )


@tool(description="List the current user's playlists")
async def spotify_list_my_playlists(limit: int = 20, offset: int = 0) -> dict[str, Any]:
    """Get a list of the playlists owned or followed by the current user.

    Args:
        limit: Max number of playlists to return (1-50, default 20).
        offset: Index of the first playlist to return (default 0).
    """
    return await spotify_get(
        "/v1/me/playlists",
        params={"limit": limit, "offset": offset},
    )


@tool(description="Create a new playlist for the current user")
async def spotify_create_playlist(
    name: str,
    description: str = "",
    public: bool = True,
    collaborative: bool = False,
) -> dict[str, Any]:
    """Create a new playlist.

    Args:
        name: Name for the new playlist.
        description: Optional playlist description.
        public: Whether the playlist is public (default True).
        collaborative: Whether the playlist is collaborative (default False).
                       Must set public=False if collaborative=True.
    """
    user = await spotify_get("/v1/me")
    user_id = user["id"]

    body: dict[str, Any] = {"name": name, "public": public, "collaborative": collaborative}
    if description:
        body["description"] = description

    return await spotify_post(f"/v1/users/{user_id}/playlists", body=body)


@tool(description="Add tracks or episodes to a playlist")
async def spotify_add_to_playlist(
    playlist_id: str,
    uris: str,
    position: int = -1,
) -> dict[str, Any]:
    """Add one or more items to a playlist.

    Args:
        playlist_id: The Spotify ID of the playlist.
        uris: Comma-separated Spotify URIs to add.
              e.g. "spotify:track:4iV5W9uYEdYUVa79Axb7Rh,spotify:track:1301WleyT98MSxVHPZCA6M"
        position: Position (0-indexed) to insert the items. Use -1 to append.
    """
    body: dict[str, Any] = {"uris": [u.strip() for u in uris.split(",")]}
    if position >= 0:
        body["position"] = position

    return await spotify_post(f"/v1/playlists/{playlist_id}/items", body=body)


@tool(description="Remove tracks or episodes from a playlist")
async def spotify_remove_from_playlist(
    playlist_id: str,
    uris: str,
) -> dict[str, Any]:
    """Remove items from a playlist.

    Args:
        playlist_id: The Spotify ID of the playlist.
        uris: Comma-separated Spotify URIs to remove.
    """
    tracks = [{"uri": u.strip()} for u in uris.split(",")]
    return await spotify_delete(
        f"/v1/playlists/{playlist_id}/items",
        body={"tracks": tracks},
    )


@tool(description="Update a playlist's name, description, or visibility")
async def spotify_update_playlist(
    playlist_id: str,
    name: str = "",
    description: str = "",
    public: bool = True,
    collaborative: bool = False,
) -> dict[str, Any]:
    """Update playlist details.

    Args:
        playlist_id: The Spotify ID of the playlist.
        name: New name (leave empty to keep current).
        description: New description (leave empty to keep current).
        public: Whether the playlist is public.
        collaborative: Whether the playlist is collaborative.
    """
    body: dict[str, Any] = {"public": public, "collaborative": collaborative}
    if name:
        body["name"] = name
    if description:
        body["description"] = description

    await spotify_put(f"/v1/playlists/{playlist_id}", body=body)
    return {"message": f"Playlist {playlist_id} updated"}


playlist_tools = [
    spotify_get_playlist,
    spotify_get_playlist_items,
    spotify_list_my_playlists,
    spotify_create_playlist,
    spotify_add_to_playlist,
    spotify_remove_from_playlist,
    spotify_update_playlist,
]
