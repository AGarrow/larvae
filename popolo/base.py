import validictory
import json
import os


class PopoloBase(dict):
    """
    This is the base class for all the Popolo objects. This contains
    commom methods and abstractions for popolo objects.

    All popolo objects subclass the native `dict bits.
    """

    _schema_name = None  # to be overridden by children. Something like
    #             "person" or "organizations". Used in :func:`validate`.

    def _validate(self):
        """
        Implementation-local validation method.
        """
        pass

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
        self._validate()
        curpath = os.path.dirname(os.path.abspath(__file__))
        schema = json.load(open(os.path.join(
            curpath, "schemas", "%s.json" % (self._schema_name)), 'r'))
        validictory.validate(self, schema, required_by_default=False)
