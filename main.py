import os
from dotenv import load_dotenv

from cryptography.fernet import Fernet

import re

import discord
from discord.ext import commands

import spotipy
from spotipy.oauth2 import SpotifyPKCE

load_dotenv()

GLOBAL_COUNT = 0

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
DISCORD_BOT_ID = os.getenv("DISCORD_BOT_ID")
KEY = os.getenv("KEY")

SPECIFIED_CHANNELS = [850273140268728342]

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

sp_oauth = SpotifyPKCE(client_id=SPOTIPY_CLIENT_ID,redirect_uri=SPOTIPY_REDIRECT_URI,scope="playlist-modify-private",cache_handler=spotipy.MemoryCacheHandler())

cipher_suite = Fernet(KEY.encode())

users = {}

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())
    
def decrypt_data(data):
    return cipher_suite.decrypt(data).decode()

def get_channel_name(channel_id):
    channel = bot.get_channel(channel_id)
    return channel.name if channel else "Unknown Channel"

@bot.event
async def on_ready():
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1

    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")
    print('------')
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Sorry, the command `{ctx.message.content}` is not recognized. Please use `!help` to see available commands.",delete_after=120)
    else:
        print(f"An error occurred: {type(error).__name__}, {error}")

@bot.event
async def on_message(message):
    global GLOBAL_COUNT
    await bot.process_commands(message)

    if message.author == bot.user:
        return

    if message.channel.id not in SPECIFIED_CHANNELS:
        return
    
    if GLOBAL_COUNT == 0:
        return

    words = message.content.split()

    spotify_track_regex = re.compile(r'https://open\.spotify\.com/track/([a-zA-Z0-9]+)')
    
    for word in words:
        match = spotify_track_regex.search(word)
        if match:
            track_id = match.group(1)
            # await add_track_to_playlist(track_id)     #have to implement
            await message.reply(f"Added Spotify track with ID {track_id} to the playlist!",delete_after=120)

    # await bot.process_commands(message)

@bot.command(name='ping',brief="To check Bot's Status")
async def ping(ctx):
    await ctx.message.reply('Pong!',delete_after=120)

@bot.command(name='status',brief="Shows listening status")
async def status(ctx):
    user_id = ctx.author.id
    if user_id in users:
        await ctx.message.reply(f"Listening status: {'listening' if users[user_id]['flag'] else 'not listening'}.",delete_after=120)
    else:
        await ctx.message.reply(f"You need to log in with `{bot.command_prefix}spotify_login` before using this command.",delete_after=120)

@bot.command(name='toggle_listen')
async def toggle_listen(ctx):
    global GLOBAL_COUNT
    user_id = ctx.author.id
    if user_id in users:
        GLOBAL_COUNT += -1 if users[user_id]["flag"] else 1
        # print(users[user_id]["flag"])
        users[user_id]["flag"] = not users[user_id]["flag"]  # Toggle the flag (1 to 0 or 0 to 1)
        # print(users[user_id]["flag"],end="\n\n")
        await ctx.message.reply(f"Listening flag toggled. Now {'listening' if users[user_id]['flag'] else 'not listening'}.",delete_after=120)
    else:
        await ctx.message.reply(f"You need to log in with `{bot.command_prefix}spotify_login` before using this command.",delete_after=120)

@bot.command(name='spotify_login',brief="Login to Spotify")
async def spotify_login(ctx):
    global GLOBAL_COUNT
    try:
        auth_url = sp_oauth.get_authorize_url()
        await ctx.author.send(f'Click [here]({auth_url}) to log in to Spotify.',delete_after=120)
        await ctx.author.send("Paste the code from the redirect URL:",delete_after=120)
        await ctx.message.reply('I have sent you a dm with the Spotify login link.',delete_after=120)

        def check(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        try:
            message = await bot.wait_for("message", check=check, timeout=60)
            code = message.content
            access_token = sp_oauth.get_access_token(code)
            if access_token:
                # users[ctx.author.id] = encrypt_data(access_token)
                # users[ctx.author.id]['flag']=True
                users[ctx.author.id] = {'access_token': encrypt_data(access_token), 'flag': True}
                GLOBAL_COUNT += 1
                sp = spotipy.Spotify(auth=access_token)
                user_info = sp.current_user()
                await ctx.author.send(f"Logged in as: {user_info['display_name']} (ID: {user_info['id']})",delete_after=120)

                # await message.delete() #doesnt work in DMs, only user can delete their messages in their DMs not bots
                await ctx.author.send("Please delete the previous messages for security reasons.",delete_after=120)
            else:
                await ctx.author.send("Failed to get access token.",delete_after=120)
        except spotipy.SpotifyOauthError as oauth_error:
            if "invalid_grant" in str(oauth_error):
                await ctx.author.send("Error during Spotify authentication: The provided authorization code is invalid. Please initiate the login process again.",delete_after=120)
            else:
                await ctx.author.send(f"Error during Spotify authentication: {oauth_error}. Please try again after sometime.",delete_after=120)
        except TimeoutError:
            await ctx.author.send("Login timeout. Please try again.",delete_after=120)
    except spotipy.SpotifyException as e:
        await ctx.author.send(f"Error during Spotify authentication: {e}. [Please note that this application is currently in development mode, and access is limited to users registered on the app's dashboard. The app can accommodate a maximum of 25 users, and only those registered users have access to this bot. If you want to use it, please DM the creator your Spotify email.]",delete_after=120)

@bot.command(name='playlists',brief="Lists your playlists")
async def playlists(ctx):
    if ctx.author.id in users:
        encrypted_access_token = users[ctx.author.id]['access_token']
        sp = spotipy.Spotify(auth=decrypt_data(encrypted_access_token))
        playlists = sp.current_user_playlists()
        
        embed = discord.Embed(title="Your Playlists", color=0x1DB954)
        
        for playlist in playlists['items']:
            embed.add_field(name=playlist['name'], value=f"Tracks: {playlist['tracks']['total']}", inline=False)
        
        await ctx.message.reply(embed=embed,delete_after=120)
    else:
        await ctx.message.reply(f"You need to log in with `{bot.command_prefix}spotify_login` before using this command.",delete_after=120)



class CustomHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Available Commands", color=0x3498db)

        for command in bot.commands:
            embed.add_field(name=f"`{bot.command_prefix}{command.name}`", value=command.brief or "Shows this Message", inline=True)
        embed.add_field(name="Important Note:", value="This application is currently in development mode. Access is limited to users registered on the app's dashboard. The app can accommodate a maximum of 25 users, and only those registered users have access to this bot. If you want to use it, please DM the creator your Spotify email.", inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

# @bot.command(name='help')
# async def help_command(ctx):
#     embed = discord.Embed(title="Available Commands", color=0x3498`db)

#     for command in bot.commands:
#         embed.add_field(name=f"!{command.name}", value=command.brief, inline=False)

#     await ctx.send(embed=embed)

bot.help_command = CustomHelpCommand()

bot.run(DISCORD_BOT_ID)