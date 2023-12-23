import spotipy
import os
from spotipy.oauth2 import SpotifyPKCE


def create_auth_manager():
    return SpotifyPKCE(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-private playlist-read-private",
        cache_handler=spotipy.MemoryCacheHandler(),
        open_browser=False,
    )
