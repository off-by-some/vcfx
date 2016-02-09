from vcfx.field.nodes import Field

class Key(Field):
    KEY = "KEY"
    def __init__(self, *a, **kw):
        super(Key, self).__init__(*a, **kw)
