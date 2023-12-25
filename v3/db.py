from typing import TypedDict, Optional, List, Dict, Any


class UsersDict(TypedDict):
    name: str
    channels: Dict[str, any]
    flag: bool


class UserStore:
    def __init__(self) -> None:
        # self.__users = {}
        self.__users: dict[id, UsersDict] = {}
        print("UserStore Created")

    def add_user(self, id, auth_manager) -> None:
        self.__users[id] = {
            "auth_manager": auth_manager,
            "channels": {},
            # "playlist_ids": {},
            "flag": True,
        }
        print(f"added new user: {id}")

    def get_or_set_channel(self, user_id, channel_id, channel_name) -> UsersDict:
        return self.__users[user_id]["channels"].setdefault(
            channel_id,
            {
                "name": channel_name,
                "playlists": {"spotify": "", "youtube": ""},
                "flag": True,
            },
        )

    def get_user(self, id) -> int:
        return self.__users.get(id, None)

    def get_auth_manager(self, id):
        return self.__users[id]["auth_manager"]

    def get_flag(self, user_id, channel_id=None, channel_name=None) -> bool | None:
        if user_id in self.__users:
            if channel_id is None:
                return self.__users[user_id]["flag"]
            else:
                return self.get_or_set_channel(user_id, channel_id, channel_name)[
                    "flag"
                ]
                # return self.__users[user_id]["channels"][channel_id]["flag"]
        else:
            return None

    def toggle_flag(self, user_id, channel_id=None, channel_name=None) -> bool:
        if user_id in self.__users:
            if channel_id == None:
                self.__users[user_id]["flag"] = not self.__users[user_id]["flag"]
            else:
                self.get_or_set_channel(user_id, channel_id, channel_name)
                self.__users[user_id]["channels"][channel_id][
                    "flag"
                ] = not self.__users[user_id]["channels"][channel_id]["flag"]
            return True
        else:
            return False

    def del_user(self, id) -> int:
        if id in self.__users:
            del self.__users[id]
            print(f"deleted user: {id}")
            return 1
        else:
            print(f"user not found: {id}")
            return 0

    def __del__(self) -> None:
        print("UserStore deleted")

    def get_active_listeners(self, channel_id, channel_name) -> List[int]:
        active_listeners = []
        for user_id, user_data in self.__users.items():
            self.get_or_set_channel(user_id, channel_id, channel_name)
            if user_data.get("flag", True) == True:
                if user_data["channels"][channel_id].get("flag", True) == True:
                    active_listeners.append(user_id)
        return active_listeners

    def set_playlist_id(
        self, user_id, which, channel_id, playlist_id, channel_name
    ) -> bool:
        if which != "spotify" and which != "youtube":
            return False
        if user_id in self.__users:
            self.get_or_set_channel(user_id, channel_id, channel_name)
            self.__users[user_id]["channels"][channel_id]["playlists"][
                which
            ] = playlist_id
            return True
        else:
            return False

    def get_channels_info(self, user_id) -> Dict[str, Any]:
        if user_id in self.__users:
            return self.__users[user_id]["channels"]
        else:
            return {}

    def get_playlist_ids(self, user_id) -> Dict[str, Dict[str, int]] | None:
        if user_id in self.__users:
            all_channels = self.__users[user_id]["channels"]

            playlist_data = {}

            for channel_id, channel_data in all_channels.items():
                if "playlists" in channel_data:
                    spotify_playlist_id = channel_data["playlists"]["spotify"]
                    youtube_playlist_id = channel_data["playlists"]["youtube"]

                    playlist_data[channel_data["name"]] = {
                        "spotify": spotify_playlist_id,
                        "youtube": youtube_playlist_id,
                    }

            return playlist_data
        else:
            return None

    def get_playlist_id(self, user_id, channel_id, channel_name, which) -> int | None:
        if which != "spotify" and which != "youtube":
            return False
        if user_id in self.__users:
            self.get_or_set_channel(user_id, channel_id, channel_name)
            return self.__users[user_id]["channels"][channel_id]["playlists"].get(
                which, ""
            )
        else:
            return None


class ServerDict(TypedDict):
    name: str
    flag: bool
    users: UserStore


class ServerStore:
    def __init__(self, where=None) -> int:
        # self.__servers = {}
        self.__servers: Dict[int, ServerDict] = {}
        print("ServerStore created", where)

    def add_server(self, server_id, server_name=None) -> None:
        if server_id not in self.__servers:
            self.__servers[server_id] = {
                "name": server_name,
                # "channels": {},
                "flag": True,
                "users": UserStore(),
            }
            print(f"Added new server: {server_name} ({server_id})")
        else:
            print(f"Server {server_name} ({server_id}) already exists")

    def get_server(self, server_id) -> Dict[str, UserStore]:
        # print(self.__servers)
        return self.__servers[server_id]

    def get_server_users(self, server_id) -> UserStore:
        return self.__servers[server_id]["users"]

    def get_flag(self, server_id) -> bool | None:
        if server_id in self.__servers:
            return self.__servers[server_id]["flag"]
        else:
            return None

    def toggle_flag(self, server_id) -> bool:
        if server_id in self.__servers:
            self.__servers[server_id]["flag"] = not self.__servers[server_id]["flag"]
            return True
        else:
            return False

    def __del__(self):
        print("ServerStore deleted")
