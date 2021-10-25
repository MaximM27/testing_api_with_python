import pytest


def test_small_phrase():
    phrase = input("Set a phrase: ")
    assert(len(phrase) < 15), f"There are more then 15 symbols in entered phrase"
