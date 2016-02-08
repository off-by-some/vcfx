from pydash.collections import filter_ as ifilter, pluck

class Field(object):
    KEY = None

    def __init__(self, rawvalue=None, attrs=[], lineno=0, label="", subkey=None):
        self.preferred = False
        self.types = pluck(attrs, "type")
        self.value = rawvalue
        self.lineno = lineno
        self.label = label

        if rawvalue is not None:
            self.value = self.clean_value(rawvalue)

        # IOS adds their own format for custom fields in the form of
        # <subkey>.<key>, i.e item6.ADR
        self.subkey = subkey

        # The user has determined this as the preferred item out of a list
        if "pref" in self.types:
            self.preferred = True

    def clean_value(self, rawvalue):
        return rawvalue

    def __repr__(self):
        className = self.__class__.__name__
        data = (className, self.subkey, self.KEY, self.lineno)
        return '<%s subkey="%s" key="%s" lineno="%s" />' % data


class Unknown(Field):
    KEY = None
    def __init__(self, *a, **kw):
        super(Unknown, self).__init__(*a, **kw)

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
    """
       Special note:  The structured property value corresponds, in
          sequence, to the Family Names (also known as surnames), Given
          Names, Additional Names, Honorific Prefixes, and Honorific
          Suffixes.  The text components are separated by the SEMICOLON
          character (U+003B).  Individual text components can include
          multiple text values separated by the COMMA character (U+002C).
          This property is based on the semantics of the X.520 individual
          name attributes [CCITT.X520.1988].  The property SHOULD be present
          in the vCard object when the name of the object the vCard
          represents follows the X.520 model.

          The SORT-AS parameter MAY be applied to this property.

       ABNF:

         N-param = "VALUE=text" / sort-as-param / language-param
                 / altid-param / any-param
         N-value = list-component 4(";" list-component)

       Examples:

                 N:Public;John;Quinlan;Mr.;Esq.

                 N:Stevenson;John;Philip,Paul;Dr.;Jr.,M.D.,A.C.P.
    """

    KEY = "N"

    def __init__(self, *a, **kw):
        super(Name, self).__init__(*a, **kw)

    def clean_value(self, v):
        vals = v.strip("\r\n").split(";")
        if len(vals) is not 5:
            raise ValueError("Value format for Name is incorrect")

        self.last = vals[0]
        self.first = vals[1]
        self.additional = ifilter(vals[2].split(","), bool)
        self.suffixes = ifilter(vals[3].split(","), bool)
        self.prefixes = ifilter(vals[4].split(","), bool)


class FullName(Field):
    """
       Special notes:  This property is based on the semantics of the X.520
          Common Name attribute [CCITT.X520.1988].  The property MUST be
          present in the vCard object.

       ABNF:

         FN-param = "VALUE=text" / type-param / language-param / altid-param
                  / pid-param / pref-param / any-param
         FN-value = text

       Example:

             FN:Mr. John Q. Public\, Esq.
    """

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

class Gender(Field):
    KEY = "GENDER"
    def __init__(self, *a, **kw):
        super(Gender, self).__init__(*a, **kw)

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
