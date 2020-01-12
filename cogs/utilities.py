import discord
from discord.ext import commands


class Utilities(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def load(self, ctx, extension):
        self.client.load_extension(f'cogs.{extension}')
        print(f'Loaded {extension}')
        await ctx.send(f'Loaded {extension}')

    @commands.command()
    async def unload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        print(f'Unloaded {extension}')
        await ctx.send(f'Unloaded {extension}')

    @commands.command()
    async def reload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        print(f'Unloaded {extension}')
        self.client.load_extension(f'cogs.{extension}')
        print(f'Loaded {extension}')
        await ctx.send(f'Reloaded {extension}')


def setup(client):
    client.add_cog(Utilities(client))
