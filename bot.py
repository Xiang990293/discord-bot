#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler
import discord
from discord.ext import commands
import functions.get_jdata as getj
import os
import inspect
import threading

MODE = 1 - ("setting.json" in os.listdir('.'))
# mode = {"debug": 0, "run": 1}

bot = commands.Bot(command_prefix = '\\', intents=discord.Intents.all(), case_insensitive=True, self_bot=True)

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='./temp_file', **kwargs)

def start_http_server():
	ip = getj.get_jdata(MODE)["ip"]
	with socketserver.TCPServer((ip, 8080), MyHTTPRequestHandler) as httpd:
		print(f"HTTP server running on {ip}:8080...")
		httpd.serve_forever()

@bot.command(name="synccmd", alienses=["synccommands"], help="同步斜線指令")
@commands.has_permissions(administrator=True)
async def synccommands(ctx):
	await bot.tree.sync()
	await ctx.send("同步完成")

@bot.event
async def on_ready():
	print(f"等登!機器人已經上線")

	for filename in os.listdir('./cmds'):
		if filename.endswith('.py'):
			print(f'載入 cmds.{filename[:-3]} 完成!')
			await bot.load_extension(f'cmds.{filename[:-3]}')
	print(f'載入完成!')

	http_thread = threading.Thread(target=start_http_server)
	http_thread.start()


@bot.hybrid_command(with_app_command=True, help="加載模組")
async def load(ctx, 模組):
	await interaction.response.defer()
	extension = 模組
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

@bot.hybrid_command(with_app_command=True, help="重載模組")
async def reload(ctx, 模組):
	await interaction.response.defer()
	extension = 模組 
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

@bot.hybrid_command(with_app_command=True, help="停用模組")
async def unload(ctx, 模組):
	# music_cog = bot.get_cog("music")
	# if music_cog.vc != None | music_cog.vc.is_connected():
	# 	music_cog.vc.disconnect()
	await interaction.response.defer()
	extension = 模組
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

@bot.hybrid_command(name='bot_test', aliases=['btest'], help="機器人測試指令")
async def bot_test(ctx, *, arg):
	res = eval(arg)
	print(str(res))
	if inspect.isawaitable(res):
		await ctx.send("```await "+arg+"```\n"+ str(await res))
	else:
		await ctx.send("```"+arg+"```\n"+ str(res))

if __name__ == "__main__":
	bot.run(getj.get_jdata(MODE)["token"])