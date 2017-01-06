from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library

standard_library.install_aliases()

from vcfx.field.nodes import Field

class Key(Field):
    KEY = "KEY"
    def __init__(self, *a, **kw):
        super(Key, self).__init__(*a, **kw)
