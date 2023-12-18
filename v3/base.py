import os
from dotenv import load_dotenv

from cryptography.fernet import Fernet

import re

import atexit
import signal
import sys

import asyncio
import discord
from discord.ext import commands

import spotipy
from spotipy.oauth2 import SpotifyPKCE

import pickle

import random

from cryptography.fernet import Fernet

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
DISCORD_BOT_ID = os.getenv("DISCORD_BOT_ID")
CREATOR_ID = os.getenv("CREATOR_ID")

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

cipher_suite = Fernet(Fernet.generate_key())


# have to implement
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


serversdb = ServerStore()


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


@atexit.register
def goodbye():
    print("GoodBye.")
    # sys.exit(0)


def exit_handler(signum, frame):
    print(f"Received signal {signum}. Exiting gracefully.")
    sys.exit(0)


def create_auth_manager():
    return SpotifyPKCE(
        client_id=SPOTIPY_CLIENT_ID,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-private playlist-read-private",
        cache_handler=spotipy.MemoryCacheHandler(),
        open_browser=False,
    )


def encrypt_data(data):
    return cipher_suite.encrypt(pickle.dumps(data))


def decrypt_data(data):
    return pickle.loads(cipher_suite.decrypt(data))


class CustomHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Available Commands:", color=0x3498DB)

        embed.add_field(
            name="About:",
            value="Yo, I'm your paatu-manager 🎶! I only vibe with Spotify song links for now (not playlists or tracks; my boss is thinking of adding YouTube too). Drop those links, and I'll add them to playlists. Let's make this server bumpin'!",
            inline=False,
        )

        for command in bot.commands:
            if not command.name.startswith("!"):
                embed.add_field(
                    name=f"`{bot.command_prefix}{command.name}`",
                    value=command.brief or "Shows this Message",
                    inline=True,
                )

        embed.add_field(
            name="Fun Fact:",
            value="Oh, and let me spill some tea - chief is still deciding if YouTube tracks are cool enough. Imagine, right?",
            inline=False,
        )

        embed.add_field(
            name="IMPORTANT NOTE:",
            value="This bot's in development. Limited to 25 spotify users on the dashboard. Only they can access. Wanna join? DM my boss your Spotify email.",
            inline=False,
        )

        channel = self.get_destination()
        await channel.send(embed=embed)

    @bot.event
    async def on_ready():
        guild_count = 0

        for guild in bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")
            serversdb.add_server(guild.id, guild.name)
            guild_count += 1

        print("paatu-manager.exe is in " + str(guild_count) + " guilds.")
        print("------")
        print(f"Logged in as {bot.user.name} ({bot.user.id})")
        print("------")

    @bot.event
    async def on_guild_join(guild):
        print("++++++")
        print("Bot has been added to a new server")
        print("List of servers the bot is in: ")

        serversdb.add_server(guild.id, guild.name)

        for guild in bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")

        print(f"paatu-manager.exe is in {len(bot.guilds)} guilds.")
        print("++++++")

    @bot.event
    async def ping(ctx):
        await ctx.message.reply("Pong!", delete_after=120)

def main():
    global serversdb, bot
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    try:
        bot.help_command = CustomHelpCommand()
        bot.serversdb = serversdb
        bot.run(DISCORD_BOT_ID)

    except Exception as e:
        print(f"Exception: {e}")

    finally:
        # if "users" in locals():
        #     del users
        if "serversdb" in locals():
            del serversdb
        if "bot" in locals():
            del bot
        print("finally DBs deleted!")


if __name__ == "__main__":
    main()
