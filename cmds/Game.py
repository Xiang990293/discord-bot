import discord
from discord.ext import commands
from discord import app_commands
from core.classes import Cog_Extension
import random
import math

class Game(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)

	@commands.tree.hybrid_command(name='roll_dice', aliases=['dice','roll'], with_app_command=True, help="擲顆骰子，接受兩個數字：次數 面數")
	@app_commands.choices(name=[
		app_commands.Choice(name='Name 1', value=1),
		app_commands.Choice(name='Name 2', value=2)
	])
	@app_commands.choices(day=[
		app_commands.Choice(name='Monday', value=1),
		app_commands.Choice(name='Tuesday', value=2)
	])
	async def roll_dice(self, ctx, times = 1, face = 6, dice_expression = "1d6"):
		"""擲顆骰子，接受兩個數字：次數 面數"""
		def dice(face):
			rand = random.random()
			rand *= face
			rand = math.floor(rand) + 1
			return rand
		
		def roll_dice_multiple(times, face):
			if times == 1: return dice(face)
			return [dice(face) for i in range(times)]

		if times == 0: times = 1
		if face == 0: face = 6

		result = roll_dice_multiple(times, face)

		await ctx.send(f"你擲了 {times} 個 {face} 面骰\n點數是 {result}")
		(state,) = dice_expression
		if "d" in state:
			try:
				cut_pos = state.find("d")
				times = int(state[0:cut_pos])
				face = int(state[cut_pos+1:])
				result = roll_dice_multiple(times, face)

				await ctx.send(f"你擲了 {times} 個 {face} 面骰\n點數是 {result}")
			except Exception as e:
				await ctx.send(f"骰子格式錯誤：{e}")
		
		
async def setup(bot):
	await bot.add_cog(Game(bot))