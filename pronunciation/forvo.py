import base64
import io
import re
from typing import Tuple

import requests

# FROM: https://gist.github.com/mikob/24a908471e38370f40d302b1cb1b41fb
# TODO: Print all possible pronunciations?

FAKE_BROWSER_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "accept-language": "en-US,en;q=0.9,ja;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}


def get_forvo_pronunciation_link(word: str) -> str | None:
    webPageUrl = f"https://forvo.com/search/{word}/el/"
    # s = requests.Session()
    # res = s.get('https://forvo.com')
    # cookies = dict(res.cookies)
    webPageText = requests.get(webPageUrl, headers=FAKE_BROWSER_HEADERS).text
    pageTextList = re.findall('<article class="search_words.*?</article>', webPageText, re.DOTALL)
    if len(pageTextList) > 0:
        # first result might be search_words empty
        pageText = pageTextList[-1]
        pronunciations = re.findall("Play\(\d+,'(.*?)'", pageText)
        if pronunciations:
            for l in range(len(pronunciations)):
                pronunciations[l] = base64.b64decode(pronunciations[l]).decode()
            print("Found %d pronunciations for %s" % (len(pronunciations), word))
            return "https://forvo.com/mp3/%s" % pronunciations[0]
    return None


def get_forvo_pronunciation_audio(word: str) -> Tuple[str | None, io.BytesIO | None]:
    audio_link = get_forvo_pronunciation_link(word)
    # Could not find the forvo link for this word.
    if audio_link is None:
        return (None, None)
    response = requests.get(audio_link, headers=FAKE_BROWSER_HEADERS)
    audio_file = io.BytesIO(response.content)
    return (audio_link, audio_file)
