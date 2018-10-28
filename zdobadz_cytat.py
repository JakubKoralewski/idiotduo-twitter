"""
Ten plik korzysta ze strony twojabiblia.pl, selenium i Chrome, aby zdobyc cytat z Biblii.
"""

from selenium import webdriver

driver = webdriver.Chrome()
with driver:
    driver.get('http://twojabiblia.pl/?page=quote')
    cytat = driver.find_element_by_class_name('NS')
    autor = driver.find_element_by_class_name('OS')
    ksiega = driver.find_element_by_class_name('MS')

    BibliaCytat = {
        'cytat': cytat.text,
        'autor': autor.text,
        'ksiega': ksiega.text
    }

import re
# Wyszukaj « » i dodaj na poczatek lub koniec jesli znajduje sie tylko jeden ALBO usuń?
# np.:
"""
“ Dobra jest sól; lecz jeśli nawet sól smak swój utraci, to czymże ją zaprawić? 
Nie nadaje się ani do ziemi, ani do nawozu; precz się ją wyrzuca. Kto ma uszy do słuchania, niechaj słucha!» ”
"""
# into
