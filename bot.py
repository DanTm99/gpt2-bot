import discord
import os
from discord.ext import commands, tasks

API_KEY = ''

client = commands.Bot(command_prefix=';;')


# Load all .py files in cog folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')


client.run(API_KEY)
