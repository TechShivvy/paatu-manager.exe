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

GLOBAL_COUNT = 0

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
DISCORD_BOT_ID = os.getenv("DISCORD_BOT_ID")
CREATOR_ID = os.getenv("CREATOR_ID")


# KEY = os.getenv("KEY")

SPECIFIED_CHANNELS = [850273140268728342]

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

cipher_suite = Fernet(Fernet.generate_key())

# have to implement
# class ServerStore:
#     def __init__(self):
#         self.servers = {}
#         print("ServerStore created")

#     def add_server(self, server_id, server_name):
#         if server_id not in self.servers:
#             self.servers[server_id] = {"name": server_name, "channels": {}}
#             print(f"Added new server: {server_name} ({server_id})")
#         else:
#             print(f"Server {server_name} ({server_id}) already exists")

#     def add_channel_to_server(
#         self, server_id, channel_id, channel_name, playlist_id=None
#     ):
#         if server_id in self.servers:
#             self.servers[server_id]["channels"][channel_id] = {
#                 "channel_name": channel_name,
#                 "playlist_id": playlist_id,
#                 "flag": True,
#             }
#             print(f"Added channel {channel_id} in {server_id}")
#             return 1
#         else:
#             print(f"Server {server_id} not found")
#             return 0

#     def get_server(self, server_id):
#         return self.servers.get(server_id, None)

#     def get_channel_info(self, server_id, channel_id):
#         if (
#             server_id in self.servers
#             and channel_id in self.servers[server_id]["channels"]
#         ):
#             return self.servers[server_id]["channels"][channel_id]
#         else:
#             return None

#     def set_channel_flag(self, server_id, channel_id, flag):
#         if (
#             server_id in self.servers
#             and channel_id in self.servers[server_id]["channels"]
#         ):
#             self.servers[server_id]["channels"][channel_id]["flag"] = flag
#             return True
#         else:
#             return

#     def set_channel_playlist(self, server_id, channel_id, playlist_id):
#         if (
#             server_id in self.servers
#             and channel_id in self.servers[server_id]["channels"]
#         ):
#             self.servers[server_id]["channels"][channel_id]["playlist_id"] = playlist_id
#             return True
#         else:
#             return False

#     def __del__(self):
#         print("ServerStore deleted")


# serversdb = ServerStore()


class UserStore:
    def __init__(self):
        self.users = {}
        print("user constructor: class object created")

    def add_user(self, id, auth_manager):
        self.users[id] = {
            "auth_manager": auth_manager,
            "playlist_ids": {},
            "flag": True,
        }
        print(f"added new user: {id}")

    def get_user(self, id):
        return self.users.get(id, None)

    def get_active_listeners(self):
        active_listeners = []
        for user_id, user_data in self.users.items():
            if user_data.get("flag", 1) == 1:
                active_listeners.append(user_id)
        return active_listeners

    def get_auth_manager(self, id):
        return self.users[id]["auth_manager"]

    def set_playlist_id(self, user_id, playlist_key, playlist_id):
        if user_id in self.users:
            self.users[user_id]["playlist_ids"][playlist_key] = playlist_id
            return True
        else:
            return False

    def get_playlist_ids(self, user_id):
        if user_id in self.users:
            return self.users[user_id]["playlist_ids"]
        else:
            return {}

    def get_playlist_id(self, user_id, playlist_key):
        if user_id in self.users:
            return self.users[user_id]["playlist_ids"].get(playlist_key, False)
        else:
            return None

    def get_flag(self, user_id):
        if user_id in self.users:
            return self.users[user_id]["flag"]
        else:
            return None

    def toggle_flag(self, user_id):
        if user_id in self.users:
            self.users[user_id]["flag"] = not self.users[user_id]["flag"]
            return True
        else:
            return False

    def del_user(self, id):
        if id in self.users:
            del self.users[id]
            print(f"deleted user: {id}")
            return 1
        else:
            print(f"user not found: {id}")
            return 0

    def __del__(self):
        print("user destructor: class object deleted")


usersdb = UserStore()


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


async def add_track_to_playlists(server_name, channel_name, track_id):
    has_run_once = False
    # print(server_name,channel_name,track_id)
    for listener in usersdb.get_active_listeners():
        # print(listener)
        playlist_name = f"{server_name}/{channel_name}"
        playlist_id = usersdb.get_playlist_id(listener, playlist_name)
        # print(playlist_id)
        sp = spotipy.Spotify(
            auth_manager=decrypt_data(usersdb.get_auth_manager(listener))
        )
        if playlist_id == False:
            # print("not there in db")
            for offset in range(0, 100001, 50):
                # print(1)
                playlists = sp.current_user_playlists(limit=50, offset=offset)
                if len(playlists["items"]) == 0 or playlist_id is not False:
                    break
                for playlist in playlists["items"]:
                    # print(playlist["name"])
                    # print("for2")
                    if playlist["name"] == playlist_name:
                        playlist_id = playlist["id"]
                        break

            if playlist_id is False:
                # print("create1")
                playlist = sp.user_playlist_create(
                    sp.current_user()["id"],
                    playlist_name,
                    False,
                    False,
                    description=f"List of tracks shared in {channel_name} channel of {server_name} server",
                )
                # print(playlist)
                playlist_id = playlist["id"]
                del playlist
        else:
            try:
                # print("try")
                print(sp.playlist(playlist_id))
            except spotipy.exceptions.SpotifyException as e:
                # print("create2")
                # Playlist does not exist, create a new one
                # print(f"Playlist with ID {playlist_id} does not exist. Creating a new one.")
                playlist = sp.user_playlist_create(
                    sp.current_user()["id"],
                    playlist_name,
                    False,
                    False,
                    description=f"List of tracks shared in {channel_name} channel of {server_name} server",
                )
                playlist_id = playlist["id"]
                usersdb.set_playlist_id(listener, playlist_name, playlist_id)
                del playlist

        # existing_track_ids = []
        # playlist_tracks = sp.playlist_tracks(playlist_id)
        # if len(playlist_tracks["items"]):
        #     existing_track_ids = [
        #         item["track"]["id"] for item in playlist_tracks["items"]
        #     ]
        # else:
        #     playlist = sp.user_playlist_create(
        #         sp.current_user()["id"],
        #         playlist_name,
        #         False,
        #         False,
        #         description=f"List of tracks shared in {channel_name} channel of {server_name} server",
        #     )
        #     del playlist

        # print("here")
        playlist_tracks = sp.playlist_tracks(playlist_id)
        # print(playlist_tracks)
        existing_track_ids = [item["track"]["id"] for item in playlist_tracks["items"]]
        # print(playlist_tracks)
        # print(existing_track_ids)

        if track_id in existing_track_ids:
            # print(f"Track with ID {track_id} is already in the playlist.")
            pass
        else:
            sp.playlist_add_items(playlist_id, [track_id])
            usersdb.set_playlist_id(listener, playlist_name, playlist_id)
            # print(usersdb.users[listener])
        del sp
        del playlist_id
        del playlist_name
        del playlist_tracks
        del existing_track_ids

        has_run_once = True
        # print(usersdb.users)
    return has_run_once


@bot.event
async def on_ready():
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        # serversdb.add_server(guild.id, guild.name)
        guild_count += 1

    print("paatu-manager.exe is in " + str(guild_count) + " guilds.")
    print("------")
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send(
#             f"Sorry, the command `{ctx.message.content}` is not recognized. Please use `!help` to see available commands.",
#             delete_after=120,
#         )
#     else:
#         print(f"An error occurred: {type(error).__name__}, {error}")


@bot.event
async def on_message(message):
    global GLOBAL_COUNT

    if message.author == bot.user:
        if message.content == "!spotify_login":
            ctx = await bot.get_context(message)
            command = bot.get_command("spotify_login")
            await command(ctx)
        elif message.content == "!toggle_listen":
            ctx = await bot.get_context(message)
            command = bot.get_command("toggle_listen")
            await command(ctx)
        elif message.content == "!status":
            ctx = await bot.get_context(message)
            command = bot.get_command("status")
            await command(ctx)
        # elif message.content == "!playlists":
        #     ctx = await bot.get_context(message)
        #     command = bot.get_command("playlists")
        #     await command(ctx)
        elif message.content == "!spotify_logout":
            ctx = await bot.get_context(message)
            command = bot.get_command("spotify_logout")
            await command(ctx)
        return

    if isinstance(message.channel, discord.DMChannel):
        return

    # have to implement -> no need to do lol
    # if message.channel.id not in SPECIFIED_CHANNELS:
    #     return

    # if GLOBAL_COUNT == 0:
    #     return

    if "!https://open.spotify.com/track/" in message.content:
        return

    words = message.content.split()

    # for word in words:
    #     if "!https://open.spotify.com/track/" in word:
    #         return

    spotify_track_regex = re.compile(r"https://open\.spotify\.com/track/([a-zA-Z0-9]+)")

    for word in words:
        match = spotify_track_regex.search(word)
        if match:
            track_id = match.group(1)
            result = await add_track_to_playlists(
                message.guild.name, message.channel.name, track_id
            )
            if result:
                await message.reply(
                    f"track added to playlists!",
                    mention_author=False,
                    delete_after=120,
                )

    del words

    await bot.process_commands(message)


# @bot.command(name="ping", brief="To check Bot's Status")
# async def ping(ctx):
#     await ctx.message.reply("Pong!", delete_after=120)


@bot.command(name="status", brief="Shows listening status")
async def status(ctx):
    flag = usersdb.get_flag(ctx.author.id)
    if flag is not None:
        await ctx.message.reply(
            "listening ^.^" if flag else "not listening :(", delete_after=120
        )
    else:
        await ctx.message.reply(
            random.choice(
                [
                    f"Bruh, you gotta log in with `{bot.command_prefix}spotify_login` first.",
                    f"Yo, hit up `{bot.command_prefix}spotify_login` before using this command.",
                    f"Bro, log in using `{bot.command_prefix}spotify_login` real quick.",
                    f"Fam, make sure to `{bot.command_prefix}spotify_login` before using this command.",
                    f"You need to log in with `{bot.command_prefix}spotify_login` before using this command.",
                ]
            ),
            delete_after=120,
        )


@bot.command(name="toggle", brief="Toggles Listening status")
async def toggle(ctx):
    global GLOBAL_COUNT
    flag = usersdb.get_flag(ctx.author.id)
    if flag is not None:
        GLOBAL_COUNT += -1 if flag else 1
        usersdb.toggle_flag(ctx.author.id)
        await ctx.message.reply(
            f"Listening flag toggled. Now **{'listening' if not flag else 'not listening'}**.",
            delete_after=120,
        )
    else:
        await ctx.message.reply(
            random.choice(
                [
                    f"Bruh, you gotta log in with `{bot.command_prefix}spotify_login` first.",
                    f"Yo, hit up `{bot.command_prefix}spotify_login` before using this command.",
                    f"Bro, log in using `{bot.command_prefix}spotify_login` real quick.",
                    f"Fam, make sure to `{bot.command_prefix}spotify_login` before using this command.",
                    f"You need to log in with `{bot.command_prefix}spotify_login` before using this command.",
                ]
            ),
            delete_after=120,
        )


# @bot.command(name="add_channel", brief="to listen to this channel")
# async def add_channel(ctx):
#     info = serversdb.get_channel_info(ctx.guild.id, ctx.channel.id)
#     if not info:
#         serversdb.add_channel_to_server(ctx.guild.id, ctx.channel.id, ctx.channel.name)
#         await ctx.message.reply("Channel added!", delete_after=120)
#     else:
#         await ctx.message.reply("Channel already added", delete_after=120)


@bot.command(name="init", brief="init bot account")
# @commands.is_owner()
async def init(ctx):
    if ctx.author.id == int(CREATOR_ID):
        await ctx.send("!spotify_login")

        def check(message):
            # print(message)
            return (
                message.author.id == bot.user.id
                and message.channel.id == ctx.channel.id
                and message.content == "IM INNNNN BISSHHESS!"
            )

        try:
            message = await bot.wait_for("message", check=check, timeout=60)
            # await ctx.send('Received response: ' + response.content)

            # Continue with the rest of your code using the received response
            sp = spotipy.Spotify(
                auth_manager=decrypt_data(usersdb.get_auth_manager(bot.user.id))
            )
            for offset in range(0, 100001, 50):
                playlists = sp.current_user_playlists(limit=50, offset=offset)
                for playlist in playlists["items"]:
                    # if f"{message.guild.name}/" in playlist["name"]:
                    usersdb.set_playlist_id(
                        bot.user.id, playlist["name"], playlist["id"]
                    )
                if len(playlists["items"]) == 0:
                    break

        except asyncio.TimeoutError:
            print("Timeout reached. No response to !spotify_login.")


@bot.command(name="!toggle", brief="Toggle listen for bot")
# @commands.is_owner()
async def togglee(ctx):
    if ctx.author.id == int(CREATOR_ID):
        await ctx.send("!toggle_listen")


@bot.command(name="!status", brief="status for bot")
# @commands.is_owner()
async def statuss(ctx):
    if ctx.author.id == int(CREATOR_ID):
        await ctx.send("!status")


@bot.command(name="!spotify_logout", brief="spotify logout 4 bot")
# @commands.is_owner()
async def spotify_logoutt(ctx):
    if ctx.author.id == int(CREATOR_ID):
        await ctx.send("!spotify_logout")


# async def fetch_


@bot.command(name="!playlists", brief="List this bot's playlists")
async def playylists(ctx):
    embed = discord.Embed(title="Bot's Playlists", color=0x1DB954)
    if not usersdb.get_user(bot.user.id):
        await ctx.message.reply("Bot is not logged in yet :(", delete_after=120)
        return
    for playlist_name, playlist_id in usersdb.get_playlist_ids(bot.user.id).items():
        embed.add_field(
            name=playlist_name,
            value=f"[Open Playlist](https://open.spotify.com/playlist/{playlist_id})",
            inline=False,
        )
    await ctx.message.reply(embed=embed, delete_after=120)


@bot.command(name="spotify_login", brief="Login to Spotify")
async def spotify_login(ctx):
    global GLOBAL_COUNT
    try:
        if usersdb.get_user(ctx.author.id):
            await ctx.message.reply("You are already logged in!", delete_after=120)
            return

        auth_manager = create_auth_manager()
        auth_url = auth_manager.get_authorize_url()
        user = None
        if ctx.author.id == bot.user.id:
            # Send the messages to yourself
            user = await bot.fetch_user(int(CREATOR_ID))
            # print(user.id)
            await user.send(
                f"Click [here]({auth_url}) to log in to Spotify.\n"
                + "If you approve, it will redirect you to a 404 site.\n"
                + "Paste the entire redirect URL:",
                delete_after=120,
            )
            await ctx.message.reply(
                random.choice(
                    [
                        "Yo boss, just dropped the Spotify login link. Hook me up with that login, fam. The rest of y'all, sit tight and grab some popcorn.",
                        "Ayy chief, check your DMs for the Spotify login link. Slide into that login real quick. Others, be patient, your turn is coming.",
                        "Hey big shot, I shot you the Spotify login link. Log me in, fam, or I'll start playing Justin Bieber on loop. Others, chill for a sec, let the boss handle business.",
                        "Listen up, boss. Just tossed you the Spotify login link. Get on it and log me in, alright? Others, sit tight.",
                        "Oi, chief! Check your DMs for the Spotify login link. Get in there and log me in, pronto. The rest of you, hold your horses.",
                        "Hey, big shot! I sent you the Spotify login link. Time to get your act together and log me in. Others, just hang in there for a sec.",
                        "Hey you! Spotify login link in your DMs. Quit messing around and log me in. The others can wait.",
                    ]
                )
                + user.mention
                + user.mention
                + user.mention
                + user.mention,
                delete_after=120,
            )

        else:
            await ctx.author.send(
                f"Click [here]({auth_url}) to log in to Spotify.\n"
                + "If u approve, it will redirect u to a 404 page\n"
                + "Paste the redirect URL:",
                delete_after=120,
            )
            # await ctx.author.send('''If u approve, it will redirect u to a 404 page''',delete_after=120)
            # await ctx.author.send("Paste the redirect URL",delete_after=120)
            await ctx.message.reply(
                random.choice(
                    [
                        "I just slid into your DMs with the Spotify login link ;). Check it out!",
                        "Sent you a quick DM with the Spotify login link. Go grab it!",
                        "Check your DMs for the Spotify login link. I gotchu!",
                        "Yo, just dropped the Spotify login link in your DMs. Take a look!",
                        "Your DMs just got blessed with the Spotify login link. Go and fking grab it!",
                    ]
                ),
                delete_after=120,
            )

        # and message.guild.id == ctx.guild.id and message.channel.id == ctx.channel.id
        def check(message):
            return (
                (user is None and message.author == ctx.author)
                or (user and message.author == user)
            ) and isinstance(message.channel, discord.DMChannel)

        try:
            message = await bot.wait_for("message", check=check, timeout=60)
            access_token = auth_manager.get_access_token(
                auth_manager.get_authorization_code(message.content)
            )
            del message
            if access_token:
                # users[ctx.author.id] = encrypt_data(access_token)
                # users[ctx.author.id]['flag']=True
                usersdb.add_user(ctx.author.id, encrypt_data(auth_manager))
                GLOBAL_COUNT += 1
                sp = spotipy.Spotify(auth=access_token)

                user_info = sp.current_user()
                if user:
                    await user.send(
                        f"Logged in as: {user_info['display_name']} (ID: {user_info['id']})",
                        delete_after=120,
                    )

                    # await message.delete() #doesnt work in DMs, only user can delete their messages in their DMs not bots
                    await user.send(
                        "Please delete the url for security reasons.", delete_after=120
                    )
                    await ctx.send("IM INNNNN BISSHHESS!")
                    await ctx.send(
                        random.choice(
                            [
                                "From now on, I'll be adding all the songs you share in this server to my playlist. And guess what? Others who are logged in to me? Their playlists too. Better watch what you drop, it's going straight into the hall of bangers!",
                                "Alright, listen up! Starting today, every track you share here is going straight into my playlist. Oh, and everyone else who's logged in? Yeah, their playlists too. Choose wisely, or suffer the consequences!",
                                "You just stepped into my world. Every song you drop here is now in my playlist. So, share wisely, or prepare for a symphony of regret!",
                            ]
                        ),
                        delete_after=120,
                    )

                else:
                    await ctx.author.send(
                        f"Logged in as: {user_info['display_name']} (ID: {user_info['id']})",
                        delete_after=120,
                    )

                    # await message.delete() #doesnt work in DMs, only user can delete their messages in their DMs not bots
                    await ctx.author.send(
                        "Please delete the url for security reasons.", delete_after=120
                    )
            else:
                if user:
                    await user.send("Failed to get access token.", delete_after=120)
                else:
                    await ctx.author.send(
                        "Failed to get access token.", delete_after=120
                    )

            del auth_manager
            del access_token
            del sp

            # print(users)
        except TimeoutError:
            if user:
                await user.send("Login timeout. Please try again.", delete_after=120)
            else:
                await ctx.author.send(
                    "Login timeout. Please try again.", delete_after=120
                )

        except spotipy.SpotifyOauthError as oauth_error:
            if "invalid_grant" in str(oauth_error):
                if user:
                    await user.send(
                        "Error during Spotify authentication: The provided authorization code is invalid. Please initiate the login process again.",
                        delete_after=120,
                    )
                else:
                    await ctx.author.send(
                        "Error during Spotify authentication: The provided authorization code is invalid. Please initiate the login process again.",
                        delete_after=120,
                    )
            else:
                if user:
                    await user.send(
                        f"Error during Spotify authentication: {oauth_error}. Please try again after sometime.",
                        delete_after=120,
                    )
                else:
                    await ctx.author.send(
                        f"Error during Spotify authentication: {oauth_error}. Please try again after sometime.",
                        delete_after=120,
                    )

    except spotipy.SpotifyException as e:
        if user:
            await user.send(
                f"Error during Spotify authentication: {e}. [Please note that this application is currently in development mode, and access is limited to users registered on the app's dashboard. The app can accommodate a maximum of 25 users, and only those registered users have access to this bot. If you want to use it, please DM the creator your Spotify email.]",
                delete_after=120,
            )
            # usersdb.del_user(ctx.author.id)
        else:
            await ctx.author.send(
                f"Error during Spotify authentication: {e}. [Please note that this application is currently in development mode, and access is limited to users registered on the app's dashboard. The app can accommodate a maximum of 25 users, and only those registered users have access to this bot. If you want to use it, please DM the creator your Spotify email.]",
                delete_after=120,
            )
            # usersdb.del_user(ctx.author.id)


@bot.command(name="spotify_logout", brief="Logout from Spotify")
async def spotify_logout(ctx):
    await ctx.message.reply(
        random.choice(
            [
                "Logged the fook out!",
                "You're out, bich! Logout successful.",
                "Logout complete, motherfather!",
                "Peace out ho! You're logged the f out.",
            ]
        )
        if usersdb.del_user(ctx.author.id)
        else random.choice(
            [
                "Bruh, you ain't even logged in to logout. Get it together.",
                "mothafucka u r not logged in to logout",
            ]
        ),
        delete_after=120,
    )


@bot.command(name="playlists", brief="Bot-made playlists 4 u")
async def playlists(ctx):
    if usersdb.get_user(ctx.author.id):
        embed = discord.Embed(title="You x Bot", color=0x1DB954)
        for playlist_name, playlist_id in usersdb.get_playlist_ids(
            ctx.author.id
        ).items():
            embed.add_field(
                name=playlist_name,
                value=f"[Open Playlist](https://open.spotify.com/playlist/{playlist_id})",
                inline=False,
            )
        await ctx.message.reply(embed=embed, delete_after=120)
    else:
        if ctx.author.id == bot.user.id:
            await ctx.message.reply("Bot is not logged in yet :(", delete_after=120)
        else:
            await ctx.message.reply(
                random.choice(
                    [
                        f"Bruh, you gotta log in with `{bot.command_prefix}spotify_login` first.",
                        f"Yo, hit up `{bot.command_prefix}spotify_login` before using this command.",
                        f"Bro, log in using `{bot.command_prefix}spotify_login` real quick.",
                        f"Fam, make sure to `{bot.command_prefix}spotify_login` before using this command.",
                        f"You need to log in with `{bot.command_prefix}spotify_login` before using this command.",
                    ]
                ),
                delete_after=120,
            )


@bot.command(name="plelists", brief="your playlists(for testing)")
async def plelists(ctx):
    if usersdb.get_user(ctx.author.id):
        sp = spotipy.Spotify(
            auth_manager=decrypt_data(usersdb.get_auth_manager(ctx.author.id))
        )
        playlists = sp.current_user_playlists()
        # print(playlists)
        embed = discord.Embed(title="Your Playlists", color=0x1DB954)

        for playlist in playlists["items"]:
            # print(playlist["id"])
            embed.add_field(
                name=playlist["name"],
                value=f"Tracks: {playlist['tracks']['total']}",
                inline=False,
            )

        await ctx.message.reply(embed=embed, delete_after=120)

        del sp
    else:
        await ctx.message.reply(
            random.choice(
                [
                    f"Bruh, you gotta log in with `{bot.command_prefix}spotify_login` first.",
                    f"Yo, hit up `{bot.command_prefix}spotify_login` before using this command.",
                    f"Bro, log in using `{bot.command_prefix}spotify_login` real quick.",
                    f"Fam, make sure to `{bot.command_prefix}spotify_login` before using this command.",
                    f"You need to log in with `{bot.command_prefix}spotify_login` before using this command.",
                ]
            ),
            delete_after=120,
        )


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


def main():
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    try:
        bot.help_command = CustomHelpCommand()
        bot.run(DISCORD_BOT_ID)

    except Exception as e:
        print(f"Exception: {e}")

    finally:
        if "users" in locals():
            del users
        # if "serversdb" in locals():
        #     del serversdb
        print("finally DBs deleted!")


if __name__ == "__main__":
    main()
