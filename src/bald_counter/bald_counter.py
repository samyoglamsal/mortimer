import asyncio
import discord
import matplotlib.pyplot as plt

from datetime import timedelta
from discord.ext import commands
from io import BytesIO
from src.utils.logging import create_logger
from src.database_clients.database_client import DatabaseClient

logger = create_logger(__name__)
GREENBALD_ID = 217434504372027392

class BaldCounter(commands.Cog):
    db_client = DatabaseClient()

    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.analyzing_greenbald = False

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("BaldCounter ready")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        
        if message.author.id == GREENBALD_ID and not self.analyzing_greenbald:
            await self.analyze_greenbald(message)

    async def analyze_greenbald(self, message: discord.Message) -> int:
        self.analyzing_greenbald = True 
        await asyncio.sleep(10)

        messages = message.channel.history(limit=100)
        count = 0
        async for entry in messages:
            if entry.author.id == GREENBALD_ID and (
                timedelta(minutes=0) <= entry.created_at - message.created_at <= timedelta(minutes=1)
            ):
                count += 1

        self.db_client.add_mortimer_bald_count(count)
        data = self.db_client.get_mortimer_bald_counts()
        plot = self.create_plot(data)
        await message.channel.send(file=discord.File(fp=plot, filename="plot.png"))
        self.analyzing_greenbald = False

    def create_plot(self, data: list[tuple[str, int]]):
        buffer = BytesIO()
        plt.plot([x[1] for x in data])
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        return buffer

def setup(bot: discord.Bot):
    bot.add_cog(BaldCounter(bot))
