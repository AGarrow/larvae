from ..organization import PopoloOrganization
from validictory import ValidationError


def test_basic_invalid_organization():
    """ Make sure we can make an invalid orga """
    orga = PopoloOrganization("guid", "name")
    orga.validate()

    orga.name = None
    try:
        assert "Garbage test compare" == orga.validate()
    except ValidationError:
        pass


def test_add_post():
    """ Test that we can hack posts in on the fly'"""
    orga = PopoloOrganization("guid", "name")
    orga.validate()

    orga.add_post("pguid", "Human Readable Name", "Chef")

    assert orga.posts == [
        {"id": "pguid",
         "role": "Chef",
         "label": "Human Readable Name",
        }
    ]

    try:
        orga.add_post(None, "Human Readable Name", "Chef")
        assert ("Garbage compare") == orga.validate()
    except ValidationError:
        pass

