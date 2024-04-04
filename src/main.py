import os
import discord

from src.utils.logging import create_logger

logger = create_logger(__name__)

def get_bot():
    bot = discord.Bot()

    dirname = os.path.dirname(__file__)
    for filename in os.listdir(os.path.join(dirname, './cogs')):
        if filename.endswith("_cog.py"):
            bot.load_extension(f"src.cogs.{filename.split('.')[0]}")

    return bot
    

if __name__ == "__main__":
    bot = get_bot()
    bot.run(os.environ["BOT_TOKEN"])