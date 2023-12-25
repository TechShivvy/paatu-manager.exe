import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

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

async def main():
    global bot

    try:
        async with bot:
            # await load()
            await bot.start(os.getenv("DISCORD_BOT_ID"))

    except Exception as e:
        print(f"Exception: {e}")

    finally:
        print("finally!")


if __name__ == "__main__":
    discord.utils.setup_logging()
    asyncio.run(main())
