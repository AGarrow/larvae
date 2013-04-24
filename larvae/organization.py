from larvae.base import LarvaeBase


class Organization(LarvaeBase):
    """
    A single popolo encoded Organization
    """

    __slots__ = ('classification', 'dissolution_date', 'founding_date',
                 '_id', 'identifiers', 'name', 'other_names', 'parent_id',
                 'posts', 'geography_id', 'contact_details')

    _post_slots = ('contact_details', 'end_date', 'id', 'label',
                   'organization_id', 'role', 'start_date', 'chamber',
                   'district', 'geography_id')

    _schema_name = "organization"

    def __init__(self, name, **kwargs):
        """
        Constructor for the Organization object.
        """
        super(Organization, self).__init__()
        self.name = name
        self.identifiers = []
        self.posts = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_identifier(self, identifier, scheme=None):
        data = {"identifier": identifier}
        if scheme:
            data['scheme'] = scheme
        self.identifiers.append(data)

    def add_post(self, guid, label, role, **kwargs):
        post = {"id": guid, "label": label, "role": role}
        for k, v in kwargs.items():
            if k not in self._post_slots:
                raise AttributeError(
                    '{0} not a valid kwarg for add_post'.format(k))
            post[k] = v
        self.posts.append(post)
