from larvae.base import LarvaeBase


class Membership(LarvaeBase):
    """
    A single popolo encoded Membership.
    """

    _schema_name = "membership"
    __slots__ = ("_id", "organization_id", "person_id", "post_id",
                 "role", "start_date", "end_date", "contact_details")

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

        for k, v in kwargs.items():
            setattr(self, k, v)
