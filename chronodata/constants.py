# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides a namespace for typed constants."""

from dataclasses import dataclass
from typing import ClassVar, Literal


@dataclass(frozen=True)
class Arg:
    """The following constants are used as arguments to procedure calls
    such as Pandas DataFrames or NumPy."""

    GED: str = '.ged'
    GEDLEN: int = 4
    GRAMPS: str = '.gramps'
    GRAMPSLEN: int = 7
    JSON: str = '.json'
    JSONLEN: int = 5
    INDEX: str = 'index'
    INT: str = 'int'
    LOCATION: str = 'lower right'
    WRITE: str = 'w'
    READ: str = 'r'


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
    EMPTY: str = ''
    EXPERIMENT: str = 'EXPERIMENT'
    GREGORIAN: str = 'GREGORIAN'
    SECULAR: str = 'SECULAR'


@dataclass(frozen=True)
class String:
    """The following constants define strings that are neither keys
    nor values of a dictionary, but are used in generating comments,
    formatting numbers or other processes.
    """

    NEGATIVE: str = '-'
    NEWLINE: str = '\n'
    SPACE: str = ' '


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


@dataclass(frozen=True)
class Key:
    """The following constants define the keys that are used
    for dictionaries."""

    ACTORS: str = 'ACTORS'
    BEGIN: str = 'BEGIN'
    BIRTH: str = 'BIRTH'
    CAL: str = 'CALENDAR'
    CHALLENGES: str = 'CHALLENGES'
    COMMENTS: str = 'COMMENTS'
    DATE: str = 'DATE'
    DEATH: str = 'DEATH'
    DESC: str = 'DESC'
    END: str = 'END'
    EVENTS: str = 'EVENTS'
    FATHER: str = 'FATHER'
    FEMALE: str = 'FEMALE'
    FILE: str = 'FILENAME'
    LABELS: str = 'LABELS'
    MALE: str = 'MALE'
    MARKERS: str = 'MARKERS'
    MESSAGE: str = 'MSG'
    MOTHER: str = 'MOTHER'
    NAME: str = 'NAME'
    PRE: str = 'PRE'
    PERIODS: str = 'PERIODS'
    POST: str = 'POST'
    SOURCES: str = 'SOURCES'
    STRICT: str = 'STRICT'
    TEXTS: str = 'TEXTS'
    TIMESTAMP: str = 'TIMESTAMP'
    ZERO: str = 'ZERO'
    keys: ClassVar = [
        ACTORS,
        BEGIN,
        BIRTH,
        CAL,
        CHALLENGES,
        COMMENTS,
        DATE,
        DEATH,
        DESC,
        END,
        EVENTS,
        FATHER,
        FEMALE,
        FILE,
        LABELS,
        MALE,
        MARKERS,
        MOTHER,
        NAME,
        PERIODS,
        POST,
        PRE,
        SOURCES,
        STRICT,
        TEXTS,
        ZERO,
    ]


@dataclass(frozen=True)
class Tag:
    """Constant definitions of standard tags:

    References
    --------
    [Specifications](https://github.com/FamilySearch/GEDCOM/blob/main/specification/gedcom-1-hierarchical-container-format.md)
    """

    ABBR: str = 'ABBR'
    ADDR: str = 'ADDR'
    ADOP: str = 'ADOP'
    ADOP_FAMC: str = 'ADOPT-FAMC'
    ADOPTED: str = 'ADOPTED'  # ?#
    ADR1: str = 'ADR1'
    ADR2: str = 'ADR2'
    ADR3: str = 'ADR3'
    AFN: str = 'AFN'
    AGE: str = 'AGE'
    AGNC: str = 'AGNC'
    AKA: str = 'AKA'  # ?#
    ALIA: str = 'ALIA'
    ANCI: str = 'ANCI'
    ANUL: str = 'ANUL'
    ASSO: str = 'ASSO'
    AUDIO: str = 'AUDIO'  # ?#
    AUTH: str = 'AUTH'
    BAPL: str = 'BAPL'
    BAPM: str = 'BAPM'
    BARM: str = 'BARM'
    BASM: str = 'BASM'
    BIRT: str = 'BIRT'
    BIRTH: str = 'BIRTH'  # ?#
    BLES: str = 'BLES'
    BOTH: str = 'BOTH'  # ?#
    BTC: str = 'BTC'  # ?#
    BURI: str = 'BURI'
    CALN: str = 'CALN'
    CANCELED: str = 'CANCELED'  # ?#
    CARD: str = 'CARD'  # ?#
    CAST: str = 'CAST'
    CAUS: str = 'CAUS'
    CENS: str = 'CENS'  # ?#
    CHALLENGED: str = 'CHALLENGED'  # ?#
    CHAN: str = 'CHAN'
    CHIL: str = 'CHIL'
    CHILD: str = 'CHILD'  # ?#
    CHALLENGE: str = 'CHALLENGE'
    CHR: str = 'CHR'
    CHRONOS: str = 'CHRONOS'
    CHRA: str = 'CHRA'
    CITY: str = 'CITY'
    CLERGY: str = 'CLERGY'  # ?#
    COMPLETED: str = 'COMPLETED'  # ?#
    CONF: str = 'CONF'
    CONFIDENTIAL: str = 'CONFIDENTIAL'  # ?#
    CONL: str = 'CONL'
    CONT: str = 'CONT'
    COPR: str = 'COPR'
    CORP: str = 'CORP'
    CREA: str = 'CREA'
    CREM: str = 'CREM'
    CROP: str = 'CROP'
    CTRY: str = 'CTRY'
    DATA: str = 'DATA'
    DATA_EVEN: str = 'DATA-EVEN'
    DATA_EVEN_DATE: str = 'DATA-EVEN-DATE'
    DATE: str = 'DATE'
    DATE_exact: str = 'DATA-exact'
    DEAT: str = 'DEAT'
    DESI: str = 'DESI'
    DEST: str = 'DEST'
    DISPROVEN: str = 'DISPROVEN'  # ?#
    DIV: str = 'DIV'
    DIVF: str = 'DIVF'
    DNS: str = 'DNS'  # ?#
    DNS_CAN: str = 'DNS_CAN'  # ?#
    DSCR: str = 'DSCR'
    EDUC: str = 'EDUC'
    ELECTRONIC: str = 'ELECTRONIC'  # ?#
    EMAIL: str = 'EMAIL'
    EMIG: str = 'EMIG'
    ENDL: str = 'ENDL'
    ENGA: str = 'ENGA'
    EVENT: str = 'EVEN'  # ?#
    EXCLUDED: str = 'EXCLUDED'  # ?#
    EXID: str = 'EXID'
    EXID_TYPE: str = 'EXID-TYPE'
    F: str = 'F'  # ?#
    FACT: str = 'FACT'  # ?#
    FAM: str = 'FAM'  # ?#
    FATH: str = 'FATH'  # ?#
    FAM_CENS: str = 'FAM-CENS'
    FAM_EVEN: str = 'FAM-EVEN'
    FAM_FACT: str = 'FAM-FACT'
    FAM_HUSB: str = 'FAM-HUSB'
    FAM_NCHI: str = 'FAM-NCHI'
    FAM_RESI: str = 'FAM-RESI'
    FAM_WIFE: str = 'FAM-WIFE'
    FAMC: str = 'FAMC'
    FAMC_ADOPT: str = 'FAMC-ADOPT'
    FAMC_STAT: str = 'FAMC-STAT'
    FAMS: str = 'FAMS'
    FAX: str = 'FAX'
    FCOM: str = 'FCOM'
    FICHE: str = 'FICHE'  # ?#
    FILE: str = 'FILE'
    FILE_TRAN: str = 'FILE-TRAN'
    FILM: str = 'FILM'  # ?#
    FORM: str = 'FORM'
    FOSTER: str = 'FOSTER'  # ?#
    FRIEND: str = 'FRIEND'  # ?#
    GEDC: str = 'GEDC'
    GIVN: str = 'GIVN'
    GODP: str = 'GODP'  # ?#
    GRAD: str = 'GRAD'
    HEAD: str = 'HEAD'
    HEAD_DATE: str = 'HEAD-DATE'
    HEAD_LANG: str = 'HEAD-LANG'
    HEAD_PLAC: str = 'HEAD-PLAC'
    HEAD_PLAC_FORM: str = 'HEAD-PLAC-FORM'
    HEAD_SOUR: str = 'HEAD-SOUR'
    HEAD_SOUR_DATA: str = 'HEAD-SOUR-DATA'
    HEIGHT: str = 'HEIGHT'
    HUSB: str = 'HUSB'
    IDNO: str = 'IDNO'
    IMMI: str = 'IMMI'
    IMMIGRANT: str = 'IMMIGRANT'  # ?#
    INDI: str = 'INDI'
    INDI_CENS: str = 'INDI-CENS'
    INDI_EVEN: str = 'INDI-EVEN'
    INDI_FACT: str = 'INDI-FACT'
    INDI_FAMC: str = 'INDI-FAMC'
    INDI_NAME: str = 'INDI-NAME'
    INDI_NCHI: str = 'INDI-NCHI'
    INDI_RELI: str = 'INDI-RELI'
    INDI_RESI: str = 'INDI-RESI'
    INDI_TITL: str = 'INDI-TITLE'
    INFANT: str = 'INFANT'  # ?#
    INIL: str = 'INIL'
    LANG: str = 'LANG'
    LATI: str = 'LATI'
    LEFT: str = 'LEFT'
    LOCKED: str = 'LOCKED'  # ?#
    LONG: str = 'LONG'
    M: str = 'M'  # ?#
    MAGAZINE: str = 'MAGAZINE'  # ?#
    MAIDEN: str = 'MAIDEN'  # ?#
    MAP: str = 'MAP'
    MARB: str = 'MARB'
    MARC: str = 'MARC'
    MARL: str = 'MARL'
    MARR: str = 'MARR'
    MARRIED: str = 'MARRIED'  # ?#
    MARS: str = 'MARS'
    MEDI: str = 'MEDI'
    MIME: str = 'MIME'
    MOTH: str = 'MOTH'  # ?#
    MULTIPLE: str = 'MULTIPLE'  # ?#
    NAME: str = 'NAME'
    NAME_TRAN: str = 'NAME-TRAN'
    NAME_TYPE: str = 'NAME-TYPE'
    NATI: str = 'NATI'
    NATU: str = 'NATU'
    NCHI: str = 'NCHI'
    NEWSPAPER: str = 'NEWSPAPER'  # ?#
    NGHBR: str = 'NEIGHBOR'  # ?#
    NICK: str = 'NICK'
    NMR: str = 'NMR'
    NO: str = 'NO'
    NO_DATE: str = 'NO-DATE'
    NOTE: str = 'NOTE'
    NOTE_TRAN: str = 'NOTE-TRAN'
    NPFX: str = 'NPFX'
    NSFX: str = 'NSFX'
    OBJE: str = 'OBJE'
    OCCU: str = 'OCCU'
    OFFICIATOR: str = 'OFFICIATOR'  # ?#
    ORDN: str = 'ORDN'
    OTHER: str = 'OTHER'  # ?#
    PAGE: str = 'PAGE'
    PEDI: str = 'PEDI'
    PARENT: str = 'PARENT'  # ?#
    PHON: str = 'PHON'
    PHOTO: str = 'PHOTO'  # ?#
    PHRASE: str = 'PHRASE'
    PLAC: str = 'PLAC'
    PLAC_FORM: str = 'PLAC-FORM'
    PLAC_TRAN: str = 'PLAC-TRAN'
    POST: str = 'POST'
    PRE_1970: str = 'PRE_1970'  # ?#
    PRIVACY: str = 'PRIVACY'  # ?#
    PROB: str = 'PROB'
    PROFESSIONAL: str = 'PROFESSIONAL'  # ?#
    PROP: str = 'PROP'
    PROVEN: str = 'PROVEN'
    PUBL: str = 'PUBL'
    QUAY: str = 'QUAY'
    QUAY0: str = '0'  # ?#
    QUAY1: str = '1'  # ?#
    QUAY2: str = '2'  # ?#
    QUAY3: str = '3'  # ?#
    REFN: str = 'REFN'
    RELI: str = 'RELI'
    REPO: str = 'REPO'
    RESN: str = 'RESN'
    RETI: str = 'RETI'
    RIN: str = 'RIN'
    ROLE: str = 'ROLE'
    SCHMA: str = 'SCHMA'
    SDATE: str = 'SDATE'
    SEALING: str = 'SEALING'  # ?#
    SEX: str = 'SEX'
    SLGC: str = 'SLGC'
    SLGS: str = 'SLGS'
    SNOTE: str = 'SNOTE'
    SOUR: str = 'SOUR'
    SOUR_DATA: str = 'SOUR-DATA'
    SOUR_EVEN: str = 'SOUR-EVEN'
    SPFX: str = 'SPFX'
    SPOU: str = 'SPOU'  # ?#
    STILLBORN: str = 'STILLBORN'  # ?#
    SUBMITTED: str = 'SUBMITTED'  # ?#
    SSN: str = 'SSN'
    STAE: str = 'STAE'
    STAT: str = 'STAT'  # ?#
    SUBM: str = 'SUBM'
    SUBM_LANG: str = 'SUBM-LANG'
    SURN: str = 'SURN'
    TAG: str = 'TAG'
    TEMP: str = 'TEMP'
    TESTCASES: str = 'TEST CASES'
    TEXT: str = 'TEXT'
    TIME: str = 'TIME'
    TITL: str = 'TITL'
    TOMBSTONE: str = 'TOMBSTONE'  # ?#
    TOP: str = 'TOP'
    TRAN: str = 'TRAN'  # ?#
    TRLR: str = 'TRLR'
    TYPE: str = 'TYPE'
    U: str = 'U'  # ?#
    UNCLEARED: str = 'UNCLEARED'  # ?#
    UID: str = 'UID'
    VERS: str = 'VERS'
    VIDEO: str = 'VIDEO'  # ?#
    WIDTH: str = 'WIDTH'
    WIFE: str = 'WIFE'
    WILL: str = 'WILL'
    WITN: str = 'WITN'  # ?#
    WWW: str = 'WWW'
    X: str = 'X'  # ?#
    cal_FRENCH_R: str = 'cal-FRENCH_R'
    cal_GREGORIAN: str = 'cal-GREGORIAN'
    cal_HEBREW: str = 'cal-HEBREW'
    cal_JULIAN: str = 'cal-JULIAN'
    enum_0: str = 'enum-0'
    enum_1: str = 'enum-1'
    enum_2: str = 'enum-2'
    enum_3: str = 'enum-3'
    enum_ADOP_HUSB: str = 'enum-ADOP-HUSB'
    enum_ADOP_WIFE: str = 'enum-ADOP-WIFE'
    enum_ADOPTED: str = 'enum-ADOPTED'
    enum_AKA: str = 'enum-AKA'
    enum_AUDIO: str = 'enum-AUDIO'
    enum_BIC: str = 'enum-BIC'
    enum_BIRTH: str = 'enum-BIRTH'
    enum_BOOK: str = 'enum-BOOK'
    enum_BOTH: str = 'enum-BOTH'
    enum_CANCELED: str = 'enum-CANCELED'
    enum_CARD: str = 'enum-CARD'
    enum_CENS: str = 'enum-CENS'
    enum_CHALLENGED: str = 'enum-CHALLENGED'
    enum_CHIL: str = 'enum-CHIL'
    enum_CHILD: str = 'enum-CHILD'
    enum_CLERGY: str = 'enum-CLERGY'
    enum_COMPLETED: str = 'enum-COMPLETED'
    enum_CONFIDENTIAL: str = 'enum-CONFIDENTIAL'
    enum_DISPROVEN: str = 'enum-DISPROVEN'
    enum_DNS: str = 'enum-DNS'
    enum_DNS_CAN: str = 'enum-DNS-CAN'
    enum_ELECTRONIC: str = 'enum-ELECTRONIC'
    enum_EVEN: str = 'enum-EVEN'
    enum_EXCLUDED: str = 'enum-EXCLUDED'
    enum_F: str = 'enum-F'
    enum_FACT: str = 'enum-FACT'
    enum_FATH: str = 'enum-FATH'
    enum_FICHE: str = 'enum-FICHE'
    enum_FILM: str = 'enum-FILM'
    enum_FOSTER: str = 'enum-FOSTER'
    enum_FRIEND: str = 'enum-FRIEND'
    enum_GODP: str = 'enum-GODP'
    enum_HUSB: str = 'enum-HUSB'
    enum_IMMIGRANT: str = 'enum-IMMIGRANT'
    enum_INFANT: str = 'enum-INFANT'
    enum_LOCKED: str = 'enum-LOCKED'
    enum_M: str = 'enum-M'
    enum_MAGAZINE: str = 'enum-MAGAZINE'
    enum_MAIDEN: str = 'enum-MAIDEN'
    enum_MANUSCRIPT: str = 'enum-MANUSCRIPT'
    enum_MAP: str = 'enum-MAP'
    enum_MARRIED: str = 'enum-MARRIED'
    enum_MOTH: str = 'enum-MOTH'
    enum_MULTIPLE: str = 'enum-MULTIPLE'
    enum_NCHI: str = 'enum-NCHI'
    enum_NEWSPAPER: str = 'enum-NEWSPAPER'
    enum_NGHBR: str = 'enum-NGHBR'
    enum_OFFICIATOR: str = 'enum-OFFICIATOR'
    enum_OTHER: str = 'enum-OTHER'
    enum_PARENT: str = 'enum-PARENT'
    enum_PHOTO: str = 'enum-PHOTO'
    enum_PRE_1970: str = 'enum-PRE_1970'
    enum_PRIVACY: str = 'enum-PRIVACY'
    enum_PROFESSIONAL: str = 'enum-PROFESSIONAL'
    enum_PROVEN: str = 'enum-PROVEN'
    enum_RESI: str = 'enum-RESI'
    enum_SEALING: str = 'enum-SEALING'
    enum_SPOU: str = 'enum-SPOU'
    enum_STILLBORN: str = 'enum-STILLBORN'
    enum_TOMBSTONE: str = 'enum-TOMBSTONE'
    enum_U: str = 'enum-U'
    enum_UNCLEARED: str = 'enum-UNCLEARED'
    enum_VIDEO: str = 'enum-VIDEO'
    enum_WIFE: str = 'enum-WIFE'
    enum_WITN: str = 'enum-WITN'
    enum_X: str = 'enum-X'


@dataclass(frozen=True)
class ExtTag:
    """Constant definitions for extention tags."""

    _DATE: str = '_DATE'
    _LOC: str = '_LOC'
    _PARTNER: str = 'PARTNER'
    _POP: str = '_POP'


@dataclass(frozen=True)
class Line:
    """Strings to write a GEDCOM file."""

    HEAD: str = f'0 {Tag.HEAD}\n1 {Tag.GEDC}\n2 {Tag.VERS} 7.0\n'
    SUBM: str = f'0 {Tag.SUBM}\n1 {Tag.NAME} ChronoData\n'
    TAIL: str = f'0 {Tag.TRLR}\n'


@dataclass(frozen=True)
class Calendar:
    """The following dictionaries define the constants for
    particular calendars using previously defined constants.
    """

    BEFORE_PRESENT: ClassVar = {
        Key.NAME: Value.BEFORE_PRESENT,
        Key.POST: Value.EMPTY,
        Key.PRE: Value.BP,
        Key.STRICT: True,
        Key.ZERO: False,
    }
    EXPERIMENT: ClassVar = {
        Key.NAME: Value.EXPERIMENT,
        Key.POST: Value.EMPTY,
        Key.PRE: Value.EMPTY,
        Key.STRICT: True,
        Key.ZERO: False,
    }
    GREGORIAN: ClassVar = {
        Key.NAME: Value.GREGORIAN,
        Key.POST: Value.AD,
        Key.PRE: Value.BC,
        Key.STRICT: True,
        Key.ZERO: False,
    }
    SECULAR: ClassVar = {
        Key.NAME: Value.SECULAR,
        Key.POST: Value.CE,
        Key.PRE: Value.BCE,
        Key.STRICT: True,
        Key.ZERO: False,
    }
    calendars: ClassVar = [
        BEFORE_PRESENT,
        EXPERIMENT,
        GREGORIAN,
        SECULAR,
    ]
