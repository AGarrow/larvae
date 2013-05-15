from larvae.base import LarvaeBase


class Membership(LarvaeBase):
    """
    A single popolo encoded Membership.
    """

    _type = _schema_name = "membership"
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

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.person_id + ' membership in ' + self.organization_id
    __unicode__ = __str__