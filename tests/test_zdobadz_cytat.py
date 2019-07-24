import pytest
from bot.text_src import zdobadz_cytat
from .utils.assert_quote import assert_quote

def __test_single_quote(cytat):
	assert_quote(cytat)

def test_get_cytat_online():
	"""
	Sprawdź pozyskiwanie cytatu z Biblii.
	"""
	cytat = zdobadz_cytat()
	__test_single_quote(cytat)

@pytest.mark.webtest
def test_get_many_cytat_online():
	"""
	Sprawdź pozyskiwanie cytatów z Biblii.
	"""
	for i in range(5):
		__test_single_quote(zdobadz_cytat())