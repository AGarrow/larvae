from ..event import Event
from validictory import ValidationError


def test_basic_invalid_person():
    """ test that we can create an event """
    bob = Event("get-together", "2013-04")
