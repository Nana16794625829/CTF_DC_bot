import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(".env")
DC_bot_token = os.getenv("DC_bot_token")


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)


# 完成啟動機器人的提示
@bot.event
async def on_ready():
    print(f'目前登入身份 --> {bot.user}')


# 載入指定指令檔
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")


# 重新載入指定指令檔
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")


# 卸載指定指令檔
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")


# 啟動機器人時自動載入指令檔
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(DC_bot_token)


if __name__ == "__main__":
    asyncio.run(main())
