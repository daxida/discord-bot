"""
Wiktionary Parser for Greek Pages
Example usage: fetch_wiktionary("καλημέρα", blacklist=['Προφορά'])
Returns as a JSON containing word types and entries
"""

import json
import requests
from bs4 import BeautifulSoup
from typing import List, Any, Dict

URL = "https://el.wiktionary.org/wiki/{}?printable=yes"

# fmt: off
ENTRIES = [
    "Ετυμολογία", "Ετυμολογία_1", "Ετυμολογία_2", 
    "Προφορά", "Προφορά_1", "Προφορά_2",
    "Επιφώνημα", "Εκφράσεις",
    "Ουσιαστικό", "Επίθετο", "Επίρρημα", "Μεταφράσεις",
    "Συγγενικά", "Συνώνυμα", "Αντώνυμα", "Σύνθετα", "Δείτε_επίσης",
    "Κλιτικός_τύπος_επιθέτου", "Κλιτικός_τύπος_ουσιαστικού",
    "Πολυλεκτικοί_όροι", "Σημειώσεις"
]
# fmt: on


def test_fetch():
    word = "καλημέρα"
    res = fetch_wiktionary(word)

    j = json.dumps(res, indent=2, ensure_ascii=False)
    print(j)


def fetch_wiktionary(word: str, blacklist: List[str] = [], whitelist: List[str] = []) -> Dict[str, List[str]]:
    page = requests.get(URL.format(word))
    soup = BeautifulSoup(page.content, "html.parser")

    remove_ancient_greek(soup)

    entries = ENTRIES[:]
    if whitelist:
        entries = whitelist
    for entry in blacklist:
        entries.remove(entry)

    parts_of_speech = dict()
    for entry in entries:
        entry_elements = fetch_entries(soup, entry)
        if entry_elements is not None:
            parts_of_speech[entry] = entry_elements

    return parts_of_speech


def fetch_entries(soup: Any, entry_type: str) -> List[str] | None:
    # find position of page element with desired type
    results = soup.find("span", id=entry_type)
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


def remove_ancient_greek(soup: Any) -> None:
    # find where the ancient greek section begins
    tag_to_remove = soup.find("span", id="Αρχαία_ελληνικά_(grc)")
    if tag_to_remove:
        parent = tag_to_remove.find_parent()
        # remove everything under ancient section (always below modern)
        for sibling in parent.find_next_siblings():
            sibling.extract()


if __name__ == "__main__":
    # test for successful response
    test_fetch()