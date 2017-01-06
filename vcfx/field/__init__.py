from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import filter
from future import standard_library

standard_library.install_aliases()

from vcfx import util
from vcfx.field.nodes import Unknown

M_NAMES = [
    "address", "calendar", "communication",
    "custom", "explanatory", "general",
    "geographical", "identification",
    "organizational", "security"
]

modules = util.get_modules(M_NAMES, __path__, __name__)

all_nodes = []
for m in modules:
    all_nodes += util.filter_defined_cls(m)

all_nodes.append(Unknown)

def get_field_by_key(key=None):
    found = list(filter(lambda x: x.KEY == key, all_nodes))

    if len(found) == 0:
        return Unknown

    return found[0]


__all__ = [
    "all_nodes",
    "get_field_by_key",
]
