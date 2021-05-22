import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import pickle
import asyncio
import random
from keyboardgame import kg
import os

bot = commands.Bot(command_prefix="$", help_command = None)
game = discord.Game("$도움")
yon = ["예", "ㅇ"]

@bot.event
async def on_ready():
    print("준비완료")
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command()
@commands.is_owner()
async def 파일생성(ctx):
    try:
        with open("user_data_level.bin", "rb") as f:
            user_data_l = pickle.load(f)
        with open("user_data_exp.bin", "rb") as f:
            user_data_e = pickle.load(f)
        await ctx.send("이미 파일이 있습니다.")
    except FileNotFoundError:
        with open("user_data_level.bin", "wb+") as f:
            user_data_l = dict()
            pickle.dump(user_data_l, f)
        with open("user_data_exp.bin", "wb+") as f:
            user_data_e = dict()
            pickle.dump(user_data_e, f)
        await ctx.send("파일 생성이 완료되었습니다.")


@bot.command()
async def 등록(ctx):
    try:
        with open("user_data_level.bin", "rb") as f:
            user_data_l = pickle.load(f)
        with open("user_data_exp.bin", "rb") as f:
            user_data_e = pickle.load(f)
    except FileNotFoundError:
        with open("user_data_level.bin", "wb+") as f:
            user_data_l = dict()
            pickle.dump(user_data_l, f)
        with open("user_data_exp.bin", "wb+") as f:
            user_data_e = dict()
            pickle.dump(user_data_e, f)

    embed = discord.Embed(title="미니게임 봇", description="등록하시겠습니까? (예 or 아니요) ($은 빼고 적어주세요)", color=0x00ff00)
    embed.set_footer(text=str(ctx.message.author))
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=10.0)
        if msg.content in yon:
            if str(ctx.author.id) not in user_data_l:
                user_data_e[str(ctx.author.id)] = 0
                user_data_l[str(ctx.author.id)] = 1
                await ctx.send("즐거운 게임세상에 오신것을 환영합니다, " + ctx.message.author.mention + "님!")
            else:
                await ctx.send(ctx.message.author.mention + " 이미 등록하셨습니다.")
        else:
            await ctx.send(ctx.message.author.mention + " 등록이 취소되었습니다.")
    except asyncio.TimeoutError:
        await ctx.send(ctx.message.author.mention + " 시간이 초과되었습니다.")

    with open("user_data_exp.bin", "wb") as f:
        pickle.dump(user_data_e, f)
    with open("user_data_level.bin", "wb") as f:
        pickle.dump(user_data_l, f)


@bot.command()
async def 정보(ctx):
    try:
        with open("user_data_level.bin", "rb") as f:
            user_data_l = pickle.load(f)
        with open("user_data_exp.bin", "rb") as f:
            user_data_e = pickle.load(f)
    except FileNotFoundError:
        with open("user_data_level.bin", "wb+") as f:
            user_data_l = dict()
            pickle.dump(user_data_l, f)
        with open("user_data_exp.bin", "wb+") as f:
            user_data_e = dict()
            pickle.dump(user_data_e, f)
    if str(ctx.author.id) not in user_data_l:
        await ctx.send(ctx.message.author.mention + "님은 아직 등록하지 않으셨습니다.")


    else:
        if user_data_e[str(ctx.author.id)] >= user_data_l[str(ctx.author.id)] ** 2 * 50:
            user_data_l[str(ctx.author.id)] += 1
            embed = discord.Embed(title=f"{ctx.author.name}" + "님의 정보")
            embed.add_field(name="레벨", value=user_data_l[str(ctx.author.id)], inline=False)
            embed.add_field(name="경험치", value=str(user_data_e[str(ctx.author.id)]) + " / " + str(
                user_data_l[str(ctx.author.id)] ** 2 * 50), inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"{ctx.author.name}" + "님의 정보")
            embed.add_field(name="레벨", value=user_data_l[str(ctx.author.id)], inline=False)
            embed.add_field(name="경험치", value=str(user_data_e[str(ctx.author.id)]) + " / " + str(
                user_data_l[str(ctx.author.id)] ** 2 * 50), inline=False)
            await ctx.send(embed=embed)

@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title="강화게임")
    embed.add_field(name="설정", value="$등록", inline=False)
    embed.add_field(name="정보", value="$정보", inline=False)
    embed.add_field(name="게임", value="$두더지잡기\n$키보드워리어(제작중)", inline=False)
    await ctx.send(embed=embed)



# @bot.command()
# async def 초기화(ctx):
#     with open("user_data_level.bin", "rb") as f:
#         user_data_l = pickle.load(f)
#     with open("user_data_exp.bin", "rb") as f:
#         user_data_e = pickle.load(f)
#     with open("user_data_weapon.bin", "rb") as f:
#         user_data_w = pickle.load(f)
#     with open("w_str.bin", "rb") as f:
#         w_str = pickle.load(f)
#     if user_data_w[str(ctx.author.id)] == "없음":
#         await ctx.send(ctx.message.author.mention + "님은 무기를 가지고 계시지 않습니다.")
#
#     elif str(ctx.author.id) not in user_data_w:
#         await ctx.send(ctx.message.author.mention + "님은 등록되지 않은 사용자입니다.")
#
#     else:
#         await ctx.send(ctx.message.author.mention + " 어떤 것을 초기화하실지 입력해주세요. (무기 or 게임정보)")
#
#         def check(m):
#             return m.author == ctx.author and m.channel == ctx.channel
#
#         try:
#             msg = await bot.wait_for('message', check=check, timeout=10.0)
#             if msg.content == "무기":
#                 await ctx.send(ctx.message.author.mention + " 정말 " + user_data_w[
#                     str(ctx.author.id)] + "을(를) 초기화하시겠습니까? 초기화 후엔 복구가 불가능합니다.")
#                 await ctx.send("정말 초기화하시려면 무기 이름을 똑같이 입력해주세요.")
#                 try:
#                     w = await bot.wait_for('message', check=check, timeout=10.0)
#                     if w.content == user_data_w[str(ctx.author.id)]:
#                         await ctx.send(ctx.message.author.mention + " 무기 초기화가 완료되었습니다.")
#                         user_data_w[str(ctx.author.id)] = "없음"
#                         w_str[str(ctx.author.id)] = 20
#                     else:
#                         await ctx.send(ctx.message.author.mention + " 무기 이름이 일치하지 않습니다.")
#                 except asyncio.TimeoutError:
#                     await ctx.send(ctx.message.author.mention + " 시간이 초과되었습니다.")
#             elif msg.content == "게임정보":
#                 await ctx.send(
#                     ctx.message.author.mention + " 정말 정보를 초기화하시겠습니까? 무기와 레벨 등 모든 정보가 다 삭제됩니다.\n 초기화 후엔 복구가 불가능합니다.")
#                 await ctx.send("정말 초기화하시려면 무기 이름을 똑같이 입력해주세요.")
#                 try:
#                     w = await bot.wait_for('message', check=check, timeout=10.0)
#                     if w.content == user_data_w[str(ctx.author.id)]:
#                         await ctx.send("모든 정보 초기화가 완료되었습니다.")
#                         user_data_w[str(ctx.author.id)] = "없음"
#                         user_data_l[str(ctx.author.id)] = 1
#                         user_data_e[str(ctx.author.id)] = 0
#                         w_str[str(ctx.author.id)] = 20
#                     else:
#                         await ctx.send(ctx.message.author.mention + " 무기 이름이 일치하지 않습니다.")
#                 except asyncio.TimeoutError:
#                     await ctx.send(ctx.message.author.mention + " 시간이 초과되었습니다.")
#             else:
#                 await ctx.send(ctx.message.author.mention + " 초기화가 취소되었습니다.")
#         except asyncio.TimeoutError:
#             await ctx.send(ctx.message.author.mention + " 시간이 초과되었습니다.")
#     with open("user_data_weapon.bin", "wb") as f:
#         pickle.dump(user_data_w, f)
#     with open("user_data_level.bin", "wb") as f:
#         pickle.dump(user_data_l, f)
#     with open("user_data_exp.bin", "wb") as f:
#         pickle.dump(user_data_e, f)
#     with open("w_str.bin", "wb") as f:
#         pickle.dump(w_str, f)


@bot.command()
async def 두더지잡기(ctx):
    with open("user_data_level.bin", "rb") as f:
        user_data_l = pickle.load(f)
    with open("user_data_exp.bin", "rb") as f:
        user_data_e = pickle.load(f)
    if str(ctx.author.id) not in user_data_l:
        await ctx.send(ctx.message.author.mention + "님은 아직 등록하지 않으셨습니다. $등록을 통해 등록해주세요.")
    else:
        embed = discord.Embed(title="두더지잡기", description="시작하시려면 👍을 눌러주세요. (취소 : 👎)", color=0xB55E0D)
        embed.add_field(name="게임방법", value="10개의 구멍중 한 곳에서 두더지가 튀어나왔다가 다시 들어갑니다. 두더지가 있던 구멍을 잘 기억해서 입력해주세요!",
                        inline=False)
        msg = await ctx.send(embed=embed)
        r_list = ['👍', '👎']
        for r in r_list:
            await msg.add_reaction(r)

        def check(reaction, user):
            return str(reaction) in r_list and user == ctx.author and reaction.message.id == msg.id

        try:
            reaction, user = await bot.wait_for("reaction_add", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send("시간이 초과되었습니다.")
        else:
            if str(reaction) == '👍':
                game_f = ["O O O O O O O O O O", "🌚 O O O O O O O O O", "O 🌚 O O O O O O O O",
                          "O O 🌚 O O O O O O O", "O O O 🌚 O O O O O O", "O O O O 🌚 O O O O O",
                          "O O O O O 🌚 O O O O",
                          "O O O O O O 🌚 O O O", "O O O O O O O 🌚 O O", "O O O O O O O O 🌚 O",
                          "O O O O O O O O O 🌚"]

                embed = discord.Embed(title=game_f[0], color=0xB55E0D)
                msg = await ctx.send(embed=embed)
                msg2 = await ctx.send("3초 후에 두더지가 등장합니다!")
                await asyncio.sleep(1.0)
                await msg2.edit(content="2초 후에 두더지가 등장합니다!")
                await asyncio.sleep(1.0)
                await msg2.edit(content="1초 후에 두더지가 등장합니다!")
                await asyncio.sleep(1.0)
                await msg2.edit(content="두더지가 등장합니다!")
                t = random.randint(1, 3)
                f = random.randint(1, 10)
                await asyncio.sleep(t)
                embed2 = discord.Embed(title=game_f[f], color=0xB55E0D)
                await msg.edit(embed=embed2)
                await asyncio.sleep(0.07)
                await msg.edit(embed=embed)
                await msg2.edit(content=ctx.message.author.mention + " 두더지는 몇 번째 구멍에서 나왔을까요? (3초 안에 입력해주세요.)")

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                try:
                    hole = await bot.wait_for('message', check=check, timeout=3.0)
                    if hole.content == str(f):
                        await ctx.send(ctx.message.author.mention + " 두더지를 잡는데 성공하셨습니다! 경험치 3을 얻었습니다.")
                        user_data_e[str(ctx.author.id)] += 3
                        with open("user_data_exp.bin", "wb") as f:
                            pickle.dump(user_data_e, f)
                        if user_data_e[str(ctx.author.id)] >= user_data_e[str(ctx.author.id)] ** 2 * 50:
                            await ctx.send(ctx.message.author.mention + " 레벨업!")
                            user_data_l[str(ctx.author.id)] += 1
                            user_data_e[str(ctx.author.id)] = user_data_e[str(ctx.author.id)] - user_data_e[
                                str(ctx.author.id)] ** 2 * 50
                            with open("user_data_exp.bin", "wb") as f:
                                pickle.dump(user_data_e, f)
                            with open("user_data_level.bin", "wb") as f:
                                pickle.dump(user_data_e, f)
                        else:
                            pass

                    else:
                        await ctx.send(
                            ctx.message.author.mention + " 두더지를 잡는데 실패하셨습니다! 두더지는 " + str(f) + "번째 구멍에서 나왔었습니다!")
                except asyncio.TimeoutError:
                    await ctx.send(ctx.message.author.mention + " 시간초과! 두더지는 " + str(f) + "번째 구멍에서 나왔었습니다!")
            else:
                await ctx.send("취소되었습니다.")

@bot.command()
async def 키보드워리어(ctx):
    with open("user_data_level.bin", "rb") as f:
        user_data_l = pickle.load(f)
    with open("user_data_exp.bin", "rb") as f:
        user_data_e = pickle.load(f)

    if str(ctx.author.id) not in user_data_l:
        await ctx.send(ctx.message.author.mention + "님은 아직 등록하지 않으셨습니다.")

    else:
        embed = discord.Embed(title="키보드워리어", description="시작하시려면 👍을 눌러주세요. (취소 : 👎)", color=0xB55E0D)
        embed.add_field(name="게임방법", value=None, inline=False)
        msg = await ctx.send(embed=embed)
        r_list = ['👍', '👎']
        for r in r_list:
            await msg.add_reaction(r)

        def check(reaction, user):
            return str(reaction) in r_list and user == ctx.author and reaction.message.id == msg.id

        def check2(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            reaction, user = await bot.wait_for("reaction_add", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send("시간이 초과되었습니다.")
        else:
            if str(reaction) == '👍':
                await ctx.send("어떤 난이도로 설정하시겠습니까? (1.쉬움, 2.보통, 3.어려움)")
                try:

                    lev = await bot.wait_for('message', check=check2, timeout=10.0)
                    if lev.content == str(1) or lev.content == "쉬움":
                        embed = discord.Embed(title="키보드워리어", description="잠시 후 적군이 몰려옵니다!", color=0x000000)
                        game = await ctx.send(embed=embed)
                        await asyncio.sleep(3.0)
                        for i in range(0, 10):
                            enemy = None
                            enemy = kg(1)
                            embed2 = discord.Embed(title="키보드워리어", description=enemy, color=0x000000)
                            embed3 = discord.Embed(title="키보드워리어", description="처치 성공!", color=0x000000)
                            embed4 = discord.Embed(title="키보드워리어", description="처치 실패!", color=0x000000)
                            embed5 = discord.Embed(title="키보드워리어", description="시간 초과!", color=0x000000)
                            await game.edit(embed=embed2)
                            try:
                                e_name = await bot.wait_for('message', check=check2, timeout=3.0)
                                if enemy == e_name.content:
                                    await game.edit(embed=embed3)
                                    await e_name.delete()
                                    await asyncio.sleep(0.3)
                                    continue
                                else:
                                    await game.edit(embed=embed4)
                                    await e_name.delete()
                                    break
                            except asyncio.TimeoutError:
                                await game.edit(embed=embed5)
                                break
                        await ctx.send(ctx.message.author.mention + " 게임이 종료되었습니다!")
#####################################보통#####################################
                    elif lev.content == str(2) or lev.content == "보통":
                        embed = discord.Embed(title="키보드워리어", description="잠시 후 적군이 몰려옵니다!", color=0x000000)
                        game = await ctx.send(embed=embed)
                        await asyncio.sleep(3.0)
                        for i in range(0, 15):
                            enemy = None
                            enemy = kg(2)
                            embed2 = discord.Embed(title="키보드워리어", description=enemy, color=0x000000)
                            embed3 = discord.Embed(title="키보드워리어", description="처치 성공!", color=0x000000)
                            embed4 = discord.Embed(title="키보드워리어", description="처치 실패!", color=0x000000)
                            embed5 = discord.Embed(title="키보드워리어", description="시간 초과!", color=0x000000)
                            await game.edit(embed=embed2)
                            try:
                                e_name = await bot.wait_for('message', check=check2, timeout=3.0)
                                if enemy == e_name.content:
                                    await game.edit(embed=embed3)
                                    await e_name.delete()
                                    await asyncio.sleep(0.3)
                                    continue
                                else:
                                    await game.edit(embed=embed4)
                                    await e_name.delete()

                                    break
                            except asyncio.TimeoutError:
                                await game.edit(embed=embed5)

                                break
                        await ctx.send(ctx.message.author.mention + " 게임이 종료되었습니다!")
#####################################어려움#####################################
                    elif lev.content == str(3) or lev.content == "어려움":
                        await ctx.send("준비중")
                        # embed = discord.Embed(title="키보드워리어", description="잠시 후 적군이 몰려옵니다!", color=0x000000)
                        # game = await ctx.send(embed=embed)
                        # await asyncio.sleep(3.0)
                        # for i in range(0, 15):
                        #     enemy = None
                        #     enemy = kg(3)
                        #     embed2 = discord.Embed(title="키보드워리어", description=enemy, color=0x000000)
                        #     embed3 = discord.Embed(title="키보드워리어", description="처치 성공!", color=0x000000)
                        #     embed4 = discord.Embed(title="키보드워리어", description="처치 실패!", color=0x000000)
                        #     embed5 = discord.Embed(title="키보드워리어", description="시간 초과!", color=0x000000)
                        #     await game.edit(embed=embed2)
                        #     try:
                        #         e_name = await bot.wait_for('message', check=check2, timeout=2.0)
                        #         if enemy == e_name.content:
                        #             await game.edit(embed=embed3)
                        #             await e_name.delete()
                        #             await asyncio.sleep(0.5)
                        #             continue
                        #         else:
                        #             await game.edit(embed=embed4)
                        #             await e_name.delete()
                        #
                        #             break
                        #     except asyncio.TimeoutError:
                        #         await game.edit(embed=embed5)
                        #
                        #         break
                        # await ctx.send(ctx.message.author.mention + " 게임이 종료되었습니다!")


                except asyncio.TimeoutError:
                    await ctx.send("시간이 초과되었습니다.")
access_token = os.environ["BOT_TOKEN"]
bot.run(access_token)
