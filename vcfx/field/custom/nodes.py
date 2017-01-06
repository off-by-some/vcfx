from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()
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
