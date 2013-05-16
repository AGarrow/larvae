from larvae.base import LarvaeBase
from .schemas.event import schema


class Event(LarvaeBase):
    """
    Details for an event in larvae format
    """
    _type = "event"
    _schema = schema
    __slots__ = ("when", "all_day", "description", "documents",
                 "end", "links", "location", "notes", "participants",
                 "agenda", "sources", "status", "type",)

    def __init__(self, description, when, **kwargs):
        super(Event, self).__init__()
        self.when = when
        self.description = description
        self.all_day = False
        self.documents = []
        self.end = None
        self.links = []
        self.location = None
        self.notes = []
        self.participants = []
        self.agenda = []
        self.sources = []
        self.status = "current"
        self.type = "event"

        for k, v in kwargs.items():
            setattr(self, k, v)
