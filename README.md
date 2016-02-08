# vcfx
A Python 3 Vcard parser

### Todo:
There are still some things left to do:
  - Proper value parsing and assignment on all fields per spec (you may still grab the unparsed value if there is one with `Field.value`)
  - Vcard 2.1 support (Really just need to write a `parseline2` function similar to `parseline3` in parser.js)
  - Custom fields for android
  - URL support for photos
  - Identification of `Unknown` rows & flattening of the `vAST` when iterating over the reader
  - vcard construction

### Usage:
```python
from vcfx import reader

vcard = reader("/home/rum/Programming/vcfx/fixtures/reggie-smalls-ios-v3.0.vcf")

# All attribute functions with plural names return generators
list(vcard.addresses())
# Out[1]:
# [ <Address subkey="item8" key="ADR" lineno="26"  />,
#   <Address subkey="item9" key="ADR" lineno="27"  />,
#   <Address subkey="item10" key="ADR" lineno="28" />,
#   <Address subkey="item11" key="ADR" lineno="29" /> ]

# While the latter return singular items
vcard.fullname().value
# Out[2]: 'Reginald Smalls'

vcard.name().first
#Out[3]: 'Reginald'

# You also may iterate over the vcard directly, one line at a time
for field in vcard:
  print(field)
# <Begin subkey="None" key="BEGIN" lineno="0" />
# <Version subkey="None" key="VERSION" lineno="1" />
# <Prodid subkey="None" key="PRODID" lineno="2" />
# <Name subkey="None" key="N" lineno="3" />
# ...
```

### Supported Fields and Properties Available

#### Name:
- `first :: str`        -- First name (Given name)
- `last :: str`         -- Last name (Surname)
- `additional :: [str]` -- Additional names for the contact
- `suffixes :: [str]`   -- Formal suffixes
- `prefixes :: [str]`   -- Formal prefixes

#### FullName
- `value :: str`        -- The full name of the contact

#### Photo
- `b64 :: str`          -- Base64 representation of the contact's photo
