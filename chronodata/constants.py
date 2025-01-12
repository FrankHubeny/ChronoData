# chronodata/constants.py
# Licensed under a 3-clause BSD style license - see LICENSE.md
# chronodata/enums.py
# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Enumeration classes to build a dataset formatted according
to the GEDCOM standard.

Some of these enumerations came from the GEDCOM specifications.
Others were added to aid in setting up the NamedTuples for the
users to fill with data.

All of them have a `NONE` element as a default for an empty string value.
This NONE value is not part of the GEDCOM standard and does not
appear in the output.

References:
    - [Date Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
    - [Python Enum Support](https://docs.python.org/3/library/enum.html#)
    - [PEP 435](https://peps.python.org/pep-0435/)
    - [RealPython Tutorial](https://realpython.com/python-enum/)
"""

__all__ = [
    'Adop',
    'ApproxDate',
    'EvenAttr',
    'Event',
    'FamAttr',
    'FamEven',
    'FamcStat',
    'Id',
    'IndiAttr',
    'IndiEven',
    'MediaType',
    'Medium',
    'NameType',
    'Pedi',
    'Quay',
    'RangeDate',
    'Record',
    'Resn',
    'RestrictDate',
    'Role',
    'Sex',
    'Stat',
    'Tag',
]

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Literal

# class AgeConstants:
#     """Age enumerations for the Age NamedTuple."""

#     UNIT: ClassVar = {
#         'y': 'y',
#         'year': 'y',
#         'm': 'month',
#         'month': 'm',
#         'd': 'd',
#         'day': 'd',
#         'w': 'w',
#         'week': 'w',
#     }
#     BOUND: ClassVar = {'<', '>'}
#     NAME: ClassVar = {'U'}


@dataclass(frozen=True)
class Value:
    """The following constants are dictionary values."""

    AD: str = ' AD'
    BC: str = ' BC'
    BCE: str = ' BCE'
    BEFORE_PRESENT: str = 'BEFORE PRESENT'
    BP: str = ' BP'
    CE: str = ' CE'
    DATETIME_EPOCH: int = 1970
    #EMPTY: str = ''
    EPOCH: str = 'Epoch'
    EXPERIMENT: str = 'EXPERIMENT'
    GREGORIAN: str = 'GREGORIAN'
    ISO: str = 'ISO'
    MAX_MONTHS: str = 'Max Months'
    MONTH_NAMES: str = 'Month Names'
    MONTH_MAX_DAYS: str = 'Month Max Days'
    SECULAR: str = 'SECULAR'


class Cal:
    """GEDCOM codes for various calendars."""

    CALENDARS: ClassVar = {
        Value.GREGORIAN: {
            Value.MAX_MONTHS: 12,
            Value.MONTH_NAMES: {
                '01': 'JAN',
                '02': 'FEB',
                '03': 'MAR',
                '04': 'APR',
                '05': 'MAY',
                '06': 'JUN',
                '07': 'JUL',
                '08': 'AUG',
                '09': 'SEP',
                '10': 'OCT',
                '11': 'NOV',
                '12': 'DEC',
            },
            Value.ISO: {
                'JAN': '01',
                'FEB': '02',
                'MAR': '03',
                'APR': '04',
                'MAY': '05',
                'JUN': '06',
                'JUL': '07',
                'AUG': '08',
                'SEP': '09',
                'OCT': '10',
                'NOV': '11',
                'DEC': '12',
            },
            Value.MONTH_MAX_DAYS: {
                '01': 31,
                '02': 29,
                '03': 31,
                '04': 30,
                '05': 31,
                '06': 30,
                '07': 31,
                '08': 31,
                '09': 30,
                '10': 31,
                '11': 30,
                '12': 31,
            },
            Value.EPOCH: ' BCE',
        }
    }


@dataclass(frozen=True)
class Number:
    CSVLEN: int = 4
    GEDLEN: int = 4
    GRAMPSLEN: int = 7
    JSONLEN: int = 5


@dataclass(frozen=True)
class String:
    """The following values are part of the configuration of the GEDCOM standard
    or the Geography package.  They are not part of messages to the user
    and so do not require internationalization.
    """

    ATSIGN: str = '@'
    BANNED: str = r'[\u0000-\u001F\u007F\uD800-\uDFFF\uFFFE\uFFFF]'
    BC: str = 'BCE'
    COLON: str = ':'
    CSV: str = '.csv'
    DAY: str = 'd'
    DOUBLE_NEWLINE: str = '\n\n'
    EMPTY: str = ''
    #EVENT: str = 'EVENT'
    FORM_DEFAULT1: str = 'City'
    FORM_DEFAULT2: str = 'County'
    FORM_DEFAULT3: str = 'State'
    FORM_DEFAULT4: str = 'Country'
    FRENCH_R: str = 'FRENCH_R'
    GED: str = '.ged'
    GRAMPS: str = '.gramps'
    GREATER_THAN: str = '>'
    GREGORIAN: str = 'GREGORIAN'
    HEBREW: str = 'HEBREW'
    HYPHEN: str = '-'
    INDENT: str = '    '
    INDEX: str = 'index'
    INT: str = 'int'
    JSON: str = '.json'
    JULIAN: str = 'JULIAN'
    #LANG_URI: str = 'http://'
    MONTH: str = 'm'
    MONTH_NAMES: str = 'Month Names'
    NEGATIVE: str = '-'
    NEWLINE: str = '\n'
    NOW: str = 'now'
    OCCURRED: Literal['Y'] = 'Y'
    PLACE_FULL = 'F'
    PLACE_SHORT = 'S'
    PLACE_TRANSLATION = 'T'
    MAX = 'MAX'
    MIN = 'MIN'
    READ: str = 'r'
    SPACE: str = ' '
    T: str = 'T'
    UNDERLINE: str = '_'
    UNDETERMINED: str = 'und'
    VERSION: str = '7.0'
    Z: str = 'Z'


@dataclass(frozen=True)
class Unit:
    """The following constants define NumPy units used in datetime64 object."""

    ATTOSECOND: Literal['as'] = 'as'
    DAY: Literal['D'] = 'D'
    FEMTOSECOND: Literal['fs'] = 'fs'
    HOUR: Literal['h'] = 'h'
    MICROSECOND: Literal['us'] = 'us'
    MILLISECOND: Literal['ms'] = 'ms'
    MINUTE: Literal['m'] = 'm'
    MONTH: Literal['M'] = 'M'
    NANOSECOND: Literal['ns'] = 'ns'
    PICOSECOND: Literal['ps'] = 'ps'
    SECOND: Literal['s'] = 's'
    WEEK: Literal['W'] = 'W'
    YEAR: Literal['Y'] = 'Y'
    units: ClassVar = [
        ['Year', YEAR],
        ['Month', MONTH],
        ['Week', WEEK],
        ['Day', DAY],
        ['Hour', HOUR],
        ['Minute', MINUTE],
        ['Second', SECOND],
        ['Millisecond', MILLISECOND],
        ['Microsecond', MICROSECOND],
        ['Nanosecond', NANOSECOND],
        ['Femtosecond', FEMTOSECOND],
        ['Picosecond', PICOSECOND],
        ['Attosecond', ATTOSECOND],
    ]


class Adop(Enum):
    """Tags for who made the adoption of the person into the family.

    Reference:
        - [GEDCOM Adop Enumeration](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumset-ADOP)
    """

    HUSB = 'HUSB'
    WIFE = 'WIFE'
    BOTH = 'BOTH'
    NONE = String.EMPTY


class ApproxDate(Enum):
    """Enumeration values for date approximations.

    Reference:
        - [Date](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
    """

    ABT = 'ABT'
    CAL = 'CAL'
    EST = 'EST'
    NONE = String.EMPTY


class EvenAttr(Enum):
    """Tags for an event or attribute information.

    Reference:
        - [GEDCOM Event Attribute Enumeration](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumset-EVENATTR)"""

    CENS = 'CENS'
    NCHI = 'NCHI'
    RESI = 'RESI'
    FACT = 'FACT'
    EVEN = 'EVEN'
    NONE = String.EMPTY


class Event(Enum):
    """Tags for events."""

    ADOP = 'ADOP'
    ANUL = 'ANUL'
    BAPM = 'BAPM'
    BARM = 'BARM'
    BASM = 'BASM'
    BIRT = 'BIRT'
    BLES = 'BLES'
    BURI = 'BURI'
    CENS = 'CENS'
    CHR = 'CHR'
    CHRA = 'CHRA'
    CONF = 'CONF'
    CREM = 'CREM'
    DEAT = 'DEAT'
    DIV = 'DIV'
    DIVF = 'DIVF'
    EMIG = 'EMIG'
    ENGA = 'ENGA'
    EVEN = 'EVEN'
    FCOM = 'FCOM'
    GRAD = 'GRAD'
    IMMI = 'IMMI'
    MARB = 'MARB'
    MARC = 'MARC'
    MARL = 'MARL'
    MARR = 'MARR'
    MARS = 'MARS'
    NATU = 'NATU'
    ORDN = 'ORDN'
    PROB = 'PROB'
    RETI = 'RETI'
    WILL = 'WILL'
    NONE = String.EMPTY


class FamAttr(Enum):
    NCHI = 'NCHI'
    RESI = 'RESI'
    FACT = 'FACT'
    NONE = String.EMPTY


class FamcStat(Enum):
    CHALLENGED = 'CHALLENGED'
    DISPROVEN = 'DISPROVEN'
    PROVEN = 'PROVEN'
    NONE = String.EMPTY


class FamEven(Enum):
    ANUL = 'ANUL'
    CENS = 'CENS'
    DIV = 'DIV'
    DIVF = 'DIVF'
    ENGA = 'ENGA'
    MARB = 'MARB'
    MARC = 'MARC'
    MARL = 'MARL'
    MARR = 'MARR'
    MARS = 'MARS'
    EVEN = 'EVEN'
    NONE = String.EMPTY


class GreaterLessThan(Enum):
    GREATER = '>'
    LESS = '<'
    NONE = String.EMPTY


class Id(Enum):
    REFN = 'REFN'
    UID = 'UID'
    EXID = 'EXID'
    NONE = String.EMPTY


class IndiAttr(Enum):
    CAST = 'CAST'
    DSCR = 'DSCR'
    EDUC = 'EDUC'
    IDNO = 'IDNO'
    NATI = 'NATI'
    NCHI = 'NCHI'
    NMR = 'NMR'
    OCCU = 'OCCU'
    PROP = 'PROP'
    RELI = 'RELI'
    RESI = 'RESI'
    SSN = 'SSN'
    TITL = 'TITL'
    FACT = 'FACT'
    NONE = String.EMPTY


class IndiEven(Enum):
    ADOP = 'ADOP'
    BAPM = 'BAPM'
    BARM = 'BARM'
    BASM = 'BASM'
    BIRT = 'BIRT'
    BLES = 'BLES'
    BURI = 'BURI'
    CENS = 'CENS'
    CHR = 'CHR'
    CHRA = 'CHRA'
    CONF = 'CONF'
    CREM = 'CREM'
    DEAT = 'DEAT'
    EMIG = 'EMIG'
    FCOM = 'FCOM'
    GRAD = 'GRAD'
    IMMI = 'IMMI'
    NATU = 'NATU'
    ORDN = 'ORDN'
    PROB = 'PROB'
    RETI = 'RETI'
    WILL = 'WILL'
    EVEN = 'EVEN'
    NONE = String.EMPTY


class Latitude(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    NONE = String.EMPTY


class Longitude(Enum):
    EAST = 'E'
    WEST = 'W'
    NONE = String.EMPTY


class Medium(Enum):
    AUDIO = 'AUDIO'
    BOOK = 'BOOK'
    CARD = 'CARD'
    ELECTRONIC = 'ELECTRONIC'
    FICHE = 'FICHE'
    FILM = 'FILM'
    MAGAZINE = 'MAGAZINE'
    MANUSCRIPT = 'MANUSCRIPT'
    MAP = 'MAP'
    NEWSPAPER = 'NEWSPAPER'
    PHOTO = 'PHOTO'
    TOMBSTONE = 'TOMBSTONE'
    VIDEO = 'VIDEO'
    OTHER = 'OTHER'
    NONE = String.EMPTY


class MediaType(Enum):
    TEXT_HTML = 'TEXT_HTML'
    TEXT_PLAIN = 'TEXT_PLAIN'
    NONE = String.EMPTY


class NameType(Enum):
    AKA = 'AKA'
    BIRTH = 'BIRTH'
    IMMIGRANT = 'IMMIGRANT'
    MAIDEN = 'MAIDEN'
    MARRIED = 'MARRIED'
    PROFESSIONAL = 'PROFESSIONAL'
    OTHER = 'OTHER'
    NONE = String.EMPTY


class Pedi(Enum):
    ADOPTED = 'ADOPTED'
    BIRTH = 'BIRTH'
    FOSTER = 'FOSTER'
    SEALING = 'SEALING'
    OTHER = 'OTHER'
    NONE = String.EMPTY


class PersonalNamePieceTag(Enum):
    NPFX = 'NPFX'
    GIVN = 'GIVN'
    NICK = 'NICK'
    SPFX = 'SPFX'
    SURN = 'SURN'
    NSFX = 'NSFX'
    NONE = String.EMPTY


class Quay(Enum):
    QUAY0 = '0'
    QUAY1 = '1'
    QUAY2 = '2'
    QUAY3 = '3'
    NONE = String.EMPTY


class RangeDate(Enum):
    """
    Enumeration values for date ranges.

    Reference:

    [Date](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
    """

    BET = 'BET'
    AND = 'AND'
    AFT = 'AFT'
    BEF = 'BEF'
    NONE = String.EMPTY


class Record(str, Enum):
    FAM = 'FAM'
    INDI = 'INDI'
    OBJE = 'OBJE'
    REPO = 'REPO'
    SNOTE = 'SNOTE'
    SOUR = 'SOUR'
    SUBM = 'SUBM'
    NONE = String.EMPTY


class Resn(Enum):
    """
    Restriction codes or NONE for no restriction.

    Reference:

    - [GEDCOM RESN Enumeration](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#RESN)
    - [GEDCOM RESN Codes](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumset-RESN)
    """

    CONFIDENTIAL = 'CONFIDENTIAL'
    LOCKED = 'LOCKED'
    PRIVACY = 'PRIVACY'
    NONE = String.EMPTY


class RestrictDate(Enum):
    """Enumeration values for all date restrictions.

    Reference:

    [Date](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
    """

    FROM = 'FROM'
    TO = 'TO'
    BET = 'BET'
    AND = 'AND'
    BEF = 'BEF'
    AFT = 'AFT'
    CAL = 'CAL'
    EST = 'EST'
    NONE = String.EMPTY


class Role(Enum):
    CHIL = 'CHIL'
    CLERGY = 'CLERGY'
    FATH = 'FATH'
    FRIEND = 'FRIEND'
    GODP = 'GODP'
    HUSB = 'HUSB'
    MOTH = 'MOTH'
    MULTIPLE = 'MULTIPLE'
    NGHBR = 'NGHBR'
    OFFICIATOR = 'OFFICIATOR'
    PARENT = 'PARENT'
    SPOU = 'SPOU'
    WIFE = 'WIFE'
    WITN = 'WITN'
    OTHER = 'OTHER'
    NONE = String.EMPTY


class Sex(Enum):
    M = 'M'
    F = 'F'
    X = 'X'
    U = 'U'
    NONE = String.EMPTY


class Stat(Enum):
    BIC = 'BIC'
    CANCELED = 'CANCELED'
    CHILD = 'CHILD'
    COMPLETED = 'COMPLETED'
    EXCLUDED = 'EXCLUDED'
    DNS = 'DNS'
    DNS_CAN = 'DNS_CAN'
    INFANT = 'INFANT'
    PRE_1970 = 'PRE_1970'
    STILLBORN = 'STILLBORN'
    SUBMITTED = 'SUBMITTED'
    UNCLEARED = 'UNCLEARED'
    NONE = String.EMPTY


class Tag(Enum):
    """Tags used for various structure types in the GEDCOM standard.

    Reference
    ---------
    - [GEDCOM Structure Types](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#structure-types)
    """

    ABBR = 'ABBR'
    ADDR = 'ADDR'
    ADOP = 'ADOP'
    ADR1 = 'ADR1'
    ADR2 = 'ADR2'
    ADR3 = 'ADR3'
    AGE = 'AGE'
    AGNC = 'AGNC'
    ALIA = 'ALIA'
    ANCI = 'ANCI'
    ANUL = 'ANUL'
    ASSO = 'ASSO'
    AUTH = 'AUTH'
    BAPL = 'BAPL'
    BAPM = 'BAPM'
    BARM = 'BARM'
    BASM = 'BASM'
    BIRT = 'BIRT'
    BLES = 'BLES'
    BURI = 'BURI'
    CALN = 'CALN'
    CAST = 'CAST'
    CAUS = 'CAUS'
    CENS = 'CENS'
    CHAN = 'CHAN'
    CHIL = 'CHIL'
    CHR = 'CHR'
    CHRA = 'CHRA'
    CITY = 'CITY'
    CONF = 'CONF'
    CONL = 'CONL'
    CONT = 'CONT'
    COPR = 'COPR'
    CORP = 'CORP'
    CREA = 'CREA'
    CREM = 'CREM'
    CROP = 'CROP'
    CTRY = 'CTRY'
    DATA = 'DATA'
    DATE = 'DATE'
    DEAT = 'DEAT'
    DESI = 'DESI'
    DEST = 'DEST'
    DIV = 'DIV'
    DIVF = 'DIVF'
    DSCR = 'DSCR'
    EDUC = 'EDUC'
    EMAIL = 'EMAIL'
    EMIG = 'EMIG'
    ENDL = 'ENDL'
    ENGA = 'ENGA'
    EVEN = 'EVEN'
    EXID = 'EXID'
    FACT = 'FACT'
    FAM = 'FAM'
    FATH = 'FATH'
    FAMC = 'FAMC'
    FAMS = 'FAMS'
    FAX = 'FAX'
    FCOM = 'FCOM'
    FILE = 'FILE'
    FILM = 'FILM'
    FORM = 'FORM'
    GEDC = 'GEDC'
    GIVN = 'GIVN'
    GRAD = 'GRAD'
    HEAD = 'HEAD'
    HEIGHT = 'HEIGHT'
    HUSB = 'HUSB'
    IDNO = 'IDNO'
    IMMI = 'IMMI'
    INDI = 'INDI'
    INIL = 'INIL'
    LANG = 'LANG'
    LANG_ = '_LANG'
    LATI = 'LATI'
    LEFT = 'LEFT'
    LONG = 'LONG'
    MAP = 'MAP'
    MARB = 'MARB'
    MARC = 'MARC'
    MARL = 'MARL'
    MARR = 'MARR'
    MARS = 'MARS'
    MEDI = 'MEDI'
    MIME = 'MIME'
    NAME = 'NAME'
    NATI = 'NATI'
    NATU = 'NATU'
    NCHI = 'NCHI'
    NICK = 'NICK'
    NMR = 'NMR'
    NO = 'NO'
    NOTE = 'NOTE'
    NPFX = 'NPFX'
    NSFX = 'NSFX'
    OBJE = 'OBJE'
    OCCU = 'OCCU'
    ORDN = 'ORDN'
    PAGE = 'PAGE'
    PEDI = 'PEDI'
    PHON = 'PHON'
    PHRASE = 'PHRASE'
    PLAC = 'PLAC'
    POST = 'POST'
    PROB = 'PROB'
    PROP = 'PROP'
    PUBL = 'PUBL'
    QUAY = 'QUAY'
    REFN = 'REFN'
    RELI = 'RELI'
    REPO = 'REPO'
    RESI = 'RESI'
    RESN = 'RESN'
    RETI = 'RETI'
    ROLE = 'ROLE'
    SCHMA = 'SCHMA'
    SDATE = 'SDATE'
    SEX = 'SEX'
    SLGC = 'SLGC'
    SLGS = 'SLGS'
    SNOTE = 'SNOTE'
    SOUR = 'SOUR'
    SPFX = 'SPFX'
    SPOU = 'SPOU'
    SSN = 'SSN'
    STAE = 'STAE'
    STAT = 'STAT'
    SUBM = 'SUBM'
    SURN = 'SURN'
    TAG = 'TAG'
    TEMP = 'TEMP'
    TEXT = 'TEXT'
    TIME = 'TIME'
    TITL = 'TITL'
    TOP = 'TOP'
    TRAN = 'TRAN'
    TRLR = 'TRLR'
    TYPE = 'TYPE'
    UID = 'UID'
    VERS = 'VERS'
    WIDTH = 'WIDTH'
    WIFE = 'WIFE'
    WILL = 'WILL'
    WWW = 'WWW'
    NONE = String.EMPTY
