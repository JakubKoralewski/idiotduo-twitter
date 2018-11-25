"""
Ten plik bierze wszystkie dane wygenerowane przez poprzednie skrypty i umieszcza je na Twitterze.
"""
import os
import argparse
import random
import string

parser = argparse.ArgumentParser(description='Wytweetuj obrazek.')
#parser.add_argument('--base64', type=bool, nargs='?', default=False, const=True, help='wypluj obrazek w base64')
parser.add_argument('--base64','-b64', action='store_true',
                    help='wypluj obrazek w base64 (dla testow na heroku)')
parser.add_argument('--string', '-s', help='sprecyzuj wybrany tekst (int or str)')
parser.add_argument('--test', '-t', action='store_true', help='dla testow lokalnych')
args = parser.parse_args()
is_base64 = args.base64
string_info = args.string
is_test = args.test

if is_test and is_base64:
    raise Exception(f"Nie mozesz jednoczesnie testowac lokalnie i na heroku!\nis_test = {is_test}, is_base64 = {is_base64}")

if not isinstance(string_info, str):
    string = ''.join(random.choices(string.digits + string.ascii_letters + ' ', k=string_info))
else:
    string = string_info

print(f'string: {string}')


# Kolejnosc wykonywania dzialan:

# 1. Zdobadz klatke z Youtube.
import randomowa_klatka
# 2. Zdobadz cytat.
#import zdobadz_cytat
# 3. Polacz cytat i klatke w jednym obrazie.
import obrazek
obrazek.zapisz_obrazek(cytat=string)


# 4. Zdobadz cytat z obrazka.py
z = obrazek.slownik_z_cytatem['z']
autor = obrazek.slownik_z_cytatem['autor']

if z == 'zdobadz_cytat':
    ksiega = obrazek.slownik_z_cytatem['ksiega']
    status = f'Cytat na dziś!\n{ksiega}: {autor}.'
elif z == 'slowo_na_dzis':
    slowo_na_dzis = obrazek.slownik_z_cytatem['tytul']
    status = f'Słowo na dziś!\nDzisiejsze słowo to: "{slowo_na_dzis}"! Autor: {autor}.'

if is_base64:
    import sys
    from base64 import b64encode
    print(b64encode(open('klatka_ready.jpg', 'rb').read()), file=sys.stderr)
    print('spelniono test(b64), wychodze')
    sys.exit(0)

elif is_test:
    print(f'status: {status}\nklatka_ready.jpg powinna byc dla ciebie gotowa')
    print('spelniono test, wychodze')
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
