import discord
import logging
from discord.ext import commands
from config import TOKEN

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

async def load_cogs():
    cogs = [
        "cogs.channel_managers",
        "cogs.interactions"
    ]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
        except Exception as e:
            logging.error(f"Ошибка загрузки {cog}: {e}")

@bot.event
async def on_ready():
    logging.info(f"Бот {bot.user} запущен!")
    await load_cogs()

if __name__ == "__main__":
    bot.run(TOKEN)