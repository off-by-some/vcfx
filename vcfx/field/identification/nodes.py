from vcfx.field.nodes import Field
from pydash.collections import filter_ as ifilter

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


class Nickname(Field):
    KEY = "NICKNAME"
    def __init__(self, *a, **kw):
        super(Nickname, self).__init__(*a, **kw)

class Photo(Field):
    KEY = "PHOTO"
    def __init__(self, *a, **kw):
        self.b64 = None
        super(Photo, self).__init__(*a, **kw)

class Birthday(Field):
    KEY = "BDAY"
    def __init__(self, *a, **kw):
        super(Birthday, self).__init__(*a, **kw)

class Anniversary(Field):
    KEY = "ANNIVERSARY"
    def __init__(self, *a, **kw):
        super(Anniversary, self).__init__(*a, **kw)

class Gender(Field):
    KEY = "GENDER"
    def __init__(self, *a, **kw):
        super(Gender, self).__init__(*a, **kw)
