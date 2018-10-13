"""
Ten plik zdobywa randomową klatkę z filmow Idiot Duo i zapisuje ja do pliku klatka.jpg
"""
import os
import urllib.request
import json
import random
import youtube_dl
from ffmpy import FFmpeg

url = 'https://www.googleapis.com/youtube/v3/playlistItems?playlistId=UUIc8KwlF3e3-GW4Y1p0X6tQ&key=' + \
    os.environ['api_key'] + '&part=snippet&maxResults=50'

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

    with urllib.request.urlopen(url+pageToken) as page:
        print('Zbieram liste filmow.')
        data = json.loads(page.read().decode())
        try:
            # JEŚLI BĘDZIEMY MIEĆ WIĘCEJ NIŻ 50 FILMÓW
            # należy szukać nextPageToken, otworzyć go i dodać więcej id
            print('Probuje zdobyc nastepna strone.')
            nextPageToken = data['nextPageToken']
            jestNastepnaStrona = True
        except KeyError:
            print('Jest tylko jedna strona.')
            jestNastepnaStrona = False

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


with open('playlistitems.json', 'r', encoding='UTF-8') as f:
    data = json.load(f)

ids = []

zdobadzId(data['items'])
print('ids: ', ids)

wybranyFilm = random.choice(ids)

ydl_opts = {
    'format': 'bestvideo/best',
    'outtmpl': 'klatka.jpg',
    'external_downloader': 'ffmpeg.exe',
    'external_downloader_args': None,
    'verbose': True,
    'debug_printtraffic': True
}
ydl = youtube_dl.YoutubeDL(ydl_opts)

with ydl:
    info_dict = ydl.extract_info(wybranyFilm, download=False)
    urlPliku = info_dict.get('url')
    dlugosc = info_dict.get('duration')

losowyCzas = random.uniform(0, dlugosc)

ff = FFmpeg(
    inputs={urlPliku: '-y'},
    outputs={'klatka.jpg': f'-ss {losowyCzas:.2f} -vframes 1 -q:v 2'}
)

print(ff.cmd)
ff.run()
