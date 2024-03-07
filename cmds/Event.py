import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import os
import functions.get_jdata as getj

MODE = 1

jdata = getj.get_jdata(MODE)

class Event(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)
	
	@commands.Cog.listener()
	async def on_member_join(self, member):
		channel = self.bot.get_channel(int(jdata['welcome_channel_id']))
		print(f'{member}! 歡迎你的加入!')
		await channel.send(f'{member}! 歡迎你的加入!')

	@commands.Cog.listener()
	async def on_member_leave(self,member):
		channel = self.bot.get_channel(int(jdata['leave_channel_id']))
		print(f'{member}! 希望你會永遠記得我們!')
		await channel.send(f'{member}! 希望你會永遠記得我們!')

	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.content.startswith('!!'):
			await msg.delete()
			await msg.channel.send("現在指令前綴已經更改為\\，請將原本的!!改成\\後再試一次")
		elif 'ji394su3' in msg.content:
			await msg.delete()
			await msg.channel.send("我愛你")

async def setup(bot):
	await bot.add_cog(Event(bot))