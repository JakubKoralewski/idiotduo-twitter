"""
Zwraca informację czy skrypt znajduje się na heroku
"""
import os

if 'api_key' in os.environ:
    on_remote = True
else:
    on_remote = False
