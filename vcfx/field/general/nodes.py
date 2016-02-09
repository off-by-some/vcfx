from vcfx.field.nodes import Field

class Begin(Field):
    KEY = "BEGIN"
    def __init__(self, *a, **kw):
        super(Begin, self).__init__(*a, **kw)

class End(Field):
    KEY = "END"
    def __init__(self, *a, **kw):
        super(End, self).__init__(*a, **kw)

class Source(Field):
    KEY = "SOURCE"
    SCALAR = True
    def __init__(self, *a, **kw):
        super(Source, self).__init__(*a, **kw)

class Kind(Field):
    KEY = "KIND"
    def __init__(self, *a, **kw):
        super(Kind, self).__init__(*a, **kw)

class XML(Field):
    KEY = "XML"
    def __init__(self, *a, **kw):
        super(XML, self).__init__(*a, **kw)
