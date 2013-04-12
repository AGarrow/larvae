from popolo.base import PopoloBase


class PopoloMembership(PopoloBase):
    """
    A single popolo encoded Membership.
    """

    _schema_name = "membership"

    def __init__(self, guid, person_id, organization_id, **kwargs):
        """
        Constructor for the Person object.

        We require a unique ID, person ID, organization ID, as required by the
        popolo spec. Additional arguments may be given, which match those
        defined by popolo.
        """
        self['id'] = guid
        self['person_id'] = person_id
        self['organization_id'] = organization_id
        for arg in kwargs:
            self[arg] = kwargs[arg]
