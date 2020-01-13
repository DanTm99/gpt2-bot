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
# A dictionary from argument names to a lambda that determines how to parse the string representing its value
CONFIG_KEY_PARSER = {
    'model_name': lambda s: s,
    'length': lambda i: int(i),
    'temperature': lambda f: float(f),
    'top_k': lambda i: int(i),
    'top_p': lambda f: float(f),
    'include_prefix': lambda b: b == 'True',
}


def parse_generate_arguments(arguments):
    return_value = {}
    for key in arguments:
        return_value[key] = CONFIG_KEY_PARSER[key](arguments[key])

    return return_value


def is_valid_config(config):
    """

    :param config: A string representing the name of a config
    :return: Whether or not the config is used by this program
    """
    return config in CONFIG_KEY_PARSER


def is_valid_config_value(config, value):
    try:
        CONFIG_KEY_PARSER[config](value)  # Check if the parser for this config works
    except ValueError or KeyError:
        return False
    return True


class Gpt2(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.sess = gpt2.start_tf_sess()

        self.config = {}
        # If the config file is invalid the default config will be loaded
        # If the config is modified via command this will overwrite the invalid config file
        self.load_config(False)
        gpt2.load_gpt2(self.sess, model_name=self.config['model_name'])

    @commands.command(aliases=['generate', 'gpt2'])
    async def gpt2_generate(self, ctx, *, arg=None):
        print('Command gpt2_generate triggered')
        await ctx.send("Generating...")
        if arg:
            if self.is_model_downloaded():
                if arg:
                    args = parse_generate_arguments(self.config)
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

    @commands.command(aliases=['config'])
    async def gpt2_set_config(self, ctx, *, arg=None):
        print('Command gpt2_set_config triggered')
        if arg:
            configs = {key: value for [key, value] in [a.split('=') for a in arg.split(' ')]}
            for config in configs:
                if not is_valid_config(config):  # Check if the config name exists
                    await ctx.send(f"ERROR: Invalid config name {config}")
                    return
                elif not is_valid_config_value(config, configs[config]):
                    await ctx.send(f"ERROR: Invalid config {config}={configs[config]}")
                    return
            self.update_config(**configs)
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
            if is_valid_config(key):
                value = kwargs[key]
                if is_valid_config_value(key, value):
                    self.config[key] = value
                else:
                    print(f'Invalid config {key}={value}')
            else:
                print(f'Invalid config key: {key}')

        if write:
            self.write_config()

    def reset_config(self, write=True):
        self.config = DEFAULT_CONFIG.copy()

        if write:
            self.write_config()

    def load_config(self, write_if_default=True):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as file:
                for line in file:
                    key, value = line.rstrip().split('=')
                    if is_valid_config_value(key, value):
                        self.config[key] = value
                    else:
                        self.reset_config(write_if_default)  # Load default config instead
                        return
        else:
            self.reset_config(write_if_default)

    def write_config(self):
        with open(CONFIG_PATH, 'w+') as file:
            file.truncate()  # Erase contents of config file
            for key in self.config:
                file.write(f'{key}={self.config[key]}\n')


def setup(client):
    client.add_cog(Gpt2(client))
