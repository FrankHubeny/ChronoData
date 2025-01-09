# chronodata/constants.py
# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides a namespace for typed constants."""

from dataclasses import dataclass
from typing import ClassVar, Literal


class AgeConstants:
    """Age enumerations for the Age NamedTuple."""

    UNIT: ClassVar = {
        'y': 'y',
        'year': 'y',
        'm': 'month',
        'month': 'm',
        'd': 'd',
        'day': 'd',
        'w': 'w',
        'week': 'w',
    }
    BOUND: ClassVar = {'<', '>'}
    NAME: ClassVar = {'U'}


@dataclass(frozen=True)
class Choice:
    ADOP: frozenset[str] = frozenset({'HUSB', 'WIFE', 'BOTH'})
    APPROXIMATE_DATE: frozenset[str] = frozenset({'ABT', 'CAL', 'EST'})
    EAST_WEST: frozenset[str] = frozenset({'E', 'W'})
    EXTENSION_TAG: frozenset[str] = frozenset({'LANG_',})
    EVENT: frozenset[str] = frozenset(
        {
            'ADOP',
            'ANUL',
            'BAPM',
            'BARM',
            'BASM',
            'BIRT',
            'BLES',
            'BURI',
            'CENS',
            'CHR',
            'CHRA',
            'CONF',
            'CREM',
            'DEAT',
            'DIV',
            'DIVF',
            'EMIG',
            'ENGA',
            'EVEN',
            'FCOM',
            'GRAD',
            'IMMI',
            'MARB',
            'MARC',
            'MARL',
            'MARR',
            'MARS',
            'NATU',
            'ORDN',
            'PROB',
            'RETI',
            'WILL',
        }
    )
    EVENT_ATTRIBUTE: frozenset[str] = frozenset(
        {'CENS', 'NCHI', 'RESI', 'FACT', 'EVEN'}
    )
    FAMC_STAT: frozenset[str] = frozenset({'CHALLENGED', 'DISPROVEN', 'PROVEN'})
    FAMILY_ATTRIBUTE: frozenset[str] = frozenset({'NCHI', 'RESI', 'FACT'})
    FAMILY_EVENT: frozenset[str] = frozenset(
        {
            'ANUL',
            'CENS',
            'DIV',
            'DIVF',
            'ENGA',
            'MARB',
            'MARC',
            'MARL',
            'MARR',
            'MARS',
            'EVEN',
        }
    )
    GREATER_LESS_THAN: frozenset[str] = frozenset({'', '<', '>'})
    ID: frozenset[str] = frozenset({'EXID', 'REFN', 'UID'})
    INDIVIDUAL_ATTRIBUTE: frozenset[str] = frozenset(
        {
            'CAST',
            'DSCR',
            'EDUC',
            'IDNO',
            'NATI',
            'NCHI',
            'NMR',
            'OCCU',
            'PROP',
            'RELI',
            'RESI',
            'SSN',
            'TITL',
            'FACT',
        }
    )
    INDIVIDUAL_EVENT: frozenset[str] = frozenset(
        {
            'ADOP',
            'BAPM',
            'BARM',
            'BASM',
            'BIRT',
            'BLES',
            'BURI',
            'CENS',
            'CHR',
            'CHRA',
            'CONF',
            'CREM',
            'DEAT',
            'EMIG',
            'FCOM',
            'GRAD',
            'IMMI',
            'NATU',
            'ORDN',
            'PROB',
            'RETI',
            'WILL',
            'EVEN',
        }
    )
    MEDI: frozenset[str] = frozenset(
        {
            'AUDIO',
            'BOOK',
            'CARD',
            'ELECTRONIC',
            'FICHE',
            'FILM',
            'MAGAZINE',
            'MANUSCRIPT',
            'MAP',
            'NEWSPAPER',
            'PHOTO',
            'TOMBSTONE',
            'VIDEO',
            'OTHER',
        }
    )
    MEDIA_TYPE: frozenset[str] = frozenset({'TEXT_HTML', 'TEXT_PLAIN'})
    NAME_TYPE: frozenset[str] = frozenset(
        {
            'AKA',
            'BIRTH',
            'IMMIGRANT',
            'MAIDEN',
            'MARRIED',
            'PROFESSIONAL',
            'OTHER',
        }
    )
    NORTH_SOUTH: frozenset[str] = frozenset({'N', 'S'})
    PEDI: frozenset[str] = frozenset(
        {'ADOPTED', 'BIRTH', 'FOSTER', 'SEALING', 'OTHER'}
    )
    PERSONAL_NAME_PIECE: frozenset[str] = frozenset(
        {'GIVN', 'NICK', 'NPFX', 'NSFX', 'SPFX', 'SURN'}
    )
    QUALITY: frozenset[str] = frozenset({'0', '1', '2', '3'})
    RANGE_DATE: frozenset[str] = frozenset({'AFT', 'AND', 'BEF', 'BET'})
    RECORD: frozenset[str] = frozenset(
        {'FAM', 'INDI', 'OBJE', 'REPO', 'SNOTE', 'SOUR', 'SUBM'}
    )
    RESTRICT_DATE: frozenset[str] = frozenset(
        {'AFT', 'AND', 'BEF', 'BET', 'CAL', 'EST', 'FROM', 'TO'}
    )
    RESTRICTION: frozenset[str] = frozenset(
        {'CONFIDENTIAL', 'LOCKED', 'PRIVACY'}
    )
    ROLE: frozenset[str] = frozenset(
        {
            'CHIL',
            'CLERGY',
            'FATH',
            'FRIEND',
            'GODP',
            'HUSB',
            'MOTH',
            'MULTIPLE',
            'NGHBR',
            'OFFICIATOR',
            'PARENT',
            'SPOU',
            'WIFE',
            'WITN',
            'OTHER',
        }
    )
    SEX: frozenset[str] = frozenset({'F', 'M', 'U', 'X'})
    STAT: frozenset[str] = frozenset(
        {
            'BIC',
            'CANCELED',
            'CHILD',
            'COMPLETED',
            'EXCLUDED',
            'DNS',
            'DNS_CAN',
            'INFANT',
            'PRE_1970',
            'STILLBORN',
            'SUBMITTED',
            'UNCLEARED',
        }
    )


# @dataclass(frozen=True)
# class Arg:
#     """The following constants are used as arguments to procedure calls
#     such as Pandas DataFrames or NumPy."""

#     CSV: str = '.csv'
#     CSVLEN: int = 4
#     GED: str = '.ged'
#     GEDLEN: int = 4
#     GRAMPS: str = '.gramps'
#     GRAMPSLEN: int = 7
#     JSON: str = '.json'
#     JSONLEN: int = 5
#     INDEX: str = 'index'
#     INT: str = 'int'
#     LOCATION: str = 'lower right'
#     WRITE: str = 'w'
#     READ: str = 'r'


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
    """The following constants define strings that are neither keys
    nor values of a dictionary, but are used in generating comments,
    formatting numbers or other processes.
    """

    ATSIGN: str = '@'
    BANNED: str = r'[\u0000-\u001F\u007F\uD800-\uDFFF\uFFFE\uFFFF]'
    BC: str = 'BCE'
    CHRON_NAMES: str = 'CHRON NAMES'
    CHRONS: str = 'CHRONS'
    COLON: str = ':'
    CSV: str = '.csv'
    DATA: str = 'DATA'
    DATE: str = 'DATE'
    DAY: str = 'd'
    EMPTY: str = ''
    EVENT: str = 'EVENT'
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
    LANG_URI: str = 'http://'
    LESS_THAN: str = '<'
    LOCATION: str = 'lower right'
    MAX_MONTHS: str = 'Max Months'
    MONTH: str = 'm'
    MONTH_NAMES: str = 'Month Names'
    MONTH_MAX_DAYS: str = 'Month Max Days'
    NAME: str = 'NAME'
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
    TESTCASES: str = 'TEST CASES'
    UNDERLINE: str = '_'
    UNDETERMINED: str = 'und'
    VERSION: str = '7.0'
    WEEK: str = 'w'
    WRITE: str = 'w'
    YEAR: str = 'y'
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
    CHRON_NAMES: str = 'CHRON NAMES'
    CHRONS: str = 'CHRONS'
    DATA: str = 'DATA'
    DATE: str = 'DATE'
    EVENT: str = 'EVENT'
    NAME: str = 'NAME'
    TESTCASES: str = 'TEST CASES'


@dataclass(frozen=True)
class Calendar:
    """The following dictionaries define the constants for
    particular calendars using previously defined constants.
    """

    BEFORE_PRESENT: ClassVar = {
        Key.NAME: Value.BEFORE_PRESENT,
        Key.POST: '',
        Key.PRE: Value.BP,
        Key.STRICT: True,
        Key.ZERO: False,
    }
    EXPERIMENT: ClassVar = {
        Key.NAME: Value.EXPERIMENT,
        Key.POST: '',
        Key.PRE: '',
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
