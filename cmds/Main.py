from core.classes import Cog_Extension
import discord
from discord.ext import commands
import json
import os
from PIL import Image
import functions.get_jdata as getj

MODE = 1

jdata = getj.get_jdata(MODE)

class Main(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)
	
	@commands.hybrid_command(name="ping", alienses=["pinglagecy"], with_app_command=True, help="顯示延遲毫秒數")
	async def pinglatency(self, ctx):
		await ctx.send(f'{round(self.bot.latency*1000*100)/100} (ms)', delete_after=30.0)

	@commands.hybrid_command(name="picture", with_app_command=True, help="將圖片url顯示出來")
	async def picture(self, ctx, url: str):
		if url=="":
			await ctx.send(file=discord.File("NoURL.png"))
		else:
			await ctx.send(url)

	@commands.hybrid_command(name="test", with_app_command=True, help="機器人精神測試")
	async def test(self, ctx):
		await ctx.send(f"{ctx.message.channel}, I am here!")

	@commands.hybrid_command(name="delete", aliases=["del", "clc"], with_app_command=True, help="刪除特定數量的訊息，默認為 1 個")
	async def delete(self, ctx, arg: int):
		await ctx.channel.purge(limit=arg)

	# @commands.hybrid_command(name="change_version", aliases=["version", "cver"], help="更改顯示版本")
	# async def change_version(self, ctx, arg):
	# 	await ctx.message.delete()

async def setup(bot):
	await bot.add_cog(Main(bot))