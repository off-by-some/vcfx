from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()
from vcfx.field.nodes import Field

#######
# TODO(cassidy): Figure out what `CALADRURI` actually is and implement support
#######

class BusyTime(Field):
    KEY = "FBURL"
    def __init__(self, *a, **kw):
        super(BusyTime, self).__init__(*a, **kw)
