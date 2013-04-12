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

    def validate(self):
        """
        Validate that the Popolo object is a valid object. This uses
        `self._schema_name` to load the schema, and validate `self` against
        it.

        On error, this will raise a `validictory.ValidationError`.
        """
        curpath = os.path.dirname(os.path.abspath(__file__))
        schema = json.load(open(os.path.join(
            curpath, "schemas", "%s.json" % (self._schema_name)), 'r'))
        validictory.validate(self, schema, required_by_default=False)
