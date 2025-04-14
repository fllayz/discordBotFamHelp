import discord
from discord.ext import commands
from utils.database import Database
from utils.views import ConfirmationView, AdminView


class Fines(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fines_db = Database("fines")

    @commands.slash_command()
    @commands.has_any_role(*ADMIN_ROLES)
    async def fine(self, ctx, member: discord.Member, amount: int, reason: str):
        view = ConfirmationView(ctx.author.id)
        await ctx.respond(
            f"Выдать штраф {member.mention} на сумму {amount}$?",
            view=view
        )

        await view.wait()
        if view.value:
            with self.fines_db.transaction() as data:
                fines = data.setdefault(str(member.id), [])
                fines.append({
                    "amount": amount,
                    "reason": reason,
                    "status": "unpaid"
                })

            await ctx.edit(
                content=f"✅ Штраф выдан {member.mention}",
                view=None
            )


async def setup(bot):
    await bot.add_cog(Fines(bot))