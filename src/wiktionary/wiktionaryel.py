"""
Wiktionary Parser for Greek Pages
Example usage: fetch_wiktionary("καλημέρα", blacklist=['Προφορά'])
Returns as a JSON containing word types and entries
"""

import json
import requests
from bs4 import BeautifulSoup
from typing import List, Any, Dict

# fmt: off
ENTRIES = [
    "Ετυμολογία", "Ετυμολογία_1", "Ετυμολογία_2", 
    "Προφορά", "Προφορά_1", "Προφορά_2",
    "Επιφώνημα", "Έκφραση", "Ουσιαστικό", 
    "Εκφράσεις", "Επίθετο", "Επίρρημα", "Συνώνυμα", "Αντώνυμα",
    "Κλιτικός_τύπος_επιθέτου", "Κλιτικός_τύπος_ουσιαστικού",
    "Πολυλεκτικοί_όροι", "Σημειώσεις"
] # Μεταφράσεις, "Σύνθετα", "Συγγενικά" cut off here
ENTRIES_EN = [
    "Etymology", "Etymology_1", "Etymology_2",
    "Pronunciation", "Pronunciation_2", "Pronunciation_3",
    "Interjection", "Interjection_2", "Expression",
    "Expression_2", "Expressions", "Noun", "Noun_2",
    "Adjective", "Adjective_2", "Adverb", "Adverb_2",
    "Related", "Synonyms", "Antonyms", "Synonyms_2", "Antonyms_2"
]
# fmt: on

def test_fetch():
    word = "καλημέρα"
    res = fetch_wiktionary(word, "greek")
    j = json.dumps(res, indent=2, ensure_ascii=False)
    print(j)


def fetch_wiktionary(
    word: str, language: str
    ) -> Dict[str, List[str]]:
        
    lang_str = "el"
    URL = "https://el.wiktionary.org/wiki/{}?printable=yes"
    if language == "english":
        lang_str = "en"
        URL = "https://en.wiktionary.org/wiki/{}?printable=yes"
    
    page = requests.get(URL.format(word))
    soup = BeautifulSoup(page.content, "html.parser")
    remove_ancient_greek(soup, language)

    entries = ENTRIES[:]
    if language == "english":
        entries = ENTRIES_EN[:]

    parts_of_speech = dict()
    for entry in entries:
        entry_elements = fetch_entries(soup, entry)
        if entry_elements is not None:
            parts_of_speech[entry] = entry_elements

    return parts_of_speech


def fetch_entries(soup: Any, entry_type: str) -> List[str] | None:
    # find position of page element with desired type
    results = soup.find(["h3", "h4"], id=entry_type)
    if not results:
        return None

    entry_elements = []
    # due to wiktionary formatting, finds body under the entry
    next_element = results.parent.find_next_sibling()

    # used for translations and other lists in divs
    if next_element and next_element.name == "div":
        list_element = next_element.find_all("li")
        if list_element:
            for element in list_element:
                # add to the entry list
                entry_elements.append(element.text)
    else:
        # these element types denote new entries so they terminate the loop
        while next_element and next_element.name not in ["h3", "h4", "h5", "div"]:
            list_element = next_element.find_all("li")
            # if only one instance of entry (e.g. only one definition)
            if not list_element:
                entry_elements.append(next_element.text)
                next_element = next_element.find_next_sibling()
            else:
                for element in list_element:
                    entry_elements.append(element.text)
                next_element = next_element.find_next_sibling()

    return entry_elements


def remove_ancient_greek(soup: Any, language: str) -> None:
    # find where the ancient greek section begins
    if language == "english":
        remove_string = "Ancient_Greek"
        stop_at_string = "Greek"
    else:
        remove_string = "Αρχαία_ελληνικά_(grc)"
        stop_at_string = None
        
    tag_to_remove = soup.find("h2", id=remove_string)
    
    if tag_to_remove:
        current_element = tag_to_remove.find_parent()
        while current_element:
            next_sibling = current_element.find_next_sibling()
            if next_sibling and stop_at_string and next_sibling.find("h2", string=stop_at_string):
                break
            
            # remove the current element and move to next sibling
            current_element.extract()
            current_element = next_sibling


if __name__ == "__main__":
    # test for successful response
    test_fetch()
