import requests
from bs4 import BeautifulSoup

GREEKLISH = str.maketrans(
    {
        "a": "α",
        "b": "β",
        "c": "σ",  # There's no direct equivalent for 'c' in Greek, but 'σ' is commonly used in borrowed words
        "d": "δ",
        "e": "ε",
        "f": "φ",
        "g": "γ",
        "h": "η",
        "i": "ι",
        "j": "τζ",  # The Greek equivalent of 'j' is 'τζ'
        "k": "κ",
        "l": "λ",
        "m": "μ",
        "n": "ν",
        "o": "ο",
        "p": "π",
        "q": "κ",  # Similar to 'k'
        "r": "ρ",
        "s": "σ",
        "t": "τ",
        "u": "υ",
        "v": "β",  # Similar to 'b'
        "w": "ω",
        "x": "χ",
        "y": "υ",
        "z": "ζ",  # The Greek equivalent of 'z' is 'ζ'
    }
)


def is_english(word: str) -> bool:
    return all(ord(ch) < 200 for ch in word)


def greeklish_to_greek_characters(word: str) -> str:
    return word.lower().translate(GREEKLISH)


def greeklish_to_greek(word: str) -> str:
    """
    Snippet from the wordref script that requests WordReference to get
    the greek accented version of the given word.

    Examples:
        * greeklish_to_greek("xara")     => χαρά
        * greeklish_to_greek("χαρα")     => χαρά
        * greeklish_to_greek("χαρά")     => χαρά
        * greeklish_to_greek("nonsense") => nonsense
    """

    greek_word_no_accents = greeklish_to_greek_characters(word)
    url = f"https://www.wordreference.com/gren/{greek_word_no_accents}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        word = (
            soup.find("table", {"class": "WRD"})
            .find("tr", {"class": "even"})
            .find("td", {"class": "FrWrd"})
            .strong.text.split()[0]
        )
    except:
        pass

    return word
