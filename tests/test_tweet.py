import pytest
from bot.tweet import main
import os

@pytest.mark.webtest
def test_10_klatka():
    for i in range(15):
        """
        Do zrobienia:
        
        Sprawdź czy wykonanie funkcji przekracza 2 minuty, jeśli tak to rzuć błąd.
        """
        main(test=True, nazwa=os.path.join('tests','output', f'klatka_test_ready{i}.jpg'), typ=i)