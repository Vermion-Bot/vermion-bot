import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ {bot.user} Elindult!")

async def load_cogs():
    for filename in os.listdir("./vermion-bot/commands"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"commands.{filename[:-3]}")
            print(f"✅ {filename} betöltve")

async def setup():
    await load_cogs()

bot.setup_hook = setup
bot.run(os.getenv('DISCORD_TOKEN'))