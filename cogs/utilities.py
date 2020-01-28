import subprocess

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

    @commands.command()
    async def update(self, ctx, *, arg=None):
        print('Command update triggered')
        await ctx.send('Updating and shutting down...')
        subprocess.call('git pull')
        await ctx.bot.logout()

    @commands.command()
    async def stop(self, ctx, *, arg=None):
        print('Command stop triggered')
        await ctx.send('Shutting down...')
        await ctx.bot.logout()


def setup(client):
    client.add_cog(Utilities(client))
