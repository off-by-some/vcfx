from pydash.collections import filter_ as ifilter, pluck

class Field(object):
    KEY = None

    def __init__(self, value="", attrs=[], lineno=0, subkey=None):
        self.preferred = False
        self.types = pluck(attrs, "type")
        self.value = value
        self.lineno = lineno

        # IOS adds their own format for custom fields in the form of
        # <subkey>.<key>, i.e item6.ADR
        self.subkey = None

        # The user has determined this as the preferred item out of a list
        if "pref" in self.types:
            self.preferred = True


class Unknown:
    KEY = None
    def __init__(self, value="", line=0, lineno=0):
        self.line = line
        self.lineno = lineno

class Begin(Field):
    KEY = "BEGIN"
    def __init__(self, *a, **kw):
        super(Begin, self).__init__(*a, **kw)

class Version(Field):
    KEY = "VERSION"
    def __init__(self, *a, **kw):
        super(Version, self).__init__(*a, **kw)

class Prodid(Field):
    KEY = "PRODID"
    def __init__(self, *a, **kw):
        super(Prodid, self).__init__(*a, **kw)

class Name(Field):
    KEY = "N"
    def __init__(self, *a, **kw):
        super(Name, self).__init__(*a, **kw)

class FullName(Field):
    KEY = "FN"
    def __init__(self, *a, **kw):
        super(FullName, self).__init__(*a, **kw)

class Organization(Field):
    KEY = "ORG"
    def __init__(self, *a, **kw):
        super(Organization, self).__init__(*a, **kw)

class Email(Field):
    KEY = "EMAIL"
    def __init__(self, *a, **kw):
        super(Email, self).__init__(*a, **kw)

class Photo(Field):
    KEY = "PHOTO"
    def __init__(self, *a, **kw):
        super(Photo, self).__init__(*a, **kw)

class Telephone(Field):
    KEY = "TEL"
    def __init__(self, *a, **kw):
        super(Telephone, self).__init__(*a, **kw)

class Address(Field):
    KEY = "ADR"
    def __init__(self, *a, **kw):
        super(Address, self).__init__(*a, **kw)

class IOSLabel(Field):
    """Custom labels for ios"""

    KEY = "X-ABLabel"
    def __init__(self, *a, **kw):
        super(IOSLabel, self).__init__(*a, **kw)

class Url(Field):
    KEY = "URL"
    def __init__(self, *a, **kw):
        super(Url, self).__init__(*a, **kw)

class Birthday(Field):
    KEY = "BDAY"
    def __init__(self, *a, **kw):
        super(Birthday, self).__init__(*a, **kw)

class AlternateBirthday(Field):
    KEY = "X-ALTBDAY"
    def __init__(self, *a, **kw):
        super(AlternateBirthday, self).__init__(*a, **kw)

class End(Field):
    KEY = "END"
    def __init__(self, *a, **kw):
        super(End, self).__init__(*a, **kw)

ALL = [
    Begin, Prodid, Version, Name, FullName, Organization, Email,
    Telephone, Address, IOSLabel, Url, Birthday,
    AlternateBirthday, Photo, End
]

def getField(fieldKey=None):
    if fieldKey == None:
        return Unknown

    found = ifilter(ALL, lambda x: x.KEY == fieldKey)

    if len(found) == 0:
        return Unknown

    return found[0]
