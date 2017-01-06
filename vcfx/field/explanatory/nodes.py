from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()
from vcfx.field.nodes import Field

class Categories(Field):
    KEY = "CATEGORIES"
    def __init__(self, *a, **kw):
        super(Categories, self).__init__(*a, **kw)

    def clean_values(self, v):
        self.value = v.strip("\r\n").split(",")

class Note(Field):
    KEY = "NOTE"
    def __init__(self, *a, **kw):
        super(Note, self).__init__(*a, **kw)

class Prodid(Field):
    KEY = "PRODID"
    def __init__(self, *a, **kw):
        super(Prodid, self).__init__(*a, **kw)

class Revision(Field):
    KEY = "REV"
    def __init__(self, *a, **kw):
        super(Revision, self).__init__(*a, **kw)

class Sound(Field):
    KEY = "SOUND"
    def __init__(self, *a, **kw):
        super(Sound, self).__init__(*a, **kw)

class UID(Field):
    KEY = "UID"
    def __init__(self, *a, **kw):
        super(UID, self).__init__(*a, **kw)

class ClientPIDMap(Field):
    KEY = "CLIENTPIDMAP"
    def __init__(self, *a, **kw):
        super(ClientPIDMap, self).__init__(*a, **kw)

class Url(Field):
    KEY = "URL"
    SCALAR = True
    def __init__(self, *a, **kw):
        super(Url, self).__init__(*a, **kw)

class Version(Field):
    KEY = "VERSION"
    def __init__(self, *a, **kw):
        super(Version, self).__init__(*a, **kw)
