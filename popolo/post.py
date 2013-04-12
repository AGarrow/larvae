from popolo.base import PopoloBase


class PopoloPost(PopoloBase):
    """
    A single popolo encoded Post object.
    """

    _schema_name = "post"

    def __init__(self, guid, label, organization_id, role, **kwargs):
        """
        Constructor for the Post object.

        We require an ID, label, organization id and a role, as required
        by the Popolo spec. Additional keys may be entered as well, and placed
        lovingly onto the object.
        """
        self['id'] = guid
        self['label'] = label
        self['organization_id'] = organization_id
        self['role'] = role  # XXX: validate role.

        for arg in kwargs:
            self[arg] = kwargs[arg]
