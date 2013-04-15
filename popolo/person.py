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
        self['links'] = []
        self['other_names'] = []
        for arg in kwargs:
            self[arg] = kwargs[arg]

    def add_link(self, note, url, **kwargs):
        payload = kwargs.copy()
        payload.update({"note": note, "url": url})
        self['links'].append(payload)

    def add_name(self, name, note, **kwargs):
        payload = kwargs.copy()
        payload.update({"name": name, "note": note})
        self['other_names'].append(payload)
