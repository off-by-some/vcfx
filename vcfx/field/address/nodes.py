from vcfx.field.nodes import Field

class Address(Field):
    KEY = "ADR"
    SCALAR = True
    def __init__(self, *a, **kw):
        super(Address, self).__init__(*a, **kw)

        self.po_box = None
        self.extended_address = None
        self.street_address = None
        self.locality = None
        self.region = None
        self.postal_code = None
        self.country = None

    def clean_value(self, val=""):
        segs = val.strip("\r\n").split(";")

        (
            self.po_box, self.extended_address, self.street_address,
            self.locality, self.region, self.postal_code,
            self.country
        ) = segs
