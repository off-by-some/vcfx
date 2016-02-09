from vcfx.field.nodes import Field

#######
# TODO(cassidy): Figure out what `CALADRURI` actually is and implement support
#######

class BusyTime(Field):
    KEY = "FBURL"
    def __init__(self, *a, **kw):
        super(BusyTime, self).__init__(*a, **kw)
