import discord
from discord import Guild, app_commands
from discord.ext import commands
from sys import stdout
from db import ServerStore
import random
from mybot import CustomBot


class Playlist(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot
        self.bot.serversdb: ServerStore

    @commands.command(name="!playlists", brief="Shows Bot's Playlists")
    async def playlistss(self, ctx: commands.Context):
        await self.bot.get_command("playlists")(ctx)

    @commands.command(name="playlists", brief="Shows You x Bot Playlists")
    async def playlists(self, ctx):
        ctxx = self.bot.user if ctx.message.content == "!!playlists" else ctx.author
        if self.bot.serversdb.get_server_users(ctx.guild.id).get_user(ctxx.id):
            embed1 = discord.Embed(title="Spotify", color=0x1DB954)
            embed2 = discord.Embed(title="Youtube", color=0xFF0000)
            channels_info = self.bot.serversdb.get_server_users(
                ctx.guild.id
            ).get_channels_info(ctxx.id)

            for channel_id, channel_data in channels_info.items():
                channel_name = channel_data["name"]
                server_name = ctx.guild.name
                spoti_playlist_id = channel_data["playlists"]["spotify"]
                yt_playlist_id = channel_data["playlists"]["youtube"]

                if spoti_playlist_id:
                    embed1.add_field(
                        name=f"{server_name}/{channel_name}",
                        value=f"[Open Playlist](https://open.spotify.com/playlist/{spoti_playlist_id})",
                        inline=False,
                    )

                if yt_playlist_id:
                    embed2.add_field(
                        name=f"{server_name}/{channel_name}",
                        value=yt_playlist_id,
                        inline=False,
                    )

            if not embed1.fields and not embed2.fields:
                await ctx.message.reply("No playlists found.")
            else:
                if embed1.fields:
                    await ctx.message.reply(embed=embed1)
                if embed2.fields:
                    await ctx.message.reply(embed=embed2)

        else:
            if self.bot.user == ctxx:
                await ctx.message.reply("Bot is not logged in yet :(", delete_after=120)
            else:
                await ctx.message.reply(
                    random.choice(
                        [
                            f"Bruh, you gotta log in with `{self.bot.command_prefix}spotify_login` first.",
                            f"Yo, hit up `{self.bot.command_prefix}spotify_login` before using this command.",
                            f"Bro, log in using `{self.bot.command_prefix}spotify_login` real quick.",
                            f"Fam, make sure to `{self.bot.command_prefix}spotify_login` before using this command.",
                            f"You need to log in with `{self.bot.command_prefix}spotify_login` before using this command.",
                        ]
                    ),
                    delete_after=120,
                )


async def setup(bot):
    await bot.add_cog(Playlist(bot))
