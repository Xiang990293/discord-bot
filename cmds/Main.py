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

	@commands.command(name="synccmd", alienses=["synccommands"], help="同步斜線指令")
	@commands.has_permissions(administrator=True)
	async def synccommands(ctx):
		await bot.tree.sync()
		await ctx.send("同步完成")
	
	@commands.hybrid_command(name="ping", alienses=["pinglagecy"], help="顯示延遲毫秒數")
	async def pinglatency(self, ctx):
		await ctx.message.delete()
		await ctx.send(f'{round(self.bot.latency*1000*100)/100} (ms)', delete_after=30.0)

	@commands.hybrid_command()
	async def picture(self, ctx, *arg):
		if arg == ():
			await ctx.message.delete()
			await ctx.send(file=discord.File("NoURL.png"))
		else:
			await ctx.message.delete()
			pic = arg[0]
			await ctx.send(pic)

	@commands.hybrid_command()
	async def test(self, ctx):
		await ctx.message.delete()
		await ctx.send(f"{ctx.message.channel}, I am here!")

	@commands.hybrid_command(name="delete", aliases=["del", "clc"], help="刪除特定數量的訊息，默認為 1 個")
	async def delete(self, ctx, arg: int):
		await ctx.message.delete()
		await ctx.channel.purge(limit=arg)

	# @commands.hybrid_command(name="change_version", aliases=["version", "cver"], help="更改顯示版本")
	# async def change_version(self, ctx, arg):
	# 	await ctx.message.delete()

async def setup(bot):
	await bot.add_cog(Main(bot))