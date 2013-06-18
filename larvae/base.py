import uuid
from larvae.utils import DatetimeValidator


class LarvaeBase(object):
    """
    This is the base class for all the Open Civic objects. This contains
    common methods and abstractions for OCD objects.
    """

    # needs slots defined so children __slots__ are enforced
    __slots__ = ('_id', 'sources', '_related', 'jurisdiction')

    # to be overridden by children. Something like "person" or "organization".
    # Used in :func:`validate`.
    _type = None
    _schema = None

    def __init__(self):
        self._id = str(uuid.uuid1())
        self.sources = []

    def validate(self):
        """
        Validate that we have a valid object.

        On error, this will either raise a `ValueError` or a
        `validictory.ValidationError` (a subclass of `ValueError`).

        This also expects that the schemas assume that omitting required
        in the schema asserts the field is optional, not required. This is
        due to upstream schemas being in JSON Schema v3, and not validictory's
        modified syntax.
        """
        validator = DatetimeValidator(required_by_default=False)
        validator.validate(self.as_dict(), self._schema)

    def as_dict(self):
        d = {}
        all_slots = set(self.__slots__)
        for cls in self.__class__.__mro__:
            all_slots |= set(cls.__slots__)
            if cls == LarvaeBase:
                break
        for attr in all_slots:
            if attr != '_related' and hasattr(self, attr):
                d[attr] = getattr(self, attr)
        d['_type'] = self._type
        return d

    def add_source(self, url, note=None):
        """ Add a source URL from which data was collected """
        self.sources.append({'url': url, 'note': note})
