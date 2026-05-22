import pytest

def test_len():
    phrase = input("Set a phrase: ")
    assert len(phrase) <= 15, "Input is more than 15 symbols!!!"