import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import os

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(int(jdata['leave_channel_id']))
        print(f'{member}! 歡迎你的加入!')
        await channel.send(f'{member}! 歡迎你的加入!')

    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(int(jdata['welcome_channel_id']))
        print(f'{member}! 希望你會永遠記得我們!')
        await channel.send(f'{member}! 希望你會永遠記得我們!')

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == 'people':
            await msg.channel.send("hi")

def setup(bot):
    bot.add_cog(Event(bot))