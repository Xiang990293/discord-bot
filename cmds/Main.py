from core.classes import Cog_Extension
import discord
from discord.ext import commands
import json

class Main(Cog_Extension):
    
    @commands.command()
    async def pinglatency(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} (ms)')

    @commands.command()
    async def picture(self, ctx):
        pic = discord.File()
        await ctx.send

    @commands.command()
    async def test(self, ctx):
        await ctx.send(ctx.message.channel)

def setup(bot):
    bot.add_cog(Main(bot))