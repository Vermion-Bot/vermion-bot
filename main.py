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
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

db = DatabaseManager(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

bot.db = db

def sync_bot_guilds():
    guilds_data = []
    for guild in bot.guilds:
        guilds_data.append({
            'id': guild.id,
            'name': guild.name,
            'member_count': guild.member_count
        })
    
    db.sync_bot_guilds(guilds_data)

@bot.event
async def on_ready():
    await bot.tree.sync()
    sync_bot_guilds()
    
    print(f"""
    ╔══════════════════════════════════════════════╗
    ║  {bot.user} sikeresen elindult!           ║
    ╠══════════════════════════════════════════════╣
    ║  🌐 Dashboard: http://localhost:8000        ║
    ║  🔐 OAuth2 bejelentkezés aktív              ║
    ║  📊 {len(bot.guilds)} szerver                              ║
    ╚══════════════════════════════════════════════╝
    """)

async def load_cogs():
    cogs_path = Path(__file__).parent / "commands"
    if cogs_path.exists():
        for filename in os.listdir(cogs_path):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    await bot.load_extension(f"commands.{filename[:-3]}")
                    print(f"✅ {filename} betöltve")
                except Exception as e:
                    print(f"❌ Hiba {filename} betöltése során: {e}")

bot.setup_hook = load_cogs

try:
    bot.run(os.getenv('DISCORD_TOKEN'))
finally:
    db.close()