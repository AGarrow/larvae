from larvae.base import LarvaeBase
from .schemas.vote import schema


class Vote(LarvaeBase):
    """
    """
    _type = "vote"
    _schema = schema
    __slots__ = ("session", "chamber", "date", "motion", "type", "passed",
                 "bill", "vote_counts", "roll_call", "sources",
                 'openstates_id',)

    def __init__(self, session, date, motion, type, passed,
                 yes_count, no_count, other_count=0,
                 chamber=None, **kwargs):

        super(Vote, self).__init__()

        if not isinstance(type, list):
            type = [type]

        self.session = session
        self.date = date
        self.motion = motion
        self.type = type
        self.passed = passed
        self.chamber = chamber
        self.roll_call = []

        self.vote_counts = [
            {"vote_type": "yes", "count": yes_count},
            {"vote_type": "no", "count": no_count},
            {"vote_type": "other", "count": other_count},
        ]

        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_bill(self, name, id=None, chamber=None):
        self.bill = {
            "id": id,
            "name": name,
            "chamber": chamber
        }

    def vote(self, name, how, id=None):
        self.roll_call.append({
            "vote_type": how,
            "person": {
                "name": name,
                "id": id,
            }
        })

    def yes(self, name, id=None, **kwargs):
        return self.vote(name, 'yes', id=id, **kwargs)

    def no(self, name, id=None, **kwargs):
        return self.vote(name, 'no', id=id, **kwargs)

    def other(self, name, id=None, **kwargs):
        return self.vote(name, 'other', id=id, **kwargs)
