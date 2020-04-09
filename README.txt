GPT2 Bot

A simple discord bot written in Python that utilises existing Python libraries to allow for simple interaction with OpenAI's GPT-2 text generator.


Setup

Clone the repository and navigate into it via this command:
git clone https://github.com/DanTm99/gpt2-bot.git

To use this with your GPU you must have and NVIDIA GPU with a CUDA Compute Capability 3.5 or higher.
If you have the required hardware you must install the required software on your system as shown here: https://www.tensorflow.org/install/gpu#software_requirements

Install the required packages as normal to use this with GPU support:

Install the required packages as normal to use this with GPU support using this command:
pip3 install -r requirements.txt

To use this without GPU support use the following command instead using this command:
pip3 install -r requirements-no-gpu.txt

Create apikey.txt containing the api key for your bot using this command (replace API_KEY with your Discord bot's api key):
echo "[API_KEY]" > apikey.txt

Usage

Run bot.py to start the bot using this command:
python3 bot.py

This bot responds to commands sent to any Discord server it's a part of.
By default messages must start with ;; to be recognised as a command. This can be changed by changing COMMAND_PREFIX in bot.py.

;;download_model downloads the GPT-2 model and must be used to generate text.

;;generate [prompt] generates text that starts with an optional prompt.