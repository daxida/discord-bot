import discord
from wordref.longest import highlightSynonyms
import urllib

class Entry:
    def __init__(self, link: str, gr_word: str, GrEn: bool, is_random: bool):
        self.link = link
        self.gr_word = gr_word
        self.GrEn = GrEn
        self.is_random = is_random

        self.en_word = None
        self.gr_synonyms = set()
        self.en_synonyms = set()
        self.sentences = set()
        self.POS = "" # Parts of speech
        self.is_good_entry = False

    def diagnostic(self):
        if not self.link:
            print(f"Exiting, couldn't find the link.")
            return
        if not self.gr_word:
            print(f"Exiting, couldn't find the greek word.")
            return
        if not self.en_word:
            print(f"Exiting, couldn't find the english word.")
            return
        if not self.gr_synonyms:
            print(f"Exiting, couldn't find a greek synonym.")
            return
        if not self.en_synonyms:
            print(f"Exiting, couldn't find an english synonym.")
            return
        if not self.sentences:
            print(f"Exiting, couldn't find any sentence.")
            return
        if not self.POS:
            print(f"Couldn't find POS.")

        self.is_good_entry = True

    def sort_by_contains_word(self):
        self.sentences = list(self.sentences)
        if self.GrEn:
            self.sentences.sort(
                key=lambda pair: self.gr_word in pair[0], reverse=True)
        else:
            self.sentences.sort(
                key=lambda pair: self.en_word in pair[0], reverse=True)

    def debug(self, amount_sentences_shown=10):
        ''' Stringifies the entry in a debug format '''

        print()
        print("#"*70)

        # Some sortings for easier reading (CARE IT CHANGES THE SET TO LIST).
        self.gr_synonyms = sorted(self.gr_synonyms)
        self.en_synonyms = sorted(self.en_synonyms)
        self.sentences = sorted(self.sentences)

        msg = "\n"
        msg += f"{self.link}\n"
        msg += "\n"
        msg += f"Greek word: --------- {self.gr_word}\n"
        msg += f"English word: ------- {self.en_word}\n"
        msg += f"POS: ---------------- {self.POS}\n"
        msg += "\n"
        msg += f"Greek synonyms: ----- {self.gr_synonyms}\n"
        msg += f"English synonyms: --- {self.en_synonyms}\n"
        msg += "\n"
        for idx, (gsen, esen) in enumerate(list(self.sentences)[0:amount_sentences_shown]):
            msg += f"> {idx + 1}. {gsen}\n"
            msg += f"> {idx + 1}. {highlightSynonyms(gsen, self.gr_synonyms)}\n"
            msg += f"> {idx + 1}. {esen}\n"
            msg += f"> {idx + 1}. {highlightSynonyms(esen, self.en_synonyms)}\n"

        print(msg)

        # OPENS THE LINK IN A NEW TAB
        # open_website = input('Type 1 to open the webpage\n')
        open_website = "1"
        if open_website == "1":
            tmp = self.link.replace("https://", "")
            encoded_url = urllib.parse.quote(f'{tmp}')
            # webbrowser.open_new(f"https://{encoded_url}")
            print(f"https://{encoded_url}")


    def to_embed(self, amount_sentences_shown=10):
        ''' 
        Turns the entry into a Discord embed.
        https://plainenglish.io/blog/send-an-embed-with-a-discord-bot-in-python
        '''

        title = "∙∙∙∙∙ " 
        if not self.GrEn:
            self.POS = None
            self.gr_word, self.en_word = self.en_word, self.gr_word
            self.sentences = [(esen, gsen) for gsen, esen in self.sentences]
        self.sort_by_contains_word()

        tail_POS = f" - *{self.POS}*" if self.POS else ""
        title   += f"{self.gr_word}{tail_POS} ∙∙∙∙∙"
        
        # desc formatting 
        desc = ""
        desc += f"**Translations:** ||{self.en_word}||\n"
        desc += "**Sentences:**\n"
        for idx, (gsen, esen) in enumerate(list(self.sentences)[0:amount_sentences_shown]):
            desc += f"> {idx + 1}. {highlightSynonyms(gsen, self.gr_synonyms)}\n"
            desc += f"> {idx + 1}. ||{highlightSynonyms(esen, self.en_synonyms)}||\n"

        footer = ""
        footer += f"Did you know the answer?" # 🇾es or 🇳o?"

        embed = discord.Embed(
            title=title, 
            url=f"{self.link}", 
            description=desc,
            color=0xFF5733,
        )
        
        # embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
        embed.set_footer(text=footer)

        return embed
