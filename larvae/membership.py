from larvae.base import LarvaeBase
from .schemas.membership import schema


class Membership(LarvaeBase):
    """
    A single popolo encoded Membership.
    """

    _type = "membership"
    _schema = schema
    __slots__ = ("organization_id", "person_id", "post_id", "role",
                 "start_date", "end_date", "contact_details", "district",
                 "chamber")

    def __init__(self, person_id, organization_id, **kwargs):
        """
        Constructor for the Person object.

        We require a person ID and organization ID, as required by the
        popolo spec. Additional arguments may be given, which match those
        defined by popolo.
        """
        super(Membership, self).__init__()
        self.person_id = person_id
        self.organization_id = organization_id
        self.contact_details = []
        self.start_date = None
        self.end_date = None
        self.post_id = None
        self.role = None

        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_contact_detail(self, type, value, note):
        self.contact_details.append({"type": type,
                                     "value": value,
                                     "note": note})

    def __str__(self):
        return self.person_id + ' membership in ' + self.organization_id
    __unicode__ = __str__
