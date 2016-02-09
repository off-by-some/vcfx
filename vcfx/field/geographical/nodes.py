from vcfx.field.nodes import Field

class TimeZone(Field):
    KEY = "TZ"
    def __init__(self, *a, **kw):
        super(TimeZone, self).__init__(*a, **kw)

class GlobalPosition(Field):
    KEY = "GEO"
    def __init__(self, *a, **kw):
        super(GlobalPosition, self).__init__(*a, **kw)
