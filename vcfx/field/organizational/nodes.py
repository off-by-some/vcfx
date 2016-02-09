from vcfx.field.nodes import Field

class Organization(Field):
    KEY = "ORG"
    def __init__(self, *a, **kw):
        super(Organization, self).__init__(*a, **kw)

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
