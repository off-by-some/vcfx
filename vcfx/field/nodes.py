from pydash.collections import pluck

class Field(object):
    KEY = None

    # Can there be many of us?
    SCALAR = False

    def __init__(self, rawvalue=None, attrs=[], lineno=0, label="", subkey=None):
        self.preferred = False
        self.types = pluck(attrs, "type")
        self.value = rawvalue
        self.lineno = lineno
        self.label = label

        # We are formatting for the user to see
        self._pretty = False

        if rawvalue is not None:
            self._pretty = True
            self.value = self.clean_value(rawvalue)

        # IOS adds their own format for custom fields in the form of
        # <subkey>.<key>, i.e item6.ADR
        self.subkey = subkey

        # The user has determined this as the preferred item out of a list
        if "pref" in self.types:
            self.preferred = True

    def clean_value(self, rawvalue):
        if type(rawvalue) is str:
            # Any and all strings should end in a CRLF
            return rawvalue.strip("\r\n")
        else:
            return rawvalue

    def __repr__(self):
        className = self.__class__.__name__
        data = (className, self.subkey, self.KEY, self.lineno)
        return '<%s subkey="%s" key="%s" lineno="%s" />' % data


class Unknown(Field):
    KEY = "FOLDED"
    SCALAR = True
    def __init__(self, *a, **kw):
        super(Unknown, self).__init__(*a, **kw)
