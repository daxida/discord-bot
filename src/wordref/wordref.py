import re
from typing import List

import requests
from bs4 import BeautifulSoup

from wordref.entry import Entry
from wordref.greeklish import greeklish_to_greek

ATTRIBUTES_EL = {
    "επίθ": "adj",
    "επίθ άκλ": "TODO",
    "φρ ως": "TODO",  # φράση ως ... πχ. ουσ θηλ
    "ουσ ουδ": "neut. n.",
    "ουσ αρσ": "masc. n.",
    "ουσ θηλ": "fem. n.",
    "ρ έκφρ": "TODO",
    "ρ αμ + επίρ": "TODO",
    "ρ αμ": "TODO",
    "ρ μ + πρόθ": "TODO",
    "ρ μ": "TODO",
    "έκφρ": "TODO",
    "περίφρ": "TODO",
}
ATTRIBUTES_EN = {
    "adj",
    "adv",
    " n",
    "v expr",
    "vi",
    "vtr phrasal sep",
    "vtr + prep",
    "vtr",
}
TAG = "\033[33mWORDREF:\033[0m"


def is_english(word: str) -> bool:
    return all(ord(ch) < 200 for ch in word)


def parse_words(text: str) -> List[str]:
    """
    Wordref groups the words together with their attributes.
    This extracts the word by deleting the attributes from a set list.
    """

    attributes = ATTRIBUTES_EN if is_english(text) else ATTRIBUTES_EL

    while True:
        original_text = text
        text = text.strip()
        for att in attributes:
            pattern = re.escape(att) + r"$"
            text = re.sub(pattern, "", text)
            text = re.sub(r"\+$", "", text)
        if original_text == text:
            break

    return text.split(", ")


class Wordref:
    """
    Deals with the scraping of Wordref.

    Everything is stored in an Entry class, where the suitability logic and formatting is done.
    """

    wordref_url = "https://www.wordreference.com"

    def __init__(
        self, word: str, gr_en: bool, hide_words: bool, min_sentences_shown: int, max_sentences_shown: int
    ):
        self.word = word
        self.gr_en = gr_en
        self.hide_words = hide_words
        self.min_sentences_shown = min_sentences_shown
        self.max_sentences_shown = max_sentences_shown

        self.is_random = word is None

        # Support greeklish (try fetching the greekified word)
        if gr_en and word and is_english(word):
            self.word = greeklish_to_greek(word)

    def debug(self) -> None:
        entry = self.fetch_entry()
        return entry.debug(self.amount_sentences_shown)

    def embed(self):
        max_iterations = 5
        for _ in range(max_iterations):
            entry = self.fetch_entry()
            entry.add_embed()

            if entry.is_valid_embed:
                print(f"{TAG} found a valid embed for {self.word}")
                return entry.embed

        raise Exception(f"Couldn't fetch an embed in {max_iterations} tries")

    def fetch_entry(self) -> Entry:
        max_iterations = 5
        for _ in range(max_iterations):
            entry = self.try_fetch_entry()

            if entry.is_valid_entry:
                return entry

        raise Exception(f"Couldn't fetch an entry in {max_iterations} tries")

    def try_fetch_entry(self) -> Entry:
        if self.is_random:
            extension = "random/gren"
        else:
            self.word = self.word.strip()
            extension = f"{'engr' if is_english(self.word) else 'gren'}/{self.word}"

        url = f"{Wordref.wordref_url}/{extension}"

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Account for the query word being written without accents by scraping the accented word.
        self.word = (
            soup.find("table", {"class": "WRD"})
            .find("tr", {"class": "even"})
            .find("td", {"class": "FrWrd"})
            .strong.text.split()[0]
        )
        link = f"{Wordref.wordref_url}/gren/{self.word}"

        entry = Entry(
            link,
            self.word,
            self.gr_en,
            self.hide_words,
            self.min_sentences_shown,
            self.max_sentences_shown,
            self.is_random,
        )

        print(f"{TAG} requesting {url}")
        print(f"{TAG} trying to fetch '{self.word}' ({link})")
        print(f"{TAG}\n{entry}")

        for res in soup.find_all("table", {"class": "WRD"}):
            self.try_fetch_word(res, entry)
            self.try_fetch_sentences(res, entry)

        return entry

    def try_fetch_word(self, res, entry: Entry):
        for item in res.find_all("tr", {"class": ["even", "odd"]}):
            FrWrd = item.find("td", {"class": "FrWrd"})
            ToWrd = item.find("td", {"class": "ToWrd"})

            if not FrWrd or not ToWrd:
                continue

            en_text = ToWrd.text
            gr_text = FrWrd.text

            if is_english(FrWrd.text):
                en_text, gr_text = gr_text, en_text

            if not entry.en_word:
                entry.en_word = en_text.strip()

            # Parts of speech
            if (entry.gr_pos is None) and entry.gr_word:
                if len(gr_text.split()) > 1 and entry.gr_word in gr_text:
                    entry.gr_pos = gr_text.replace(entry.gr_word, "").strip()
                    if "," in entry.gr_pos:
                        entry.gr_pos = ""

            # Synonyms
            for word in parse_words(gr_text):
                entry.gr_synonyms.add(word)
            for word in parse_words(en_text):
                entry.en_synonyms.add(word)

    def try_fetch_sentences(self, res, entry: Entry):
        # Options:
        # 1 -> Stores every pair (even when there are
        #      two translations to a sentence)
        # Ex.
        # (EN) The supposed masterpiece discovered in the old house was a fake.
        # (T1) Το υποτιθέμενο έργο τέχνης που βρέθηκε στο παλιό σπίτι ήταν πλαστό.
        # (T2) Το δήθεν έργο τέχνης που βρέθηκε στο παλιό σπίτι ήταν πλαστό.

        # 2 -> Store only one pair giving priority to containing the original word.

        gr_sentence = ""
        en_sentence = ""
        for item in res.find_all("tr", {"class": ["even", "odd"]}):
            FrEx = item.find("td", {"class": "FrEx"})
            ToEx = item.find("td", {"class": "ToEx"})

            # Resets buffered sentences
            if not FrEx and not ToEx:
                en_sentence = ""
                gr_sentence = ""

            # Buffers sentences to then group them in pairs
            if FrEx:
                en_sentence = FrEx.text
            if ToEx:
                gr_sentence = ToEx.text
                # Delete "Translation not found" message
                if "Αυτή η πρόταση δεν είναι μετάφραση της αγγλικής πρότασης." in gr_sentence:
                    gr_sentence = ""

            # Groups them in pairs
            if gr_sentence and en_sentence:
                # Option 1
                # entry.sentences.add((gr_sentence, en_sentence))

                # Option 2
                stored_already = False
                for stored_pair in entry.sentences:
                    stored_greek, stored_english = stored_pair
                    if self.gr_en is True:
                        if stored_english == en_sentence:
                            stored_already = True
                            # Our stored answer is already fine
                            if self.word and self.word in stored_greek:
                                break
                            else:
                                entry.sentences.remove((stored_greek, stored_english))
                                entry.sentences.add((gr_sentence, en_sentence))
                                break
                    # We want our english sentences containing "word"
                    else:
                        if stored_greek == gr_sentence:
                            stored_already = True
                            # Our stored answer is already fine
                            if self.word and self.word in stored_english:
                                break
                            else:
                                entry.sentences.remove((stored_greek, stored_english))
                                entry.sentences.add((gr_sentence, en_sentence))
                                break
                if not stored_already:
                    entry.sentences.add((gr_sentence, en_sentence))
