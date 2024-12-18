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

class Record(str, Enum):
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
