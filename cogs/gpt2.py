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
    """
    Convert the config into the correct format for arguments for the generate function
    The conversion for each argument is determined by the argument's name and CONFIG_KEY_PARSER
    :param arguments: A dictionary from an argument name to a string representing the value for that argument
    :return: A dictionary from an argument name to the value to be passed for that argument
    """
    return_value = {}
    for key in arguments:
        return_value[key] = CONFIG_KEY_PARSER[key](arguments[key])

    return return_value


def is_valid_config(config):
    """
    :param config: A string representing the name of a config
    :return: Whether or not the config is recognised by this program
    """
    return config in CONFIG_KEY_PARSER


def is_valid_config_value(config, value):
    """
    :param config: A string representing the name of a config
    :param value: A string representing a value for the config
    :return: Whether or not the the value for a recognised config is in the correct format
    """
    try:
        CONFIG_KEY_PARSER[config](value)
    except ValueError or KeyError:
        return False
    return True


class Gpt2(commands.Cog):

    def __init__(self, client):
        """
        Read the config from the file at the path CONFIG_PATH, if the config file is not in the expected format or
        contains a config that isn't recognised, the config is loaded from the dictionary DEFAULT_CONFIG.

        Initialise a TensorFlow session for gpt2 then load the GPT2 model as determined by the config.

        NOTE: If the config is modified after the DEFAULT_CONFIG has been loaded it, it will be overwritten.
        """
        self.client = client
        self.config = {}
        self.load_config(False)

        self.sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(self.sess, model_name=self.config['model_name'])

    @commands.command(aliases=['generate', 'gpt2'])
    async def gpt2_generate(self, ctx, *, arg=None):
        """
        Generate a text sample from a given prompt using GPT-2.
        The arguments and their values for the generation is determined by the config.
        :param arg: The prompt to generate the text sample on
        """
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
        """
        Set the name of the GPT-2 model in the config by setting model_name if it's a valid model name.
        :param arg: The value to set model_name to
        """
        print('Command gpt2_set_model triggered')
        if arg:
            if arg in VALID_MODELS:
                self.update_config(model_name=arg)
            else:
                await ctx.send(f"ERROR: Invalid model name {arg}")
        else:
            await ctx.send("ERROR: Argument required")

    @commands.command(aliases=['set_length'])
    async def gpt2_set_length(self, ctx, *, arg=None):
        """
        Set the length of the samples produced by GPT-2 when producing samples.
        The value represents the number of tokens (i.e. words) each produced sample will contain.
        :param arg: The value to set length to. This must be a positive integer
        """
        print('Command gpt2_set_length triggered')
        if arg:
            try:
                i = int(arg)
                assert i > 0
            except ValueError or AssertionError:
                ctx.send("ERROR: Argument must be a positive integer number")
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
    async def gpt2_reset_config(self, ctx, *, arg=None):
        print('Command gpt2_reset_config triggered')
        if arg:
            await ctx.send('Argument not allowed')
        else:
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
