import json
import random
import os

with open('static\slowo_na_dzis.txt', 'r') as plik:
    slowo_na_dzis = json.load(plik)

slowo_na_dzis = random.choice(slowo_na_dzis)

tytul = slowo_na_dzis["tytul"]
opis = slowo_na_dzis["opis"]


def unormalizuj_wielkosc(text: str) -> str:
    text = text.lower()
    text = text[0].upper() + text[1:]
    return text

def polacz_cytat_z_opisem(tytul, opis) -> str:
    """
    Napraw poniższe problemy:
    "Prawem kaduka Czyli:(...)"
    https://twitter.com/idiot2duo/status/1067720245467594752

    
    """
    if opis[0].isupper():
        nowy_opis = opis[0].lower() + opis[1:]
        return f'{tytul}, {nowy_opis}'



# Jesli nie ma tytulowego slowo na poczatku opisu.
if tytul not in opis[:len(tytul)+2]:
    # Dodaj je.
    tytul = unormalizuj_wielkosc(tytul)
    #cytat = f'{tytul} {opis}'
    cytat = polacz_cytat_z_opisem(tytul, opis)
else:
    cytat = slowo_na_dzis


print(slowo_na_dzis)


slowo_na_dzis = {
    'cytat': cytat,
    'autor': slowo_na_dzis["autor"],
    'tytul': tytul,
    'z': 'slowo_na_dzis'
}
