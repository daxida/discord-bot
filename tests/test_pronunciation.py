from pronunciation.pronunciation import get_pronunciation
from utils import NotFoundException, fix_greek_spelling


def test_existing_pronunciation():
    word = "ευχαριστώ"
    message, _ = get_pronunciation(word)
    assert message == "Word: ευχαριστώ\nIPA: ef.xa.ɾiˈsto\n"


def test_non_existing_pronunciation():
    word = "μπλαμπλα"
    try:
        get_pronunciation(word)
        assert False, "Expected NotFoundException but no exception was raised."
    except NotFoundException:
        pass  # Test passes if NotFoundException is raised
    except Exception as e:
        assert False, f"Expected NotFoundException but got {type(e).__name__}"


def test_retry_pronunciation():
    word = "ευχαριστω"
    try:
        get_pronunciation(word)
        assert False, "Should fail the first time"
    except NotFoundException:
        word = fix_greek_spelling(word)
        message, _ = get_pronunciation(word)
        assert message == "Word: ευχαριστώ\nIPA: ef.xa.ɾiˈsto\n"
