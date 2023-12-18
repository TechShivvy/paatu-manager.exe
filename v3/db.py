class ServerStore:
    def __init__(self):
        self.__servers = {}
        print("ServerStore created")

    def add_server(self, server_id, server_name):
        if server_id not in self.__servers:
            self.__servers[server_id] = {
                "name": server_name,
                "channels": {},
                "users": UserStore(),
            }
            print(f"Added new server: {server_name} ({server_id})")
        else:
            print(f"Server {server_name} ({server_id}) already exists")

    def add_channel(self, server_id, channel_id, channel_name, playlist_id=None):
        if server_id in self.__servers:
            self.__servers[server_id]["channels"][channel_id] = {
                "channel_name": channel_name,
                "playlist_id": playlist_id,
                "flag": True,
            }
            print(f"Added channel {channel_id} in {server_id}")
            return 1
        else:
            print(f"Server {server_id} not found")
            return 0

    def get_server(self, server_id):
        return self.__servers.get(server_id, None)

    def get_channel_info(self, server_id, channel_id):
        if (
            server_id in self.__servers
            and channel_id in self.__servers[server_id]["channels"]
        ):
            return self.__servers[server_id]["channels"][channel_id]
        else:
            return None

    def set_channel_flag(self, server_id, channel_id, flag):
        if (
            server_id in self.__servers
            and channel_id in self.__servers[server_id]["channels"]
        ):
            self.__servers[server_id]["channels"][channel_id]["flag"] = flag
            return True
        else:
            return None

    def set_channel_playlist(self, server_id, channel_id, playlist_id):
        if (
            server_id in self.__servers
            and channel_id in self.__servers[server_id]["channels"]
        ):
            self.__servers[server_id]["channels"][channel_id][
                "playlist_id"
            ] = playlist_id
            return True
        else:
            return None

    def __del__(self):
        print("ServerStore deleted")


class UserStore:
    def __init__(self):
        self.__users = {}
        print("UserStore Created")

    def add_user(self, id, auth_manager):
        self.__users[id] = {
            "auth_manager": auth_manager,
            "playlist_ids": {},
            "flag": True,
        }
        print(f"added new user: {id}")

    def get_user(self, id):
        return self.__users.get(id, None)

    def get_active_listeners(self):
        active_listeners = []
        for user_id, user_data in self.__users.items():
            if user_data.get("flag", 1) == 1:
                active_listeners.append(user_id)
        return active_listeners

    def get_auth_manager(self, id):
        return self.__users[id]["auth_manager"]

    def set_playlist_id(self, user_id, playlist_key, playlist_id):
        if user_id in self.__users:
            self.__users[user_id]["playlist_ids"][playlist_key] = playlist_id
            return True
        else:
            return False

    def get_playlist_ids(self, user_id):
        if user_id in self.__users:
            return self.__users[user_id]["playlist_ids"]
        else:
            return {}

    def get_playlist_id(self, user_id, playlist_key):
        if user_id in self.__users:
            return self.__users[user_id]["playlist_ids"].get(playlist_key, False)
        else:
            return None

    def get_flag(self, user_id):
        if user_id in self.__users:
            return self.__users[user_id]["flag"]
        else:
            return None

    def toggle_flag(self, user_id):
        if user_id in self.__users:
            self.__users[user_id]["flag"] = not self.__users[user_id]["flag"]
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
