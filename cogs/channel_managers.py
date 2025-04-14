import discord
from discord.ext import commands
from utils.views import ShopView, AutoparkView
from utils.database import Database
from config import CHANNEL_IDS, SHOP_ITEMS, CAR_RENTAL  # Добавляем импорт

class ChannelManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database("channels")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.initialize_channels()

    async def initialize_channels(self):
        for name, cid in CHANNEL_IDS.items():
            channel = self.bot.get_channel(cid)
            if not channel: continue

            with self.db.transaction() as data:
                if not data.get(str(cid)):
                    embed = self._create_embed(name)
                    view = self._create_view(name)
                    msg = await channel.send(embed=embed, view=view)
                    data[str(cid)] = msg.id

    def _create_embed(self, name):
        embeds = {
            "shop": discord.Embed(
                title="🛒 Магазин",
                color=0x00ff00
            ),
            "autopark": discord.Embed(
                title="🚗 Автопарк",
                color=0x7289da
            )
        }
        return embeds.get(name)

    def _create_view(self, name):
        if name == "shop":
            return ShopView()
        elif name == "autopark":
            return AutoparkView()
        return None

async def setup(bot):
    await bot.add_cog(ChannelManager(bot))