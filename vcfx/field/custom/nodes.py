from vcfx.field.nodes import Field

class IOSLabel(Field):
    """Custom labels for ios"""

    KEY = "X-ABLabel"
    SCALAR = True

    def __init__(self, *a, **kw):
        super(IOSLabel, self).__init__(*a, **kw)

class AlternateBirthday(Field):
    KEY = "X-ALTBDAY"
    def __init__(self, *a, **kw):
        super(AlternateBirthday, self).__init__(*a, **kw)
