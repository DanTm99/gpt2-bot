import os

import gpt_2_simple as gpt2
from discord.ext import commands

VALID_MODELS = ['124M', '355M', '774M', '1558M']
CONFIG_PATH = 'gpt2.config'
DEFAULT_CONFIG = {
    'model_name': '124M',
    'length': '10',
    'temperature': '0.7',
    'top_k': '0',  # How many previous words to consider when generating a new word. 0 means unlimited
    'top_p': '0.9',
    'include_prefix': 'True'
}
CONFIG_KEY_PARSER = {
    'length': lambda i: int(i),
    'temperature': lambda f: float(f),
    'top_k': lambda i: int(i),
    'top_p': lambda f: float(f),
    'include_prefix': lambda b: b == 'True',
}


def parse_generate_arguments(arguments):
    return_value = {}
    for key in arguments:
        if key in CONFIG_KEY_PARSER:
            return_value[key] = CONFIG_KEY_PARSER[key](arguments[key])
        else:  # If there is no parser keep it the same
            return_value[key] = arguments[key]

    return return_value


class Gpt2(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.sess = gpt2.start_tf_sess()
        self.n = None

        self.config = {}
        self.load_config()
        gpt2.load_gpt2(self.sess, model_name=self.config['model_name'])

    @commands.command(aliases=['generate'])
    async def gpt2_generate(self, ctx, *, arg=None, **kwargs):
        print('Command gpt2_generate triggered')
        await ctx.send("Generating...")
        if arg:
            if self.is_model_downloaded():
                if arg:
                    args = parse_generate_arguments(self.config)
                    if 'n' in kwargs:
                        sample = gpt2.generate(self.sess, prefix=arg, return_as_list=True, length=kwargs['n'], **args)[0]
                    else:
                        sample = gpt2.generate(self.sess, prefix=arg, return_as_list=True, **args)[0]
                    await ctx.send(sample)
                else:
                    await ctx.send("ERROR: Argument required")
            else:
                await ctx.send(f"ERROR: Model {DEFAULT_CONFIG['model_name']} not downloaded")
        else:
            await ctx.send("ERROR: Argument required")

    @commands.command(aliases=['set_model'])
    async def gpt2_set_model(self, ctx, *, arg=None):
        print('Command gpt2_set_model triggered')
        if arg:
            if arg in VALID_MODELS:
                self.update_config(model_name=arg)
            else:
                await ctx.send("ERROR: Invalid argument")
        else:
            await ctx.send("ERROR: Argument required")

    @commands.command(aliases=['set_length'])
    async def gpt2_set_length(self, ctx, *, arg=None):
        print('Command gpt2_set_length triggered')
        if arg:
            try:
                i = int(arg)
                assert i > 0
            except ValueError or AssertionError:
                ctx.send("ERROR: Argument must be a positive whole number")
            self.update_config(length=arg)
        else:
            await ctx.send("ERROR: Argument required")

    @commands.command(aliases=['download_model'])
    async def gpt2_download_model(self, ctx, *, arg=None):
        print('Command gpt2_download_model triggered')

        if arg:
            if arg in VALID_MODELS:
                gpt2.download_gpt2(model_name=arg)
                await ctx.send("Model downloaded")
            else:
                await ctx.send("ERROR: Invalid argument")
        else:
            model_name = self.config['model_name']
            if model_name in VALID_MODELS:
                gpt2.download_gpt2(model_name=model_name)
            else:
                await ctx.send("ERROR: Invalid model_name in config")

    @commands.command(aliases=['reset_config'])
    async def gpt2_reset_config(self, ctx):
        print('Command gpt2_reset_config triggered')
        self.reset_config()
        await ctx.send('Config reset')

    def is_model_downloaded(self):
        model_name = self.config['model_name']
        return os.path.exists(f'models/{model_name}')

    def update_config(self, write=True, **kwargs):
        for key in kwargs:
            if key in self.config:
                self.config[key] = kwargs[key]
            else:
                print(f'Invalid config key: {key}')

        if write:
            self.write_config()

    def reset_config(self, write=True):
        self.config = DEFAULT_CONFIG

        if write:
            self.write_config()

    def load_config(self, write_if_default=True):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as file:
                for line in file:
                    key, value = line.rstrip().split('=')
                    self.config[key] = value
        else:
            self.reset_config(write_if_default)

    def write_config(self):
        with open(CONFIG_PATH, 'w+') as file:
            file.truncate()  # Erase contents of config file
            for key in self.config:
                file.write(f'{key}={self.config[key]}\n')


def setup(client):
    client.add_cog(Gpt2(client))
