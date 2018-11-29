#import pytest
from bot.tweet import main
from timeout import timeout

def test_generalny():
    for i in range(10):
        """
        Do zrobienia:
        
        Sprawdź czy wykonanie funkcji przekracza 2 minuty, jeśli tak to rzuć błąd.
        """
        main(test=True, nazwa=f'tests\\output\\klatka_test_ready{i}.jpg')