"""
Ten plik bierze cytat i obrazek, a nastepnie dodaje go do obrazka.
"""

import random
import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import textwrap


def narysuj_obrys(text, x, y, outline_size, font, draw):
    draw.text((x-outline_size, y-outline_size), text, font=font, fill="black")
    draw.text((x+outline_size, y-outline_size), text, font=font, fill="black")
    draw.text((x+outline_size, y+outline_size), text, font=font, fill="black")
    draw.text((x-outline_size, y+outline_size), text, font=font, fill="black")
    draw.text((x-outline_size, y), text, font=font, fill="black")
    draw.text((x+outline_size, y), text, font=font, fill="black")
    draw.text((x, y+outline_size), text, font=font, fill="black")
    draw.text((x, y-outline_size), text, font=font, fill="black")


def suma_wysokosc(lista: [], font: ImageFont.truetype) -> int or float:
    suma_wysokosc = 0
    for item in lista:
        suma_wysokosc += font.getsize(item)[1]
    return suma_wysokosc


def znajdz_najdluzszy_cytat(lista: [str], font: ImageFont.truetype) -> str:
    """Znajduje najdluzszy tekst w dostarczonej liscie."""
    najdluzszy = lista[0]
    for line in lista:
        if font.getsize(line)[0] > font.getsize(najdluzszy)[0]:
            najdluzszy = line
    return najdluzszy


obecna_szerokosc_linii = 40  # startowa szerokosc
IMG_FRACTION = 0.85
VIDEO_RATIO = 1920/1080  # =~ 1.8
RATIO_SENSITIVITY = 0.4


def wielkosc_czcionki(**kwargs) -> (int and []):
    """
    Oblicz potrzebna wielkosc czcionki.

    Args:
        **kwargs:
            cytat (str): tekst do ktorego dopasowac czcionke
            font (ImageFont.truetype): czcionka
            szerokosc: img.width
            wysokosc: img.height
            obecna_szerokosc_linii: OPTIONAL (40)

    """

    font = kwargs["font"]
    szerokosc = kwargs["szerokosc"]
    wysokosc = kwargs["wysokosc"]
    obecna_szerokosc_linii = kwargs.get(
        "obecna_szerokosc_linii", 40)  # default 40, optional
    cytat_lista = cytat_lista = textwrap.wrap(
        kwargs["cytat"], width=obecna_szerokosc_linii, fix_sentence_endings=True)

    ratio_szerokosc = IMG_FRACTION * szerokosc
    ratio_wysokosc = IMG_FRACTION * wysokosc

    najdluzszyCytat = znajdz_najdluzszy_cytat(cytat_lista, font)
    szerokosc_najdluzszej = font.getsize(najdluzszyCytat)[0]
    wysokosc = suma_wysokosc(cytat_lista, font)
    font_size = 1

    while szerokosc_najdluzszej < ratio_szerokosc and wysokosc < ratio_wysokosc:
        szerokosc_najdluzszej = font.getsize(najdluzszyCytat)[0]
        wysokosc = suma_wysokosc(cytat_lista, font)
        # iterate until the text size is just larger than the criteria
        font_size += 1
        font = ImageFont.truetype("comic/comic.ttf", font_size)

    if not VIDEO_RATIO - RATIO_SENSITIVITY < szerokosc_najdluzszej / wysokosc:
        cytat = kwargs["cytat"]
        obecna_szerokosc_linii += 5
        cytat_lista = textwrap.wrap(
            cytat, width=obecna_szerokosc_linii, fix_sentence_endings=True)
        font_size = wielkosc_czcionki()

    return font_size, cytat_lista


# testowy cytat
""" biblia_cytat = {
    'cytat': '" ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki!ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki! ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki!ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki!"',
    'autor': 'Jakub Koralewski'
} """

slownik_z_cytatem = None


def zapisz_obrazek(**kwargs):
    # Wygeneruj obrazek 'klatka.jpg'
    import randomowa_klatka
    """
    Zapisuje obrazek do pliku.

    Args:
        **kwargs: 
            cytat (str): nadpisz cytat tekstu

    """
    global slownik_z_cytatem  # zeby mozna bylo uzyc z poziomu tweet.py | inaczej 'TypeError: 'NoneType' object is not subscriptable'


    # jeśli nadpisano cytat przy wykonaniu funkcji
    if 'cytat' in kwargs:
        cytat = kwargs["cytat"]
        autor = ''
        print('cytat nadpisany')
    else:
        print('cytat NIEnadpisany, zdobywam tradycyjnymi sposobami')
        try:
            from zdobadz_cytat import biblia_cytat
            slownik_z_cytatem = biblia_cytat

            del biblia_cytat
        except:
            from slowo_na_dzis import slowo_na_dzis
            slownik_z_cytatem = slowo_na_dzis

            del slowo_na_dzis
        
        print(slownik_z_cytatem)
        cytat = slownik_z_cytatem['cytat']
        autor = slownik_z_cytatem['autor']

    print(f'cytat: {cytat}')

    try:
        img = Image.open('klatka.jpg')
    except FileNotFoundError:
        # randomowa_klatka.py fail
        # sprobuj ponownie
        import randomowa_klatka
        img = Image.open('klatka.jpg')

    width, height = img.size
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("comic/comic.ttf", 1)

    # zbadaj optymalna wielkosc czcionki
    font_size, cytat_lista = wielkosc_czcionki(
        cytat=cytat, font=font, szerokosc=img.width, wysokosc=img.height)

    # wybierzmy losowy kolor
    # niech to bedzie niezmienna lista 3 losowych liczb w tym przedziale
    # R, G, B
    rand_color = tuple([random.randint(100, 255) for i in range(3)])

    cala_wysokosc = suma_wysokosc(cytat_lista, font)

    poczatkowa_wysokosc = height/2 - cala_wysokosc/2

    print(f'img height: {img.height}, img.width: {img.width}, font: {font.size}, cala_wysokosc: {cala_wysokosc}, poczatkowa_wysokosc: {poczatkowa_wysokosc}')

    offset = poczatkowa_wysokosc
    outline_size = 3
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
        draw.text((x, y), line, font=font, fill=rand_color)

        # offset kontroluje wysokosc tekstu
        # za kazda linia tekstu zwieksza sie o wysokosc danej linii
        offset += font.getsize(line)[1]

    img.save('klatka_ready.jpg')


if __name__ == "__main__":
    print('imported obrazek.py')
