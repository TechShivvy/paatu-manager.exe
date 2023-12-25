import discord
from discord import Guild, app_commands
from discord.ext import commands
from sys import stdout
from db import ServerStore
from mybot import CustomBot


class General(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot
        # self.bot.serversdb: ServerStore  # Optional type hint, may not change color
        # assert isinstance(
        #     bot.serversdb, ServerStore
        # ), "bot.serversdb must be an instance of ServerStore"

        # if isinstance(bot.serversdb, ServerStore):
        #     self.bot.serversdb: ServerStore = bot.serversdb
        # super().__init__()
        # else:
        #     raise ValueError("The 'bot' parameter must be an instance of commands.Bot.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        # await self.bot.tree.sync()
        guild_count = 0

        for guild in self.bot.guilds:
            print(f"- {guild.id} (name: {guild.name})", flush=True)
            self.bot.serversdb.add_server(guild.id, guild.name)
            guild_count += 1

        print("paatu-manager.exe is in " + str(guild_count) + " guilds.")
        print("------")
        print(f"Logged in as {self.bot.user.name} ({self.bot.user.id})")
        print("------")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        print("++++++")
        print("Bot has been added to a new server")
        print("List of servers the bot is in: ")

        self.bot.serversdb.add_server(guild.id, guild.name)

        for guild in self.bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")

        print(f"paatu-manager.exe is in {len(self.bot.guilds)} guilds.")
        print("++++++")

    @commands.command(name="ping", brief="To check Bot's Status")
    # @commands.hybrid_command(name="ping", brief="To check Bot's ping")
    async def ping(self, ctx: commands.Context):
        await ctx.message.reply(f"Pong!...{self.bot.latency*1000}", delete_after=120)

    @commands.command(name="ding", brief="To test cogs' reload")
    async def ding(self, ctx: commands.Context):
        await ctx.message.reply("Dong!", delete_after=120)

    @commands.command(name="about", brief="About the bot")
    async def about(self, ctx: commands.Context):
        embed = discord.Embed(title="About:", color=0x3498DB)
        embed.add_field(
            name="",
            value="Yo, I'm your paatu-manager 🎶! I only vibe with Spotify song links for now (not playlists or tracks; my boss is thinking of adding YouTube too). Drop those links, and I'll add them to playlists. Let's make this server bumpin'!",
            inline=False,
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

        await ctx.send(embed=embed)

    # @app_commands.command()
    # @app_commands.describe(
    #     first_value="The first value you want to add something to",
    #     second_value="The value you want to add to the first value",
    # )
    # async def add(
    #     self, interaction: discord.Interaction, first_value: int, second_value: int
    # ):
    #     """Adds two numbers together."""
    #     await interaction.response.send_message(
    #         f"{first_value} + {second_value} = {first_value + second_value}",
    #         ephemeral=True,
    #     )
    #     message = await interaction.original_response()
    #     print(message)

    @commands.command(name="sync")
    async def sync(self, ctx: commands.Context):
        synced = await self.bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")


async def setup(bot: CustomBot):
    await bot.add_cog(General(bot))
