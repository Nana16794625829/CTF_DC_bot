import os
from scrap import scrap as event
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv("../.env")
channel_id = os.getenv("PROGRESSING_CHANNEL_ID")
server_id = os.getenv("SERVER_ID")


class ProgressingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ctf_list = []
        self.guild = None
        self.channel = None
        self.progressing_event.start()

    async def send_msg(self):
        try:
            if len(self.ctf_list) == 0:
                await self.channel.send("今天沒有進行中的賽事")

            for ctf_event in self.ctf_list:
                name = ctf_event.get("event_name")
                date = ctf_event.get("date")
                weight = ctf_event.get("weight")
                url = ctf_event.get("url")

                await self.channel.send(f"在 {date} 期間 {name} 賽事進行中，權重：{weight}。")
                await self.channel.send(url)

        except Exception as e:
            await self.channel.send(f"無法獲取賽事資訊，錯誤: {str(e)}")

    @tasks.loop(hours=24)
    async def progressing_event(self):
        # 確保bot已經完成開機才能正常存取server
        await self.bot.wait_until_ready()
        self.guild = self.bot.get_guild(int(server_id))
        self.channel = self.guild.get_channel(int(channel_id))
        self.ctf_list = event.get_progressing()
        await self.send_msg()

    @commands.command()
    async def start_progressing_event(self, ctx):
        if not self.progressing_event.is_running():
            self.progressing_event.start()
            await ctx.send("已開啟賽事推播功能")

        else:
            await ctx.send("賽事推播功能使用中")

    # 關閉賽事推播功能
    @commands.command()
    async def stop_progressing_event(self, ctx):
        if self.progressing_event.is_running():
            self.progressing_event.cancel()
            await ctx.send("已關閉賽事推播功能")

        else:
            await ctx.send("賽事推播功能未開啟")


# 將Cog載入Bot中
async def setup(bot: commands.Bot):
    await bot.add_cog(ProgressingCog(bot))
