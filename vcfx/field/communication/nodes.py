from vcfx.field.nodes import Field

class Telephone(Field):
    KEY = "TEL"
    SCALAR = True

    def __init__(self, *a, **kw):
        super(Telephone, self).__init__(*a, **kw)

class Email(Field):
    KEY = "EMAIL"
    SCALAR = True

    def __init__(self, *a, **kw):
        super(Email, self).__init__(*a, **kw)

class IMPP(Field):
    KEY = "IMPP"
    SCALAR = True

    def __init__(self, *a, **kw):
        super(IMPP, self).__init__(*a, **kw)

class Language(Field):
    KEY = "LANG"
    SCALAR = True
    def __init__(self, *a, **kw):
        super(Language, self).__init__(*a, **kw)
