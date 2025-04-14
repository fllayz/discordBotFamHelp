import discord
from discord.ext import commands, tasks
from utils.database import Database
from utils.views import ConfirmationView
from config import EVENT_POINTS

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users_db = Database("users")
        self.voice_users = {}
        self.voice_check.start()

    @tasks.loop(minutes=15)
    async def voice_check(self):
        with self.users_db.transaction() as data:
            for user_id, minutes in self.voice_users.items():
                points = minutes // 5
                data.setdefault(user_id, {"balance": 0})["balance"] += points
                self.voice_users[user_id] = 0

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel and after.channel.id == VOICE_CHANNEL_ID:
            self.voice_users[str(member.id)] = 0
        elif before.channel and before.channel.id == VOICE_CHANNEL_ID:
            if str(member.id) in self.voice_users:
                del self.voice_users[str(member.id)]

    @commands.slash_command()
    async def balance(self, ctx):
        with self.users_db.transaction() as data:
            balance = data.get(str(ctx.author.id), {}).get("balance", 0)
        await ctx.respond(f"Ваш баланс: {balance} очков", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Economy(bot))