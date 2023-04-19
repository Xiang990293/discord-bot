import discord
from discord.ext import commands
from core.classes import Cog_Extension
from yt_dlp import YoutubeDL

class music_cog(Cog_Extension):
	def __init__(self, bot):
		Cog_Extension.__init__()
		
		self.is_playing = False
		self.is_paused = False

		self.music_queue = []
		self.YDL_OPTIONS = {"format":"bestaudio", "nopalaylist":"True"}
		self.FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}

		self.vc = None

	def search_yt(self, item):
		with YoutubeDL(self.YDL_OPTIONS) as ydl:
			try:
				info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
			except Exception:
				return False
			return {'source': info["format"][0]['url'], 'title': info["title"]}

	def play_next(self):
		if len(self.music_queue) > 0:
			self.is_playing = True

			m_url = self.music_queue[0]['source']

			self.music_queue.pop()
	
			self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next)
		else:
			self.is_playing = False
	
	async def play_music(self, ctx):
		if len(self.music_queue) > 0:
			self.is_playing = True
			m_url = self.music_queue[0][0]['source']

			if self.vc == None or not self.vc.is_connected():
				self.vc = await self.musicqueue[0][1].connect()

				if self.vc == None:
					await ctx.send("無法連接至語音頻道")
					return
			else:
				await self.vc.move_to(self.musicqueue[0][1])
			
			self.music_queue.pop(0)
			
			self.vc.play(discord.FFmoegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

		else:
			self.is_playing = False
		
	@commands.command(name='play', aliases=['p', 'playing'], help="播放所選的Youtube歌曲")
	async def play(self, ctx, *args):
		query = " ".join(args)
		
		voice_channel = ctx.author.voice.channel()
		if voice_channel == None:
			await ctx.send("請進到語音頻道")
		elif self.is_paused:
			self.vc.resume()
		else:
			song = self.search_yt(query)
			if type(song) == type(True):
				await ctx.send("無法下載歌曲。非正確的格式，請嘗試不同的關鍵字")
			else:
				await ctx.send("歌曲已經加入清單之中")
				self.music_queue.append([song, voice_channel])

				if self.is_playing == False:
					await self.play_music(ctx)
	@commands.command(name='pause', aliases=['pa','stop','stopped'], help="停止播放目前的歌曲")
	async def pause(self, ctx, *args):
		if self.is_playing:
			self.is_playing = False
			self.is_paused = True
			self.vc.pause()
			await ctx.send("歌曲已暫停")
		elif self.is_paused:
			self.vc.resume()
			await ctx.send("歌曲再次播放~")

	@commands.command(name="resume", aliases=['r'], help="重新播放目前的歌曲")
	async def resume(self, ctx, *args):
		if self.is_playing:
			self.is_playing = True
			self.is_paused = False
			self.vc.resume()
			await ctx.send("歌曲再次播放")

	@commands.command(name='skip', aliases=['s'], help="跳過目前的歌曲")
	async def skip(self, ctx, *args):
		if self.vc != None and self.vc:
			self.vc.stop()
			await self.play_music(ctx)
	
	@commands.command(name='queue', aliases=['q','queue'], help="列出所有目前在清單中的所有歌曲")
	async def queue(self, ctx):
		retval = ""

		for i in range(0, len(self.music_queue)):
			if i > 4: break
			retval += self.music_queue[i][0]['title'] + "\n"
			
		if retval != "":
			await ctx.send(retval)
		else:
			await ctx.send("目前清單中沒有任何歌曲")

	@commands.command(name='clear', aliases=['c'], help="清除目前清單中所有歌曲")
	async def clear(self, ctx, *args):
		if self.vc != None and self.is_playing:
			self.vc.stop()
		self.music_queue = []
		await ctx.send("目前清單已清除")

	@commands.command(name='volume', aliases=['v'], help="設定音量")
	async def volume(self, ctx, *args):
		if self.vc!= None and self.is_playing:
			self.vc.volume = int(args[0])
			await ctx.send("音量已設定為 %s" % args[0])
		else:
			await ctx.send("目前沒有音量設定")

	@commands.command(name='leave', aliases=['l'], help="請我離開頻道")
	async def leave(self, ctx):
		self.is_playing = False
		self.is_paused = False
		await self.vc.disconnect()
		
async def setup(bot):
	await bot.add_cog(music_cog(bot))