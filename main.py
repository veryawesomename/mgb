import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='%')

token = 'Nzc5NjEyMTg1OTA2NjQyOTc0.X7jEbQ.C9b-n_rECETmMAszmTv4ypbz454'
game = discord.Game("테스트 봇")

@bot.event
async def on_ready():
    print("로그인")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def 안녕(ctx):
    await ctx.send("안녕")



bot.run(token)