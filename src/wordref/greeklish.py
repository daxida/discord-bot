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


def greeklish_to_greek(s: str) -> str:
    return s.lower().translate(GREEKLISH)
