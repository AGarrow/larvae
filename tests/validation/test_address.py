from popolo.address import PopoloAddress


_TEST_ADDRESS = """
20700 North Park Blvd,
University Heights, Ohio
44118"""


def test_invalid_address_entry():
    """ Test to make sure we can't make empty addresses. """
    try:
        assert True == PopoloAddress("guid", 'capitol')
    except ValueError:
        pass


def test_valid_address_entry():
    """ Test to make sure we can create an address """
    address = PopoloAddress("guid", 'capitol', fax="Who the hell uses a fax")
    address = PopoloAddress("guid", 'capitol', address=_TEST_ADDRESS)
