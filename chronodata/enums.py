# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Enumeration classes to build a dataset formatted according
to the GEDCOM standard.

References
----------

- [Date Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
- [Python Enum Support](https://docs.python.org/3/library/enum.html#)
- [PEP 435](https://peps.python.org/pep-0435/)
- [RealPython Tutorial](https://realpython.com/python-enum/)
"""

from enum import Enum


class ApproxDate(Enum):
    """Enumeration values for date approximations.

    Reference
    ---------
    [Date](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
    """

    ABT = 'ABT'
    CAL = 'CAL'
    EST = 'EST'


class GreaterLessThan(Enum):
    EQUAL = ''
    GREATER = '>'
    LESS = '<'


class RangeDate(Enum):
    """Enumeration values for date ranges.

    Reference
    ---------
    [Date](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
    """

    BET = 'BET'
    AND = 'AND'
    AFT = 'AFT'
    BEF = 'BEF'


class RestrictDate(Enum):
    """Enumeration values for all date restrictions.

    Reference
    ---------
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


class Sex(Enum):
    M = 'M'
    F = 'F'
    X = 'X'
    U = 'U'


class Adop(Enum):
    HUSB = 'HUSB'
    WIFE = 'WIFE'
    BOTH = 'BOTH'


class EvenAttr(Enum):
    CENS = 'CENS'
    NCHI = 'NCHI'
    RESI = 'RESI'
    FACT = 'FACT'
    EVEN = 'EVEN'


class FamcStat(Enum):
    CHALLENGED = 'CHALLENGED'
    DISPROVEN = 'DISPROVEN'
    PROVEN = 'PROVEN'


class FamAttr(Enum):
    NCHI = 'NCHI'
    RESI = 'RESI'
    FACT = 'FACT'


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


class Id(Enum):
    REFN = 'REFN'
    UID = 'UID'
    EXID = 'EXID'


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


class Medi(Enum):
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


class MediaType(Enum):
    TEXT_HTML = 'TEXT_HTML'
    TEXT_PLAIN = 'TEXT_PLAIN'


class NameType(Enum):
    AKA = 'AKA'
    BIRTH = 'BIRTH'
    IMMIGRANT = 'IMMIGRANT'
    MAIDEN = 'MAIDEN'
    MARRIED = 'MARRIED'
    PROFESSIONAL = 'PROFESSIONAL'
    OTHER = 'OTHER'


class Pedi(Enum):
    ADOPTED = 'ADOPTED'
    BIRTH = 'BIRTH'
    FOSTER = 'FOSTER'
    SEALING = 'SEALING'
    OTHER = 'OTHER'


class PersonalNamePiece(Enum):
    NPFX = 'NPFX'
    GIVN = 'GIVN'
    NICK = 'NICK'
    SPFX = 'SPFX'
    SURN = 'SURN'
    NSFX = 'NSFX'

class Quay(Enum):
    QUAY0 = '0'
    QUAY1 = '1'
    QUAY2 = '2'
    QUAY3 = '3'

class Records(Enum):
    FAM = 'FAM'
    INDI = 'INDI'
    OBJE = 'OBJE'
    REPO = 'REPO'
    SNOTE = 'SNOTE'
    SOUR = 'SOUR'
    SUBM = 'SUBM'

class Resn(Enum):
    CONFIDENTIAL = 'CONFIDENTIAL'
    LOCKED = 'LOCKED'
    PRIVACY = 'PRIVACY'

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
