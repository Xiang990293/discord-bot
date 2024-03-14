import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import os
import requests
import functions.get_jdata as getj
from bot import MODE

PATH = ["127.0.0.1","minecraft-discord-bot.fly.dev"]
FLY_API_HOSTNAME = "https://minecraft-discord-bot.fly.dev"
FLY_API_TOKEN = getj.get_jdata_with_key("fly_api_token", MODE)
VOLUME_ID = getj.get_jdata_with_key("volume_id", MODE)
UPLOAD_URL = f"{FLY_API_HOSTNAME}/v1/apps/minecraft-discord-bot/volumes/{VOLUME_ID}"

class file(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)

	async def upload_file(self, file, name):
		headers = {
			"Authorization": f"Bearer {FLY_API_TOKEN}",
			"Content-Type": "application/octet-stream"
		}
		files = {"file": (name, file)}
		response = requests.post(UPLOAD_URL, files=files, headers=headers)
		print(response.text)

	def download_file(self, file_name):
		response = requests.get(UPLOAD_URL)
		if response.status_code == 200:
			with open(file_name, "wb") as f:
				f.write(response.content)
		else:
			print("File not found or error occurred")

	async def get_volume_content(self):
		headers = {
			"Authorization": f"Bearer {FLY_API_TOKEN}",
			"Content-Type": "application/json"
		}

		try:
			response = requests.get(UPLOAD_URL, headers=headers)
			if response.status_code == 200:
				return response.content
			else:
				return None
		except Exception as e:
			print(f"Error accessing volume: {e}")
			return None

	@commands.command(name='upload', aliases=['ufile','upf'], help="Upload a file to the server")
	async def upload(self, ctx):
		# Check if a file is attached to the message
		if len(ctx.message.attachments) == 0:
			await ctx.send("請附加一個檔案用以上傳")
			return

		# Get the first attachment (assuming only one file is attached)
		attachment = ctx.message.attachments[0]

		# Download the attached file
		file_content = await attachment.read()

		# Save the file to the volume
		await self.upload_file(file_content, attachment.filename)
		# with open(f"/path/to/volume/{attachment.filename}", "wb") as f:
		# 	f.write(file_content)

		await ctx.send(f"檔案 {attachment.filename} 上傳成功。")

	@commands.command(name='download', aliases=['dfile','downf'], help="Download a file from the server")
	async def download(self, ctx, file_name):
		self.download_file(file_name)
		await ctx.send("File downloaded successfully!")
	
	
async def setup(bot):
	await bot.add_cog(file(bot))