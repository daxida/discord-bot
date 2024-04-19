Discord bot for learning greek at the [greek server](https://discord.gg/greek).

## How to use

First of all, you will need a discord bot. For how to set it up you can check the documentation [here](https://discordpy.readthedocs.io/en/stable/discord.html).

1. (Optional) Create a virtual environment and activate it: `python3 -m venv venv`.
2. Install the required packages: `pip install -r requirements.txt`.
3. Get your TOKEN from [here](https://discord.com/developers/applications).
4. Create a `.env` file in the root directory with the following format:
   <br>`TOKEN="Mytoken"`.
5. Launch the bot `python3 src/main.py`

## Notes
The formatting is done with `ruff`. If you want to contribute, it will be appreciated (but not needed) if you could run `ruff format` prior to committing. You can install it with `pip install ruff`.