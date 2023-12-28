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
	
	@commands.command(name="ping", alienses=["pinglagecy"], help="顯示延遲毫秒數")
	async def pinglatency(self, ctx):
		await ctx.message.delete()
		await ctx.send(f'{round(self.bot.latency*1000*100)/100} (ms)', delete_after=30.0)

	@commands.command()
	async def picture(self, ctx, *arg):
		if arg == ():
			await ctx.message.delete()
			await ctx.send(file=discord.File("NoURL.png"))
		else:
			await ctx.message.delete()
			pic = arg[0]
			await ctx.send(pic)

	@commands.command()
	async def test(self, ctx):
		await ctx.message.delete()
		await ctx.send(f"{ctx.message.channel}, I am here!")

	@commands.command(name="delete", aliases=["del", "clc"], help="刪除特定數量的訊息，默認為 1 個")
	async def delete(self, ctx, arg):
		await ctx.message.delete()
		try:
			arg = int(arg)
			await ctx.channel.purge(limit=arg)
		except TypeError:
			await ctx.send(f"參數錯誤: {arg}，必須是正整數")
		except ValueError:
			await ctx.send(f"參數錯誤: {arg}，必須是正整數")

	@commands.command(name="change_version", aliases=["version", "cver"], help="更改顯示版本")
	async def change_version(self, ctx, arg):
		await ctx.message.delete()

async def setup(bot):
	await bot.add_cog(Main(bot))