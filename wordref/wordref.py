import requests
import os
import re

from wordref.entry import Entry

from bs4 import BeautifulSoup
from typing import List


attributes_el = {
    'επίθ': 'adj',
    'επίθ άκλ': 'TODO',

    'φρ ως': 'TODO', # φράση ως ... πχ. ουσ θηλ

    'ουσ ουδ': 'neut. n.',
    'ουσ αρσ': 'masc. n.',
    'ουσ θηλ': 'fem. n.',

    'ρ έκφρ':      'TODO',
    'ρ αμ + επίρ': 'TODO',
    'ρ αμ':        'TODO',
    'ρ μ + πρόθ':  'TODO',
    'ρ μ':         'TODO',

    'έκφρ': 'TODO',
    'περίφρ':      'TODO',
}
attributes_en = {
    'adj',
    'adv',
    ' n',

    'v expr',
    'vi',
    'vtr phrasal sep',
    'vtr + prep',
    'vtr',
}


def is_english(word: str) -> bool:
    return all(ord(ch) < 200 for ch in word)


def parse_words(text: str) -> List[str]:
    ''' 
    Wordref groups the words together with their attributes.
    This extracts the word by deleting the attributes from a set list.
    '''

    attributes = attributes_en if is_english(text) else attributes_el

    while True:
        original_text = text
        text = text.strip()
        for att in attributes:
            pattern = re.escape(att) + r'$'
            text = re.sub(pattern, '', text)
            text = re.sub(r'\+$', '', text)
        if original_text == text:
            break

    return text.split(', ')


class Wordref:
    wordref_url = "https://www.wordreference.com"

    def __init__(self, word: str, GrEn: bool, amount_sentences_shown=5):
        self.word = word
        self.GrEn = GrEn
        self.amount_sentences_shown = amount_sentences_shown
        self.entry = None

    def run(self):
        ''' Tries to fetch an entry object. Stores it in self.entry '''

        self.url = f"{self.wordref_url}/random/gren"  # default is random

        if self.word:
            self.word = self.word.strip()
            if is_english(self.word):
                self.url = f"{self.wordref_url}/gren/{self.word}"
            else:
                self.url = f"{self.wordref_url}/engr/{self.word}"

        found, message = False, None

        while not found:
            found, entry = self.fetch()

            # To prevent Discord message length error later on:
            # HTTPException: 400 Bad Request (error code: 40060)
            if len(entry.to_embed(self.amount_sentences_shown)) >= 2000:
                found = False

        self.entry = entry

    def debug(self):
        ''' Tries to fetch an entry. Then returns the stringified version. '''
        if not self.entry:
            self.run()
        return self.entry.debug(self.amount_sentences_shown)

    def embed(self):
        ''' Tries to fetch an entry. Then returns the embed version. '''
        if not self.entry:
            self.run()
        return self.entry.to_embed(self.amount_sentences_shown)

    def fetch(self, min_sentences=1):
        ''' Fetches an entry '''

        assert min_sentences <= self.amount_sentences_shown

        response = requests.get(self.url)
        if response.status_code != 200:
            print(f"Couldn't find {word}, sorry!")
            return False, None

        soup = BeautifulSoup(response.text, 'html.parser')
        gr_word = soup.find("h3", {"class": "headerWord"}).text
        link = f"{self.wordref_url}/gren/{gr_word}"

        entry = Entry(link, gr_word, self.GrEn, is_random="random" in self.url)

        for res in soup.find_all("table", {"class": "WRD"}):
            # WORDS
            for item in res.find_all("tr", {"class": ["even", "odd"]}):
                FrWrd = item.find("td", {"class": "FrWrd"})
                ToWrd = item.find("td", {"class": "ToWrd"})

                if FrWrd and ToWrd:
                    en_text = ToWrd.text
                    gr_text = FrWrd.text

                    if is_english(FrWrd.text):
                        en_text, gr_text = gr_text, en_text

                    if not entry.en_word:
                        entry.en_word = en_text.strip()

                    # POS 
                    # Fetches the POS of the queried word
                    if not entry.POS:
                        if len(gr_text.split()) > 1 and entry.gr_word in gr_text:
                            entry.POS = gr_text.replace(entry.gr_word, '').strip()
                        if ',' in entry.POS:
                            entry.POS = ''

                    # SYNONYMS
                    for word in parse_words(gr_text):
                        entry.gr_synonyms.add(word)
                    for word in parse_words(en_text):
                        entry.en_synonyms.add(word)

            # SENTENCES

            # Options:
            # 1 -> Stores every pair (even when there are
            #      two translations to a sentence)
            # Ex.
            # (EN) The supposed masterpiece discovered in the old house was a fake.
            # (T1) Το υποτιθέμενο έργο τέχνης που βρέθηκε στο παλιό σπίτι ήταν πλαστό.
            # (T2) Το δήθεν έργο τέχνης που βρέθηκε στο παλιό σπίτι ήταν πλαστό.

            # 2 -> Store only one pair giving priority to containing the original word.

            gr_sentence = ''
            en_sentence = ''
            for item in res.find_all("tr", {"class": ["even", "odd"]}):
                FrEx = item.find("td", {"class": "FrEx"})
                ToEx = item.find("td", {"class": "ToEx"})

                # Resets buffered sentences
                if not FrEx and not ToEx:
                    en_sentence = ''
                    gr_sentence = ''

                # Buffers sentences to then group them in pairs
                if FrEx:
                    en_sentence = FrEx.text
                if ToEx:
                    gr_sentence = ToEx.text
                    # Delete "Translation not found" message
                    if 'Αυτή η πρόταση δεν είναι μετάφραση της αγγλικής πρότασης.' in gr_sentence:
                        gr_sentence = ''

                # Groups them in pairs
                if gr_sentence and en_sentence:
                    # Option 1
                    # entry.sentences.add((gr_sentence, en_sentence))

                    # Option 2
                    stored_already = False
                    for stored_pair in entry.sentences:
                        stored_greek, stored_english = stored_pair
                        if self.GrEn is True:
                            if stored_english == en_sentence:
                                stored_already = True
                                # Our stored answer is already fine
                                if self.word in stored_greek:
                                    break
                                else:
                                    entry.sentences.remove(
                                        (stored_greek, stored_english))
                                    entry.sentences.add(
                                        (gr_sentence, en_sentence))
                                    break
                        # We want our english sentences containing "word"
                        else:
                            if stored_greek == gr_sentence:
                                stored_already = True
                                # Our stored answer is already fine
                                if self.word in stored_english:
                                    break
                                else:
                                    entry.sentences.remove(
                                        (stored_greek, stored_english))
                                    entry.sentences.add(
                                        (gr_sentence, en_sentence))
                                    break
                    if not stored_already:
                        entry.sentences.add((gr_sentence, en_sentence))

        entry.diagnostic()
        found = entry.is_good_entry

        # entry.debug(self.amount_sentences_shown)
        # message = entry.to_plain_message(self.amount_sentences_shown)

        return found, entry


# print(Wordref(word="ταυτότητα", GrEn=True).debug())
