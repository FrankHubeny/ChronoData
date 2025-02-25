# gedcom.py
"""Store GEDCOM specific constants, tags, enumeration sets and structure representations.

These are values that may be used in the Tag position of a GEDCOM line
    where a line contains the following components:
        - Required Level: A non-negative integer denoting the level of the line.
        - Optional Xref: A cross-reference identifier.
        - Required Tag: A value from this enumeration class or an extended Tag defined by the `Schema` class.
        - Optional LineVal: A string or value from a GEDCOM enumeration set.
            This is also called the payload.

    Values from this enumeration class are defined as enumeration sets to validate the use of the tag
    in a structure type.  The following are such Tag subenumerations:
        - `FamAttr`:
        - `IndiAttr`:
        - `IndiEven`:
        - `PersonalNamePieceTag`:
        - `Record`:

    The GEDCOM enumeration sets are implemented as enumeration classes with the similar names.  These
    are not Tags nor subenumerations of Tag, but independent enumeration classes.
        - `Adop`: [ADOP enumset]()
        - `Even`: [EVEN enumset]()
        - `EvenAttr`: [EVEN-ATTR enumset]()
        - `FamcStat`: [FAMC-STAT enumset]()
        - `Medium`: [MEDI enumset]()
        - `NameType`: [NAME-TYPE enumset]()
        - `Pedi`: [PEDI enumset]()
        - `Quay`: [QUAY enumset]()
        - `Resn`: [RESN enumset]()
        - `Role`: [ROLE enumset]()
        - `Sex`: [SEX enumset]()
        - `Stat`: [ord-STAT enumset]()


These enumation sets should not be confused with Tags.  They are used in the LineVal part of
a GEDCOM line rather than the Tag part of the line.

    References:
        [GEDCOM Enumeration Values](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#enumeration-values)
        [GEDCOM Line](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#lines)
        [GEDCOM Structure Types](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#structure-types)
        [GEDCOM Specification](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)
"""

__all__ = [
    'Adop',
    'Even',
    'EvenAttr',
    'FamAttr',
    'FamEven',
    'FamcStat',
    'Id',
    'IndiAttr',
    'IndiEven',
    'Medium',
    'NameType',
    'OverView',
    'Pedi',
    'PersonalNamePieceTag',
    'Quay',
    'Record',
    'Resn',
    'Role',
    'Sex',
    'Specs',
    'Stat',
    'Tag',
]

from dataclasses import dataclass
from enum import Enum
from typing import Any, NamedTuple


class Config:
    """Values specifying which version of the GEDCOM specification are being used."""

    VERSION: str = '7'
    GEDVERSION: str = f'{VERSION}.0'
    TERMS: str = f'https://gedcom.io/terms/v{VERSION}/'
    SPECS: str = (
        f'https://gedcom.io/specifications/FamilySearchGEDCOMv{VERSION}.html'
    )


class DataType(Enum):
    """Enumerate the GEDCOM data types.

    Reference:
        [GEDCOM Data Types](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#datatypes)
    """

    TEXT = 'Text'
    INTEGER = 'Integer'
    ENUMERATION = 'Enumeration'
    DATE = 'Date'
    TIME = 'Time'
    AGE = 'Age'
    LIST = 'List'
    PERSONAL_NAME = 'Personal Name'
    LANGUAGE = 'Language'
    MEDIA_TYPE = 'Media Type'
    SPECIAL = 'Special'
    FILE_PATH = 'File Path'


class Line(NamedTuple):
    """A datastructure to store a GEDCOM line with documentation."""

    tag: str
    data_type: DataType
    required: bool
    many: bool
    docs: str
    increment: int = 0
    xref: bool = False
    extra: str = ''
    supers: list[Any] | None = None
    subs: list[Any] | None = None

    def show(self, level: int = 0) -> str:
        return f'{level + self.increment} {self.tag} {self.data_type} ({self.required}:{self.many}) {self.docs}'


class Tag(Enum):
    """Enumerate all of the standard tags signalling structure types in the GEDCOM specification."""

    ABBR = 'ABBR'
    ADDR = 'ADDR'
    ADOP = 'ADOP'
    ADOPTED = 'ADOPTED'
    ADR1 = 'ADR1'
    ADR2 = 'ADR2'
    ADR3 = 'ADR3'
    AGE = 'AGE'
    AGNC = 'AGNC'
    AKA = 'AKA'
    ALIA = 'ALIA'
    ANCI = 'ANCI'
    ANUL = 'ANUL'
    ASSO = 'ASSO'
    AUDIO = 'AUDIO'
    AUTH = 'AUTH'
    BAPL = 'BAPL'
    BAPM = 'BAPM'
    BARM = 'BARM'
    BASM = 'BASM'
    BIC = 'BIC'
    BIRT = 'BIRT'
    BIRTH = 'BIRTH'
    BLES = 'BLES'
    BOOK = 'BOOK'
    BOTH = 'BOTH'
    BURI = 'BURI'
    CALN = 'CALN'
    CANCELED = 'CANCELED'
    CARD = 'CARD'
    CAST = 'CAST'
    CAUS = 'CAUS'
    CENS = 'CENS'
    CHALLENGED = 'CHALLENGED'
    CHAN = 'CHAN'
    CHIL = 'CHIL'
    CHILD = 'CHILD'
    CHR = 'CHR'
    CHRA = 'CHRA'
    CITY = 'CITY'
    CLERGY = 'CLERGY'
    COMPLETED = 'COMPLETED'
    CONC = 'CONC'
    CONF = 'CONF'
    CONFIDENTIAL = 'CONFIDENTIAL'
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
    DISPROVEN = 'DISPROVEN'
    DIV = 'DIV'
    DIVF = 'DIVF'
    DNS = 'DNS'
    DNS_CAN = 'DNS_CAN'
    DSCR = 'DSCR'
    EDUC = 'EDUC'
    ELECTRONIC = 'ELECTRONIC'
    EMAIL = 'EMAIL'
    EMIG = 'EMIG'
    ENDL = 'ENDL'
    ENGA = 'ENGA'
    EVEN = 'EVEN'
    EXCLUDED = 'EXCLUDED'
    EXID = 'EXID'
    F = 'F'
    FACT = 'FACT'
    FAM = 'FAM'
    FATH = 'FATH'
    FAMC = 'FAMC'
    FAMS = 'FAMS'
    FAX = 'FAX'
    FCOM = 'FCOM'
    FICHE = 'FICHE'
    FILE = 'FILE'
    FILM = 'FILM'
    FORM = 'FORM'
    FOSTER = 'FOSTER'
    FRENCH_R = 'FRENCH_R'
    FRIEND = 'FRIEND'
    GEDC = 'GEDC'
    GIVN = 'GIVN'
    GODP = 'GODP'
    GRAD = 'GRAD'
    GREGORIAN = 'GREGORIAN'
    HEAD = 'HEAD'
    HEBREW = 'HEBREW'
    HEIGHT = 'HEIGHT'
    HUSB = 'HUSB'
    IDNO = 'IDNO'
    IMMI = 'IMMI'
    IMMIGRANT = 'IMMIGRANT'
    INDI = 'INDI'
    INFANT = 'INFANT'
    INIL = 'INIL'
    JULIAN = 'JULIAN'
    LANG = 'LANG'
    LANG_ = '_LANG'
    LATI = 'LATI'
    LEFT = 'LEFT'
    LOCKED = 'LOCKED'
    LONG = 'LONG'
    M = 'M'
    MAGAZINE = 'MAGAZINE'
    MAIDEN = 'MAIDEN'
    MANUSCRIPT = 'MANUSCRIPT'
    MAP = 'MAP'
    MARB = 'MARB'
    MARC = 'MARC'
    MARL = 'MARL'
    MARR = 'MARR'
    MARRIED = 'MARRIED'
    MARS = 'MARS'
    MEDI = 'MEDI'
    MIME = 'MIME'
    MOTH = 'MOTH'
    MULTIPLE = 'MULTIPLE'
    NAME = 'NAME'
    NATI = 'NATI'
    NATU = 'NATU'
    NCHI = 'NCHI'
    NEWSPAPER = 'NEWSPAPER'
    NGHBR = 'NGHBR'
    NICK = 'NICK'
    NMR = 'NMR'
    NO = 'NO'
    NOTE = 'NOTE'
    NPFX = 'NPFX'
    NSFX = 'NSFX'
    OBJE = 'OBJE'
    OCCU = 'OCCU'
    OFFICIATOR = 'OFFICIATOR'
    ORDN = 'ORDN'
    OTHER = 'OTHER'
    PAGE = 'PAGE'
    PARENT = 'PARENT'
    PEDI = 'PEDI'
    PHON = 'PHON'
    PHOTO = 'PHOTO'
    PHRASE = 'PHRASE'
    PLAC = 'PLAC'
    POST = 'POST'
    PROB = 'PROB'
    PRE_1970 = 'PRE_1970'
    PRIVACY = 'PRIVACY'
    PROFESSIONAL = 'PROFESSIONAL'
    PROP = 'PROP'
    PROVEN = 'PROVEN'
    PUBL = 'PUBL'
    QUAY = 'QUAY'
    QUAY0 = '0'
    QUAY1 = '1'
    QUAY2 = '2'
    QUAY3 = '3'
    REFN = 'REFN'
    RELI = 'RELI'
    REPO = 'REPO'
    RESI = 'RESI'
    RESN = 'RESN'
    RETI = 'RETI'
    ROLE = 'ROLE'
    SCHMA = 'SCHMA'
    SDATE = 'SDATE'
    SEALING = 'SEALING'
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
    STILLBORN = 'STILLBORN'
    SUBM = 'SUBM'
    SUBMITTED = 'SUBMITTED'
    SURN = 'SURN'
    TAG = 'TAG'
    TEMP = 'TEMP'
    TEXT = 'TEXT'
    TIME = 'TIME'
    TITL = 'TITL'
    TOMBSTONE = 'TOMBSTONE'
    TOP = 'TOP'
    TRAN = 'TRAN'
    TRLR = 'TRLR'
    TYPE = 'TYPE'
    U = 'U'
    UID = 'UID'
    UNCLEARED = 'UNCLEARED'
    VERS = 'VERS'
    VIDEO = 'VIDEO'
    WIDTH = 'WIDTH'
    WIFE = 'WIFE'
    WILL = 'WILL'
    WITN = 'WITN'
    WWW = 'WWW'
    X = 'X'
    NONE = ''


@dataclass(frozen=True)
class Docs:
    ABBR = f'{Config.TERMS}{Tag.ABBR.value}'
    ADDR = f'{Config.TERMS}{Tag.ADDR.value}'
    ADOP = f'{Config.TERMS}{Tag.ADOP.value}'
    ADOP_FAMC = f'{Config.TERMS}{Tag.ADOP.value}-{Tag.FAMC.value}'
    ADR1 = f'{Config.TERMS}{Tag.ADR1.value}'
    ADR2 = f'{Config.TERMS}{Tag.ADR2.value}'
    ADR3 = f'{Config.TERMS}{Tag.ADR3.value}'
    AGE = f'{Config.TERMS}{Tag.AGE.value}'
    AGNC = f'{Config.TERMS}{Tag.AGNC.value}'
    ALIA = f'{Config.TERMS}{Tag.ALIA.value}'
    ANCI = f'{Config.TERMS}{Tag.ANCI.value}'
    ANUL = f'{Config.TERMS}{Tag.ANUL.value}'
    ASSO = f'{Config.TERMS}{Tag.ASSO.value}'
    AUTH = f'{Config.TERMS}{Tag.AUTH.value}'
    BAPL = f'{Config.TERMS}{Tag.BAPL.value}'
    BAPM = f'{Config.TERMS}{Tag.BAPM.value}'
    BARM = f'{Config.TERMS}{Tag.BARM.value}'
    BASM = f'{Config.TERMS}{Tag.BASM.value}'
    BIRT = f'{Config.TERMS}{Tag.BIRT.value}'
    BLES = f'{Config.TERMS}{Tag.BLES.value}'
    BURI = f'{Config.TERMS}{Tag.BURI.value}'
    CALN = f'{Config.TERMS}{Tag.CALN.value}'
    CAST = f'{Config.TERMS}{Tag.CAST.value}'
    CAUS = f'{Config.TERMS}{Tag.CAUS.value}'
    CHAN = f'{Config.TERMS}{Tag.CHAN.value}'
    CHIL = f'{Config.TERMS}{Tag.CHIL.value}'
    CHR = f'{Config.TERMS}{Tag.CHR.value}'
    CHRA = f'{Config.TERMS}{Tag.CHRA.value}'
    CITY = f'{Config.TERMS}{Tag.CITY.value}'
    CONF = f'{Config.TERMS}{Tag.CONF.value}'
    CONL = f'{Config.TERMS}{Tag.CONL.value}'
    COPR = f'{Config.TERMS}{Tag.COPR.value}'
    CORP = f'{Config.TERMS}{Tag.CORP.value}'
    CREA = f'{Config.TERMS}{Tag.CREA.value}'
    CREM = f'{Config.TERMS}{Tag.CREM.value}'
    CROP = f'{Config.TERMS}{Tag.CROP.value}'
    CTRY = f'{Config.TERMS}{Tag.CTRY.value}'
    DATA = f'{Config.TERMS}{Tag.DATA.value}'
    DATA_EVEN = f'{Config.TERMS}{Tag.DATA.value}-{Tag.EVEN.value}'
    DATA_EVEN_DATE = (
        f'{Config.TERMS}{Tag.DATA.value}-{Tag.EVEN.value}-{Tag.DATE.value}'
    )
    DATE = f'{Config.TERMS}{Tag.DATE.value}'
    DATE_EXACT = f'{Config.TERMS}{Tag.DATE.value}-exact'
    DEAT = f'{Config.TERMS}{Tag.DEAT.value}'
    DESI = f'{Config.TERMS}{Tag.DESI.value}'
    DEST = f'{Config.TERMS}{Tag.DEST.value}'
    DIV = f'{Config.TERMS}{Tag.DIV.value}'
    DIVF = f'{Config.TERMS}{Tag.DIVF.value}'
    DSCR = f'{Config.TERMS}{Tag.DSCR.value}'
    EDUC = f'{Config.TERMS}{Tag.EDUC.value}'
    EMAIL = f'{Config.TERMS}{Tag.EMAIL.value}'
    EMIG = f'{Config.TERMS}{Tag.EMIG.value}'
    ENDL = f'{Config.TERMS}{Tag.ENDL.value}'
    ENGA = f'{Config.TERMS}{Tag.ENGA.value}'
    EXID = f'{Config.TERMS}{Tag.EXID.value}'
    EXID_TYPE = f'{Config.TERMS}{Tag.EXID.value}-{Tag.TYPE.value}'
    FAM_CENS = f'{Config.TERMS}{Tag.FAM.value}-{Tag.CENS.value}'
    FAM_EVEN = f'{Config.TERMS}{Tag.FAM.value}-{Tag.EVEN.value}'
    FAM_FACT = f'{Config.TERMS}{Tag.FAM.value}-{Tag.FACT.value}'
    FAM_HUSB = f'{Config.TERMS}{Tag.FAM.value}-{Tag.HUSB.value}'
    FAM_NCHI = f'{Config.TERMS}{Tag.FAM.value}-{Tag.NCHI.value}'
    FAM_RESI = f'{Config.TERMS}{Tag.FAM.value}-{Tag.RESI.value}'
    FAM_WIFE = f'{Config.TERMS}{Tag.FAM.value}-{Tag.WIFE.value}'
    FAMC = f'{Config.TERMS}{Tag.FAMC.value}'
    FAMC_ADOP = f'{Config.TERMS}{Tag.FAMC.value}-{Tag.ADOP.value}'
    FAMC_STAT = f'{Config.TERMS}{Tag.FAMC.value}-{Tag.STAT.value}'
    FAMS = f'{Config.TERMS}{Tag.FAMS.value}'
    FAX = f'{Config.TERMS}{Tag.FAX.value}'
    FCOM = f'{Config.TERMS}{Tag.FCOM.value}'
    FILE = f'{Config.TERMS}{Tag.FILE.value}'
    FILE_TRAN = f'{Config.TERMS}{Tag.FILE.value}-{Tag.TRAN.value}'
    FORM = f'{Config.TERMS}{Tag.FORM.value}'
    GEDC = f'{Config.TERMS}{Tag.GEDC.value}'
    GEDC_VERS = f'{Config.TERMS}{Tag.GEDC.value}-{Tag.VERS.value}'
    GIVN = f'{Config.TERMS}{Tag.GIVN.value}'
    GRAD = f'{Config.TERMS}{Tag.GRAD.value}'
    HEAD = f'{Config.TERMS}{Tag.HEAD.value}'
    HEAD_DATE = f'{Config.TERMS}{Tag.HEAD.value}-{Tag.DATE.value}'
    HEAD_PLAC = f'{Config.TERMS}{Tag.HEAD.value}-{Tag.PLAC.value}'
    HEAD_PLAC_FORM = (
        f'{Config.TERMS}{Tag.HEAD.value}-{Tag.PLAC.value}-{Tag.FORM.value}'
    )
    HEAD_SOUR = f'{Config.TERMS}{Tag.HEAD.value}-{Tag.SOUR.value}'
    HEAD_SOUR_DATA = (
        f'{Config.TERMS}{Tag.HEAD.value}-{Tag.SOUR.value}-{Tag.DATA.value}'
    )
    HEIGHT = f'{Config.TERMS}{Tag.HEIGHT.value}'
    HUSB = f'{Config.TERMS}{Tag.HUSB.value}'
    IDNO = f'{Config.TERMS}{Tag.IDNO.value}'
    IMMI = f'{Config.TERMS}{Tag.IMMI.value}'
    INDI_CENS = f'{Config.TERMS}{Tag.INDI.value}-{Tag.CENS.value}'
    INDI_EVEN = f'{Config.TERMS}{Tag.INDI.value}-{Tag.EVEN.value}'
    INDI_FACT = f'{Config.TERMS}{Tag.INDI.value}-{Tag.FACT.value}'
    INDI_FAMC = f'{Config.TERMS}{Tag.INDI.value}-{Tag.FAMC.value}'
    INDI_NAME = f'{Config.TERMS}{Tag.INDI.value}-{Tag.NAME.value}'
    INDI_NCHI = f'{Config.TERMS}{Tag.INDI.value}-{Tag.NCHI.value}'
    INDI_RELI = f'{Config.TERMS}{Tag.INDI.value}-{Tag.RELI.value}'
    INDI_RESI = f'{Config.TERMS}{Tag.INDI.value}-{Tag.RESI.value}'
    INDI_TITL = f'{Config.TERMS}{Tag.INDI.value}-{Tag.TITL.value}'
    INIL = f'{Config.TERMS}{Tag.INIL.value}'
    LANG = f'{Config.TERMS}{Tag.LANG.value}'
    LATI = f'{Config.TERMS}{Tag.LATI.value}'
    LEFT = f'{Config.TERMS}{Tag.LEFT.value}'
    LONG = f'{Config.TERMS}{Tag.LONG.value}'
    MAP = f'{Config.TERMS}{Tag.MAP.value}'
    MARB = f'{Config.TERMS}{Tag.MARB.value}'
    MARC = f'{Config.TERMS}{Tag.MARC.value}'
    MARL = f'{Config.TERMS}{Tag.MARL.value}'
    MARR = f'{Config.TERMS}{Tag.MARR.value}'
    MARS = f'{Config.TERMS}{Tag.MARS.value}'
    MEDI = f'{Config.TERMS}{Tag.MEDI.value}'
    MIME = f'{Config.TERMS}{Tag.MIME.value}'
    NAME = f'{Config.TERMS}{Tag.NAME.value}'
    NAME_TRAN = f'{Config.TERMS}{Tag.NAME.value}-{Tag.TRAN.value}'
    NAME_TYPE = f'{Config.TERMS}{Tag.NAME.value}-{Tag.TYPE.value}'
    NATI = f'{Config.TERMS}{Tag.NATI.value}'
    NATU = f'{Config.TERMS}{Tag.NATU.value}'
    NICK = f'{Config.TERMS}{Tag.NICK.value}'
    NMR = f'{Config.TERMS}{Tag.NMR.value}'
    NO = f'{Config.TERMS}{Tag.NO.value}'
    NO_DATE = f'{Config.TERMS}{Tag.NO.value}-{Tag.DATE.value}'
    NOTE = f'{Config.TERMS}{Tag.NOTE.value}'
    NOTE_TRAN = f'{Config.TERMS}{Tag.NOTE.value}-{Tag.TRAN.value}'
    NPFX = f'{Config.TERMS}{Tag.NPFX.value}'
    NSFX = f'{Config.TERMS}{Tag.NSFX.value}'
    OBJE = f'{Config.TERMS}{Tag.OBJE.value}'
    OCCU = f'{Config.TERMS}{Tag.OCCU.value}'
    ORD_STAT = f'{Config.TERMS}ord-{Tag.STAT.value}'
    ORDN = f'{Config.TERMS}{Tag.ORDN.value}'
    PAGE = f'{Config.TERMS}{Tag.PAGE.value}'
    PEDI = f'{Config.TERMS}{Tag.PEDI.value}'
    PHON = f'{Config.TERMS}{Tag.PHON.value}'
    PHRASE = f'{Config.TERMS}{Tag.PHRASE.value}'
    PLAC = f'{Config.TERMS}{Tag.PLAC.value}'
    PLAC_FORM = f'{Config.TERMS}{Tag.PLAC.value}-{Tag.FORM.value}'
    PLAC_TRAN = f'{Config.TERMS}{Tag.PLAC.value}-{Tag.TRAN.value}'
    POST = f'{Config.TERMS}{Tag.POST.value}'
    PROB = f'{Config.TERMS}{Tag.PROB.value}'
    PROP = f'{Config.TERMS}{Tag.PROP.value}'
    PUBL = f'{Config.TERMS}{Tag.PUBL.value}'
    QUAY = f'{Config.TERMS}{Tag.QUAY.value}'
    RECORD_FAM = f'{Config.TERMS}record-{Tag.FAM.value}'
    RECORD_INDI = f'{Config.TERMS}record-{Tag.INDI.value}'
    RECORD_OBJE = f'{Config.TERMS}record-{Tag.OBJE.value}'
    RECORD_REPO = f'{Config.TERMS}record-{Tag.REPO.value}'
    RECORD_SNOTE = f'{Config.TERMS}record-{Tag.SNOTE.value}'
    RECORD_SOUR = f'{Config.TERMS}record-{Tag.SOUR.value}'
    RECORD_SUBM = f'{Config.TERMS}record-{Tag.SUBM.value}'
    REFN = f'{Config.TERMS}{Tag.REFN.value}'
    RELI = f'{Config.TERMS}{Tag.RELI.value}'
    REPO = f'{Config.TERMS}{Tag.REPO.value}'
    RESN = f'{Config.TERMS}{Tag.RESN.value}'
    RETI = f'{Config.TERMS}{Tag.RETI.value}'
    ROLE = f'{Config.TERMS}{Tag.ROLE.value}'
    SCHMA = f'{Config.TERMS}{Tag.SCHMA.value}'
    SDATE = f'{Config.TERMS}{Tag.SDATE.value}'
    SEX = f'{Config.TERMS}{Tag.SEX.value}'
    SLGC = f'{Config.TERMS}{Tag.SLGC.value}'
    SLGS = f'{Config.TERMS}{Tag.SLGS.value}'
    SNOTE = f'{Config.TERMS}{Tag.SNOTE.value}'
    SOUR = f'{Config.TERMS}{Tag.SOUR.value}'
    SOUR_DATA = f'{Config.TERMS}{Tag.SOUR.value}-{Tag.DATA.value}'
    SOUR_EVEN = f'{Config.TERMS}{Tag.SOUR.value}-{Tag.EVEN.value}'
    SPFX = f'{Config.TERMS}{Tag.SPFX.value}'
    SSN = f'{Config.TERMS}{Tag.SSN.value}'
    STAE = f'{Config.TERMS}{Tag.STAE.value}'
    SUBM = f'{Config.TERMS}{Tag.SUBM.value}'
    SUBM_LANG = f'{Config.TERMS}{Tag.SUBM.value}-{Tag.LANG.value}'
    SURN = f'{Config.TERMS}{Tag.SURN.value}'
    TAG = f'{Config.TERMS}{Tag.TAG.value}'
    TEMP = f'{Config.TERMS}{Tag.TEMP.value}'
    TEXT = f'{Config.TERMS}{Tag.TEXT.value}'
    TIME = f'{Config.TERMS}{Tag.TIME.value}'
    TITL = f'{Config.TERMS}{Tag.TITL.value}'
    TOP = f'{Config.TERMS}{Tag.TOP.value}'
    TYPE = f'{Config.TERMS}{Tag.TYPE.value}'
    UID = f'{Config.TERMS}{Tag.UID.value}'
    VERS = f'{Config.TERMS}{Tag.VERS.value}'
    WIDTH = f'{Config.TERMS}{Tag.WIDTH.value}'
    WIFE = f'{Config.TERMS}{Tag.WIFE.value}'
    WILL = f'{Config.TERMS}{Tag.WILL.value}'
    WWW = f'{Config.TERMS}{Tag.WWW.value}'


@dataclass(frozen=True)
class OverView:
    """Provide a description of the seven record types and the header record.

    Descriptions of structures between `<<` and `>>` are structure names.  Below
    these structure names are their expansion.
    If the expansion has been given earlier, it is not repeated.
    Since these start at level 0 the `+` is removed and the `n` is replaced
    with 0 for this overview.
    Individual tags have links to their yaml definitions.

    The first number is the level of the line. Then comes the tag with payload description.
    To the right is a quantity key `{optionality:quantity}`.  The optionality flag
    can be either 1 for mandatory or 0 for optiona.  The quantity flag can be either
    1 for single or M for multiple.  Following this is a link to the tag specfication.

    The actual GEDCOM file does not contain the indentations.  The indentations are used here
    and in the GEDCOM specification to make the different levels more evident.

    Example:
        To display this information import `OverView` from the gedcom module and print the
        the desired record.  To print the Header record do the following.  Only the first line
        is displayed in the example.
        >>> from genedata.gedcom import OverView
        >>> print(OverView.DATE_VALUE)  # doctest: +ELLIPSIS
        <BLANKLINE>
        n DATE <DateValue>                     {1:1}  [DATE](https://gedcom.io/terms/v7/DATE)
          +1 TIME <Time>                       {0:1}  [TIME](https://gedcom.io/terms/v7/TIME)
          +1 PHRASE <Text>                     {0:1}  [PHRASE](https://gedcom.io/terms/v7/PHRASE)
        <BLANKLINE>

    Reference:
        [The FamilySearch GEDCOM Specifications](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)
    """

    ADDRESS_STRUCTURE: str = f"""
n {Tag.ADDR.value} <Special>                       {{1:1}}  [{Tag.ADDR.value}]({Docs.ADDR})
  +1 {Tag.ADR1.value} <Special>                    {{0:1}}  [{Tag.ADR1.value}]({Docs.ADR1})
  +1 {Tag.ADR2.value} <Special>                    {{0:1}}  [{Tag.ADR2.value}]({Docs.ADR2})
  +1 {Tag.ADR3.value} <Special>                    {{0:1}}  [{Tag.ADR3.value}]({Docs.ADR3})
  +1 {Tag.CITY.value} <Special>                    {{0:1}}  [{Tag.CITY.value}]({Docs.CITY})
  +1 {Tag.STAE.value} <Special>                    {{0:1}}  [{Tag.STAE.value}]({Docs.STAE})
  +1 {Tag.POST.value} <Special>                    {{0:1}}  [{Tag.POST.value}]({Docs.POST})
  +1 {Tag.CTRY.value} <Special>                    {{0:1}}  [{Tag.CTRY.value}]({Docs.CTRY})  
"""
    ASSOCIATION_STRUCTURE: str = f"""
n {Tag.ASSO.value} @<XREF:INDI>@                   {{1:1}}  [{Tag.ASSO.value}]({Docs.ASSO})
  +1 {Tag.PHRASE.value} <Text>                     {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
  +1 {Tag.ROLE.value} <Enum>                       {{1:1}}  [{Tag.ROLE.value}]({Docs.ROLE})
     +2 {Tag.PHRASE.value} <Text>                  {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
  +1 <<SOURCE_CITATION>>               {{0:M}}
"""
    CHANGE_DATE: str = f"""
n {Tag.CHAN.value}                                 {{1:1}}  [{Tag.CHAN.value}]({Docs.CHAN})
  +1 {Tag.DATE.value} <DateExact>                  {{1:1}}  [{Tag.DATE}-exact]({Docs.DATE_EXACT})
     +2 {Tag.TIME.value} <Time>                    {{0:1}}  [{Tag.TIME.value}]({Docs.TIME})
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
"""
    CREATION_DATE: str = f"""
n {Tag.CREA.value}                                 {{1:1}}  [{Tag.CREA.value}]({Docs.CREA})
  +1 {Tag.DATE.value} <DateExact>                  {{1:1}}  [{Tag.DATE.value}-exact]({Docs.DATE_EXACT})
     +2 {Tag.TIME.value} <Time>                    {{0:1}}  [{Tag.TIME.value}]({Docs.TIME})
"""
    DATE_VALUE: str = f"""
n {Tag.DATE.value} <DateValue>                     {{1:1}}  [{Tag.DATE.value}]({Docs.DATE})
  +1 {Tag.TIME.value} <Time>                       {{0:1}}  [{Tag.TIME.value}]({Docs.TIME})
  +1 {Tag.PHRASE.value} <Text>                     {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
"""
    EVENT_DETAIL: str = f"""
n <<DATE_VALUE>>                       {{0:1}}
n <<PLACE_STRUCTURE>>                  {{0:1}}
n <<ADDRESS_STRUCTURE>>                {{0:1}}
n {Tag.PHON.value} <Special>                       {{0:M}}  [{Tag.PHON.value}]({Docs.PHON})
n {Tag.EMAIL.value} <Special>                      {{0:M}}  [{Tag.EMAIL.value}]({Docs.EMAIL})
n {Tag.FAX.value} <Special>                        {{0:M}}  [{Tag.FAX.value}]({Docs.FAX})
n {Tag.WWW.value} <Special>                        {{0:M}}  [{Tag.WWW.value}]({Docs.WWW})
n {Tag.AGNC.value} <Text>                          {{0:1}}  [{Tag.AGNC.value}]({Docs.AGNC})
n {Tag.RELI.value} <Text>                          {{0:1}}  [{Tag.RELI.value}]({Docs.RELI})
n {Tag.CAUS.value} <Text>                          {{0:1}}  [{Tag.CAUS.value}]({Docs.CAUS})
n {Tag.RESN.value} <List:Enum>                     {{0:1}}  [{Tag.RESN.value}]({Docs.RESN})
n {Tag.SDATE.value} <DateValue>                    {{0:1}}  [{Tag.SDATE.value}]({Docs.SDATE})
  +1 {Tag.TIME.value} <Time>                       {{0:1}}  [{Tag.TIME.value}]({Docs.TIME})
  +1 {Tag.PHRASE.value} <Text>                     {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
n <<ASSOCIATION_STRUCTURE>>            {{0:M}}
n <<NOTE_STRUCTURE>>                   {{0:M}}
n <<SOURCE_CITATION>>                  {{0:M}}
n <<MULTIMEDIA_LINK>>                  {{0:M}}
n {Tag.UID.value} <Special>                        {{0:M}}  [{Tag.UID.value}]()
"""
    FAMILY: str = f"""
0 @XREF:FAM@ {Tag.FAM.value}                       {{1:1}}  [record-{Tag.FAM.value}]({Docs.RECORD_FAM})
  1 {Tag.RESN.value} <List:Enum>                   {{0:1}}  [{Tag.RESN.value}]({Docs.RESN})
  1 <<FAMILY_ATTRIBUTE_STRUCTURE>>     {{0:M}}
  1 <<FAMILY_EVENT_STRUCTURE>>         {{0:M}}
  1 <<NON_EVENT_STRUCTURE>>            {{0:M}}
  1 {Tag.HUSB.value} @<XREF:INDI>@                 {{0:1}}  [{Tag.FAM.value}-{Tag.HUSB.value}]({Docs.FAM_HUSB})
    2 {Tag.PHRASE.value} <Text>                    {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
  1 {Tag.WIFE.value} @<XREF:INDI>@                 {{0:1}}  [{Tag.FAM.value}-{Tag.WIFE.value}]({Docs.FAM_WIFE})
    2 {Tag.PHRASE.value} <Text>                    {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
  1 {Tag.CHIL.value} @<XREF:INDI>@                 {{0:M}}  [{Tag.CHIL.value}]({Docs.CHIL})
    2 {Tag.PHRASE.value} <Text>                    {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
  1 <<ASSOCIATION_STRUCTURE>>          {{0:M}}
  1 {Tag.SUBM.value} @<XREF:SUBM>@                 {{0:M}}  [{Tag.SUBM.value}]({Docs.SUBM})
  1 <<LDS_SPOUSE_SEALING>>             {{0:M}}
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<NOTE_STRUCTURE>>                 {{0:M}}
  1 <<SOURCE_CITATION>>                {{0:M}}
  1 <<MULTIMEDIA_LINK>>                {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""
    FAMILY_ATTRIBUTE_STRUCTURE: str = f"""
[
n {Tag.NCHI.value} <Integer>                       {{1:1}}  [{Tag.FAM.value}-{Tag.NCHI.value}]({Docs.FAM_NCHI})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.RESI.value} <Text>                          {{1:1}}  [{Tag.FAM.value}-{Tag.RESI.value}]({Docs.FAM_RESI})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.FACT.value} <Text>                          {{1:1}}  [{Tag.FAM.value}-{Tag.FACT.value}]({Docs.FAM_FACT})
  +1 {Tag.TYPE.value} <Text>                       {{1:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
]
"""
    FAMILY_EVENT_DETAIL: str = f"""
n {Tag.HUSB.value}                                 {{0:1}}  [{Tag.HUSB.value}]({Docs.HUSB})
  +1 {Tag.AGE.value} <Age>                         {{1:1}}  [{Tag.AGE.value}]({Docs.AGE})
     +2 {Tag.PHRASE.value} <Text>                  {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
n {Tag.WIFE.value}                                 {{0:1}}  [{Tag.WIFE.value}]({Docs.WIFE})
  +1 {Tag.AGE.value} <Age>                         {{1:1}}  [{Tag.AGE.value}]({Docs.AGE})
     +2 {Tag.PHRASE.value} <Text>                  {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
n <<EVENT_DETAIL>>                     {{0:1}}
"""
    FAMILY_EVENT_STRUCTURE: str = f"""
[
n {Tag.ANUL.value} [Y|<NULL>]                      {{1:1}}  [{Tag.ANUL.value}]({Docs.ANUL})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.CENS.value} [Y|<NULL>]                      {{1:1}}  [{Tag.FAM.value}-{Tag.CENS.value}]({Docs.FAM_CENS})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.DIV.value} [Y|<NULL>]                       {{1:1}}  [{Tag.DIV.value}]({Docs.DIV})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.DIVF.value} [Y|<NULL>]                      {{1:1}}  [{Tag.DIVF.value}]({Docs.DIVF})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.ENGA.value} [Y|<NULL>]                      {{1:1}}  [{Tag.ENGA.value}]({Docs.ENGA})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.MARB.value} [Y|<NULL>]                      {{1:1}}  [{Tag.MARB.value}]({Docs.MARB})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.MARC.value} [Y|<NULL>]                      {{1:1}}  [{Tag.MARC.value}]({Docs.MARC})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.MARL.value} [Y|<NULL>]                      {{1:1}}  [{Tag.MARL.value}]({Docs.MARL})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.MARR.value} [Y|<NULL>]                      {{1:1}}  [{Tag.MARR.value}]({Docs.MARR})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.MARS.value} [Y|<NULL>]                      {{1:1}}  [{Tag.MARS.value}]({Docs.MARS})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n {Tag.EVEN.value} <Text>                          {{1:1}}  [{Tag.FAM.value}-{Tag.EVEN.value}]({Docs.FAM_EVEN})
  +1 {Tag.TYPE.value} <Text>                       {{1:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
]
"""
    HEADER: str = f"""
0 {Tag.HEAD.value}                                 {{1:1}}  [{Tag.HEAD.value}]({Docs.HEAD})
  1 {Tag.GEDC.value}                               {{1:1}}  [{Tag.GEDC.value}]({Docs.GEDC})
    2 {Tag.VERS.value} <Special>                   {{1:1}}  [{Tag.GEDC.value}-{Tag.VERS.value}]({Docs.GEDC_VERS})
  1 {Tag.SCHMA.value}                              {{0:1}}  [{Tag.SCHMA.value}]({Docs.SCHMA})
    2 {Tag.TAG.value} <Special>                    {{0:M}}  [{Tag.TAG.value}]({Docs.TAG})
  1 {Tag.SOUR.value} <Special>                     {{0:1}}  [{Tag.HEAD.value}-SOUR]({Docs.HEAD_SOUR})
    2 {Tag.VERS.value} <Special>                   {{0:1}}  [{Tag.VERS.value}]({Docs.VERS})
    2 {Tag.NAME.value} <Text>                      {{0:1}}  [{Tag.NAME.value}]({Docs.NAME})
    2 {Tag.CORP.value} <Text>                      {{0:1}}  [{Tag.CORP.value}]({Docs.CORP})
      3 <<ADDRESS_STRUCTURE>>          {{0:1}}
      3 {Tag.PHON.value} <Special>                 {{0:M}}  [{Tag.PHON.value}]({Docs.PHON})
      3 {Tag.EMAIL.value} <Special>                {{0:M}}  [{Tag.EMAIL.value}]({Docs.EMAIL})
      3 {Tag.FAX.value} <Special>                  {{0:M}}  [{Tag.FAX.value}]({Docs.FAX})
      3 {Tag.WWW.value} <Special>                  {{0:M}}  [{Tag.WWW.value}]({Docs.WWW})
    2 {Tag.DATA.value} <Text>                      {{0:1}}  [{Tag.HEAD.value}-{Tag.SOUR.value}-{Tag.DATA.value}]({Docs.HEAD_SOUR_DATA})
      3 {Tag.DATE.value} <DateExact>               {{0:1}}  [{Tag.DATE.value}-exact]({Docs.DATE_EXACT})
        4 {Tag.TIME.value} <Time>                  {{0:1}}  [{Tag.TIME.value}]({Docs.TIME})
      3 {Tag.COPR.value} <Text>                    {{0:1}}  [{Tag.COPR.value}]({Docs.COPR})
  1 {Tag.DEST.value} <Special>                     {{0:1}}  [{Tag.HEAD.value}-{Tag.DATE.value}]({Docs.HEAD_DATE})
    2 {Tag.TIME.value} <Time>                      {{0:1}}  [{Tag.TIME.value}]({Docs.TIME})
  1 {Tag.SUBM.value} @<XREF:SUBM>@                 {{0:1}}  [{Tag.SUBM.value}]({Docs.SUBM})
  1 {Tag.COPR.value} <Text>                        {{0:1}}  [{Tag.COPR.value}]({Docs.COPR})
  1 {Tag.LANG.value} <Language>                    {{0:1}}  [{Tag.HEAD.value}-{Tag.LANG.value}]({Docs.LANG})
  1 {Tag.PLAC.value}                               {{0:1}}  [{Tag.HEAD.value}-{Tag.PLAC.value}]({Docs.HEAD_PLAC})
    2 {Tag.FORM.value} <List:Text>                 {{1:1}}  [{Tag.HEAD.value}-{Tag.PLAC.value}-{Tag.FORM.value}]({Docs.HEAD_PLAC_FORM})
  1 <<NOTE_STRUCTURE>>                 {{0:1}}
    """
    IDENTIFIER_STRUCTURE: str = f"""
[
n {Tag.REFN.value} <Special>                       {{1:1}}  [{Tag.REFN.value}]({Docs.REFN})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
|
n {Tag.UID.value} <Special>                        {{1:1}}  [{Tag.UID.value}]({Docs.UID})
|
n {Tag.EXID.value} <Special>                       {{1:1}}  [{Tag.EXID.value}]({Docs.EXID})
  +1 {Tag.TYPE.value} <Special>                    {{0:1}}  [{Tag.EXID.value}-{Tag.TYPE.value}]({Docs.EXID_TYPE})
]
"""
    INDIVIDUAL: str = f"""
0 @XREF:INDI@ {Tag.INDI.value}                     {{1:1}}  [record-{Tag.INDI.value}]({Docs.RECORD_INDI})
  1 {Tag.RESN.value} <List:Enum>                   {{0:1}}  [{Tag.RESN.value}]({Docs.RESN})
  1 <<PERSONAL_NAME_STRUCTURE>>        {{0:M}}
  1 {Tag.SEX.value} <Enum>                         {{0:1}}  [{Tag.SEX.value}]({Docs.SEX})
  1 <<INDIVIDUAL_ATTRIBUTE_STRUCTURE>> {{0:M}}
  1 <<INDIVIDUAL_EVENT_STRUCTURE>>     {{0:M}}
  1 <<NON_EVENT_STRUCTURE>>            {{0:M}}
  1 <<LDS_INDIVIDUAL_ORDINANCE>>       {{0:M}}
  1 {Tag.FAMC.value} @<XREF:FAM>@                  {{0:M}}  [{Tag.INDI.value}-{Tag.FAMC.value}]({Docs.INDI_FAMC})
    2 {Tag.PEDI.value} <Enum>                      {{0:1}}  [{Tag.PEDI.value}]({Docs.PEDI})
      3 {Tag.PHRASE.value} <Text>                  {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
    2 {Tag.STAT.value} <Enum>                      {{0:1}}  [{Tag.FAMC.value}-{Tag.STAT.value}]({Docs.FAMC_STAT})
      3 {Tag.PHRASE.value} <Text>                  {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
    2 <<NOTE_STRUCTURE>>               {{0:M}}
  1 {Tag.FAMS.value} @<XREF:FAM>@                  {{0:M}}  [{Tag.FAMS.value}]({Docs.FAMS})
    2 <<NOTE_STRUCTURE>>               {{0:M}}
  1 {Tag.SUBM.value} @<XREF:SUBM>@                 {{0:M}}  [{Tag.SUBM.value}]({Docs.SUBM})
  1 <<ASSOCIATION_STRUCTURE>>          {{0:M}}
  1 {Tag.ALIA.value} @<XREF:INDI>@                 {{0:M}}  [{Tag.ALIA.value}]({Docs.ALIA})
    2 {Tag.PHRASE.value} <Text>                    {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
  1 {Tag.ANCI.value} @<XREF:SUBM>@                 {{0:M}}  [{Tag.ANCI.value}]({Docs.ANCI})
  1 {Tag.DESI.value} @<XREF:SUBM>@                 {{0:M}}  [{Tag.DESI.value}]({Docs.DESI})
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<NOTE_STRUCTURE>>                 {{0:M}}
  1 <<SOURCE_CITATION>>                {{0:M}}
  1 <<MULTIMEDIA_LINK>>                {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""
    INDIVIDUAL_ATTRIBUTE_STRUCTURE: str = f"""
[
n {Tag.CAST.value} <Text>                          {{1:1}}  [{Tag.CAST.value}]({Docs.CAST})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.DSCR.value} <Text>                          {{1:1}}  [{Tag.DSCR.value}]({Docs.DSCR})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.EDUC.value} <Text>                          {{1:1}}  [{Tag.EDUC.value}]({Docs.EDUC})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.IDNO.value} <Special>                       {{1:1}}  [{Tag.IDNO.value}]({Docs.IDNO})
  +1 {Tag.TYPE.value} <Text>                       {{1:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.NATI.value} <Text>                          {{1:1}}  [{Tag.NATI.value}]({Docs.NATI})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.NCHI.value} <Integer>                       {{1:1}}  [{Tag.INDI.value}-{Tag.NCHI.value}]({Docs.INDI_NCHI})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.NMR.value} <Integer>                        {{1:1}}  [{Tag.NMR.value}]({Docs.NMR})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.OCCU.value} <Text>                          {{1:1}}  [{Tag.OCCU.value}]({Docs.OCCU})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.PROP.value} <Text>                          {{1:1}}  [{Tag.PROP.value}]({Docs.PROP})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.RELI.value} <Text>                          {{1:1}}  [{Tag.INDI.value}-{Tag.RELI.value}]({Docs.INDI_RELI})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.RESI.value} <Text>                          {{1:1}}  [{Tag.INDI.value}-{Tag.RESI.value}]({Docs.INDI_RESI})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.SSN.value} <Special>                        {{1:1}}  [{Tag.SSN.value}]({Docs.SSN})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.TITL.value} <Text>                          {{1:1}}  [{Tag.INDI.value}-{Tag.TITL.value}]({Docs.INDI_TITL})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.FACT.value} <Text>                          {{1:1}}  [{Tag.INDI.value}-{Tag.FACT.value}]({Docs.INDI_FACT})
  +1 {Tag.TYPE.value} <Text>                       {{1:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
]
"""
    INDIVIDUAL_EVENT_DETAIL: str = f"""
n <<EVENT_DETAIL>>                     {{1:1}}
n {Tag.AGE.value} <Age>                            {{0:1}}  [{Tag.AGE.value}]({Docs.AGE})
  +1 {Tag.PHRASE.value} <Text>                     {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
"""
    INDIVIDUAL_EVENT_STRUCTURE: str = f"""
[
n {Tag.ADOP.value} [Y|<NULL>]                      {{1:1}}  [{Tag.ADOP.value}]({Docs.ADOP})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
  +1 {Tag.FAMC.value} @<XREF:FAM>@                 {{0:1}}  [{Tag.ADOP.value}-{Tag.FAMC.value}]({Docs.ADOP_FAMC})
     +2 {Tag.ADOP.value} <Enum>                    {{0:1}}  [{Tag.FAMC.value}-{Tag.ADOP.value}]({Docs.FAMC_ADOP})
        +3 {Tag.PHRASE.value} <Text>               {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
|
n {Tag.BAPM.value} [Y|<NULL>]                      {{1:1}}  [{Tag.BAPM.value}]({Docs.BAPM})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.BARM.value} [Y|<NULL>]                      {{1:1}}  [{Tag.BARM.value}]({Docs.BARM})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.BASM.value} [Y|<NULL>]                      {{1:1}}  [{Tag.BASM.value}]({Docs.BASM})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.BIRT.value} [Y|<NULL>]                      {{1:1}}  [{Tag.BIRT.value}]({Docs.BIRT})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
  +1 {Tag.FAMC.value} @<XREF:FAM>@                 {{0:1}}  [{Tag.FAMC.value}]({Docs.TYPE})
|
n {Tag.BLES.value} [Y|<NULL>]                      {{1:1}}  [{Tag.BLES.value}]({Docs.BLES})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.BURI.value} [Y|<NULL>]                      {{1:1}}  [{Tag.BURI.value}]({Docs.BURI})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}

n {Tag.CENS.value} [Y|<NULL>]                      {{1:1}}  [{Tag.INDI.value}-{Tag.CENS.value}]({Docs.INDI_CENS})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.CHR.value} [Y|<NULL>]                       {{1:1}}  [{Tag.CHR.value}]({Docs.CHR})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
  +1 {Tag.FAMC.value} @<XREF:FAM>@                 {{0:1}}  [{Tag.FAMC.value}]({Docs.FAMC})
|
n {Tag.CHRA.value} [Y|<NULL>]                      {{1:1}}  [{Tag.CHRA.value}]({Docs.CHRA})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.CONF.value} [Y|<NULL>]                      {{1:1}}  [{Tag.CONF.value}]({Docs.CONF})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.CREM.value} [Y|<NULL>]                      {{1:1}}  [{Tag.CREM.value}]({Docs.CREM})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.DEAT.value} [Y|<NULL>]                      {{1:1}}  [{Tag.DEAT.value}]({Docs.DEAT})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.EMIG.value} [Y|<NULL>]                      {{1:1}}  [{Tag.EMIG.value}]({Docs.EMIG})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.FCOM.value} [Y|<NULL>]                      {{1:1}}  [{Tag.FCOM.value}]({Docs.FCOM})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.GRAD.value} [Y|<NULL>]                      {{1:1}}  [{Tag.GRAD.value}]({Docs.GRAD})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.IMMI.value} [Y|<NULL>]                      {{1:1}}  [{Tag.IMMI.value}]({Docs.IMMI})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.NATU.value} [Y|<NULL>]                      {{1:1}}  [{Tag.NATU.value}]({Docs.NATU})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.ORDN.value} [Y|<NULL>]                      {{1:1}}  [{Tag.ORDN.value}]({Docs.ORDN})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.PROB.value} [Y|<NULL>]                      {{1:1}}  [{Tag.PROB.value}]({Docs.PROB})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.RETI.value} [Y|<NULL>]                      {{1:1}}  [{Tag.RETI.value}]({Docs.RETI})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.WILL.value} [Y|<NULL>]                      {{1:1}}  [{Tag.WILL.value}]({Docs.WILL})
  +1 {Tag.TYPE.value} <Text>                       {{0:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n {Tag.EVEN.value} <Text>                          {{1:1}}  [{Tag.INDI.value}-{Tag.EVEN.value}]({Docs.INDI_EVEN})
  +1 {Tag.TYPE.value} <Text>                       {{1:1}}  [{Tag.TYPE.value}]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
]
"""
    LDS_ORDINANCE_DETAIL: str = f"""
n <<DATE_VALUE>>                       {{:1}}
n TEMP <Text>                          {{0:1}}  [{Tag.TEMP.value}]({Docs.TEMP})
n <<PLACE_STRUCTURE>>                  {{0:1}}
n {Tag.STAT.value} <Enum>                          {{0:1}}  [ord-{Tag.STAT.value}]({Docs.ORD_STAT})
  +1 {Tag.DATE.value} <DateExact>                  {{1:1}}  [{Tag.DATE.value}-exact]({Docs.DATE_EXACT})
     +2 {Tag.TIME.value} <Time>                    {{0:1}}  [{Tag.TIME.value}]({Docs.TIME})
n <<NOTE_STRUCTURE>>                   {{0:M}}
n <<SOURCE_CITATION>>                  {{0:M}}
"""
    LDS_INDIVIDUAL_ORDINANCE: str = f"""
[
n {Tag.BAPL.value}                                 {{1:1}}  [{Tag.BAPL.value}]({Docs.BAPL})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
|
n {Tag.CONL.value}                                 {{1:1}}  [{Tag.CONL.value}]({Docs.CONL})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
|
n {Tag.ENDL.value}                                 {{1:1}}  [{Tag.ENDL.value}]({Docs.ENDL})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
|
n {Tag.INIL.value}                                 {{1:1}}  [{Tag.INIL.value}]({Docs.INIL})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
|
n {Tag.SLGC.value}                                 {{1:1}}  [{Tag.SLGC.value}]({Docs.SLGC})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
  +1 {Tag.FAMC.value} @<XREF:FAM>@                 {{1:1}}  [{Tag.FAMC.value}]({Docs.FAMC})
]
"""
    LDS_SPOUSE_SEALING = f"""
n {Tag.SLGS.value}                                 {{1:1}}  [{Tag.SLGS.value}]({Docs.SLGS})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
"""
    MULTIMEDIA: str = f"""
0 @XREF:OBJE@ {Tag.OBJE.value}                     {{1:1}}  [record-{Tag.OBJE.value}]({Docs.RECORD_OBJE})
  1 {Tag.RESN.value} <List:Enum>                   {{0:1}}  [{Tag.RESN.value}]({Docs.RESN})
  1 {Tag.FILE.value} <FilePath>                    {{1:M}}  [{Tag.FILE.value}]({Docs.FILE})
    2 {Tag.FORM.value} <MediaType>                 {{1:1}}  [{Tag.FORM.value}]({Docs.FORM})
      3 {Tag.MEDI.value} <Enum>                    {{0:1}}  [{Tag.MEDI.value}]({Docs.MEDI})
        4 {Tag.PHRASE.value} <Text>                {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
    2 {Tag.TITL.value} <Text>                      {{0:1}}  [{Tag.TITL.value}]({Docs.TITL})
    2 {Tag.TRAN.value} <FilePath>                  {{0:M}}  [{Tag.FILE.value}-{Tag.TRAN.value}]({Docs.FILE_TRAN})
      3 {Tag.FORM.value} <MediaType>               {{1:1}}  [{Tag.FORM.value}]({Docs.FORM})
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<NOTE_STRUCTURE>>                 {{0:M}}
  1 <<SOURCE_CITATION>>                {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""
    MULTIMEDIA_LINK: str = f"""
n {Tag.OBJE.value} @<XREF:OBJE>@                   {{1:1}} [{Tag.OBJE.value}]({Docs.OBJE})
  +1 {Tag.CROP.value}                              {{0:1}}  [{Tag.CROP.value}]({Docs.CROP})
    +2 {Tag.TOP.value} <Integer>                   {{0:1}}  [{Tag.TOP.value}]({Docs.TOP})
    +2 {Tag.LEFT.value} <Integer>                  {{0:1}}  [{Tag.LEFT.value}]({Docs.LEFT})
    +2 {Tag.HEIGHT.value} <Integer>                {{0:1}}  [{Tag.HEIGHT.value}]({Docs.HEIGHT})
    +2 {Tag.WIDTH.value} <Integer>                 {{0:1}}  [{Tag.WIDTH.value}]({Docs.WIDTH})
  +1 {Tag.TITL.value} <Text>                       {{0:1}}  [{Tag.TITL.value}]({Docs.TITL})
"""
    NON_EVENT_STRUCTURE: str = f"""
n {Tag.NO.value} <Enum>                            {{1:1}}  [{Tag.NO.value}]({Docs.NO})
  +1 {Tag.DATE.value} <DatePeriod>                 {{0:1}}  [{Tag.NO.value}-{Tag.DATE.value}]({Docs.NO_DATE})
     +2 {Tag.PHRASE.value} <Text>                  {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
  +1 <<SOURCE_CITATION>>               {{0:M}}
"""
    NOTE_STRUCTURE: str = f"""
[
n {Tag.NOTE.value} <Text>                          {{1:1}}  [{Tag.NOTE.value}]({Docs.NOTE})
  +1 {Tag.MIME.value} <MediaType>                  {{0:1}}  [{Tag.MIME.value}]({Docs.MIME})
  +1 {Tag.LANG.value} <Language>                   {{0:1}}  [{Tag.LANG.value}]({Docs.LANG})
  +1 {Tag.TRAN.value} <Text>                       {{0:M}}  [{Tag.NOTE.value}-{Tag.TRAN.value}]({Docs.NOTE_TRAN})
    +2 {Tag.MIME.value} <MediaType>                {{0:1}}  [{Tag.MIME.value}]({Docs.MIME})
    +2 {Tag.LANG.value} <Language>                 {{0:1}}  [{Tag.LANG.value}]({Docs.LANG})
  +1 <<SOURCE_CITATION>>               {{0:M}}
|
n {Tag.SNOTE.value} @<XREF:SNOTE>@                 {{1:1}}  [{Tag.SNOTE.value}]({Docs.SNOTE})
]
"""
    PERSONAL_NAME_PIECES: str = f"""
n {Tag.NPFX.value} <Text>                          {{0:M}}  [{Tag.NPFX.value}]({Docs.NPFX})
n {Tag.GIVN.value} <Text>                          {{0:M}}  [{Tag.GIVN.value}]({Docs.GIVN})
n {Tag.NICK.value} <Text>                          {{0:M}}  [{Tag.NICK.value}]({Docs.NICK})
n {Tag.SPFX.value} <Text>                          {{0:M}}  [{Tag.SPFX.value}]({Docs.SPFX})
n {Tag.SURN.value} <Text>                          {{0:M}}  [{Tag.SURN.value}]({Docs.SURN})
n {Tag.NSFX.value} <Text>                          {{0:M}}  [{Tag.NSFX.value}]({Docs.NSFX})
"""
    PERSONAL_NAME_STRUCTURE: str = f"""
n {Tag.NAME.value} <PersonalName>                  {{1:1}}  [{Tag.INDI.value}-{Tag.NAME.value}]({Docs.INDI_NAME})
  +1 {Tag.TYPE.value} <Enum>                       {{0:1}}  [{Tag.NAME.value}-{Tag.TYPE.value}]({Docs.NAME_TYPE})
     +2 {Tag.PHRASE.value} <Text>                  {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
  +1 <<PERSONAL_NAME_PIECES>>          {{0:1}}
  +1 {Tag.TRAN.value} <PersonalName>               {{0:M}}  [{Tag.NAME.value}-{Tag.TRAN.value}]({Docs.NAME_TRAN})
     +2 {Tag.LANG.value} <Language>                {{1:1}}  [{Tag.LANG.value}]({Docs.LANG})
     +2 <<PERSONAL_NAME_PIECES>>       {{0:1}}
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
  +1 <<SOURCE_CITATION>>               {{0:M}}
"""
    PLACE_STRUCTURE: str = f"""
n {Tag.PLAC.value} <List:Text>                     {{1:1}}   [{Tag.PLAC.value}]({Docs.PLAC})
  +1 {Tag.FORM.value} <List:Text>                  {{0:1}}   [{Tag.PLAC.value}-{Tag.FORM.value}]({Docs.PLAC_FORM})
  +1 {Tag.LANG.value} <Language>                   {{0:1}}   [{Tag.LANG.value}]({Docs.LANG})
  +1 {Tag.TRAN.value} <List:Text>                  {{0:M}}   [{Tag.PLAC.value}-{Tag.TRAN.value}]({Docs.PLAC_TRAN})
     +2 {Tag.LANG.value} <Language>                {{1:1}}   [{Tag.LANG.value}]({Docs.LANG})
  +1 {Tag.MAP.value}                               {{0:1}}   [{Tag.MAP.value}]({Docs.MAP})
     +2 {Tag.LATI.value} <Special>                 {{1:1}}   [{Tag.LATI.value}]({Docs.LATI})
     +2 {Tag.LONG.value} <Special>                 {{1:1}}   [{Tag.LONG.value}]({Docs.LONG})
  +1 {Tag.EXID.value} <Special>                    {{0:M}}   [{Tag.EXID.value}]({Docs.EXID})
     +2 {Tag.TYPE.value} <Special>                 {{0:1}}   [{Tag.EXID.value}-{Tag.TYPE.value}]({Docs.EXID_TYPE})
  +1 <<NOTE_STRUCTURE>>                {{0:M}} 
"""
    REPOSITORY: str = f"""
0 @XREF:REPO@ {Tag.REPO.value}                     {{1:1}}  [record-{Tag.REPO.value}]({Docs.RECORD_REPO})
  1 {Tag.NAME.value} <Text>                        {{1:1}}  [{Tag.NAME.value}]({Docs.NAME})
  1 <<ADDRESS_STRUCTURE>>              {{0:1}}
  1 {Tag.PHON.value} <Special>                     {{0:M}}  [{Tag.PHON.value}]({Docs.PHON})
  1 {Tag.EMAIL.value} <Special>                    {{0:M}}  [{Tag.EMAIL.value}]({Docs.EMAIL})
  1 {Tag.FAX.value} <Special>                      {{0:M}}  [{Tag.FAX.value}]({Docs.FAX})
  1 {Tag.WWW.value} <Special>                      {{0:M}}  [{Tag.WWW.value}]({Docs.WWW})
  1 <<NOTE_STRUCTURE>>                 {{0:M}}
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""
    SHARED_NOTE: str = f"""
0 @XREF:SNOTE@ {Tag.SNOTE.value} <Text>            {{1:1}}  [record-{Tag.SNOTE.value}]({Docs.RECORD_SNOTE})
  1 {Tag.MIME.value} <MediaType>                   {{0:1}}  [{Tag.MIME.value}]({Docs.MIME})
  1 {Tag.LANG.value} <Language>                    {{0:1}}  [{Tag.LANG.value}]({Docs.LANG})
  1 {Tag.TRAN.value} <Text>                        {{0:M}}  [{Tag.NOTE.value}-{Tag.TRAN.value}]({Docs.NOTE_TRAN})
    2 {Tag.MIME.value} <MediaType>                 {{0:1}}  [{Tag.MIME.value}]({Docs.MIME})
    2 {Tag.LANG.value} <Language>                  {{0:1}}  [{Tag.LANG.value}]({Docs.LANG})
  1 <<SOURCE_CITATION>>                {{0:M}}
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""
    SOURCE: str = f"""
0 @XREF:SOUR@ {Tag.SOUR.value}                     {{1:1}}  [record-{Tag.SOUR.value}]({Docs.RECORD_SOUR})
  1 {Tag.DATA.value}                               {{0:1}}  [{Tag.DATA.value}]({Docs.DATA})
    2 {Tag.EVEN.value} <List:Enum>                 {{0:M}}  [{Tag.DATA.value}-{Tag.EVEN.value}]({Docs.DATA_EVEN})
      3 {Tag.DATE.value} <DatePeriod>              {{0:1}}  [{Tag.DATA.value}-{Tag.EVEN.value}-{Tag.DATE.value}]({Docs.DATA_EVEN_DATE})
        4 {Tag.PHRASE.value} <Text>                {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
      3 <<PLACE_STRUCTURE>>            {{0:1}}
    2 {Tag.AGNC.value} <Text>                      {{0:1}}  [{Tag.AGNC.value}]({Docs.AGNC})
    2 <<NOTE_STRUCTURE>>               {{0:M}}
  1 {Tag.AUTH.value} <Text>                        {{0:1}}  [{Tag.AUTH.value}]({Docs.AUTH})
  1 {Tag.TITL.value} <Text>                        {{0:1}}  [{Tag.TITL.value}]({Docs.TITL})
  1 {Tag.ABBR.value} <Text>                        {{0:1}}  [{Tag.ABBR.value}]({Docs.ABBR})
  1 {Tag.PUBL.value} <Text>                        {{0:1}}  [{Tag.PUBL.value}]({Docs.PUBL})
  1 {Tag.TEXT.value} <Text>                        {{0:1}}  [{Tag.TEXT.value}]({Docs.TEXT})
    2 {Tag.MIME.value} <MediaType>                 {{0:1}}  [{Tag.MIME.value}]({Docs.MIME})
    2 {Tag.LANG.value} <Language>                  {{0:1}}  [{Tag.LANG.value}]({Docs.LANG})
  1 <<SOURCE_REPOSITORY_CITATION>>     {{0:M}}
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<NOTE_STRUCTURE>>                 {{0:M}}
  1 <<MULTIMEDIA_LINK>>                {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""
    SOURCE_CITATION: str = f"""
n {Tag.SOUR.value} @<XREF:SOUR>@                   {{1:1}}  [{Tag.SOUR.value}]({Docs.SOUR})
  +1 {Tag.PAGE.value} <Text>                       {{0:1}}  [{Tag.PAGE.value}]({Docs.PAGE})
  +1 {Tag.DATA.value}                              {{0:1}}  [{Tag.SOUR.value}-{Tag.DATA.value}]({Docs.SOUR_DATA})
    +2 <<DATE_VALUE>>                  {{0:1}}
    +2 {Tag.TEXT.value} <Text>                     {{0:M}}  [{Tag.TEXT.value}]({Docs.TEXT})
      +3 {Tag.MIME.value} <MediaType>              {{0:1}}  [{Tag.MIME.value}]({Docs.MIME})
      +3 {Tag.LANG.value} <Language>               {{0:1}}  [{Tag.LANG.value}]({Docs.LANG})
  +1 {Tag.EVEN.value} <Enum>                       {{0:1}}  [{Tag.SOUR.value}-{Tag.EVEN.value}]({Docs.SOUR_EVEN})
    +2 {Tag.PHRASE.value} <Text>                   {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
    +2 {Tag.ROLE.value} <Enum>                     {{0:1}}  [{Tag.ROLE.value}]({Docs.ROLE})
      +3 {Tag.PHRASE.value} <Text>                 {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
  +1 {Tag.QUAY.value} <Enum>                       {{0:1}}  [{Tag.QUAY.value}]({Docs.QUAY})
  +1 <<MULTIMEDIA_LINK>>               {{0:M}}
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
"""
    SOURCE_REPOSITORY_CITATION: str = f"""
n {Tag.REPO.value} @<XREF:REPO>@                   {{1:1}}  [{Tag.REPO.value}]({Docs.REPO})
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
  +1 {Tag.CALN.value} <Special>                    {{0:M}}  [{Tag.CALN.value}]({Docs.CALN})
     +2 {Tag.MEDI.value} <Enum>                    {{0:1}}  [{Tag.MEDI.value}]({Docs.MEDI})
        +3 {Tag.PHRASE.value} <Text>               {{0:1}}  [{Tag.PHRASE.value}]({Docs.PHRASE})
"""
    SUBMITTER: str = f"""
0 @XREF:SUBM@ {Tag.SUBM.value}                     {{1:1}}  [record-{Tag.SUBM.value}]({Docs.RECORD_SUBM})
  1 {Tag.NAME.value} <Text>                        {{1:1}}  [{Tag.NAME.value}]({Docs.NAME})
  1 <<ADDRESS_STRUCTURE>>              {{0:1}}
  1 {Tag.PHON.value} <Special>                     {{0:M}}  [{Tag.PHON.value}]({Docs.PHON})
  1 {Tag.EMAIL.value} <Special>                    {{0:M}}  [{Tag.EMAIL.value}]({Docs.EMAIL})
  1 {Tag.FAX.value} <Special>                      {{0:M}}  [{Tag.FAX.value}]({Docs.FAX})
  1 {Tag.WWW.value} <Special>                      {{0:M}}  [{Tag.WWW.value}]({Docs.WWW})
  1 <<MULTIMEDIA_LINK>>                {{0:M}}
  1 {Tag.LANG.value} <Language>                    {{0:M}}  [{Tag.SUBM.value}-{Tag.LANG.value}]({Docs.SUBM_LANG})
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<NOTE_STRUCTURE>>                 {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""


@dataclass(frozen=True)
class Specs:
    ADDRESS: str = f'{Config.SPECS}#ADDRESS_STRUCTURE'
    AGE: str = f'{Config.SPECS}#age'
    ALIAS: str = f'{Config.SPECS}#ALIA'
    ASSOCIATION: str = f'{Config.SPECS}#ASSOCIATION_STRUCTURE'
    CHANGE_DATE: str = f'{Config.SPECS}#CHANGE_DATE'
    CHILD: str = f'{Config.SPECS}#CHIL'
    CREATION_DATE: str = f'{Config.SPECS}#CREATION_DATE'
    DATE: str = f'{Config.SPECS}#date'
    DATE_VALUE: str = f'{Config.SPECS}#DATE_VALUE'
    EVENT_DETAIL: str = f'{Config.SPECS}#EVENT_DETAIL'
    EXID: str = f'{Config.SPECS}#EXID'
    EXTENSION: str = f'{Config.SPECS}#extensions'
    FAMILY: str = f'{Config.SPECS}#FAMILY_RECORD'
    FAMILY_ATTRIBUTE: str = f'{Config.SPECS}#FAMILY_ATTRIBUTE_STRUCTURE'
    FAMILY_CHILD: str = f'{Config.SPECS}#FAMC'
    FAMILY_EVENT: str = f'{Config.SPECS}#FAMILY_EVENT_STRUCTURE'
    FAMILY_EVENT_DETAIL: str = f'{Config.SPECS}#FAMILY_EVENT_DETAIL'
    FAMILY_SPOUSE: str = f'{Config.SPECS}#FAMS'
    FILE: str = ''
    FILE_TRANSLATION: str = ''
    FRENCH_R: str = f'{Config.SPECS}#FRENCH_R'
    GREGORIAN: str = f'{Config.SPECS}#GREGORIAN'
    HEADER: str = f'{Config.SPECS}#HEADER'
    HEBREW: str = f'{Config.SPECS}#HEBREW'
    HUSBAND: str = f'{Config.SPECS}#HUSB'
    IDENTIFIER: str = f'{Config.SPECS}#IDENTIFIER_STRUCTURE'
    INDIVIDUAL: str = f'{Config.SPECS}#INDIVIDUAL_RECORD'
    INDIVIDUAL_ATTRIBUTE: str = f'{Config.SPECS}#INDIVIDUAL_ATTRIBUTE_STRUCTURE'
    INDIVIDUAL_EVENT: str = f'{Config.SPECS}#INDIVIDUAL_EVENT_STRUCTURE'
    INDIVIDUAL_EVENT_DETAIL: str = f'{Config.SPECS}#INDIVIDUAL_EVENT_DETAIL'
    JULIAN: str = f'{Config.SPECS}#JULIAN'
    LDS_INDIVIDUAL_ORDINANCE: str = f'{Config.SPECS}#LDS_INDIVIDUAL_ORDINANCE'
    LDS_ORDINANCE_DETAIL: str = f'{Config.SPECS}#LDS_ORDINANCE_DETAIL'
    LDS_SPOUSE_SEALING: str = f'{Config.SPECS}#LDS_SPOUSE_SEALING'
    MAP: str = f'{Config.SPECS}#MAP'
    MULTIMEDIA: str = f'{Config.SPECS}#MULTIMEDIA_RECORD'
    MULTIMEDIA_LINK: str = f'{Config.SPECS}#MULTIMEDIA_LINK'
    NON_EVENT: str = f'{Config.SPECS}#NON_EVENT_STRUCTURE'
    NOTE: str = f'{Config.SPECS}#NOTE_STRUCTURE'
    PERSONAL_NAME: str = f'{Config.SPECS}#PERSONAL_NAME_STRUCTURE'
    PERSONAL_NAME_PIECES: str = f'{Config.SPECS}#PERSONAL_NAME_PIECES'
    PLACE: str = f'{Config.SPECS}#PLACE_STRUCTURE'
    REPOSITORY: str = f'{Config.SPECS}#REPOSITORY_RECORD'
    SCHEMA: str = f'{Config.SPECS}#SCHMA'
    SHARED_NOTE: str = f'{Config.SPECS}#SHARED_NOTE_RECORD'
    SOURCE: str = f'{Config.SPECS}#SOURCE_RECORD'
    SOURCE_EVENT: str = ''
    SOURCE_CITATION: str = f'{Config.SPECS}#SOURCE_CITATION'
    SOURCE_REPOSITORY_CITATION: str = (
        f'{Config.SPECS}#SOURCE_REPOSITORY_CITATION'
    )
    SUBMITTER: str = f'{Config.SPECS}#SUBMITTER_RECORD'
    TIME: str = f'{Config.SPECS}#time'
    WIFE: str = f'{Config.SPECS}#WIFE'


@dataclass(frozen=True)
class Default:
    AGE_DAY: str = 'd'
    AGE_MONTH: str = 'm'
    AGE_WEEK: str = 'w'
    AGE_YEAR: str = 'y'
    ATSIGN: str = '@'
    BANNED: str = r'[\u0000-\u001F\u007F\uD800-\uDFFF\uFFFE\uFFFF]'
    BRACKET_RIGHT: str = ']'
    BRACKET_LEFT: str = '['
    BRACKET_LEFT_RIGHT: str = '[]'
    CARDINALITY_ANY_NUMBER: str = ':M}'
    CARDINALITY_OPTIONAL: str = '{0:'
    CARDINALITY_REQUIRED: str = '{1:'
    CARDINALITY_SINGULAR: str = ':1}'
    COMMA: str = ','
    COMMA_REQUIRED: str = ',  # REQUIRED'
    CHOICE: int = 1
    DATE_DAY: int = 0
    DATE_MONTH: int = 0
    DATE_YEAR: int = 0
    DATE_WEEK: int = 0
    DAYS: int = 0
    EMPTY: str = ''
    EOL: str = '\n'
    EOL_DOUBLE: str = '\n\n'
    GREATER_LESS_THAN: str = '>'
    HEIGHT: int = 0
    HYPHEN: str = '-'
    INDENT: str = '    '
    KIND_STANDARD: str = 'stdTag'
    KIND_EXTENDED: str = 'extTag'
    LEFT: int = 0
    LIST_ITEM_SEPARATOR: str = ', '
    MAP_LATITUDE: float = 0.0
    MAP_LONGITUDE: float = 0.0
    MIME: str = ''
    MONTHS: int = 0
    NONE: str = 'None'
    OCCURRED: str = 'Y'
    PAYLOAD_EMPTY: str = EMPTY
    PHONE_AREA_MIN: int = 0
    PHONE_AREA_MAX: int = 1000
    PHONE_COUNTRY_MIN: int = 0
    PHONE_COUNTRY_MAX: int = 1000
    PHONE_LINE_MIN: int = 0
    PHONE_LINE_MAX: int = 10000
    PHONE_PREFIX_MIN: int = 0
    PHONE_PREFIX_MAX: int = 1000
    PHONE_STRING_SET: str = '0123456789)(+ '
    PLACE_FORM1: str = 'City'
    PLACE_FORM2: str = 'County'
    PLACE_FORM3: str = 'State'
    PLACE_FORM4: str = 'Country'
    QUOTE_SINGLE: str = "'"
    QUOTE_DOUBLE: str = '"'
    SLASH: str = '/'
    SPACE: str = ' '
    SPACE_DOUBLE: str = '  '
    T: str = 'T'
    TIME_HOUR: int = 0
    TIME_MINUTE: int = 0
    TIME_SECOND: float = 0.0
    TIME_UTC: bool = False
    TOP: int = 0
    TRAILER: str = '0 TRLR'
    UNDERLINE: str = '_'
    UTF8: str = 'utf-8'
    VOID_POINTER: str = '@VOID@'
    WEEKS: int = 0
    WIDTH: int = 0
    YAML_CALENDARS: str = 'calendars'
    YAML_CHANGE_CONTROLLER: str = 'change controller'
    YAML_CONTACT: str = 'contact'
    YAML_DIRECTIVE: str = '%YAML 1.2'
    YAML_DIRECTIVE_END_MARKER: str = '---'
    YAML_DOCUMENT_END_MARKER: str = '...'
    YAML_DOCUMENTATION: str = 'documentation'
    YAML_ENUMERATION_VALUES: str = 'enumeration values'
    YAML_EPOCHS: str = 'epochs'
    YAML_EXTENSION_TAGS: str = 'extension tags'
    YAML_FRAGMENT: str = 'fragment'
    YAML_HELP_TEXT: str = 'help text'
    YAML_LABEL: str = 'label'
    YAML_LANG: str = 'lang'
    YAML_MONTHS: str = 'months'
    YAML_PAYLOAD: str = 'payload'
    YAML_SPECIFICATION: str = 'specification'
    YAML_STANDARD_TAG: str = 'standard tag'
    YAML_SUBSTRUCTURES: str = 'substructures'
    YAML_SUPERSTRUCTURES: str = 'superstructures'
    YAML_TYPE: str = 'type'
    YAML_URI: str = 'uri'
    YAML_VALUE_OF: str = 'value of'
    YEARS: int = 0
    Z: str = 'Z'


class Even(Enum):
    """Tags used for events in general."""

    CENS = Tag.CENS.value
    ADOP = Tag.ADOP.value
    BAPM = Tag.BAPM.value
    BARM = Tag.BARM.value
    BASM = Tag.BASM.value
    BIRT = Tag.BIRT.value
    BLES = Tag.BLES.value
    BURI = Tag.BURI.value
    CHR = Tag.CHR.value
    CHRA = Tag.CHRA.value
    CONF = Tag.CONF.value
    CREM = Tag.CREM.value
    DEAT = Tag.DEAT.value
    EMIG = Tag.EMIG.value
    FCOM = Tag.FCOM.value
    GRAD = Tag.GRAD.value
    IMMI = Tag.IMMI.value
    NATU = Tag.NATU.value
    ORDN = Tag.ORDN.value
    PROB = Tag.PROB.value
    RETI = Tag.RETI.value
    WILL = Tag.WILL.value
    ANUL = Tag.ANUL.value
    DIV = Tag.DIV.value
    DIVF = Tag.DIVF.value
    ENGA = Tag.ENGA.value
    MARB = Tag.MARB.value
    MARC = Tag.MARC.value
    MARL = Tag.MARL.value
    MARR = Tag.MARR.value
    MARS = Tag.MARS.value


class FamAttr(Enum):
    """Tags used for family attributes.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM INDIEVEN]()
    """

    NCHI = Tag.NCHI.value
    RESI = Tag.RESI.value
    FACT = Tag.FACT.value
    NONE = Tag.NONE.value


class FamcStat(Enum):
    CHALLENGED = 'CHALLENGED'
    DISPROVEN = 'DISPROVEN'
    PROVEN = 'PROVEN'
    NONE = ''


class FamEven(Enum):
    """Tags used for family events.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM FAMC-EVEN](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#family-events)
    """

    ANUL = Tag.ANUL.value
    CENS = Tag.CENS.value
    DIV = Tag.DIV.value
    DIVF = Tag.DIVF.value
    ENGA = Tag.ENGA.value
    MARB = Tag.MARB.value
    MARC = Tag.MARC.value
    MARL = Tag.MARL.value
    MARR = Tag.MARR.value
    MARS = Tag.MARS.value
    EVEN = Tag.EVEN.value
    NONE = Tag.NONE.value


class Id(Enum):
    """Tags used for identifier values.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM Identifiers]()
    """

    REFN = Tag.REFN.value
    UID = Tag.UID.value
    EXID = Tag.EXID.value
    NONE = Tag.NONE.value


class IndiAttr(Enum):
    """Tags used for individual attributes.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM INDIEVEN]()
    """

    CAST = Tag.CAST.value
    DSCR = Tag.DSCR.value
    EDUC = Tag.EDUC.value
    IDNO = Tag.IDNO.value
    NATI = Tag.NATI.value
    NCHI = Tag.NCHI.value
    NMR = Tag.NMR.value
    OCCU = Tag.OCCU.value
    PROP = Tag.PROP.value
    RELI = Tag.RELI.value
    RESI = Tag.RESI.value
    SSN = Tag.SSN.value
    TITL = Tag.TITL.value
    FACT = Tag.FACT.value
    NONE = Tag.NONE.value


class IndiEven(Enum):
    """Tags used for individual events.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM INDIEVEN]()
    """

    ADOP = Tag.ADOP.value
    BAPM = Tag.BAPM.value
    BARM = Tag.BARM.value
    BASM = Tag.BASM.value
    BIRT = Tag.BIRT.value
    BLES = Tag.BLES.value
    BURI = Tag.BURI.value
    CENS = Tag.CENS.value
    CHR = Tag.CHR.value
    CHRA = Tag.CHRA.value
    CONF = Tag.CONF.value
    CREM = Tag.CREM.value
    DEAT = Tag.DEAT.value
    EMIG = Tag.EMIG.value
    FCOM = Tag.FCOM.value
    GRAD = Tag.GRAD.value
    IMMI = Tag.IMMI.value
    NATU = Tag.NATU.value
    ORDN = Tag.ORDN.value
    PROB = Tag.PROB.value
    RETI = Tag.RETI.value
    WILL = Tag.WILL.value
    EVEN = Tag.EVEN.value
    NONE = Tag.NONE.value


class PersonalNamePieceTag(Enum):
    """Tags used for Personal Name Piece lines.

    This is a subenumeration of the Tag enumeration class.

    Reference:
        [GEDCOM]()
    """

    NPFX = Tag.NPFX.value
    GIVN = Tag.GIVN.value
    NICK = Tag.NICK.value
    SPFX = Tag.SPFX.value
    SURN = Tag.SURN.value
    NSFX = Tag.NSFX.value
    NONE = Tag.NONE.value


class Record(str, Enum):
    """Tags used for Records.

    This is a subenumeration of the Tag enumeration class.

    Reference:
        [GEDCOM RECORD]()
    """

    FAM = Tag.FAM.value
    INDI = Tag.INDI.value
    OBJE = Tag.OBJE.value
    REPO = Tag.REPO.value
    SNOTE = Tag.SNOTE.value
    SOUR = Tag.SOUR.value
    SUBM = Tag.SUBM.value
    NONE = Tag.NONE.value


class Adop(Enum):
    """Implement the GEDCOM enumeration set ADOP as an enumeration class.

    Reference:
        - [GEDCOM Adop Enumeration](https://gedcom.io/terms/v7/enumset-ADOP)
    """

    HUSB = Tag.HUSB.value
    WIFE = Tag.WIFE.value
    BOTH = Tag.BOTH.value
    NONE = Tag.NONE.value


class EvenAttr(Enum):
    """Implement the GEDCOM enumeration set EVENATTR as an enumeration class.

    Reference:
        [GEDCOM EVENATTR enumeration set](https://gedcom.io/terms/v7/enumset-EVENATTR)
    """

    CENS = Tag.CENS.value
    NCHI = Tag.NCHI.value
    RESI = Tag.RESI.value
    FACT = Tag.FACT.value
    EVEN = Tag.EVEN.value
    NONE = Tag.NONE.value


class Medium(Enum):
    """Implement the GEDCOM enumeration set MEDI as an enumeration class.

    Reference:
        [GEDCOM MEDI enumeration set](https://gedcom.io/terms/v7/enumset-MEDI)
    """

    AUDIO = Tag.AUDIO.value
    BOOK = Tag.BOOK.value
    CARD = Tag.CARD.value
    ELECTRONIC = Tag.ELECTRONIC.value
    FICHE = Tag.FICHE.value
    FILM = Tag.FILM.value
    MAGAZINE = Tag.MAGAZINE.value
    MANUSCRIPT = Tag.MANUSCRIPT.value
    MAP = Tag.MAP.value
    NEWSPAPER = Tag.NEWSPAPER.value
    PHOTO = Tag.PHOTO.value
    TOMBSTONE = Tag.TOMBSTONE.value
    VIDEO = Tag.VIDEO.value
    OTHER = Tag.OTHER.value
    NONE = Tag.NONE.value


class NameType(Enum):
    """Implement the GEDCOM enumeration set NAME-TYPE as an eneration class.

    Reference:
        [GEDCOM NAME-TYPE enumeration set](https://gedcom.io/terms/v7/enumset-NAME-TYPE)
    """

    AKA = Tag.AKA.value
    BIRTH = Tag.BIRTH.value
    IMMIGRANT = Tag.IMMIGRANT.value
    MAIDEN = Tag.MAIDEN.value
    MARRIED = Tag.MARRIED.value
    PROFESSIONAL = Tag.PROFESSIONAL.value
    OTHER = Tag.OTHER.value
    NONE = Tag.NONE.value


class Pedi(Enum):
    """Implement the GEDCOM enumeration set PEDI as an enumeration class.

    Reference:
        [GEDCOM PEDI enumeration set](https://gedcom.io/terms/v7/enumset-PEDI)
    """

    ADOPTED = Tag.ADOPTED.value
    BIRTH = Tag.BIRTH.value
    FOSTER = Tag.FOSTER.value
    SEALING = Tag.SEALING.value
    OTHER = Tag.OTHER.value
    NONE = Tag.NONE.value


class Quay(Enum):
    """Implement the GEDCOM enumeration set QUAY as an enumeration class.

    Reference:
        [GEDCOM QUAY enumeration set](https://gedcom.io/terms/v7/enumset-QUAY)
    """

    QUAY0 = Tag.QUAY0.value
    QUAY1 = Tag.QUAY1.value
    QUAY2 = Tag.QUAY2.value
    QUAY3 = Tag.QUAY3.value
    NONE = Tag.NONE.value


class Resn(Enum):
    """Implement the GEDCOM enumeration set RESN as an enumeration class.

    Reference:
        [GEDCOM RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
    """

    CONFIDENTIAL = Tag.CONFIDENTIAL.value
    LOCKED = Tag.LOCKED.value
    PRIVACY = Tag.PRIVACY.value
    NONE = Tag.NONE.value


class Role(Enum):
    """Implement the GEDCOM enumeration set ROLE as an enumeration class.

    Reference:
        [GEDCOM ROLE enumeration set](https://gedcom.io/terms/v7/enumset-ROLE)
    """

    CHIL = Tag.CHIL.value
    CLERGY = Tag.CLERGY.value
    FATH = Tag.FATH.value
    FRIEND = Tag.FRIEND.value
    GODP = Tag.GODP.value
    HUSB = Tag.HUSB.value
    MOTH = Tag.MOTH.value
    MULTIPLE = Tag.MULTIPLE.value
    NGHBR = Tag.NGHBR.value
    OFFICIATOR = Tag.OFFICIATOR.value
    PARENT = Tag.PARENT.value
    SPOU = Tag.SPOU.value
    WIFE = Tag.WIFE.value
    WITN = Tag.WITN.value
    OTHER = Tag.OTHER.value
    NONE = Tag.NONE.value


class Sex(Enum):
    """Implement the GEDCOM SEX enumeration set as an enumeration class.

    Reference:
        [GEDCOM SEX enumeration set]()
    """

    M = Tag.M.value
    F = Tag.F.value
    X = Tag.X.value
    U = Tag.U.value
    NONE = Tag.NONE.value


class Stat(Enum):
    """Implement the GEDCOM enumeration set ord-STAT as an enumeration class.

    Reference:
        [GEDCOM ord-STAT enumeration set](https://gedcom.io/terms/v7/enumset-ord-STAT)
    """

    BIC = Tag.BIC.value
    CANCELED = Tag.CANCELED.value
    CHILD = Tag.CHILD.value
    COMPLETED = Tag.COMPLETED.value
    EXCLUDED = Tag.EXCLUDED.value
    DNS = Tag.DNS.value
    DNS_CAN = Tag.DNS_CAN.value
    INFANT = Tag.INFANT.value
    PRE_1970 = Tag.PRE_1970.value
    STILLBORN = Tag.STILLBORN.value
    SUBMITTED = Tag.SUBMITTED.value
    UNCLEARED = Tag.UNCLEARED.value
    NONE = Tag.NONE.value


class TagTuple(NamedTuple):
    """Store standard and extension tag information."""

    value: str = Default.EMPTY
    kind: str = Default.KIND_STANDARD
    supers: list[str] | None = None
    subs: list[str] | None = None
    required: list[str] | None = None
    single: list[str] | None = None
    enumsets: list[str] | None = None
    lang: str = Default.EMPTY
    type: str = Default.EMPTY
    uri: str = Default.EMPTY
    fragment: str = Default.EMPTY
    standard_tag: str = Default.EMPTY
    extension_tags: list[str] | None = None
    specification: str = Default.EMPTY
    label: str | None = None
    help_text: str | None = None
    documentation: list[str] | None = None
    payload: str = Default.EMPTY
    substructures: dict[str, str] | None = None
    superstructures: dict[str, str] | None = None
    enumeration_values: list[str] | None = None
    value_of: dict[str, str] = {}  # noqa: RUF012
    calendars: list[str] | None = None
    months: list[str] | None = None
    epochs: list[str] | None = None
    contact: str = Default.EMPTY
    change_controller: str = Default.EMPTY
    yamldict: dict[str, Any] | None = None

    def show(self) -> str:
        return f"{self.value} = TagTuple(value='{self.value}', supers={self.supers}, subs={self.subs}, required={self.required}, single={self.single}, enumsets={self.enumsets})"
    
    def code(self) -> str:
        return f"""
TagTuple(
  value = {self.value},
  kind = {self.kind},
  supers = {self.supers},
  subs = {self.subs},
  required = {self.required},
  single = {self.single},
  enumsets = {self.enumsets},
  lang = '{self.lang}',
  type = '{self.type}',
  uri = '{self.uri}',
  fragment = '{self.fragment}',
  standard_tag = '{self.standard_tag}',
  extension_tags = {self.extension_tags},
  specification = '{self.specification}',
  label = {self.label},
  help_text = {self.help_text},
  documentation = {self.documentation},
  payload = '{self.payload}',
  substructures = {self.substructures},
  superstructures = {self.superstructures},
  enumeration_values = {self.enumeration_values},
  value_of = {self.value_of},
  calendars = {self.calendars},
  months = {self.months},
  epochs = {self.epochs},
  contact = '{self.contact}',
  change_controller = '{self.change_controller}',
  yamldict = {self.yamldict},
)
"""


class StdTag(Enum):
    """Generated definitions based on the enumeration class `Tag` and used to check extensions.

    When a new version of the GEDCOM standard `genedata.store.TagYaml.generate` should be rerun
    in a Notebook cell.  Copy the definitions into this class.
    """

    ABBR = TagTuple(value='ABBR', supers=['record-SOUR'], subs=[], required=[], single=[], enumsets=[])
    ADDR = TagTuple(value='ADDR', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CORP', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL', 'record-REPO', 'record-SUBM'], subs=['ADR1', 'ADR2', 'ADR3', 'CITY', 'CTRY', 'POST', 'STAE'], required=[], single=['ADR1', 'ADR2', 'ADR3', 'CITY', 'CTRY', 'POST', 'STAE'], enumsets=[])
    ADOP = TagTuple(value='ADOP', supers=['record-INDI'], subs=['ADDR', 'ADOP-FAMC', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'ADOP-FAMC', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    ADR1 = TagTuple(value='ADR1', supers=['ADDR'], subs=[], required=[], single=[], enumsets=[])
    ADR2 = TagTuple(value='ADR2', supers=['ADDR'], subs=[], required=[], single=[], enumsets=[])
    ADR3 = TagTuple(value='ADR3', supers=['ADDR'], subs=[], required=[], single=[], enumsets=[])
    AGE = TagTuple(value='AGE', supers=['ADOP', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CREM', 'DEAT', 'DSCR', 'EDUC', 'EMIG', 'FCOM', 'GRAD', 'HUSB', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WIFE', 'WILL'], subs=['PHRASE'], required=[], single=['PHRASE'], enumsets=[])
    AGNC = TagTuple(value='AGNC', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CREM', 'DATA', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL'], subs=[], required=[], single=[], enumsets=[])
    ALIA = TagTuple(value='ALIA', supers=['record-INDI'], subs=['PHRASE'], required=[], single=['PHRASE'], enumsets=[])
    ANCI = TagTuple(value='ANCI', supers=['record-INDI'], subs=[], required=[], single=[], enumsets=[])
    ANUL = TagTuple(value='ANUL', supers=['record-FAM'], subs=['ADDR', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'HUSB', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WIFE', 'WWW'], required=[], single=['ADDR', 'AGNC', 'CAUS', 'DATE', 'HUSB', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE', 'WIFE'], enumsets=['EVEN', 'EVENATTR'])
    ASSO = TagTuple(value='ASSO', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL', 'record-FAM', 'record-INDI'], subs=['NOTE', 'PHRASE', 'ROLE', 'SNOTE', 'SOUR'], required=['ROLE'], single=['PHRASE', 'ROLE'], enumsets=[])
    AUTH = TagTuple(value='AUTH', supers=['record-SOUR'], subs=[], required=[], single=[], enumsets=[])
    BAPL = TagTuple(value='BAPL', supers=['record-INDI'], subs=['DATE', 'NOTE', 'PLAC', 'SNOTE', 'SOUR', 'TEMP', 'ord-STAT'], required=[], single=['DATE', 'PLAC', 'TEMP', 'ord-STAT'], enumsets=[])
    BAPM = TagTuple(value='BAPM', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    BARM = TagTuple(value='BARM', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    BASM = TagTuple(value='BASM', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    BIRT = TagTuple(value='BIRT', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAMC', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'FAMC', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    BLES = TagTuple(value='BLES', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    BURI = TagTuple(value='BURI', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    CALN = TagTuple(value='CALN', supers=['REPO'], subs=['MEDI'], required=[], single=['MEDI'], enumsets=[])
    CAST = TagTuple(value='CAST', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVENATTR'])
    CAUS = TagTuple(value='CAUS', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL'], subs=[], required=[], single=[], enumsets=[])
    CHAN = TagTuple(value='CHAN', supers=['record-FAM', 'record-INDI', 'record-OBJE', 'record-REPO', 'record-SNOTE', 'record-SOUR', 'record-SUBM'], subs=['DATE-exact', 'NOTE', 'SNOTE'], required=['DATE-exact'], single=['DATE-exact'], enumsets=[])
    CHIL = TagTuple(value='CHIL', supers=['record-FAM'], subs=['PHRASE'], required=[], single=['PHRASE'], enumsets=[])
    CHR = TagTuple(value='CHR', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAMC', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'FAMC', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    CHRA = TagTuple(value='CHRA', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    CITY = TagTuple(value='CITY', supers=['ADDR'], subs=[], required=[], single=[], enumsets=[])
    CONF = TagTuple(value='CONF', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    CONL = TagTuple(value='CONL', supers=['record-INDI'], subs=['DATE', 'NOTE', 'PLAC', 'SNOTE', 'SOUR', 'TEMP', 'ord-STAT'], required=[], single=['DATE', 'PLAC', 'TEMP', 'ord-STAT'], enumsets=[])
    CONT = TagTuple(value='CONT', supers=[], subs=[], required=[], single=[], enumsets=[])
    COPR = TagTuple(value='COPR', supers=['HEAD', 'HEAD-SOUR-DATA'], subs=[], required=[], single=[], enumsets=[])
    CORP = TagTuple(value='CORP', supers=['HEAD-SOUR'], subs=['ADDR', 'EMAIL', 'FAX', 'PHON', 'WWW'], required=[], single=['ADDR'], enumsets=[])
    CREA = TagTuple(value='CREA', supers=['record-FAM', 'record-INDI', 'record-OBJE', 'record-REPO', 'record-SNOTE', 'record-SOUR', 'record-SUBM'], subs=['DATE-exact'], required=['DATE-exact'], single=['DATE-exact'], enumsets=[])
    CREM = TagTuple(value='CREM', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    CROP = TagTuple(value='CROP', supers=['OBJE'], subs=['HEIGHT', 'LEFT', 'TOP', 'WIDTH'], required=[], single=['HEIGHT', 'LEFT', 'TOP', 'WIDTH'], enumsets=[])
    CTRY = TagTuple(value='CTRY', supers=['ADDR'], subs=[], required=[], single=[], enumsets=[])
    DATA = TagTuple(value='DATA', supers=['record-SOUR'], subs=['AGNC', 'DATA-EVEN', 'NOTE', 'SNOTE'], required=[], single=['AGNC'], enumsets=[])
    DATE = TagTuple(value='DATE', supers=['ADOP', 'ANUL', 'BAPL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CONL', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENDL', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'INIL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SLGC', 'SLGS', 'SOUR-DATA', 'SSN', 'WILL'], subs=['PHRASE', 'TIME'], required=[], single=['PHRASE', 'TIME'], enumsets=[])
    DEAT = TagTuple(value='DEAT', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    DESI = TagTuple(value='DESI', supers=['record-INDI'], subs=[], required=[], single=[], enumsets=[])
    DEST = TagTuple(value='DEST', supers=['HEAD'], subs=[], required=[], single=[], enumsets=[])
    DIV = TagTuple(value='DIV', supers=['record-FAM'], subs=['ADDR', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'HUSB', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WIFE', 'WWW'], required=[], single=['ADDR', 'AGNC', 'CAUS', 'DATE', 'HUSB', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE', 'WIFE'], enumsets=['EVEN', 'EVENATTR'])
    DIVF = TagTuple(value='DIVF', supers=['record-FAM'], subs=['ADDR', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'HUSB', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WIFE', 'WWW'], required=[], single=['ADDR', 'AGNC', 'CAUS', 'DATE', 'HUSB', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE', 'WIFE'], enumsets=['EVEN', 'EVENATTR'])
    DSCR = TagTuple(value='DSCR', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVENATTR'])
    EDUC = TagTuple(value='EDUC', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVENATTR'])
    EMAIL = TagTuple(value='EMAIL', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CORP', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL', 'record-REPO', 'record-SUBM'], subs=[], required=[], single=[], enumsets=[])
    EMIG = TagTuple(value='EMIG', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    ENDL = TagTuple(value='ENDL', supers=['record-INDI'], subs=['DATE', 'NOTE', 'PLAC', 'SNOTE', 'SOUR', 'TEMP', 'ord-STAT'], required=[], single=['DATE', 'PLAC', 'TEMP', 'ord-STAT'], enumsets=[])
    ENGA = TagTuple(value='ENGA', supers=['record-FAM'], subs=['ADDR', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'HUSB', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WIFE', 'WWW'], required=[], single=['ADDR', 'AGNC', 'CAUS', 'DATE', 'HUSB', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE', 'WIFE'], enumsets=['EVEN', 'EVENATTR'])
    EXID = TagTuple(value='EXID', supers=['PLAC', 'record-FAM', 'record-INDI', 'record-OBJE', 'record-REPO', 'record-SNOTE', 'record-SOUR', 'record-SUBM'], subs=['EXID-TYPE'], required=[], single=['EXID-TYPE'], enumsets=[])
    FAMC = TagTuple(value='FAMC', supers=['BIRT', 'CHR', 'SLGC'], subs=[], required=[], single=[], enumsets=[])
    FAMS = TagTuple(value='FAMS', supers=['record-INDI'], subs=['NOTE', 'SNOTE'], required=[], single=[], enumsets=[])
    FAX = TagTuple(value='FAX', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CORP', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL', 'record-REPO', 'record-SUBM'], subs=[], required=[], single=[], enumsets=[])
    FCOM = TagTuple(value='FCOM', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    FILE = TagTuple(value='FILE', supers=['record-OBJE'], subs=['FILE-TRAN', 'FORM', 'TITL'], required=['FORM'], single=['FORM', 'TITL'], enumsets=[])
    FORM = TagTuple(value='FORM', supers=['FILE', 'FILE-TRAN'], subs=['MEDI'], required=[], single=['MEDI'], enumsets=[])
    GEDC = TagTuple(value='GEDC', supers=['HEAD'], subs=['GEDC-VERS'], required=['GEDC-VERS'], single=['GEDC-VERS'], enumsets=[])
    GIVN = TagTuple(value='GIVN', supers=['INDI-NAME', 'NAME-TRAN'], subs=[], required=[], single=[], enumsets=[])
    GRAD = TagTuple(value='GRAD', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    HEAD = TagTuple(value='HEAD', supers=[], subs=['COPR', 'DEST', 'GEDC', 'HEAD-DATE', 'HEAD-LANG', 'HEAD-PLAC', 'HEAD-SOUR', 'NOTE', 'SCHMA', 'SNOTE', 'SUBM'], required=['GEDC'], single=['COPR', 'DEST', 'GEDC', 'HEAD-DATE', 'HEAD-LANG', 'HEAD-PLAC', 'HEAD-SOUR', 'NOTE', 'SCHMA', 'SNOTE', 'SUBM'], enumsets=[])
    HEIGHT = TagTuple(value='HEIGHT', supers=['CROP'], subs=[], required=[], single=[], enumsets=[])
    HUSB = TagTuple(value='HUSB', supers=['ANUL', 'DIV', 'DIVF', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS'], subs=['AGE'], required=['AGE'], single=['AGE'], enumsets=[])
    IDNO = TagTuple(value='IDNO', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=['TYPE'], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVENATTR'])
    IMMI = TagTuple(value='IMMI', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    INIL = TagTuple(value='INIL', supers=['record-INDI'], subs=['DATE', 'NOTE', 'PLAC', 'SNOTE', 'SOUR', 'TEMP', 'ord-STAT'], required=[], single=['DATE', 'PLAC', 'TEMP', 'ord-STAT'], enumsets=[])
    LANG = TagTuple(value='LANG', supers=['NAME-TRAN', 'NOTE', 'NOTE-TRAN', 'PLAC', 'PLAC-TRAN', 'TEXT', 'record-SNOTE'], subs=[], required=[], single=[], enumsets=[])
    LATI = TagTuple(value='LATI', supers=['MAP'], subs=[], required=[], single=[], enumsets=[])
    LEFT = TagTuple(value='LEFT', supers=['CROP'], subs=[], required=[], single=[], enumsets=[])
    LONG = TagTuple(value='LONG', supers=['MAP'], subs=[], required=[], single=[], enumsets=[])
    MAP = TagTuple(value='MAP', supers=['PLAC'], subs=['LATI', 'LONG'], required=['LATI', 'LONG'], single=['LATI', 'LONG'], enumsets=[])
    MARB = TagTuple(value='MARB', supers=['record-FAM'], subs=['ADDR', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'HUSB', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WIFE', 'WWW'], required=[], single=['ADDR', 'AGNC', 'CAUS', 'DATE', 'HUSB', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE', 'WIFE'], enumsets=['EVEN', 'EVENATTR'])
    MARC = TagTuple(value='MARC', supers=['record-FAM'], subs=['ADDR', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'HUSB', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WIFE', 'WWW'], required=[], single=['ADDR', 'AGNC', 'CAUS', 'DATE', 'HUSB', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE', 'WIFE'], enumsets=['EVEN', 'EVENATTR'])
    MARL = TagTuple(value='MARL', supers=['record-FAM'], subs=['ADDR', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'HUSB', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WIFE', 'WWW'], required=[], single=['ADDR', 'AGNC', 'CAUS', 'DATE', 'HUSB', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE', 'WIFE'], enumsets=['EVEN', 'EVENATTR'])
    MARR = TagTuple(value='MARR', supers=['record-FAM'], subs=['ADDR', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'HUSB', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WIFE', 'WWW'], required=[], single=['ADDR', 'AGNC', 'CAUS', 'DATE', 'HUSB', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE', 'WIFE'], enumsets=['EVEN', 'EVENATTR'])
    MARS = TagTuple(value='MARS', supers=['record-FAM'], subs=['ADDR', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'HUSB', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WIFE', 'WWW'], required=[], single=['ADDR', 'AGNC', 'CAUS', 'DATE', 'HUSB', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE', 'WIFE'], enumsets=['EVEN', 'EVENATTR'])
    MEDI = TagTuple(value='MEDI', supers=['CALN', 'FORM'], subs=['PHRASE'], required=[], single=['PHRASE'], enumsets=[])
    MIME = TagTuple(value='MIME', supers=[], subs=[], required=[], single=[], enumsets=[])
    NAME = TagTuple(value='NAME', supers=['HEAD-SOUR', 'record-REPO', 'record-SUBM'], subs=[], required=[], single=[], enumsets=[])
    NATI = TagTuple(value='NATI', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVENATTR'])
    NATU = TagTuple(value='NATU', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    NICK = TagTuple(value='NICK', supers=['INDI-NAME', 'NAME-TRAN'], subs=[], required=[], single=[], enumsets=[])
    NMR = TagTuple(value='NMR', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVENATTR'])
    NO = TagTuple(value='NO', supers=['record-FAM', 'record-INDI'], subs=['NO-DATE', 'NOTE', 'SNOTE', 'SOUR'], required=[], single=['NO-DATE'], enumsets=[])
    NOTE = TagTuple(value='NOTE', supers=['ADOP', 'ANUL', 'ASSO', 'BAPL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHAN', 'CHR', 'CHRA', 'CONF', 'CONL', 'CREM', 'DATA', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENDL', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FAMS', 'FCOM', 'GRAD', 'HEAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-FAMC', 'INDI-NAME', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'INIL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'NO', 'OCCU', 'ORDN', 'PLAC', 'PROB', 'PROP', 'REPO', 'RETI', 'SLGC', 'SLGS', 'SOUR', 'SSN', 'WILL', 'record-FAM', 'record-INDI', 'record-OBJE', 'record-REPO', 'record-SOUR', 'record-SUBM'], subs=['LANG', 'MIME', 'NOTE-TRAN', 'SOUR'], required=[], single=['LANG', 'MIME'], enumsets=[])
    NPFX = TagTuple(value='NPFX', supers=['INDI-NAME', 'NAME-TRAN'], subs=[], required=[], single=[], enumsets=[])
    NSFX = TagTuple(value='NSFX', supers=['INDI-NAME', 'NAME-TRAN'], subs=[], required=[], single=[], enumsets=[])
    OBJE = TagTuple(value='OBJE', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SOUR', 'SSN', 'WILL', 'record-FAM', 'record-INDI', 'record-SOUR', 'record-SUBM'], subs=['CROP', 'TITL'], required=[], single=['CROP', 'TITL'], enumsets=[])
    OCCU = TagTuple(value='OCCU', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVENATTR'])
    ORDN = TagTuple(value='ORDN', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    PAGE = TagTuple(value='PAGE', supers=['SOUR'], subs=[], required=[], single=[], enumsets=[])
    PEDI = TagTuple(value='PEDI', supers=['INDI-FAMC'], subs=['PHRASE'], required=[], single=['PHRASE'], enumsets=[])
    PHON = TagTuple(value='PHON', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CORP', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL', 'record-REPO', 'record-SUBM'], subs=[], required=[], single=[], enumsets=[])
    PHRASE = TagTuple(value='PHRASE', supers=['AGE', 'ALIA', 'ASSO', 'CHIL', 'DATA-EVEN-DATE', 'DATE', 'FAM-HUSB', 'FAM-WIFE', 'FAMC-ADOP', 'FAMC-STAT', 'MEDI', 'NAME-TYPE', 'NO-DATE', 'PEDI', 'ROLE', 'SDATE', 'SOUR-EVEN'], subs=[], required=[], single=[], enumsets=[])
    PLAC = TagTuple(value='PLAC', supers=['ADOP', 'ANUL', 'BAPL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CONL', 'CREM', 'DATA-EVEN', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENDL', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'INIL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SLGC', 'SLGS', 'SSN', 'WILL'], subs=['EXID', 'LANG', 'MAP', 'NOTE', 'PLAC-FORM', 'PLAC-TRAN', 'SNOTE'], required=[], single=['LANG', 'MAP', 'PLAC-FORM'], enumsets=[])
    POST = TagTuple(value='POST', supers=['ADDR'], subs=[], required=[], single=[], enumsets=[])
    PROB = TagTuple(value='PROB', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    PROP = TagTuple(value='PROP', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVENATTR'])
    PUBL = TagTuple(value='PUBL', supers=['record-SOUR'], subs=[], required=[], single=[], enumsets=[])
    QUAY = TagTuple(value='QUAY', supers=['SOUR'], subs=[], required=[], single=[], enumsets=[])
    REFN = TagTuple(value='REFN', supers=['record-FAM', 'record-INDI', 'record-OBJE', 'record-REPO', 'record-SNOTE', 'record-SOUR', 'record-SUBM'], subs=['TYPE'], required=[], single=['TYPE'], enumsets=[])
    RELI = TagTuple(value='RELI', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL'], subs=[], required=[], single=[], enumsets=['EVENATTR'])
    REPO = TagTuple(value='REPO', supers=['record-SOUR'], subs=['CALN', 'NOTE', 'SNOTE'], required=[], single=[], enumsets=[])
    RESN = TagTuple(value='RESN', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL', 'record-FAM', 'record-INDI', 'record-OBJE'], subs=[], required=[], single=[], enumsets=[])
    RETI = TagTuple(value='RETI', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    ROLE = TagTuple(value='ROLE', supers=['ASSO', 'SOUR-EVEN'], subs=['PHRASE'], required=[], single=['PHRASE'], enumsets=[])
    SCHMA = TagTuple(value='SCHMA', supers=['HEAD'], subs=['TAG'], required=[], single=[], enumsets=[])
    SDATE = TagTuple(value='SDATE', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL'], subs=['PHRASE', 'TIME'], required=[], single=['PHRASE', 'TIME'], enumsets=[])
    SEX = TagTuple(value='SEX', supers=['record-INDI'], subs=[], required=[], single=[], enumsets=[])
    SLGC = TagTuple(value='SLGC', supers=['record-INDI'], subs=['DATE', 'FAMC', 'NOTE', 'PLAC', 'SNOTE', 'SOUR', 'TEMP', 'ord-STAT'], required=['FAMC'], single=['DATE', 'FAMC', 'PLAC', 'TEMP', 'ord-STAT'], enumsets=[])
    SLGS = TagTuple(value='SLGS', supers=['record-FAM'], subs=['DATE', 'NOTE', 'PLAC', 'SNOTE', 'SOUR', 'TEMP', 'ord-STAT'], required=[], single=['DATE', 'PLAC', 'TEMP', 'ord-STAT'], enumsets=[])
    SNOTE = TagTuple(value='SNOTE', supers=['ADOP', 'ANUL', 'ASSO', 'BAPL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHAN', 'CHR', 'CHRA', 'CONF', 'CONL', 'CREM', 'DATA', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENDL', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FAMS', 'FCOM', 'GRAD', 'HEAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-FAMC', 'INDI-NAME', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'INIL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'NO', 'OCCU', 'ORDN', 'PLAC', 'PROB', 'PROP', 'REPO', 'RETI', 'SLGC', 'SLGS', 'SOUR', 'SSN', 'WILL', 'record-FAM', 'record-INDI', 'record-OBJE', 'record-REPO', 'record-SOUR', 'record-SUBM'], subs=[], required=[], single=[], enumsets=[])
    SOUR = TagTuple(value='SOUR', supers=['ADOP', 'ANUL', 'ASSO', 'BAPL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CONL', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENDL', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NAME', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'INIL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'NO', 'NOTE', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SLGC', 'SLGS', 'SSN', 'WILL', 'record-FAM', 'record-INDI', 'record-OBJE', 'record-SNOTE'], subs=['NOTE', 'OBJE', 'PAGE', 'QUAY', 'SNOTE', 'SOUR-DATA', 'SOUR-EVEN'], required=[], single=['PAGE', 'QUAY', 'SOUR-DATA', 'SOUR-EVEN'], enumsets=[])
    SPFX = TagTuple(value='SPFX', supers=['INDI-NAME', 'NAME-TRAN'], subs=[], required=[], single=[], enumsets=[])
    SSN = TagTuple(value='SSN', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVENATTR'])
    STAE = TagTuple(value='STAE', supers=['ADDR'], subs=[], required=[], single=[], enumsets=[])
    SUBM = TagTuple(value='SUBM', supers=['HEAD', 'record-FAM', 'record-INDI'], subs=[], required=[], single=[], enumsets=[])
    SURN = TagTuple(value='SURN', supers=['INDI-NAME', 'NAME-TRAN'], subs=[], required=[], single=[], enumsets=[])
    TAG = TagTuple(value='TAG', supers=['SCHMA'], subs=[], required=[], single=[], enumsets=[])
    TEMP = TagTuple(value='TEMP', supers=['BAPL', 'CONL', 'ENDL', 'INIL', 'SLGC', 'SLGS'], subs=[], required=[], single=[], enumsets=[])
    TEXT = TagTuple(value='TEXT', supers=['SOUR-DATA', 'record-SOUR'], subs=['LANG', 'MIME'], required=[], single=['LANG', 'MIME'], enumsets=[])
    TIME = TagTuple(value='TIME', supers=['DATE', 'DATE-exact', 'HEAD-DATE', 'SDATE'], subs=[], required=[], single=[], enumsets=[])
    TITL = TagTuple(value='TITL', supers=['FILE', 'OBJE', 'record-SOUR'], subs=[], required=[], single=[], enumsets=['EVENATTR'])
    TOP = TagTuple(value='TOP', supers=['CROP'], subs=[], required=[], single=[], enumsets=[])
    TRLR = TagTuple(value='TRLR', supers=[], subs=[], required=[], single=[], enumsets=[])
    TYPE = TagTuple(value='TYPE', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'REFN', 'RETI', 'SSN', 'WILL'], subs=[], required=[], single=[], enumsets=[])
    UID = TagTuple(value='UID', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL', 'record-FAM', 'record-INDI', 'record-OBJE', 'record-REPO', 'record-SNOTE', 'record-SOUR', 'record-SUBM'], subs=[], required=[], single=[], enumsets=[])
    VERS = TagTuple(value='VERS', supers=['HEAD-SOUR'], subs=[], required=[], single=[], enumsets=[])
    WIDTH = TagTuple(value='WIDTH', supers=['CROP'], subs=[], required=[], single=[], enumsets=[])
    WIFE = TagTuple(value='WIFE', supers=['ANUL', 'DIV', 'DIVF', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS'], subs=['AGE'], required=['AGE'], single=['AGE'], enumsets=[])
    WILL = TagTuple(value='WILL', supers=['record-INDI'], subs=['ADDR', 'AGE', 'AGNC', 'ASSO', 'CAUS', 'DATE', 'EMAIL', 'FAX', 'NOTE', 'OBJE', 'PHON', 'PLAC', 'RELI', 'RESN', 'SDATE', 'SNOTE', 'SOUR', 'TYPE', 'UID', 'WWW'], required=[], single=['ADDR', 'AGE', 'AGNC', 'CAUS', 'DATE', 'PLAC', 'RELI', 'RESN', 'SDATE', 'TYPE'], enumsets=['EVEN', 'EVENATTR'])
    WWW = TagTuple(value='WWW', supers=['ADOP', 'ANUL', 'BAPM', 'BARM', 'BASM', 'BIRT', 'BLES', 'BURI', 'CAST', 'CHR', 'CHRA', 'CONF', 'CORP', 'CREM', 'DEAT', 'DIV', 'DIVF', 'DSCR', 'EDUC', 'EMIG', 'ENGA', 'FAM-CENS', 'FAM-EVEN', 'FAM-FACT', 'FAM-NCHI', 'FAM-RESI', 'FCOM', 'GRAD', 'IDNO', 'IMMI', 'INDI-CENS', 'INDI-EVEN', 'INDI-FACT', 'INDI-NCHI', 'INDI-RELI', 'INDI-RESI', 'INDI-TITL', 'MARB', 'MARC', 'MARL', 'MARR', 'MARS', 'NATI', 'NATU', 'NMR', 'OCCU', 'ORDN', 'PROB', 'PROP', 'RETI', 'SSN', 'WILL', 'record-REPO', 'record-SUBM'], subs=[], required=[], single=[], enumsets=[])