"""
Ten plik zdobywa randomową klatkę z filmow Idiot Duo i zapisuje ja do pliku 'klatka.jpg'
"""
def zapisz_klatke():
    import os
    import random
    import youtube_dl
    from ffmpy import FFmpeg

    from bot.ids import ids

    wybranyFilm = random.choice(ids)

    ydl_opts = {
        'format': '(bestvideo/best)[protocol!=http_dash_segments]'
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)

    with ydl:
        info_dict = ydl.extract_info(wybranyFilm, download=False)
        urlPliku = info_dict.get('url')
        dlugosc = info_dict.get('duration')

    losowyCzas = random.uniform(0, dlugosc)

    print(f'Calkowita dlugosc = {dlugosc}\nWybrana dlugosc = {losowyCzas}')

    assert 0 <= losowyCzas <= dlugosc, 'Randomowo wybrany losowyCzas nie zawiera sie w przedziale <0;dlugosc>'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    inputs = '-y -user_agent {user_agent}'

    from bot.config import FFMPEG_PATH
    ff = FFmpeg(
        # jesli istnieje environment path do ffmpeg (circleCI[nie zaimplementowano], heroku) to uzyj defaultowej wartosci 'ffmpeg'
        # inaczej dobierz ze .exe ze statica
        executable = FFMPEG_PATH if 'ffmpeg' not in os.environ else 'ffmpeg',
        inputs={urlPliku: inputs},
        outputs={os.path.join(os.getcwd(), "output", "klatka.jpg"): f'-ss {losowyCzas:.2f} -frames:v 1 -q:v 2'})

    print(ff.cmd)
    ff.run()

if __name__ == '__main__':
    zapisz_klatke()