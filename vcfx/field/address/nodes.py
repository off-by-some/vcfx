from vcfx.field.nodes import Field

class Address(Field):
    KEY = "ADR"
    SCALAR = True
    def __init__(self, *a, **kw):
        super(Address, self).__init__(*a, **kw)
