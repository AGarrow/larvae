from larvae.base import LarvaeBase
from .schemas.event import schema


class Event(LarvaeBase):
    """
    Details for an event in larvae format
    """
    _type = "event"
    _schema = schema
    __slots__ = ("start", "all_day", "description", "documents",
                 "end", "links", "location", "notes", "participants",
                 "agenda", "sources", "canceled", "type",)

    def __init__(self, description, start, location, **kwargs):
        super(Event, self).__init__()
        self.start = start
        self.description = description
        self.all_day = False
        self.documents = []
        self.end = None
        self.links = []
        self.location = location
        self.notes = []
        self.participants = []
        self.agenda = []
        self.sources = []
        self.canceled = False
        self.type = "event"

        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_source(self, url, note=None):
        self.sources.append({
            'url': url,
            "note": note
        })

    def add_link(self, url, note=None):
        self.links.append({
            "url": url,
            "note": note
        })
