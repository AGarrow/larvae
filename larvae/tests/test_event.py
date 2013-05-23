from ..event import Event


def test_basic_invalid_person():
    """ test that we can create an event """
    e = Event(description="get-together",
              start="2013-04",
              location="Joe's Place")

    e.add_source(url='foobar')
    e.validate()

    e.add_link("http://foobar.baz")
    e.add_link("http://foobar.baz", note="foo")
    e.validate()
