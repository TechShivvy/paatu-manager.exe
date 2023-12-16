import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
DISCORD_BOT_ID= os.getenv("DISCORD_BOT_ID")

intents = discord.Intents.all()
intents.message_content = True  
intents.members=True

bot = commands.Bot(command_prefix='!',intents=intents)

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope='user-read-playback-state user-modify-playback-state', cache_path=".spotifycache")


    

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

# health check
@bot.command(name='ping')
async def ping(ctx):
    # await ctx.send('Pong!')
    await ctx.message.reply('Pong!')

@bot.command(name='spotify_login')
async def spotify_login(ctx):
    auth_url = sp_oauth.get_authorize_url()
    # await ctx.author.send(f'Click the following link to log in to Spotify: {auth_url}')
    await ctx.message.reply(f'Click [here]({auth_url}) to log in to Spotify.')
    # await ctx.message.reply('I have sent you a direct message with the Spotify login link.')

# Command to handle Spotify authorization callback
@bot.command(name='spotify_callback')
async def spotify_callback(ctx, code):  
    token_info = sp_oauth.get_access_token(code)
    # You can save the access token and other information in a database or use it for further Spotify API requests
    await ctx.author.send('Spotify login successful! You can now use Spotify commands.')


bot.run(DISCORD_BOT_ID)
