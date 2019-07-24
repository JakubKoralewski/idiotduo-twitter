from bot.config import RICK_AND_MORTY_SCREENPLAY_URL
from selenium import webdriver
from bot.on_remote import on_remote
from pprint import pprint
import random
import re

from .translate import translate

OPTIMAL_CHARACTER_COUNT = 200

def get_rnm_quote():
	if on_remote:
		driver = webdriver.Chrome()
	else:
		from bot.config import WEB_DRIVER_PATH
		import os
		print(f'cwd: {os.getcwd()}')
		print(f'webpath: {WEB_DRIVER_PATH}')
		driver = webdriver.Chrome(executable_path=WEB_DRIVER_PATH)
	with driver:
		driver.get(RICK_AND_MORTY_SCREENPLAY_URL)
		episodes = driver.find_elements_by_class_name('season-episode-title')
		episode = random.choice(episodes)
		del episodes
		episode_title = episode.text[3:]
		episode_url = episode.get_attribute('href')

		episode_data = episode_url.split('&')[1].split('=')[1]
		season = int(episode_data[1:3])
		episode = int(episode_data[4:7])
		del episode_data
		
		driver.get(episode_url)
		del episode_url

		text_element = driver.find_element_by_class_name('scrolling-script-container')
		text = text_element.text
		del text_element
		punctuation = "?.!"
		split_text = re.split(f"([{punctuation}])", text)
		
		# Get random quote
		index = random.randrange(0, len(split_text) - 30)

		character_count = 0
		split_quote = []
		
		while character_count < OPTIMAL_CHARACTER_COUNT:
			quote = split_text[index].strip()
			if not quote.endswith(("mr.", "mrs.")):
				character_count += len(quote)
			split_quote.append(quote)
			index += 1
			
		quote = ""
		for q in split_quote:
			if len(q) < 2:
				quote += f"{q} "
			else:
				quote += q
		for i in range(2):
			if quote[0] in f"{punctuation} ":
				# Remove punctuation and spaces at the beginning
				quote = quote[1:]
		if quote[-1] not in punctuation:
			# Add punctuation at the end
			quote = quote + "."
		
		print(f'quote before translating:\n{quote}')
		quote = translate(quote, lang="pl")
		print(f'quote:\n{quote}')

		return {
			'cytat': quote,
			'autor': "Księga Ryszarda i Mortymera",
			'ksiega': f"{translate(episode_title, lang='pl')} {season}, {episode}",
			'z': 'rick_and_morty'
		}
		
		
if __name__ == "__main__":
	pprint(get_rnm_quote())
		