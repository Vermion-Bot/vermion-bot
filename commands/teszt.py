import discord
from discord.ext import commands
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

class TesztCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.app_commands.command(name="teszt", description="Tesztelek")
    async def teszt(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        
        test_message = self.bot.db.get_test_message(guild_id)
        
        if test_message:
            await interaction.response.send_message(test_message)
        else:
            await interaction.response.send_message(
                f"❌ Nincs konfigurált üzenet erre a guild-re!\n"
                f"Állítsd be a dashboardon: http://localhost:8000"
            )

async def setup(bot):
    await bot.add_cog(TesztCog(bot))