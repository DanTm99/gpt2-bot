# GPT2 Bot

A simple discord bot written in Python that utilises existing Python libraries to allow for simple interaction with [OpenAI](https://openai.com)'s [GPT-2 text generator](https://openai.com/blog/better-language-models/).

## Setup

Clone the repository and navigate into it:
```shell
git clone https://github.com/DanTm99/gpt2-bot.git
cd gpt2-bot
```

Install the required packages:
```shell
pip3 install -r requirements.txt
```

To use this without GPU support use the following command instead:
```shell
pip3 install -r requirements-no-gpu.txt
```

This has only been tested with the versions of the requirements as given in `requirements.txt`. You may update packages beyond these versions if you wish.


**TensorFlow 2.0 is currently not supported** and the gpt-2-simple package will throw an assertion if it's installed, so TensorFlow 1.15.2 is recommended.

Create `apikey.txt` containing the api key for your bot:
```shell
echo "[API_KEY]" > apikey.txt
```
Replace `[API_KEY]` with your api key.

Run `bot.py` to start the bot:
```shell
python3 bot.py
```

## Usage

This bot responds to commands sent to any Discord server it's a part of. By default messages must start with `;;` to be recognised as a command. This can be changed by changing `COMMAND_PREFIX` in `bot.py`.

`;;download_model` downloads the GPT-2 model and must be used to generate text.

`;;generate [prompt]` generates text that starts with an optional prompt.