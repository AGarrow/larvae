from ..organization import Organization
from validictory import ValidationError


def test_basic_invalid_organization():
    """ Make sure we can make an invalid orga """
    orga = Organization("name")
    orga.validate()

    orga.name = None
    try:
        assert "Garbage test compare" == orga.validate()
    except ValidationError:
        pass


def test_add_post():
    """ Test that we can hack posts in on the fly'"""
    orga = Organization("name")
    orga.validate()

    orga.add_post("Human Readable Name", "Chef")

    assert orga.posts[0]['role'] == "Chef"
    assert orga.posts[0]['label'] == "Human Readable Name"

    try:
        assert "Garbage" == orga.add_identifier("id10t", foo="bar")
    except TypeError:
        pass

    orga.add_identifier("id10t")
    orga.add_identifier("l0l", scheme="kruft")

    assert orga.identifiers[-1]['scheme'] == "kruft"
    assert orga.identifiers[0]['identifier'] == "id10t"
    assert not hasattr(orga.identifiers[0], "scheme")


def test_add_contact():
    """ test we can add a contact detail to an orga """
    orga = Organization("name")
    orga.validate()

    orga.add_contact_detail(type='pigeon',
                            value='39328',
                            note='His name is Joe')

    orga.validate()
