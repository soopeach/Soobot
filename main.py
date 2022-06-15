import asyncio
import random
from data import Token # 토큰 값을 가져옴.
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='$') # 명령어의 시작이 $ / ex) $안녕
global timer
timer = {}

global rockPaperScissors
rockPaperScissors = ["가위","바위","보"]




@bot.event
async def on_ready():
    print(f'{bot.user.name}이 연결되었습니다.')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.event
async def on_command_error(ctx, error):
    if(isinstance(error, commands.CommandNotFound)):
        await ctx.send("해당 명령어는 존재하지 않습니다")

@bot.command(aliases=['hello','인사'])
async def 안녕(ctx):
    await ctx.send("{}아, 안녕".format(ctx.author.mention))
    # if(ctx.author.mention == "<@424218532922916895>") :
    #     await ctx.send("{}아, 안녕".format(ctx.author.mention))
    #     print(f'{ctx.author.mention} 은 멘션 {ctx.author}은 그냥')
    # else :
    #     await ctx.send("{}아, 꺼져".format(ctx.author.mention))

@bot.command(aliases=['저녁'])
async def 저녁골라줘(ctx, *args):
    await ctx.send(f"저녁은 {args[random.randrange(0, len(args))]} 드세용~!")

@bot.command()
async def 따라하기(ctx,*,text):
    await ctx.send(text)

@bot.command()
async def 송인준(ctx):
    await ctx.send("송인준은 브론즈가 딱이야!")

@bot.command()
async def 명령어(ctx):
    embed = discord.Embed(title="명령어 종류 <== 사용 예시 보기",url="https://github.com/soopeach/sooBot", description="명령어의 종류는 아래와 같습니다.", color=0x0aa40f)
    embed.add_field(name="따라하기", value="입력 받은 텍스트를 봇이 따라합니다.\n", inline=False)
    embed.add_field(name="저녁골라줘 / 저녁", value="저녁이 고민될 땐? 저녁골라줘를 사용해보세요.\n", inline=False)
    embed.add_field(name="안녕 / 인사 / hello", value="봇이 인사해줍니다.\n", inline=False)
    embed.add_field(name="가위바위보", value="봇과 가위바위보를 할 수 있습니다.\n", inline=False)
    embed.add_field(name="공부시간측정", value="사용자의 공부시간을 측정합니다.\n", inline=False)
    embed.set_footer(text="현재 Soobot의 기능은 위와 같습니다.\n")
    await ctx.send(embed=embed)

@bot.command()
async def 공부시간측정(ctx, *, user):
    global timer

    if user in timer and timer[user] != -1:
        await ctx.send(timeConverter(user, timer[user]))
        timer[user] = -1
        # print('종료')
    else :
        timer[user] = 0
        await ctx.send(f"{user}님의 공부시간을 측정하기 시작합니다.")
        # print(timer)
        while (timer[user] >= 0) :
            timer[user] += 1
            await asyncio.sleep(1)
            # print(timer[user])
            # if timer[user] % 10 == 0 :
            #     await ctx.send(f"축하합니다.{user}님 공부시작 {timer[user]}초 돌파")
            if timer[user] > 3600 * 24 :
                await ctx.send("1일이 경과하였습니다. 시간을 초기화하겠습니다.")
                timer[user] = -1

# 초를 보내면 시, 분, 초를 계산해줌.
def timeConverter(user, sec) :
    min = sec // 60
    hour = min // 60
    sec %= 60
    min %= 60

    # print(f'{user}님은 {hour}시간 {min}분 {sec}초 공부하셨습니다.')
    return f'{user}님은 {hour}시간 {min}분 {sec}초 공부하셨습니다.'

@bot.command()
async def 가위바위보(ctx,*,player):

    botThrow = rockPaperScissors[random.randrange(0,len(rockPaperScissors))]
    result = resultOfRockPaperScissors(player,botThrow)
    if result == "에러":
        content = "잘못된 형식입니다. {}님 가위, 바위, 보 중 하나를 내주세요!".format(ctx.author.mention)
    else : content = "제가 낸 것은 {}, {}님이 낸 것은 {}, {}.".format(botThrow, ctx.author.mention, player, result)
    await ctx.send(content)

def resultOfRockPaperScissors(player, botThrow) :
    win = "제가 이겼습니다"
    lose = "제가 졌습니다"
    #비겼을 때
    if player == botThrow :
        result = "비겼습니다"

    # 플레이어가 가위를 냈을 떼
    if player == "가위" :
        if botThrow == "바위":
            result = win
        if botThrow == "보":
            result = lose

    # 플레이어가 바위를 냈을 떼
    elif player == "바위" :
        if botThrow == "가위" :
            result = lose
        if botThrow == "보":
            result = win

    # 플레이어가 보를 냈을 떼
    elif player == "보" :
        if botThrow == "가위" :
            result = win
        if botThrow == "바위":
            result = lose
    else :
        result = "에러"
    return result

bot.run(Token)




