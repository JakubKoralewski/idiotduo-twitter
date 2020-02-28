"""
Ten plik zdobywa randomową klatkę z filmow Idiot Duo i zapisuje ja do pliku 'klatka.jpg'
"""

import os
import random
import youtube_dl
from ffmpy import FFmpeg

class FrameDownloadError(Exception):
	def __init__(self, message):
		super().__init__(message)


class FrameDownloadAnswer:
	TryElse = 0
	Success = 1

	def Error(message):
		return FrameDownloadError(message)

def zapisz_klatke(url=None,ids=None,seed=None):
	if not ids:
		from .ids import ids

	if not url:
		if seed is not None:
			random.seed(seed*seed + seed)
		url = random.choice(ids)

	ydl_opts = {
		'format': '(bestvideo/best)[protocol!=http_dash_segments]'
	}
	ydl = youtube_dl.YoutubeDL(ydl_opts)

	response = None
	tries = 0
	while response != FrameDownloadAnswer.Success and tries < 5:
		response = zapisz_jedna_klatke(url=url, ydl=ydl)
		if response == FrameDownloadAnswer.TryElse:
			if not ids:
				from .ids import ids
			ids.remove(url)
			url = random.choice(ids)
			return zapisz_klatke(url=url)
		tries += 1
	
	if response != FrameDownloadAnswer.Success:
		raise FrameDownloadAnswer.Error(f"Could not download url: {url}, after {tries+1} tries")
	elif response == FrameDownloadAnswer.Success:
		return response
	else:
		raise FrameDownloadError.Error(f"Got a TryElse even though a TryElse should be handled above.") 
		

def zapisz_jedna_klatke(**args):
	url = args.get('url')
	ydl = args.get('ydl')
	with ydl:
		try:
			info_dict = ydl.extract_info(url, download=False)
		except youtube_dl.DownloadError as e:
			return FrameDownloadAnswer.TryElse
		urlPliku = info_dict.get('url')
		dlugosc = info_dict.get('duration')

	random_time = random.uniform(0, dlugosc)

	print(f'Calkowita dlugosc = {dlugosc}\nWybrana dlugosc = {random_time}')

	assert 0 <= random_time <= dlugosc, 'Randomowo wybrany random_time nie zawiera sie w przedziale <0;dlugosc>'

	user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
	inputs = f'-y -user_agent "{user_agent}"'

	from bot.config import FFMPEG_PATH
	from bot.on_remote import on_remote
	ff = FFmpeg(
		# jesli istnieje environment path do ffmpeg (circleCI[nie zaimplementowano], heroku) to uzyj defaultowej wartosci 'ffmpeg'
		# inaczej dobierz ze .exe ze statica
		executable=FFMPEG_PATH if not on_remote else 'ffmpeg',
		inputs={urlPliku: inputs},
		outputs={os.path.join(os.getcwd(), "output", "klatka.jpg"): f'-ss {random_time:.2f} -frames:v 1 -q:v 2'})

	print(ff.cmd)
	ff.run()
	return FrameDownloadAnswer.Success


if __name__ == '__main__':
	zapisz_klatke()
