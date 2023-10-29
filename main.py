import discord
from discord import app_commands
from dotenv import dotenv_values
from help.help import HelpMessage
from wordref.wordref import Wordref
from gr_datetime.gr_date import get_full_date


config = dotenv_values(".env")


class MyClient(discord.Client):
    def __init__(self, _intents):
        super().__init__(intents=_intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"Bot is ready! {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents)
tree = app_commands.CommandTree(client)


@tree.command(name="wotdgr", description="Prompts a random Greek word from Wordref")
async def self(interaction: discord.Interaction):
    try:
        embedded_msg = Wordref(word=None, GrEn=True).embed()
    except Exception as e:
        embedded_msg = f"Error: {str(e)}"
    finally:
        if isinstance(embedded_msg, discord.Embed):
            await interaction.response.send_message(embed=embedded_msg)
        else:
            await interaction.response.send_message(content=embedded_msg)


@tree.command(name="wotden", description="Prompts a random english word from Wordref")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(
        embed=Wordref(word=None, GrEn=False).embed()
    )


@tree.command(name="searchgr", description="Searches the given greek word in Wordref")
async def self(interaction: discord.Interaction, word: str):
    await interaction.response.send_message(embed=Wordref(word=word, GrEn=True).embed())


@tree.command(name="searchen", description="Searches the given english word in Wordref")
async def self(interaction: discord.Interaction, word: str):
    await interaction.response.send_message(
        embed=Wordref(word=word, GrEn=False).embed()
    )


@tree.command(name="helprafa", description="Explains rafabot")
async def self(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Explains rafabot", description=HelpMessage().message, color=0xFF5733
    )
    await interaction.response.send_message(embed=embed)


@tree.command(name="date", description="Prompts date in Fidis format")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(get_full_date())


if __name__ == "__main__":
    client.run(config["TOKEN"])
