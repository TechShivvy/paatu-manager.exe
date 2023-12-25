import discord
from discord import app_commands
from discord.ext import commands

import os

from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.hybrid_command()
@app_commands.autocomplete()
async def test(ctx):
    await ctx.send("This is a hybrid command!")

@bot.tree.command
@app_commands.context_menu()
async def react(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message('Very cool message!', ephemeral=True)

@app_commands.context_menu()
async def ban(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f'Should I actually ban {user}...', ephemeral=True)


bot.run(os.getenv("DISCORD_BOT_ID"))
