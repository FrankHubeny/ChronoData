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
    'AdopEnum',
    'EvenAttrEnum',
    'EvenEnum',
    'FamAttrEnum',
    'FamEvenEnum',
    'FamcStatEnum',
    'IdEnum',
    'IndiAttrEnum',
    'IndiEvenEnum',
    'MediumEnum',
    'NameTypeEnum',
    'OverView',
    'PediEnum',
    'PersonalNamePieceTag',
    'QuayEnum',
    'Record',
    'ResnEnum',
    'RoleEnum',
    'SexEnum',
    'Specs',
    'StatEnum',
    'StdTag',
    'Tag',
    'Terms',
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
    LATI_DEFAULT: float = 0.0
    LATI_HIGH: float = 90.0
    LATI_LOW: float = -90.0
    LATI_NORTH: str = 'N'
    LATI_PRECISION: str = '.6f'
    LATI_SOUTH: str = 'S'
    LEFT: int = 0
    LIST_ITEM_SEPARATOR: str = ', '
    LONG_DEFAULT: float = 0.0
    LONG_EAST: str = 'E'
    LONG_HIGH: float = 180.0
    LONG_LOW: float = -180.0
    LONG_PRECISION: str = '.6f'
    LONG_WEST: str = 'W'
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


class EvenEnum(Enum):
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
    NONE = Tag.NONE.value


class FamAttrEnum(Enum):
    """Tags used for family attributes.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM INDIEVEN]()
    """

    NCHI = Tag.NCHI.value
    RESI = Tag.RESI.value
    FACT = Tag.FACT.value
    NONE = Tag.NONE.value


class FamcStatEnum(Enum):
    CHALLENGED = 'CHALLENGED'
    DISPROVEN = 'DISPROVEN'
    PROVEN = 'PROVEN'
    NONE = Tag.NONE.value


class FamEvenEnum(Enum):
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


class IdEnum(Enum):
    """Tags used for identifier values.

    This is a sub-enumeration of the Tag enumeration class.

    Reference:
        [GEDCOM Identifiers]()
    """

    REFN = Tag.REFN.value
    UID = Tag.UID.value
    EXID = Tag.EXID.value
    NONE = Tag.NONE.value


class IndiAttrEnum(Enum):
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


class IndiEvenEnum(Enum):
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


class AdopEnum(Enum):
    """Implement the GEDCOM enumeration set ADOP as an enumeration class.

    Reference:
        - [GEDCOM Adop Enumeration](https://gedcom.io/terms/v7/enumset-ADOP)
    """

    HUSB = Tag.HUSB.value
    WIFE = Tag.WIFE.value
    BOTH = Tag.BOTH.value
    NONE = Tag.NONE.value


class EvenAttrEnum(Enum):
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
    ADOP = Tag.ADOP
    BAPM = Tag.BAPM
    BARM = Tag.BARM
    BASM = Tag.BASM
    BIRT = Tag.BIRT
    BLES = Tag.BLES
    BURI = Tag.BURI
    CHR = Tag.CHR
    CHRA = Tag.CHRA
    CONF = Tag.CONF
    CREM = Tag.CREM
    DEAT = Tag.DEAT
    EMIG = Tag.EMIG
    FCOM = Tag.FCOM
    GRAD = Tag.GRAD
    IMMI = Tag.IMMI
    NATU = Tag.NATU
    ORDN = Tag.ORDN
    PROB = Tag.PROB
    RETI = Tag.RETI
    WILL = Tag.WILL
    ANUL = Tag.ANUL
    DIV = Tag.DIV
    DIVF = Tag.DIVF
    ENGA = Tag.ENGA
    MARB = Tag.MARB
    MARC = Tag.MARC
    MARL = Tag.MARL
    MARR = Tag.MARR
    MARS = Tag.MARS
    CAST = Tag.CAST
    DSCR = Tag.DSCR
    EDUC = Tag.EDUC
    IDNO = Tag.IDNO
    NATI = Tag.NATI
    NMR = Tag.NMR
    OCCU = Tag.OCCU
    PROP = Tag.PROP
    RELI = Tag.RELI
    SSN = Tag.SSN
    TITL = Tag.TITL


class MediumEnum(Enum):
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


class NameTypeEnum(Enum):
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


class PediEnum(Enum):
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


class QuayEnum(Enum):
    """Implement the GEDCOM enumeration set QUAY as an enumeration class.

    Reference:
        [GEDCOM QUAY enumeration set](https://gedcom.io/terms/v7/enumset-QUAY)
    """

    QUAY0 = Tag.QUAY0.value
    QUAY1 = Tag.QUAY1.value
    QUAY2 = Tag.QUAY2.value
    QUAY3 = Tag.QUAY3.value
    NONE = Tag.NONE.value


class ResnEnum(Enum):
    """Implement the GEDCOM enumeration set RESN as an enumeration class.

    Reference:
        [GEDCOM RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
    """

    CONFIDENTIAL = Tag.CONFIDENTIAL.value
    LOCKED = Tag.LOCKED.value
    PRIVACY = Tag.PRIVACY.value
    NONE = Tag.NONE.value


class RoleEnum(Enum):
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


class SexEnum(Enum):
    """Implement the GEDCOM SEX enumeration set as an enumeration class.

    Reference:
        [GEDCOM SEX enumeration set]()
    """

    M = Tag.M.value
    F = Tag.F.value
    X = Tag.X.value
    U = Tag.U.value
    NONE = Tag.NONE.value


class StatEnum(Enum):
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
    enums: list[str] | None = None
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
        return f"    {self.value} = TagTuple(value='{self.value.upper()}', standard_tag='{self.standard_tag}', supers={self.supers}, subs={self.subs}, required={self.required}, single={self.single}, enumsets={self.enumsets}, enums={self.enums})"
    
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
  enums = {self.enums},
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

class Terms(Enum):
    """Terms containing GEDCOM specifications.

    For each version of GEDCOM this data is collected and stored in a module.
    The methods reference this data to identify the name of the tag, whether
    the substructure is required or not and the cardinality of the substructure.

    The `TagYaml` class retrieves these and stores data in a `TagTuple` NamedTuple
    which is made visible in `StdTag`.

    See Also:
      `StdTag`
      `TagTuple`
      `TagYaml`

    Reference:
      [GEDCOM Tags](https://github.com/FamilySearch/GEDCOM/tree/main/extracted-files/tags)
    """

    ABBR = 'ABBR'
    ADDR = 'ADDR'
    ADOP = 'ADOP'
    ADOP_FAMC = 'ADOP-FAMC'
    ADR1 = 'ADR1'
    ADR2 = 'ADR2'
    ADR3 = 'ADR3'
    AFN = 'AFN'
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
    CALN = 'CALN'
    CAST = 'CAST'
    CAUS = 'CAUS'
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
    DATA_EVEN = 'DATA-EVEN'
    DATA_EVEN_DATE = 'DATA-EVEN-DATE'
    DATE = 'DATE'
    DATE_EXACT = 'DATE-exact'
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
    EXID = 'EXID'
    EXID_TYPE = 'EXID-TYPE'
    FAM_CENS = 'FAM-CENS'
    FAM_EVEN = 'FAM-EVEN'
    FAM_FACT = 'FAM-FACT'
    FAM_HUSB = 'FAM-HUSB'
    FAM_NCHI = 'FAM-NCHI'
    FAM_RESI = 'FAM-RESI'
    FAM_WIFE = 'FAM-WIFE'
    FAMC = 'FAMC'
    FAMC_ADOP = 'FAMC-ADOP'
    FAMC_STAT = 'FAMC-STAT'
    FAMS = 'FAMS'
    FAX = 'FAX'
    FCOM = 'FCOM'
    FILE = 'FILE'
    FILE_TRAN = 'FILE-TRAN'
    FORM = 'FORM'
    GEDC = 'GEDC'
    GEDC_VERS = 'GEDC-VERS'
    GIVN = 'GIVN'
    GRAD = 'GRAD'
    HEAD = 'HEAD'
    HEAD_DATE = 'HEAD-DATE'
    HEAD_LANG = 'HEAD-LANG'
    HEAD_PLAC = 'HEAD-PLAC'
    HEAD_PLAC_FORM = 'HEAD-PLAC-FORM'
    HEAD_SOUR = 'HEAD-SOUR'
    HEAD_SOUR_DATA = 'HEAD-SOUR-DATA'
    HEIGHT = 'HEIGHT'
    HUSB = 'HUSB'
    IDNO = 'IDNO'
    IMMI = 'IMMI'
    INDI_CENS = 'INDI-CENS'
    INDI_EVEN = 'INDI-EVEN'
    INDI_FACT = 'INDI-FACT'
    INDI_FAMC = 'INDI-FAMC'
    INDI_NAME = 'INDI-NAME'
    INDI_NCHI = 'INDI-NCHI'
    INDI_RELI = 'INDI-RELI'
    INDI_RESI = 'INDI-RESI'
    INDI_TITL = 'INDI-TITL'
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
    NAME_TRAN = 'NAME-TRAN'
    NAME_TYPE = 'NAME-TYPE'
    NATI = 'NATI'
    NATU = 'NATU'
    NICK = 'NICK'
    NMR = 'NMR'
    NO = 'NO'
    NO_DATE = 'NO-DATE'
    NOTE = 'NOTE'
    NOTE_TRAN = 'NOTE-TRAN'
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
    PLAC_FORM = 'PLAC-FORM'
    PLAC_TRAN = 'PLAC-TRAN'
    POST = 'POST'
    PROB = 'PROB'
    PROP = 'PROP'
    PUBL = 'PUBL'
    QUAY = 'QUAY'
    REFN = 'REFN'
    RELI = 'RELI'
    REPO = 'REPO'
    RESN = 'RESN'
    RETI = 'RETI'
    RFN = 'RFN'
    RIN = 'RIN'
    ROLE = 'ROLE'
    SCHMA = 'SCHMA'
    SDATE = 'SDATE'
    SEX = 'SEX'
    SLGC = 'SLGC'
    SLGS = 'SLGS'
    SNOTE = 'SNOTE'
    SOUR = 'SOUR'
    SOUR_DATA = 'SOUR-DATA'
    SOUR_EVEN = 'SOUR-EVEN'
    SPFX = 'SPFX'
    SSN = 'SSN'
    STAE = 'STAE'
    SUBM = 'SUBM'
    SUBM_LANG = 'SUBM-LANG'
    SURN = 'SURN'
    TAG = 'TAG'
    TEMP = 'TEMP'
    TEXT = 'TEXT'
    TIME = 'TIME'
    TITL = 'TITL'
    TOP = 'TOP'
    TRLR = 'TRLR'
    TYPE = 'TYPE'
    UID = 'UID'
    VERS = 'VERS'
    WIDTH = 'WIDTH'
    WIFE = 'WIFE'
    WILL = 'WILL'
    WWW = 'WWW'
    CAL_FRENCH_R = 'cal-FRENCH_R'
    CAL_GREGORIAN = 'cal-GREGORIAN'
    CAL_HEBREW = 'cal-HEBREW'
    CAL_JULIAN = 'cal-JULIAN'
    ENUM_0 = 'enum-0'
    ENUM_1 = 'enum-1'
    ENUM_2 = 'enum-2'
    ENUM_3 = 'enum-3'
    ENUM_ADOP_HUSB = 'enum-ADOP-HUSB'
    ENUM_ADOP_WIFE = 'enum-ADOP-WIFE'
    ENUM_ADOPTED = 'enum-ADOPTED'
    ENUM_AKA = 'enum-AKA'
    ENUM_AUDIO = 'enum-AUDIO'
    ENUM_BIC = 'enum-BIC'
    ENUM_BIRTH = 'enum-BIRTH'
    ENUM_BOOK = 'enum-BOOK'
    ENUM_BOTH = 'enum-BOTH'
    ENUM_CANCELED = 'enum-CANCELED'
    ENUM_CARD = 'enum-CARD'
    ENUM_CENS = 'enum-CENS'
    ENUM_CHALLENGED = 'enum-CHALLENGED'
    ENUM_CHIL = 'enum-CHIL'
    ENUM_CHILD = 'enum-CHILD'
    ENUM_CLERGY = 'enum-CLERGY'
    ENUM_COMPLETED = 'enum-COMPLETED'
    ENUM_CONFIDENTIAL = 'enum-CONFIDENTIAL'
    ENUM_DISPROVEN = 'enum-DISPROVEN'
    ENUM_DNS = 'enum-DNS'
    ENUM_DNS_CAN = 'enum-DNS_CAN'
    ENUM_ELECTRONIC = 'enum-ELECTRONIC'
    ENUM_EVEN = 'enum-EVEN'
    ENUM_EXCLUDED = 'enum-EXCLUDED'
    ENUM_F = 'enum-F'
    ENUM_FACT = 'enum-FACT'
    ENUM_FATH = 'enum-FATH'
    ENUM_FICHE = 'enum-FICHE'
    ENUM_FILM = 'enum-FILM'
    ENUM_FOSTER = 'enum-FOSTER'
    ENUM_FRIEND = 'enum-FRIEND'
    ENUM_GODP = 'enum-GODP'
    ENUM_HUSB = 'enum-HUSB'
    ENUM_IMMIGRANT = 'enum-IMMIGRANT'
    ENUM_INFANT = 'enum-INFANT'
    ENUM_LOCKED = 'enum-LOCKED'
    ENUM_M = 'enum-M'
    ENUM_MAGAZINE = 'enum-MAGAZINE'
    ENUM_MAIDEN = 'enum-MAIDEN'
    ENUM_MANUSCRIPT = 'enum-MANUSCRIPT'
    ENUM_MAP = 'enum-MAP'
    ENUM_MARRIED = 'enum-MARRIED'
    ENUM_MOTH = 'enum-MOTH'
    ENUM_MULTIPLE = 'enum-MULTIPLE'
    ENUM_NCHI = 'enum-NCHI'
    ENUM_NEWSPAPER = 'enum-NEWSPAPER'
    ENUM_NGHBR = 'enum-NGHBR'
    ENUM_OFFICIATOR = 'enum-OFFICIATOR'
    ENUM_OTHER = 'enum-OTHER'
    ENUM_PARENT = 'enum-PARENT'
    ENUM_PHOTO = 'enum-PHOTO'
    ENUM_PRE_1970 = 'enum-PRE_1970'
    ENUM_PRIVACY = 'enum-PRIVACY'
    ENUM_PROFESSIONAL = 'enum-PROFESSIONAL'
    ENUM_PROVEN = 'enum-PROVEN'
    ENUM_RESI = 'enum-RESI'
    ENUM_SEALING = 'enum-SEALING'
    ENUM_SPOU = 'enum-SPOU'
    ENUM_STILLBORN = 'enum-STILLBORN'
    ENUM_SUBMITTED = 'enum-SUBMITTED'
    ENUM_TOMBSTONE = 'enum-TOMBSTONE'
    ENUM_U = 'enum-U'
    ENUM_UNCLEARED = 'enum-UNCLEARED'
    ENUM_VIDEO = 'enum-VIDEO'
    ENUM_WIFE = 'enum-WIFE'
    ENUM_WITN = 'enum-WITN'
    ENUM_X = 'enum-X'
    ENUMSET_ADOP = 'enumset-ADOP'
    ENUMSET_EVEN = 'enumset-EVEN'
    ENUMSET_EVENATTR = 'enumset-EVENATTR'
    ENUMSET_MEDI = 'enumset-MEDI'
    ENUMSET_NAME_TYPE = 'enumset-NAME-TYPE'
    ENUMSET_PEDI = 'enumset-PEDI'
    ENUMSET_QUAY = 'enumset-QUAY'
    ENUMSET_RESN = 'enumset-RESN'
    ENUMSET_ROLE = 'enumset-ROLE'
    ENUMSET_SEX = 'enumset-SEX'
    ENUMSET_ORD_STAT = 'enumset-ord-STAT'
    MONTH_AAV = 'month-AAV'
    MONTH_ADR = 'month-ADR'
    MONTH_ADS = 'month-ADS'
    MONTH_APR = 'month-APR'
    MONTH_AUG = 'month-AUG'
    MONTH_BRUM = 'month-BRUM'
    MONTH_COMP = 'month-COMP'
    MONTH_CSH = 'month-CSH'
    MONTH_DEC = 'month-DEC'
    MONTH_ELL = 'month-ELL'
    MONTH_FEB = 'month-FEB'
    MONTH_FLOR = 'month-FLOR'
    MONTH_FRIM = 'month-FRIM'
    MONTH_FRUC = 'month-FRUC'
    MONTH_GERM = 'month-GERM'
    MONTH_IYR = 'month-IYR'
    MONTH_JAN = 'month-JAN'
    MONTH_JUL = 'month-JUL'
    MONTH_JUN = 'month-JUN'
    MONTH_KSL = 'month-KSL'
    MONTH_MAR = 'month-MAR'
    MONTH_MAY = 'month-MAY'
    MONTH_MESS = 'month-MESS'
    MONTH_NIVO = 'month-NIVO'
    MONTH_NOV = 'month-NOV'
    MONTH_NSN = 'month-NSN'
    MONTH_OCT = 'month-OCT'
    MONTH_PLUV = 'month-PLUV'
    MONTH_PRAI = 'month-PRAI'
    MONTH_SEP = 'month-SEP'
    MONTH_SHV = 'month-SHV'
    MONTH_SVN = 'month-SVN'
    MONTH_THER = 'month-THER'
    MONTH_TMZ = 'month-TMZ'
    MONTH_TSH = 'month-TSH'
    MONTH_TVT = 'month-TVT'
    MONTH_VEND = 'month-VEND'
    MONTH_VENT = 'month-VENT'
    ORD_STAT = 'ord-STAT'
    RECORD_FAM = 'record-FAM'
    RECORD_INDI = 'record-INDI'
    RECORD_OBJE = 'record-OBJE'
    RECORD_REPO = 'record-REPO'
    RECORD_SNOTE = 'record-SNOTE'
    RECORD_SOUR = 'record-SOUR'
    RECORD_SUBM = 'record-SUBM'
    TYPE_AGE = 'type-Age'
    TYPE_DATE = 'type-Date'
    TYPE_ENUM = 'type-Enum'
    TYPE_FILEPATH = 'type-FilePath'
    TYPE_LIST = 'type-List'
    TYPE_NAME = 'type-Name'
    TYPE_TIME = 'type-Time'




class StdTag(Enum):
    """Generated definitions based on the enumeration class `Tag` and used to check extensions.

    When a new version of the GEDCOM standard `genedata.store.TagYaml.generate` should be rerun
    in a Notebook cell.  Copy the definitions into this class.
    """

    Abbr = TagTuple(value='ABBR', standard_tag='ABBR', supers=['RecordSour'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Addr = TagTuple(value='ADDR', standard_tag='ADDR', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Corp', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will', 'RecordRepo', 'RecordSubm'], subs=['Adr1', 'Adr2', 'Adr3', 'City', 'Ctry', 'Post', 'Stae'], required=[], single=['Adr1', 'Adr2', 'Adr3', 'City', 'Ctry', 'Post', 'Stae'], enumsets=[], enums=[])
    Adop = TagTuple(value='ADOP', standard_tag='ADOP', supers=['RecordIndi'], subs=['Addr', 'AdopFamc', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'AdopFamc', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    AdopFamc = TagTuple(value='ADOPFAMC', standard_tag='FAMC', supers=['Adop'], subs=['FamcAdop'], required=[], single=['FamcAdop'], enumsets=[], enums=[])
    Adr1 = TagTuple(value='ADR1', standard_tag='ADR1', supers=['Addr'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Adr2 = TagTuple(value='ADR2', standard_tag='ADR2', supers=['Addr'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Adr3 = TagTuple(value='ADR3', standard_tag='ADR3', supers=['Addr'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Afn = TagTuple(value='AFN', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    Age = TagTuple(value='AGE', standard_tag='AGE', supers=['Adop', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Crem', 'Deat', 'Dscr', 'Educ', 'Emig', 'Fcom', 'Grad', 'Husb', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Wife', 'Will'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    Agnc = TagTuple(value='AGNC', standard_tag='AGNC', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Crem', 'Data', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Alia = TagTuple(value='ALIA', standard_tag='ALIA', supers=['RecordIndi'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    Anci = TagTuple(value='ANCI', standard_tag='ANCI', supers=['RecordIndi'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Anul = TagTuple(value='ANUL', standard_tag='ANUL', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Asso = TagTuple(value='ASSO', standard_tag='ASSO', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will', 'RecordFam', 'RecordIndi'], subs=['Note', 'Phrase', 'Role', 'Snote', 'Sour'], required=['Role'], single=['Phrase', 'Role'], enumsets=[], enums=[])
    Auth = TagTuple(value='AUTH', standard_tag='AUTH', supers=['RecordSour'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Bapl = TagTuple(value='BAPL', standard_tag='BAPL', supers=['RecordIndi'], subs=['Date', 'Note', 'Plac', 'Snote', 'Sour', 'Temp', 'OrdStat'], required=[], single=['Date', 'Plac', 'Temp', 'OrdStat'], enumsets=[], enums=[])
    Bapm = TagTuple(value='BAPM', standard_tag='BAPM', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Barm = TagTuple(value='BARM', standard_tag='BARM', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Basm = TagTuple(value='BASM', standard_tag='BASM', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Birt = TagTuple(value='BIRT', standard_tag='BIRT', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Famc', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Famc', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Bles = TagTuple(value='BLES', standard_tag='BLES', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Caln = TagTuple(value='CALN', standard_tag='CALN', supers=['Repo'], subs=['Medi'], required=[], single=['Medi'], enumsets=[], enums=[])
    Cast = TagTuple(value='CAST', standard_tag='CAST', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVENATTR'], enums=[])
    Caus = TagTuple(value='CAUS', standard_tag='CAUS', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Chan = TagTuple(value='CHAN', standard_tag='CHAN', supers=['RecordFam', 'RecordIndi', 'RecordObje', 'RecordRepo', 'RecordSnote', 'RecordSour', 'RecordSubm'], subs=['DateExact', 'Note', 'Snote'], required=['DateExact'], single=['DateExact'], enumsets=[], enums=[])
    Chil = TagTuple(value='CHIL', standard_tag='CHIL', supers=['RecordFam'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    Chr = TagTuple(value='CHR', standard_tag='CHR', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Famc', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Famc', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Chra = TagTuple(value='CHRA', standard_tag='CHRA', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    City = TagTuple(value='CITY', standard_tag='CITY', supers=['Addr'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Conf = TagTuple(value='CONF', standard_tag='CONF', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Conl = TagTuple(value='CONL', standard_tag='CONL', supers=['RecordIndi'], subs=['Date', 'Note', 'Plac', 'Snote', 'Sour', 'Temp', 'OrdStat'], required=[], single=['Date', 'Plac', 'Temp', 'OrdStat'], enumsets=[], enums=[])
    Cont = TagTuple(value='CONT', standard_tag='CONT', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    Copr = TagTuple(value='COPR', standard_tag='COPR', supers=['Head', 'HeadSourData'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Corp = TagTuple(value='CORP', standard_tag='CORP', supers=['HeadSour'], subs=['Addr', 'Email', 'Fax', 'Phon', 'Www'], required=[], single=['Addr'], enumsets=[], enums=[])
    Crea = TagTuple(value='CREA', standard_tag='CREA', supers=['RecordFam', 'RecordIndi', 'RecordObje', 'RecordRepo', 'RecordSnote', 'RecordSour', 'RecordSubm'], subs=['DateExact'], required=['DateExact'], single=['DateExact'], enumsets=[], enums=[])
    Crem = TagTuple(value='CREM', standard_tag='CREM', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Crop = TagTuple(value='CROP', standard_tag='CROP', supers=['Obje'], subs=['Height', 'Left', 'Top', 'Width'], required=[], single=['Height', 'Left', 'Top', 'Width'], enumsets=[], enums=[])
    Ctry = TagTuple(value='CTRY', standard_tag='CTRY', supers=['Addr'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Data = TagTuple(value='DATA', standard_tag='DATA', supers=['RecordSour'], subs=['Agnc', 'DataEven', 'Note', 'Snote'], required=[], single=['Agnc'], enumsets=[], enums=[])
    DataEven = TagTuple(value='DATAEVEN', standard_tag='EVEN', supers=['Data'], subs=['DataEvenDate', 'Plac'], required=[], single=['DataEvenDate', 'Plac'], enumsets=[], enums=[])
    DataEvenDate = TagTuple(value='DATAEVENDATE', standard_tag='DATE', supers=['DataEven'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    Date = TagTuple(value='DATE', standard_tag='DATE', supers=['Adop', 'Anul', 'Bapl', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Conl', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Endl', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Inil', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Slgc', 'Slgs', 'SourData', 'Ssn', 'Will'], subs=['Phrase', 'Time'], required=[], single=['Phrase', 'Time'], enumsets=[], enums=[])
    DateExact = TagTuple(value='DATEEXACT', standard_tag='DATE', supers=['Chan', 'Crea', 'HeadSourData', 'OrdStat'], subs=['Time'], required=[], single=['Time'], enumsets=[], enums=[])
    Deat = TagTuple(value='DEAT', standard_tag='DEAT', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Desi = TagTuple(value='DESI', standard_tag='DESI', supers=['RecordIndi'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Dest = TagTuple(value='DEST', standard_tag='DEST', supers=['Head'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Div = TagTuple(value='DIV', standard_tag='DIV', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Divf = TagTuple(value='DIVF', standard_tag='DIVF', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Dscr = TagTuple(value='DSCR', standard_tag='DSCR', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVENATTR'], enums=[])
    Educ = TagTuple(value='EDUC', standard_tag='EDUC', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVENATTR'], enums=[])
    Email = TagTuple(value='EMAIL', standard_tag='EMAIL', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Corp', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will', 'RecordRepo', 'RecordSubm'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Emig = TagTuple(value='EMIG', standard_tag='EMIG', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Endl = TagTuple(value='ENDL', standard_tag='ENDL', supers=['RecordIndi'], subs=['Date', 'Note', 'Plac', 'Snote', 'Sour', 'Temp', 'OrdStat'], required=[], single=['Date', 'Plac', 'Temp', 'OrdStat'], enumsets=[], enums=[])
    Enga = TagTuple(value='ENGA', standard_tag='ENGA', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Exid = TagTuple(value='EXID', standard_tag='EXID', supers=['Plac', 'RecordFam', 'RecordIndi', 'RecordObje', 'RecordRepo', 'RecordSnote', 'RecordSour', 'RecordSubm'], subs=['ExidType'], required=[], single=['ExidType'], enumsets=[], enums=[])
    ExidType = TagTuple(value='EXIDTYPE', standard_tag='TYPE', supers=['Exid'], subs=[], required=[], single=[], enumsets=[], enums=[])
    FamCens = TagTuple(value='FAMCENS', standard_tag='CENS', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=[], enums=[])
    FamEven = TagTuple(value='FAMEVEN', standard_tag='EVEN', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=['Type'], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=[], enums=[])
    FamFact = TagTuple(value='FAMFACT', standard_tag='FACT', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=['Type'], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=[], enums=[])
    FamHusb = TagTuple(value='FAMHUSB', standard_tag='HUSB', supers=['RecordFam'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    FamNchi = TagTuple(value='FAMNCHI', standard_tag='NCHI', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=[], enums=[])
    FamResi = TagTuple(value='FAMRESI', standard_tag='RESI', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=[], enums=[])
    FamWife = TagTuple(value='FAMWIFE', standard_tag='WIFE', supers=['RecordFam'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    Famc = TagTuple(value='FAMC', standard_tag='FAMC', supers=['Birt', 'Chr', 'Slgc'], subs=[], required=[], single=[], enumsets=[], enums=[])
    FamcAdop = TagTuple(value='FAMCADOP', standard_tag='ADOP', supers=['AdopFamc'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    FamcStat = TagTuple(value='FAMCSTAT', standard_tag='STAT', supers=['IndiFamc'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    Fams = TagTuple(value='FAMS', standard_tag='FAMS', supers=['RecordIndi'], subs=['Note', 'Snote'], required=[], single=[], enumsets=[], enums=[])
    Fax = TagTuple(value='FAX', standard_tag='FAX', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Corp', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will', 'RecordRepo', 'RecordSubm'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Fcom = TagTuple(value='FCOM', standard_tag='FCOM', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    File = TagTuple(value='FILE', standard_tag='FILE', supers=['RecordObje'], subs=['FileTran', 'Form', 'Titl'], required=['Form'], single=['Form', 'Titl'], enumsets=[], enums=[])
    FileTran = TagTuple(value='FILETRAN', standard_tag='TRAN', supers=['File'], subs=['Form'], required=['Form'], single=['Form'], enumsets=[], enums=[])
    Form = TagTuple(value='FORM', standard_tag='FORM', supers=['File', 'FileTran'], subs=['Medi'], required=[], single=['Medi'], enumsets=[], enums=[])
    Gedc = TagTuple(value='GEDC', standard_tag='GEDC', supers=['Head'], subs=['GedcVers'], required=['GedcVers'], single=['GedcVers'], enumsets=[], enums=[])
    GedcVers = TagTuple(value='GEDCVERS', standard_tag='VERS', supers=['Gedc'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Givn = TagTuple(value='GIVN', standard_tag='GIVN', supers=['IndiName', 'NameTran'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Grad = TagTuple(value='GRAD', standard_tag='GRAD', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Head = TagTuple(value='HEAD', standard_tag='HEAD', supers=[], subs=['Copr', 'Dest', 'Gedc', 'HeadDate', 'HeadLang', 'HeadPlac', 'HeadSour', 'Note', 'Schma', 'Snote', 'Subm'], required=['Gedc'], single=['Copr', 'Dest', 'Gedc', 'HeadDate', 'HeadLang', 'HeadPlac', 'HeadSour', 'Note', 'Schma', 'Snote', 'Subm'], enumsets=[], enums=[])
    HeadDate = TagTuple(value='HEADDATE', standard_tag='DATE', supers=['Head'], subs=['Time'], required=[], single=['Time'], enumsets=[], enums=[])
    HeadLang = TagTuple(value='HEADLANG', standard_tag='LANG', supers=['Head'], subs=[], required=[], single=[], enumsets=[], enums=[])
    HeadPlac = TagTuple(value='HEADPLAC', standard_tag='PLAC', supers=['Head'], subs=['HeadPlacForm'], required=['HeadPlacForm'], single=['HeadPlacForm'], enumsets=[], enums=[])
    HeadPlacForm = TagTuple(value='HEADPLACFORM', standard_tag='FORM', supers=['HeadPlac'], subs=[], required=[], single=[], enumsets=[], enums=[])
    HeadSour = TagTuple(value='HEADSOUR', standard_tag='SOUR', supers=['Head'], subs=['Corp', 'HeadSourData', 'Name', 'Vers'], required=[], single=['Corp', 'HeadSourData', 'Name', 'Vers'], enumsets=[], enums=[])
    HeadSourData = TagTuple(value='HEADSOURDATA', standard_tag='DATA', supers=['HeadSour'], subs=['Copr', 'DateExact'], required=[], single=['Copr', 'DateExact'], enumsets=[], enums=[])
    Height = TagTuple(value='HEIGHT', standard_tag='HEIGHT', supers=['Crop'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Husb = TagTuple(value='HUSB', standard_tag='HUSB', supers=['Anul', 'Div', 'Divf', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars'], subs=['Age'], required=['Age'], single=['Age'], enumsets=[], enums=[])
    Idno = TagTuple(value='IDNO', standard_tag='IDNO', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=['Type'], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVENATTR'], enums=[])
    Immi = TagTuple(value='IMMI', standard_tag='IMMI', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    IndiCens = TagTuple(value='INDICENS', standard_tag='CENS', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=[], enums=[])
    IndiEven = TagTuple(value='INDIEVEN', standard_tag='EVEN', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=['Type'], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=[], enums=[])
    IndiFact = TagTuple(value='INDIFACT', standard_tag='FACT', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=['Type'], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=[], enums=[])
    IndiFamc = TagTuple(value='INDIFAMC', standard_tag='FAMC', supers=['RecordIndi'], subs=['FamcStat', 'Note', 'Pedi', 'Snote'], required=[], single=['FamcStat', 'Pedi'], enumsets=[], enums=[])
    IndiName = TagTuple(value='INDINAME', standard_tag='NAME', supers=['RecordIndi'], subs=['Givn', 'NameTran', 'NameType', 'Nick', 'Note', 'Npfx', 'Nsfx', 'Snote', 'Sour', 'Spfx', 'Surn'], required=[], single=['NameType'], enumsets=[], enums=[])
    IndiNchi = TagTuple(value='INDINCHI', standard_tag='NCHI', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=[], enums=[])
    IndiReli = TagTuple(value='INDIRELI', standard_tag='RELI', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=[], enums=[])
    IndiResi = TagTuple(value='INDIRESI', standard_tag='RESI', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=[], enums=[])
    IndiTitl = TagTuple(value='INDITITL', standard_tag='TITL', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=[], enums=[])
    Inil = TagTuple(value='INIL', standard_tag='INIL', supers=['RecordIndi'], subs=['Date', 'Note', 'Plac', 'Snote', 'Sour', 'Temp', 'OrdStat'], required=[], single=['Date', 'Plac', 'Temp', 'OrdStat'], enumsets=[], enums=[])
    Lang = TagTuple(value='LANG', standard_tag='LANG', supers=['NameTran', 'Note', 'NoteTran', 'Plac', 'PlacTran', 'Text', 'RecordSnote'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Lati = TagTuple(value='LATI', standard_tag='LATI', supers=['Map'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Left = TagTuple(value='LEFT', standard_tag='LEFT', supers=['Crop'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Long = TagTuple(value='LONG', standard_tag='LONG', supers=['Map'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Map = TagTuple(value='MAP', standard_tag='MAP', supers=['Plac'], subs=['Lati', 'Long'], required=['Lati', 'Long'], single=['Lati', 'Long'], enumsets=[], enums=[])
    Marb = TagTuple(value='MARB', standard_tag='MARB', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Marc = TagTuple(value='MARC', standard_tag='MARC', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Marl = TagTuple(value='MARL', standard_tag='MARL', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Marr = TagTuple(value='MARR', standard_tag='MARR', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Mars = TagTuple(value='MARS', standard_tag='MARS', supers=['RecordFam'], subs=['Addr', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Husb', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Wife', 'Www'], required=[], single=['Addr', 'Agnc', 'Caus', 'Date', 'Husb', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type', 'Wife'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Medi = TagTuple(value='MEDI', standard_tag='MEDI', supers=['Caln', 'Form'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    Mime = TagTuple(value='MIME', standard_tag='MIME', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    Name = TagTuple(value='NAME', standard_tag='NAME', supers=['HeadSour', 'RecordRepo', 'RecordSubm'], subs=[], required=[], single=[], enumsets=[], enums=[])
    NameTran = TagTuple(value='NAMETRAN', standard_tag='TRAN', supers=['IndiName'], subs=['Givn', 'Lang', 'Nick', 'Npfx', 'Nsfx', 'Spfx', 'Surn'], required=['Lang'], single=['Lang'], enumsets=[], enums=[])
    NameType = TagTuple(value='NAMETYPE', standard_tag='TYPE', supers=['IndiName'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    Nati = TagTuple(value='NATI', standard_tag='NATI', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVENATTR'], enums=[])
    Natu = TagTuple(value='NATU', standard_tag='NATU', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Nick = TagTuple(value='NICK', standard_tag='NICK', supers=['IndiName', 'NameTran'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Nmr = TagTuple(value='NMR', standard_tag='NMR', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVENATTR'], enums=[])
    No = TagTuple(value='NO', standard_tag='NO', supers=['RecordFam', 'RecordIndi'], subs=['NoDate', 'Note', 'Snote', 'Sour'], required=[], single=['NoDate'], enumsets=[], enums=[])
    NoDate = TagTuple(value='NODATE', standard_tag='DATE', supers=['No'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    Note = TagTuple(value='NOTE', standard_tag='NOTE', supers=['Adop', 'Anul', 'Asso', 'Bapl', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chan', 'Chr', 'Chra', 'Conf', 'Conl', 'Crem', 'Data', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Endl', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fams', 'Fcom', 'Grad', 'Head', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiFamc', 'IndiName', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Inil', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'No', 'Occu', 'Ordn', 'Plac', 'Prob', 'Prop', 'Repo', 'Reti', 'Slgc', 'Slgs', 'Sour', 'Ssn', 'Will', 'RecordFam', 'RecordIndi', 'RecordObje', 'RecordRepo', 'RecordSour', 'RecordSubm'], subs=['Lang', 'Mime', 'NoteTran', 'Sour'], required=[], single=['Lang', 'Mime'], enumsets=[], enums=[])
    NoteTran = TagTuple(value='NOTETRAN', standard_tag='TRAN', supers=['Note', 'RecordSnote'], subs=['Lang', 'Mime'], required=[], single=['Lang', 'Mime'], enumsets=[], enums=[])
    Npfx = TagTuple(value='NPFX', standard_tag='NPFX', supers=['IndiName', 'NameTran'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Nsfx = TagTuple(value='NSFX', standard_tag='NSFX', supers=['IndiName', 'NameTran'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Obje = TagTuple(value='OBJE', standard_tag='OBJE', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Sour', 'Ssn', 'Will', 'RecordFam', 'RecordIndi', 'RecordSour', 'RecordSubm'], subs=['Crop', 'Titl'], required=[], single=['Crop', 'Titl'], enumsets=[], enums=[])
    Occu = TagTuple(value='OCCU', standard_tag='OCCU', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVENATTR'], enums=[])
    Ordn = TagTuple(value='ORDN', standard_tag='ORDN', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Page = TagTuple(value='PAGE', standard_tag='PAGE', supers=['Sour'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Pedi = TagTuple(value='PEDI', standard_tag='PEDI', supers=['IndiFamc'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    Phon = TagTuple(value='PHON', standard_tag='PHON', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Corp', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will', 'RecordRepo', 'RecordSubm'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Phrase = TagTuple(value='PHRASE', standard_tag='PHRASE', supers=['Age', 'Alia', 'Asso', 'Chil', 'DataEvenDate', 'Date', 'FamHusb', 'FamWife', 'FamcAdop', 'FamcStat', 'Medi', 'NameType', 'NoDate', 'Pedi', 'Role', 'Sdate', 'SourEven'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Plac = TagTuple(value='PLAC', standard_tag='PLAC', supers=['Adop', 'Anul', 'Bapl', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Conl', 'Crem', 'DataEven', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Endl', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Inil', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Slgc', 'Slgs', 'Ssn', 'Will'], subs=['Exid', 'Lang', 'Map', 'Note', 'PlacForm', 'PlacTran', 'Snote'], required=[], single=['Lang', 'Map', 'PlacForm'], enumsets=[], enums=[])
    PlacForm = TagTuple(value='PLACFORM', standard_tag='FORM', supers=['Plac'], subs=[], required=[], single=[], enumsets=[], enums=[])
    PlacTran = TagTuple(value='PLACTRAN', standard_tag='TRAN', supers=['Plac'], subs=['Lang'], required=['Lang'], single=['Lang'], enumsets=[], enums=[])
    Post = TagTuple(value='POST', standard_tag='POST', supers=['Addr'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Prob = TagTuple(value='PROB', standard_tag='PROB', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Prop = TagTuple(value='PROP', standard_tag='PROP', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVENATTR'], enums=[])
    Publ = TagTuple(value='PUBL', standard_tag='PUBL', supers=['RecordSour'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Quay = TagTuple(value='QUAY', standard_tag='QUAY', supers=['Sour'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Refn = TagTuple(value='REFN', standard_tag='REFN', supers=['RecordFam', 'RecordIndi', 'RecordObje', 'RecordRepo', 'RecordSnote', 'RecordSour', 'RecordSubm'], subs=['Type'], required=[], single=['Type'], enumsets=[], enums=[])
    Reli = TagTuple(value='RELI', standard_tag='RELI', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will'], subs=[], required=[], single=[], enumsets=['EVENATTR'], enums=[])
    Repo = TagTuple(value='REPO', standard_tag='REPO', supers=['RecordSour'], subs=['Caln', 'Note', 'Snote'], required=[], single=[], enumsets=[], enums=[])
    Resn = TagTuple(value='RESN', standard_tag='RESN', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will', 'RecordFam', 'RecordIndi', 'RecordObje'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Reti = TagTuple(value='RETI', standard_tag='RETI', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Rfn = TagTuple(value='RFN', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    Rin = TagTuple(value='RIN', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    Role = TagTuple(value='ROLE', standard_tag='ROLE', supers=['Asso', 'SourEven'], subs=['Phrase'], required=[], single=['Phrase'], enumsets=[], enums=[])
    Schma = TagTuple(value='SCHMA', standard_tag='SCHMA', supers=['Head'], subs=['Tag'], required=[], single=[], enumsets=[], enums=[])
    Sdate = TagTuple(value='SDATE', standard_tag='SDATE', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will'], subs=['Phrase', 'Time'], required=[], single=['Phrase', 'Time'], enumsets=[], enums=[])
    Sex = TagTuple(value='SEX', standard_tag='SEX', supers=['RecordIndi'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Slgc = TagTuple(value='SLGC', standard_tag='SLGC', supers=['RecordIndi'], subs=['Date', 'Famc', 'Note', 'Plac', 'Snote', 'Sour', 'Temp', 'OrdStat'], required=['Famc'], single=['Date', 'Famc', 'Plac', 'Temp', 'OrdStat'], enumsets=[], enums=[])
    Slgs = TagTuple(value='SLGS', standard_tag='SLGS', supers=['RecordFam'], subs=['Date', 'Note', 'Plac', 'Snote', 'Sour', 'Temp', 'OrdStat'], required=[], single=['Date', 'Plac', 'Temp', 'OrdStat'], enumsets=[], enums=[])
    Snote = TagTuple(value='SNOTE', standard_tag='SNOTE', supers=['Adop', 'Anul', 'Asso', 'Bapl', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chan', 'Chr', 'Chra', 'Conf', 'Conl', 'Crem', 'Data', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Endl', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fams', 'Fcom', 'Grad', 'Head', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiFamc', 'IndiName', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Inil', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'No', 'Occu', 'Ordn', 'Plac', 'Prob', 'Prop', 'Repo', 'Reti', 'Slgc', 'Slgs', 'Sour', 'Ssn', 'Will', 'RecordFam', 'RecordIndi', 'RecordObje', 'RecordRepo', 'RecordSour', 'RecordSubm'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Sour = TagTuple(value='SOUR', standard_tag='SOUR', supers=['Adop', 'Anul', 'Asso', 'Bapl', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Conl', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Endl', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiName', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Inil', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'No', 'Note', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Slgc', 'Slgs', 'Ssn', 'Will', 'RecordFam', 'RecordIndi', 'RecordObje', 'RecordSnote'], subs=['Note', 'Obje', 'Page', 'Quay', 'Snote', 'SourData', 'SourEven'], required=[], single=['Page', 'Quay', 'SourData', 'SourEven'], enumsets=[], enums=[])
    SourData = TagTuple(value='SOURDATA', standard_tag='DATA', supers=['Sour'], subs=['Date', 'Text'], required=[], single=['Date'], enumsets=[], enums=[])
    SourEven = TagTuple(value='SOUREVEN', standard_tag='EVEN', supers=['Sour'], subs=['Phrase', 'Role'], required=[], single=['Phrase', 'Role'], enumsets=[], enums=[])
    Spfx = TagTuple(value='SPFX', standard_tag='SPFX', supers=['IndiName', 'NameTran'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Ssn = TagTuple(value='SSN', standard_tag='SSN', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVENATTR'], enums=[])
    Stae = TagTuple(value='STAE', standard_tag='STAE', supers=['Addr'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Subm = TagTuple(value='SUBM', standard_tag='SUBM', supers=['Head', 'RecordFam', 'RecordIndi'], subs=[], required=[], single=[], enumsets=[], enums=[])
    SubmLang = TagTuple(value='SUBMLANG', standard_tag='LANG', supers=['RecordSubm'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Surn = TagTuple(value='SURN', standard_tag='SURN', supers=['IndiName', 'NameTran'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Tag = TagTuple(value='TAG', standard_tag='TAG', supers=['Schma'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Temp = TagTuple(value='TEMP', standard_tag='TEMP', supers=['Bapl', 'Conl', 'Endl', 'Inil', 'Slgc', 'Slgs'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Text = TagTuple(value='TEXT', standard_tag='TEXT', supers=['SourData', 'RecordSour'], subs=['Lang', 'Mime'], required=[], single=['Lang', 'Mime'], enumsets=[], enums=[])
    Time = TagTuple(value='TIME', standard_tag='TIME', supers=['Date', 'DateExact', 'HeadDate', 'Sdate'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Titl = TagTuple(value='TITL', standard_tag='TITL', supers=['File', 'Obje', 'RecordSour'], subs=[], required=[], single=[], enumsets=['EVENATTR'], enums=[])
    Top = TagTuple(value='TOP', standard_tag='TOP', supers=['Crop'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Trlr = TagTuple(value='TRLR', standard_tag='TRLR', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    Type = TagTuple(value='TYPE', standard_tag='TYPE', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Refn', 'Reti', 'Ssn', 'Will'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Uid = TagTuple(value='UID', standard_tag='UID', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will', 'RecordFam', 'RecordIndi', 'RecordObje', 'RecordRepo', 'RecordSnote', 'RecordSour', 'RecordSubm'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Vers = TagTuple(value='VERS', standard_tag='VERS', supers=['HeadSour'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Width = TagTuple(value='WIDTH', standard_tag='WIDTH', supers=['Crop'], subs=[], required=[], single=[], enumsets=[], enums=[])
    Wife = TagTuple(value='WIFE', standard_tag='WIFE', supers=['Anul', 'Div', 'Divf', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars'], subs=['Age'], required=['Age'], single=['Age'], enumsets=[], enums=[])
    Will = TagTuple(value='WILL', standard_tag='WILL', supers=['RecordIndi'], subs=['Addr', 'Age', 'Agnc', 'Asso', 'Caus', 'Date', 'Email', 'Fax', 'Note', 'Obje', 'Phon', 'Plac', 'Reli', 'Resn', 'Sdate', 'Snote', 'Sour', 'Type', 'Uid', 'Www'], required=[], single=['Addr', 'Age', 'Agnc', 'Caus', 'Date', 'Plac', 'Reli', 'Resn', 'Sdate', 'Type'], enumsets=['EVEN', 'EVENATTR'], enums=[])
    Www = TagTuple(value='WWW', standard_tag='WWW', supers=['Adop', 'Anul', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chr', 'Chra', 'Conf', 'Corp', 'Crem', 'Deat', 'Div', 'Divf', 'Dscr', 'Educ', 'Emig', 'Enga', 'FamCens', 'FamEven', 'FamFact', 'FamNchi', 'FamResi', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'Nati', 'Natu', 'Nmr', 'Occu', 'Ordn', 'Prob', 'Prop', 'Reti', 'Ssn', 'Will', 'RecordRepo', 'RecordSubm'], subs=[], required=[], single=[], enumsets=[], enums=[])
    CalFrench_R = TagTuple(value='CALFRENCH_R', standard_tag='FRENCH_R', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    CalGregorian = TagTuple(value='CALGREGORIAN', standard_tag='GREGORIAN', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    CalHebrew = TagTuple(value='CALHEBREW', standard_tag='HEBREW', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    CalJulian = TagTuple(value='CALJULIAN', standard_tag='JULIAN', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    Enum0 = TagTuple(value='ENUM0', standard_tag='0', supers=[], subs=[], required=[], single=[], enumsets=['QUAY'], enums=[])
    Enum1 = TagTuple(value='ENUM1', standard_tag='1', supers=[], subs=[], required=[], single=[], enumsets=['QUAY'], enums=[])
    Enum2 = TagTuple(value='ENUM2', standard_tag='2', supers=[], subs=[], required=[], single=[], enumsets=['QUAY'], enums=[])
    Enum3 = TagTuple(value='ENUM3', standard_tag='3', supers=[], subs=[], required=[], single=[], enumsets=['QUAY'], enums=[])
    EnumAdopHusb = TagTuple(value='ENUMADOPHUSB', standard_tag='HUSB', supers=[], subs=[], required=[], single=[], enumsets=['ADOP'], enums=[])
    EnumAdopWife = TagTuple(value='ENUMADOPWIFE', standard_tag='WIFE', supers=[], subs=[], required=[], single=[], enumsets=['ADOP'], enums=[])
    EnumAdopted = TagTuple(value='ENUMADOPTED', standard_tag='ADOPTED', supers=[], subs=[], required=[], single=[], enumsets=['PEDI'], enums=[])
    EnumAka = TagTuple(value='ENUMAKA', standard_tag='AKA', supers=[], subs=[], required=[], single=[], enumsets=['TYPE'], enums=[])
    EnumAudio = TagTuple(value='ENUMAUDIO', standard_tag='AUDIO', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumBic = TagTuple(value='ENUMBIC', standard_tag='BIC', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumBirth = TagTuple(value='ENUMBIRTH', standard_tag='BIRTH', supers=[], subs=[], required=[], single=[], enumsets=['TYPE', 'PEDI'], enums=[])
    EnumBook = TagTuple(value='ENUMBOOK', standard_tag='BOOK', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumBoth = TagTuple(value='ENUMBOTH', standard_tag='BOTH', supers=[], subs=[], required=[], single=[], enumsets=['ADOP'], enums=[])
    EnumCanceled = TagTuple(value='ENUMCANCELED', standard_tag='CANCELED', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumCard = TagTuple(value='ENUMCARD', standard_tag='CARD', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumCens = TagTuple(value='ENUMCENS', standard_tag='CENS', supers=[], subs=[], required=[], single=[], enumsets=['EVEN', 'EVENATTR'], enums=[])
    EnumChallenged = TagTuple(value='ENUMCHALLENGED', standard_tag='CHALLENGED', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumChil = TagTuple(value='ENUMCHIL', standard_tag='CHIL', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumChild = TagTuple(value='ENUMCHILD', standard_tag='CHILD', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumClergy = TagTuple(value='ENUMCLERGY', standard_tag='CLERGY', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumCompleted = TagTuple(value='ENUMCOMPLETED', standard_tag='COMPLETED', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumConfidential = TagTuple(value='ENUMCONFIDENTIAL', standard_tag='CONFIDENTIAL', supers=[], subs=[], required=[], single=[], enumsets=['RESN'], enums=[])
    EnumDisproven = TagTuple(value='ENUMDISPROVEN', standard_tag='DISPROVEN', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumDns = TagTuple(value='ENUMDNS', standard_tag='DNS', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumDns_Can = TagTuple(value='ENUMDNS_CAN', standard_tag='DNS_CAN', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumElectronic = TagTuple(value='ENUMELECTRONIC', standard_tag='ELECTRONIC', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumEven = TagTuple(value='ENUMEVEN', standard_tag='EVEN', supers=[], subs=[], required=[], single=[], enumsets=['EVENATTR'], enums=[])
    EnumExcluded = TagTuple(value='ENUMEXCLUDED', standard_tag='EXCLUDED', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumF = TagTuple(value='ENUMF', standard_tag='F', supers=[], subs=[], required=[], single=[], enumsets=['SEX'], enums=[])
    EnumFact = TagTuple(value='ENUMFACT', standard_tag='FACT', supers=[], subs=[], required=[], single=[], enumsets=['EVENATTR'], enums=[])
    EnumFath = TagTuple(value='ENUMFATH', standard_tag='FATH', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumFiche = TagTuple(value='ENUMFICHE', standard_tag='FICHE', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumFilm = TagTuple(value='ENUMFILM', standard_tag='FILM', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumFoster = TagTuple(value='ENUMFOSTER', standard_tag='FOSTER', supers=[], subs=[], required=[], single=[], enumsets=['PEDI'], enums=[])
    EnumFriend = TagTuple(value='ENUMFRIEND', standard_tag='FRIEND', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumGodp = TagTuple(value='ENUMGODP', standard_tag='GODP', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumHusb = TagTuple(value='ENUMHUSB', standard_tag='HUSB', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumImmigrant = TagTuple(value='ENUMIMMIGRANT', standard_tag='IMMIGRANT', supers=[], subs=[], required=[], single=[], enumsets=['TYPE'], enums=[])
    EnumInfant = TagTuple(value='ENUMINFANT', standard_tag='INFANT', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumLocked = TagTuple(value='ENUMLOCKED', standard_tag='LOCKED', supers=[], subs=[], required=[], single=[], enumsets=['RESN'], enums=[])
    EnumM = TagTuple(value='ENUMM', standard_tag='M', supers=[], subs=[], required=[], single=[], enumsets=['SEX'], enums=[])
    EnumMagazine = TagTuple(value='ENUMMAGAZINE', standard_tag='MAGAZINE', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumMaiden = TagTuple(value='ENUMMAIDEN', standard_tag='MAIDEN', supers=[], subs=[], required=[], single=[], enumsets=['TYPE'], enums=[])
    EnumManuscript = TagTuple(value='ENUMMANUSCRIPT', standard_tag='MANUSCRIPT', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumMap = TagTuple(value='ENUMMAP', standard_tag='MAP', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumMarried = TagTuple(value='ENUMMARRIED', standard_tag='MARRIED', supers=[], subs=[], required=[], single=[], enumsets=['TYPE'], enums=[])
    EnumMoth = TagTuple(value='ENUMMOTH', standard_tag='MOTH', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumMultiple = TagTuple(value='ENUMMULTIPLE', standard_tag='MULTIPLE', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumNchi = TagTuple(value='ENUMNCHI', standard_tag='NCHI', supers=[], subs=[], required=[], single=[], enumsets=['EVENATTR'], enums=[])
    EnumNewspaper = TagTuple(value='ENUMNEWSPAPER', standard_tag='NEWSPAPER', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumNghbr = TagTuple(value='ENUMNGHBR', standard_tag='NGHBR', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumOfficiator = TagTuple(value='ENUMOFFICIATOR', standard_tag='OFFICIATOR', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumOther = TagTuple(value='ENUMOTHER', standard_tag='OTHER', supers=[], subs=[], required=[], single=[], enumsets=['MEDI', 'TYPE', 'PEDI', 'ROLE'], enums=[])
    EnumParent = TagTuple(value='ENUMPARENT', standard_tag='PARENT', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumPhoto = TagTuple(value='ENUMPHOTO', standard_tag='PHOTO', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumPre_1970 = TagTuple(value='ENUMPRE_1970', standard_tag='PRE_1970', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumPrivacy = TagTuple(value='ENUMPRIVACY', standard_tag='PRIVACY', supers=[], subs=[], required=[], single=[], enumsets=['RESN'], enums=[])
    EnumProfessional = TagTuple(value='ENUMPROFESSIONAL', standard_tag='PROFESSIONAL', supers=[], subs=[], required=[], single=[], enumsets=['TYPE'], enums=[])
    EnumProven = TagTuple(value='ENUMPROVEN', standard_tag='PROVEN', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumResi = TagTuple(value='ENUMRESI', standard_tag='RESI', supers=[], subs=[], required=[], single=[], enumsets=['EVENATTR'], enums=[])
    EnumSealing = TagTuple(value='ENUMSEALING', standard_tag='SEALING', supers=[], subs=[], required=[], single=[], enumsets=['PEDI'], enums=[])
    EnumSpou = TagTuple(value='ENUMSPOU', standard_tag='SPOU', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumStillborn = TagTuple(value='ENUMSTILLBORN', standard_tag='STILLBORN', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumSubmitted = TagTuple(value='ENUMSUBMITTED', standard_tag='SUBMITTED', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumTombstone = TagTuple(value='ENUMTOMBSTONE', standard_tag='TOMBSTONE', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumU = TagTuple(value='ENUMU', standard_tag='U', supers=[], subs=[], required=[], single=[], enumsets=['SEX'], enums=[])
    EnumUncleared = TagTuple(value='ENUMUNCLEARED', standard_tag='UNCLEARED', supers=[], subs=[], required=[], single=[], enumsets=['STAT'], enums=[])
    EnumVideo = TagTuple(value='ENUMVIDEO', standard_tag='VIDEO', supers=[], subs=[], required=[], single=[], enumsets=['MEDI'], enums=[])
    EnumWife = TagTuple(value='ENUMWIFE', standard_tag='WIFE', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumWitn = TagTuple(value='ENUMWITN', standard_tag='WITN', supers=[], subs=[], required=[], single=[], enumsets=['ROLE'], enums=[])
    EnumX = TagTuple(value='ENUMX', standard_tag='X', supers=[], subs=[], required=[], single=[], enumsets=['SEX'], enums=[])
    EnumsetAdop = TagTuple(value='ENUMSETADOP', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=['HUSB', 'WIFE', 'BOTH'])
    EnumsetEven = TagTuple(value='ENUMSETEVEN', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=['CENS', 'https://gedcom.io/terms/v7/ADOP', 'https://gedcom.io/terms/v7/BAPM', 'https://gedcom.io/terms/v7/BARM', 'https://gedcom.io/terms/v7/BASM', 'https://gedcom.io/terms/v7/BIRT', 'https://gedcom.io/terms/v7/BLES', 'https://gedcom.io/terms/v7/BURI', 'https://gedcom.io/terms/v7/CHR', 'https://gedcom.io/terms/v7/CHRA', 'https://gedcom.io/terms/v7/CONF', 'https://gedcom.io/terms/v7/CREM', 'https://gedcom.io/terms/v7/DEAT', 'https://gedcom.io/terms/v7/EMIG', 'https://gedcom.io/terms/v7/FCOM', 'https://gedcom.io/terms/v7/GRAD', 'https://gedcom.io/terms/v7/IMMI', 'https://gedcom.io/terms/v7/NATU', 'https://gedcom.io/terms/v7/ORDN', 'https://gedcom.io/terms/v7/PROB', 'https://gedcom.io/terms/v7/RETI', 'https://gedcom.io/terms/v7/WILL', 'https://gedcom.io/terms/v7/ANUL', 'https://gedcom.io/terms/v7/DIV', 'https://gedcom.io/terms/v7/DIVF', 'https://gedcom.io/terms/v7/ENGA', 'https://gedcom.io/terms/v7/MARB', 'https://gedcom.io/terms/v7/MARC', 'https://gedcom.io/terms/v7/MARL', 'https://gedcom.io/terms/v7/MARR', 'https://gedcom.io/terms/v7/MARS'])
    EnumsetEvenattr = TagTuple(value='ENUMSETEVENATTR', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=['CENS', 'NCHI', 'RESI', 'FACT', 'EVEN', 'https://gedcom.io/terms/v7/ADOP', 'https://gedcom.io/terms/v7/BAPM', 'https://gedcom.io/terms/v7/BARM', 'https://gedcom.io/terms/v7/BASM', 'https://gedcom.io/terms/v7/BIRT', 'https://gedcom.io/terms/v7/BLES', 'https://gedcom.io/terms/v7/BURI', 'https://gedcom.io/terms/v7/CHR', 'https://gedcom.io/terms/v7/CHRA', 'https://gedcom.io/terms/v7/CONF', 'https://gedcom.io/terms/v7/CREM', 'https://gedcom.io/terms/v7/DEAT', 'https://gedcom.io/terms/v7/EMIG', 'https://gedcom.io/terms/v7/FCOM', 'https://gedcom.io/terms/v7/GRAD', 'https://gedcom.io/terms/v7/IMMI', 'https://gedcom.io/terms/v7/NATU', 'https://gedcom.io/terms/v7/ORDN', 'https://gedcom.io/terms/v7/PROB', 'https://gedcom.io/terms/v7/RETI', 'https://gedcom.io/terms/v7/WILL', 'https://gedcom.io/terms/v7/ANUL', 'https://gedcom.io/terms/v7/DIV', 'https://gedcom.io/terms/v7/DIVF', 'https://gedcom.io/terms/v7/ENGA', 'https://gedcom.io/terms/v7/MARB', 'https://gedcom.io/terms/v7/MARC', 'https://gedcom.io/terms/v7/MARL', 'https://gedcom.io/terms/v7/MARR', 'https://gedcom.io/terms/v7/MARS', 'https://gedcom.io/terms/v7/CAST', 'https://gedcom.io/terms/v7/DSCR', 'https://gedcom.io/terms/v7/EDUC', 'https://gedcom.io/terms/v7/IDNO', 'https://gedcom.io/terms/v7/NATI', 'https://gedcom.io/terms/v7/NMR', 'https://gedcom.io/terms/v7/OCCU', 'https://gedcom.io/terms/v7/PROP', 'https://gedcom.io/terms/v7/RELI', 'https://gedcom.io/terms/v7/SSN', 'https://gedcom.io/terms/v7/TITL'])
    EnumsetMedi = TagTuple(value='ENUMSETMEDI', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=['AUDIO', 'BOOK', 'CARD', 'ELECTRONIC', 'FICHE', 'FILM', 'MAGAZINE', 'MANUSCRIPT', 'MAP', 'NEWSPAPER', 'PHOTO', 'TOMBSTONE', 'VIDEO', 'OTHER'])
    EnumsetNameType = TagTuple(value='ENUMSETNAMETYPE', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=['AKA', 'BIRTH', 'IMMIGRANT', 'MAIDEN', 'MARRIED', 'PROFESSIONAL', 'OTHER'])
    EnumsetPedi = TagTuple(value='ENUMSETPEDI', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=['ADOPTED', 'BIRTH', 'FOSTER', 'SEALING', 'OTHER'])
    EnumsetQuay = TagTuple(value='ENUMSETQUAY', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=['0', '1', '2', '3'])
    EnumsetResn = TagTuple(value='ENUMSETRESN', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=['CONFIDENTIAL', 'LOCKED', 'PRIVACY'])
    EnumsetRole = TagTuple(value='ENUMSETROLE', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=['CHIL', 'CLERGY', 'FATH', 'FRIEND', 'GODP', 'HUSB', 'MOTH', 'MULTIPLE', 'NGHBR', 'OFFICIATOR', 'PARENT', 'SPOU', 'WIFE', 'WITN', 'OTHER'])
    EnumsetSex = TagTuple(value='ENUMSETSEX', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=['M', 'F', 'X', 'U'])
    EnumsetOrdStat = TagTuple(value='ENUMSETORDSTAT', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=['BIC', 'CANCELED', 'CHILD', 'COMPLETED', 'EXCLUDED', 'DNS', 'DNS_CAN', 'INFANT', 'PRE_1970', 'STILLBORN', 'SUBMITTED', 'UNCLEARED'])
    MonthAav = TagTuple(value='MONTHAAV', standard_tag='AAV', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthAdr = TagTuple(value='MONTHADR', standard_tag='ADR', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthAds = TagTuple(value='MONTHADS', standard_tag='ADS', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthApr = TagTuple(value='MONTHAPR', standard_tag='APR', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthAug = TagTuple(value='MONTHAUG', standard_tag='AUG', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthBrum = TagTuple(value='MONTHBRUM', standard_tag='BRUM', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthComp = TagTuple(value='MONTHCOMP', standard_tag='COMP', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthCsh = TagTuple(value='MONTHCSH', standard_tag='CSH', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthDec = TagTuple(value='MONTHDEC', standard_tag='DEC', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthEll = TagTuple(value='MONTHELL', standard_tag='ELL', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthFeb = TagTuple(value='MONTHFEB', standard_tag='FEB', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthFlor = TagTuple(value='MONTHFLOR', standard_tag='FLOR', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthFrim = TagTuple(value='MONTHFRIM', standard_tag='FRIM', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthFruc = TagTuple(value='MONTHFRUC', standard_tag='FRUC', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthGerm = TagTuple(value='MONTHGERM', standard_tag='GERM', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthIyr = TagTuple(value='MONTHIYR', standard_tag='IYR', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthJan = TagTuple(value='MONTHJAN', standard_tag='JAN', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthJul = TagTuple(value='MONTHJUL', standard_tag='JUL', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthJun = TagTuple(value='MONTHJUN', standard_tag='JUN', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthKsl = TagTuple(value='MONTHKSL', standard_tag='KSL', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthMar = TagTuple(value='MONTHMAR', standard_tag='MAR', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthMay = TagTuple(value='MONTHMAY', standard_tag='MAY', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthMess = TagTuple(value='MONTHMESS', standard_tag='MESS', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthNivo = TagTuple(value='MONTHNIVO', standard_tag='NIVO', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthNov = TagTuple(value='MONTHNOV', standard_tag='NOV', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthNsn = TagTuple(value='MONTHNSN', standard_tag='NSN', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthOct = TagTuple(value='MONTHOCT', standard_tag='OCT', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthPluv = TagTuple(value='MONTHPLUV', standard_tag='PLUV', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthPrai = TagTuple(value='MONTHPRAI', standard_tag='PRAI', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthSep = TagTuple(value='MONTHSEP', standard_tag='SEP', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthShv = TagTuple(value='MONTHSHV', standard_tag='SHV', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthSvn = TagTuple(value='MONTHSVN', standard_tag='SVN', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthTher = TagTuple(value='MONTHTHER', standard_tag='THER', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthTmz = TagTuple(value='MONTHTMZ', standard_tag='TMZ', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthTsh = TagTuple(value='MONTHTSH', standard_tag='TSH', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthTvt = TagTuple(value='MONTHTVT', standard_tag='TVT', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthVend = TagTuple(value='MONTHVEND', standard_tag='VEND', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    MonthVent = TagTuple(value='MONTHVENT', standard_tag='VENT', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    OrdStat = TagTuple(value='ORDSTAT', standard_tag='STAT', supers=['Bapl', 'Conl', 'Endl', 'Inil', 'Slgc', 'Slgs'], subs=['DateExact'], required=['DateExact'], single=['DateExact'], enumsets=[], enums=[])
    RecordFam = TagTuple(value='RECORDFAM', standard_tag='FAM', supers=[], subs=['Anul', 'Asso', 'Chan', 'Chil', 'Crea', 'Div', 'Divf', 'Enga', 'Exid', 'FamCens', 'FamEven', 'FamFact', 'FamHusb', 'FamNchi', 'FamResi', 'FamWife', 'Marb', 'Marc', 'Marl', 'Marr', 'Mars', 'No', 'Note', 'Obje', 'Refn', 'Resn', 'Slgs', 'Snote', 'Sour', 'Subm', 'Uid'], required=[], single=['Chan', 'Crea', 'FamHusb', 'FamWife', 'Resn'], enumsets=[], enums=[])
    RecordIndi = TagTuple(value='RECORDINDI', standard_tag='INDI', supers=[], subs=['Adop', 'Alia', 'Anci', 'Asso', 'Bapl', 'Bapm', 'Barm', 'Basm', 'Birt', 'Bles', 'Buri', 'Cast', 'Chan', 'Chr', 'Chra', 'Conf', 'Conl', 'Crea', 'Crem', 'Deat', 'Desi', 'Dscr', 'Educ', 'Emig', 'Endl', 'Exid', 'Fams', 'Fcom', 'Grad', 'Idno', 'Immi', 'IndiCens', 'IndiEven', 'IndiFact', 'IndiFamc', 'IndiName', 'IndiNchi', 'IndiReli', 'IndiResi', 'IndiTitl', 'Inil', 'Nati', 'Natu', 'Nmr', 'No', 'Note', 'Obje', 'Occu', 'Ordn', 'Prob', 'Prop', 'Refn', 'Resn', 'Reti', 'Sex', 'Slgc', 'Snote', 'Sour', 'Ssn', 'Subm', 'Uid', 'Will'], required=[], single=['Chan', 'Crea', 'Resn', 'Sex'], enumsets=[], enums=[])
    RecordObje = TagTuple(value='RECORDOBJE', standard_tag='OBJE', supers=[], subs=['Chan', 'Crea', 'Exid', 'File', 'Note', 'Refn', 'Resn', 'Snote', 'Sour', 'Uid'], required=['File'], single=['Chan', 'Crea', 'Resn'], enumsets=[], enums=[])
    RecordRepo = TagTuple(value='RECORDREPO', standard_tag='REPO', supers=[], subs=['Addr', 'Chan', 'Crea', 'Email', 'Exid', 'Fax', 'Name', 'Note', 'Phon', 'Refn', 'Snote', 'Uid', 'Www'], required=['Name'], single=['Addr', 'Chan', 'Crea', 'Name'], enumsets=[], enums=[])
    RecordSnote = TagTuple(value='RECORDSNOTE', standard_tag='SNOTE', supers=[], subs=['Chan', 'Crea', 'Exid', 'Lang', 'Mime', 'NoteTran', 'Refn', 'Sour', 'Uid'], required=[], single=['Chan', 'Crea', 'Lang', 'Mime'], enumsets=[], enums=[])
    RecordSour = TagTuple(value='RECORDSOUR', standard_tag='SOUR', supers=[], subs=['Abbr', 'Auth', 'Chan', 'Crea', 'Data', 'Exid', 'Note', 'Obje', 'Publ', 'Refn', 'Repo', 'Snote', 'Text', 'Titl', 'Uid'], required=[], single=['Abbr', 'Auth', 'Chan', 'Crea', 'Data', 'Publ', 'Text', 'Titl'], enumsets=[], enums=[])
    RecordSubm = TagTuple(value='RECORDSUBM', standard_tag='SUBM', supers=[], subs=['Addr', 'Chan', 'Crea', 'Email', 'Exid', 'Fax', 'Name', 'Note', 'Obje', 'Phon', 'Refn', 'Snote', 'SubmLang', 'Uid', 'Www'], required=['Name'], single=['Addr', 'Chan', 'Crea', 'Name'], enumsets=[], enums=[])
    TypeAge = TagTuple(value='TYPEAGE', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    TypeDate = TagTuple(value='TYPEDATE', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    TypeEnum = TagTuple(value='TYPEENUM', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    TypeFilepath = TagTuple(value='TYPEFILEPATH', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    TypeList = TagTuple(value='TYPELIST', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    TypeName = TagTuple(value='TYPENAME', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
    TypeTime = TagTuple(value='TYPETIME', standard_tag='', supers=[], subs=[], required=[], single=[], enumsets=[], enums=[])
