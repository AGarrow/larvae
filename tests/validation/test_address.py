from popolo.address import PopoloAddress


def test_invalid_address_entry():
    """ Test to make sure we can't make empty addresses. """
    try:
        assert True == PopoloAddress("guid", 'capitol')
    except ValueError:
        pass


def test_valid_address_entry():
    """ Test to make sure we can create an address """
    address = PopoloAddress("guid", 'capitol', fax="Who the hell uses a fax")
