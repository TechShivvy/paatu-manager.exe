from typing import TypedDict, Optional


class UserStore:
    def __init__(self):
        self.__users = {}
        print("UserStore Created")

    def add_user(self, id, auth_manager):
        self.__users[id] = {
            "auth_manager": auth_manager,
            "channels": {},
            # "playlist_ids": {},
            "flag": True,
        }
        print(f"added new user: {id}")

    def get_or_set_channel(self, user_id, channel_id, channel_name):
        # if channel_id not in self.__users[user_id]["channels"].keys():
        #     self.__users[user_id]["channels"][channel_id] = {
        #         "name": channel_name,
        #         "playlists": {"spotify": "", "youtube": ""},
        #         "flag": True,
        #     }
        #     return True
        # return False

        return self.__users[user_id]["channels"].setdefault(
            channel_id,
            {
                "name": channel_name,
                "playlists": {"spotify": "", "youtube": ""},
                "flag": True,
            },
        )

    def get_user(self, id):
        return self.__users.get(id, None)

    def get_auth_manager(self, id):
        return self.__users[id]["auth_manager"]

    def get_flag(self, user_id, channel_id=None, channel_name=None):
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

    def toggle_flag(self, user_id, channel_id=None, channel_name=None):
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

    def del_user(self, id):
        if id in self.__users:
            del self.__users[id]
            print(f"deleted user: {id}")
            return 1
        else:
            print(f"user not found: {id}")
            return 0

    def __del__(self):
        print("UserStore deleted")

    def get_active_listeners(self, channel_id, channel_name):
        active_listeners = []
        for user_id, user_data in self.__users.items():
            self.get_or_set_channel(user_id, channel_id, channel_name)
            if user_data.get("flag", True) == True:
                if user_data["channels"][channel_id].get("flag", True) == True:
                    active_listeners.append(user_id)
        return active_listeners

    def set_playlist_id(self, user_id, which, channel_id, playlist_id, channel_name):
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

    def get_channels_info(self, user_id):
        if user_id in self.__users:
            return self.__users[user_id]["channels"]
        else:
            return {}

    def get_playlist_ids(self, user_id):
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

    def get_playlist_id(self, user_id, channel_id, channel_name, which):
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
    def __init__(self, where=None):
        # self.__servers = {}
        self.__servers: dict[int, ServerDict] = {}
        print("ServerStore created", where)

    def add_server(self, server_id, server_name=None):
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

    def get_server(self, server_id) -> dict[str, UserStore]:
        # print(self.__servers)
        return self.__servers[server_id]

    def get_server_users(self, server_id) -> UserStore:
        return self.__servers[server_id]["users"]

    def get_flag(self, server_id):
        if server_id in self.__servers:
            return self.__servers[server_id]["flag"]
        else:
            return None

    def toggle_flag(self, server_id):
        if server_id in self.__servers:
            self.__servers[server_id]["flag"] = not self.__servers[server_id]["flag"]
            return True
        else:
            return False

    # def get_server(self, server_id) -> dict[str, UserStore]: #not correct typehint, but works so
    #     return self.__servers.get(server_id, None)

    # def get_channel_info(self, server_id, channel_id):
    #     if (
    #         server_id in self.__servers
    #         and channel_id in self.__servers[server_id]["channels"]
    #     ):
    #         return self.__servers[server_id]["channels"][channel_id]
    #     else:
    #         return None

    # def set_channel_flag(self, server_id, channel_id, flag):
    #     if (
    #         server_id in self.__servers
    #         and channel_id in self.__servers[server_id]["channels"]
    #     ):
    #         self.__servers[server_id]["channels"][channel_id]["flag"] = flag
    #         return True
    #     else:
    #         return None

    # def set_channel_playlist(self, server_id, channel_id, playlist_id, which):
    #     if which != "spotify" or which != "youtube":
    #         return False
    #     if (
    #         server_id in self.__servers
    #         and channel_id in self.__servers[server_id]["channels"]
    #     ):
    #         self.__servers[server_id]["channels"][channel_id]["playlist_id"][
    #             which
    #         ] = playlist_id
    #         return True
    #     else:
    #         return None

    def __del__(self):
        print("ServerStore deleted")


# serversdb = ServerStore()
