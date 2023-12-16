import spotipy
from spotipy.oauth2 import SpotifyPKCE
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
scope="playlist-modify-private",
token = spotipy.util.prompt_for_user_token("hello",scope,SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,oauth_manager=spotipy.SpotifyOAuth(username="hello",cache_handler=spotipy.MemoryCacheHandler()))

if token:
    print("Access token obtained successfully!")
else:
    print("Can't get token for")

sp = spotipy.Spotify(auth=token)

playlists = sp.current_user_playlists()
for playlist in playlists['items']:
    print(playlist['name'])