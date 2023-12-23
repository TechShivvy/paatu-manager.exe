import discord
from discord.ext import commands
import asyncio
import spotipy
import random
from utils.spotify import create_auth_manager
from utils.crypt import *
from db import *


class Session(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="!spotify_login", brief="init bot account")
    # @commands.is_owner()
    @commands.has_permissions(administrator=True)
    async def init(self, ctx: commands.Context):
        # await ctx.send("!spotify_login")
        await self.bot.get_command("spotify_login")(ctx)

        def check(message: discord.Message):
            return (
                message.author.id == self.bot.user.id
                and message.channel.id == ctx.channel.id
                and message.content == "IM INNNNN BISSHHESS!"
            )

        try:
            message = await self.bot.wait_for("message", check=check, timeout=60)

            # await ctx.send('Received response: ' + response.content)

            # sp = spotipy.Spotify(
            #     auth_manager=decrypt_data(usersdb.get_auth_manager(self.bot.user.id))
            # )
            # for offset in range(0, 100001, 50):
            #     playlists = sp.current_user_playlists(limit=50, offset=offset)
            #     for playlist in playlists["items"]:
            #         # if f"{message.guild.name}/" in playlist["name"]:
            #         usersdb.set_playlist_id(self.bot.user.id, playlist["name"], playlist["id"])
            #     if len(playlists["items"]) == 0:
            #         break

        except asyncio.TimeoutError:
            print("Timeout reached. No response to !spotify_login.")

    @commands.command(name="!spotify_logout", brief="spotify logout 4 bot")
    # @commands.is_owner()
    @commands.has_permissions(administrator=True)
    async def deinit(self, ctx: commands.Context):
        await self.bot.get_command("spotify_logout")(ctx)

    @commands.command(name="spotify_login", brief="Login to Spotify")
    async def spotify_login(self, ctx: commands.Context):
        try:
            ctxx = (
                self.bot.user
                if ctx.message.content == "!!spotify_login"
                else ctx.author
            )
            if serversdb.get_server(ctx.guild.id)["users"].get_user(ctxx.id):
                await ctx.message.reply("You are already logged in!", delete_after=120)
                return

            auth_manager = create_auth_manager()
            auth_url = auth_manager.get_authorize_url()
            await ctx.author.send(
                f"Click [here]({auth_url}) to log in to Spotify.\n"
                + "If u approve, it will redirect u to a 404 page\n"
                + "Paste the redirect URL:",
                delete_after=120,
            )
            await ctx.message.reply(
                random.choice(
                    [
                        "I just slid into your DMs with the Spotify login link ;). Check it out!",
                        "Sent you a quick DM with the Spotify login link. Go grab it!",
                        "Check your DMs for the Spotify login link. I gotchu!",
                        "Yo, just dropped the Spotify login link in your DMs. Take a look!",
                        "Your DMs just got blessed with the Spotify login link. Go and fking grab it!",
                    ]
                )
                if ctxx == ctx.author
                else (
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
                    + ctx.message.author.mention
                    + ctx.message.author.mention
                    + ctx.message.author.mention
                    + ctx.message.author.mention
                ),
                delete_after=120,
            )

            # and message.guild.id == ctx.guild.id and message.channel.id == ctx.channel.id
            def check(message: discord.Message):
                return message.author == ctx.author and isinstance(
                    message.channel, discord.DMChannel
                )

            try:
                message = await self.bot.wait_for("message", check=check, timeout=60)
                access_token = auth_manager.get_access_token(
                    auth_manager.get_authorization_code(message.content)
                )

                if access_token:
                    # users[ctx.author.id] = encrypt_data(access_token)
                    # users[ctx.author.id]['flag']=True
                    serversdb.get_server(ctx.guild.id)["users"].add_user(
                        ctxx.id, encrypt_data(auth_manager)
                    )
                    sp = spotipy.Spotify(auth=access_token)

                    user_info = sp.current_user()

                    await ctx.author.send(
                        f"Logged in as: {user_info['display_name']} (ID: {user_info['id']})",
                        delete_after=120,
                    )

                    # await message.delete() #doesnt work in DMs, only user can delete their messages in their DMs not bots
                    await ctx.author.send(
                        "Please delete the url for security reasons.", delete_after=120
                    )

                    if ctxx == self.bot.user:
                        await ctx.send("IM INNNNN BISSHHESS!")
                        await ctx.send(
                            random.choice(
                                [
                                    "From now on, I'll be adding all the songs you share in this server to my playlist. And guess what? Others who are logged in to me? Their playlists too. Better watch what you drop, it's going straight into the hall of bangers!",
                                    "Alright, listen up! Starting today, every track you share here is going straight into my playlist. Oh, and everyone else who's logged in? Yeah, their playlists too. Choose wisely, or suffer the consequences!",
                                    "You just stepped into my world. Every song you drop here is now in my playlist. So, share wisely, or prepare for a symphony of regret!",
                                ]
                            ),
                        )

                else:
                    await ctx.author.send(
                        "Failed to get access token.", delete_after=120
                    )

                # del auth_manager
                # del access_token
                # del message
                # del sp

                # print(users)
            except TimeoutError:
                await ctx.author.send(
                    "Login timeout. Please try again.", delete_after=120
                )

            except spotipy.SpotifyOauthError as oauth_error:
                if "invalid_grant" in str(oauth_error):
                    await ctx.author.send(
                        "Error during Spotify authentication: The provided authorization code is invalid. Please initiate the login process again.",
                        delete_after=120,
                    )
                else:
                    await ctx.author.send(
                        f"Error during Spotify authentication: {oauth_error}. Please try again after sometime.",
                        delete_after=120,
                    )
            finally:
                del user_info, message, access_token

        except spotipy.SpotifyException as e:
            await ctx.author.send(
                f"Error during Spotify authentication: {e}. [Please note that this application is currently in development mode, and access is limited to users registered on the app's dashboard. The app can accommodate a maximum of 25 users, and only those registered users have access to this self.bot. If you want to use it, please DM the creator your Spotify email.]",
                delete_after=120,
            )
        finally:
            del auth_manager, sp

    @commands.command(name="spotify_logout", brief="Logout from Spotify")
    async def spotify_logout(self, ctx: commands.Context):
        ctxx = (
            self.bot.user if ctx.message.content == "!!spotify_logout" else ctx.author
        )
        await ctx.message.reply(
            random.choice(
                [
                    "Logged the fook out!",
                    "You're out, bich! Logout successful.",
                    "Logout complete, motherfather!",
                    "Peace out ho! You're logged the f out.",
                ]
            )
            if (serversdb.get_server(ctx.guild.id)["users"]).del_user(ctxx.id)
            else random.choice(
                [
                    "Bruh, you ain't even logged in to logout. Get it together.",
                    "mothafucka u r not logged in to logout",
                ]
            ),
            delete_after=120,
        )


async def setup(bot):
    await bot.add_cog(Session(bot))
