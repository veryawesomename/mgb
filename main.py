import discord
import os


from discord.ext import commands

bot = commands.Bot(command_prefix='%')

game = discord.Game("테스트 봇")

@bot.event
async def on_ready():
    print("로그인")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕")


access_token = os.environ["BOT_TOKEN"]
bot.run(access_token)
