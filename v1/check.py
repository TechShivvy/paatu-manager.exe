import spotipy
from spotipy.oauth2 import SpotifyPKCE
import os
from dotenv import load_dotenv
import pickle

load_dotenv()


from cryptography.fernet import Fernet
def encrypt_data(data):
    return cipher_suite.encrypt(pickle.dumps(data))
    
def decrypt_data(data):
    return pickle.loads(cipher_suite.decrypt(data))


SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
KEY = os.getenv("KEY")
scope="playlist-modify-private",
cipher_suite = Fernet(KEY.encode())
# Define your Spotify app credentials
client_id = SPOTIPY_CLIENT_ID
redirect_uri = SPOTIPY_REDIRECT_URI

# Create a SpotifyPKCE object with your credentials
sp_oauth = SpotifyPKCE(username="hello",client_id=client_id, scope=scope,redirect_uri=redirect_uri,cache_handler=spotipy.MemoryCacheHandler(),open_browser=False)

sp = spotipy.Spotify(auth_manager=decrypt_data(encrypt_data(sp_oauth)))

print(sp_oauth.get_cached_token)
print(sp.me()['id'])
