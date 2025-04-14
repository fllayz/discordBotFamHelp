import discord
from discord.ext import commands
from utils.database import Database
from utils.views import ConfirmationView, AdminView
from config import CAR_RENTAL_PRICES, ADMIN_ROLES


class Autopark(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cars_db = Database("autopark")
        self.users_db = Database("users")

    async def generate_autopark_embed(self):
        embed = discord.Embed(
            title="🚗 Автопарк",
            description="Арендуйте транспорт:",
            color=0x7289da
        )

        for car, price in CAR_RENTAL_PRICES.items():
            with self.cars_db.transaction() as data:
                available = data.get(car, 5)
                embed.add_field(
                    name=f"{car.capitalize()} - {price} очков/час",
                    value=f"Доступно: {available}",
                    inline=False
                )

        return embed


class AutoparkView(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(Select(
            placeholder="Выберите транспорт",
            options=[
                SelectOption(label=car.capitalize(), description=f"{price} очков/час")
                for car, price in CAR_RENTAL_PRICES.items()
            ],
            custom_id="autopark_select"
        ))

        if ADMIN_ROLES:
            self.add_item(Button(
                style=discord.ButtonStyle.red,
                label="Управление (Админ)",
                custom_id="autopark_admin",
                row=1
            ))


async def setup(bot):
    await bot.add_cog(Autopark(bot))