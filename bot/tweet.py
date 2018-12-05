"""Ten plik bierze wszystkie dane wygenerowane przez poprzednie skrypty i umieszcza je na Twitterze.
"""
string_val = False
is_test = False


""" # vscode debugger
import sys
sys.path.append('F:\\projects\\twitter_idiot_duo_bot\\idiotduobiblia_heroku')
print(f'sys.path: {sys.path}\n') """


def main(**kwargs):
    import os
    print(f'cwd: {os.getcwd()}')
    for root, dirs, files in os.walk(os.path.join(os.getcwd(),'static')):
        print(f'root: {root},\ndirs: {dirs},\nfiles: {files}')
    # for unit testing
    is_test = kwargs.get('test', False)
    nazwa = kwargs.get('nazwa', False)

    from bot.randomowa_klatka import zapisz_klatke
    zapisz_klatke()

    from bot.obrazek import zapisz_obrazek
    slownik_z_cytatem = {}
    # jesli dostarczono argument --string
    if string_val:
        # to wtedy test
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
        # inaczej 4real is happenink!
        try:
            from bot.zdobadz_cytat import biblia_cytat
            slownik_z_cytatem = biblia_cytat()
            x = slownik_z_cytatem["cytat"]
        except:
            from bot.slowo_na_dzis import slowo_na_dzis
            slownik_z_cytatem = slowo_na_dzis()
        zapisz_obrazek(cytat=slownik_z_cytatem["cytat"].strip(), nazwa=nazwa)


    z = slownik_z_cytatem['z']
    autor = slownik_z_cytatem['autor']

    if z == 'zdobadz_cytat':
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
    from bot.ids import on_remote

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
        if odp.lower() not in ['yes']:
            print('Zdecydowales nie wstawiac tweeta.\nUWAGA! Wychodze!')
            return
    api.PostUpdate(status, 'klatka_ready.jpg')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Wytweetuj obrazek.')
    parser.add_argument(
        '--string', '-s', help='sprecyzuj wybrany tekst (int or str)')
    parser.add_argument('--test', '-t', action='store_true',
                        help='dla testow lokalnych')
    # opcjonalnie automatycznie stworz podana ilosc tweetów
    parser.add_argument('--ilosc', '-i', type=int,
                        help='ile razy wykonac to cus')
    args = parser.parse_args()
    string_val = args.string
    is_test = args.test
    ilosc = args.ilosc
    if not ilosc:
        ilosc = 1
    for i in range(ilosc):
        main()