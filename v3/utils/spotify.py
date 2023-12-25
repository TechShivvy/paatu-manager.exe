import spotipy
import os
from spotipy.oauth2 import SpotifyPKCE
from db import ServerStore
from utils.crypt import *


def create_auth_manager():
    return SpotifyPKCE(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        # scope="playlist-modify-private,playlist-read-private,playlist-modify-public,user-library-modify,user-library-read",
        scope="playlist-modify-private,playlist-read-private",
        cache_handler=spotipy.MemoryCacheHandler(),
        open_browser=False,
    )


async def add_track_to_playlists(
    serversdb: ServerStore,
    server_id,
    channel_id,
    server_name,
    channel_name,
    track_id,
    which,
):
    try:
        if not serversdb.get_flag(server_id):
            print("no flag")
            return False

        has_run_once = False
        for listener in serversdb.get_server_users(server_id).get_active_listeners(
            channel_id, channel_name
        ):
            print(listener)
            playlist_id = serversdb.get_server_users(server_id).get_playlist_id(
                listener, channel_id, channel_name, which
            )
            print(playlist_id)
            sp = spotipy.Spotify(
                auth_manager=decrypt_data(
                    serversdb.get_server_users(server_id).get_auth_manager(listener)
                )
            )
            if playlist_id == "":
                print("create1")
                playlist = sp.user_playlist_create(
                    sp.current_user()["id"],
                    f"{server_name}/{channel_name}",
                    False,
                    False,
                    description=f"List of tracks shared in {{{server_id} >>> {channel_id}}} - pme",
                )
                print(playlist)
                playlist_id = playlist["id"]
                del playlist
            else:
                try:
                    print("try")
                    if playlist_id != "":
                        print(sp.playlist(playlist_id))
                except spotipy.exceptions.SpotifyException as e:
                    print("create2")
                    playlist = sp.user_playlist_create(
                        sp.current_user()["id"],
                        f"{server_name}/{channel_name}",
                        False,
                        False,
                        description=f"List of tracks shared in {{{server_id} >>> {channel_id}}} - pme",
                    )
                    playlist_id = playlist["id"]
                    serversdb.get_server_users(server_id).set_playlist_id(
                        listener, which, channel_id, playlist_id, channel_name
                    )
                    del playlist

            playlist_tracks = sp.playlist_tracks(playlist_id)
            existing_track_ids = [
                item["track"]["id"] for item in playlist_tracks["items"]
            ]
            print(playlist_tracks)
            print(existing_track_ids)

            if track_id in existing_track_ids:
                pass
            else:
                sp.playlist_add_items(playlist_id, [track_id])
                serversdb.get_server_users(server_id).set_playlist_id(
                    listener, which, channel_id, playlist_id, channel_name
                )
                has_run_once = True

            del sp
            del playlist_id
            del playlist_tracks
            del existing_track_ids

        return has_run_once

    except Exception as e:
        print(f"Error {e} while adding tracks to playlists")

    finally:
        print("finally in adding tracks")
