from wordref.wordref import Wordref


def test_wordref():
    word = "ημερήσιος"
    gr_en = True
    hide_words = True
    min_sentences_shown = 1
    max_sentences_shown = 5

    wordref = Wordref(word, gr_en, hide_words, min_sentences_shown, max_sentences_shown)
    entry = wordref.try_fetch_entry()

    assert entry.gr_en == gr_en
    assert entry.hide_words == hide_words
    assert entry.min_sentences_shown == min_sentences_shown
    assert entry.max_sentences_shown == max_sentences_shown

    # print(entry)

    # FIXME: the last one should not be a synonym
    en_synonyms = {"daily", "quotidian", "diurnal", "μη διαθέσιμη μετάφραση"}
    assert entry.en_synonyms == en_synonyms
