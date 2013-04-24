from larvae.base import LarvaeBase


class Person(LarvaeBase):
    """
    Details for a Person in Popolo format.
    """

    _schema_name = "person"

    __slots__ = ('name', '_id', 'gender', 'birth_date',
                 'death_date', 'image', 'summary', 'biography', 'links',
                 'other_names', 'extras', 'contact_details')
    _other_name_slots = ('name', 'start_date', 'end_date', 'note')

    def __init__(self, name, **kwargs):
        super(Person, self).__init__()
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.links = []
        self.other_names = []
        self.extras = {}

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
