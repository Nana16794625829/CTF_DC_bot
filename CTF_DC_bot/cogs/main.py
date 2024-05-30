import discord
from discord.ext import commands


# 定義名為 Main 的 Cog
class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 透過前綴指令觸發機器人
    @commands.command()
    async def Test(self, ctx: commands.Context):
        await ctx.send("Response for the test.")

    # 透過關鍵字觸發機器人
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.content == "Hello":
            await message.channel.send("Hello, world!")


# 將 Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
