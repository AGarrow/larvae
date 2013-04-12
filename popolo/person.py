from popolo.base import PopoloBase


class PopoloPerson(PopoloBase):
    """
    A single popolo encoded Person.
    """

    _schema_name = "person"

    def __init__(self, guid, name, **kwargs):
        """
        Constructor for the Person object.

        We require a unique ID and name for the person, as required by the
        popolo spec. Additional arguments may be given, which match those
        defined by popolo.
        """
        self['name'] = name
        self['id'] = guid
