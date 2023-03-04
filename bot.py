import discord
from discord.ext import commands
import json
import os

from help_cog import help_cog
from music_cog import music_cog

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix = '!!')

bot.remove_command('help')

bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))

@bot.command()
async def on_ready():
    print(f"等登!機器人已經上線")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'載入 {extension} 完成!')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'重新載入 {extension} 完成!')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'卸載 {extension} 完成!')

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
    bot.run(jdata['token'])