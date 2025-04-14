import discord
from discord.ext import commands
from utils.database import Database
from utils.views import ConfirmationView
from config import *
from config import SHOP_ITEMS, CAR_RENTAL  # Добавляем импорт

class Interactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users_db = Database("users")
        self.cars_db = Database("cars")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        custom_id = interaction.data.get("custom_id")
        if not custom_id: return

        # Обработка магазина
        if custom_id.startswith("shop_"):
            await self._handle_shop(interaction, custom_id[5:])

        # Обработка автопарка
        elif custom_id == "autopark_select":
            await self._handle_autopark(interaction)

    async def _handle_shop(self, interaction, item_name):
        item = SHOP_ITEMS.get(item_name)
        if not item: return

        with self.users_db.transaction() as users:
            balance = users.get(str(interaction.user.id), {}).get("balance", 0)
            if balance < item["price"]:
                return await interaction.response.send_message(
                    "❌ Недостаточно средств!",
                    ephemeral=True
                )

            users[str(interaction.user.id)]["balance"] -= item["price"]
            if "role_id" in item:
                role = interaction.guild.get_role(item["role_id"])
                await interaction.user.add_roles(role)

            await interaction.response.send_message(
                f"✅ Вы купили {item_name}!",
                ephemeral=True
            )

    async def _handle_autopark(self, interaction):
        car = interaction.data["values"][0].lower()
        data = CAR_RENTAL.get(car)

        with self.users_db.transaction() as users, self.cars_db.transaction() as cars:
            if users[str(interaction.user.id)].get("balance", 0) < data["price"]:
                return await interaction.response.send_message(
                    "❌ Недостаточно средств!",
                    ephemeral=True
                )

            if cars.get(car, 0) <= 0:
                return await interaction.response.send_message(
                    "❌ Машины закончились!",
                    ephemeral=True
                )

            users[str(interaction.user.id)]["balance"] -= data["price"]
            cars[car] -= 1

            await interaction.response.send_message(
                f"✅ Вы арендовали {car.capitalize()}!",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Interactions(bot))