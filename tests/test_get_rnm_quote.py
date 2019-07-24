import pytest
from bot.text_src import get_rnm_quote
from .utils.assert_quote import assert_quote

def test_get_rnm_quote():
    quote = get_rnm_quote()
    assert_quote(quote)