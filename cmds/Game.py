import discord
from discord.ext import commands
from core.classes import Cog_Extension
import random
import math

class Game(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)

	@commands.command(name='roll_dice', aliases=['dice','roll'], help="擲顆骰子，接受兩個數字：次數 面數")
	async def roll_dice(self, ctx, *args):
		await ctx.message.delete()

		def dice(face):
			if type(face)!=type(100):
				return -1
			rand = random.random()
			rand *= face
			rand = math.floor(rand) + 1
			return rand

		if args == ():
			await ctx.send(f"你擲了 1 個 6 面骰\n點數是 {dice(6)}")
			return
		
		(times, face) = args
		times = int(times)
		face = int(face)
		
		if type(times) != type(100):
			await ctx.send("次數輸入錯誤，請輸入整數")

		if type(face) != type(100):
			await ctx.send("面數輸入錯誤，請輸入整數")

		result = [dice(face) for i in range(times)]

		await ctx.send(f"你擲了 {times} 個 {face} 面骰\n點數是 {result}")
		
		
async def setup(bot):
	await bot.add_cog(Game(bot))