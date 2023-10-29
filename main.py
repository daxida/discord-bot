import discord
from discord import app_commands
from dotenv import dotenv_values
from wordref.wordref import Wordref
from gr_datetime.gr_date import get_date


config = dotenv_values('.env')


class MyClient(discord.Client):
    def __init__(self, _intents):
        super().__init__(intents=_intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'Bot is ready! {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents)
tree = app_commands.CommandTree(client)

# Base command. Prompts a random word entry from wordref.
@tree.command(
    name="wotdgr",
    description="Prompts a random Greek word entry from Wordref"
)
async def self(interaction: discord.Interaction):
    try:
        embedded_msg = Wordref(word=None, GrEn=True).embed()
    except requests.exceptions.RequestException as e:
        embedded_msg = f"Request Exception: {str(e)}"
    except Exception as e:
        embedded_msg = f"Error: {str(e)}"
    finally:
        if isinstance(embedded_msg, discord.Embed):
            await interaction.response.send_message(embed=embedded_msg)
        else:
            await interaction.response.send_message(content=embedded_msg)



# Prompts a random word entry from wordref but from English to Greek.
@tree.command(
    name="wotden",
    description="Prompts a random english word entry from wordref")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(embed=Wordref(word=None, GrEn=False).embed())


@tree.command(
    name="searchgr",
    description="Searches for the given greek word in wordref")
async def self(interaction: discord.Interaction, word: str):
    await interaction.response.send_message(embed=Wordref(word=word, GrEn=True).embed())


@tree.command(
    name="searchen",
    description="Prompts a random word entry from wordref")
async def self(interaction: discord.Interaction, word: str):
    await interaction.response.send_message(embed=Wordref(word=word, GrEn=False).embed())


HELP_MESSAGE = """
```You have four commands (and this help) available:
1. wotdgr ---> random greek word entry
2. wotden ---> random english word
3. searchgr -> (+greek word) searches the given greek word
4. searchen -> (+english word) searches the given english word
5. randomq --> (WIP) random greek question (from a set dabase)
6. helprafa -> prompts this help message```
"""

# https://plainenglish.io/blog/send-an-embed-with-a-discord-bot-in-python
@tree.command(
    name="helprafa",
    description="Explains rafabot")
async def self(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Explains rafabot",
        # url="https://realdrewdata.medium.com/",
        description=HELP_MESSAGE,
        color=0xFF5733
    )
    await interaction.response.send_message(embed=embed)

# Dates
@tree.command(
    name="date",
    description="Prompts date in Fidis format")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(get_date())


if __name__ == '__main__':
    client.run(config['TOKEN'])
