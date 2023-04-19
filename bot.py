import discord
from discord.ext import commands
import json
import os

with open('setting.json', 'r', encoding='utf8') as jfile:
	jdata = json.load(jfile)

bot = commands.Bot(command_prefix = '!!', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)

@bot.event
async def on_ready():
	print(f"等登!機器人已經上線")

	for filename in os.listdir('./cmds'):
		if filename.endswith('.py'):
			print(f'cmds.{filename[:-3]}')
			await bot.load_extension(f'cmds.{filename[:-3]}')


@bot.command()
async def load(ctx, extension):
	if extension != 'all':
		bot.load_extension(f'cmds.{extension}')
		print(bot.load_extension(f'cmds.{extension}'))
		await ctx.send(f'載入 {extension} 完成!')
	else:
		for filename in os.listdir('./cmds'):
			if filename.endswith('.py'):
				print(f'cmds.{filename[:-3]}')
				await bot.load_extension(f'cmds.{filename[:-3]}')

@bot.command()
async def reload(ctx, extension):
	if extension != 'all':
		bot.reload_extension(f'cmds.{extension}')
		await ctx.send(f'重新載入 {extension} 完成!')
	else:
		for filename in os.listdir('./cmds'):
			if filename.endswith('.py'):
				await bot.reload_extension(f'cmds.{filename[:-3]}')

@bot.command()
async def unload(ctx, extension):
	if extension != 'all':
		bot.unload_extension(f'cmds.{extension}')
		await ctx.send(f'卸載 {extension} 完成!')
	else:
		for filename in os.listdir('./cmds'):
			if filename.endswith('.py'):
				await bot.unload_extension(f'cmds.{filename[:-3]}')


if __name__ == "__main__":
	bot.run(jdata['token'])