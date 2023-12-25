from imports import *
from utils.crypt import *
from discord import app_commands
from db import ServerStore
from utils.spotify import add_track_to_playlists

load_dotenv()

# SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
# SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
# DISCORD_BOT_ID = os.getenv("DISCORD_BOT_ID")
# CREATOR_ID = os.getenv("CREATOR_ID")

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


def exit_handler(signum, frame):
    print(f"Received signal {signum}. Exiting gracefully.")
    sys.exit(0)


@atexit.register
def goodbye():
    print("GoodBye.")
    # sys.exit(0)


@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")


@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")


@bot.command()
async def reload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await bot.load_extension(f"cogs.{extension}")


async def load():
    for filename in os.listdir("./v3/cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_message(message: discord.Message):
    # print(bot.serversdb._ServerStore__servers)
    # self.bot.dispatch('custom_event', message)

    if (
        message.author.id == bot.user.id
        or (not message.guild)
        or message.channel.type == discord.ChannelType.private
        or isinstance(message.channel, discord.DMChannel)
    ):
        return

    # if (
    #     not bot.serversdb.get_flag(message.guild.id)
    #     and message.content != "!!power"
    #     and message.content != "!!supply"
    # ):
    #     return
    await bot.process_commands(message)

    if "!https://open.spotify.com/track/" in message.content:
        return

    words = message.content.split()

    spotify_track_regex = re.compile(r"https://open\.spotify\.com/track/([a-zA-Z0-9]+)")

    for word in words:
        match = spotify_track_regex.search(word)
        if match:
            track_id = match.group(1)
            result = await add_track_to_playlists(
                bot.serversdb,
                message.guild.id,
                message.channel.id,
                message.guild.name,
                message.channel.name,
                track_id,
                "spotify",
            )
            if result:
                await message.reply(
                    f"track added to playlists!",
                    mention_author=False,
                    delete_after=120,
                )

    del words


class CustomHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Available Commands:", color=0x3498DB)
        channel = self.get_destination()

        # embed.add_field(
        #     name="About:",
        #     value="Yo, I'm your paatu-manager 🎶! I only vibe with Spotify song links for now (not playlists or tracks; my boss is thinking of adding YouTube too). Drop those links, and I'll add them to playlists. Let's make this server bumpin'!",
        #     inline=False,
        # )

        # await channel.send(embed=embed)
        # embed.clear_fields()

        for command in bot.commands:
            if not any(
                command.name.startswith(prefix)
                for prefix in ["!", "load", "unload", "reload"]
            ):
                embed.add_field(
                    name=f"`{bot.command_prefix}{command.name}`",
                    value=command.brief or "Shows this Message",
                    inline=True,
                )

        await channel.send(embed=embed)
        # embed.clear_fields()

        # embed.add_field(
        #     name="Fun Fact:",
        #     value="Oh, and let me spill some tea - chief is still deciding if YouTube tracks are cool enough. Imagine, right?",
        #     inline=False,
        # )

        # embed.add_field(
        #     name="IMPORTANT NOTE:",
        #     value="This bot's in development. Limited to 25 spotify users on the dashboard. Only they can access. Wanna join? DM my boss your Spotify email.",
        #     inline=False,
        # )

        # channel = self.get_destination()
        # await channel.send(embed=embed)


async def main():
    global bot
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    try:
        async with bot:
            bot.help_command = CustomHelpCommand()
            bot.serversdb: ServerStore = ServerStore()

            await load()
            await bot.start(os.getenv("DISCORD_BOT_ID"))

    except Exception as e:
        print(f"Exception: {e}")

    finally:
        # if "serversdb" in locals():
        #     del serversdb
        if "bot" in locals():
            del bot
        print("finally DBs deleted!")


if __name__ == "__main__":
    # global serversdb
    # serversdb = ServerStore("main")
    discord.utils.setup_logging()
    asyncio.run(main())
