"""
Ten plik korzysta ze strony twojabiblia.pl, selenium i Chrome, aby zdobyc cytat z Biblii.

Problemem w tym pliku jest to, że selenium czeka, aż strona przestanie się ładować, mimo że 
cytat już się załadował.
"""

from selenium import webdriver
from bot.on_remote import on_remote


def biblia_cytat():
	if on_remote:
		driver = webdriver.Chrome()
	else:
		from bot.config import WEB_DRIVER_PATH
		import os
		print(f'cwd: {os.getcwd()}')
		print(f'webpath: {WEB_DRIVER_PATH}')
		driver = webdriver.Chrome(executable_path=WEB_DRIVER_PATH)

	with driver:
		driver.get('http://twojabiblia.pl/?page=quote')
		try:
			cytat = driver.find_element_by_class_name('NS')
		except selenium.common.exceptions.NoSuchElementException as e:
			print(f'HTML: {driver.page_source}')
			raise e
		autor = driver.find_element_by_class_name('OS')
		ksiega = driver.find_element_by_class_name('MS')

		return {
			'cytat': cytat.text,
			'autor': autor.text,
			'ksiega': ksiega.text,
			'z': 'zdobadz_cytat'
		}


#import re
# Wyszukaj « » i dodaj na poczatek lub koniec jesli znajduje sie tylko jeden ALBO usuń?
# np.:
"""
“ Dobra jest sól; lecz jeśli nawet sól smak swój utraci, to czymże ją zaprawić? 
Nie nadaje się ani do ziemi, ani do nawozu; precz się ją wyrzuca. Kto ma uszy do słuchania, niechaj słucha!» ”
"""
# into
