from vcfx.field.nodes import Field

class Telephone(Field):
    KEY = "TEL"
    SCALAR = True

    def __init__(self, *a, **kw):
        super(Telephone, self).__init__(*a, **kw)
        self.can_sms = False
        self.can_call = False
        self.can_fax = False
        self.can_video_conference = False
        self.is_TTY = False

    def process_attrs(self, attrs):
        if "text" in attrs:
            self.can_sms = True
        if "voice" in attrs:
            self.can_call = True
        if "fax" in attrs:
            self.can_fax = True
        if "video" in attrs:
            self.can_video_conference = True
        if "pager" in attrs:
            self.is_pager = True
        if "textphone" in attrs: # Deaf people don't even use these anymore
             self.is_TTY = True

class Email(Field):
    KEY = "EMAIL"
    SCALAR = True

    def __init__(self, *a, **kw):
        super(Email, self).__init__(*a, **kw)

class IMPP(Field):
    KEY = "IMPP"
    SCALAR = True

    def __init__(self, *a, **kw):
        super(IMPP, self).__init__(*a, **kw)

class Language(Field):
    KEY = "LANG"
    SCALAR = True
    def __init__(self, *a, **kw):
        super(Language, self).__init__(*a, **kw)
