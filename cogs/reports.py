import discord
from discord.ui import Modal, TextInput
from discord.ext import commands
from utils.database import Database
from config import EVENT_POINTS

class ReportModal(Modal):
    def __init__(self):
        super().__init__(title="Отчёт о мероприятии")
        self.add_item(TextInput(label="Тип мероприятия"))
        self.add_item(TextInput(label="Ссылка на скриншот", style=TextInputStyle.url))

class Reports(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reports_db = Database("reports")

    @commands.slash_command()
    async def report(self, ctx):
        await ctx.send_modal(ReportModal())

    @commands.Cog.listener()
    async def on_modal_submit(self, interaction: discord.Interaction):
        if interaction.custom_id != "ReportModal":
            return

        event_type = interaction.data["components"][0]["components"][0]["value"]
        screenshot = interaction.data["components"][1]["components"][0]["value"]

        points = EVENT_POINTS.get(event_type, 0)
        if points > 0:
            with Database("users").transaction() as data:
                user_data = data.setdefault(str(interaction.user.id), {"balance": 0})
                user_data["balance"] += points

            await interaction.response.send_message(
                f"✅ Отчёт принят! Начислено {points} очков",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Reports(bot))