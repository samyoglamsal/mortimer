import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from src.database_clients.database_client import DatabaseClient
from src.utils.logging import create_logger

logger = create_logger(__name__)

class Shitsheet(commands.Cog):
    BANNED_USERS = [272873412571955200]

    shitsheet = SlashCommandGroup("shitsheet")
    db_client = DatabaseClient()

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Ready")

    @shitsheet.command(name="update")
    async def update_shitsheet(self, ctx):
        if ctx.user.id in self.BANNED_USERS:
            await ctx.respond("You are BANNED nerd")
            return

        self.db_client.add_shitsheet_entry(ctx.user.id, ctx.user.name)

        user_poops = self.db_client.get_shitsheet_entries_by_user_id(ctx.user.id)
        await ctx.respond(f"You are now shitting at {len(user_poops)}.")
    

def setup(bot: discord.Bot):
    bot.add_cog(Shitsheet(bot))
