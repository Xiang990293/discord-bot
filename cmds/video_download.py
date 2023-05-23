import discord
from discord.ext import commands
from core.classes import Cog_Extension
from yt_dlp import YoutubeDL
from google.cloud import storage
import functions.google_drive as fgd
import yt_dlp
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
		
		self.amount = 0
		self.options = {
			'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
			'outtmpl': f'temp_file/download_{self.amount}.%(ext)s'
		}

	@commands.command(name='reset', aliases=['rs'], help="下載影片")
	async def reset(self, ctx):
		await ctx.message.delete()
		self.amount = 0
		print("下載除列已清空")
		await ctx.send("下載除列已清空")
		
	@commands.command(name='download_video', aliases=['dv', 'dvid'], help="下載影片")
	async def dowmload_video(self, ctx, url: str):
		def is_url_available(url):
			try:
				with YoutubeDL() as ydl:
					ydl.extract_info(url, download=False)
				return True
			except yt_dlp.utils.DownloadError:
				return False
		
		def upload_to_gcs(file_data, project_id, bucket_name, filename):
			self.bot.loop.create_task(ctx.send("正在上傳雲端..."))
			print("正在上傳雲端...")
			
			return fgd.upload_to_gcs(file_data, project_id, bucket_name, filename)

		def download_and_upload(url, options):
			filename, info_dict = fgd.download_and_upload(url, options)

			# Upload the file to Google Cloud Storage
			with open(filename, "rb") as f:
				file_data = f.read()
			upload_url = upload_to_gcs(file_data, PROJECT_ID, BUCKET_NAME, f"{info_dict['title']}.mp4")
			encoded_url = urllib.parse.quote(upload_url, safe=':/')

			# Delete the downloaded file
			os.remove(filename)

			self.amount -= 1

			# Send the message with the download URL
			message = f"已將下載結果上傳雲端，可供下載: {encoded_url}"
			self.bot.loop.create_task(ctx.send(message))

			self.bot.loop.create_task(ctx.send(f"下載期限為30天", delete_after=30))

		if ctx.author.bot:
			await ctx.message.delete()
			await ctx.send(f"嗶啵！啵嗶。機器人！")
		else:
			await ctx.message.delete()
			if self.amount == 0:
				self.amount += 1
				await ctx.send(f"正在檢查連結是否可用...")
				if is_url_available(url):
					print(f"正在下載： {url}")
					await ctx.send(f"正在下載： {url}")
					thread = threading.Thread(target=download_and_upload, args=(url, self.options))
					thread.start()
				else:
					print("影片連結不可用")
					await ctx.send("影片連結不可用")
					self.amount == 0
				
			else:
				print("目前在下載其他影片")
				await ctx.send("目前在下載其他影片...")


	@commands.command(name='download_options', aliases=['dopt', 'dops', 'doptions'], help="播放所選的Youtube歌曲")
	async def download_options(self, ctx, option_name: str, option_value: str):
		# 設定下載選項
		if option_name in self.options:
			self.options[option_name] = option_value
			await ctx.send(f"已將下載設定 {option_name} 設為 {option_value}")
		else:
			await ctx.send(f":warning: 無效的下載設定 {option_name}")

		await ctx.send(f"設定完成")

	@commands.command()
	async def test_lib(self, ctx, url):
		encoded_url = urllib.parse.quote(url, safe=':/')

		message = f"{encoded_url}"
		self.bot.loop.create_task(ctx.send(message))
		
async def setup(bot):
	await bot.add_cog(video_download(bot))