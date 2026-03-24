# Spotify MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server for
the [Spotify Web API](https://developer.spotify.com/documentation/web-api),
built with the [Dedalus MCP](https://docs.dedaluslabs.ai/dmcp/) framework.

## Features

**37 tools** covering the full Spotify Web API surface:

| Category | Tools | Scopes |
|----------|-------|--------|
| **Playback** | get playback state, currently playing, play, pause, skip next/previous, seek, volume, shuffle, repeat, devices, transfer playback, add to queue, get queue | `user-read-playback-state` `user-modify-playback-state` `user-read-currently-playing` |
| **Playlists** | get playlist, get playlist items, list my playlists, create playlist, add/remove items, update playlist | `playlist-read-private` `playlist-read-collaborative` `playlist-modify-public` `playlist-modify-private` |
| **Search** | search across tracks, artists, albums, playlists, shows, episodes | — |
| **Library** | get/save/remove saved tracks, check saved tracks, get/save/remove saved albums | `user-library-read` `user-library-modify` |
| **Tracks & Artists** | get track, get tracks, get album, album tracks, get artist, artist top tracks, related artists, recommendations | — |
| **Users** | current user profile, user profile by ID, top artists/tracks, recently played | `user-read-private` `user-read-email` `user-top-read` `user-read-recently-played` |

## Architecture

```
src/
├── main.py              # CLI entry point
├── server.py            # MCPServer factory + tool collection
├── client.py            # Test client
├── spotify/
│   ├── config.py        # DAuth Connection (SPOTIFY_ACCESS_TOKEN)
│   └── request.py       # REST helpers via ctx.dispatch
└── tools/
    ├── __init__.py      # Tool registry (spotify_tools)
    ├── playback.py      # Playback control
    ├── playlists.py     # Playlist CRUD
    ├── search.py        # Catalog search
    ├── library.py       # User library
    ├── tracks.py        # Track/album/artist info
    └── users.py         # User profiles & personalization
```

## Authentication

This server uses **DAuth** (Dedalus Auth) to manage Spotify OAuth tokens.
The `SPOTIFY_ACCESS_TOKEN` secret is injected by the Dedalus platform at
runtime — your code never sees raw credentials.

The Spotify app should be configured for the
[Authorization Code flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow)
with the following scopes:

```
user-read-playback-state
user-modify-playback-state
user-read-currently-playing
app-remote-control
streaming
playlist-read-private
playlist-read-collaborative
playlist-modify-private
playlist-modify-public
user-read-playback-position
user-top-read
user-read-recently-played
user-library-modify
user-library-read
user-read-email
user-read-private
```

## Setup

### Prerequisites

- Python 3.10+
- A Spotify Developer account with a registered app
- Spotify Premium (required for playback control)

### Install

```bash
pip install -e .
```

Or with individual dependencies:

```bash
pip install -r requirements.txt
```

### Configure

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

### Run

```bash
python -m src.main
```

The server starts on `http://0.0.0.0:8080` with the MCP endpoint at `/mcp`.

### Test

With the server running, verify it responds:

```bash
python -m src.client
```

## API Reference

All tools follow the Spotify Web API conventions:

- Base URL: `https://api.spotify.com`
- Uses `/playlists/{id}/items` (not deprecated `/tracks`)
- Uses `/me/tracks` and `/me/albums` for library (not deprecated type-specific endpoints)
- Handles HTTP 429 rate limits via the Dedalus framework

See the [Spotify Web API Reference](https://developer.spotify.com/documentation/web-api/reference)
for full endpoint documentation.

## License

MIT
