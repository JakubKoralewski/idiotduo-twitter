import pytest
from bot.text_src import slowo_na_dzis
from bot.config import SLOWO_NA_DZIS_PATH
from .utils.assert_quote import assert_quote_slowo_na_dzis
from pprint import pprint
import json

def test_get_offline():
    """
    Sprawdź prawidłowe działanie odczytu cytatu z pliku json.
    """
    for i in range(5):
        cytat = slowo_na_dzis()
        pprint(cytat)
        assert cytat["autor"]
        assert cytat["cytat"]
        assert cytat["tytul"]
        assert cytat["z"]

def test_all_fields_exist_in_the_json_file():
    """
    Sprawdź poprawność samego pliku.
    """
    with open(SLOWO_NA_DZIS_PATH, 'r', encoding='UTF-8') as plik:
        slowo_na_dzis = json.load(plik)
    for cytat in slowo_na_dzis:
        pprint(cytat)
        assert_quote_slowo_na_dzis(cytat)