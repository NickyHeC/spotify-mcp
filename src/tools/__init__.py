"""Tool registry for spotify-mcp.

Modules:
  playback  -- get_playback_state, get_currently_playing, play, pause,
               skip_next, skip_previous, seek, set_volume, set_shuffle,
               set_repeat, get_devices, transfer_playback, add_to_queue
  playlists -- get_playlist, list_my_playlists, create_playlist,
               add_to_playlist, remove_from_playlist, update_playlist
  search    -- search_spotify
  library   -- get_saved_tracks, save_tracks, remove_saved_tracks,
               get_saved_albums, save_albums, remove_saved_albums,
               check_saved_tracks
  tracks    -- get_track, get_album, get_artist, get_artist_top_tracks
  users     -- get_current_user, get_top_items, get_recently_played
"""

from __future__ import annotations

from tools.library import library_tools
from tools.playback import playback_tools
from tools.playlists import playlist_tools
from tools.search import search_tools
from tools.tracks import track_tools
from tools.users import user_tools

spotify_tools = [
    *playback_tools,
    *playlist_tools,
    *search_tools,
    *library_tools,
    *track_tools,
    *user_tools,
]
