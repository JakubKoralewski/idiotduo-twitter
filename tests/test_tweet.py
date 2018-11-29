#import pytest
from bot.tweet import main

def test_10_klatka():
    for i in range(10):
        """
        Do zrobienia:
        
        Sprawdź czy wykonanie funkcji przekracza 2 minuty, jeśli tak to rzuć błąd.
        """
        main(test=True, nazwa=f'tests\\output\\klatka_test_ready.jpg')