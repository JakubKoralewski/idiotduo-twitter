import urllib.request
import urllib3.exceptions
import json
import os

on_heroku = False
if 'api_key' in os.environ:
    on_heroku = True
    api_key = os.environ['api_key']
else:
    import config
    api_key = config.api_key

url = 'https://www.googleapis.com/youtube/v3/playlistItems?playlistId=UUIc8KwlF3e3-GW4Y1p0X6tQ&key=' + \
    api_key + '&part=snippet&maxResults=50'

jestNastepnaStrona = None
nextPageToken = None


def zdobadzJSON(*args):
    try:
        #print('Probuje zdobyc token.')
        token = args[0]
        pageToken = f'&token={token}'
    except:
        print('Brak tokena.')
        pageToken = ''
    max_proby = 3
    for i in range(max_proby):
        try:
            with urllib.request.urlopen(url+pageToken) as page:
                print('Zbieram liste filmow.')
                data = json.loads(page.read().decode())
                try:
                    # JEŚLI BĘDZIEMY MIEĆ WIĘCEJ NIŻ 50 FILMÓW
                    # należy szukać nextPageToken, otworzyć go i dodać więcej id
                    print('Patrze czy jest nastepna strona.')
                    nextPageToken = data['nextPageToken']
                    jestNastepnaStrona = True
                except KeyError:
                    print('Jest tylko jedna strona.')
                    jestNastepnaStrona = False
        except urllib3.exceptions.ProtocolError:
            print(f'caught urllib3.exceptions.ProtocolError, trying again!')
            continue
        return data


def zdobadzId(itemy):
    for film in itemy:
        id = film['snippet']['resourceId']['videoId']
        ids.append(id)
    if jestNastepnaStrona:
        print('Biorę id z następnej strony.')
        data = zdobadzJSON(nextPageToken)
        zdobadzId(data['items'])


data = zdobadzJSON()


ids = []

zdobadzId(data['items'])
print('ids: ', ids)
