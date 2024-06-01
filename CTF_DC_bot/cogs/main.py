import os
from scrap import scrap as event
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv("../.env")
channel_id = os.getenv("CHANNEL_ID")
server_id = os.getenv("SERVER_ID")


# 定義名為 Main 的 Cog
class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ctf_list = []
        self.guild = None
        self.channel = None
        self.upcoming_event.start()

    def cog_unload(self):
        self.upcoming_event.cancel()

    # 定時發送賽事訊息
    @tasks.loop(seconds=90)
    async def upcoming_event(self):
        # 確保bot已經完成開機才能正常存取server
        await self.bot.wait_until_ready()
        self.guild = self.bot.get_guild(int(server_id))
        self.channel = self.guild.get_channel(int(channel_id))
        self.ctf_list = event.get_info(event.rows)

        try:
            if len(self.ctf_list) == 0:
                await self.channel.send("近期沒有權重25以上的賽事")

            for ctf_event in self.ctf_list:
                name = ctf_event.get("event_name")
                date = ctf_event.get("date")
                weight = ctf_event.get("weight")
                url = ctf_event.get("url")

                await self.channel.send(f"{name}將在{date}舉辦，權重：{weight}。")
                await self.channel.send(url)

        except Exception as e:
            await self.channel.send(f"無法獲取賽事資訊，錯誤: {str(e)}")

    # 啟動賽事推播功能
    @commands.command()
    async def start_upcoming_event(self, ctx):
        if not self.upcoming_event.is_running():
            self.upcoming_event.start()
            await ctx.send("已開啟賽事推播功能")

        else:
            await ctx.send("賽事推播功能使用中")

    # 關閉賽事推播功能
    @commands.command()
    async def stop_upcoming_event(self, ctx):
        if self.upcoming_event.is_running():
            self.upcoming_event.cancel()
            await ctx.send("已關閉賽事推播功能")

        else:
            await ctx.send("賽事推播功能未開啟")


# 將 Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
