from larvae.base import LarvaeBase

from larvae.organization import Organization
from larvae.utils import add_associated_link
from larvae.person import Person
from larvae.bill import Bill

from .schemas.event import schema


class EventAgendaItem(dict):
    event = None
    _add_associated_link = add_associated_link

    def __init__(self, description, event):
        super(EventAgendaItem, self).__init__({
            "description": description,
            "related_entities": [],
            "subjects": [],
            "media": [],
        })
        self.event = event

    def add_subject(self, what):
        self['subjects'].append(what)

    def add_committee(self, committee, id=None, type='participant'):
        self.add_entity(committee, 'committee', id, type)

    def add_bill(self, bill, id=None, type='consideration'):
        self.add_entity(bill, 'bill', id, type)

    def add_person(self, person, id=None, type='participant'):
        self.add_entity(person, 'person', id, type)

    def add_media_link(
        self, name, url, type='media',
        mimetype=None,
        offset=None,
        on_duplicate='error'
    ):
        return self._add_associated_link(
            collection='media',
            name=name,
            url=url,
            type=type,
            offset=offset,
            mimetype=mimetype,
            on_duplicate=on_duplicate)


    def add_entity(self, name, entity_type, id, type):
        self['related_entities'].append({
            "name": name,
            "entity_type": entity_type,
            "id": id,
            "type": type,
        })


class Event(LarvaeBase):
    """
    Details for an event in larvae format
    """
    _type = "event"
    _schema = schema
    __slots__ = ("when", "all_day", "name", "description", "documents",
                 "end", "links", "location", "participants",
                 "agenda", "sources", "status", "type", 'session',
                 'openstates_id',)

    def __init__(self, name, when, location, session=None, **kwargs):
        super(Event, self).__init__()
        self.when = when
        self.name = name
        self.all_day = False
        self.documents = []
        self.end = None
        self.links = []
        self.location = {"name": location,
                         "note": None,
                         "coordinates": None}
        self.participants = []
        self.agenda = []
        self.sources = []
        self.status = "confirmed"
        self.type = "event"
        self._related = []
        self.session = session

        for k, v in kwargs.items():
            setattr(self, k, v)

    def set_coordinates(self, lat, lon):
        self.location['coordinates'] = {
            "latitude": lat,
            "longitude": lon
        }

    def add_source(self, url, note=None):
        info = { "url": url, "note": note }
        self.sources.append(info)

    def add_link(self, url, note=None):
        info = { "url": url, "note": note }
        self.links.append(info)

    def add_document(self, name, url):
        self.documents.append({
            "name": name,
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

    def add_agenda_item(self, description):
        obj = EventAgendaItem(description, self)
        self.agenda.append(obj)
        return obj
