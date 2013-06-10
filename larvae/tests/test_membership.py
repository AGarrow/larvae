from ..membership import Membership


def test_basic_invalid_membership():
    """ Make sure that we can create an invalid membership and break """
    membership = Membership("person_id", "orga_id")
    membership.validate()

    membership.person_id = None
    try:
        assert "nonsense" == membership.validate()
    except ValueError:
        pass


def test_basic_invalid_membership():
    """ Ensure contact details work for memberships """
    membership = Membership("person_id", "orga_id")
    membership.validate()

    membership.add_contact_detail(type='foo',
                                  value='bar',
                                  note='baz')
    membership.validate()
