from popolo.base import PopoloBase


class PopoloOrganization(PopoloBase):
    """
    A single popolo encoded Organization
    """

    _schema_name = "organization"

    def __init__(self, guid, name, **kwargs):
        """
        Constructor for the Organization object.

        We require an ID and a Name, as required by the Popolo spec.
        """
        self['name'] = name
        self['id'] = guid
        self['identifiers'] = []
        for arg in kwargs:
            self[arg] = kwargs[arg]

    def add_identifier(self, identifier, **kwargs):
        data = kwargs.copy()
        data.update({"identifier": identifier})
        self['identifiers'].append(data)
