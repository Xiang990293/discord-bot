from core.classes import Cog_Extension
import discord
from discord.ext import commands
import json
import os
from PIL import Image

class Main(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)
	
	@commands.command(name="ping", alienses=["pinglagecy"], help="顯示延遲毫秒數")
	async def pinglatency(self, ctx):
		await ctx.send(f'{round(self.bot.latency*1000)} (ms)')

	@commands.command()
	async def picture(self, ctx, *arg):
		if arg == ():
			await ctx.send(file=discord.File("NoURL.png"))
		else:
			pic = arg[0]
			await ctx.send(pic)

	@commands.command()
	async def test(self, ctx):
		await ctx.send(f"{ctx.message.channel}, I am here!")

async def setup(bot):
	await bot.add_cog(Main(bot))