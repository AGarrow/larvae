from larvae.base import LarvaeBase


class Organization(LarvaeBase):
    """
    A single popolo encoded Organization
    """

    __slots__ = ('classification', 'dissolution_date', 'founding_date',
                 'identifiers', 'name', 'other_names', 'parent_id',
                 'posts', 'openstates_id', 'contact_details', 'geography_id')

    _post_slots = ('end_date', 'id', 'label', 'organization_id', 'role',
                   'start_date', 'chamber', 'district', 'geography_id',
                   'num_seats')

    _type = _schema_name = "organization"

    def __init__(self, name, **kwargs):
        """
        Constructor for the Organization object.
        """
        super(Organization, self).__init__()
        self.name = name
        self.identifiers = []
        self.posts = []
        self.contact_details = []
        self._related = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.name
    __unicode__ = __str__

    def __repr__(self):
        as_dict = self.as_dict()
        list(map(as_dict.pop, ('_type', '_id', 'name')))
        args = (self.__class__.__name__, self.name, as_dict)
        return '%s(name=%r, **%r)' % args

    @property
    def parent(self):
        return self.parent_id

    @parent.setter
    def parent(self, val):
        self.parent_id = val._id

    def add_identifier(self, identifier, scheme=None):
        data = {"identifier": identifier}
        if scheme:
            data['scheme'] = scheme
        self.identifiers.append(data)

    def add_post(self, label, role, **kwargs):
        post = {"label": label, "role": role}
        for k, v in kwargs.items():
            if k not in self._post_slots:
                raise AttributeError(
                    '{0} not a valid kwarg for add_post'.format(k))
            post[k] = v
        self.posts.append(post)

    def add_contact_detail(self, type, value, note):
        self.contact_details.append({"type": type,
                                     "value": value,
                                     "note": note})
