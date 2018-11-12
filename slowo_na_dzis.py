import json
import random

with open('slowo_na_dzis.txt', 'r') as plik:
    slowo_na_dzis = json.load(plik)

slowo_na_dzis = random.choice(slowo_na_dzis)

print(slowo_na_dzis)


slowo_na_dzis = {
    'cytat': f'{slowo_na_dzis["tytul"]} {slowo_na_dzis["opis"]}',
    'autor': slowo_na_dzis["autor"],
    'tytul': slowo_na_dzis["tytul"],
    'ksiega': '',
    'z': 'slowo_na_dzis'
}
