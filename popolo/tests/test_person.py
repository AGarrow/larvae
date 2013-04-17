from ..person import Person
from validictory import ValidationError


def test_basic_invalid_person():
    """ Test that we can create an invalid person, and validation will fail """
    bob = Person("Bob B. Johnson")
    bob.validate()

    try:
        bob.name = None
        assert not bob.validate()
    except ValidationError:
        pass


def test_magic_methods():
    """ Test the magic methods work """
    bob = Person("John Q. Public, Esq.",
                 gender="male", image="http://example.com/john.jpg",
                 summary="Some person")
    bob.validate()

    bob.add_link("Twitter Account",
                 "http://twitter.com/ev")

    assert bob.links == [
        {"note": "Twitter Account",
         "url": "http://twitter.com/ev"}
    ]

    bob.add_name("Thiston", note="What my friends call me")

    assert bob.other_names == [
        {"name": "Thiston",
         "note": "What my friends call me"}
    ]

    bob.add_name("Johnseph Q. Publico",
                 note="Birth name",
                 start_date="1920-01",
                 end_date="1949-12-31")

    assert bob.other_names == [
        {"name": "Thiston",
         "note": "What my friends call me"},
        {"name": "Johnseph Q. Publico",
         "note": "Birth name",
         "start_date": "1920-01",
         "end_date": "1949-12-31"}
    ]
