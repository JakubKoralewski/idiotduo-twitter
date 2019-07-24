from bot.image.ids import ids

def test_ids():
    """
    Sprawdź pozyskiwanie id z YouTube wszystkich filmów Idiot Duo.
    """
    assert ids
    assert len(ids) > 0
