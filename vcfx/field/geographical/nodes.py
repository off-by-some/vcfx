from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()
from vcfx.field.nodes import Field

class TimeZone(Field):
    KEY = "TZ"
    def __init__(self, *a, **kw):
        super(TimeZone, self).__init__(*a, **kw)

class GlobalPosition(Field):
    KEY = "GEO"
    def __init__(self, *a, **kw):
        super(GlobalPosition, self).__init__(*a, **kw)
