import discord, datetime, time
from discord.ext import commands
import asyncio
from urllib import request
import time
import random
import pickle
import warnings
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
import re
import asyncio
import discord 
import bs4
import urllib
import re
import requests
from discord.ext import commands
import os
import time
import random
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
import json
from urllib import request
import bs4
import urllib
import re
import requests
import lxml
from discord.ext import commands
import os
import time
import random
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
import json
from urllib import request
import platform
import psutil
from Tools.func import can_use, sendEmbed, getdata, writedata, getnow, warn
from Tools.var import embedcolor, mainprefix
from random import randint
import pickle
from datetime import datetime
from os.path import isfile, isdir
from os import makedirs





embedcolor = 0xffff33
embederrorcolor = 0xff0000
start_time = time.time()

class Test(commands.Cog, name="관리자"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 팀포(self, ctx):
        await ctx.trigger_typing()

        randomNum = random.randrange(1, 4)
        if randomNum == 1:
            embed = discord.Embed(description="응 갓겜 망겜이라하면 니얼굴 검바~!")
            await ctx.send(embed=embed)
        if randomNum == 2:
            embed = discord.Embed(description="니 리펙스~! (리펙스면 좋은점 디도스, 코딩 할수있음)")
            await ctx.send(embed=embed)
        if randomNum == 3:
            embed = discord.Embed(description="응 갓겜 망겜 소리 없음 ㅅㄱ 망겜이라고 하면 니얼굴 한국~!")
            await ctx.send(embed=embed)

    



   

def setup(bot):
    bot.add_cog(Test(bot))