# Licensed under a 3-clause BSD style license - see LICENSE.md
"""This module provides a namespace for typed constants."""

from dataclasses import dataclass
from typing import ClassVar, Literal


@dataclass(frozen=True)
class Arg:
    """The following constants are used as arguments to procedure calls
    such as Pandas DataFrames or NumPy."""

    CSV: str = '.csv'
    CSVLEN: int = 4
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
    EPOCH: str = 'Epoch'
    EXPERIMENT: str = 'EXPERIMENT'
    GREGORIAN: str = 'GREGORIAN'
    MAX_MONTHS: str = 'Max Months'
    MONTH_NAMES: str = 'Month Names'
    MONTH_MAX_DAYS: str = 'Month Max Days'
    SECULAR: str = 'SECULAR'

class Cal:
    """GEDCOM Month codes for various calendars."""

    CALENDARS: ClassVar = {
        Value.GREGORIAN: {
            Value.MAX_MONTHS : 12,
            Value.MONTH_NAMES : {
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
            Value.EPOCH: ' BCE'
        }
    }


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
