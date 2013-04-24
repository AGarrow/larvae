from larvae.base import LarvaeBase
import uuid


class Organization(LarvaeBase):
    """
    A single popolo encoded Organization
    """

    __slots__ = ('classification', 'dissolution_date', 'founding_date',
                 '_id', 'identifiers', 'name', 'other_names', 'parent_id',
                 'posts', 'openstates_id', 'contact_details', 'geography_id')

    _post_slots = ('end_date', 'id', 'label', 'organization_id', 'role',
                   'start_date', 'chamber', 'district', 'geography_id')

    _type = _schema_name = "organization"

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

    def add_post(self, label, role, **kwargs):
        post = {"id": str(uuid.uuid1()), "label": label, "role": role}
        for k, v in kwargs.items():
            if k not in self._post_slots:
                raise AttributeError(
                    '{0} not a valid kwarg for add_post'.format(k))
            post[k] = v
        self.posts.append(post)
