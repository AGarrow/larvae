from popolo.organization import PopoloOrganization
from validictory import ValidationError


def test_basic_invalid_organization():
    """ Make sure we can make an invalid orga """
    orga = PopoloOrganization("guid", "name")
    orga.validate()

    orga['name'] = None
    try:
        assert "Garbage test compare" == orga.validate()
    except ValidationError:
        pass
