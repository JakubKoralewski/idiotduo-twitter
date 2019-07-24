import pytest
from bot.zdobadz_cytat import biblia_cytat

def __test_single_quote(cytat):
	assert cytat
	assert cytat["autor"]
	assert cytat["cytat"]
	assert cytat["ksiega"]
	assert cytat["z"]

def test_get_cytat_online():
	"""
	Sprawdź pozyskiwanie cytatu z Biblii.
	"""
	cytat = biblia_cytat()
	__test_single_quote(cytat)

@pytest.mark.webtest
def test_get_many_cytat_online():
	"""
	Sprawdź pozyskiwanie cytatów z Biblii.
	"""
	for i in range(5):
		__test_single_quote(biblia_cytat())