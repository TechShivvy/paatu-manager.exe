import spotipy
from spotipy.oauth2 import SpotifyPKCE
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
scope="playlist-modify-private",

# Define your Spotify app credentials
client_id = SPOTIPY_CLIENT_ID
redirect_uri = SPOTIPY_REDIRECT_URI

# Create a SpotifyPKCE object with your credentials
sp_oauth = SpotifyPKCE(username="hello",client_id=client_id, scope=scope,redirect_uri=redirect_uri,cache_handler=spotipy.MemoryCacheHandler())

sp_oauth1 = SpotifyPKCE(username="hey",client_id=client_id, scope=scope,redirect_uri=redirect_uri,cache_handler=spotipy.MemoryCacheHandler(),open_browser=False)


print(type(sp_oauth))


# # # Get the authorization URL
# auth_url = sp_oauth.get_authorize_url()

# # # Open the authorization URL in a web browser
# import webbrowser
# webbrowser.open(auth_url)

# # # After the user logs in and grants permissions, Spotify will redirect to the specified redirect_uri with a code

# # # Extract the code from the redirected URL (you might need to manually copy it)
# code = input("Paste the code from the redirect URL here: ")
# # # Get the access token using the code
# token_info = sp_oauth.get_access_token(code)

# token = spotipy.util.prompt_for_user_token("hello",scope,SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI)

i=0
# Use the access token to make API requests
if True:
    # print(token_info)
    # access_token = token
    i+=1
    if i%2:
        sp = spotipy.Spotify(auth_manager=sp_oauth)
        print(sp_oauth.get_cached_token)
        print(sp.me()['id'])

        playlist_tracks = sp.playlist('1nXyBudZQhuBbITwQy')
        print(playlist_tracks)

    # else:
    #     sp= spotipy.Spotify(auth_manager=sp_oauth1)
    #     playlists = sp.current_user_playlists()
    #     for playlist in playlists['items']:
    #         print(playlist['name'])


    # Now you can make API requests using the sp object
    
else:
    print("Failed to get access token.")
