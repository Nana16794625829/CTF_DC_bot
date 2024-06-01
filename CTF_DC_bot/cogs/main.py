from scrap import scrap as event
import discord
from discord.ext import commands


# 定義名為 Main 的 Cog
class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ctf_list = []

    # 透過前綴指令觸發機器人
    @commands.command()
    async def upcoming_event(self, ctx: commands.Context):
        self.ctf_list = event.get_info(event.rows)

        try:
            if len(self.ctf_list) == 0:
                await ctx.send("近期沒有權重25以上的賽事")
                print(self.ctf_list)
                print(event.ctf_list)
            else:
                for ctf_event in self.ctf_list:
                    name = ctf_event.get("event_name")
                    date = ctf_event.get("date")
                    weight = ctf_event.get("weight")
                    url = ctf_event.get("url")

                    await ctx.send(f"{name}將在{date}舉辦，這場賽事的權重有{weight}。")
                    await ctx.send(url)

        except Exception as e:
            await ctx.send(f"無法獲取賽事資訊，錯誤: {str(e)}")

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
