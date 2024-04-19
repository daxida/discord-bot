from wiktionary.wiktionaryel import fetch_wiktionary
from typing import List
import json
import discord


def embed_message(
    word: str, language: str, blacklist: List[str] = [], whitelist: List[str] = []
) -> discord.Embed:
    # fetch and parse wiktionary page from here
    res = fetch_wiktionary(word, language, blacklist, whitelist)

    title = f"∙∙∙∙∙ {word} ∙∙∙∙∙"
    link = f"https://el.wiktionary.org/wiki/{word}"
    description = ""

    # loop through json
    for key in res.keys():
        formatted_key = key.replace("_", " ")
        description += f"**{formatted_key}: **" + "\n"
        # formatting nonsense, some entries aren't needed
        if key == "Προφορά":
            description += "∙ " + str(res[key][0].split("\n")[0]) + "\n"
        elif key in [
            "Επίθετο",
            "Ουσιαστικό",
            "Επίρρημα",
            "Επιφώνημα",
            "Κλιτικός_τύπος_επιθέτου",
            "Κλιτικός_τύπος_ουσιαστικού",
        ]:
            for entry in res[key][1:]:
                description += "> " + str(entry.strip("\n")) + "\n"
        elif key in ["Ετυμολογία", "Προφορά"]:
            for entry in res[key]:
                description += "∙ " + str(entry.strip("\n")) + "\n"
        else:
            for entry in res[key]:
                description += "> " + str(entry.strip("\n")) + "\n"

    # create embed object
    embed = discord.Embed(title=title, url=link, description=description, color=0x3392FF)

    embed.set_footer(text=f"https://forvo.com/word/{word}/#el")

    return embed
