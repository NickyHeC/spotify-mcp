"""Spotify REST API client utilities.

Provides HTTP access to the Spotify Web API using Dedalus dispatch.
All requests go through the Dedalus enclave so credentials are never
exposed to user code.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from dedalus_mcp import HttpMethod, HttpRequest, get_context

from spotify.config import spotify


async def spotify_api_request(
    method: str,
    endpoint: str,
    body: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> dict[str, Any] | list[Any]:
    """Make a request to the Spotify Web API using Dedalus dispatch.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, PATCH).
        endpoint: API path relative to https://api.spotify.com
                  (e.g. ``/v1/me/player``).
        body: Optional JSON body for POST/PUT/PATCH requests.
        params: Optional query parameters.

    Returns:
        Parsed JSON response body (dict or list).

    Raises:
        ValueError: When the API returns an error.
    """
    ctx = get_context()

    path = endpoint
    if params:
        filtered = {k: v for k, v in params.items() if v is not None}
        if filtered:
            path = f"{endpoint}?{urlencode(filtered)}"

    resp = await ctx.dispatch(
        "spotify-mcp",
        HttpRequest(
            method=HttpMethod(method),
            path=path,
            body=body,
        ),
    )

    if resp.success:
        if resp.response is None or resp.response.body is None:
            return {}
        return resp.response.body

    error_msg = "Spotify request failed"
    if resp.error:
        error_msg = resp.error.message
    raise ValueError(error_msg)


async def spotify_get(endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
    """Convenience wrapper for GET requests."""
    return await spotify_api_request("GET", endpoint, params=params)


async def spotify_post(endpoint: str, body: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
    """Convenience wrapper for POST requests."""
    return await spotify_api_request("POST", endpoint, body=body)


async def spotify_put(endpoint: str, body: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
    """Convenience wrapper for PUT requests."""
    return await spotify_api_request("PUT", endpoint, body=body)


async def spotify_delete(endpoint: str, body: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
    """Convenience wrapper for DELETE requests."""
    return await spotify_api_request("DELETE", endpoint, body=body)
