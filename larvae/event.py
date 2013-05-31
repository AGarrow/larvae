from larvae.base import LarvaeBase

from larvae.organization import Organization
from larvae.person import Person
from larvae.bill import Bill

from .schemas.event import schema


class EventAgendaItem(dict):
    event = None

    def __init__(self, note, event):
        super(EventAgendaItem, self).__init__({
            "note": note,
            "related_entities": []
        })
        self.event = event

    def add_committee(self, committee, type='participant'):
        self.add_entity(committee, 'committee', None, type)

    def add_bill(self, bill, type='consideration'):
        self.add_entity(bill, 'bill', None, type)

    def add_person(self, person, type='participant'):
        self.add_entity(person, 'person', None, type)

    def add_entity(self, entity, entity_type, entity_id, type):
        self['related_entities'].append({
            "entity": entity,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "type": type,
        })


class Event(LarvaeBase):
    """
    Details for an event in larvae format
    """
    _type = "event"
    _schema = schema
    __slots__ = ("start", "all_day", "description", "documents",
                 "end", "links", "location", "participants",
                 "agenda", "sources", "canceled", "type", 'session')

    def __init__(self, description, start, location, session=None, **kwargs):
        super(Event, self).__init__()
        self.start = start
        self.description = description
        self.all_day = False
        self.documents = []
        self.end = None
        self.links = []
        self.location = location
        self.participants = []
        self.agenda = []
        self.sources = []
        self.canceled = False
        self.type = "event"
        self._related = []
        self.session = session

        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_source(self, url, note=None):
        info = { "url": url, "note": note }
        self.sources.append(info)

    def add_link(self, url, note=None):
        info = { "url": url, "note": note }
        self.links.append(info)

    def add_document(self, note, url):
        self.documents.append({
            "note": note,
            "url": url
        })

    def add_person(self, who, type='participant', chamber=None):
        return self.add_participant(
            participant=who,
            participant_type='person',
            chamber=chamber,
            type=type)

    def add_participant(self, participant, participant_type,
                        type='participant', chamber=None):
        self.participants.append({
            "chamber": chamber,
            "type": type,
            "participant_type": participant_type,
            "participant": participant
        })

    def add_agenda_item(self, note):
        obj = EventAgendaItem(note, self)
        self.agenda.append(obj)
        return obj
