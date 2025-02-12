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


@dataclass(frozen=True)
class Docs:
    ABBR = 'https://gedcom.io/terms/v7/ABBR'
    ADDR = 'https://gedcom.io/terms/v7/ADDR'
    ADOP = 'https://gedcom.io/terms/v7/ADOP'
    ADOP_FAMC = 'https://gedcom.io/terms/v7/ADOP-FAMC'
    ADR1 = 'https://gedcom.io/terms/v7/ADR1'
    ADR2 = 'https://gedcom.io/terms/v7/ADR2'
    ADR3 = 'https://gedcom.io/terms/v7/ADR3'
    AGE = 'https://gedcom.io/terms/v7/AGE'
    AGNC = 'https://gedcom.io/terms/v7/AGNC'
    ALIA = 'https://gedcom.io/terms/v7/ALIA'
    ANCI = 'https://gedcom.io/terms/v7/ANCI'
    ANUL = 'https://gedcom.io/terms/v7/ANUL'
    ASSO = 'https://gedcom.io/terms/v7/ASSO'
    AUTH = 'https://gedcom.io/terms/v7/AUTH'
    BAPL = 'https://gedcom.io/terms/v7/BAPL'
    BAPM = 'https://gedcom.io/terms/v7/BAPM'
    BARM = 'https://gedcom.io/terms/v7/BARM'
    BASM = 'https://gedcom.io/terms/v7/BASM'
    BIRT = 'https://gedcom.io/terms/v7/BIRT'
    BLES = 'https://gedcom.io/terms/v7/BLES'
    BURI = 'https://gedcom.io/terms/v7/BURI'
    CALN = 'https://gedcom.io/terms/v7/CALN'
    CAST = 'https://gedcom.io/terms/v7/CAST'
    CAUS = 'https://gedcom.io/terms/v7/CAUS'
    CHAN = 'https://gedcom.io/terms/v7/CHAN'
    CHIL = 'https://gedcom.io/terms/v7/CHIL'
    CHR = 'https://gedcom.io/terms/v7/CHR'
    CHRA = 'https://gedcom.io/terms/v7/CHRA'
    CITY = 'https://gedcom.io/terms/v7/CITY'
    CONF = 'https://gedcom.io/terms/v7/CONF'
    CONL = 'https://gedcom.io/terms/v7/CONL'
    COPR = 'https://gedcom.io/terms/v7/COPR'
    CORP = 'https://gedcom.io/terms/v7/CORP'
    CREA = 'https://gedcom.io/terms/v7/CREA'
    CREM = 'https://gedcom.io/terms/v7/CREM'
    CROP = 'https://gedcom.io/terms/v7/CROP'
    CTRY = 'https://gedcom.io/terms/v7/CTRY'
    DATA = 'https://gedcom.io/terms/v7/DATA'
    DATA_EVEN = 'https://gedcom.io/terms/v7/DATA-EVEN'
    DATA_EVEN_DATE = 'https://gedcom.io/terms/v7/DATA-EVEN-DATE'
    DATE = 'https://gedcom.io/terms/v7/DATE'
    DATE_EXACT = 'https://gedcom.io/terms/v7/DATE-exact'
    DEAT = 'https://gedcom.io/terms/v7/DEAT'
    DESI = 'https://gedcom.io/terms/v7/DESI'
    DEST = 'https://gedcom.io/terms/v7/DEST'
    DIV = 'https://gedcom.io/terms/v7/DIV'
    DIVF = 'https://gedcom.io/terms/v7/DIVF'
    DSCR = 'https://gedcom.io/terms/v7/DSCR'
    EDUC = 'https://gedcom.io/terms/v7/EDUC'
    EMAIL = 'https://gedcom.io/terms/v7/EMAIL'
    EMIG = 'https://gedcom.io/terms/v7/EMIG'
    ENDL = 'https://gedcom.io/terms/v7/ENDL'
    ENGA = 'https://gedcom.io/terms/v7/ENGA'
    EXID = 'https://gedcom.io/terms/v7/EXID'
    EXID_TYPE = 'https://gedcom.io/terms/v7/EXID-TYPE'
    FAM_CENS = 'https://gedcom.io/terms/v7/FAM-CENS'
    FAM_EVEN = 'https://gedcom.io/terms/v7/FAM-EVEN'
    FAM_FACT = 'https://gedcom.io/terms/v7/FAM-FACT'
    FAM_HUSB = 'https://gedcom.io/terms/v7/FAM-HUSB'
    FAM_NCHI = 'https://gedcom.io/terms/v7/FAM-NCHI'
    FAM_RESI = 'https://gedcom.io/terms/v7/FAM-RESI'
    FAM_WIFE = 'https://gedcom.io/terms/v7/FAM-WIFE'
    FAMC = 'https://gedcom.io/terms/v7/FAMC'
    FAMC_ADOP = 'https://gedcom.io/terms/v7/FAMC-ADOP'
    FAMC_STAT = 'https://gedcom.io/terms/v7/FAMC-STAT'
    FAMS = 'https://gedcom.io/terms/v7/FAMS'
    FAX = 'https://gedcom.io/terms/v7/FAX'
    FCOM = 'https://gedcom.io/terms/v7/FCOM'
    FILE = 'https://gedcom.io/terms/v7/FILE'
    FILE_TRAN = 'https://gedcom.io/terms/v7/FILE-TRAN'
    FORM = 'https://gedcom.io/terms/v7/FORM'
    GEDC = 'https://gedcom.io/terms/v7/GEDC'
    GEDC_VERS = 'https://gedcom.io/terms/v7/GEDC-VERS'
    GIVN = 'https://gedcom.io/terms/v7/GIVN'
    GRAD = 'https://gedcom.io/terms/v7/GRAD'
    HEAD = 'https://gedcom.io/terms/v7/HEAD'
    HEAD_DATE = 'https://gedcom.io/terms/v7/HEAD-DATE'
    HEAD_PLAC = 'https://gedcom.io/terms/v7/HEAD-PLAC'
    HEAD_PLAC_FORM = 'https://gedcom.io/terms/v7/HEAD-PLAC-FORM'
    HEAD_SOUR = 'https://gedcom.io/terms/v7/HEAD-SOUR'
    HEAD_SOUR_DATA = 'https://gedcom.io/terms/v7/HEAD-SOUR-DATA'
    HEIGHT = 'https://gedcom.io/terms/v7/HEIGHT'
    HUSB = 'https://gedcom.io/terms/v7/HUSB'
    IDNO = 'https://gedcom.io/terms/v7/IDNO'
    IMMI = 'https://gedcom.io/terms/v7/IMMI'
    INDI_CENS = 'https://gedcom.io/terms/v7/INDI-CENS'
    INDI_EVEN = 'https://gedcom.io/terms/v7/INDI-EVEN'
    INDI_FACT = 'https://gedcom.io/terms/v7/INDI-FACT'
    INDI_FAMC = 'https://gedcom.io/terms/v7/INDI-FAMC'
    INDI_NAME = 'https://gedcom.io/terms/v7/INDI-NAME'
    INDI_NCHI = 'https://gedcom.io/terms/v7/INDI-NCHI'
    INDI_RELI = 'https://gedcom.io/terms/v7/INDI-RELI'
    INDI_RESI = 'https://gedcom.io/terms/v7/INDI-RESI'
    INDI_TITL = 'https://gedcom.io/terms/v7/INDI-TITL'
    INIL = 'https://gedcom.io/terms/v7/INIL'
    LANG = 'https://gedcom.io/terms/v7/LANG'
    LATI = 'https://gedcom.io/terms/v7/LATI'
    LEFT = 'https://gedcom.io/terms/v7/LEFT'
    LONG = 'https://gedcom.io/terms/v7/LONG'
    MAP = 'https://gedcom.io/terms/v7/MAP'
    MARB = 'https://gedcom.io/terms/v7/MARB'
    MARC = 'https://gedcom.io/terms/v7/MARC'
    MARL = 'https://gedcom.io/terms/v7/MARL'
    MARR = 'https://gedcom.io/terms/v7/MARR'
    MARS = 'https://gedcom.io/terms/v7/MARS'
    MEDI = 'https://gedcom.io/terms/v7/MEDI'
    MIME = 'https://gedcom.io/terms/v7/MIME'
    NAME = 'https://gedcom.io/terms/v7/NAME'
    NAME_TRAN = 'https://gedcom.io/terms/v7/NAME-TRAN'
    NAME_TYPE = 'https://gedcom.io/terms/v7/NAME-TYPE'
    NATI = 'https://gedcom.io/terms/v7/NATI'
    NATU = 'https://gedcom.io/terms/v7/NATU'
    NICK = 'https://gedcom.io/terms/v7/NICK'
    NMR = 'https://gedcom.io/terms/v7/NMR'
    NO = 'https://gedcom.io/terms/v7/NO'
    NO_DATE = 'https://gedcom.io/terms/v7/NO-DATE'
    NOTE = 'https://gedcom.io/terms/v7/NOTE'
    NOTE_TRAN = 'https://gedcom.io/terms/v7/NOTE-TRAN'
    NPFX = 'https://gedcom.io/terms/v7/NPFX'
    NSFX = 'https://gedcom.io/terms/v7/NSFX'
    OBJE = 'https://gedcom.io/terms/v7/OBJE'
    OCCU = 'https://gedcom.io/terms/v7/OCCU'
    ORD_STAT = 'https://gedcom.io/terms/v7/ord-STAT'
    ORDN = 'https://gedcom.io/terms/v7/ORDN'
    PAGE = 'https://gedcom.io/terms/v7/PAGE'
    PEDI = 'https://gedcom.io/terms/v7/PEDI'
    PHON = 'https://gedcom.io/terms/v7/PHON'
    PHRASE = 'https://gedcom.io/terms/v7/PHRASE'
    PLAC = 'https://gedcom.io/terms/v7/PLAC'
    PLAC_FORM = 'https://gedcom.io/terms/v7/PLAC-FORM'
    PLAC_TRAN = 'https://gedcom.io/terms/v7/PLAC-TRAN'
    POST = 'https://gedcom.io/terms/v7/POST'
    PROB = 'https://gedcom.io/terms/v7/PROB'
    PROP = 'https://gedcom.io/terms/v7/PROP'
    PUBL = 'https://gedcom.io/terms/v7/PUBL'
    QUAY = 'https://gedcom.io/terms/v7/QUAY'
    RECORD_FAM = 'https://gedcom.io/terms/v7/record-FAM'
    RECORD_INDI = 'https://gedcom.io/terms/v7/record-INDI'
    RECORD_OBJE = 'https://gedcom.io/terms/v7/record-OBJE'
    RECORD_REPO = 'https://gedcom.io/terms/v7/record-REPO'
    RECORD_SNOTE = 'https://gedcom.io/terms/v7/record-SNOTE'
    RECORD_SOUR = 'https://gedcom.io/terms/v7/record-SOUR'
    RECORD_SUBM = 'https://gedcom.io/terms/v7/record-SUBM'
    REFN = 'https://gedcom.io/terms/v7/REFN'
    RELI = 'https://gedcom.io/terms/v7/RELI'
    REPO = 'https://gedcom.io/terms/v7/REPO'
    RESN = 'https://gedcom.io/terms/v7/RESN'
    RETI = 'https://gedcom.io/terms/v7/RETI'
    ROLE = 'https://gedcom.io/terms/v7/ROLE'
    SCHMA = 'https://gedcom.io/terms/v7/SCHMA'
    SDATE = 'https://gedcom.io/terms/v7/SDATE'
    SEX = 'https://gedcom.io/terms/v7/SEX'
    SLGC = 'https://gedcom.io/terms/v7/SLGC'
    SLGS = 'https://gedcom.io/terms/v7/SLGS'
    SNOTE = 'https://gedcom.io/terms/v7/SNOTE'
    SOUR = 'https://gedcom.io/terms/v7/SOUR'
    SOUR_DATA = 'https://gedcom.io/terms/v7/SOUR-DATA'
    SOUR_EVEN = 'https://gedcom.io/terms/v7/SOUR-EVEN'
    SPFX = 'https://gedcom.io/terms/v7/SPFX'
    SSN = 'https://gedcom.io/terms/v7/SSN'
    STAE = 'https://gedcom.io/terms/v7/STAE'
    SUBM = 'https://gedcom.io/terms/v7/SUBM'
    SUBM_LANG = 'https://gedcom.io/terms/v7/SUBM-LANG'
    SURN = 'https://gedcom.io/terms/v7/SURN'
    TAG = 'https://gedcom.io/terms/v7/TAG'
    TEMP = 'https://gedcom.io/terms/v7/TEMP'
    TEXT = 'https://gedcom.io/terms/v7/TEXT'
    TIME = 'https://gedcom.io/terms/v7/TIME'
    TITL = 'https://gedcom.io/terms/v7/TITL'
    TOP = 'https://gedcom.io/terms/v7/TOP'
    TYPE = 'https://gedcom.io/terms/v7/TYPE'
    UID = 'https://gedcom.io/terms/v7/UID'
    VERS = 'https://gedcom.io/terms/v7/VERS'
    WIDTH = 'https://gedcom.io/terms/v7/WIDTH'
    WIFE = 'https://gedcom.io/terms/v7/WIFE'
    WILL = 'https://gedcom.io/terms/v7/WILL'
    WWW = 'https://gedcom.io/terms/v7/WWW'


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
        >>> print(OverView.HEADER)  # doctest: +ELLIPSIS
        <BLANKLINE>
        0 HEAD                                 {1:1}  [g7:HEAD](https://gedcom.io/terms/v7/HEAD)
          1 GEDC                               {1:1}  [g7:GEDC](https://gedcom.io/terms/v7/GEDC)
            2 VERS <Special>                   {1:1}  [g7:GEDC-VERS](https://gedcom.io/terms/v7/GEDC-VERS)
          1 SCHMA                              {0:1}  [g7:SCHMA](https://gedcom.io/terms/v7/SCHMA)
            2 TAG <Special>                    {0:M}  [g7:TAG](https://gedcom.io/terms/v7/TAG)
          1 SOUR <Special>                     {0:1}  [g7:HEAD-SOUR](https://gedcom.io/terms/v7/HEAD-SOUR)
            2 VERS <Special>                   {0:1}  [g7:VERS](https://gedcom.io/terms/v7/VERS)
            2 NAME <Text>                      {0:1}  [g7:NAME](https://gedcom.io/terms/v7/NAME)
            2 CORP <Text>                      {0:1}  [g7:CORP](https://gedcom.io/terms/v7/CORP)
              3 <<ADDRESS_STRUCTURE>>          {0:1}
              3 PHON <Special>                 {0:M}  [g7:PHON](https://gedcom.io/terms/v7/PHON)
              3 EMAIL <Special>                {0:M}  [g7:EMAIL](https://gedcom.io/terms/v7/EMAIL)
              3 FAX <Special>                  {0:M}  [g7:FAX](https://gedcom.io/terms/v7/FAX)
              3 WWW <Special>                  {0:M}  [g7:WWW](https://gedcom.io/terms/v7/WWW)
            2 DATA <Text>                      {0:1}  [g7:HEAD-SOUR-DATA](https://gedcom.io/terms/v7/HEAD-SOUR-DATA)
              3 DATE <DateExact>               {0:1}  [g7:DATE-exact](https://gedcom.io/terms/v7/DATE-exact)
                4 TIME <Time>                  {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
              3 COPR <Text>                    {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
          1 DEST <Special>                     {0:1}  [g7:DEST](https://gedcom.io/terms/v7/DEST)
          1 DATE <DateExact>                   {0:1}  [g7:HEAD-DATE](https://gedcom.io/terms/v7/HEAD-DATE)
            2 TIME <Time>                      {0:1}  [g7:TIME](https://gedcom.io/terms/v7/TIME)
          1 SUBM @<XREF:SUBM>@                 {0:1}  [g7:SUBM](https://gedcom.io/terms/v7/SUBM)
          1 COPR <Text>                        {0:1}  [g7:COPR](https://gedcom.io/terms/v7/COPR)
          1 LANG <Language>                    {0:1}  [g7:HEAD-LANG](https://gedcom.io/terms/v7/LANG)
          1 PLAC                               {0:1}  [g7:HEAD-PLAC](https://gedcom.io/terms/v7/HEAD-PLAC)
            2 FORM <List:Text>                 {1:1}  [g7:HEAD-PLAC-FORM](https://gedcom.io/terms/v7/HEAD-PLAC-FORM)
          1 <<NOTE_STRUCTURE>>                 {0:1}
        <BLANKLINE>

    Reference:
        [The FamilySearch GEDCOM Specifications](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html)
    """

    ADDRESS_STRUCTURE: str = f"""
n ADDR <Special>                       {{1:1}}  [g7:ADDR]({Docs.ADDR})
  +1 ADR1 <Special>                    {{0:1}}  [g7:ADR1]({Docs.ADR1})
  +1 ADR2 <Special>                    {{0:1}}  [g7:ADR2]({Docs.ADR2})
  +1 ADR3 <Special>                    {{0:1}}  [g7:ADR3]({Docs.ADR3})
  +1 CITY <Special>                    {{0:1}}  [g7:CITY]({Docs.CITY})
  +1 STAE <Special>                    {{0:1}}  [g7:STAE]({Docs.STAE})
  +1 POST <Special>                    {{0:1}}  [g7:POST]({Docs.POST})
  +1 CTRY <Special>                    {{0:1}}  [g7:CTRY]({Docs.CTRY})  
"""
    ASSOCIATION_STRUCTURE: str = f"""
n ASSO @<XREF:INDI>@                   {{1:1}}  [g7:ASSO]({Docs.ASSO})
  +1 PHRASE <Text>                     {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
  +1 ROLE <Enum>                       {{1:1}}  [g7:ROLE]({Docs.ROLE})
     +2 PHRASE <Text>                  {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
  +1 <<SOURCE_CITATION>>               {{0:M}}
"""
    CHANGE_DATE: str = f"""
n CHAN                                 {{1:1}}  [g7:CHAN]({Docs.CHAN})
  +1 DATE <DateExact>                  {{1:1}}  [g7:DATE-exact]({Docs.DATE_EXACT})
     +2 TIME <Time>                    {{0:1}}  [g7:TIME]({Docs.TIME})
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
"""
    CREATION_DATE: str = f"""
n CREA                                 {{1:1}}  [g7:CREA]({Docs.CREA})
  +1 DATE <DateExact>                  {{1:1}}  [g7:DATE-exact]({Docs.DATE_EXACT})
     +2 TIME <Time>                    {{0:1}}  [g7:TIME]({Docs.TIME})
"""
    DATE_VALUE: str = f"""
n DATE <DateValue>                     {{1:1}}  [g7:DATE]({Docs.DATE})
  +1 TIME <Time>                       {{0:1}}  [g7:TIME]({Docs.TIME})
  +1 PHRASE <Text>                     {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
"""
    EVENT_DETAIL: str = f"""
n <<DATE_VALUE>>                       {{0:1}}
n <<PLACE_STRUCTURE>>                  {{0:1}}
n <<ADDRESS_STRUCTURE>>                {{0:1}}
n PHON <Special>                       {{0:M}}  [g7:PHON]({Docs.PHON})
n EMAIL <Special>                      {{0:M}}  [g7:EMAIL]({Docs.EMAIL})
n FAX <Special>                        {{0:M}}  [g7:FAX]({Docs.FAX})
n WWW <Special>                        {{0:M}}  [g7:WWW]({Docs.WWW})
n AGNC <Text>                          {{0:1}}  [g7:AGNC]({Docs.AGNC})
n RELI <Text>                          {{0:1}}  [g7:RELI]({Docs.RELI})
n CAUS <Text>                          {{0:1}}  [g7:CAUS]({Docs.CAUS})
n RESN <List:Enum>                     {{0:1}}  [g7:RESN]({Docs.RESN})
n SDATE <DateValue>                    {{0:1}}  [g7:SDATE]({Docs.SDATE})
  +1 TIME <Time>                       {{0:1}}  [g7:TIME]({Docs.TIME})
  +1 PHRASE <Text>                     {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
n <<ASSOCIATION_STRUCTURE>>            {{0:M}}
n <<NOTE_STRUCTURE>>                   {{0:M}}
n <<SOURCE_CITATION>>                  {{0:M}}
n <<MULTIMEDIA_LINK>>                  {{0:M}}
n UID <Special>                        {{0:M}}  [g7:UID]()
"""
    FAMILY: str = f"""
0 @XREF:FAM@ FAM                       {{1:1}}  [g7:record-FAM]({Docs.RECORD_FAM})
  1 RESN <List:Enum>                   {{0:1}}  [g7:RESN]({Docs.RESN})
  1 <<FAMILY_ATTRIBUTE_STRUCTURE>>     {{0:M}}
  1 <<FAMILY_EVENT_STRUCTURE>>         {{0:M}}
  1 <<NON_EVENT_STRUCTURE>>            {{0:M}}
  1 HUSB @<XREF:INDI>@                 {{0:1}}  [g7:FAM-HUSB]({Docs.FAM_HUSB})
    2 PHRASE <Text>                    {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
  1 WIFE @<XREF:INDI>@                 {{0:1}}  [g7:FAM-WIFE]({Docs.FAM_WIFE})
    2 PHRASE <Text>                    {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
  1 CHIL @<XREF:INDI>@                 {{0:M}}  [g7:CHIL]({Docs.CHIL})
    2 PHRASE <Text>                    {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
  1 <<ASSOCIATION_STRUCTURE>>          {{0:M}}
  1 SUBM @<XREF:SUBM>@                 {{0:M}}  [g7:SUBM]({Docs.SUBM})
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
n NCHI <Integer>                       {{1:1}}  [g7:FAM-NCHI]({Docs.FAM_NCHI})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n RESI <Text>                          {{1:1}}  [g7:FAM-RESI]({Docs.FAM_RESI})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n FACT <Text>                          {{1:1}}  [g7:FAM-FACT]({Docs.FAM_FACT})
  +1 TYPE <Text>                       {{1:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
]
"""
    FAMILY_EVENT_DETAIL: str = f"""
n HUSB                                 {{0:1}}  [g7:HUSB]({Docs.HUSB})
  +1 AGE <Age>                         {{1:1}}  [g7:AGE]({Docs.AGE})
     +2 PHRASE <Text>                  {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
n WIFE                                 {{0:1}}  [g7:WIFE]({Docs.WIFE})
  +1 AGE <Age>                         {{1:1}}  [g7:AGE]({Docs.AGE})
     +2 PHRASE <Text>                  {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
n <<EVENT_DETAIL>>                     {{0:1}}
"""
    FAMILY_EVENT_STRUCTURE: str = f"""
[
n ANUL [Y|<NULL>]                      {{1:1}}  [g7:ANUL]({Docs.ANUL})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n CENS [Y|<NULL>]                      {{1:1}}  [g7:FAM-CENS]({Docs.FAM_CENS})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n DIV [Y|<NULL>]                       {{1:1}}  [g7:DIV]({Docs.DIV})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n DIVF [Y|<NULL>]                      {{1:1}}  [g7:DIVF]({Docs.DIVF})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n ENGA [Y|<NULL>]                      {{1:1}}  [g7:ENGA]({Docs.ENGA})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n MARB [Y|<NULL>]                      {{1:1}}  [g7:MARB]({Docs.MARB})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n MARC [Y|<NULL>]                      {{1:1}}  [g7:MARC]({Docs.MARC})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n MARL [Y|<NULL>]                      {{1:1}}  [g7:MARL]({Docs.MARL})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n MARR [Y|<NULL>]                      {{1:1}}  [g7:MARR]({Docs.MARR})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n MARS [Y|<NULL>]                      {{1:1}}  [g7:MARS]({Docs.MARS})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
|
n EVEN <Text>                          {{1:1}}  [g7:FAM-EVEN]({Docs.FAM_EVEN})
  +1 TYPE <Text>                       {{1:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<FAMILY_EVENT_DETAIL>>           {{0:1}}
]
"""
    HEADER: str = f"""
0 HEAD                                 {{1:1}}  [g7:HEAD]({Docs.HEAD})
  1 GEDC                               {{1:1}}  [g7:GEDC]({Docs.GEDC})
    2 VERS <Special>                   {{1:1}}  [g7:GEDC-VERS]({Docs.GEDC_VERS})
  1 SCHMA                              {{0:1}}  [g7:SCHMA]({Docs.SCHMA})
    2 TAG <Special>                    {{0:M}}  [g7:TAG]({Docs.TAG})
  1 SOUR <Special>                     {{0:1}}  [g7:HEAD-SOUR]({Docs.HEAD_SOUR})
    2 VERS <Special>                   {{0:1}}  [g7:VERS]({Docs.VERS})
    2 NAME <Text>                      {{0:1}}  [g7:NAME]({Docs.NAME})
    2 CORP <Text>                      {{0:1}}  [g7:CORP]({Docs.CORP})
      3 <<ADDRESS_STRUCTURE>>          {{0:1}}
      3 PHON <Special>                 {{0:M}}  [g7:PHON]({Docs.PHON})
      3 EMAIL <Special>                {{0:M}}  [g7:EMAIL]({Docs.EMAIL})
      3 FAX <Special>                  {{0:M}}  [g7:FAX]({Docs.FAX})
      3 WWW <Special>                  {{0:M}}  [g7:WWW]({Docs.WWW})
    2 DATA <Text>                      {{0:1}}  [g7:HEAD-SOUR-DATA]({Docs.HEAD_SOUR_DATA})
      3 DATE <DateExact>               {{0:1}}  [g7:DATE-exact]({Docs.DATE_EXACT})
        4 TIME <Time>                  {{0:1}}  [g7:TIME]({Docs.TIME})
      3 COPR <Text>                    {{0:1}}  [g7:COPR]({Docs.COPR})
  1 DEST <Special>                     {{0:1}}  [g7:DEST]({Docs.DEST})
  1 DATE <DateExact>                   {{0:1}}  [g7:HEAD-DATE]({Docs.HEAD_DATE})
    2 TIME <Time>                      {{0:1}}  [g7:TIME]({Docs.TIME})
  1 SUBM @<XREF:SUBM>@                 {{0:1}}  [g7:SUBM]({Docs.SUBM})
  1 COPR <Text>                        {{0:1}}  [g7:COPR]({Docs.COPR})
  1 LANG <Language>                    {{0:1}}  [g7:HEAD-LANG]({Docs.LANG})
  1 PLAC                               {{0:1}}  [g7:HEAD-PLAC]({Docs.HEAD_PLAC})
    2 FORM <List:Text>                 {{1:1}}  [g7:HEAD-PLAC-FORM]({Docs.HEAD_PLAC_FORM})
  1 <<NOTE_STRUCTURE>>                 {{0:1}}
    """
    IDENTIFIER_STRUCTURE: str = f"""
[
n REFN <Special>                       {{1:1}}  [g7:REFN]({Docs.REFN})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
|
n UID <Special>                        {{1:1}}  [g7:UID]({Docs.UID})
|
n EXID <Special>                       {{1:1}}  [g7:EXID]({Docs.EXID})
  +1 TYPE <Special>                    {{0:1}}  [g7:EXID-TYPE]({Docs.EXID_TYPE})
]
"""
    INDIVIDUAL: str = f"""
0 @XREF:INDI@ INDI                     {{1:1}}  [g7:record-INDI]({Docs.RECORD_INDI})
  1 RESN <List:Enum>                   {{0:1}}  [g7:RESN]({Docs.RESN})
  1 <<PERSONAL_NAME_STRUCTURE>>        {{0:M}}
  1 SEX <Enum>                         {{0:1}}  [g7:SEX]({Docs.SEX})
  1 <<INDIVIDUAL_ATTRIBUTE_STRUCTURE>> {{0:M}}
  1 <<INDIVIDUAL_EVENT_STRUCTURE>>     {{0:M}}
  1 <<NON_EVENT_STRUCTURE>>            {{0:M}}
  1 <<LDS_INDIVIDUAL_ORDINANCE>>       {{0:M}}
  1 FAMC @<XREF:FAM>@                  {{0:M}}  [g7:INDI-FAMC]({Docs.INDI_FAMC})
    2 PEDI <Enum>                      {{0:1}}  [g7:PEDI]({Docs.PEDI})
      3 PHRASE <Text>                  {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
    2 STAT <Enum>                      {{0:1}}  [g7:FAMC-STAT]({Docs.FAMC_STAT})
      3 PHRASE <Text>                  {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
    2 <<NOTE_STRUCTURE>>               {{0:M}}
  1 FAMS @<XREF:FAM>@                  {{0:M}}  [g7:FAMS]({Docs.FAMS})
    2 <<NOTE_STRUCTURE>>               {{0:M}}
  1 SUBM @<XREF:SUBM>@                 {{0:M}}  [g7:SUBM]({Docs.SUBM})
  1 <<ASSOCIATION_STRUCTURE>>          {{0:M}}
  1 ALIA @<XREF:INDI>@                 {{0:M}}  [g7:ALIA]({Docs.ALIA})
    2 PHRASE <Text>                    {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
  1 ANCI @<XREF:SUBM>@                 {{0:M}}  [g7:ANCI]({Docs.ANCI})
  1 DESI @<XREF:SUBM>@                 {{0:M}}  [g7:DESI]({Docs.DESI})
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<NOTE_STRUCTURE>>                 {{0:M}}
  1 <<SOURCE_CITATION>>                {{0:M}}
  1 <<MULTIMEDIA_LINK>>                {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""
    INDIVIDUAL_ATTRIBUTE_STRUCTURE: str = f"""
[
n CAST <Text>                          {{1:1}}  [g7:CAST]({Docs.CAST})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n DSCR <Text>                          {{1:1}}  [g7:DSCR]({Docs.DSCR})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n EDUC <Text>                          {{1:1}}  [g7:EDUC]({Docs.EDUC})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n IDNO <Special>                       {{1:1}}  [g7:IDNO]({Docs.IDNO})
  +1 TYPE <Text>                       {{1:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n NATI <Text>                          {{1:1}}  [g7:NATI]({Docs.NATI})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n NCHI <Integer>                       {{1:1}}  [g7:INDI-NCHI]({Docs.INDI_NCHI})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n NMR <Integer>                        {{1:1}}  [g7:NMR]({Docs.NMR})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n OCCU <Text>                          {{1:1}}  [g7:OCCU]({Docs.OCCU})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n PROP <Text>                          {{1:1}}  [g7:PROP]({Docs.PROP})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n RELI <Text>                          {{1:1}}  [g7:INDI-RELI]({Docs.INDI_RELI})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n RESI <Text>                          {{1:1}}  [g7:INDI-RESI]({Docs.INDI_RESI})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n SSN <Special>                        {{1:1}}  [g7:SSN]({Docs.SSN})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n TITL <Text>                          {{1:1}}  [g7:INDI-TITL]({Docs.INDI_TITL})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n FACT <Text>                          {{1:1}}  [g7:INDI-FACT]({Docs.INDI_FACT})
  +1 TYPE <Text>                       {{1:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
]
"""
    INDIVIDUAL_EVENT_DETAIL: str = f"""
n <<EVENT_DETAIL>>                     {{1:1}}
n AGE <Age>                            {{0:1}}  [g7:AGE]({Docs.AGE})
  +1 PHRASE <Text>                     {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
"""
    INDIVIDUAL_EVENT_STRUCTURE: str = f"""
[
n ADOP [Y|<NULL>]                      {{1:1}}  [g7:ADOP]({Docs.ADOP})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
  +1 FAMC @<XREF:FAM>@                 {{0:1}}  [g7:ADOP-FAMC]({Docs.ADOP_FAMC})
     +2 ADOP <Enum>                    {{0:1}}  [g7:FAMC-ADOP]({Docs.FAMC_ADOP})
        +3 PHRASE <Text>               {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
|
n BAPM [Y|<NULL>]                      {{1:1}}  [g7:BAPM]({Docs.BAPM})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n BARM [Y|<NULL>]                      {{1:1}}  [g7:BARM]({Docs.BARM})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n BASM [Y|<NULL>]                      {{1:1}}  [g7:BASM]({Docs.BASM})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n BIRT [Y|<NULL>]                      {{1:1}}  [g7:BIRT]({Docs.BIRT})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
  +1 FAMC @<XREF:FAM>@                 {{0:1}}  [g7:FAMC]({Docs.TYPE})
|
n BLES [Y|<NULL>]                      {{1:1}}  [g7:BLES]({Docs.BLES})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n BURI [Y|<NULL>]                      {{1:1}}  [g7:BURI]({Docs.BURI})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}

n CENS [Y|<NULL>]                      {{1:1}}  [g7:INDI-CENS]({Docs.INDI_CENS})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n CHR [Y|<NULL>]                       {{1:1}}  [g7:CHR]({Docs.CHR})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
  +1 FAMC @<XREF:FAM>@                 {{0:1}}  [g7:FAMC]({Docs.FAMC})
|
n CHRA [Y|<NULL>]                      {{1:1}}  [g7:CHRA]({Docs.CHRA})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n CONF [Y|<NULL>]                      {{1:1}}  [g7:CONF]({Docs.CONF})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n CREM [Y|<NULL>]                      {{1:1}}  [g7:CREM]({Docs.CREM})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n DEAT [Y|<NULL>]                      {{1:1}}  [g7:DEAT]({Docs.DEAT})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n EMIG [Y|<NULL>]                      {{1:1}}  [g7:EMIG]({Docs.EMIG})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n FCOM [Y|<NULL>]                      {{1:1}}  [g7:FCOM]({Docs.FCOM})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n GRAD [Y|<NULL>]                      {{1:1}}  [g7:GRAD]({Docs.GRAD})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n IMMI [Y|<NULL>]                      {{1:1}}  [g7:IMMI]({Docs.IMMI})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n NATU [Y|<NULL>]                      {{1:1}}  [g7:NATU]({Docs.NATU})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n ORDN [Y|<NULL>]                      {{1:1}}  [g7:ORDN]({Docs.ORDN})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n PROB [Y|<NULL>]                      {{1:1}}  [g7:PROB]({Docs.PROB})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n RETI [Y|<NULL>]                      {{1:1}}  [g7:RETI]({Docs.RETI})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n WILL [Y|<NULL>]                      {{1:1}}  [g7:WILL]({Docs.WILL})
  +1 TYPE <Text>                       {{0:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
|
n EVEN <Text>                          {{1:1}}  [g7:INDI-EVEN]({Docs.INDI_EVEN})
  +1 TYPE <Text>                       {{1:1}}  [g7:TYPE]({Docs.TYPE})
  +1 <<INDIVIDUAL_EVENT_DETAIL>>       {{0:1}}
]
"""
    LDS_ORDINANCE_DETAIL: str = f"""
n <<DATE_VALUE>>                       {{:1}}
n TEMP <Text>                          {{0:1}}  [g7:TEMP]({Docs.TEMP})
n <<PLACE_STRUCTURE>>                  {{0:1}}
n STAT <Enum>                          {{0:1}}  [g7:ord-STAT]({Docs.ORD_STAT})
  +1 DATE <DateExact>                  {{1:1}}  [g7:DATE-exact]({Docs.DATE_EXACT})
     +2 TIME <Time>                    {{0:1}}  [g7:TIME]({Docs.TIME})
n <<NOTE_STRUCTURE>>                   {{0:M}}
n <<SOURCE_CITATION>>                  {{0:M}}
"""
    LDS_INDIVIDUAL_ORDINANCE: str = f"""
[
n BAPL                                 {{1:1}}  [g7:BAPL]({Docs.BAPL})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
|
n CONL                                 {{1:1}}  [g7:CONL]({Docs.CONL})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
|
n ENDL                                 {{1:1}}  [g7:ENDL]({Docs.ENDL})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
|
n INIL                                 {{1:1}}  [g7:INIL]({Docs.INIL})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
|
n SLGC                                 {{1:1}}  [g7:SLGC]({Docs.SLGC})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
  +1 FAMC @<XREF:FAM>@                 {{1:1}}  [g7:FAMC]({Docs.FAMC})
]
"""
    LDS_SPOUSE_SEALING = f"""
n SLGS                                 {{1:1}}  [g7:SLGS]({Docs.SLGS})
  +1 <<LDS_ORDINANCE_DETAIL>>          {{0:1}}
"""
    MULTIMEDIA: str = f"""
0 @XREF:OBJE@ OBJE                     {{1:1}}  [g7:record-OBJE]({Docs.RECORD_OBJE})
  1 RESN <List:Enum>                   {{0:1}}  [g7:RESN]({Docs.RESN})
  1 FILE <FilePath>                    {{1:M}}  [g7:FILE]({Docs.FILE})
    2 FORM <MediaType>                 {{1:1}}  [g7:FORM]({Docs.FORM})
      3 MEDI <Enum>                    {{0:1}}  [g7:MEDI]({Docs.MEDI})
        4 PHRASE <Text>                {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
    2 TITL <Text>                      {{0:1}}  [g7:TITL]({Docs.TITL})
    2 TRAN <FilePath>                  {{0:M}}  [g7:FILE-TRAN]({Docs.FILE_TRAN})
      3 FORM <MediaType>               {{1:1}}  [g7:FORM]({Docs.FORM})
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<NOTE_STRUCTURE>>                 {{0:M}}
  1 <<SOURCE_CITATION>>                {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""
    MULTIMEDIA_LINK: str = f"""
n OBJE @<XREF:OBJE>@                   {{1:1}} [g7:OBJE]({Docs.OBJE})
  +1 CROP                              {{0:1}}  [g7:CROP]({Docs.CROP})
    +2 TOP <Integer>                   {{0:1}}  [g7:TOP]({Docs.TOP})
    +2 LEFT <Integer>                  {{0:1}}  [g7:LEFT]({Docs.LEFT})
    +2 HEIGHT <Integer>                {{0:1}}  [g7:HEIGHT]({Docs.HEIGHT})
    +2 WIDTH <Integer>                 {{0:1}}  [g7:WIDTH]({Docs.WIDTH})
  +1 TITL <Text>                       {{0:1}}  [g7:TITL]({Docs.TITL})
"""
    NON_EVENT_STRUCTURE: str = f"""
n NO <Enum>                            {{1:1}}  [g7:NO]({Docs.NO})
  +1 DATE <DatePeriod>                 {{0:1}}  [g7:NO-DATE]({Docs.NO_DATE})
     +2 PHRASE <Text>                  {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
  +1 <<SOURCE_CITATION>>               {{0:M}}
"""
    NOTE_STRUCTURE: str = f"""
[
n NOTE <Text>                          {{1:1}}  [g7:NOTE]({Docs.NOTE})
  +1 MIME <MediaType>                  {{0:1}}  [g7:MIME]({Docs.MIME})
  +1 LANG <Language>                   {{0:1}}  [g7:LANG]({Docs.LANG})
  +1 TRAN <Text>                       {{0:M}}  [g7:NOTE-TRAN]({Docs.NOTE_TRAN})
    +2 MIME <MediaType>                {{0:1}}  [g7:MIME]({Docs.MIME})
    +2 LANG <Language>                 {{0:1}}  [g7:LANG]({Docs.LANG})
  +1 <<SOURCE_CITATION>>               {{0:M}}
|
n SNOTE @<XREF:SNOTE>@                 {{1:1}}  [g7:SNOTE]({Docs.SNOTE})
]
"""
    PERSONAL_NAME_PIECES: str = f"""
n NPFX <Text>                          {{0:M}}  [g7:NPFX]({Docs.NPFX})
n GIVN <Text>                          {{0:M}}  [g7:GIVN]({Docs.GIVN})
n NICK <Text>                          {{0:M}}  [g7:NICK]({Docs.NICK})
n SPFX <Text>                          {{0:M}}  [g7:SPFX]({Docs.SPFX})
n SURN <Text>                          {{0:M}}  [g7:SURN]({Docs.SURN})
n NSFX <Text>                          {{0:M}}  [g7:NSFX]({Docs.NSFX})
"""
    PERSONAL_NAME_STRUCTURE: str = f"""
n NAME <PersonalName>                  {{1:1}}  [g7:INDI-NAME]({Docs.INDI_NAME})
  +1 TYPE <Enum>                       {{0:1}}  [g7:NAME-TYPE]({Docs.NAME_TYPE})
     +2 PHRASE <Text>                  {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
  +1 <<PERSONAL_NAME_PIECES>>          {{0:1}}
  +1 TRAN <PersonalName>               {{0:M}}  [g7:NAME-TRAN]({Docs.NAME_TRAN})
     +2 LANG <Language>                {{1:1}}  [g7:LANG]({Docs.LANG})
     +2 <<PERSONAL_NAME_PIECES>>       {{0:1}}
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
  +1 <<SOURCE_CITATION>>               {{0:M}}
"""
    PLACE_STRUCTURE: str = f"""
n PLAC <List:Text>                     {{1:1}}   [g7:PLAC]({Docs.PLAC})
  +1 FORM <List:Text>                  {{0:1}}   [g7:PLAC-FORM]({Docs.PLAC_FORM})
  +1 LANG <Language>                   {{0:1}}   [g7:LANG]({Docs.LANG})
  +1 TRAN <List:Text>                  {{0:M}}   [g7:PLAC-TRAN]({Docs.PLAC_TRAN})
     +2 LANG <Language>                {{1:1}}   [g7:LANG]({Docs.LANG})
  +1 MAP                               {{0:1}}   [g7:MAP]({Docs.MAP})
     +2 LATI <Special>                 {{1:1}}   [g7:LATI]({Docs.LATI})
     +2 LONG <Special>                 {{1:1}}   [g7:LONG]({Docs.LONG})
  +1 EXID <Special>                    {{0:M}}   [g7:EXID]({Docs.EXID})
     +2 TYPE <Special>                 {{0:1}}   [g7:EXID-TYPE]({Docs.EXID_TYPE})
  +1 <<NOTE_STRUCTURE>>                {{0:M}} 
"""
    REPOSITORY: str = f"""
0 @XREF:REPO@ REPO                     {{1:1}}  [g7:record-REPO]({Docs.RECORD_REPO})
  1 NAME <Text>                        {{1:1}}  [g7:NAME]({Docs.NAME})
  1 <<ADDRESS_STRUCTURE>>              {{0:1}}
  1 PHON <Special>                     {{0:M}}  [g7:PHON]({Docs.PHON})
  1 EMAIL <Special>                    {{0:M}}  [g7:EMAIL]({Docs.EMAIL})
  1 FAX <Special>                      {{0:M}}  [g7:FAX]({Docs.FAX})
  1 WWW <Special>                      {{0:M}}  [g7:WWW]({Docs.WWW})
  1 <<NOTE_STRUCTURE>>                 {{0:M}}
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""
    SHARED_NOTE: str = f"""
0 @XREF:SNOTE@ SNOTE <Text>            {{1:1}}  [g7:record-SNOTE]({Docs.RECORD_SNOTE})
  1 MIME <MediaType>                   {{0:1}}  [g7:MIME]({Docs.MIME})
  1 LANG <Language>                    {{0:1}}  [g7:LANG]({Docs.LANG})
  1 TRAN <Text>                        {{0:M}}  [g7:NOTE-TRAN]({Docs.NOTE_TRAN})
    2 MIME <MediaType>                 {{0:1}}  [g7:MIME]({Docs.MIME})
    2 LANG <Language>                  {{0:1}}  [g7:LANG]({Docs.LANG})
  1 <<SOURCE_CITATION>>                {{0:M}}
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""
    SOURCE: str = f"""
0 @XREF:SOUR@ SOUR                     {{1:1}}  [g7:record-SOUR]({Docs.RECORD_SOUR})
  1 DATA                               {{0:1}}  [g7:DATA]({Docs.DATA})
    2 EVEN <List:Enum>                 {{0:M}}  [g7:DATA-EVEN]({Docs.DATA_EVEN})
      3 DATE <DatePeriod>              {{0:1}}  [g7:DATA-EVEN-DATE]({Docs.DATA_EVEN_DATE})
        4 PHRASE <Text>                {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
      3 <<PLACE_STRUCTURE>>            {{0:1}}
    2 AGNC <Text>                      {{0:1}}  [g7:AGNC]({Docs.AGNC})
    2 <<NOTE_STRUCTURE>>               {{0:M}}
  1 AUTH <Text>                        {{0:1}}  [g7:AUTH]({Docs.AUTH})
  1 TITL <Text>                        {{0:1}}  [g7:TITL]({Docs.TITL})
  1 ABBR <Text>                        {{0:1}}  [g7:ABBR]({Docs.ABBR})
  1 PUBL <Text>                        {{0:1}}  [g7:PUBL]({Docs.PUBL})
  1 TEXT <Text>                        {{0:1}}  [g7:TEXT]({Docs.TEXT})
    2 MIME <MediaType>                 {{0:1}}  [g7:MIME]({Docs.MIME})
    2 LANG <Language>                  {{0:1}}  [g7:LANG]({Docs.LANG})
  1 <<SOURCE_REPOSITORY_CITATION>>     {{0:M}}
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<NOTE_STRUCTURE>>                 {{0:M}}
  1 <<MULTIMEDIA_LINK>>                {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""
    SOURCE_CITATION: str = f"""
n SOUR @<XREF:SOUR>@                   {{1:1}}  [g7:SOUR]({Docs.SOUR})
  +1 PAGE <Text>                       {{0:1}}  [g7:PAGE]({Docs.PAGE})
  +1 DATA                              {{0:1}}  [g7:SOUR-DATA]({Docs.SOUR_DATA})
    +2 <<DATE_VALUE>>                  {{0:1}}
    +2 TEXT <Text>                     {{0:M}}  [g7:TEXT]({Docs.TEXT})
      +3 MIME <MediaType>              {{0:1}}  [g7:MIME]({Docs.MIME})
      +3 LANG <Language>               {{0:1}}  [g7:LANG]({Docs.LANG})
  +1 EVEN <Enum>                       {{0:1}}  [g7:SOUR-EVEN]({Docs.SOUR_EVEN})
    +2 PHRASE <Text>                   {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
    +2 ROLE <Enum>                     {{0:1}}  [g7:ROLE]({Docs.ROLE})
      +3 PHRASE <Text>                 {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
  +1 QUAY <Enum>                       {{0:1}}  [g7:QUAY]({Docs.QUAY})
  +1 <<MULTIMEDIA_LINK>>               {{0:M}}
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
"""
    SOURCE_REPOSITORY_CITATION: str = f"""
n REPO @<XREF:REPO>@                   {{1:1}}  [g7:REPO]({Docs.REPO})
  +1 <<NOTE_STRUCTURE>>                {{0:M}}
  +1 CALN <Special>                    {{0:M}}  [g7:CALN]({Docs.CALN})
     +2 MEDI <Enum>                    {{0:1}}  [g7:MEDI]({Docs.MEDI})
        +3 PHRASE <Text>               {{0:1}}  [g7:PHRASE]({Docs.PHRASE})
"""
    SUBMITTER: str = f"""
0 @XREF:SUBM@ SUBM                     {{1:1}}  [g7:record-SUBM]({Docs.RECORD_SUBM})
  1 NAME <Text>                        {{1:1}}  [g7:NAME]({Docs.NAME})
  1 <<ADDRESS_STRUCTURE>>              {{0:1}}
  1 PHON <Special>                     {{0:M}}  [g7:PHON]({Docs.PHON})
  1 EMAIL <Special>                    {{0:M}}  [g7:EMAIL]({Docs.EMAIL})
  1 FAX <Special>                      {{0:M}}  [g7:FAX]({Docs.FAX})
  1 WWW <Special>                      {{0:M}}  [g7:WWW]({Docs.WWW})
  1 <<MULTIMEDIA_LINK>>                {{0:M}}
  1 LANG <Language>                    {{0:M}}  [g7:SUBM-LANG]({Docs.SUBM_LANG})
  1 <<IDENTIFIER_STRUCTURE>>           {{0:M}}
  1 <<NOTE_STRUCTURE>>                 {{0:M}}
  1 <<CHANGE_DATE>>                    {{0:1}}
  1 <<CREATION_DATE>>                  {{0:1}}
"""


@dataclass(frozen=True)
class Specs:
    ADDRESS: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ADDRESS_STRUCTURE'
    AGE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#age'
    ALIAS: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ALIA'
    )
    ASSOCIATION: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#ASSOCIATION_STRUCTURE'
    CHANGE_DATE: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CHANGE_DATE'
    )
    CHILD: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CHIL'
    )
    CREATION_DATE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#CREATION_DATE'
    DATE: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date'
    )
    DATE_VALUE: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#DATE_VALUE'
    )
    EVENT_DETAIL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#EVENT_DETAIL'
    EXID: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#EXID'
    )
    EXTENSION: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#extensions'
    )
    FAMILY: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_RECORD'
    FAMILY_ATTRIBUTE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_ATTRIBUTE_STRUCTURE'
    FAMILY_CHILD: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMC'
    )
    FAMILY_EVENT: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_STRUCTURE'
    FAMILY_EVENT_DETAIL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMILY_EVENT_DETAIL'
    FAMILY_SPOUSE: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FAMS'
    )
    FILE: str = ''
    FILE_TRANSLATION: str = ''
    FRENCH_R: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#FRENCH_R'
    )
    GREGORIAN: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#GREGORIAN'
    )
    HEADER: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HEADER'
    )
    HEBREW: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HEBREW'
    )
    HUSBAND: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#HUSB'
    )
    IDENTIFIER: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#IDENTIFIER_STRUCTURE'
    INDIVIDUAL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_RECORD'
    INDIVIDUAL_ATTRIBUTE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_ATTRIBUTE_STRUCTURE'
    INDIVIDUAL_EVENT: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_STRUCTURE'
    INDIVIDUAL_EVENT_DETAIL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#INDIVIDUAL_EVENT_DETAIL'
    JULIAN: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#JULIAN'
    )
    LDS_INDIVIDUAL_ORDINANCE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_INDIVIDUAL_ORDINANCE'
    LDS_ORDINANCE_DETAIL: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_ORDINANCE_DETAIL'
    LDS_SPOUSE_SEALING: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#LDS_SPOUSE_SEALING'
    MAP: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MAP'
    MULTIMEDIA: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_RECORD'
    MULTIMEDIA_LINK: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#MULTIMEDIA_LINK'
    NON_EVENT: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NON_EVENT_STRUCTURE'
    NOTE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#NOTE_STRUCTURE'
    PERSONAL_NAME: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_STRUCTURE'
    PERSONAL_NAME_PIECES: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PERSONAL_NAME_PIECES'
    PLACE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#PLACE_STRUCTURE'
    REPOSITORY: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#REPOSITORY_RECORD'
    SCHEMA: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SCHMA'
    )
    SHARED_NOTE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SHARED_NOTE_RECORD'
    SOURCE: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_RECORD'
    SOURCE_EVENT: str = ''
    SOURCE_CITATION: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_CITATION'
    SOURCE_REPOSITORY_CITATION: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SOURCE_REPOSITORY_CITATION'
    SUBMITTER: str = 'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#SUBMITTER_RECORD'
    TIME: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#time'
    )
    WIFE: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#WIFE'
    )


@dataclass(frozen=True)
class Default:
    CHOICE: int = 1
    DATE_DAY: int = 0
    DATE_MONTH: int = 0
    DATE_YEAR: int = 0
    DATE_WEEK: int = 0
    DAYS: int = 0
    EMPTY: str = ''
    GREATER_LESS_THAN: str = '>'
    HEIGHT: int = 0
    LEFT: int = 0
    MAP_LATITUDE: float = 0.0
    MAP_LONGITUDE: float = 0.0
    MIME: str = ''
    MONTHS: int = 0
    NONE: str = 'None'
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
    POINTER: str = '@VOID@'
    QUOTE_SINGLE: str = "'"
    QUOTE_DOUBLE: str = '"'
    TIME_HOUR: int = 0
    TIME_MINUTE: int = 0
    TIME_SECOND: float = 0.0
    TIME_UTC: bool = False
    TOP: int = 0
    WEEKS: int = 0
    WIDTH: int = 0
    YEARS: int = 0


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
