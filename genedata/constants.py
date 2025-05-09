# genedata/constants.py
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
    'ApproxDate',
    'GedFlag',
    'RangeDate',
    'RestrictDate',
]

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Literal


class Config:
    """Values specifying which version of the GEDCOM specification are being used."""

    VERSION: str = '70'
    GEDVERSION: str = '7.0'
    TERMS: str = 'https://gedcom.io/terms/v7/'
    SPECS: str = (
        'https://gedcom.io/specifications/FamilySearchGEDCOMv7.html'
    )


@dataclass(frozen=True)
class Default:
    AGE_DAY: str = 'd'
    AGE_MONTH: str = 'm'
    AGE_WEEK: str = 'w'
    AGE_YEAR: str = 'y'
    ATSIGN: str = '@'
    ATSIGN_DOUBLE: str = '@@'
    BANNED: str = r'[\u0000-\u001F\u007F\uD800-\uDFFF\uFFFE\uFFFF]'
    BAR: str = '|'
    BRACE_LEFT: str = '{'
    BRACE_RIGHT: str = '}'
    BRACKET_RIGHT: str = ']'
    BRACKET_LEFT: str = '['
    BRACKET_LEFT_RIGHT: str = '[]'
    CALENDAR_DEFAULT: str = 'GREGORIAN'
    CALENDAR_KEY_DEFAULT: str = 'cal-GREGORIAN'
    CARDINALITY_ANY_NUMBER: str = ':M}'
    CARDINALITY_OPTIONAL: str = '{0:'
    CARDINALITY_REQUIRED: str = '{1:'
    CARDINALITY_SINGULAR: str = ':1}'
    CLASS_EXT: str = 'RecordExt'
    CLASS_FAM: str = 'RecordFam'
    CLASS_INDI: str = 'RecordIndi'
    CLASS_OBJE: str = 'RecordObje'
    CLASS_REPO: str = 'RecordRepo'
    CLASS_SNOTE: str = 'RecordSnote'
    CLASS_SOUR: str = 'RecordSour'
    CLASS_SUBM: str = 'RecordSubm'
    CODE_CLASS: str = 'gc.'
    CODE_CLASS_VARIABLE: str = 'gc'
    CODE_GENEALOGY: str = 'g.'
    CODE_GENEALOGY_VARIABLE: str = 'g'
    CODE_SUBS: str = 'subs'
    CODE_VALUE: str = 'value'
    COLON: str = ':'
    COLUMN_RECORDS: str = 'Records'
    COLUMN_COUNT: str = 'Count'
    COMMA: str = ','
    COMMA_REQUIRED: str = ',  # REQUIRED'
    CHOICE: int = 1
    CONT: str = 'CONT'
    DATE_EXACT_SPACES: int = 2
    DATE_EXACT_MAX_SIZE: int = len('01 JAN -2000') 
    DATE_DAY: int = 0
    DATE_MONTH: int = 0
    DATE_YEAR: int = 0
    DATE_WEEK: int = 0
    DAYS: int = 0
    EMPTY: str = ''
    EQUAL: str = ' = '
    EOL: str = '\n'
    EOL_CARRIAGE_RETURN: str = '\r\n'
    EOL_DOUBLE: str = '\n\n'
    GED_EXT_SCHMA: str = f'{EOL}1 SCHMA{EOL}'
    GED_EXT_TAG: str = '2 TAG '
    GED_HEADER: str = f'0 HEAD{EOL}'
    GED_REPLACE_THIS: str = ' REPLACETHISWITHANENDOFLINE '
    GED_TRAILER: str = f'{EOL}0 TRLR'
    GED_VERSIONS: frozenset[str] = frozenset(
        [
            '7.0',
        ]
    )
    GED_VERSION_START: str = f'{EOL}1 GEDC{EOL}2 VERS '
    GED_VERSION_END: str = EOL
    GREATER_LESS_THAN: str = '>'
    HEAD_LINE: str = f'0 HEAD{EOL}'
    #HEADER: str = f'{HEAD_LINE}1 GEDC{EOL}2 VERS '
    HEIGHT: int = 0
    HYPHEN: str = '-'
    IGNORE: frozenset[str] = frozenset([
        'CONT',
        'TRLR',
    ])
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
    LINE_LENGTH: int = 75
    LIST_ITEM_SEPARATOR: str = ', '
    LONG_DEFAULT: float = 0.0
    LONG_EAST: str = 'E'
    LONG_HIGH: float = 180.0
    LONG_LOW: float = -180.0
    LONG_PRECISION: str = '.6f'
    LONG_WEST: str = 'W'
    MANY: str = 'Many'
    MIME: str = ''
    MONTHS: int = 0
    NO: str = 'No'
    NOID: str = 'NOID'
    NONE: str = 'None'
    OCCURRED: str = 'Y'
    ONLY_ONE: str = 'Only One'
    PARENS_LEFT: str = '('
    PARENS_RIGHT: str = ')'
    PAYLOAD_EMPTY: str = EMPTY
    PERIOD: str = '.'
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
    RECORD: str = 'record'
    EXT_RECORD_TYPE: str = 'ext'
    FAM_RECORD_TYPE: str = 'fam'
    INDI_RECORD_TYPE: str = 'indi'
    OBJE_RECORD_TYPE: str = 'obje'
    REPO_RECORD_TYPE: str = 'repo'
    SNOTE_RECORD_TYPE: str = 'snote'
    SOUR_RECORD_TYPE: str = 'sour'
    SUBM_RECORD_TYPE: str = 'subm'
    # RECORD_TYPES: frozenset[str] = frozenset([
    #     FAM_RECORD_TYPE,
    #     INDI_RECORD_TYPE,
    #     OBJE_RECORD_TYPE,
    #     REPO_RECORD_TYPE,
    #     SNOTE_RECORD_TYPE,
    #     SOUR_RECORD_TYPE,
    #     SUBM_RECORD_TYPE,
    # ])
    RECORD_CLASS: tuple[str, str, str, str, str, str, str, str, str] = (
        'Head',
        'RecordFam',
        'RecordIndi',
        'RecordObje',
        'RecordRepo',
        'RecordSnote',
        'RecordSour',
        'RecordSubm',
        'Trlr',
    )
    RECORD_TYPES: tuple[str, str, str, str, str, str, str] = (
        'FAM',
        'INDI',
        'OBJE',
        'REPO',
        'SNOTE',
        'SOUR',
        'SUBM',
    )
    SLASH: str = '/'
    SPACE: str = ' '
    SPACE_DOUBLE: str = '  '
    STAGE: str = 'stage'
    T: str = 'T'
    TAG_EXT: str = 'EXT'
    TAG_FAM: str = 'FAM'
    TAG_INDI: str = 'INDI'
    TAG_OBJE: str = 'OBJE'
    TAG_REPO: str = 'REPO'
    TAG_SNOTE: str = 'SNOTE'
    TAG_SOUR: str = 'SOUR'
    TAG_SUBM: str = 'SUBM'
    TEST_BASE: str = 'Base'
    TEST_ONE_SUB: str = 'One Sub'
    TEST_REQUIRED: str = 'Required'
    TEST_PERMITTED: str = 'Permitted'
    TEST_SINGLE: str = 'Single'
    TEST_PAYLOAD: str = 'Payload'
    TIME_HOUR: int = 0
    TIME_MIN_HOUR: int = 0
    TIME_MAX_HOUR: int = 23
    TIME_MINUTE: int = 0
    TIME_MIN_MINUTE: int = 0
    TIME_MAX_MINUTE: int = 59
    TIME_SECOND: float = 0.0
    TIME_MIN_SECOND: float = 0.0
    TIME_MAX_SECOND: float = 60.0
    TIME_UTC: bool = False
    TIME_UTC_CODE: str = 'Z'
    TOP: int = 0
    TRAILER: str = '0 TRLR'
    TRLR: str = 'TRLR'
    UNDERLINE: str = '_'
    URL_CALENDAR: str = 'calendar/standard/'
    URL_CALENDAR_PREFIX: str = 'cal-'
    URL_DATATYPE: str = 'data-type/standard/'
    URL_DATATYPE_PREFIX: str = 'type-'
    URL_ENUMERATION: str = 'enumeration/standard/'
    URL_ENUMERATION_PREFIX: str = 'enum-'
    URL_ENUMERATION_SET: str = 'enumeration-set/standard/'
    URL_ENUMERATION_SET_PREFIX: str = 'enumset-'
    URL_MONTH: str = 'month/standard/'
    URL_MONTH_PREFIX: str = 'month-'
    URL_STRUCTURE: str = 'structure/standard/'
    URL_STRUCTURE_PREFIX: str = ''
    URL_STRUCTURE_EXTENSION: str = 'structure/extension/'
    URL_STRUCTURE_EXTENSION_PREFIX: str = ''
    URL_URI: str = 'uri/exid-types/'
    URL_URI_PREFIX: str = ''
    UTF8: str = 'utf-8'
    VOID_NAME: str = 'VOID'
    VOID_POINTER: str = f'@{VOID_NAME}@'
    WEEKS: int = 0
    WIDTH: int = 0
    XREF: str = 'xref'
    XREF_FAMILY: str = 'FamilyXref'
    XREF_INDIVIDUAL: str = 'IndividualXref'
    XREF_MULTIMEDIA: str = 'MultimediaXref'
    XREF_REPOSITORY: str = 'RepositoryXref'
    XREF_SHARED_NOTE: str = 'SharedNoteXref'
    XREF_SOURCE: str = 'SourceXref'
    XREF_SUBMITTER: str = 'SubmitterXref'
    YAML_CALENDARS: str = 'calendars'
    YAML_CARDINALITY_ANY_NUMBER: str = ':M}'
    YAML_CARDINALITY_OPTIONAL: str = '{0:'
    YAML_CARDINALITY_REQUIRED: str = '{1:'
    YAML_CARDINALITY_SINGULAR: str = ':1}'
    YAML_CHANGE_CONTROLLER: str = 'change controller'
    YAML_CLASS_NAME: str = 'class name'
    YAML_CONTACT: str = 'contact'
    YAML_DIRECTIVE: str = '%YAML 1.2'
    YAML_DIRECTIVE_END_MARKER: str = '---'
    YAML_DOCUMENT_END_MARKER: str = f'{EOL}...'
    YAML_DOCUMENTATION: str = 'documentation'
    YAML_ENUMERATION_SET: str = 'enumeration set'
    YAML_ENUM_KEY: str = 'enum key'
    YAML_ENUM_TAGS: str = 'enum tags'
    YAML_ENUMERATION_VALUES: str = 'enumeration values'
    YAML_EPOCHS: str = 'epochs'
    YAML_EXTENSION_TAGS: str = 'extension tags'
    YAML_FILE_END: str = '.yaml'
    YAML_FRAGMENT: str = 'fragment'
    YAML_HELP_TEXT: str = 'help text'
    YAML_KEY: str = 'key'
    YAML_LABEL: str = 'label'
    YAML_LANG: str = 'lang'
    YAML_LOAD_FILE: str = 'load file'
    YAML_LOAD_TAG: str = 'load tag'
    YAML_META: str = 'meta'
    YAML_MONTHS: str = 'months'
    YAML_PAYLOAD: str = 'payload'
    YAML_PERMITTED: str = 'permitted'
    YAML_PERMITTED_KEY: str = 'permitted key'
    YAML_REQUIRED: str = 'required'
    YAML_SOURCE: str = 'source'
    YAML_SINGULAR: str = 'single'
    YAML_SPECIFICATION: str = 'specification'
    YAML_STANDARD_TAG: str = 'standard tag'
    YAML_SUBSTRUCTURES: str = 'substructures'
    YAML_SUPERSTRUCTURES: str = 'superstructures'
    YAML_TYPE: str = 'type'
    YAML_TYPE_CALENDAR: str = 'calendar'
    YAML_TYPE_DATATYPE: str = 'data type'
    YAML_TYPE_ENUMERATION: str = 'enumeration'
    YAML_TYPE_ENUMERATION_SET: str = 'enumeration set'
    YAML_TYPE_MONTH: str = 'month'
    YAML_TYPE_STRUCTURE: str = 'structure'
    YAML_TYPE_URI: str = 'uri'
    YAML_TYPE_CODES: frozenset[str] = frozenset(
        [
            YAML_TYPE_CALENDAR,
            YAML_TYPE_DATATYPE,
            YAML_TYPE_ENUMERATION,
            YAML_TYPE_ENUMERATION_SET,
            YAML_TYPE_MONTH,
            YAML_TYPE_STRUCTURE,
            YAML_TYPE_URI,
        ]
    )
    YAML_TAG_TYPES: frozenset[str] = frozenset(
        [
            'calendar',
            'enumeration',
            'month',
            'structure',
        ]
    )
    YAML_URI: str = 'uri'
    YAML_VALUE_OF: str = 'value of'
    YAML_VERSION: str = 'version'
    YAML_WITH_HYPHEN: str = '\n    > - '
    YAML_WITHOUT_HYPHEN: str = '\n    >   '
    YEARS: int = 0
    YES: str = 'Yes'
    Z: str = 'Z'


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
    # EMPTY: str = ''
    EPOCH: str = 'Epoch'
    EXPERIMENT: str = 'EXPERIMENT'
    GREGORIAN: str = 'GREGORIAN'
    ISO: str = 'ISO'
    MAX_MONTHS: str = 'Max Months'
    MONTH_NAMES: str = 'Month Names'
    MONTH_MAX_DAYS: str = 'Month Max Days'
    SECULAR: str = 'SECULAR'


class CalendarName(Enum):
    """Names of recognized calendars.

    Reference:
        - [Date](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
    """

    GREGORIAN = 'GREGORIAN'
    JULIAN = 'JULIAN'
    FRENCH_R = 'FRENCH_R'
    HEBREW = 'HEBREW'
    NONE = 'NONE'


class Cal:
    """GEDCOM codes for various calendars."""

    CALENDARS: ClassVar = {
        CalendarName.HEBREW: {
            Value.MAX_MONTHS: 13,
            Value.MONTH_NAMES: {
                '01': 'TSH',
                '02': 'CSH',
                '03': 'KSL',
                '04': 'TVT',
                '05': 'SHV',
                '06': 'ADR',
                '07': 'ADS',
                '08': 'NSN',
                '09': 'IYR',
                '10': 'SVN',
                '11': 'TMZ',
                '12': 'AAV',
                '13': 'ELL',
            },
            Value.ISO: {
                'TSH': '09',
                'CSH': '02',
                'KSL': '03',
                'TVT': '04',
                'SHV': '05',
                'ADR': '06',
                'ADS': '07',
                'NSN': '08',
                'IYR': '09',
                'SVN': '10',
                'TMZ': '11',
                'AAV': '12',
                'ELL': '13',
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
            Value.EPOCH: '',
        },
        CalendarName.GREGORIAN: {
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
            Value.EPOCH: 'BCE',
        },
        CalendarName.JULIAN: {
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
            Value.EPOCH: 'BCE',
        },
        CalendarName.FRENCH_R: {
            Value.MAX_MONTHS: 13,
            Value.MONTH_NAMES: {
                '01': 'VEND',
                '02': 'BRUM',
                '03': 'FRIM',
                '04': 'NIVO',
                '05': 'PLUV',
                '06': 'VENT',
                '07': 'GERM',
                '08': 'FLOR',
                '09': 'PRAI',
                '10': 'MESS',
                '11': 'THER',
                '12': 'FRUC',
                '13': 'COMP',
            },
            Value.ISO: {
                'VEND': '10',
                'BRUM': '11',
                'FRIM': '12',
                'NIVO': '01',
                'PLUV': '02',
                'VENT': '03',
                'GERM': '04',
                'FLOR': '05',
                'PRAI': '06',
                'MESS': '07',
                'THER': '08',
                'FRUC': '09',
                'COMP': '09',
            },
            Value.MONTH_MAX_DAYS: {
                '01': 30,
                '02': 30,
                '03': 30,
                '04': 30,
                '05': 30,
                '06': 30,
                '07': 30,
                '08': 30,
                '09': 30,
                '10': 30,
                '11': 30,
                '12': 30,
                '13': 5,
            },
            Value.EPOCH: '',
        },
    }


# @dataclass(frozen=True)
# class Number:
#     CSVLEN: int = 4
#     GEDLEN: int = 4
#     GRAMPSLEN: int = 7
#     JSONLEN: int = 5


@dataclass(frozen=True)
class String:
    """The following values are part of the configuration of the GEDCOM standard
    or the Geography package.  They are not part of messages to the user
    and so do not require internationalization.
    """

    # ATSIGN: str = '@'
    # BANNED: str = r'[\u0000-\u001F\u007F\uD800-\uDFFF\uFFFE\uFFFF]'
    BC: str = 'BCE'
    # COLON: str = ':'
    # COMMA: str = ','
    CSV: str = '.csv'
    # DAY: str = 'd'
    # DOUBLE_NEWLINE: str = '\n\n'
    EMPTY: str = ''
    # EOL: str = '\n'
    # EVENT: str = 'EVENT'
    # FORM_DEFAULT1: str = 'City'
    # FORM_DEFAULT2: str = 'County'
    # FORM_DEFAULT3: str = 'State'
    # FORM_DEFAULT4: str = 'Country'
    FRENCH_R: str = 'FRENCH_R'
    GED: str = '.ged'
    GRAMPS: str = '.gramps'
    # GREATER_THAN: str = '>'
    GREGORIAN: str = 'GREGORIAN'
    HEBREW: str = 'HEBREW'
    # HYPHEN: str = '-'
    # INDENT: str = '    '
    # INDEX: str = 'index'
    INT: str = 'int'
    JSON: str = '.json'
    JULIAN: str = 'JULIAN'
    # LEFT_BRACKET: str = '['
    # LEFT_RIGHT_BRACKET: str = '[]'
    # LEFT_RIGHT_BRACKET_REQUIRED: str = '[]  <- REQUIRED'
    # LIST_ITEM_SEPARATOR: str = ', '
    MONTH: str = 'm'
    MONTH_NAMES: str = 'Month Names'
    NEGATIVE: str = '-'
    NOW: str = 'now'
    # OCCURRED: Literal['Y'] = 'Y'
    # MAX = 'MAX'
    # MIN = 'MIN'
    READ: str = 'r'
    # REQUIRED: str = '  <- REQUIRED'
    # RIGHT_BRACKET: str = ']'
    # SLASH: str = '/'
    # SPACE: str = ' '
    # T: str = 'T'
    # UNDERLINE: str = '_'
    # UNDETERMINED: str = 'und'
    # VERSION: str = '7.0'
    WRITE: str = 'w'
    # Z: str = 'Z'


class GedFlag:
    """These strings signal special processing for the ged methods.

    The GedFlag constants contain the name of NamedTuple class as the first part of their names
    to help locate them.  The second part of their names contain a description of
    the function they are signalling to occur.

    """

    PLACENAME_FULL: Literal['F'] = 'F'
    PLACENAME_SHORT: Literal['S'] = 'S'
    PLACENAME_TRANSLATION: Literal['T'] = 'T'


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


class ApproxDate(Enum):
    """Enumeration values for date approximations.

    Reference:
        - [Date](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#date)
    """

    ABT = 'ABT'
    CAL = 'CAL'
    EST = 'EST'
    NONE = ''


# class Event(Enum):
#     """Tags for events."""

#     ADOP = 'ADOP'
#     ANUL = 'ANUL'
#     BAPM = 'BAPM'
#     BARM = 'BARM'
#     BASM = 'BASM'
#     BIRT = 'BIRT'
#     BLES = 'BLES'
#     BURI = 'BURI'
#     CENS = 'CENS'
#     CHR = 'CHR'
#     CHRA = 'CHRA'
#     CONF = 'CONF'
#     CREM = 'CREM'
#     DEAT = 'DEAT'
#     DIV = 'DIV'
#     DIVF = 'DIVF'
#     EMIG = 'EMIG'
#     ENGA = 'ENGA'
#     EVEN = 'EVEN'
#     FCOM = 'FCOM'
#     GRAD = 'GRAD'
#     IMMI = 'IMMI'
#     MARB = 'MARB'
#     MARC = 'MARC'
#     MARL = 'MARL'
#     MARR = 'MARR'
#     MARS = 'MARS'
#     NATU = 'NATU'
#     ORDN = 'ORDN'
#     PROB = 'PROB'
#     RETI = 'RETI'
#     WILL = 'WILL'
#     NONE = String.EMPTY


class GreaterLessThan(Enum):
    GREATER = '>'
    LESS = '<'
    NONE = ''


class Latitude(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    NONE = String.EMPTY


class Longitude(Enum):
    EAST = 'E'
    WEST = 'W'
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


# class MediaType(Enum):
#     """"""

#     TEXT_HTML = 'TEXT_HTML'
#     TEXT_PLAIN = 'TEXT_PLAIN'
#     NONE = String.EMPTY


# class Tag(Enum):
#     """Enumerate all of the standard tags signalling structure types in the GEDCOM specification."""

#     ABBR = 'ABBR'
#     ADDR = 'ADDR'
#     ADOP = 'ADOP'
#     ADR1 = 'ADR1'
#     ADR2 = 'ADR2'
#     ADR3 = 'ADR3'
#     AGE = 'AGE'
#     AGNC = 'AGNC'
#     ALIA = 'ALIA'
#     ANCI = 'ANCI'
#     ANUL = 'ANUL'
#     ASSO = 'ASSO'
#     AUTH = 'AUTH'
#     BAPL = 'BAPL'
#     BAPM = 'BAPM'
#     BARM = 'BARM'
#     BASM = 'BASM'
#     BIRT = 'BIRT'
#     BLES = 'BLES'
#     BURI = 'BURI'
#     CALN = 'CALN'
#     CAST = 'CAST'
#     CAUS = 'CAUS'
#     CENS = 'CENS'
#     CHAN = 'CHAN'
#     CHIL = 'CHIL'
#     CHR = 'CHR'
#     CHRA = 'CHRA'
#     CITY = 'CITY'
#     CONF = 'CONF'
#     CONL = 'CONL'
#     CONT = 'CONT'
#     COPR = 'COPR'
#     CORP = 'CORP'
#     CREA = 'CREA'
#     CREM = 'CREM'
#     CROP = 'CROP'
#     CTRY = 'CTRY'
#     DATA = 'DATA'
#     DATE = 'DATE'
#     DEAT = 'DEAT'
#     DESI = 'DESI'
#     DEST = 'DEST'
#     DIV = 'DIV'
#     DIVF = 'DIVF'
#     DSCR = 'DSCR'
#     EDUC = 'EDUC'
#     EMAIL = 'EMAIL'
#     EMIG = 'EMIG'
#     ENDL = 'ENDL'
#     ENGA = 'ENGA'
#     EVEN = 'EVEN'
#     EXID = 'EXID'
#     FACT = 'FACT'
#     FAM = 'FAM'
#     FATH = 'FATH'
#     FAMC = 'FAMC'
#     FAMS = 'FAMS'
#     FAX = 'FAX'
#     FCOM = 'FCOM'
#     FILE = 'FILE'
#     FILM = 'FILM'
#     FORM = 'FORM'
#     FRENCH_R = 'FRENCH_R'
#     GEDC = 'GEDC'
#     GIVN = 'GIVN'
#     GRAD = 'GRAD'
#     GREGORIAN = 'GREGORIAN'
#     HEAD = 'HEAD'
#     HEBREW = 'HEBREW'
#     HEIGHT = 'HEIGHT'
#     HUSB = 'HUSB'
#     IDNO = 'IDNO'
#     IMMI = 'IMMI'
#     INDI = 'INDI'
#     INIL = 'INIL'
#     JULIAN = 'JULIAN'
#     LANG = 'LANG'
#     LANG_ = '_LANG'
#     LATI = 'LATI'
#     LEFT = 'LEFT'
#     LONG = 'LONG'
#     MAP = 'MAP'
#     MARB = 'MARB'
#     MARC = 'MARC'
#     MARL = 'MARL'
#     MARR = 'MARR'
#     MARS = 'MARS'
#     MEDI = 'MEDI'
#     MIME = 'MIME'
#     NAME = 'NAME'
#     NATI = 'NATI'
#     NATU = 'NATU'
#     NCHI = 'NCHI'
#     NICK = 'NICK'
#     NMR = 'NMR'
#     NO = 'NO'
#     NOTE = 'NOTE'
#     NPFX = 'NPFX'
#     NSFX = 'NSFX'
#     OBJE = 'OBJE'
#     OCCU = 'OCCU'
#     ORDN = 'ORDN'
#     PAGE = 'PAGE'
#     PEDI = 'PEDI'
#     PHON = 'PHON'
#     PHRASE = 'PHRASE'
#     PLAC = 'PLAC'
#     POST = 'POST'
#     PROB = 'PROB'
#     PROP = 'PROP'
#     PUBL = 'PUBL'
#     QUAY = 'QUAY'
#     REFN = 'REFN'
#     RELI = 'RELI'
#     REPO = 'REPO'
#     RESI = 'RESI'
#     RESN = 'RESN'
#     RETI = 'RETI'
#     ROLE = 'ROLE'
#     SCHMA = 'SCHMA'
#     SDATE = 'SDATE'
#     SEX = 'SEX'
#     SLGC = 'SLGC'
#     SLGS = 'SLGS'
#     SNOTE = 'SNOTE'
#     SOUR = 'SOUR'
#     SPFX = 'SPFX'
#     SPOU = 'SPOU'
#     SSN = 'SSN'
#     STAE = 'STAE'
#     STAT = 'STAT'
#     SUBM = 'SUBM'
#     SURN = 'SURN'
#     TAG = 'TAG'
#     TEMP = 'TEMP'
#     TEXT = 'TEXT'
#     TIME = 'TIME'
#     TITL = 'TITL'
#     TOP = 'TOP'
#     TRAN = 'TRAN'
#     TRLR = 'TRLR'
#     TYPE = 'TYPE'
#     UID = 'UID'
#     VERS = 'VERS'
#     WIDTH = 'WIDTH'
#     WIFE = 'WIFE'
#     WILL = 'WILL'
#     WWW = 'WWW'
#     NONE = String.EMPTY


# class FamAttr(Enum):
#     """Tags used for family attributes.

#     This is a sub-enumeration of the Tag enumeration class.

#     Reference:
#         [GEDCOM INDIEVEN]()
#     """

#     NCHI = Tag.NCHI.value
#     RESI = Tag.RESI.value
#     FACT = Tag.FACT.value
#     NONE = String.EMPTY


# class FamEven(Enum):
#     """Tags used for family events.

#     This is a sub-enumeration of the Tag enumeration class.

#     Reference:
#         [GEDCOM FAMC-EVEN](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html#family-events)
#     """

#     ANUL = Tag.ANUL.value
#     CENS = Tag.CENS.value
#     DIV = Tag.DIV.value
#     DIVF = Tag.DIVF.value
#     ENGA = Tag.ENGA.value
#     MARB = Tag.MARB.value
#     MARC = Tag.MARC.value
#     MARL = Tag.MARL.value
#     MARR = Tag.MARR.value
#     MARS = Tag.MARS.value
#     EVEN = Tag.EVEN.value
#     NONE = String.EMPTY


# class Id(Enum):
#     """Tags used for identifier values.

#     This is a sub-enumeration of the Tag enumeration class.

#     Reference:
#         [GEDCOM Identifiers]()
#     """

#     REFN = Tag.REFN.value
#     UID = Tag.UID.value
#     EXID = Tag.EXID.value
#     NONE = String.EMPTY


# class IndiAttr(Enum):
#     """Tags used for individual attributes.

#     This is a sub-enumeration of the Tag enumeration class.

#     Reference:
#         [GEDCOM INDIEVEN]()
#     """

#     CAST = Tag.CAST.value
#     DSCR = Tag.DSCR.value
#     EDUC = Tag.EDUC.value
#     IDNO = Tag.IDNO.value
#     NATI = Tag.NATI.value
#     NCHI = Tag.NCHI.value
#     NMR = Tag.NMR.value
#     OCCU = Tag.OCCU.value
#     PROP = Tag.PROP.value
#     RELI = Tag.RELI.value
#     RESI = Tag.RESI.value
#     SSN = Tag.SSN.value
#     TITL = Tag.TITL.value
#     FACT = Tag.FACT.value
#     NONE = String.EMPTY


# class IndiEven(Enum):
#     """Tags used for individual events.

#     This is a sub-enumeration of the Tag enumeration class.

#     Reference:
#         [GEDCOM INDIEVEN]()
#     """

#     ADOP = Tag.ADOP.value
#     BAPM = Tag.BAPM.value
#     BARM = Tag.BARM.value
#     BASM = Tag.BASM.value
#     BIRT = Tag.BIRT.value
#     BLES = Tag.BLES.value
#     BURI = Tag.BURI.value
#     CENS = Tag.CENS.value
#     CHR = Tag.CHR.value
#     CHRA = Tag.CHRA.value
#     CONF = Tag.CONF.value
#     CREM = Tag.CREM.value
#     DEAT = Tag.DEAT.value
#     EMIG = Tag.EMIG.value
#     FCOM = Tag.FCOM.value
#     GRAD = Tag.GRAD.value
#     IMMI = Tag.IMMI.value
#     NATU = Tag.NATU.value
#     ORDN = Tag.ORDN.value
#     PROB = Tag.PROB.value
#     RETI = Tag.RETI.value
#     WILL = Tag.WILL.value
#     EVEN = Tag.EVEN.value
#     NONE = String.EMPTY


# class PersonalNamePieceTag(Enum):
#     """Tags used for Personal Name Piece lines.

#     This is a subenumeration of the Tag enumeration class.

#     Reference:
#         [GEDCOM]()
#     """

#     NPFX = Tag.NPFX.value
#     GIVN = Tag.GIVN.value
#     NICK = Tag.NICK.value
#     SPFX = Tag.SPFX.value
#     SURN = Tag.SURN.value
#     NSFX = Tag.NSFX.value
#     NONE = String.EMPTY


# class Record(str, Enum):
#     """Tags used for Records.

#     This is a subenumeration of the Tag enumeration class.

#     Reference:
#         [GEDCOM RECORD]()
#     """

#     FAM = Tag.FAM.value
#     INDI = Tag.INDI.value
#     OBJE = Tag.OBJE.value
#     REPO = Tag.REPO.value
#     SNOTE = Tag.SNOTE.value
#     SOUR = Tag.SOUR.value
#     SUBM = Tag.SUBM.value
#     NONE = String.EMPTY


# class LineVal(Enum):
#     """Fixed values that may be used in the LineVal position of a line.

#     Some of these values may be identical to Tag values, but in this implementation
#     they are separate from Tag.  For example, even though there is a Tag.HUSB
#     definition that may be used in the Tag position of a GEDCOM line there is
#     also a LineVal.HUSB definition that may only be used in the LineVal of a
#     GEDCOM line.

#     Reference:
#         [GEDCOM LineVal Definitions]()
#     """

#     ADOPTED = 'ADOPTED'
#     AKA = 'AKA'
#     AUDIO = 'AUDIO'
#     BIC = 'BIC'
#     BIRTH = 'BIRTH'
#     BOOK = 'BOOK'
#     BOTH = 'BOTH'
#     CANCELED = 'CANCELED'
#     CARD = 'CARD'
#     CHALLENGED = 'CHALLENGED'
#     CHIL = 'CHIL'
#     CHILD = 'CHILD'
#     CLERGY = 'CLERGY'
#     COMPLETED = 'COMPLETED'
#     CONFIDENTIAL = 'CONFIDENTIAL'
#     DISPROVEN = 'DISPROVEN'
#     DNS = 'DNS'
#     DNS_CAN = 'DNS_CAN'
#     ELECTRONIC = 'ELECTRONIC'
#     EXCLUDED = 'EXCLUDED'
#     F = 'F'
#     FATH = 'FATH'
#     FICHE = 'FICHE'
#     FILM = 'FILM'
#     FOSTER = 'FOSTER'
#     FRIEND = 'FRIEND'
#     GODP = 'GODP'
#     HUSB = 'HUSB'
#     IMMIGRANT = 'IMMIGRANT'
#     INFANT = 'INFANT'
#     LOCKED = 'LOCKED'
#     MAGAZINE = 'MAGAZINE'
#     MAIDEN = 'MAIDEN'
#     MANUSCRIPT = 'MANUSCRIPT'
#     M = 'M'
#     MAP = 'MAP'
#     MARRIED = 'MARRIED'
#     MOTH = 'MOTH'
#     MULTIPLE = 'MULTIPLE'
#     NEWSPAPER = 'NEWSPAPER'
#     NGHBR = 'NGHBR'
#     OFFICIATOR = 'OFFICIATOR'
#     OTHER = 'OTHER'
#     PARENT = 'PARENT'
#     PHOTO = 'PHOTO'
#     PRE_1970 = 'PRE_1970'
#     PRIVACY = 'PRIVACY'
#     PROFESSIONAL = 'PROFESSIONAL'
#     PROVEN = 'PROVEN'
#     QUAY0 = '0'
#     QUAY1 = '1'
#     QUAY2 = '2'
#     QUAY3 = '3'
#     SEALING = 'SEALING'
#     SPOU = 'SPOU'
#     STILLBORN = 'STILLBORN'
#     SUBMITTED = 'SUBMITTED'
#     TOMBSTONE = 'TOMBSTONE'
#     U = 'U'
#     UNCLEARED = 'UNCLEARED'
#     VIDEO = 'VIDEO'
#     WIFE = 'WIFE'
#     WITN = 'WITN'
#     X = 'X'


# class Adop(Enum):
#     """Implement the GEDCOM enumeration set ADOP as an enumeration class.

#     Reference:
#         - [GEDCOM Adop Enumeration](https://gedcom.io/terms/v7/enumset-ADOP)
#     """

#     HUSB = LineVal.HUSB.value
#     WIFE = LineVal.WIFE.value
#     BOTH = LineVal.BOTH.value
#     NONE = String.EMPTY


# class EvenAttr(Enum):
#     """Implement the GEDCOM enumeration set EVENATTR as an enumeration class.

#     Reference:
#         [GEDCOM EVENATTR enumeration set](https://gedcom.io/terms/v7/enumset-EVENATTR)
#     """

#     CENS = 'CENS'
#     NCHI = 'NCHI'
#     RESI = 'RESI'
#     FACT = 'FACT'
#     EVEN = 'EVEN'
#     NONE = String.EMPTY


# class FamcStat(Enum):
#     """Implement the GEDCOM enumeration set FAMC-STAT as an enumeration class.

#     Reference:
#         [GEDCOM FAMC-STAT](https://gedcom.io/terms/v7/enumset-FAMC-STAT)
#     """

#     CHALLENGED = LineVal.CHALLENGED.value
#     DISPROVEN = LineVal.DISPROVEN.value
#     PROVEN = LineVal.PROVEN
#     NONE = String.EMPTY


# class Medium(Enum):
#     """Implement the GEDCOM enumeration set MEDI as an enumeration class.

#     Reference:
#         [GEDCOM MEDI enumeration set](https://gedcom.io/terms/v7/enumset-MEDI)
#     """

#     AUDIO = LineVal.AUDIO.value
#     BOOK = LineVal.BOOK.value
#     CARD = LineVal.CARD.value
#     ELECTRONIC = LineVal.ELECTRONIC.value
#     FICHE = LineVal.FICHE.value
#     FILM = LineVal.FILM.value
#     MAGAZINE = LineVal.MAGAZINE.value
#     MANUSCRIPT = LineVal.MANUSCRIPT.value
#     MAP = LineVal.MAP.value
#     NEWSPAPER = LineVal.NEWSPAPER.value
#     PHOTO = LineVal.PHOTO.value
#     TOMBSTONE = LineVal.TOMBSTONE.value
#     VIDEO = LineVal.VIDEO.value
#     OTHER = LineVal.OTHER.value
#     NONE = String.EMPTY


# class NameType(Enum):
#     """Implement the GEDCOM enumeration set NAME-TYPE as an eneration class.

#     Reference:
#         [GEDCOM NAME-TYPE enumeration set](https://gedcom.io/terms/v7/enumset-NAME-TYPE)
#     """

#     AKA = LineVal.AKA.value
#     BIRTH = LineVal.BIRTH.value
#     IMMIGRANT = LineVal.IMMIGRANT.value
#     MAIDEN = LineVal.MAIDEN.value
#     MARRIED = LineVal.MARRIED.value
#     PROFESSIONAL = LineVal.PROFESSIONAL.value
#     OTHER = LineVal.OTHER.value
#     NONE = String.EMPTY


# class Pedi(Enum):
#     """Implement the GEDCOM enumeration set PEDI as an enumeration class.

#     Reference:
#         [GEDCOM PEDI enumeration set](https://gedcom.io/terms/v7/enumset-PEDI)
#     """

#     ADOPTED = LineVal.ADOPTED.value
#     BIRTH = LineVal.BIRTH.value
#     FOSTER = LineVal.FOSTER.value
#     SEALING = LineVal.SEALING.value
#     OTHER = LineVal.OTHER.value
#     NONE = String.EMPTY


# class Quay(Enum):
#     """Implement the GEDCOM enumeration set QUAY as an enumeration class.

#     Reference:
#         [GEDCOM QUAY enumeration set](https://gedcom.io/terms/v7/enumset-QUAY)
#     """

#     QUAY0 = LineVal.QUAY0.value
#     QUAY1 = LineVal.QUAY1.value
#     QUAY2 = LineVal.QUAY2.value
#     QUAY3 = LineVal.QUAY3.value
#     NONE = String.EMPTY


# class Resn(Enum):
#     """Implement the GEDCOM enumeration set RESN as an enumeration class.

#     Reference:
#         [GEDCOM RESN enumeration set](https://gedcom.io/terms/v7/enumset-RESN)
#     """

#     CONFIDENTIAL = LineVal.CONFIDENTIAL.value
#     LOCKED = LineVal.LOCKED.value
#     PRIVACY = LineVal.PRIVACY.value
#     NONE = String.EMPTY


# class Role(Enum):
#     """Implement the GEDCOM enumeration set ROLE as an enumeration class.

#     Reference:
#         [GEDCOM ROLE enumeration set](https://gedcom.io/terms/v7/enumset-ROLE)
#     """

#     CHIL = LineVal.CHIL.value
#     CLERGY = LineVal.CLERGY.value
#     FATH = LineVal.FATH.value
#     FRIEND = LineVal.FRIEND.value
#     GODP = LineVal.GODP.value
#     HUSB = LineVal.HUSB.value
#     MOTH = LineVal.MOTH.value
#     MULTIPLE = LineVal.MULTIPLE.value
#     NGHBR = LineVal.NGHBR.value
#     OFFICIATOR = LineVal.OFFICIATOR.value
#     PARENT = LineVal.PARENT.value
#     SPOU = LineVal.SPOU.value
#     WIFE = LineVal.WIFE.value
#     WITN = LineVal.WITN.value
#     OTHER = LineVal.OTHER.value
#     NONE = String.EMPTY


# class Sex(Enum):
#     """Implement the GEDCOM SEX enumeration set as an enumeration class.

#     Reference:
#         [GEDCOM SEX enumeration set]()
#     """

#     M = LineVal.M.value
#     F = LineVal.F.value
#     X = LineVal.X.value
#     U = LineVal.U.value
#     NONE = String.EMPTY


# class Stat(Enum):
#     """Implement the GEDCOM enumeration set ord-STAT as an enumeration class.

#     Reference:
#         [GEDCOM ord-STAT enumeration set](https://gedcom.io/terms/v7/enumset-ord-STAT)
#     """

#     BIC = LineVal.BIC.value
#     CANCELED = LineVal.CANCELED.value
#     CHILD = LineVal.CHILD.value
#     COMPLETED = LineVal.COMPLETED.value
#     EXCLUDED = LineVal.EXCLUDED.value
#     DNS = LineVal.DNS.value
#     DNS_CAN = LineVal.DNS_CAN.value
#     INFANT = LineVal.INFANT.value
#     PRE_1970 = LineVal.PRE_1970.value
#     STILLBORN = LineVal.STILLBORN.value
#     SUBMITTED = LineVal.SUBMITTED.value
#     UNCLEARED = LineVal.UNCLEARED.value
#     NONE = String.EMPTY
