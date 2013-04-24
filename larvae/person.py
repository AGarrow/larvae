from larvae.base import LarvaeBase
from larvae.organization import Organization
from larvae.membership import Membership

_str_types = (str, unicode)


class Person(LarvaeBase):
    """
    Details for a Person in Popolo format.
    """

    _type = _schema_name = "person"

    __slots__ = ('name', '_id', 'gender', 'birth_date',
                 'death_date', 'image', 'summary', 'biography', 'links',
                 'other_names', 'extras', 'contact_details', 'openstates_id',
                 'chamber', 'district')
    _other_name_slots = ('name', 'start_date', 'end_date', 'note')

    def __init__(self, name, **kwargs):
        super(Person, self).__init__()
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.links = []
        self.other_names = []
        self.extras = {}
        self._related = []

    def add_name(self, name, **kwargs):
        other_name = {'name': name}
        for k, v in kwargs.items():
            if k not in self._other_name_slots:
                raise AttributeError('{0} not a valid kwarg for add_name'
                                     .format(k))
            other_name[k] = v
        self.other_names.append(other_name)

    def add_link(self, url, note):
        self.links.append({"note": note, "url": url})

    def add_membership(self, organization, **kwargs):
        """
            add a membership in an organization and return the membership
            object in case there are more details to add
        """
        if isinstance(organization, _str_types):
            organization = Organization(organization)
            self._related.append(organization)
        membership = Membership(self.uuid, organization.uuid, **kwargs)
        self._related.append(membership)
        return membership

    def __unicode__(self):
        return self.name
    __str__ = __unicode__
