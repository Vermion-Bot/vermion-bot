import discord
from discord.ext import commands
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.config_manager import config

class TesztCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.app_commands.command(name="teszt", description="Tesztelek")
    async def teszt(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        
        # utuility miatt sokkal könnyebb lesz kikérni értékeket!!!
        test_message = await config.get_string(guild_id, "test_message")
        
        if test_message:
            await interaction.response.send_message(test_message)
        else:
            await interaction.response.send_message(
                f"❌ Nincs konfigurált üzenet erre a guild-re! "
                f"(Guild ID: {guild_id})"
            )

async def setup(bot):
    await bot.add_cog(TesztCog(bot))