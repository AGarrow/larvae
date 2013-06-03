from ..event import Event
import datetime as dt


def event_obj():
    e = Event(description="get-together",
              start=dt.datetime.utcnow(),
              location="Joe's Place")

    e.add_source(url='foobar')
    e.validate()
    return e


def test_basic_event():
    """ test that we can create an event """
    e = Event(description="get-together",
              start=dt.datetime.utcnow(),
              location="Joe's Place")

    e.add_source(url='foobar')
    e.validate()

    e.add_link("http://foobar.baz")
    e.add_link("http://foobar.baz", note="foo")
    e.validate()

    assert len(e.links) == 2


def test_basic_agenda():
    e = Event(description="get-together",
              start=dt.datetime.utcnow(),
              location="Joe's Place")

    e.add_source(url='foobar')
    e.validate()

    agenda = e.add_agenda_item("foo bar")
    e.validate()


def test_add_person():
    e = event_obj()
    agenda = e.add_agenda_item("foo bar")
    assert agenda['related_entities'] == []

    agenda.add_person(person='John Q. Hacker', type='chair')
    e.validate()


def test_add_committee():
    e = event_obj()
    agenda = e.add_agenda_item("foo bar")
    assert agenda['related_entities'] == []

    agenda.add_committee(committee='Hello, World', type='host')
    e.validate()


def test_add_bill():
    e = event_obj()
    agenda = e.add_agenda_item("foo bar")
    assert agenda['related_entities'] == []
    agenda.add_bill(bill='HB 101', type='consideration')
    e.validate()


def test_add_document():
    e = event_obj()
    assert e.documents == []
    e.add_document(name='hello', url='http://example.com')
    assert len(e.documents) == 1
    o = e.documents[0]
    assert o['name'] == 'hello'
    assert o['url'] == 'http://example.com'
    e.validate()
