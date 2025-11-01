import discord
from discord.ext import commands
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

class dashbCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.app_commands.command(name="dash", description="dashboard link")
    async def dash(self, interaction: discord.Interaction):        
        await interaction.response.send_message("http://localhost:8000/" , ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(dashbCog(bot))