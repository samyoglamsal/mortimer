import os

from discord import Bot

def get_bot() -> Bot:
    bot = Bot()

    bot.load_extension(f"src.slacking.slacking")

    return bot

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    bot = get_bot()

    bot.run(token)
