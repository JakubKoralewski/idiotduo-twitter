"""
Ten plik bierze wszystkie dane wygenerowane przez poprzednie skrypty i umieszcza je na Twitterze.
"""

""" # vscode debugger
import sys
sys.path.append('F:\\projects\\twitter_idiot_duo_bot\\idiotduobiblia_heroku')
print(f'sys.path: {sys.path}\n') """


def main(**kwargs):
	from bot.image.randomowa_klatka import zapisz_klatke
	from bot.image.obrazek import zapisz_obrazek
	from bot.text_src import slowo_na_dzis, get_rnm_quote, zdobadz_cytat
	from pprint import pprint
	args = kwargs.get('args')
	is_test = kwargs.get('test', False)
	nazwa = kwargs.get('nazwa', None)
	typ = kwargs.get('typ', None)
	string_val = kwargs.get('string_val', None)
	
	# for unit testing:
	if args:
		is_test = args.test
		typ = args.typ
		string_val = args.string

	zapisz_klatke()
	slownik_z_cytatem = {}

	# jesli dostarczono argument --string
	if string_val:
		# jesli dostarczony argument jest liczba
		if string_val.isdigit():
			# wygeneruj randomowy string
			import string
			import random
			print('parametr "string" to nie string wiec generuje tekst')
			string = ''.join(random.choices(
				string.digits + string.ascii_letters + ' ', k=int(string_val)))
		else:
			# jesli dostarczono numer
			string = string_val
		print(f'string: {string}')
		zapisz_obrazek(cytat=string, nazwa=nazwa)
		
		slownik_z_cytatem['z'] = 'zdobadz_cytat'
		slownik_z_cytatem['autor'] = 'IDIOT FAKEN DUO'
		slownik_z_cytatem['ksiega'] = '420 6,9 XD'
	else:
		# to dzieje się w produkcji
		# manual selection
		possible_quotes = [zdobadz_cytat, slowo_na_dzis, get_rnm_quote]
		if typ in ['zdobadz_cytat', 'cytat', 'biblia_cytat']:
			print("Manual override: cytat z biblii")
			slownik_z_cytatem = zdobadz_cytat()
		elif typ in ['rnm', 'rick-and-morty', "rick_and_morty"]:
			print("Manual override: rick and morty")
			slownik_z_cytatem = get_rnm_quote()
			pprint(slownik_z_cytatem)
		elif typ in ["slowo_na_dzis", "offline", "swd", "swnd", "slowo-na-dzis"]:
			print("Manual override: offline slowo na dzis")
			slownik_z_cytatem = slowo_na_dzis()
		else:
			try:
				# if it's a number
				ai_selection = int(typ) % 3
			except:
				# automatic selection
				import datetime
				day = datetime.datetime.now().day
				ai_selection = day % 3
			slownik_z_cytatem = possible_quotes[ai_selection]()
		zapisz_obrazek(cytat=slownik_z_cytatem["cytat"].strip(), nazwa=nazwa)


	z = slownik_z_cytatem['z']
	autor = slownik_z_cytatem['autor']

	if z in ['zdobadz_cytat', 'rick_and_morty']:
		ksiega = slownik_z_cytatem['ksiega']
		status = f'Cytat na dziś!\n{ksiega}: {autor}.'
	elif z == 'slowo_na_dzis':
		slowo_na_dzis = slownik_z_cytatem['tytul']
		status = f'Słowo na dziś!\nDzisiejsze słowo to: "{slowo_na_dzis}"! Autor: {autor}.'

	if is_test:
		print(f'status: {status}\nklatka_ready.jpg powinna byc dla ciebie gotowa')
		print('spelniono test, wychodze')
		return

	# python-twitter
	import twitter
	from bot.on_remote import on_remote

	if on_remote:
		import os
		consumer_key = os.environ['consumer_key']
		consumer_secret = os.environ['consumer_secret']
		access_token = os.environ['access_token']
		access_token_secret = os.environ['access_token_secret']
	else:
		from bot.config_secret import consumer_key, consumer_secret, access_token, access_token_secret

	api = twitter.Api(consumer_key=consumer_key,
					consumer_secret=consumer_secret,
					access_token_key=access_token,
					access_token_secret=access_token_secret)

	print(api.VerifyCredentials)

	if not on_remote:
		odp = input("Na pewno chcesz wstawic tweeta nie bedac na heroku?")
		if odp.lower() not in ['yes', 'tak']:
			print('Zdecydowales nie wstawiac tweeta.\nUWAGA! Wychodze!')
			return
	api.PostUpdate(status, 'klatka_ready.jpg')


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Wytweetuj obrazek.')
	parser.add_argument(
		'--string', '-s', help='sprecyzuj wybrany tekst (int or str)', default=None)
	parser.add_argument('--test', '-t', action='store_true', default=False,
						help='dla testow lokalnych')
	# opcjonalnie automatycznie stworz podana ilosc tweetów
	parser.add_argument('--ilosc', '-i', type=int, default=None,
						help='ile razy wykonac to cus')
	# czy slowo_na_dzis czy zdobadz_cytat
	parser.add_argument('--typ', '-x', default=None,
						help='czy slowo_na_dzis czy zdobadz_cytat')

	args = parser.parse_args()
	ilosc = args.ilosc

	from bot.on_remote import on_remote
	if on_remote:
		import sentry_sdk
		import os
		sentry_url = os.environ['SENTRY_URL']
		sentry_sdk.init(sentry_url)

	if not ilosc:
		ilosc = 1
	else:
		print(f'Wybrales ilosc rowna {ilosc}.')
	
	for i in range(ilosc):
		if ilosc != 1:
			print(f'{i+1}. wykonanie.')
		main(args=args)