from popolo.base import PopoloBase


class Membership(PopoloBase):
    """
    A single popolo encoded Membership.
    """

    _schema_name = "membership"
    __slots__ = ("id", "organization_id", "person_id", "post_id",
                 "role", "start_date", "end_date", "addresses")

    def __init__(self, guid, person_id, organization_id, **kwargs):
        """
        Constructor for the Person object.

        We require a unique ID, person ID, organization ID, as required by the
        popolo spec. Additional arguments may be given, which match those
        defined by popolo.
        """
        self.id = guid
        self.person_id = person_id
        self.organization_id = organization_id
        self.addresses = []

        for k, v in kwargs.items():
            setattr(self, k, v)
