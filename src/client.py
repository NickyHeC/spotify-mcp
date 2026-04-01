"""Test Spotify connection using ConnectionTester.

Requires SPOTIFY_ACCESS_TOKEN in the environment (or .env file).

Usage:
    python -m src.client
"""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

logging.getLogger("httpx").setLevel(logging.WARNING)

from dedalus_mcp.testing import ConnectionTester, TestRequest

sys.path.insert(0, os.path.dirname(__file__))
from spotify.config import spotify


async def main() -> None:
    load_dotenv()

    print(f"Connection: {spotify.name}")
    print(f"Base URL:   {spotify.base_url}")

    try:
        tester = ConnectionTester.from_env(spotify)
    except ValueError as exc:
        print(f"\n  ERROR: {exc}")
        print("  Set SPOTIFY_ACCESS_TOKEN in .env or export it in your shell.")
        return

    print("\nSearching for 'Bohemian Rhapsody'...")
    resp = await tester.request(
        TestRequest(path="/v1/search", params={"q": "Bohemian Rhapsody", "type": "track", "limit": 3}),
    )
    print(f"  Status: {resp.status}")
    if not resp.success:
        print(f"\n  FAILED ({resp.status}). Check that SPOTIFY_ACCESS_TOKEN is valid.")
        return
    if resp.body:
        for i, track in enumerate(resp.body.get("tracks", {}).get("items", []), 1):
            artists = ", ".join(a["name"] for a in track.get("artists", []))
            print(f"  {i}. {track['name']} — {artists}")

    print("\nLooking up artist 'Radiohead'...")
    resp = await tester.request(
        TestRequest(path="/v1/search", params={"q": "Radiohead", "type": "artist", "limit": 1}),
    )
    print(f"  Status: {resp.status}")
    if resp.success and resp.body:
        artist = resp.body.get("artists", {}).get("items", [{}])[0]
        artist_id = artist.get("id", "")
        print(f"  Artist: {artist.get('name')}  (followers: {artist.get('followers', {}).get('total')})")

        if artist_id:
            print(f"\nFetching albums for {artist.get('name')}...")
            resp = await tester.request(
                TestRequest(path=f"/v1/artists/{artist_id}/albums", params={"limit": 5, "include_groups": "album"}),
            )
            print(f"  Status: {resp.status}")
            if resp.success and resp.body:
                for i, album in enumerate(resp.body.get("items", []), 1):
                    print(f"  {i}. {album['name']} ({album.get('release_date', '?')})")

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())
