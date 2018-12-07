"""
Ten plik bierze dodaje cytat do obrazka.

Istnieje problem ze sposobem w jaki dodawany jest obrys. 
Jest on po prostu rysowany wielokrotnie, raz troche na lewo, raz troche na prawo, raz troche w prawy gorny rog itp.
Jest to bardzo nieefektywne i produkuje wykropkowany obrys!
Sposoby rozwiązania problemu:
- pisz literka po literce zwiększając każda literke z osobna
- zmniejsz rozmiar obrysu i udawaj, że nic się nie dzieje ✓
- pisz w pogrubionej czcionce 𝐗
    - to nie ma sensuuu, bo https://i.imgur.com/f17WVLw.png 

Tekst czasem jest zbyt jasny dla swojego otoczenia.
Aby to rozwiazac nalezaloby obliczyc sredni kolor w obrazku i wybrac kolor "przeciwny".
"""

import random
import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import textwrap
from typing import List

from bot.config import COMIC_SANS_PATH
COMIC_SANS = COMIC_SANS_PATH + 'comic.ttf'
WRAZLIWOSC_STOSUNKOW = 0.19

def narysuj_obrys(text, x, y, outline_size, font, draw):
    draw.text((x-outline_size, y-outline_size), text, font=font, fill="black")
    draw.text((x+outline_size, y-outline_size), text, font=font, fill="black")
    draw.text((x+outline_size, y+outline_size), text, font=font, fill="black")
    draw.text((x-outline_size, y+outline_size), text, font=font, fill="black")
    draw.text((x-outline_size, y), text, font=font, fill="black")
    draw.text((x+outline_size, y), text, font=font, fill="black")
    draw.text((x, y+outline_size), text, font=font, fill="black")
    draw.text((x, y-outline_size), text, font=font, fill="black")


def polacz_zbyt_krotkie(lista: List[str], *limit_liter) -> List[str]:
    """
    Celem tej funkcji jest zmiana tego typu list: 
    ['xx','xxxxxxxxxxxx','xxxxxxxxxxxxxxx'] w ['xxxxxxxxxxxxxx','xxxxxxxxxxxxxxx']

    Args:
        lista ([str]): lista ktorej poddanie zostana funkcja,
        [limit_liter]: maksymalna ilosc liter ktorej poddane zostanie polaczenie (OPCJONALNIE),
    """
    if limit_liter:
        limit_liter = limit_liter[0]
    else:
        limit_liter = 5
    ostatni_element = len(lista) - 1
    for i in range(len(lista)):
        if not isinstance(lista[i], str):
            raise Exception(f"Lista podana funkcji polacz_zbyt_krotkie() nie zawiera stringow.\nZawiera: {lista[i]}")
        if len(lista[i]) < limit_liter:
            if i == ostatni_element:
                lista[i-1] = lista[i-1] + lista[i]
            else:
                lista[i+1] = lista[i] + lista[i+1]
            lista.pop(i)
    
    return lista
    

def czcionka(**kwargs) -> (int and []):
    """
    Oblicz potrzebna wielkosc czcionki.

    Args:
        **kwargs:
            cytat (str): tekst do ktorego dopasowac czcionke
            szerokosc: img.width
            wysokosc: img.height
            obecna_szerokosc_linii: OPTIONAL (40)
            font_size: OPTIONAL (false) if true will return font size

    """
    print("DEBUGGING CZCIONKA")
    obecna_szerokosc_linii = kwargs.get(
        "obecna_szerokosc_linii", 40)  # default 40, optional
    font_size = kwargs.get("font_size", 1)  # default 1, optional
    szerokosc = kwargs["szerokosc"]
    wysokosc = kwargs["wysokosc"]
    cytat = kwargs["cytat"]

    font = ImageFont.truetype(COMIC_SANS, font_size)
    cytat_lista = textwrap.wrap(
        cytat, width=obecna_szerokosc_linii, fix_sentence_endings=True)

    # dodaj marginesy procentowe jako 15% szerokosci
    szerokosc = int(szerokosc - 0.2 * szerokosc)
    wysokosc = int(wysokosc - 0.2 * szerokosc)

    # gdzie duzy stosunek to stosunek szerokosci do wysokosci obrazka
    duzy_stosunek = szerokosc/wysokosc
    # a maly stosunek to stosunek szerokosci do wysokosci tekstu
    maly_stosunek = 0

    zbyt_szeroki = False
    zbyt_wysoki = False
    i = 1

    while True:
        print('|',end='')

        szerokosc_najdluzszej = font.getsize(max(cytat_lista, key=len))[0]
        calkowita_wysokosc = sum([font.getsize(cytat)[1] for cytat in cytat_lista])
        zbyt_szeroki = szerokosc_najdluzszej > szerokosc
        zbyt_wysoki = calkowita_wysokosc > wysokosc
        maly_stosunek = szerokosc_najdluzszej / calkowita_wysokosc
        
        roznica_stosunkow = abs(duzy_stosunek - maly_stosunek)

        # jesli roznica stosunku nadanej szerokosci do wysokosci
        # i stosunku szerokosci do wysokosci tekstu
        # jest w granicy 0.1 (WRAZLIWOSC_STOSUNKOW)
        # !!! POTRZEBA WIECEJ WARUNKOW ABY LOSOWO-DOBRY STOSUNEK O ZBYT MALEJ CZCIONCE NIE ZOSTAL ZAAKCEPTOWANY ✓
        if roznica_stosunkow < WRAZLIWOSC_STOSUNKOW and (zbyt_szeroki or zbyt_wysoki):
            # zakoncz szukanie
            break

        # jesli szerszy niz nadana szerokosc
        if zbyt_szeroki:
            # zmniejsz ilosc liter w jednej linii 
            obecna_szerokosc_linii -= 2
            
        elif zbyt_wysoki:
            # zwieksz ilosc liter w jednej linii
            obecna_szerokosc_linii += 2
        
        if not (zbyt_szeroki and zbyt_wysoki):
            font_size += 1 
        else:
            font_size -= 1

        if i > 150:
            print('!!! UWAGA PONAD 150 razy próbowano osiągnąć idealny rozkład tekstu !!!.\nPODDAJE SIĘ!!!')
            break
        
        # odswiez zmienne
        i += 1
        font = ImageFont.truetype(COMIC_SANS, font_size)
        # podziel cytat na liste
        cytat_lista = textwrap.wrap(cytat, width=obecna_szerokosc_linii, fix_sentence_endings=True)

    return ImageFont.truetype(COMIC_SANS, font_size), cytat_lista

def otworz_img() -> Image.open:
    """Z założenia funkcja wywoływana tylko raz, więc wrzucam tutaj importy dla koncepcjonalnej prostoty."""
    
    import os
    img = None

    for file in os.listdir('output'):
        print(f'file: {file}')

        # Jesli to nie jpg to idz do nastepnego
        if not file.endswith('.jpg'):
            continue
        
        try:
            img = Image.open(os.path.join(os.getcwd(),'output',file))
            return img
        except:
            continue
    
    # jesli nic nie znaleziono, wywal blad
    if img is None:
        raise Exception("Nie ma obrazka.")


def zapisz_obrazek(**kwargs):
    # Wygeneruj obrazek 'klatka.jpg'
    """
    Zapisuje obrazek do pliku.

    Args:
        **kwargs: 
            cytat (str): nadpisz cytat tekstu

    """

    # jeśli nadpisano cytat przy wykonaniu funkcji
    if 'cytat' in kwargs:
        # TEST
        cytat = kwargs["cytat"]
        print('cytat nadpisany')
    else:
        print('cytat NIEnadpisany, zdobywam tradycyjnymi sposobami')
    
    # zawsze jest podawana (domyslnie False), dlatego nie używam __dict__.get()
    nazwa = kwargs["nazwa"]
    print(f'cytat: {cytat}', end='')
    
    img = otworz_img()

    width, height = img.size
    draw = ImageDraw.Draw(img)

    # zbadaj optymalna wielkosc czcionki
    font, cytat_lista = czcionka(
        cytat=cytat, szerokosc=img.width, wysokosc=img.height)

    cytat_lista = polacz_zbyt_krotkie(cytat_lista)
    # wybierzmy losowy kolor
    # niech to bedzie niezmienna lista 3 losowych liczb w tym przedziale
    # R, G, B
    losowy_kolor = tuple([random.randint(160, 255) for i in range(3)])

    cala_wysokosc = sum([font.getsize(cytat)[1] for cytat in cytat_lista])

    poczatkowa_wysokosc = height/2 - cala_wysokosc/2

    print(f'img height: {img.height}, img.width: {img.width}, font: {font.size}, cala_wysokosc: {cala_wysokosc}, poczatkowa_wysokosc: {poczatkowa_wysokosc}')

    offset = poczatkowa_wysokosc
    outline_size = int(font.size/25)
    # pisz cytat
    for line in cytat_lista:
        # w - szerokosc danej linii tekstu
        # h - wysokosc danej linii tekstu
        w, h = draw.textsize(line, font)

        # x, y - pozycja danej linii tekstu, gdzie:

        # x - srodek - polowa linii tekstu
        x = width/2 - w/2
        # y - obecny offset
        y = offset

        # najpierw obrys
        narysuj_obrys(line, x, y, outline_size, font, draw)
        # potem tekst
        draw.text((x, y), line, font=font, fill=losowy_kolor)

        # offset kontroluje wysokosc tekstu
        # za kazda linia tekstu zwieksza sie o wysokosc danej linii
        offset += font.getsize(line)[1]
    img.save(nazwa if nazwa else 'klatka_ready.jpg')

if __name__ == "__main__":
    print('To nie powinno sie wydarzyc!')
