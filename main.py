import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.database import DatabaseManager

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

db = DatabaseManager(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

bot.db = db

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ {bot.user} Elindult!")

async def load_cogs():
    for filename in os.listdir("./bot/commands"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"commands.{filename[:-3]}")
            print(f"✅ {filename} betöltve")

bot.setup_hook = load_cogs

try:
    bot.run(os.getenv('DISCORD_TOKEN'))
finally:
    db.close()