import discord
from discord.ext import commands

class help_cog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.help_message = """
```
常用指令：
/help - 列出所有常用指令
/p <關鍵字> - 查詢youtube歌曲，並展示出來
/q 或 /queue - 顯示目前的歌單
/skip - 跳過目前的歌曲
/clear - 清除清單中的歌曲
/leave - 請機器人我離開
/pause - 暫停目前歌曲
/resume - 解除暫停、重新播放
/stop - 
```
"""
		self.text_channel_text = []
		async def on_ready(self):
			for guild in self.bot.guilds:
				for channel in guild.text_channels:
					self.text_channel_text.append(channel)

			await self.send_to_all(self.help_message)

		async def send_to_all(self, msg):
			for text_channel in self.text_channel_text:
				await text_channel.send(msg)
		
		@commands.command(name="help", help="列出所有可用指令")
		async def help(self, ctx):
			await ctx.send(self.help_message)
