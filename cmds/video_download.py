import discord
from discord.ext import commands
from core.classes import Cog_Extension
from yt_dlp import YoutubeDL
from google.cloud import storage
import functions.google_drive as fgd
import json
import os
import threading
import urllib

with open('setting.json', 'r', encoding='utf8') as jfile:
	jdata = json.load(jfile)

PROJECT_ID = jdata['product_id']
BUCKET_NAME = jdata['bucket_name']

class video_download(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)
		
		self.options = {
			'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
			'outtmpl': 'temp_file/download.%(ext)s'
		}
		
	@commands.command(name='download_video', aliases=['dv', 'dvid'], help="下載影片")
	async def dowmload_video(self, ctx, url: str):
		def upload_to_gcs(file_data, project_id, bucket_name, filename):
			self.bot.loop.create_task(ctx.send("正在上傳雲端..."))
			
			# Create a Google Cloud Storage client
			storage_client = storage.Client(project=project_id)

			# Get a reference to the storage bucket
			bucket = storage_client.bucket(bucket_name)

			# Upload the file to the bucket
			blob = bucket.blob(filename)
			blob.upload_from_string(file_data, timeout=300)

			# Set the blob's ACL to public-read
			blob.acl.save_predefined("public-read")

			# Get the publicly accessible URL for the file
			url = f"https://storage.googleapis.com/{bucket.name}/{blob.name}"

			return url

		def download_and_upload(url, options):
			# Download the video
			with YoutubeDL(options) as ydl:
				info_dict = ydl.extract_info(url, download=True)
				filename = ydl.prepare_filename(info_dict)

			# Upload the file to Google Cloud Storage
			with open(filename, "rb") as f:
				file_data = f.read()
			upload_url = upload_to_gcs(file_data, PROJECT_ID, BUCKET_NAME, f"{info_dict['title']}.mp4")
			encoded_url = urllib.parse.quote(upload_url, safe=':/')

			# Delete the downloaded file
			os.remove(filename)

			# Send the message with the download URL
			message = f"已將下載結果上傳雲端，可供下載: {encoded_url}"
			self.bot.loop.create_task(ctx.send(message))

		if ctx.author.bot:
			await ctx.send(f"嗶啵！啵嗶。機器人！")
		else:
			thread = threading.Thread(target=download_and_upload, args=(url, self.options))
			thread.start()

			await ctx.send("正在下載影片...")


	@commands.command(name='download_options', aliases=['dopt', 'dops', 'doptions'], help="播放所選的Youtube歌曲")
	async def download_options(self, ctx, option_name: str, option_value: str):
		# 設定下載選項
		if option_name in self.options:
			self.options[option_name] = option_value
			await ctx.send(f"Download option '{option_name}' set to '{option_value}'")
		else:
			await ctx.send(f"Invalid download option '{option_name}'")

		await ctx.send(f"設定完成")

	@commands.command()
	async def test_lib(self, ctx, url):
		encoded_url = urllib.parse.quote(url, safe=':/')

		message = f"{encoded_url}"
		self.bot.loop.create_task(ctx.send(message))
		
async def setup(bot):
	await bot.add_cog(video_download(bot))