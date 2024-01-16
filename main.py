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


async def template_command(interaction: discord.Interaction, word: str, GrEn: bool):
    try:
        wordref_embed = Wordref(word=word, GrEn=GrEn).embed()
        await interaction.response.send_message(embed=wordref_embed)
    except Exception as e:
        await interaction.response.send_message(content=f"Error: {e}")


@tree.command(name="wotdgr", description="Prompts a random Greek word from Wordref")
async def wotdgr(interaction: discord.Interaction):
    await template_command(interaction, word=None, GrEn=True)


@tree.command(name="wotden", description="Prompts a random english word from Wordref")
async def wotden(interaction: discord.Interaction):
    await template_command(interaction, word=None, GrEn=False)


@tree.command(name="searchgr", description="Searches the given Greek word in Wordref")
async def searchgr(interaction: discord.Interaction, word: str):
    await template_command(interaction, word=word, GrEn=True)


@tree.command(name="searchen", description="Searches the given english word in Wordref")
async def searchen(interaction: discord.Interaction, word: str):
    await template_command(interaction, word=word, GrEn=False)


@tree.command(name="helprafa", description="Explains rafabot")
async def helprafa(interaction: discord.Interaction):
    embed = discord.Embed(title="Explains rafabot", description=HelpMessage().message, color=0xFF5733)
    await interaction.response.send_message(embed=embed)


@tree.command(name="date", description="Prompts date in Fidis format")
async def date(interaction: discord.Interaction):
    await interaction.response.send_message(get_full_date())


if __name__ == "__main__":
    client.run(config["TOKEN"])
