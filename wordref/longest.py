import re
import unicodedata


def LCS(a, b):
    """Finds the longuest common substring of a and b"""
    if a == b:
        return len(a)
    var = 0
    while a:
        i = 1
        while True:
            _buffer = a[:i]
            if _buffer in b and i < len(a):
                i += 1
            else:
                break
        if i - 1 > var:
            var = i - 1
        a = a[i:]

    return var


def remove_accents(word):
    normalized = unicodedata.normalize("NFKD", word)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def get_delta(a, b):
    aa = remove_accents(a.lower())
    bb = remove_accents(b.lower())

    max_length = max(len(aa), len(bb))
    m = max(LCS(aa, bb), LCS(bb, aa))

    return (max_length - m) / max_length


def highlightSynonyms(sentence, synonyms_list):
    for word in set(sentence.split()):
        # Removes punctuation to match the correct words
        word = re.sub(r"\(|\)|,|\.|", "", word)  # add ; ??
        for synonym in synonyms_list:
            # 1 = same word, 0 = completely different
            dif = get_delta(word, synonym)
            # If the estimated difference is lower than 0.25
            # we treat both word as the same (declension, plural etc.)
            if dif <= 0.3:
                sentence = sentence.replace(word, f"**{word}**")
                break

    return sentence
