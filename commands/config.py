import discord
from discord.ext import commands

class ConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = "http://localhost:8000"
    
    @discord.app_commands.command(name="config", description="Konfigurációs link generálása")
    async def config(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message(
                "❌ Csak a szerver tulajdonosa használhatja ezt a parancsot!",
                ephemeral=True
            )
            return
        
        guild_id = interaction.guild.id
        
        try:
            token = self.bot.db.generate_config_token(guild_id, expires_in_minutes=5)
            
            if not token:
                await interaction.response.send_message(
                    "❌ Hiba a token generálása során!",
                    ephemeral=True
                )
                return
            
            config_url = f"{self.api_url}/config?guild_id={guild_id}&token={token}"
            
            embed = discord.Embed(
                title="⚙️ Szerver Konfigurálása",
                description="Kattints az alábbi gombra a konfigurációs panel megnyitásához.",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="⏱️ Érvényes ideig",
                value="5 perc",
                inline=False
            )
            embed.add_field(
                name="⚠️ Megjegyzés",
                value="Ez a link csak egyszer használható és 5 perc után lejár.",
                inline=False
            )
            embed.set_footer(text="Biztonság első")
            
            view = discord.ui.View()
            view.add_item(discord.ui.Button(
                label="Konfigurálás",
                url=config_url,
                style=discord.ButtonStyle.primary
            ))
            
            await interaction.response.send_message(
                embed=embed,
                view=view,
                ephemeral=True
            )
            
            print(f"✅ Config parancs: {guild_id} - Token: {token[:20]}...")
            
        except Exception as e:
            print(f"❌ Hiba a config parancsban: {e}")
            await interaction.response.send_message(
                f"❌ Hiba: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(ConfigCog(bot))