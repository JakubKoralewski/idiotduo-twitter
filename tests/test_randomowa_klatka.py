import pytest
from bot.image.randomowa_klatka import *
from pprint import pprint

def test_get_random_frame_successfully():
	"""
	Sprwadź proces zapisywania randomowej klatki do dysku.
	"""
	
	from bot.image.ids import ids
	
	for i in range(5):
		zapisz_klatke(ids=ids)


def test_blocked_in_your_country():
	url = 'PN5PAFAGXJ8'
	
	zapisz_klatke(url=url)