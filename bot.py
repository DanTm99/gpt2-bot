import os

from discord.ext import commands

API_KEY_FILENAME = 'apikey.txt'
api_key = None

# Read API key from file
try:
    with open(API_KEY_FILENAME, 'r') as file:
        api_key = file.readline().rstrip()
except FileNotFoundError:
    print(f'ERROR: API key file {API_KEY_FILENAME} not found')
    exit(0)

client = commands.Bot(command_prefix=';;')


# Load all .py files in cog folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')

client.run(api_key)
