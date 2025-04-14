import discord
from discord.ext import commands
from utils.database import Database
from utils.views import ConfirmationView, PaginatorView
from config import SHOP_ITEMS


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users_db = Database("users")
        self.shop_db = Database("shop")

    async def generate_shop_embed(self):
        embed = discord.Embed(
            title="🛒 Магазин сервера",
            description="Выберите товар для покупки:",
            color=0x2b2d31
        )

        for item, data in SHOP_ITEMS.items():
            embed.add_field(
                name=f"{item} - {data['price']} очков",
                value=f"```{data.get('description', '')}```",
                inline=False
            )

        return embed


class ShopView(View):
    def __init__(self):
        super().__init__(timeout=None)

        for item in SHOP_ITEMS:
            self.add_item(Button(
                style=discord.ButtonStyle.secondary,
                label=item,
                custom_id=f"shop_{item}"
            ))


async def setup(bot):
    await bot.add_cog(Shop(bot))