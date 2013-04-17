from popolo.base import PopoloBase


class Person(PopoloBase):
    """
    Details for a Person in Popolo format.
    """

    _schema_name = "person"

    __slots__ = ('name', 'id', 'gender', 'birth_date', 'death_date', 'image',
                 'summary', 'biography', 'links', 'other_names', 'extras')
    _other_name_slots = ('name', 'start_date', 'end_date', 'note')

    def __init__(self, name, **kwargs):
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

    def add_link(self, note, url):
        self.links.append({"note": note, "url": url})
