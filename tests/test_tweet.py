import pytest
from bot.tweet import main
import os

@pytest.mark.webtest
@pytest.mark.parametrize('i', [i for i in range(15)])
def test_15_frames_whole_main_function_but_without_posting(i):
    """
    Do zrobienia:

    Sprawdź czy wykonanie funkcji przekracza 2 minuty, jeśli tak to rzuć błąd.
    """
    main(test=True, nazwa=os.path.join('tests','output', f'klatka_test_ready{i}.jpg'), typ=i)