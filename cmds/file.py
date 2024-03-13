import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import os
import requests

class file(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)

	def upload_file(self, file_path):
		url = "https://minecraft-discord-bot.fly.dev:8080/upload"
		files = {"file": open(file_path, "rb")}
		response = requests.post(url, files=files)
		print(response.text)

	def download_file(self, file_name):
		url = f"https://minecraft-discord-bot.fly.dev:8080/download/{file_name}"
		response = requests.get(url)
		if response.status_code == 200:
			with open(file_name, "wb") as f:
				f.write(response.content)
		else:
			print("File not found or error occurred")

	@commands.command(name='upload', aliases=['ufile','upf'], help="Upload a file to the server")
	async def upload(self, ctx, file_path):
		self.upload_file(file_path)
		await ctx.send("File uploaded successfully!")

	@commands.command(name='download', aliases=['dfile','downf'], help="Download a file from the server")
	async def download(self, ctx, file_name):
		self.download_file(file_name)
		await ctx.send("File downloaded successfully!")
	
	
async def setup(bot):
	await bot.add_cog(file(bot))