import requests
from bot.on_remote import on_remote
if on_remote:
	from os import environ
	api_key = environ['YANDEX_API']
	del environ
else:
	from bot.config_secret import yandex_api as api_key
import json
from pprint import pprint
from time import sleep

class TranslationError(Exception):
	def __init__(self, message, text=None, lang=None, code=None, answer=None):
		super().__init__(message)

def translate(text, lang=None):
	r = requests.get(f"https://translate.yandex.net/api/v1.5/tr.json/translate?key={api_key}&text={text}&lang={lang}")
	print("json:")
	answer = r.json()
	if answer['code'] >= 400:
		print(answer)
		raise TranslationError(f"Error code {answer['code']} from Yandex.", text=text, lang=lang, answer=answer)
	return answer['text'][0]

def translate_quadruple(text,lang=None):
	translated_quote = text
	langs = ["pl", "la", "mn", "pl"]
	for i in range(4):
		lang = langs[i]
		translated_quote = translate(translated_quote, lang=lang)
	return translated_quote

if __name__ == "__main__":
	print(translate_quadruple("I'm so sorry! Heavenly heads and cranial creator, forgive my \
		transgressions against family and community. May my chores complete \
		me as I complete them. - Morty. - Birdperson? You appear to be \
		dying. I will make efforts to prevent this but can promise nothing.", lang="pl"))
