"""Playback control tools for Spotify.

Requires scopes: user-read-playback-state, user-modify-playback-state,
user-read-currently-playing, app-remote-control.
"""

from __future__ import annotations

from typing import Any

from dedalus_mcp import tool

from spotify.request import spotify_get, spotify_post, spotify_put


@tool(description="Get the current playback state including track, device, and progress")
async def spotify_get_playback_state() -> dict[str, Any]:
    """Returns information about the user's current playback state,
    including track or episode, progress, and active device."""
    result = await spotify_get("/v1/me/player")
    return result if result else {"message": "No active playback session"}


@tool(description="Get the currently playing track or episode")
async def spotify_get_currently_playing() -> dict[str, Any]:
    """Returns the currently playing track or episode on the user's account."""
    result = await spotify_get("/v1/me/player/currently-playing")
    return result if result else {"message": "Nothing currently playing"}


@tool(description="Start or resume playback on a device")
async def spotify_play(
    device_id: str = "",
    context_uri: str = "",
    uris: str = "",
    offset_position: int = -1,
    position_ms: int = 0,
) -> dict[str, Any]:
    """Start or resume playback.

    Args:
        device_id: Target device ID (optional, uses active device if empty).
        context_uri: Spotify URI of context to play (album, artist, playlist).
                     e.g. "spotify:album:1Je1IMUlBXcx1Fz0WE7oPT"
        uris: Comma-separated Spotify track URIs to play.
              e.g. "spotify:track:4iV5W9uYEdYUVa79Axb7Rh,spotify:track:1301WleyT98MSxVHPZCA6M"
        offset_position: Position in the context to start playback (0-indexed).
                         Only valid when context_uri is set. Use -1 to skip.
        position_ms: Position in milliseconds to seek to (default: 0).
    """
    body: dict[str, Any] = {}
    if context_uri:
        body["context_uri"] = context_uri
    if uris:
        body["uris"] = [u.strip() for u in uris.split(",")]
    if offset_position >= 0:
        body["offset"] = {"position": offset_position}
    if position_ms > 0:
        body["position_ms"] = position_ms

    params = f"?device_id={device_id}" if device_id else ""
    await spotify_put(f"/v1/me/player/play{params}", body=body if body else None)
    return {"message": "Playback started"}


@tool(description="Pause playback on the user's active device")
async def spotify_pause(device_id: str = "") -> dict[str, Any]:
    """Pause playback on the active device.

    Args:
        device_id: Target device ID (optional, uses active device if empty).
    """
    params = f"?device_id={device_id}" if device_id else ""
    await spotify_put(f"/v1/me/player/pause{params}")
    return {"message": "Playback paused"}


@tool(description="Skip to the next track in the queue")
async def spotify_skip_next(device_id: str = "") -> dict[str, Any]:
    """Skip to the next track.

    Args:
        device_id: Target device ID (optional).
    """
    params = f"?device_id={device_id}" if device_id else ""
    await spotify_post(f"/v1/me/player/next{params}")
    return {"message": "Skipped to next track"}


@tool(description="Skip to the previous track")
async def spotify_skip_previous(device_id: str = "") -> dict[str, Any]:
    """Skip to the previous track.

    Args:
        device_id: Target device ID (optional).
    """
    params = f"?device_id={device_id}" if device_id else ""
    await spotify_post(f"/v1/me/player/previous{params}")
    return {"message": "Skipped to previous track"}


@tool(description="Seek to a position in the currently playing track")
async def spotify_seek(position_ms: int, device_id: str = "") -> dict[str, Any]:
    """Seek to a position in the currently playing track.

    Args:
        position_ms: Position in milliseconds to seek to.
        device_id: Target device ID (optional).
    """
    params = f"?position_ms={position_ms}"
    if device_id:
        params += f"&device_id={device_id}"
    await spotify_put(f"/v1/me/player/seek{params}")
    return {"message": f"Seeked to {position_ms}ms"}


@tool(description="Set playback volume (0-100)")
async def spotify_set_volume(volume_percent: int, device_id: str = "") -> dict[str, Any]:
    """Set the volume for the active device.

    Args:
        volume_percent: Volume level (0 to 100).
        device_id: Target device ID (optional).
    """
    params = f"?volume_percent={volume_percent}"
    if device_id:
        params += f"&device_id={device_id}"
    await spotify_put(f"/v1/me/player/volume{params}")
    return {"message": f"Volume set to {volume_percent}%"}


@tool(description="Toggle shuffle mode on or off")
async def spotify_set_shuffle(state: bool, device_id: str = "") -> dict[str, Any]:
    """Toggle shuffle mode.

    Args:
        state: True to enable shuffle, False to disable.
        device_id: Target device ID (optional).
    """
    params = f"?state={'true' if state else 'false'}"
    if device_id:
        params += f"&device_id={device_id}"
    await spotify_put(f"/v1/me/player/shuffle{params}")
    return {"message": f"Shuffle {'enabled' if state else 'disabled'}"}


@tool(description="Set repeat mode: track, context, or off")
async def spotify_set_repeat(state: str, device_id: str = "") -> dict[str, Any]:
    """Set the repeat mode.

    Args:
        state: Repeat mode — "track", "context", or "off".
        device_id: Target device ID (optional).
    """
    params = f"?state={state}"
    if device_id:
        params += f"&device_id={device_id}"
    await spotify_put(f"/v1/me/player/repeat{params}")
    return {"message": f"Repeat mode set to '{state}'"}


@tool(description="Get a list of the user's available playback devices")
async def spotify_get_devices() -> dict[str, Any]:
    """Get information about the user's available playback devices."""
    return await spotify_get("/v1/me/player/devices")


@tool(description="Transfer playback to a different device")
async def spotify_transfer_playback(device_id: str, play: bool = False) -> dict[str, Any]:
    """Transfer playback to a new device.

    Args:
        device_id: The ID of the device to transfer playback to.
        play: If True, playback starts on the new device; if False,
              the current playback state is kept.
    """
    await spotify_put("/v1/me/player", body={"device_ids": [device_id], "play": play})
    return {"message": f"Playback transferred to device {device_id}"}


@tool(description="Add a track or episode to the playback queue")
async def spotify_add_to_queue(uri: str, device_id: str = "") -> dict[str, Any]:
    """Add an item to the end of the playback queue.

    Args:
        uri: Spotify URI of the track or episode to add.
             e.g. "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
        device_id: Target device ID (optional).
    """
    params = f"?uri={uri}"
    if device_id:
        params += f"&device_id={device_id}"
    await spotify_post(f"/v1/me/player/queue{params}")
    return {"message": f"Added {uri} to queue"}


@tool(description="Get the user's playback queue")
async def spotify_get_queue() -> dict[str, Any]:
    """Get the list of items in the user's current playback queue."""
    return await spotify_get("/v1/me/player/queue")


playback_tools = [
    spotify_get_playback_state,
    spotify_get_currently_playing,
    spotify_play,
    spotify_pause,
    spotify_skip_next,
    spotify_skip_previous,
    spotify_seek,
    spotify_set_volume,
    spotify_set_shuffle,
    spotify_set_repeat,
    spotify_get_devices,
    spotify_transfer_playback,
    spotify_add_to_queue,
    spotify_get_queue,
]
