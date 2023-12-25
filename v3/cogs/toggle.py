import discord
from discord import Guild, app_commands
from discord.ext import commands
from sys import stdout
from db import ServerStore
import random
from mybot import CustomBot


class Toggle(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot
        self.bot.serversdb: ServerStore

    @commands.command(
        name="!toggle_server", brief="Toggles Bot's servers Listening status"
    )
    @commands.has_permissions(administrator=True)
    async def toggleeee(self, ctx: commands.Context):
        await self.bot.get_command("toggle_server")(ctx)

    @commands.command(name="toggle_server", brief="Toggles server's Listening status")
    async def toggleee(self, ctx):
        ctxx = self.bot.user if ctx.message.content == "!!toggle_server" else ctx.author
        flag = self.bot.serversdb.get_server_users(ctx.guild.id).get_flag(ctxx.id)
        if flag is not None:
            self.bot.serversdb.get_server_users(ctx.guild.id).toggle_flag(ctxx.id)
            await ctx.message.reply(
                f"Server's Listening flag toggled.\nNow **{'listening' if not flag else 'not listening'}**.",
                delete_after=120,
            )
        else:
            if self.bot.user == ctxx:
                await ctx.message.reply("Bot is not logged in yet :(", delete_after=120)
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

    @commands.command(
        name="!toggle_channel", brief="Toggles Bot's channels Listening status"
    )
    @commands.has_permissions(administrator=True)
    async def togglee(self, ctx: commands.Context):
        await self.bot.get_command("toggle_channel")(ctx)

    @commands.command(name="toggle_channel", brief="Toggles channels Listening status")
    async def toggle(self, ctx):
        ctxx = (
            self.bot.user if ctx.message.content == "!!toggle_channel" else ctx.author
        )
        flag = self.bot.serversdb.get_server_users(ctx.guild.id).get_flag(
            ctxx.id, ctx.channel.id, ctx.channel.name
        )
        if flag is not None:
            self.bot.serversdb.get_server_users(ctx.guild.id).toggle_flag(
                ctxx.id, ctx.channel.id, ctx.channel.name
            )
            await ctx.message.reply(
                f"Channel's Listening flag toggled.\nNow **{'listening' if not flag else 'not listening'}**.",
                delete_after=120,
            )
        else:
            if self.bot.user == ctxx:
                await ctx.message.reply("Bot is not logged in yet :(", delete_after=120)
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

    @commands.command(name="!status", brief="Shows Bot's listening status")
    @commands.has_permissions(administrator=True)
    async def statuss(self, ctx: commands.Context):
        await self.bot.get_command("status")(ctx)

    @commands.command(name="status", brief="Shows listening status")
    async def status(self, ctx):
        ctxx = self.bot.user if ctx.message.content == "!!status" else ctx.author
        flag_server = self.bot.serversdb.get_server_users(ctx.guild.id).get_flag(
            ctxx.id
        )
        flag_channel = self.bot.serversdb.get_server_users(ctx.guild.id).get_flag(
            ctxx.id, ctx.channel.id, ctx.channel.name
        )
        reply = ""
        if flag_server is not None and flag_channel is not None:
            reply += "Server: " + (
                "listening ^.^" if flag_server else "not listening :("
            )
            reply += "\nThis Channel: " + (
                "listening ^.^" if flag_channel else "not listening :("
            )

            await ctx.message.reply(reply, delete_after=120)

        else:
            if self.bot.user == ctxx:
                await ctx.message.reply("Bot is not logged in yet :(", delete_after=120)
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

    @commands.command(name="!supply", brief="Check Power for bot")
    @commands.has_permissions(administrator=True)
    async def supply(self, ctx: commands.Context):
        flag = self.bot.serversdb.get_flag(ctx.guild.id)
        if flag is not None:
            await ctx.message.reply(
                f"Bot is switched **{'on' if flag else 'off'}**.",
                delete_after=120,
            )

    @commands.command(name="!power", brief="Power off/on Bot")
    @commands.has_permissions(administrator=True)
    async def power(self, ctx: commands.Context):
        flag = self.bot.serversdb.get_flag(ctx.guild.id)
        if flag is not None:
            self.bot.serversdb.toggle_flag(ctx.guild.id)
            await ctx.message.reply(
                f"Bot is now switched **{'on' if not flag else 'off'}**.",
                delete_after=120,
            )


async def setup(bot: CustomBot):
    await bot.add_cog(Toggle(bot))
