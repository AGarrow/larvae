from ..event import Event


def test_basic_invalid_person():
    """ test that we can create an event """
    e = Event(description="get-together",
              when="2013-04")
    e.validate()
