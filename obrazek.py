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


def narysujObrys(text, x, y, outlineSize, font):
    draw.text((x-outlineSize, y-outlineSize), text, font=font, fill="black")
    draw.text((x+outlineSize, y-outlineSize), text, font=font, fill="black")
    draw.text((x+outlineSize, y+outlineSize), text, font=font, fill="black")
    draw.text((x-outlineSize, y+outlineSize), text, font=font, fill="black")
    draw.text((x-outlineSize, y), text, font=font, fill="black")
    draw.text((x+outlineSize, y), text, font=font, fill="black")
    draw.text((x, y+outlineSize), text, font=font, fill="black")
    draw.text((x, y-outlineSize), text, font=font, fill="black")


def sumaWysokosc(lista: [], font: ImageFont.truetype) -> int or float:
    sumaWysokosc = 0
    for item in lista:
        sumaWysokosc += font.getsize(item)[1]
    return sumaWysokosc


# testowy cytat
""" BibliaCytat = {
    'cytat': '" ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki!ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki! ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki!ALLE LUJA JEST TO BARDZO DŁUGI TEKST W KTÓRYM SPRÓBUJĘ PRZKEROCZYĆ limit tekstu jaki jest mi dany, żeby zobaczyc czy obliczenie wysokosci tekstu jest poprawnie wykorzystywane aby obliczyc wielkosc czcionki!"',
    'autor': 'Jakub Koralewski'
} """


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
imgFraction = 0.85

font = ImageFont.truetype("comic/comic.ttf", 1)

cytatLista = textwrap.wrap(cytat, width=40, fix_sentence_endings=True)


def znajd_najdluzszy_cytat(lista: [str]) -> str:
    """Znajduje najdluzszy tekst w dostarczonej liscie."""
    najdluzszy = lista[0]
    for line in lista:
        if font.getsize(line)[0] > font.getsize(najdluzszy)[0]:
            najdluzszy = line
    return najdluzszy


ratio_szerokosc = imgFraction * img.width
ratio_wysokosc = imgFraction * img.height
VIDEO_RATIO = 1920/1080  # =~ 1.8
ratio_sensitivity = 0.4
obecna_szerokosc_linii = 40


def wielkosc_czcionki():
    global cytatLista
    global font
    najdluzszyCytat = znajd_najdluzszy_cytat(cytatLista)
    szerokosc_najdluzszej = font.getsize(najdluzszyCytat)[0]
    wysokosc = sumaWysokosc(cytatLista, font)
    fontSize = 1

    while szerokosc_najdluzszej < ratio_szerokosc and wysokosc < ratio_wysokosc:
        szerokosc_najdluzszej = font.getsize(najdluzszyCytat)[0]
        wysokosc = sumaWysokosc(cytatLista, font)
        # iterate until the text size is just larger than the criteria
        fontSize += 1
        font = ImageFont.truetype("comic/comic.ttf", fontSize)

    if not VIDEO_RATIO - ratio_sensitivity < szerokosc_najdluzszej / wysokosc:
        obecna_szerokosc_linii += 5
        cytatLista = textwrap.wrap(
            cytat, width=obecna_szerokosc_linii, fix_sentence_endings=True)
        fontSize = wielkosc_czcionki()

    return fontSize


fontSize = wielkosc_czcionki()

randColor = tuple([random.randint(100, 255) for i in range(3)])

# zaczynamy pisanie

# wysrodkuj na osi y
calaWysokosc = sumaWysokosc(cytatLista, font)
srodkowaWysokosc = height/2 - calaWysokosc/2

print(f'img height: {img.height}, img.width: {img.width}, font: {font.size}, calaWysokosc: {calaWysokosc}, srodkowaWysokosc: {srodkowaWysokosc}')

# pisz cytat
offset = srodkowaWysokosc
outlineSize = 3
for line in textwrap.wrap(cytat, width=40):

    # w - szerokosc danej linii tekstu
    # h - wysokosc danej linii tekstu
    w, h = draw.textsize(line, font)

    x = width/2 - w/2
    y = offset

    # rysujemy obrys
    narysujObrys(line, x, y, outlineSize, font)

    draw.text((x, y), line, font=font, fill=randColor)
    offset += font.getsize(line)[1]

img.save('klatka_ready.jpg')
