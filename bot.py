from ssl import Options
import discord
from discord import message
from discord.enums import _is_descriptor
from discord.ext import commands
import asyncio
import datetime
import random
import time
import sys
import json
import os
import discord as d
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import aiohttp
from captcha.image import ImageCaptcha
from discord.ext.commands import has_permissions, MissingPermissions
from youtube_search import YoutubeSearch
import youtube_dl
from random import choice
import math
import aiosqlite
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
from pafy import new
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from fast_youtube_search import search_youtube
from Tools.var import prefix, embedcolor, mainprefix, version
from Tools.func import warn, errorlog, is_owner
from urllib.request import Request, urlopen
import re
import aiofiles
from bs4 import BeautifulSoup
import lxml
from youtube_dl import YoutubeDL
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio






db = sqlite3.connect("Money.db")
db_cur = db.cursor()

alarm_time = '23:33'#24hrs
channel_id = '817329494700458015'




bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.multiplier = 1
bot.welcome_channels = {}
bot.goodbye_channels = {}
user = []
musictitle = []
song_queue = []
musicnow = []

userF = []
userFlist = []
allplaylist = []

def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    chromedriver_dir = r"C:\python bot\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir, options = options)
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    
    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()
    
    return music, URL

def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx)) 

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))




url = "https://discord.com/api/webhooks/817329524889878558/bWmeDAR0ugmy9k1NvVpxnxkenuwuyycdKlJjUmLvtgM7J-NwwyGDSl1yL9gadozTJa8q" #webhook url, from here: https://i.imgur.com/f9XnAew.png


data = {
    "image" : "https://ibb.co/9nGRJFJ",
    "username" : "작동로그"
}

data["embeds"] = [
    {
        "description" : "봇이 작동되었습니다.",
        "title" : "작동로그",
    }
]

result = requests.post(url, json = data)

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print("Payload delivered successfully, code {}.".format(result.status_code))

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'downloads': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.id = data.get('id')
        self.uploader = data.get('uploader')
        self.uploaderid = data.get('uploader_id')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



@bot.event
async def on_ready():
    user = len(bot.users)
    server = len(bot.guilds)
    message = ["ㅌ도움을 쳐보세요!",  str(user) + "유저와 함께해요!", str(server) + "개의 서버에 알파프리베이트가 같이운영해요!"]
    while True:
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(message[0]))
            message.append(message.pop(0))
            await asyncio.sleep(4)

    for file in ["welcome_channels.txt", "goodbye_channels.txt"]:
        async with aiofiles.open(file, mode="a") as temp:
            pass
        
    async with aiofiles.open("welcome_channels.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.welcome_channels[int(data[0])] = (int(data[1]), " ".join(data[2:]).strip("\n"))

    async with aiofiles.open("goodbye_channels.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.goodbye_channels[int(data[0])] = (int(data[1]), " ".join(data[2:]).strip("\n"))
       

    

@bot.event
async def on_member_join(member):
    for guild_id in bot.welcome_channels:
        if guild_id == member.guild.id:
            channel_id, message = bot.welcome_channels[guild_id]
            await bot.get_guild(guild_id).get_channel(channel_id).send(f"{member.mention}님 {message}")
            return

@bot.event
async def on_member_remove(member):
    for guild_id in bot.goodbye_channels:
        if guild_id == member.guild.id:
            channel_id, message = bot.goodbye_channels[guild_id]
            await bot.get_guild(guild_id).get_channel(channel_id).send(f"{member.mention}님 {message}")
            return

@bot.command()
async def 입장채널(ctx, new_channel: discord.TextChannel=None, *, message=None):
    if new_channel != None and message != None:
        for channel in ctx.guild.channels:
            if channel == new_channel:
                bot.welcome_channels[ctx.guild.id] = (channel.id, message)
                await ctx.channel.send(f"환영 메세지를 {channel.name}에 보내고 {message}라고 보낼게요!")
                await channel.send("새로운 환영 채널입니다!")
                
                async with aiofiles.open("welcome_channels.txt", mode="a") as file:
                    await file.write(f"{ctx.guild.id} {new_channel.id} {message}\n")

                return

        await ctx.channel.send("주어진 채널을 찾을 수 없습니다.")

    else:
        await ctx.channel.send("환영 채널의 이름이나 환영 메시지를 포함하지 않았습니다.")


@bot.command()
async def 퇴장채널(ctx, new_channel: discord.TextChannel=None, *, message=None):
    if new_channel != None and message != None:
        for channel in ctx.guild.channels:
            if channel == new_channel:
                bot.goodbye_channels[ctx.guild.id] = (channel.id, message)
                await ctx.channel.send(f"퇴장 메세지를 {channel.name}에 보내고 {message}라고 보낼게요!")
                await channel.send("새로운 퇴장 채널입니다!")
                
                async with aiofiles.open("goodbye_channels.txt", mode="a") as file:
                    await file.write(f"{ctx.guild.id} {new_channel.id} {message}\n")

                return

        await ctx.channel.send("주어진 채널을 찾을 수 없습니다.")

    else:
        await ctx.channel.send("작별 채널의 이름이나 작별 메시지를 포함하지 않았습니다.")



@bot.command() 
async def 안녕(ctx):
	await ctx.send("그래 안녕!")



@bot.command(aliases=['청소'])
@commands.has_permissions(administrator=True)
async def clear(ctx, l: int = 50):
   c = await ctx.channel.purge(limit=l)
   await ctx.send(f"`{len(c)}` 개의 메세지를 삭제했습니다.", delete_after=3)
   





@bot.command()
async def 밴(ctx, user: discord.User):
	guild = ctx.guild
	mbed = discord.Embed(
		title = '처리 완료',
		description = f"{user}님이 밴을 당하셨어요!"
	)
	if ctx.author.guild_permissions.ban_members:
		await ctx.send(embed=mbed)
		await guild.ban(user=user)

@bot.command()
async def 언밴(ctx, user: discord.User):
	guild = ctx.guild
	mbed = discord.Embed(
		title = '처리완료',
		description = f"{user}님을 언밴 했어요!"
	)
	if ctx.author.guild_permissions.ban_members:
		await ctx.send(embed=mbed)
		await guild.unban(user=user)

@bot.command()
@commands.has_permissions(kick_members=True)
async def 킥(ctx, member:discord.Member):
    await member.kick()
    await ctx.send(f"{member.name}님을 킥했습니다.")

@bot.command(name="뮤트")
@commands.has_permissions(manage_messages=True)
async def mute(ctx , member: discord.Member, *, reason=None):
	guild = ctx.guild
	mutedRole = discord.utils.get(guild.roles, name="Muted")

	if not mutedRole:
		mutedRole = await guild.create_role(name="Muted")

		for channel in guild.channels:
			await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

	await member.add_roles(mutedRole, reason=reason)
	await ctx.send(f"뮤트 {member.mention} 사유: {reason}으로 뮤트를 먹으셨습니다.")
	await member.send(f"뮤트 {member.mention} 사유: {reason}으로 뮤트를 먹으셨습니다.")


@bot.command(name="언뮤트")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

	
			

	await member.remove_roles(mutedRole)
	await ctx.send(f"언뮤트 {member.mention}님이 언뮤트를 당하셨습니다.")
	await member.send(f"언뮤트 {member.mention}님이  언뮤트를 당하셨습니다.")






 
@bot.command(aliases = ['세이','메세지'])
async def say(ctx,*,message):
    await ctx.message.delete()
    emb=discord.Embed(description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    

                 
@bot.command()
@commands.has_role("💎AC ▪ MASTER💎")
async def 경품(ctx, mins : int, * , prize: str):
	embed = discord.Embed(title = "상품!", description = f"{prize}", color = ctx.author.color)

	end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60)

	embed.add_field(name = "종료 시간:", value = f"{end} UTC")
	embed.set_footer(text = f"지금부터 {mins}분 후 Emds")

	my_msg = await ctx.send(embed = embed)

	await my_msg.add_reaction("🎉")

@bot.command()
async def 리로드(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded extension: {extension}.")

@bot.command()
async def 언로드(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded extension: {extension}.")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command(aliases = ['ㅊㄴㅈㄱ'])
async def 채널제거(ctx, channel: d.TextChannel):
	mbed = d.Embed(
		title = '완료!',
		description = f'{channel}이라는 채널을 삭제했습니다.',
	)
	if ctx.author.guild_permissions.manage_channels:
		await ctx.send(embed=mbed)
		await channel.delete()


@bot.command(aliases = ['ㅊㄴㅅㅅ'])
async def 채널생성(ctx, channelName):
	guild = ctx.guild

	mbed = d.Embed(
		title = '완료!',
		description = "{}이라는 채널을 성공적으로 생성되었습니다.".format(channelName)
	)
	if ctx.author.guild_permissions.manage_channels:
		await guild.create_text_channel(name='{}'.format(channelName))
		await ctx.send(embed=mbed)
		
		
@bot.command(aliases = ['ㄸㄹㅎ'])
async def 따라해(ctx, *, text):
    await ctx.send(text)



@bot.command(pass_context=True)
async def 역할부여(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{user.name}님한테 **{role.name}**역할을 추가했어요!")

@bot.command(pass_context=True)
async def 역할제거(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"{user.name}님한테 **{role.name}**역할을 제거했어요!")

@bot.command()
async def 유튜브(ctx):
    embed = discord.Embed(colour=0x95efcc, title=f"알파캡틴유튜브")
    await ctx.send(embed=embed)
    await ctx.send('https://www.youtube.com/user/cho090501')
    
@bot.command()
async def 레일건사기템존(ctx):
    embed=discord.Embed(title='이거 눌러보셈 ㅋㅋㅋㅋㅋㅋㅋ', description = "레일건 사기템존님은?\n잼민티 내고 이상하고 병신임 이거 이욕해도됌 제목눌러보셈", color = 0xff0000, url = "https://www.youtube.com/watch?v=K51gdMm3wWM")
    embed.set_footer(text = "와 니애미 욕은 해도됌 이사람한테는 (?)")
#출처: https://tercomgame.tistory.com/138 [단순한.]
    await ctx.send(embed=embed)


@bot.command()
async def 도움(ctx):
        embed = discord.Embed(title="관리자 명령어", color=0x20ff05)
        embed.add_field(name="ㅌ도움1", value="관리자 도움말", inline=False) 
        embed.add_field(name="ㅌ도움2", value="유저 도움말", inline=False)
        embed.add_field(name="ㅌ도움3", value="게임 도움말", inline=False) 
        embed.add_field(name="ㅌ도움4", value="뮤직 도움말", inline=False)
        await ctx.send(embed=embed)



@bot.command()
async def 도움1(ctx):
        embed = discord.Embed(title="관리자 명령어", color=0x20ff05)
        embed.add_field(name="관리자 명령어", value="`ㅌ밴` `ㅌ언밴` `ㅌ뮤트` `ㅌ언뮤트` `ㅌ청소` `ㅌ역할부여` `ㅌ역할제거` `ㅌ입장채널 #채널이름 (들어오면 할말)` `ㅌ퇴장채널 #채널이름 (들어오면 할말)`", inline=False) 
        await ctx.send(embed=embed)

@bot.command()
async def 도움2(ctx):
        embed = discord.Embed(title="유저 명령어", color=0x20ff05)
        embed.add_field(name="유저명령어", value="`ㅌ시간` `ㅌ서버정보` `ㅌ유저정보` `ㅌ따라해` `ㅌ한일번역` `한영번역` `ㅌ영한번역` `ㅌ일한번역` `ㅌ날씨` `ㅌ실검` `ㅌ노래순위` `ㅌ검색` `ㅌ롤전적` `ㅌ레식전적`", inline=False) 
        await ctx.send(embed=embed)
   
@bot.command()
async def 도움4(ctx):
        embed = discord.Embed(title="뮤직 명령어", color=0x20ff05)
        embed.add_field(name="뮤직명령어", value=" `ㅌ재생 노래이름` `ㅌ들어와` `ㅌ나가` `ㅌ일시정지` `ㅌ다시재생` `ㅌ노래끄기` `ㅌ지금노래` `ㅌ멜론차트` `ㅌ대기열추가` `대기열삭제` `목록초기화` `목록` `목록재생` `ㅌ즐겨찾기` `ㅌ즐겨찾기추가` `ㅌ즐겨찾기삭제` ", inline=False) 
        await ctx.send(embed=embed)


@bot.command()
async def 마크서버(ctx, arg):
    r = requests.get('https://api.minehut.com/server/' + arg + '?byName=true')
    json_data = r.json()

    description = json_data["server"]["motd"]
    online = str(json_data["server"]["online"])
    playerCount = str(json_data["server"]["playerCount"])

    embed = discord.Embed(
        title=arg + " Server Info",
        description='서술: ' + description + '\온라인: ' + online + '\n플레이어: ' + playerCount,
        color=discord.Color.dark_green()
    )
    embed.set_thumbnail(url="https://i1.wp.com/www.craftycreations.net/wp-content/uploads/2019/08/Grass-Block-e1566147655539.png?fit=500%2C500&ssl=1")

    await ctx.send(embed=embed)




@bot.command()
async def 도움3(ctx):
    embed = discord.Embed(title="게임, 도박 도움말")
    embed.add_field(name="도박", value="`ㅌ출석` `ㅌ포인트` `송금` `ㅌ도박 (올인가능)` `ㅌ새총`", inline=False) 
    embed.set_footer(text="출처:https://github.com/sw08/Finix [제작자 sw08(민트초코)님]")
    await ctx.send(embed=embed)
   
@bot.command()
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await bot.fetch_user(user_id)
            await target.send(args)

            await ctx.channel.send("'" + args + "' dm전송이 완료되었습니다.: " + target.name)

        except:
            await ctx.channel.send("지정된 사용자한테 dm을(를)할 수 없습니다.")
        

    else:
        await ctx.channel.send("사용자 ID 및 / 또는 메시지를 제공하지 않았습니다.")
 




@bot.command()
async def 시간(ctx):
    await ctx.send(embed=discord.Embed(title="현재시간", timestamp=datetime.datetime.utcnow()))



    





@bot.command(name="검색")
async def s(ctx, *, search_query):
    temp = 0
    url_base = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="
    url = url_base + urllib.parse.quote(search_query)
    title = ["", "", "", ""]
    link = ["", "", "", ""]
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    result = soup.find_all('a', "api_txt_lines total_tit") #수정됨
    embed = discord.Embed(title="검색 결과", description=" ", color=0xf3bb76)
    for n in result:
        if temp == 4:
            break
        title[temp] = n.text #수정됨
        link[temp] = n.get("href")
        embed.add_field(name=title[temp], value=link[temp], inline=False)
        temp+=1
    embed.set_footer(text="네이버 블로그만 검색됩니다.")
    await ctx.send(embed=embed)




@bot.command()
async def 뽑기(ctx):
        await ctx.trigger_typing()
        randomNum = random.randrange(1, 3)
        if randomNum == 1:
            await ctx.send('당첨')
        if randomNum == 2:
            await ctx.send('꽝')



@bot.command()
async def 출근(ctx):
    timestamp=datetime.datetime.utcnow
    await ctx.send(f"{ctx.author.mention}님이 출근합니다.")


@bot.command()
async def 퇴근(ctx):
    timestamp=datetime.datetime.utcnow
    await ctx.send(f"{ctx.author.mention}님이 퇴근합니다. ")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandOnCooldown):
        await warn(ctx=ctx, content=f"쿨타임이 발생했어요 `{round(error.retry_after, 2)}`초 후에 다시시도해 주세요")
    elif isinstance(error, commands.CheckFailure):
        await warn(ctx=ctx, content='실행하실 조건이 충족 되지않음')
    elif isinstance(error, commands.BadArgument):
        await warn(ctx=ctx, content='올바른 값을 넣어 주세요.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await warn(ctx=ctx, content='값이 필요합니다...')
    elif isinstance(error, commands.MissingPermissions):
        await warn(ctx=ctx, content='권한이 없습니다...')
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif '403 Forbidden' in str(error):
        await warn(ctx=ctx, content='봇한테 권한을 제데로 주세요 ㅠㅠ')
    else:
        await errorlog(ctx=ctx, error=error, bot=bot)

@bot.command()
async def 검바(ctx):
    await ctx.send(f'{ctx.author.mention}, ㅁㅗㅅㅅㅐㅇㄱㅣㄴ 검바')
    time.sleep(2)
    await ctx.send(f'{ctx.author.mention} 니얼굴 검바')




@bot.command()
async def 들어와(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send('음성 채널에 유저가 없습니다.')

@bot.command()
async def 나가(ctx):
        await vc.disconnect()
   

@bot.command()
async def 재생(ctx, *, msg):
    if not vc.is_playing():
        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = "C:\python bot\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir)
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        musicnow.insert(0, entireText)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: play_next(ctx))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없어요!")


@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = entireText + "을(를) 일시정지 했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
         await ctx.send("지금 노래가 재생되지 않네요.")
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = entireText  + "을(를) 다시 재생했습니다.", color = 0x00ff00))

@bot.command()
async def 노래끄기(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = entireText  + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@bot.command()
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금은 노래가 재생되지 않네요..")
    else:
        await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))

@bot.command()
async def 멜론차트(ctx):
    if not vc.is_playing():
        
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = r"C:\python bot\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query=멜론차트")
        source = driver.page_source
        bs = BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        musicnow.insert(0, entireText)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: play_next(ctx))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없어요!")

@bot.command()
async def 즐겨찾기(ctx):
    global Ftext
    Ftext = ""
    correct = 0
    global Flist
    for i in range(len(userF)):
        if userF[i] == str(ctx.message.author.name): #userF에 유저정보가 있는지 확인
            correct = 1 #있으면 넘김
    if correct == 0:
        userF.append(str(ctx.message.author.name)) #userF에다가 유저정보를 저장
        userFlist.append([]) #유저 노래 정보 첫번째에 유저이름을 저장하는 리스트를 만듬.
        userFlist[len(userFlist)-1].append(str(ctx.message.author.name))
        
    for i in range(len(userFlist)):
        if userFlist[i][0] == str(ctx.message.author.name):
            if len(userFlist[i]) >= 2: # 노래가 있다면
                for j in range(1, len(userFlist[i])):
                    Ftext = Ftext + "\n" + str(j) + ". " + str(userFlist[i][j])
                titlename = str(ctx.message.author.name) + "님의 즐겨찾기"
                embed = discord.Embed(title = titlename, description = Ftext.strip(), color = 0x00ff00)
                embed.add_field(name = "목록에 추가\U0001F4E5", value = "즐겨찾기에 모든 곡들을 목록에 추가합니다.", inline = False)
                embed.add_field(name = "플레이리스트로 추가\U0001F4DD", value = "즐겨찾기에 모든 곡들을 새로운 플레이리스트로 저장합니다.", inline = False)
                Flist = await ctx.send(embed = embed)
                await Flist.add_reaction("\U0001F4E5")
                await Flist.add_reaction("\U0001F4DD")
            else:
                await ctx.send("아직 등록하신 즐겨찾기가 없어요.")



@bot.command()
async def 즐겨찾기추가(ctx, *, msg):
    correct = 0
    for i in range(len(userF)):
        if userF[i] == str(ctx.message.author.name): #userF에 유저정보가 있는지 확인
            correct = 1 #있으면 넘김
    if correct == 0:
        userF.append(str(ctx.message.author.name)) #userF에다가 유저정보를 저장
        userFlist.append([]) #유저 노래 정보 첫번째에 유저이름을 저장하는 리스트를 만듦.
        userFlist[len(userFlist)-1].append(str(ctx.message.author.name))

    for i in range(len(userFlist)):
        if userFlist[i][0] == str(ctx.message.author.name):
            
            options = webdriver.ChromeOptions()
            options.add_argument("headless")

            chromedriver_dir = r"C:\python bot\chromedriver.exe"
            driver = webdriver.Chrome(chromedriver_dir, options = options)
            driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
            source = driver.page_source
            bs = BeautifulSoup(source, 'lxml')
            entire = bs.find_all('a', {'id': 'video-title'})
            entireNum = entire[0]
            music = entireNum.text.strip()

            driver.quit()

            userFlist[i].append(music)
            await ctx.send(music + "(이)가 정상적으로 등록되었어요!")



@bot.command()
async def 즐겨찾기삭제(ctx, *, number):
    correct = 0
    for i in range(len(userF)):
        if userF[i] == str(ctx.message.author.name): #userF에 유저정보가 있는지 확인
            correct = 1 #있으면 넘김
    if correct == 0:
        userF.append(str(ctx.message.author.name)) #userF에다가 유저정보를 저장
        userFlist.append([]) #유저 노래 정보 첫번째에 유저이름을 저장하는 리스트를 만듦.
        userFlist[len(userFlist)-1].append(str(ctx.message.author.name))

    for i in range(len(userFlist)):
        if userFlist[i][0] == str(ctx.message.author.name):
            if len(userFlist[i]) >= 2: # 노래가 있다면
                try:
                    del userFlist[i][int(number)]
                    await ctx.send("정상적으로 삭제되었습니다.")
                except:
                     await ctx.send("입력한 숫자가 잘못되었거나 즐겨찾기의 범위를 초과하였습니다.")
            else:
                await ctx.send("즐겨찾기에 노래가 없어서 지울 수 없어요!")

@bot.command()
async def 대기열추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + "를 재생목록에 추가했어요!")

@bot.command()
async def 대기열삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
            
        await ctx.send("대기열이 정상적으로 삭제되었습니다.")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없어 삭제할 수 없어요!")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수를 벗어났습니다!")
            else:
                await ctx.send("숫자를 입력해주세요!")

@bot.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "노래목록", description = Text.strip(), color = 0x00ff00))

@bot.command()
async def 목록초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(embed = discord.Embed(title= "목록초기화", description = """목록이 정상적으로 초기화되었습니다. 이제 노래를 등록해볼까요?""", color = 0x00ff00))
    except:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")

@bot.command()
async def 목록재생(ctx):

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(user) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not vc.is_playing():
            play(ctx)
        else:
            await ctx.send("노래가 이미 재생되고 있어요!")



bot.run(os.environ['token'])
bot.remove_command("help")
asyncio.run(bot.db.close())
