import discord

import logging
import os

from src.database_clients.database_client import DatabaseClient

BANNED_USERS = [272873412571955200]

logger = logging.getLogger(__name__)
db_client = DatabaseClient()

bot_token = os.getenv("BOT_TOKEN")
bot = discord.Bot()

@bot.event
async def on_ready():
    logger.info(f"{bot.user} is ready")

@bot.command(name="update", description="Updates your poop counter")
async def update_shitsheet(ctx):
    if ctx.user.id in BANNED_USERS:
        ctx.respond("You are BANNED nerd")
        return

    db_client.add_shitsheet_entry(ctx.user.id, ctx.user.name)

    user_poops = db_client.get_shitsheet_entries_by_user_id(ctx.user.id)
    await ctx.respond(f"You are now shitting at {len(user_poops)}.")


bot.run(bot_token)