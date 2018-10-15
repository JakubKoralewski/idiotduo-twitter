"""
Ten plik bierze cytat i obrazek, a nastepnie dodaje go do obrazka.
"""

from zdobadz_cytat import BibliaCytat
import random


def narysujObrys(text, x, y, outlineSize, font):
    draw.text((x-outlineSize, y-outlineSize), text, font=font, fill="black")
    draw.text((x+outlineSize, y-outlineSize), text, font=font, fill="black")
    draw.text((x+outlineSize, y+outlineSize), text, font=font, fill="black")
    draw.text((x-outlineSize, y+outlineSize), text, font=font, fill="black")
    draw.text((x-outlineSize, y), text, font=font, fill="black")
    draw.text((x+outlineSize, y), text, font=font, fill="black")
    draw.text((x, y+outlineSize), text, font=font, fill="black")
    draw.text((x, y-outlineSize), text, font=font, fill="black")


print(BibliaCytat)
cytat = BibliaCytat['cytat']
autor = BibliaCytat['autor']
ksiega = BibliaCytat['ksiega']


import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import textwrap

img = Image.open('klatka.jpg')
width, height = img.size
draw = ImageDraw.Draw(img)

cytatLista = textwrap.wrap(cytat, width=40)

print(f'cytat: {cytat}')

fontSize = 1  # starting font size

# portion of image width you want text width to be
imgFraction = 0.85

font = ImageFont.truetype("comic/comic.ttf", fontSize)
while font.getsize(cytatLista[0])[0] < imgFraction * img.width:
    # iterate until the text size is just larger than the criteria
    fontSize += 1
    font = ImageFont.truetype("comic/comic.ttf", fontSize)

randColor = tuple([random.randint(80, 255) for i in range(3)])

# zaczynamy pisanie

# wysrodkuj na osi y
# ilosc linii
iloscLinii = len(cytatLista)
# wysokosc pojedynczej linii
pojWysokosc = font.getsize(cytatLista[0])[1]
calaWysokosc = pojWysokosc * iloscLinii
srodkowaWysokosc = height/2 - calaWysokosc/2

print(pojWysokosc)

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

# pisz autor+ksiega w prawym dolnym rogu
smallFontSize = int(fontSize / 2)
smallFont = ImageFont.truetype("comic/comici.ttf", smallFontSize)
smallText = f'{ksiega} {autor}'
smallMargin = 30
w, h = draw.textsize(smallText, smallFont)
x = img.width - w - smallMargin
y = img.height - h - smallMargin
narysujObrys(smallText, x, y, round(outlineSize/2, 0), smallFont)
draw.text((x, y), smallText, font=smallFont, fill=randColor)

img.save('klatka_ready.jpg')
