# vcfx
A Python 3 Vcard parser

### Usage:
```python
from vcfx import reader

vcard = reader("/home/rum/Programming/vcfx/fixtures/reggie-smalls-ios-v3.0.vcf")

# All field functions with plural names return generators
phones = vcard.phones()
# Out[1]:
# [<Telephone subkey="None" key="TEL" lineno="13" />,
#  <Telephone subkey="None" key="TEL" lineno="14" />,
#  ...,
#  <Telephone subkey="item7" key="TEL" lineno="24" />]

# While the latter return singular items
vcard.fullname().value
# Out[2]: 'Reginald Smalls'

vcard.name().first
# Out[3]: 'Reginald'

phones[0].can_sms
# Out[4]: False

# You also may iterate over the vcard directly, one line at a time
for field in vcard:
  print(field)
# <Begin subkey="None" key="BEGIN" lineno="0" />
# <Version subkey="None" key="VERSION" lineno="1" />
# <Prodid subkey="None" key="PRODID" lineno="2" />
# <Name subkey="None" key="N" lineno="3" />
# ...
```

### Todo:
There are still some things left to do:
  - [%75] Expose getters for all fields (You can still get every field via iteration)
  - [%55] Complete value parsing and assignment per spec RFC 6350, However grabbing the unparsed value with `<FieldName>.value` is possible.
  - [%40] Documentation of all available field APIs (I strongly encourage you to read through `vcfx.fields` if you are looking)
  - [%25] Complete attribute parsing of fields and assignment to human-readable names
  - Testing
  - [%90] Fold support, Currently if a field comes along thats longer than 80 characters, we die
  - Vcard 2.1 support (Really just need to write a `parseline2` function similar to `parseline3` in `tokenizer.js`)
  - Rip the `_vAST` logic out of the file reader in `tokenizer.py` and put it in its own class
  - [%70] Optimize position reader
  - [%5] Full X-attribute parsing
  - URL support for photos
  - Identification of `Unknown` rows & flattening of the `vAST` when iterating over the reader
  - Vcard construction
  - [%10] Vcard validation
  - In-place Vcard modification
  - Fetching and storing photos
  - Fetching and rewriting photos under various formats
  - "Safe Mode", aka stripping out fields + values that may break interoperability 

### Properties available on fields:

#### Common Properties
There are a couple of attributes that all fields share:
- `attrs :: [dict(str)]`    -- list of all the attributes associated with the node
- `label :: str`            -- A custom label associated with the field
- `preferred :: str`        -- Whether the item is the preferred item out of it's superset
- `subkey :: str`           -- The subkey of the item (used in IOS)
- `types :: [str]`          -- Any `type=` attributes found with the field (i.e `type=HOME`)
- `value :: str`            -- The full value of the field, used for fields that define a single value (i.e `FullName().value`)


#### General Properties:
##### `Begin`

- `value :: str`       -- Should _always_ be "VCARD"

##### `End`

- `value :: str`       -- Should _always_ be "VCARD"

##### `Source`

- `value :: str`       -- A URI (defined in [RFC3986]) to a directory service where an application may pull more information from   

##### `Kind`

- `value :: str`        -- Must be one of `["individual", "group", "org", "location"]`

##### `XML`

- `value :: str`        -- a single XML 1.0 element

#### Identification Properties:
##### `FullName`
- `value :: str`        -- The full name of the contact

##### `Name`:
- `first :: str`        -- First name (Given name)
- `last :: str`         -- Last name (Surname)
- `additional :: [str]` -- Additional names for the contact
- `suffixes :: [str]`   -- Formal suffixes
- `prefixes :: [str]`   -- Formal prefixes

##### `Nicknames`

- `value :: [str]`        -- Nicknames of the contact

##### `Photo`
- `b64 :: str`          -- Base64 representation of the contact's photo

##### `Birthday`

- `value :: str`

##### `Anniversary`

- `value :: str`

##### `Gender`

- `value :: str`        -- A single letter.  M stands for "male", F stands for "female", O stands for "other", N stands for "none or not applicable", U stands for "unknown".

##### `Photo`
- `b64 :: str`          -- Base64 representation of the contact's photo


#### Address Properties:
##### `Address`

- `po_box :: str`      -- The post office box
- `extended_address :: str` -- The extended address (e.g line2, Apt #, Ste #) of the contact
- `locality :: str`    -- The locality of the contact (e.g "city")
- `region   :: str`    -- e.g state, province
- `postal_code :: str` -- The postal code (or zip code) of the contact
- `country :: str`     -- Full name of the country

#### Communication Properties:
##### `Telephone`

- `value :: string`    -- A single text value containing a phone number
- `can_sms :: bool`
- `can_call :: bool`
- `can_fax :: bool`
- `can_video_conference :: bool`
- `is_TTY :: bool`

#### `Email`

- `value :: str`

#### `IMPP`

- `value :: str` -- URI for instant messaging and presence protocol communications

#### `Language`

- `value :: str` -- eg. fr, en, de
