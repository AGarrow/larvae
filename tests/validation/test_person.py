from popolo.person import PopoloPerson
from validictory import ValidationError


def test_basic_invalid_person():
    """ Test that we can create an invalid person, and validation will fail """
    bob = PopoloPerson("guid", "Bob B. Johnson")
    bob.validate()

    try:
        bob['name'] = None
        assert False == bob.validate()
    except ValidationError:
        pass
