"""Track, album, and artist info tools for Spotify."""

from __future__ import annotations

from typing import Any

from dedalus_mcp import tool

from spotify.request import spotify_get


@tool(description="Get detailed information about a track by its Spotify ID")
async def spotify_get_track(track_id: str, market: str = "") -> dict[str, Any]:
    """Get Spotify catalog information for a single track.

    Args:
        track_id: The Spotify ID of the track.
        market: ISO 3166-1 alpha-2 country code (optional).
    """
    params: dict[str, Any] = {}
    if market:
        params["market"] = market
    return await spotify_get(f"/v1/tracks/{track_id}", params=params or None)


@tool(description="Get detailed information about multiple tracks")
async def spotify_get_tracks(ids: str, market: str = "") -> dict[str, Any]:
    """Get Spotify catalog information for multiple tracks.

    Args:
        ids: Comma-separated Spotify track IDs (max 50).
        market: ISO 3166-1 alpha-2 country code (optional).
    """
    params: dict[str, Any] = {"ids": ids}
    if market:
        params["market"] = market
    return await spotify_get("/v1/tracks", params=params)


@tool(description="Get detailed information about an album by its Spotify ID")
async def spotify_get_album(album_id: str, market: str = "") -> dict[str, Any]:
    """Get Spotify catalog information for a single album.

    Args:
        album_id: The Spotify ID of the album.
        market: ISO 3166-1 alpha-2 country code (optional).
    """
    params: dict[str, Any] = {}
    if market:
        params["market"] = market
    return await spotify_get(f"/v1/albums/{album_id}", params=params or None)


@tool(description="Get the tracks in an album")
async def spotify_get_album_tracks(
    album_id: str, limit: int = 20, offset: int = 0, market: str = ""
) -> dict[str, Any]:
    """Get tracks in an album.

    Args:
        album_id: The Spotify ID of the album.
        limit: Max number of tracks to return (1-50, default 20).
        offset: Index of the first track (default 0).
        market: ISO 3166-1 alpha-2 country code (optional).
    """
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if market:
        params["market"] = market
    return await spotify_get(f"/v1/albums/{album_id}/tracks", params=params)


@tool(description="Get detailed information about an artist by their Spotify ID")
async def spotify_get_artist(artist_id: str) -> dict[str, Any]:
    """Get Spotify catalog information for a single artist.

    Args:
        artist_id: The Spotify ID of the artist.
    """
    return await spotify_get(f"/v1/artists/{artist_id}")


@tool(description="Get an artist's top tracks by country")
async def spotify_get_artist_top_tracks(artist_id: str, market: str = "US") -> dict[str, Any]:
    """Get an artist's top tracks for a given market.

    Args:
        artist_id: The Spotify ID of the artist.
        market: ISO 3166-1 alpha-2 country code (default "US").
    """
    return await spotify_get(
        f"/v1/artists/{artist_id}/top-tracks",
        params={"market": market},
    )


@tool(description="Get artists related to a given artist")
async def spotify_get_related_artists(artist_id: str) -> dict[str, Any]:
    """Get artists similar to a given artist.

    Args:
        artist_id: The Spotify ID of the artist.
    """
    return await spotify_get(f"/v1/artists/{artist_id}/related-artists")


@tool(description="Get Spotify recommendations based on seed tracks, artists, or genres")
async def spotify_get_recommendations(
    seed_tracks: str = "",
    seed_artists: str = "",
    seed_genres: str = "",
    limit: int = 20,
    market: str = "",
) -> dict[str, Any]:
    """Get track recommendations based on seeds.

    You must provide at least one seed (tracks, artists, or genres).
    Up to 5 seeds total across all three types.

    Args:
        seed_tracks: Comma-separated track IDs (optional).
        seed_artists: Comma-separated artist IDs (optional).
        seed_genres: Comma-separated genre names (optional).
                     e.g. "rock,pop,electronic"
        limit: Number of recommended tracks (1-100, default 20).
        market: ISO 3166-1 alpha-2 country code (optional).
    """
    params: dict[str, Any] = {"limit": limit}
    if seed_tracks:
        params["seed_tracks"] = seed_tracks
    if seed_artists:
        params["seed_artists"] = seed_artists
    if seed_genres:
        params["seed_genres"] = seed_genres
    if market:
        params["market"] = market

    return await spotify_get("/v1/recommendations", params=params)


track_tools = [
    spotify_get_track,
    spotify_get_tracks,
    spotify_get_album,
    spotify_get_album_tracks,
    spotify_get_artist,
    spotify_get_artist_top_tracks,
    spotify_get_related_artists,
    spotify_get_recommendations,
]
