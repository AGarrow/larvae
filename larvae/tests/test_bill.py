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
    # XXX: Check output


def test_verify_related_bill():
    """ Make sure related bills work """
    b = toy_bill()
    b.add_related_bill(bill_id="HB 2020",
                       session="2011A",
                       chamber="upper",
                       relation="companion")  # continuation?
    b.validate()


def test_verify_documents():
    """ Make sure we can add documents """
    b = toy_bill()
    b.add_document(name="Fiscal Impact",
                   date="2013-04",
                   type='foo')

    links = [{
        "url": "http://foo.bar.baz",
    }, {
        "url": "http://hi.example.com/foo#bar",
        "mimetype": "text/html"
    }]
    b.add_document(name="Fiscal Impact",
                   date="2013-04",
                   type='foo',
                   links=links)
    b.validate()

    links.append({"mimetype": "foo"})
    b.add_document(name="Fiscal Impact",
                   date="2013-04",
                   type='foo',
                   links=links)
    try:
        assert ("This shouldn't happen") == b.validate()
    except ValidationError:
        pass


def test_verify_sponsors():
    """ Make sure sponsors work """
    b = toy_bill()
    b.add_sponsor(name="Joe Bleu",
                  sponsorship_type="Author",
                  entity_type="legislator",
                  primary=True,
                  chamber="upper")
    b.validate()
