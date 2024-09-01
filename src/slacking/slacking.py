from datetime import datetime

import discord
from discord.ext import commands

from src.database.database_client import DatabaseClient

class Slacking(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot
        self.database_client = DatabaseClient()

    def is_valid_user(self, id: str) -> bool:
        """
        Checks if the given user should be tracked for slacking.
        """

        return self.database_client.get_user_info(id)[2]

    def in_slacking_window(self, message: discord.Message) -> bool:
        """
        Checks if a message is sent on Discord between 9 a.m. - 5 p.m. on a weekday.
        """
        
        timestamp = message.created_at
        if timestamp.weekday() > 4: 
            return False
        elif timestamp.hour < 9 or timestamp.hour > 17:
            return False

        return True

    async def record_slack(self, message: discord.Message) -> None:
        """
        Records the slacking instance and sends a message in the channel.
        """
        
        query = "INSERT INTO slacking VALUES (?, ?)"
        self.database_client.execute_command(query, (message.author.id, message.created_at))
        await message.reply("Slacker")

        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Slacking cog ready")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        id = str(message.author.id)
        timestamp = message.created_at

        if message.author.id == self.bot.application_id:
            return

        await self.record_slack(message)
        # if self.is_valid_user(id) and self.is_slacking(id, 

def setup(bot: discord.Bot):
    bot.add_cog(Slacking(bot))
