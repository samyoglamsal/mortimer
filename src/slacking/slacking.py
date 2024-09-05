import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from io import BytesIO

from src.database.database_client import DatabaseClient

class Slacking(commands.Cog):
    slacking_group = SlashCommandGroup("slacking")

    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot
        self.database_client = DatabaseClient()

    def is_valid_user(self, id: str) -> bool:
        """
        Checks if the given user should be tracked for slacking.
        """
        row = self.database_client.get_user_info(id)

        return row is not None and (row[2] == 1)

    def in_slacking_window(self, message: discord.Message) -> bool:
        """
        Checks if a message is sent on Discord between 9 a.m. - 5 p.m. on a weekday.
        """
        
        timestamp = message.created_at
        if timestamp.weekday() > 4: 
            print("It's a weekend")
            return False
        elif timestamp.hour < 9 or timestamp.hour > 17:
            print("It's past working hours")
            return False

        return True

    async def record_slack(self, message: discord.Message) -> None:
        """
        Records the slacking instance and sends a message in the channel.
        """
        
        query = "INSERT INTO slacking VALUES (?, ?)"
        self.database_client.execute_command(
            query,
            (message.author.id, message.created_at)
        )
        await message.reply("Slacker")

    @slacking_group.command(name="register", description="Start tracking a user for slacking") 
    async def register(self, ctx, user: Option(discord.SlashCommandOptionType.mentionable)) -> None:
        if ctx.user.id != 217434504372027392:
            return

        add_query = """
        INSERT INTO users (id, name, track_slacking)
        VALUES (?, ?, 1)
        """

        update_query = """
        UPDATE users
        SET track_slacking = ?
        WHERE id = ?
        """
        
        user_info = self.database_client.get_user_info(str(user.id))
        if user_info:
            if user_info[2]: # The third column is whether they're being tracked
                await ctx.respond(f"{user.name} is already being tracked")
                return
            else:
                self.database_client.execute_command(update_query, (1, str(user.id)))
        else:
            self.database_client.execute_command(add_query, (user.id, user.name))

        await ctx.respond(f"{user.name} is a registered slacker")

    @slacking_group.command(name="unregister", description="Stop tracking a user for slacking")
    async def unregister(self, ctx, user: Option(discord.SlashCommandOptionType.mentionable)) -> None:
        if ctx.user.id != 217434504372027392:
            return

        update_query = """
        UPDATE users
        SET track_slacking = ?
        WHERE id = ?
        """

        if self.database_client.get_user_info(str(user.id)):
            self.database_client.execute_command(update_query, (0, str(user.id)))
            await ctx.respond(f"No longer tracking {user.name} for slacking")
        else:
            await ctx.respond(f"{user.name} is already not being tracked for slacking")

    @slacking_group.command(name="report", description="Generate a slacking report")
    async def create_report(
        self, 
        ctx, 
        duration: Option(discord.SlashCommandOptionType.string, description="The length of time to generate the report", choices=["all", "week", "day"])
    ):
        now = datetime.now()
        cursor = self.database_client.con.cursor()

        slack_instances_query = "SELECT * FROM slacking"
        slack_instances: tuple[str, datetime] = [(id, datetime.fromisoformat(timestamp)) for id, timestamp in cursor.execute(slack_instances_query).fetchall()]

        slackers_query = "SELECT DISTINCT id FROM slacking"
        slackers: list[str] = [x[0] for x in cursor.execute(slackers_query).fetchall()]

        match duration:
            case "all":
                data = slack_instances
            case "week":
                data = [x for x in slack_instances if now - timedelta(hours=24 * 7) <= x[1] <= now]
            case "day":
                data = [x for x in slack_instances if now - timedelta(hours=24) <= x[1] <= now]

        pairs = []
        for slacker in slackers:
            instances = 0
            for datum in data:
                if datum[0] == slacker:
                    instances += 1
            pairs.append((slacker, instances))


        buffer = BytesIO()
        plt.bar(x=[i[0] for i in pairs], height=[i[1] for i in pairs])
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        await ctx.respond(file=discord.File(fp=buffer, filename="plot.png"))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slacking cog ready")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.application_id:
            return

        if self.is_valid_user(str(message.author.id)): # and self.in_slacking_window(message):
            await self.record_slack(message)

def setup(bot: discord.Bot):
    bot.add_cog(Slacking(bot))
