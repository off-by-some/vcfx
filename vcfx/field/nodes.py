from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
import uuid

standard_library.install_aliases()

from pydash.collections import pluck

class Field(object):
    KEY = None

    # Can there be many of us?
    SCALAR = False

    # We need to keep track of an ID if we want to use equality operators
    ID = str(uuid.uuid4())


    def __init__(self, rawvalue=None, attrs=[], lineno=0, label="", subkey=None):
        self.preferred = False
        self.types = pluck(attrs, "type")
        self.attrs = attrs
        self.value = rawvalue
        self.lineno = lineno
        self.label = label

        # Append our line number for a unique ID
        self.ID += str(lineno)

        # We are formatting for the user to see
        self._pretty = False

        self.process_attrs(attrs)

        if rawvalue is not None:
            self._pretty = True
            self.value = self.clean_value(rawvalue)

        # IOS adds their own format for custom fields in the form of
        # <subkey>.<key>, i.e item6.ADR
        self.subkey = subkey

        # The user has determined this as the preferred item out of a list
        if "pref" in self.types:
            self.preferred = True

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.ID == other.ID

    def __hash__(self):
        return hash(str(self.ID))

    def __ne__(self, other):
        return not self.__eq__(other)

    def clean_value(self, rawvalue):
        if type(rawvalue) is str:
            # Any and all strings should end in a CRLF
            return rawvalue.strip("\r\n")
        else:
            return rawvalue

    def process_attrs(self, val):
        return val

    def validate_value(self, val):
        return True

    def __repr__(self):
        className = self.__class__.__name__
        data = (className, self.subkey, self.KEY, self.lineno)
        return '<%s subkey="%s" key="%s" lineno="%s" />' % data


class Unknown(Field):
    KEY = "FOLDED"
    SCALAR = True
    def __init__(self, *a, **kw):
        super(Unknown, self).__init__(*a, **kw)
