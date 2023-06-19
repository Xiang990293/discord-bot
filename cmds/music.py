import discord
from discord.ext import commands
from core.classes import Cog_Extension
from yt_dlp import YoutubeDL
import os
import inspect

class music(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__(self, bot)

		self.vc = None
		self.is_playing = False
		self.is_paused = False

		self.music_queue = []
		self.YDL_OPTIONS = {"format":"bestaudio", "noplaylist":"True"}
		self.FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}

	def get_audio_url(self, video):
		for format in video['formats']:
			if format['acodec'] != 'none' and format['vcodec'] == 'none':
				return format['url']
		return None

	def search_yt(self, item, is_search_mode = False, long_limit=10):
		if is_search_mode:
			with YoutubeDL(self.YDL_OPTIONS) as ydl:
				try:
					info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
				except Exception:
					return False

				for format in info["formats"]:
					if format["acodec"] != "none":
						return {'source': format['url'], 'Minecraft': False, 'title': info["title"]}

				return False
		else:
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

	def play_next(self):
		if len(self.music_queue) > 0:
			self.is_playing = True
			song = self.music_queue[0]
			m_url = song['source']
			self.music_queue.pop(0)

			if song["Minecraft"] == False:
				self.vc.play(discord.FFmpegOpusAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
			else:
				self.vc.play(discord.FFmpegOpusAudio(m_url), after=lambda e: self.play_next())
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
			song = self.music_queue[0]
			m_url = song['source']
			self.music_queue.pop(0)

			if self.vc is None or not self.vc.is_connected():
				await self.connect_to_channel(ctx)
				if self.vc is None:
					await ctx.send("無法連接至語音頻道")
					return
			else:
				await self.connect_to_channel(ctx) #await self.vc.move_to(song['channel'])

			if song["Minecraft"]:
				self.vc.play(discord.FFmpegOpusAudio(m_url), after=lambda e: self.play_next())
			else:
				self.vc.play(discord.FFmpegOpusAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
		else:
			self.is_playing = False

	@commands.command(name='play', aliases=['p', 'playing'], help="播放所選的Youtube歌曲")
	async def play(self, ctx, *args, limit=10):
		await ctx.message.delete()

		vchannel = ctx.author.voice.channel

		if self.vc is None:
			self.vc = await vchannel.connect()
		elif self.is_paused:
			self.vc.resume()

		if "https://" not in args[0]:
			query = " ".join(args)
			search = self.search_yt(query, True)
			
			if type(search) == type(True):
				await ctx.send("無法下載歌曲。網址格式不正確，請嘗試不同的關鍵字、播放清單或影片")
			else:
				await ctx.send(f"搜尋結果已經加入此播放清單之中：{search['title']}")

				# res = "```"
				# for i in search:
				# 	res += i['title'] + "\n"
				# 	self.queue_append(i, False)
				# res += "```"
				self.queue_append(search, False)

				# await ctx.send(res)

				if not self.is_playing:
					await self.play_music(ctx)
		elif "playlist" in args[0]:
			url = args[0]
			playlist = self.search_yt(url, long_limit=limit)
			if type(playlist) == type(True):
				await ctx.send("無法下載歌曲。網址格式不正確，請嘗試不同的關鍵字、播放清單或影片")
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
			url = args[0]
			if "&list=" in url:
				list = url.find('&list=')
				v = url.find('&v=')
				if v < list:
					url = url[:list]
			song = self.search_yt(url, long_limit=limit)
			if type(song) == type(True):
				await ctx.send("無法下載歌曲。網址格式不正確，請嘗試不同的關鍵字、播放清單或影片")
			else:
				await ctx.send(f"歌曲已經加入此播放清單之中： {song['title']}")
				self.queue_append(song, False)

				if not self.is_playing:
					await self.play_music(ctx)
	
	@commands.command(name='playMinecraft', aliases=['pmc', 'playmc'], help="播放所選的Youtube歌曲")
	async def playMinecraft(self, ctx, arg):
		await ctx.message.delete()
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

	@commands.command(name='playing_test', aliases=['ptest', 'playtest'], help="播放所選的Youtube歌曲")
	async def playing_test(self, ctx, *, arg):
		await ctx.message.delete()
		res = eval(arg)
		print(str(res))
		if inspect.isawaitable(res):
			await ctx.send("```await "+arg+"```\n"+str(await res))
		else:
			await ctx.send("```"+arg+"```\n"+str(res))

	@commands.command(name='join', aliases=['jion'], help="加入語音頻道")
	async def join(self, ctx):
		await ctx.message.delete()
		await self.connect_to_channel(ctx)

	@commands.command(name='pause', aliases=['pa','stop','stopped'], help="停止播放目前的歌曲")
	async def pause(self, ctx):
		await ctx.message.delete()
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

	@commands.command(name="resume", aliases=['r'], help="重新播放目前的歌曲")
	async def resume(self, ctx):
		await ctx.message.delete()
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

	@commands.command(name='skip', aliases=['s'], help="跳過目前的歌曲")
	async def skip(self, ctx, *args):
		await ctx.message.delete()
		if self.vc != None and self.vc:
			self.vc.stop()
			await self.play_music(ctx)
	
	@commands.command(name='getqueue', aliases=['gque','gq','getq'], help="列出所有目前在清單中的所有歌曲")
	async def getqueue(self, ctx):
		await ctx.message.delete()
		
		if len(self.music_queue) == 0:
			await ctx.send("目前清單中沒有任何歌曲")
			return
		else:
			retval = "播放清單：```"
			for i in self.music_queue:
				retval += i['title'] + "\n"
			retval += "```"
			await ctx.send(retval)

	@commands.command(name='clear', help="清除目前清單中所有歌曲")
	async def clear(self, ctx, *args):
		await ctx.message.delete()
		if self.vc != None and self.is_playing:
			self.vc.stop()
		self.music_queue = []
		await ctx.send("目前清單已清除")

	@commands.command(name='volume', aliases=['v'], help="設定音量")
	async def volume(self, ctx, *args):
		await ctx.message.delete()
		if self.vc!= None and self.is_playing:
			self.vc.volume = int(args[0])
			await ctx.send(f"音量已設定為 {args[0]}")
		else:
			await ctx.send("目前沒有音量設定")

	@commands.command(name='leave', aliases=['l'], help="請我離開頻道")
	async def leave(self, ctx):
		await ctx.message.delete()
		self.is_playing = False
		self.is_paused = False
		await self.vc.disconnect()
		
async def setup(bot):
	await bot.add_cog(music(bot))