import discord
import pronunciation.pronunciation as pronunciation
from discord import app_commands
from dotenv import dotenv_values
from gr_datetime.gr_date import get_full_date
from help.help import HelpMessage
from utils import fix_greek_spelling
from wordref.wordref import Wordref


class MyClient(discord.Client):
    def __init__(self, _intents: discord.Intents) -> None:
        super().__init__(intents=_intents)
        self.synced = False

    async def on_ready(self) -> None:
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"\033[32mBot is ready! {self.user}\033[0m")

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents)
tree = app_commands.CommandTree(client)


async def template_command(
    interaction: discord.Interaction,
    word: str | None,
    gr_en: bool,
    hide_words: bool,
    min_sentences_shown: int,
    max_sentences_shown: int,
):
    wordref = Wordref(word, gr_en, hide_words, min_sentences_shown, max_sentences_shown)
    wordref_embed = wordref.fetch_embed()

    # In case of failure, try again once with fixed spelling.
    if wordref_embed is None and word is not None:
        original_word = word
        word = fix_greek_spelling(word)
        print(f"Converted {original_word=} to {word=}")
        wordref = Wordref(word, gr_en, hide_words, min_sentences_shown, max_sentences_shown)
        wordref_embed = wordref.fetch_embed()

    if wordref_embed is None:
        await interaction.response.send_message("The command did not succeed.")
    else:
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


@tree.command(name="forvo", description="Returns a link with a forvo pronunciation")
async def forvo(interaction: discord.Interaction, word: str):
    # We do not always want to fix the greek spelling because valid words may be
    # modified by the query to `fix_greek_spelling`: ταξίδια => ταξίδι.

    message, audio_link, audio_file = pronunciation.get_pronunciation(word)

    # In case of failure, try again once with fixed spelling.
    if audio_link is None:
        word = fix_greek_spelling(word)
        message, audio_link, audio_file = pronunciation.get_pronunciation(word)

    if audio_link is None:
        await interaction.response.send_message(f"Could not find the word {word}!")
        return
    assert audio_file is not None
    file = discord.File(audio_file, filename=f"{word}.mp3")
    await interaction.response.send_message(file=file, content=message)


if __name__ == "__main__":
    config = dotenv_values(".env")
    client.run(config["TOKEN"])
