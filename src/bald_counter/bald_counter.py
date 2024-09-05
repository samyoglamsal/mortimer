import asyncio
import discord
import matplotlib.pyplot as plt
from datetime import datetime

from datetime import timedelta
from discord.ext import commands
from io import BytesIO
from src.database.database_client import DatabaseClient

GREENBALD_ID = 217434504372027392

class BaldCounter(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.db_client = DatabaseClient()
        self.analyzing_greenbald = False

    def add_mortimer_bald_count(self, count: int):
        cursor = self.db_client.con.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mortimer'")
        if not cursor.fetchone():
            print(f"Table 'mortimer' does not exist, creating...")
            cursor.execute("CREATE TABLE mortimer (timestamp TEXT PRIMARY KEY, count INTEGER)")
    
        current_time = datetime.now().isoformat()
        cursor.execute("INSERT INTO mortimer VALUES (?, ?)", (current_time, count))
        self.db_client.con.commit()
        print(f"Successfully inserted ({current_time}, {count}) into table mortimer")

    def get_mortimer_bald_counts(self):
        cursor = self.db_client.con.cursor()
        cursor.execute("SELECT * FROM mortimer")
        return cursor.fetchall()

    @commands.Cog.listener()
    async def on_ready(self):
        print("BaldCounter ready")

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

        self.add_mortimer_bald_count(count)
        data = self.get_mortimer_bald_counts()
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
