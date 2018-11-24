"""
Ten plik bierze cytat i obrazek, a nastepnie dodaje go do obrazka.
"""
try:
    # special error for testing
    #from zdobadz_cytat import BibliaCytat
    from zdobadz_cytat import BibliaCytat
    slownik_z_cytatem = BibliaCytat
except:
    from slowo_na_dzis import slowo_na_dzis
    slownik_z_cytatem = slowo_na_dzis
import random
import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import textwrap


def narysuj_obrys(text, x, y, outlineSize, font, draw):
    draw.text((x-outlineSize, y-outlineSize), text, font=font, fill="black")
    draw.text((x+outlineSize, y-outlineSize), text, font=font, fill="black")
    draw.text((x+outlineSize, y+outlineSize), text, font=font, fill="black")
    draw.text((x-outlineSize, y+outlineSize), text, font=font, fill="black")
    draw.text((x-outlineSize, y), text, font=font, fill="black")
    draw.text((x+outlineSize, y), text, font=font, fill="black")
    draw.text((x, y+outlineSize), text, font=font, fill="black")
    draw.text((x, y-outlineSize), text, font=font, fill="black")


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

obecna_szerokosc_linii = 40 # startowa szerokosc
imgFraction = 0.85
VIDEO_RATIO = 1920/1080  # =~ 1.8
ratio_sensitivity = 0.4
def wielkosc_czcionki(**kwargs) -> int:
    """
    Oblicz potrzebna wielkosc czcionki.

    Args:
        **kwargs:
            cytat (str): tekst do ktorego dopasowac czcionke
            font (ImageFont.truetype): czcionka
            
            szerokosc_wideo: img.width
            wysokosc_wideo: img.height
            obecna_szerokosc_linii: OPTIONAL (40)

    """
    
    font = kwargs["font"]
    szerokosc_wideo = kwargs["szerokosc_wideo"]
    wysokosc_wideo = kwargs["wysokosc_wideo"]
    obecna_szerokosc_linii = kwargs.get("obecna_szerokosc_linii", 40) # default 40, optional
    cytat_lista = cytat_lista = textwrap.wrap(kwargs["cytat"], width=obecna_szerokosc_linii, fix_sentence_endings=True)

    ratio_szerokosc = imgFraction * szerokosc_wideo
    ratio_wysokosc = imgFraction * wysokosc_wideo

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

    if not VIDEO_RATIO - ratio_sensitivity < szerokosc_najdluzszej / wysokosc:
        cytat = kwargs["cytat"]
        obecna_szerokosc_linii += 5
        cytat_lista = textwrap.wrap(
            cytat, width=obecna_szerokosc_linii, fix_sentence_endings=True)
        font_size = wielkosc_czcionki()

    return font_size


# testowy cytat
""" BibliaCytat = {
    'cytat': '" ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki!ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki! ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki!ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki!"',
    'autor': 'Jakub Koralewski'
} """

def zapisz_obrazek(**kwargs):
    """
    Zapisuje obrazek do pliku.

    Args:
        **kwargs: 
            cytat (str): nadpisz cytat tekstu

    """
    if 'cytat' in **kwargs:
        cytat = kwargs["cytat"]
        autor = ''
        print('cytat overriden\n',cytat, autor)
    else:
        print(slownik_z_cytatem)
        cytat = slownik_z_cytatem['cytat']
        autor = slownik_z_cytatem['autor']

    try:
        img = Image.open('klatka.jpg')
    except FileNotFoundError:
        # randomowa_klatka.py fail
        # sprobuj ponownie
        import randomowa_klatka
        img = Image.open('klatka.jpg')
    
    width, height = img.size
    draw = ImageDraw.Draw(img)
    print(f'cytat: {cytat}')

    # portion of image width you want text width to be

    font = ImageFont.truetype("comic/comic.ttf", 1)

    font_size = wielkosc_czcionki(cytat=cytat, font=font, )

    randColor = tuple([random.randint(100, 255) for i in range(3)])

    # zaczynamy pisanie

    # wysrodkuj na osi y
    cala_wysokosc = suma_wysokosc(cytat_lista, font)
    srodkowa_wysokosc = height/2 - cala_wysokosc/2

    print(f'img height: {img.height}, img.width: {img.width}, font: {font.size}, cala_wysokosc: {cala_wysokosc}, srodkowa_wysokosc: {srodkowa_wysokosc}')

    # pisz cytat
    offset = srodkowa_wysokosc
    outlineSize = 3
    for line in textwrap.wrap(cytat, width=40):

        # w - szerokosc danej linii tekstu
        # h - wysokosc danej linii tekstu
        w, h = draw.textsize(line, font)

        x = width/2 - w/2
        y = offset

        # rysujemy obrys
        narysuj_obrys(line, x, y, outlineSize, font, draw)

        draw.text((x, y), line, font=font, fill=randColor)
        offset += font.getsize(line)[1]

    img.save('klatka_ready.jpg')

if __name__ == "__main__":
    print('imported obrazek.py')