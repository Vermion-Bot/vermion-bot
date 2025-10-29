import discord
from discord.ext import commands
import aiohttp

class TesztCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = "http://localhost:8000/api/config"
    
    @discord.app_commands.command(name="teszt", description="Tesztelek")
    async def teszt(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        print(f"🔍 Guild ID: {guild_id}")
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/{guild_id}"
                print(f"📡 API URL: {url}")
                
                async with session.get(url) as resp:
                    print(f"📊 Response status: {resp.status}")
                    data = await resp.json()
                    print(f"📦 Response data: {data}")
                    
                    test_message = data.get('test_message')
                    
                    if test_message:
                        await interaction.response.send_message(test_message)
                    else:
                        await interaction.response.send_message(
                            f"❌ Nincs konfigurált üzenet erre a guild-re! "
                            f"(Guild ID: {guild_id})"
                        )
        except Exception as e:
            print(f"❌ Hiba: {e}")
            await interaction.response.send_message(f"❌ Hiba: {str(e)}")

async def setup(bot):
    await bot.add_cog(TesztCog(bot))