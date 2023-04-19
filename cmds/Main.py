from core.classes import Cog_Extension
import discord
from discord.ext import commands
import json

class Main(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)
	
	@commands.command(name="ping", alienses=["pinglagecy"], help="顯示延遲毫秒數")
	async def pinglatency(self, ctx):
		await ctx.send(f'{round(self.bot.latency*1000)} (ms)')

	@commands.command()
	async def picture(self, ctx):
		pic = discord.File()
		await ctx.send(pic)

	@commands.command()
	async def test(self, ctx):
		await ctx.send(ctx.message.channel)

async def setup(bot):
	await bot.add_cog(Main(bot))