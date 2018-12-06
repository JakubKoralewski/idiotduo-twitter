#import pytest
from bot.tweet import main
import os

def test_10_klatka():
    for i in range(10):
        """
        Do zrobienia:
        
        Sprawdź czy wykonanie funkcji przekracza 2 minuty, jeśli tak to rzuć błąd.
        """
        main(test=True, nazwa=os.path.join('tests','output', f'klatka_test_ready{i}.jpg'))

def test_5_zdobadz_cytat():
    for i in range(10, 15):
        """
        Sprawdź czy działa określony tryb, czyli selenium twojabiblia.pl/...
        """
        main(test=True, nazwa=os.path.join('tests','output', f'klatka_test_ready{i}.jpg'), typ='biblia_cytat')