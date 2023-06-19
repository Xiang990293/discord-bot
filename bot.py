import discord
from discord.ext import commands
import json
import os
import inspect

with open('setting.json', 'r', encoding='utf8') as jfile:
	jdata = json.load(jfile)

bot = commands.Bot(command_prefix = '!!', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)

@bot.event
async def on_ready():
	print(f"等登!機器人已經上線")

	for filename in os.listdir('./cmds'):
		if filename.endswith('.py'):
			print(f'載入 cmds.{filename[:-3]} 完成!')
			await bot.load_extension(f'cmds.{filename[:-3]}')
	print(f'載入完成!')


@bot.command()
async def load(ctx, extension):
	await ctx.message.delete()
	if extension != 'all':
		if f"{extension}.py" in os.listdir('./cmds'):
			try:
				print(f'載入 cmds.{extension} 完成!')
				await bot.load_extension(f'cmds.{extension}')
				await ctx.send(f'載入 {extension} 完成!')
			except commands.ExtensionAlreadyLoaded:
				print(f'cmds.{extension} 已被載入')
				await ctx.send(f'{extension} 已被載入')
		else:
			print(f'cmds.{extension} 不存在')
			await ctx.send(f'{extension} 不存在')
	else:
		for filename in os.listdir('./cmds'):
			try:
				if filename.endswith('.py'):
					print(f'載入 cmds.{filename[:-3]} 完成!')
					await bot.load_extension(f'cmds.{filename[:-3]}')
			except commands.ExtensionAlreadyLoaded:
				continue
		await ctx.send(f'載入完成!')

@bot.command()
async def reload(ctx, extension):
	await ctx.message.delete()
	music_cog = bot.get_cog("music")
	
	if music_cog is not None:
		if music_cog.vc is not None and music_cog.vc.is_connected():
			await music_cog.vc.disconnect()
	if extension != 'all':
		if f"{extension}.py" in os.listdir('./cmds'):
			print(f'重新載入 cmds.{extension} 完成!')
			await bot.reload_extension(f'cmds.{extension}')
			await ctx.send(f'重新載入 {extension} 完成!')
		else:
			print(f'cmds.{extension} 不存在')
			await ctx.send(f'{extension} 不存在')
	else:
		for filename in os.listdir('./cmds'):
			if filename.endswith('.py'):
				print(f'重新載入 cmds.{filename[:-3]} 完成!')
				await bot.reload_extension(f'cmds.{filename[:-3]}')
		await ctx.send(f'重新載入完成!')

@bot.command()
async def unload(ctx, extension):
	await ctx.message.delete()
	# music_cog = bot.get_cog("music")
	# if music_cog.vc != None | music_cog.vc.is_connected():
	# 	music_cog.vc.disconnect()
	if extension != 'all':
		if f"{extension}.py" in os.listdir('./cmds'):
			try:
				print(f'卸載 cmds.{extension} 完成!')
				await bot.unload_extension(f'cmds.{extension}')
				await ctx.send(f'卸載 {extension} 完成!')
			except commands.ExtensionNotLoaded:
				print(f'cmds.{extension} 未被載入')
				await ctx.send(f'{extension} 未被載入')
		else:
			print(f'cmds.{extension} 不存在')
			await ctx.send(f'{extension} 不存在')
	else:
		for filename in os.listdir('./cmds'):
			try:
				if filename.endswith('.py'):
					print(f'卸載 cmds.{filename[:-3]} 完成!')
					await bot.unload_extension(f'cmds.{filename[:-3]}')
			except commands.ExtensionNotLoaded:
				continue
		await ctx.send(f'卸載完成!')

@bot.command(name='bot_test', aliases=['btest'], help="機器人測試指令")
async def bot_test(ctx, *, arg):
	await ctx.message.delete()
	res = eval(arg)
	print(str(res))
	if inspect.isawaitable(res):
		await ctx.send("```await "+arg+"```\n"+ str(await res))
	else:
		await ctx.send("```"+arg+"```\n"+ str(res))

if __name__ == "__main__":
	bot.run(jdata['token'])