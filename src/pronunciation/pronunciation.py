import io
from typing import Tuple

import pronunciation.forvo as forvo
import pronunciation.wiktionary as wiktionary


def get_pronunciation(word: str) -> Tuple[str, str | None, io.BytesIO | None]:
    message = f"Word: {word}\n"

    _ipa_link, ipa_pronunciation = wiktionary.get_wiktionary_ipa(word)
    if ipa_pronunciation:
        message += f"IPA: {ipa_pronunciation}\n"

    audio_link, audio_file = forvo.get_forvo_pronunciation_audio(word)
    # message += audio_link

    return message, audio_link, audio_file
