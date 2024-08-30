import discord
from discord.ext import commands
from discord import app_commands
from core.classes import Cog_Extension
import random
import math

class Game(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)
	
	@commands.hybrid_command(name='roll_dice', aliases=['dice','roll'], with_app_command=True, help="擲顆骰子，接受兩個數字：次數 面數")
	async def roll_dice(self, ctx, input = "1d6"):
		"""擲骰子，接受兩個數字斯n m，或骰子記號ndm"""
		def dice(face):
			rand = random.random()
			rand *= face
			rand = math.floor(rand) + 1
			return rand
		
		def roll_dice_multiple(times, face):
			if times == 1: return dice(face)
			return [dice(face) for i in range(times)]

		times, face = 1, 6

		if "d" in input:
			try:
				[times,face] = input.split(sep="d")
				[times,face] = [int(times),int(face)]
				
			except Exception as e:
				await ctx.send(f"骰子格式錯誤：{e}")
				return
		else:
			parts = input.split()
			if len(parts) != 2 or input!="":
				await ctx.send(f"骰子格式錯誤：{e}")
				return

			times, face = parts
			times, face = [int(times),int(face)]

		result = roll_dice_multiple(times, face)
		await ctx.send(f"你擲了 {times} 個 {face} 面骰\n點數是 {result}")
		
		
async def setup(bot):
	await bot.add_cog(Game(bot))