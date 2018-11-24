"""
Ten plik bierze wszystkie dane wygenerowane przez poprzednie skrypty i umieszcza je na Twitterze.
"""
import os
import argparse

parser = argparse.ArgumentParser(description='Wytweetuj obrazek.')
#parser.add_argument('--base64', type=bool, nargs='?', default=False, const=True, help='wypluj obrazek w base64')
parser.add_argument('--base64', action='store_true',
                    help='wypluj obrazek w base64')
parser.add_argument('--string', action='store_value', type=int, help='sprecyzuj wybrany te')
args = parser.parse_args()
is_base64 = args.base64


# Kolejnosc wykonywania dzialan:

# 1. Zdobadz klatke z Youtube.
import randomowa_klatka
# 2. Zdobadz cytat.
#import zdobadz_cytat
# 3. Polacz cytat i klatke w jednym obrazie.
import obrazek

# 4. Zdobadz cytat z obrazka.py
from obrazek import slownik_z_cytatem
z = slownik_z_cytatem['z']

autor = slownik_z_cytatem['autor']

if z == 'zdobadz_cytat':
    ksiega = slownik_z_cytatem['ksiega']
    status = f'Cytat na dziś!\n{ksiega}: {autor}.'
elif z == 'slowo_na_dzis':
    slowo_na_dzis = slownik_z_cytatem['tytul']
    status = f'Słowo na dziś!\nDzisiejsze słowo to: "{slowo_na_dzis}"! Autor: {autor}.'

if is_base64:
    import sys
    from base64 import b64encode
    print(b64encode(open('klatka_ready.jpg', 'rb').read()), file=sys.stderr)
    sys.exit(0)

# python-twitter
import twitter
from ids import on_heroku

if on_heroku:
    consumer_key = os.environ['consumer_key']
    consumer_secret = os.environ['consumer_secret']
    access_token = os.environ['access_token']
    access_token_secret = os.environ['access_token_secret']
else:
    import config
    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_token_secret = config.access_token_secret

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret)


print(api.VerifyCredentials)
print(
    f'randomowa_klatka.wybranyFilm: {randomowa_klatka.wybranyFilm},\nrandomowa_klatka.dlugosc: {randomowa_klatka.dlugosc},\nrandomowa_klatka.losowyCzas: {randomowa_klatka.losowyCzas:.2f}')
api.PostUpdate(status, 'klatka_ready.jpg')

# Posprzataj
os.remove('klatka_ready.jpg')
os.remove('klatka.jpg')
