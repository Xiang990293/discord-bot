import discord
from discord.ext import commands
from core.classes import Cog_Extension
from yt_dlp import YoutubeDL
import os
import inspect
import threading
import aiohttp
from http.server import SimpleHTTPRequestHandler, HTTPServer
import ast

class Music(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)

		self.vc = None
		self.is_playing = False
		self.is_paused = False
		self.loop_mode = 0
		self.playing_song = {}
		self.amount = 0
		self.options = {
			'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
			'outtmpl': f'temp_file/download_{self.amount}.%(ext)s'
		}
		
		self.HandlerClass = SimpleHTTPRequestHandler
		self.ServerClass  = HTTPServer
		self.Protocol     = "HTTP/1.0"
		self.PORT		  = 8080
		self.DIRECTORY    = "/temp_file"

		self.music_queue = []
		self.YDL_OPTIONS = {"format":"bestaudio", "noplaylist":"True"}
		self.FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}

	def get_audio_url(self, video):
		for format in video['formats']:
			try:
				if format['acodec'] != 'none' and format['vcodec'] == 'none':
					return format['url']
			except Exception:
				return format['url']
		return None

	def search_yt(self, item, is_search_mode = False, long_limit=10, is_list=False):
		if is_search_mode:
			with YoutubeDL(self.YDL_OPTIONS) as ydl:
				try:
					info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
				except Exception:
					return False

				for format in info["formats"]:
					try:
						if format["acodec"] != "none":
							return {'source': format['url'], 'Minecraft': False, 'title': info["title"]}
					except Exception:
						return {'source': format['url'], 'Minecraft': False, 'title': info["title"]}
				return False
		elif is_list:
			playlist_info = []
			with YoutubeDL(self.YDL_OPTIONS) as ydl:
				try:
					info = ydl.extract_info(item, download=False)
					if 'entries' in info:
						videos = info['entries']
						if type(long_limit) == type(1):
							videos = videos[:long_limit]
						playlist_info = [
							{
								'source': self.get_audio_url(video),
								'Minecraft': False,
								'title': video['title']
							}
							for video in videos
						]
						return playlist_info
					else:
						video = info
						return {
							'source': self.get_audio_url(video),
							'Minecraft': False,
							'title': video['title']
						}
				except Exception:
					return False
		else:
			with YoutubeDL(self.YDL_OPTIONS) as ydl:
				try:
					info = ydl.extract_info(item, download=False)
					song = {
						'source': self.get_audio_url(info),
						'Minecraft': False,
						'title': info['title']
					}
					return song
				except Exception:
					return False

	def play_next(self, previous_song):
		if previous_song != {'skip':True}:
			previous_song = self.playing_song
		if self.loop_mode == 1:
			self.music_queue.insert(0, previous_song)
		elif self.loop_mode == 2:
			self.music_queue.append(previous_song)

		if len(self.music_queue) > 0:
			self.is_playing = True
			self.playing_song = self.music_queue[0]
			self.music_queue.pop(0)

			if self.playing_song["Minecraft"] == False:
				self.vc.play(discord.FFmpegOpusAudio(self.playing_song['source'], **self.FFMPEG_OPTIONS), after=lambda e=self.playing_song: self.play_next(e))
			else:
				self.vc.play(discord.FFmpegOpusAudio(self.playing_song['source']), after=lambda e=self.playing_song: self.play_next(e))
		else:
			self.is_playing = False
	
	async def connect_to_channel(self, ctx):
		vchannel = ctx.author.voice.channel
		try:
			if self.vc == None:
				self.vc = await vchannel.connect()
			elif self.vc.is_connected() == False:
				self.vc = await vchannel.connect()
			else: 
				await self.vc.move_to(vchannel)
		except discord.ext.commands.errors.ClientException:
			pass
	
	def queue_append(self, query, isMinecraft = False):
		self.music_queue.append({'source': query['source'], 'Minecraft': isMinecraft, 'title':query['title']})
		return self.music_queue

	async def play_music(self, ctx):
		if len(self.music_queue) > 0:
			self.is_playing = True
			self.playing_song = self.music_queue[0]
			self.music_queue.pop(0)

			if self.vc is None or not self.vc.is_connected():
				await self.connect_to_channel(ctx)
				if self.vc is None:
					await ctx.send("無法連接至語音頻道")
					return
			else:
				await self.connect_to_channel(ctx) #await self.vc.move_to(song['channel'])

			if self.playing_song["Minecraft"]:
				self.vc.play(discord.FFmpegOpusAudio(self.playing_song['source']), after=lambda e=self.playing_song: self.play_next(e))
			else:
				self.vc.play(discord.FFmpegOpusAudio(self.playing_song['source'], **self.FFMPEG_OPTIONS), after=lambda e=self.playing_song: self.play_next(e))
		else:
			self.is_playing = False

	@commands.hybrid_command(name='download_video', aliases=['dv','downv','dvid'], with_app_command=True, help="下載並傳送提供之網址的影片/歌曲")
	async def download_video(self, ctx, url):
		await interaction.response.defer()  
		def is_url_available(url):
			try:
				with YoutubeDL() as ydl:
					ydl.extract_info(url, download=False)
				return True
			except ydl.utils.DownloadError:
				return False
		
		def download_video(url, options):
			with YoutubeDL(options) as ydl:
				info_dict = ydl.extract_info(url, download=True)
				filename = ydl.prepare_filename(f"info_dict")


			# self.bot.loop.create_task(ctx.send(file=filename))

			if os.path.exists(f"/bot{filename}"):
				# Send the message with the download URL
				self.bot.loop.create_task(ctx.send("下載結果: "))
				self.bot.loop.create_task(ctx.send(f"http://minecraft-discord-bot.fly.dev/{filename}"))
			else:
				self.bot.loop.create_task(ctx.send("找不到下載檔案。"))

			# Delete the downloaded file
			# os.remove(filename)

			# self.amount -= 1

			# self.bot.loop.create_task(ctx.send(f"下載期限為30天", delete_after=30))

		if ctx.author.bot:
			await ctx.send(f"嗶啵！啵嗶。機器人！")
		else:
			if self.amount == 0:
				self.amount += 1
				await ctx.send(f"```{url}```\n正在檢查連結是否可用...")
				if is_url_available(url):
					await ctx.send(f"正在下載，請稍後...")
					thread = threading.Thread(target=download_video, args=(url, self.options))
					thread.start()
				else:
					await ctx.send("```{url}```\n影片連結不可用")
					self.amount == 0
				
			else:
				await ctx.send("目前在下載其他影片...")

	@commands.hybrid_command(name='play', aliases=['p', 'playing'], with_app_command=True, help="播放所選的Youtube歌曲")
	async def play(self, ctx, *, 歌名or網址, limit=10):
		await interaction.response.defer()
		vchannel = ctx.author.voice.channel
		arg = 歌名or網址

		#檢測使用者是否在語音頻道
		if self.vc is None:
			self.vc = await vchannel.connect()
		elif self.is_paused:
			self.vc.resume()

		if limit > 20:
			await ctx.send("無法容納過大上限之播放清單，上限將下調至 20")
			limit = 20

		if ("https://" not in arg[0]) and not (arg[0].startswith('https://')):
			
			search_str = arg
			cleaned_arg = [word.replace("「","").replace("」","") for word in arg.split()] #原本不知為何加了「」會報錯
			arg = tuple(cleaned_arg)
			query = " ".join(arg)

			search = self.search_yt(query, True)
			
			if type(search) == type(True):
				await ctx.send(f"```{search_str}```\n無法下載歌曲。請嘗試不同的關鍵字、播放清單或影片")
			else:
				await ctx.send(f"```{search_str}```\n搜尋結果已經加入此播放清單之中：{search['title']}")

				# res = "```"
				# for i in search:
				# 	res += i['title'] + "\n"
				# 	self.queue_append(i, False)
				# res += "```"
				self.queue_append(search, False)

				# await ctx.send(res)

				if not self.is_playing:
					await self.play_music(ctx)
		elif "playlist" in arg[0]:
			url = arg[0]
			playlist = self.search_yt(url, long_limit=limit, is_list=True)
			if type(playlist) == type(True):
				await ctx.send("無法下載歌曲。清單網址格式不正確，請嘗試不同的關鍵字、播放清單或影片")
			else:
				await ctx.send("提供的播放清單已經加入此播放清單之中：")
				res = "```"
				for i in playlist:
					res += i['title'] + "\n"
					self.queue_append(i, False)
				res += "```"
				await ctx.send(res)

				if not self.is_playing:
					await self.play_music(ctx)
		else:
			url = arg[0]
			if "&list=" in url:
				list = url.find('&list=')
				v = url.find('&v=')
				if v < list:
					url = url[:list]
			song = self.search_yt(url, long_limit=limit, is_list=False)
			if type(song) == type(True):
				await ctx.send("無法下載歌曲。網址格式不正確，請嘗試不同的關鍵字、播放清單或影片")
			else:
				await ctx.send(f"歌曲已經加入此播放清單之中： {song['title']}")
				self.queue_append(song, False)

				if not self.is_playing:
					await self.play_music(ctx)
	
	@commands.hybrid_command(name='playminecraft', aliases=['pmc', 'playmc'], with_app_command=True, help="播放所選的Minecraft歌曲")
	async def playminecraft(self, ctx, arg: str):
		if arg == "list":
			await ctx.send("```"+str(os.listdir('files/music')).replace(".ogg', '", "\n").replace("['","").replace(".ogg']","")+"```")
			return
		
		if self.vc == None:
			await ctx.send("請進到語音頻道")
		elif self.is_paused:
			self.vc.resume()
		else:
			if arg+".ogg" in os.listdir('files/music'):
				self.music_queue.append({'source': f"files/music/{arg}.ogg", 'Minecraft': True, 'title':arg})
				await ctx.send(f"歌曲已經加入清單之中： {arg}")
			else:
				f = os.listdir('files/music')
				for i in f:
					self.music_queue.append({'source': f"files/music/{i}", 'Minecraft': True, 'title':i.replace(".ogg", "")})
			if not self.is_playing:
				await self.play_music(ctx)

	@commands.hybrid_command(name='playing_test', aliases=['ptest', 'playtest'], with_app_command=True, help="播放所選的Youtube歌曲")
	async def playing_test(self, ctx, *, arg):
		await interaction.response.defer()  
		res = eval(arg)
		print(str(res))
		if inspect.isawaitable(res):
			await ctx.send("```await "+arg+"```\n"+str(await res))
		else:
			await ctx.send("```"+arg+"```\n"+str(res))

	@commands.hybrid_command(name='searching_test', aliases=['stest', 'searchtest'], with_app_command=True, help="播放所選的Youtube歌曲")
	async def searching_test(self, ctx, *, arg):
		await interaction.response.defer()  
		search_str = arg
		cleaned_arg = [word.replace("「","").replace("」","") for word in arg.split()] #原本不知為何加了「」會報錯
		arg = tuple(cleaned_arg)
		query = " ".join(arg)
		await ctx.send(f"```{search_str}``` \n{str(query)} \n{arg[0]}: {'https://' not in arg[0]}")

	@commands.hybrid_command(name='join', aliases=['jion'], with_app_command=True, help="加入語音頻道")
	async def join(self, ctx):
		await self.connect_to_channel(ctx)
		await self.Send("已加入")

	@commands.hybrid_command(name='pause', aliases=['pa','stop','stopped'], with_app_command=True, help="停止播放目前的歌曲")
	async def pause(self, ctx):
		if self.is_playing:
			self.is_playing = False
			self.is_paused = True
			self.vc.pause()
			await ctx.send("歌曲已暫停")
		elif self.is_paused:
			self.is_playing = True
			self.is_paused = False
			self.vc.resume()
			await ctx.send("歌曲再次播放~")

	@commands.hybrid_command(name="resume", aliases=['r'], with_app_command=True, help="重新播放目前的歌曲")
	async def resume(self, ctx):
		if self.is_playing:
			self.is_playing = False
			self.is_paused = True
			self.vc.pause()
			await ctx.send("歌曲已暫停")
		elif self.is_paused:
			self.is_playing = True
			self.is_paused = False
			self.vc.resume()
			await ctx.send("歌曲再次播放")
		else:
			await ctx.send("歌曲尚未開始")

	@commands.hybrid_command(name='skip', aliases=['s'], with_app_command=True, help="跳過目前的歌曲")
	async def skip(self, ctx):
		if self.vc != None and self.vc:
			self.vc.stop()
			await self.play_next({'Skip':True})

	@commands.hybrid_command(name='loop', aliases=['looping'], with_app_command=True, help="切換重複播放模式")
	async def loop(self, ctx, arg: str):
		self.loop_mode += 1
		self.loop_mode %= 3

		if arg=="help":
			await ctx.send(f"利用 `!!loop` 進行模式切換\n單曲循環模式直接將正要開始播放的歌曲直接加入表頭\n播放列表循環模式將正要開始播放的歌曲直接加入表尾\n關閉後會再次播放當前歌曲")
		else:
			if arg=="0" or arg=="1" or arg=="2":
				self.loop_mode = int(arg)

			match self.loop_mode:
				case 0:
					loop = "正常模式"
				case 1:
					loop = "單曲循環模式"
				case 2:
					loop = "播放列表循環模式"
			
			await ctx.send(f"已切換為**{loop}**")

	@commands.hybrid_command(name='getqueue', aliases=['gque','gq','getq'], with_app_command=True, help="列出所有目前在清單中的所有歌曲")
	async def getqueue(self, ctx):
		if len(self.music_queue) == 0:
			await ctx.send("目前清單中沒有任何歌曲")
			return
		else:
			retval = "正在播放：\n```"
			retval += self.playing_song['title']
			retval += "```\n播放清單：```"
			for i in range(len(self.music_queue)):
				retval += str(i+1) + "." + self.music_queue[i]['title'] + "\n"
			retval += "```"
			await ctx.send(retval)

	@commands.hybrid_command(name='clear', with_app_command=True, help="清除目前清單中所有歌曲")
	async def clear(self, ctx):
		if self.vc != None and self.is_playing:
			self.vc.stop()
		self.music_queue = []
		await ctx.send("目前清單已清除")

	@commands.hybrid_command(name='volume', aliases=['v'], with_app_command=True, help="設定音量")
	async def volume(self, ctx, volume: int):
		if self.vc!= None and self.is_playing:
			self.vc.volume = volume
			await ctx.send(f"音量已設定為 {volume}%")
		else:
			await ctx.send("目前沒有音量設定")

	@commands.hybrid_command(name='leave', aliases=['l'], with_app_command=True, help="請我離開頻道")
	async def leave(self, ctx):
		self.is_playing = False
		self.is_paused = False
		await self.vc.disconnect()
		
async def setup(bot):
	await bot.add_cog(Music(bot))