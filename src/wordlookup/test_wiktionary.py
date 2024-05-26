import asyncio
import pytest
from wiktionaryel import run_test_fetch


# https://stackoverflow.com/questions/70015634/how-to-test-async-function-using-pytest
pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio()
async def test_wiktionary_fetch():
    """
    A simple concurrent async test.

    This uses no cache and sends quite some requests to wiktionary. Use carefully.
    Use the debug entry in the fixture to only run certain entries.
    """
    DEBUG = False

    # fmt: off
    fixture = [
        # verb,  has_result, debug
        ("αγαπώ",     True,  False),
        ("αγαπάω",    True,  False),
        ("περπατώ",   True,  False),
        ("περπατάω",  True,  False),
        ("χαραλώνω",  False, False),
        ("βρέχω",     False, False),
        ("βρίσκομαι", True,  False),
        ("ξέρω",      True,  False),
        ("είμαι",     True,  False),
    ]
    # fmt: on

    if DEBUG:
        fixture = [(verb, has_result, debug) for verb, has_result, debug in fixture if debug]

    tasks = [run_test_fetch(verb) for verb, _, _ in fixture]
    results = await asyncio.gather(*tasks)
    for (verb, has_result, _), received in zip(fixture, results):
        if has_result:
            assert received is not None, verb
        else:
            assert received is None, verb
