import spotipy
from spotipy.oauth2 import SpotifyPKCE
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")


# Define your Spotify app credentials
client_id = SPOTIPY_CLIENT_ID
redirect_uri = SPOTIPY_REDIRECT_URI

# Create a SpotifyPKCE object with your credentials
sp_oauth = SpotifyPKCE(client_id, redirect_uri)

# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()

# Open the authorization URL in a web browser
# import webbrowser
# webbrowser.open(auth_url)

# After the user logs in and grants permissions, Spotify will redirect to the specified redirect_uri with a code

# Extract the code from the redirected URL (you might need to manually copy it)
# code = input("Paste the code from the redirect URL here: ")
code="AQDe6yTtIAr2xvcjefP7cTOfOKZtvdwMeYJQhciU-frd4uZ4LtcbNBNLckqp4VRkIaA6i5AxV0YBhjHp6k4zK3WNzESbScZyQK008GyDseZDWZYmJ8rYl0v8agX7hTGCWboy2ZzJS-SitO53Y4daLb1OHxg-_VzC7Neu_K47B4L1ThlN3BrvaEAq6eJzST09baxoJEeaGzBPkBgVG3k8ZCMDgXeKM_J8Kf8ELBK1Kil7uFKB"
# Get the access token using the code
token_info = sp_oauth.get_access_token(code)

# Use the access token to make API requests
if token_info:
    print(token_info)
    access_token = token_info
    sp = spotipy.Spotify(auth=access_token)

    # Now you can make API requests using the sp object
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        print(playlist['name'])
else:
    print("Failed to get access token.")
