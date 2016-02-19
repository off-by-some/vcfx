from vcfx.field.nodes import Field

class Organization(Field):
    KEY = "ORG"
    def __init__(self, *a, **kw):
        super(Organization, self).__init__(*a, **kw)
        self.name = None
        # https://en.wikipedia.org/wiki/Organizational_unit_(computing)
        self.org_unit1 = None;
        self.org_unit2 = None;

    def clean_value(self, val=""):
        segs = val.split(";")
        self.name = segs[0]
        self.org_unit1 = segs[1]
        self.org_unit2 = segs[2]

class Title(Field):
    KEY = "TITLE"
    def __init__(self, *a, **kw):
        super(Title, self).__init__(*a, **kw)

class Role(Field):
    KEY = "ROLE"
    def __init__(self, *a, **kw):
        super(Role, self).__init__(*a, **kw)

# TODO(cassidy): Though not common, this is another type of photo to support
class Logo(Field):
    KEY = "LOGO"
    def __init__(self, *a, **kw):
        super(Logo, self).__init__(*a, **kw)

class Member(Field):
    KEY = "MEMBER"
    def __init__(self, *a, **kw):
        super(Member, self).__init__(*a, **kw)

class Related(Field):
    KEY = "RELATED"
    def __init__(self, *a, **kw):
        super(Related, self).__init__(*a, **kw)
