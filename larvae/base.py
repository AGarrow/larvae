import os
import json
import uuid
from collections import defaultdict
import validictory


class LarvaeBase(object):
    """
    This is the base class for all the Open Civic objects. This contains
    common methods and abstractions for OCD objects.
    """

    # needs slots defined so children __slots__ are enforced
    __slots__ = ('uuid', 'sources', '_related', '_type')

    # to be overridden by children. Something like "person" or "organization".
    # Used in :func:`validate`.
    _schema_name = None
    _schema_cache = defaultdict(lambda: None)

    def __init__(self):
        self.uuid = str(uuid.uuid1())
        self.sources = []
        self._type = None
        self._type = self._schema_name

    def validate(self):
        """
        Validate that the Popolo object is a valid object. This uses
        `self._schema_name` to load the schema, and validate `self` against
        it.

        On error, this will either raise a `ValueError` or a
        `validictory.ValidationError` (a subclass of `ValueError`).

        This also expects that the schemas assume that omitting required
        in the schema asserts the field is optional, not required. This is
        due to upstream schemas being in JSON Schema v3, and not validictory's
        modified syntax.
        """
        schema = LarvaeBase._schema_cache[self._schema_name]
        if schema is None:
            curpath = os.path.dirname(os.path.abspath(__file__))
            schema = json.load(open(os.path.join(
                curpath, "schemas", "%s.json" % (self._schema_name)), 'r'))
            LarvaeBase._schema_cache[self._schema_name] = schema
        validictory.validate(self.as_dict(), schema, required_by_default=False)

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
        return d

    def add_source(self, url, note=None):
        """ Add a source URL from which data was collected """
        self.sources.append({'url': url, 'note': note})
