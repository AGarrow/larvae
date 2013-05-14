from ..event import Event


def test_basic_invalid_person():
    """ test that we can create an event """
    Event("get-together", "2013-04")
