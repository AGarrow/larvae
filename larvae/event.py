from larvae.base import LarvaeBase
from .schemas.event import schema


class Event(LarvaeBase):
    """
    Details for an event in larvae format
    """
    _type = "event"
    _schema = schema
    __slots__ = ()

    def __init__(self, descr, when, **kwargs):
        pass
