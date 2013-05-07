from larvae.base import LarvaeBase
from larvae.membership import Membership


class Event(LarvaeBase):
    """
    Details for an event in larvae format
    """
    _type = _schema_name = "event"
    __slots__ = ()

    def __init__(self, descr, when, **kwargs):
        pass
