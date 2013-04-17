from ..membership import PopoloMembership


def test_basic_invalid_membership():
    """ Make sure that we can create an invalid membership and break """
    membership = PopoloMembership("guid", "person_id", "orga_id")
    membership.validate()

    membership['person_id'] = None
    try:
        assert "nonsense" == membership.validate()
    except ValueError:
        pass
