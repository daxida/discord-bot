import discord
from discord import app_commands
from dotenv import dotenv_values
from help.help import HelpMessage
from wordref.wordref import Wordref
from gr_datetime.gr_date import get_full_date


class MyClient(discord.Client):
    def __init__(self, _intents):
        super().__init__(intents=_intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"\033[32mBot is ready! {self.user}\033[0m")

    async def on_message(self, message):
        if message.author == self.user:
            return


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents)
tree = app_commands.CommandTree(client)


async def template_command(
    interaction: discord.Interaction,
    word: str,
    gr_en: bool,
    hide_words: bool,
    min_sentences_shown: int,
    max_sentences_shown: int,
):
    wordref = Wordref(word, gr_en, hide_words, min_sentences_shown, max_sentences_shown)
    wordref_embed = wordref.embed()
    await interaction.response.send_message(embed=wordref_embed)
    # try:
    #     wordref = Wordref(word, gr_en, hide_words, amount_sentences_shown)
    #     wordref_embed = wordref.embed()
    #     await interaction.response.send_message(embed=wordref_embed)
    # except Exception as e:
    #     await interaction.response.send_message(content=f"Error: {e}")


@tree.command(name="wotdgr", description="Prompts a random Greek word from Wordref")
async def wotdgr(interaction: discord.Interaction):
    await template_command(interaction, None, True, True, 1, 3)


@tree.command(name="wotden", description="Prompts a random english word from Wordref")
async def wotden(interaction: discord.Interaction):
    await template_command(interaction, None, False, True, 1, 3)


@tree.command(name="searchgr", description="Searches the given Greek word in Wordref (supports greeklish)")
async def searchgr(interaction: discord.Interaction, word: str):
    await template_command(interaction, word, True, False, 0, 2)


@tree.command(name="searchen", description="Searches the given english word in Wordref")
async def searchen(interaction: discord.Interaction, word: str):
    await template_command(interaction, word, False, False, 0, 2)


@tree.command(name="helprafa", description="Explains rafabot")
async def helprafa(interaction: discord.Interaction):
    embed = discord.Embed(title="Explains rafabot", description=HelpMessage().message, color=0xFF5733)
    await interaction.response.send_message(embed=embed)


@tree.command(name="date", description="Prompts date in Fidis format")
async def date(interaction: discord.Interaction):
    await interaction.response.send_message(get_full_date())


if __name__ == "__main__":
    config = dotenv_values(".env")
    client.run(config["TOKEN"])
