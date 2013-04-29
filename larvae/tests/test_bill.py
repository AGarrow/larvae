from ..bill import Bill
from validictory import ValidationError


def toy_bill():
    b = Bill(bill_id="HB 2017",
             session="2012A",
             title="A bill for an act to raise the cookie budget by 200%",
             type="bill")
    b.add_source("http://uri.example.com/", note="foo")
    b.validate()
    return b


def test_basic_invalid_bill():
    """ Test that we can create an invalid bill, and validation will fail """
    b = toy_bill()
    b.bill_id = None
    try:
        assert ("Big Garbage String") == b.validate()
    except ValidationError:
        pass


def test_verify_actions():
    """ Make sure actions work """
    b = toy_bill()
    b.add_action("Some dude liked it.", "some dude", "2013-04-29")
    b.validate()
