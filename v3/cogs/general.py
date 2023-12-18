import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        guild_count = 0

        for guild in self.bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")
            self.bot.serversdb.add_server(guild.id, guild.name)
            guild_count += 1

        print("paatu-manager.exe is in " + str(guild_count) + " guilds.")
        print("------")
        print(f"Logged in as {self.bot.user.name} ({self.bot.user.id})")
        print("------")

    @commands.Cog.listener('on_guild_join')
    async def on_guild_join(self, guild):
        print("++++++")
        print("Bot has been added to a new server")
        print("List of servers the bot is in: ")

        self.bot.serversdb.add_server(guild.id, guild.name)

        for guild in self.bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")

        print(f"paatu-manager.exe is in {len(self.bot.guilds)} guilds.")
        print("++++++")

    @commands.command(name="ping", brief="To check Bot's Status")
    async def ping(self, ctx):
        await ctx.message.reply("Pong!", delete_after=120)

    @commands.command(name="ding", brief="To test cogs' reload")
    async def ding(self, ctx):
        await ctx.message.reply("Dong!", delete_after=120)


async def setup(bot):
    await bot.add_cog(General(bot))
