"""
Zwraca informację czy skrypt znajduje się na heroku
"""
import os

if 'api_key' in os.environ:
    on_heroku = True
else:
    on_heroku = False
