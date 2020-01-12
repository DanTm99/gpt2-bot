import discord
from discord.ext import commands


class Setup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready')


def setup(client):
    client.add_cog(Setup(client))
