from popolo.base import PopoloBase


class PopoloAddress(PopoloBase):
    """
    A single popolo encoded Address object.
    """

    _schema_name = "address"
    _address_types = [ "address", "voice", "fax", "cell",
                      "tollfree", "video", "pager", "textphone", ]

    def __init__(self, guid, type_, **kwargs):
        """
        """
        self['id'] = guid
        self['type'] = type_
        for arg in kwargs:
            self[arg] = kwargs[arg]

    def _validate(self):
        if set(self.keys()).intersection(set(self._address_types)) == set([]):
            raise ValueError("Expected at least one address entry")
